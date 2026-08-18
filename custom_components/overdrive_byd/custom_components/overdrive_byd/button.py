from __future__ import annotations

from homeassistant.components.button import ButtonEntity

from .command import async_send_control
from .control_definitions import BUTTONS
from .control_entity import OverdriveBYDControlEntity


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data["overdrive_byd"][entry.entry_id]
    async_add_entities([OverdriveBYDButton(coordinator, d) for d in BUTTONS])


class OverdriveBYDButton(OverdriveBYDControlEntity, ButtonEntity):
    def __init__(self, coordinator, definition):
        super().__init__(coordinator, definition.key, definition.name, definition.icon)
        self.defn = definition

    async def async_press(self):
        await async_send_control(self.hass, self.coordinator.entry, self.defn.key, "PRESS")
