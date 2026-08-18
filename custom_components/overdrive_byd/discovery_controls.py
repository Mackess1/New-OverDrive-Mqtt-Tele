from __future__ import annotations

import json
import logging
from dataclasses import dataclass

from homeassistant.components import mqtt

from .const import CONF_CONTROL_TOPIC, DEFAULT_CONTROL_TOPIC

_LOGGER = logging.getLogger(__name__)
DISCOVERY_PREFIX = "homeassistant"


@dataclass(frozen=True)
class DiscoveryButton:
    object_id: str
    name: str
    key: str
    payload: str
    icon: str
    subtopic: str | None = None


# Commands are intentionally expressed as direct OverDrive /set topics.
# The configured Control Topic is the base, e.g. overdrive/vehicle/telemetry.
BUTTONS = (
    DiscoveryButton("climate_on", "Climate On", "climate", "auto", "mdi:air-conditioner", "mode"),
    DiscoveryButton("climate_off", "Climate Off", "climate", "off", "mdi:air-conditioner", "mode"),
    DiscoveryButton("open_windows", "Open Windows", "windows_all", "OPEN", "mdi:window-open"),
    DiscoveryButton("close_windows", "Close Windows", "windows_all", "CLOSE", "mdi:window-closed"),
    DiscoveryButton("stop_windows", "Stop Windows", "windows_all", "STOP", "mdi:window-shutter-alert"),
    DiscoveryButton("vent_windows", "Vent Windows", "windows_vent", "PRESS", "mdi:car-door"),
    DiscoveryButton("open_tailgate", "Open Tailgate", "tailgate", "OPEN", "mdi:car-back"),
    DiscoveryButton("close_tailgate", "Close Tailgate", "tailgate", "CLOSE", "mdi:car-back"),
    DiscoveryButton("stop_tailgate", "Stop Tailgate", "tailgate", "STOP", "mdi:stop-circle-outline"),
    DiscoveryButton("open_sunroof", "Open Sunroof", "sunroof", "OPEN", "mdi:window-shutter-open"),
    DiscoveryButton("close_sunroof", "Close Sunroof", "sunroof", "CLOSE", "mdi:window-shutter"),
    DiscoveryButton("stop_sunroof", "Stop Sunroof", "sunroof", "STOP", "mdi:stop-circle-outline"),
    DiscoveryButton("open_sunshade", "Open Sunshade", "sunshade", "OPEN", "mdi:blinds-open"),
    DiscoveryButton("close_sunshade", "Close Sunshade", "sunshade", "CLOSE", "mdi:blinds"),
    DiscoveryButton("stop_sunshade", "Stop Sunshade", "sunshade", "STOP", "mdi:stop-circle-outline"),
    DiscoveryButton("start_charging_now", "Start Charging Now", "start_charging_now", "PRESS", "mdi:battery-charging"),
    DiscoveryButton("toggle_mirrors", "Toggle Mirrors", "mirror_fold", "toggle", "mdi:car-side"),
    DiscoveryButton("toggle_steering_heat", "Toggle Steering Wheel Heat", "steering_heat", "toggle", "mdi:steering"),
    DiscoveryButton("toggle_drl", "Toggle Daytime Running Lights", "drl", "toggle", "mdi:car-light-dimmed"),
    DiscoveryButton("toggle_hazards", "Toggle Hazard Lights", "hazard", "toggle", "mdi:car-light-alert"),
    DiscoveryButton("toggle_child_lock", "Toggle Child Lock", "child_lock", "toggle", "mdi:car-door-lock"),
    DiscoveryButton("toggle_wireless_charging", "Toggle Wireless Charger", "wireless_charging", "toggle", "mdi:battery-charging-wireless"),
    DiscoveryButton("cycle_driver_seat_heat", "Cycle Driver Seat Heat", "seat_heat_driver", "toggle", "mdi:car-seat-heater"),
    DiscoveryButton("cycle_passenger_seat_heat", "Cycle Passenger Seat Heat", "seat_heat_passenger", "toggle", "mdi:car-seat-heater"),
    DiscoveryButton("cycle_driver_seat_vent", "Cycle Driver Seat Ventilation", "seat_vent_driver", "toggle", "mdi:car-seat-cooler"),
    DiscoveryButton("cycle_passenger_seat_vent", "Cycle Passenger Seat Ventilation", "seat_vent_passenger", "toggle", "mdi:car-seat-cooler"),
    DiscoveryButton("cycle_drive_mode", "Cycle Drive Mode", "drive_mode", "toggle", "mdi:car-shift-pattern"),
    DiscoveryButton("cycle_regen", "Cycle Regeneration", "regen_level", "toggle", "mdi:battery-charging-medium"),
    DiscoveryButton("cycle_steering_mode", "Cycle Steering Assist", "steering_mode", "toggle", "mdi:steering"),
    DiscoveryButton("cycle_brake_feel", "Cycle Brake Feel", "brake_feel", "toggle", "mdi:car-brake-alert"),
)


def _command_topic(base: str, button: DiscoveryButton) -> str:
    if button.subtopic:
        return f"{base}/{button.key}/{button.subtopic}/set"
    return f"{base}/{button.key}/set"


async def async_publish_control_discovery(hass, entry) -> None:
    """Publish retained native MQTT Discovery buttons for OverDrive controls."""
    base = entry.data.get(CONF_CONTROL_TOPIC, DEFAULT_CONTROL_TOPIC).strip().rstrip("/")
    device = {
        "identifiers": [f"overdrive_byd_controls_{entry.entry_id}"],
        "name": "BYD Vehicle Controls",
        "manufacturer": "BYD / OverDrive",
        "model": "MQTT Vehicle Controls",
    }

    # First publish a safe local diagnostic button. It never targets the car.
    test_unique_id = f"overdrive_byd_{entry.entry_id}_mqtt_control_test"
    test_discovery_topic = f"{DISCOVERY_PREFIX}/button/{test_unique_id}/config"
    test_payload = {
        "name": "MQTT Control Test",
        "unique_id": test_unique_id,
        "command_topic": f"overdrive_byd/{entry.entry_id}/control_test",
        "payload_press": "PING",
        "icon": "mdi:lan-check",
        "device": device,
        "entity_category": "diagnostic",
    }
    await mqtt.async_publish(
        hass,
        test_discovery_topic,
        json.dumps(test_payload, separators=(",", ":")),
        qos=0,
        retain=True,
    )

    for button in BUTTONS:
        unique_id = f"overdrive_byd_{entry.entry_id}_{button.object_id}"
        topic = f"{DISCOVERY_PREFIX}/button/{unique_id}/config"
        payload = {
            "name": button.name,
            "unique_id": unique_id,
            "command_topic": _command_topic(base, button),
            "payload_press": button.payload,
            "icon": button.icon,
            "device": device,
        }
        await mqtt.async_publish(
            hass,
            topic,
            json.dumps(payload, separators=(",", ":")),
            qos=0,
            retain=True,
        )
        _LOGGER.debug(
            "Published OverDrive control %s -> %s",
            button.name,
            payload["command_topic"],
        )

    _LOGGER.info(
        "Published %d OverDrive MQTT controls using control base %s",
        len(BUTTONS) + 1,
        base,
    )
