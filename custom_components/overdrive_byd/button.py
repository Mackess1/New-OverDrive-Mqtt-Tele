from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .command import async_send_control
from .const import DOMAIN
from .control_entity import OverdriveBYDControlEntity


@dataclass(frozen=True, kw_only=True)
class CommandButtonDef:
    key: str
    name: str
    icon: str
    command_key: str
    payload: str
    subtopic: str | None = None


# Deliberately exposed as separate HA buttons, following the UX pattern used by
# hass-byd-vehicle. These make remote commands visible on the device page even
# when the corresponding cover/climate entity is collapsed by the frontend.
COMMAND_BUTTONS: tuple[CommandButtonDef, ...] = (
    CommandButtonDef(key="open_windows", name="Open Windows", icon="mdi:window-open", command_key="windows_all", payload="OPEN"),
    CommandButtonDef(key="close_windows", name="Close Windows", icon="mdi:window-closed", command_key="windows_all", payload="CLOSE"),
    CommandButtonDef(key="stop_windows", name="Stop Windows", icon="mdi:window-shutter-alert", command_key="windows_all", payload="STOP"),
    CommandButtonDef(key="vent_windows", name="Vent Windows", icon="mdi:car-door", command_key="windows_vent", payload="PRESS"),
    CommandButtonDef(key="open_tailgate", name="Open Tailgate", icon="mdi:car-back", command_key="tailgate", payload="OPEN"),
    CommandButtonDef(key="close_tailgate", name="Close Tailgate", icon="mdi:car-back", command_key="tailgate", payload="CLOSE"),
    CommandButtonDef(key="stop_tailgate", name="Stop Tailgate", icon="mdi:stop-circle-outline", command_key="tailgate", payload="STOP"),
    CommandButtonDef(key="climate_on", name="Climate On", icon="mdi:air-conditioner", command_key="climate", subtopic="mode", payload="auto"),
    CommandButtonDef(key="climate_off", name="Climate Off", icon="mdi:air-conditioner", command_key="climate", subtopic="mode", payload="off"),
    CommandButtonDef(key="start_charging", name="Start Charging Now", icon="mdi:battery-charging", command_key="start_charging_now", payload="PRESS"),
    CommandButtonDef(key="fold_mirrors", name="Fold Mirrors", icon="mdi:car-side", command_key="mirror_fold", payload="1"),
    CommandButtonDef(key="unfold_mirrors", name="Unfold Mirrors", icon="mdi:car-side", command_key="mirror_fold", payload="0"),
    CommandButtonDef(key="open_sunroof", name="Open Sunroof", icon="mdi:window-shutter-open", command_key="sunroof", payload="OPEN"),
    CommandButtonDef(key="close_sunroof", name="Close Sunroof", icon="mdi:window-shutter", command_key="sunroof", payload="CLOSE"),
    CommandButtonDef(key="stop_sunroof", name="Stop Sunroof", icon="mdi:stop-circle-outline", command_key="sunroof", payload="STOP"),
    CommandButtonDef(key="open_sunshade", name="Open Sunshade", icon="mdi:blinds-open", command_key="sunshade", payload="OPEN"),
    CommandButtonDef(key="close_sunshade", name="Close Sunshade", icon="mdi:blinds", command_key="sunshade", payload="CLOSE"),
    CommandButtonDef(key="stop_sunshade", name="Stop Sunshade", icon="mdi:stop-circle-outline", command_key="sunshade", payload="STOP"),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([OverdriveBYDCommandButton(coordinator, d) for d in COMMAND_BUTTONS])


class OverdriveBYDCommandButton(OverdriveBYDControlEntity, ButtonEntity):
    def __init__(self, coordinator, definition: CommandButtonDef) -> None:
        super().__init__(coordinator, definition.key, definition.name, definition.icon)
        self.defn = definition

    async def async_press(self) -> None:
        await async_send_control(
            self.hass,
            self.coordinator.entry,
            self.defn.command_key,
            self.defn.payload,
            self.defn.subtopic,
        )
