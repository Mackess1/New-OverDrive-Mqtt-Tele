from __future__ import annotations

from homeassistant.components.text import TextEntity, TextMode

from .command import async_send_control
from .control_definitions import TEXTS
from .control_entity import OverdriveBYDControlEntity


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data["overdrive_byd"][entry.entry_id]
    async_add_entities([OverdriveBYDText(coordinator, d) for d in TEXTS])


class OverdriveBYDText(OverdriveBYDControlEntity, TextEntity):
    def __init__(self, coordinator, definition):
        super().__init__(coordinator, definition.key, definition.name, definition.icon, definition.category)
        self.defn = definition
        self._attr_mode = TextMode.TEXT
        self._attr_native_min = 1
        self._attr_native_max = 1024
        self._value = None

    @property
    def native_value(self):
        return self._value

    async def async_set_value(self, value: str):
        await async_send_control(self.hass, self.coordinator.entry, self.defn.key, value)
        self._value = value
        self.async_write_ha_state()
