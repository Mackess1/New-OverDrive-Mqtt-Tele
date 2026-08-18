from __future__ import annotations

import logging
from typing import Any

from homeassistant.components import mqtt

from .const import CONF_TELEMETRY_TOPIC, DEFAULT_TELEMETRY_TOPIC

_LOGGER = logging.getLogger(__name__)


def command_topic(entry, key: str, sub: str | None = None) -> str:
    """Build the official OverDrive MQTT vehicle-control topic.

    OverDrive subscribes to:
      <base>/<key>/set
      <base>/<key>/<sub>/set

    where <base> is the configured telemetry base topic.
    """
    base = entry.data.get(CONF_TELEMETRY_TOPIC, DEFAULT_TELEMETRY_TOPIC).rstrip("/")
    if sub:
        return f"{base}/{key}/{sub}/set"
    return f"{base}/{key}/set"


async def async_send_control(hass, entry, key: str, payload: Any, sub: str | None = None) -> None:
    topic = command_topic(entry, key, sub)
    value = str(payload)
    _LOGGER.debug("OverDrive control: %s <- %s", topic, value)
    # OverDrive explicitly rejects retained control commands. Keep retain=False.
    await mqtt.async_publish(hass, topic, value, qos=0, retain=False)
