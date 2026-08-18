from __future__ import annotations

import json
import logging
from typing import Any

from homeassistant.components import mqtt
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import (
    DOMAIN,
    CONF_TELEMETRY_TOPIC,
    CONF_AVAILABILITY_TOPIC,
    CONF_CONTROL_TOPIC,
    DEFAULT_TELEMETRY_TOPIC,
    DEFAULT_AVAILABILITY_TOPIC,
    DEFAULT_CONTROL_TOPIC,
)

_LOGGER = logging.getLogger(__name__)


class OverdriveBYDCoordinator(DataUpdateCoordinator):
    """Receive OverDrive telemetry from MQTT.

    OverDrive has used two telemetry layouts:
      1. Legacy: one JSON object on ``<base>``.
      2. Current: one value per ``<base>/<key>`` topic.

    Supporting both keeps existing installs working while correctly handling
    current OverDrive MQTT publishing / Home Assistant discovery behaviour.
    """

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        super().__init__(hass, _LOGGER, name=DOMAIN)

        self.entry = entry
        self.telemetry_topic = entry.data.get(
            CONF_TELEMETRY_TOPIC,
            DEFAULT_TELEMETRY_TOPIC,
        ).rstrip("/")
        self.availability_topic = entry.data.get(
            CONF_AVAILABILITY_TOPIC,
            DEFAULT_AVAILABILITY_TOPIC,
        ).rstrip("/")
        self.control_topic = entry.data.get(
            CONF_CONTROL_TOPIC,
            DEFAULT_CONTROL_TOPIC,
        ).rstrip("/")
        self.control_test_topic = f"overdrive_byd/{entry.entry_id}/control_test"

        self.data: dict[str, Any] = {}
        self.available = False
        self._unsub_telemetry: list[Any] = []
        self._unsub_availability = None
        self._unsub_control_test = None

    async def async_setup(self) -> None:
        # Legacy aggregate JSON payload.
        self._unsub_telemetry.append(
            await mqtt.async_subscribe(
                self.hass,
                self.telemetry_topic,
                self._message_received,
                qos=0,
            )
        )

        # Current OverDrive format: <base>/<key> with one value per topic.
        # Use '+' instead of '#' so command topics such as
        # <base>/climate/mode/set are not mistaken for telemetry.
        self._unsub_telemetry.append(
            await mqtt.async_subscribe(
                self.hass,
                f"{self.telemetry_topic}/+",
                self._message_received,
                qos=0,
            )
        )

        self._unsub_availability = await mqtt.async_subscribe(
            self.hass,
            self.availability_topic,
            self._availability_received,
            qos=0,
        )

        # Local broker-loopback diagnostic. This does not send anything to
        # the vehicle. The MQTT Discovery test button publishes here; seeing
        # this callback proves Home Assistant -> broker -> integration works.
        self._unsub_control_test = await mqtt.async_subscribe(
            self.hass,
            self.control_test_topic,
            self._control_test_received,
            qos=0,
        )

    async def async_unsubscribe(self) -> None:
        for unsub in self._unsub_telemetry:
            if unsub:
                unsub()
        self._unsub_telemetry.clear()

        if self._unsub_availability:
            self._unsub_availability()
            self._unsub_availability = None

        if self._unsub_control_test:
            self._unsub_control_test()
            self._unsub_control_test = None
        self._unsub_control_test = None

    @staticmethod
    def _decode_payload(payload: Any) -> Any:
        """Decode MQTT payloads safely.

        Home Assistant normally supplies MQTT payloads as strings, but bytes
        are accepted too so numeric telemetry never becomes a value such as
        ``b\'30\'``. JSON numbers, booleans, objects and arrays are decoded;
        ordinary text is returned unchanged.
        """
        if isinstance(payload, bytes):
            try:
                text = payload.decode("utf-8")
            except UnicodeDecodeError:
                text = payload.decode("utf-8", errors="replace")
        else:
            text = str(payload)

        text = text.strip()
        try:
            return json.loads(text)
        except (json.JSONDecodeError, TypeError):
            return text

    @callback
    def _message_received(self, msg) -> None:
        topic = str(msg.topic).rstrip("/")

        # Availability is also one level below the telemetry base in the
        # default configuration, so ignore it here; its dedicated callback
        # handles online/offline state.
        if topic == self.availability_topic.rstrip("/"):
            return

        payload = self._decode_payload(msg.payload)

        if topic == self.telemetry_topic:
            # Backwards-compatible aggregate payload.
            if not isinstance(payload, dict):
                _LOGGER.warning(
                    "Overdrive BYD aggregate payload is not a JSON object: %s",
                    msg.payload,
                )
                return
            self.data.update(payload)
        else:
            prefix = f"{self.telemetry_topic}/"
            if not topic.startswith(prefix):
                return

            key = topic[len(prefix):]
            if not key or "/" in key:
                return

            # Current OverDrive publishes GPS as a location object:
            # {"latitude": ..., "longitude": ...}.  The tracker entity uses
            # the historical lat/lon keys, so normalize it here.
            if key == "location" and isinstance(payload, dict):
                latitude = payload.get("latitude", payload.get("lat"))
                longitude = payload.get("longitude", payload.get("lon"))
                if latitude is not None:
                    self.data["lat"] = latitude
                if longitude is not None:
                    self.data["lon"] = longitude
                self.data["location"] = payload
            else:
                self.data[key] = payload

            # Some OverDrive builds expose the vehicle distance using the
            # ev_mileage_km field rather than odometer. Only use it as a
            # fallback when it is a plausible value; placeholder values are
            # filtered later by clean_value().
            if key == "ev_mileage_km" and "odometer" not in self.data:
                self.data["odometer"] = payload

        self.available = True
        self.async_set_updated_data(dict(self.data))


    @callback
    def _control_test_received(self, msg) -> None:
        """Record a local MQTT round-trip from the diagnostic button."""
        payload = self._decode_payload(msg.payload)
        self.data["control_test"] = f"received: {payload}"
        self.async_set_updated_data(dict(self.data))

    @callback
    def _availability_received(self, msg) -> None:
        """Handle optional OverDrive availability without masking live data.

        Different OverDrive/MQTT setups may publish ``online``/``offline``,
        booleans, or 1/0.  An unknown availability payload must not make the
        whole vehicle unavailable when telemetry is actively arriving.
        """
        payload = self._decode_payload(msg.payload)

        if isinstance(payload, bool):
            self.available = payload
        elif isinstance(payload, (int, float)):
            self.available = payload != 0
        else:
            status = str(payload).strip().lower()
            if status in {"online", "on", "true", "1", "available", "connected"}:
                self.available = True
            elif status in {"offline", "off", "false", "0", "unavailable", "disconnected"}:
                # Only mark it offline when OverDrive explicitly says so.
                self.available = False
            else:
                _LOGGER.debug("Ignoring unknown OverDrive availability payload: %r", payload)
                return

        self.async_update_listeners()
