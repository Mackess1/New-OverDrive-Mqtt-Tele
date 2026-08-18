from __future__ import annotations

from homeassistant.components.switch import SwitchEntity

from .command import async_send_control
from .control_definitions import SWITCHES
from .control_entity import OverdriveBYDControlEntity


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data["overdrive_byd"][entry.entry_id]
    async_add_entities([OverdriveBYDSwitch(coordinator, d) for d in SWITCHES])


class OverdriveBYDSwitch(OverdriveBYDControlEntity, SwitchEntity):
    def __init__(self, coordinator, definition):
        super().__init__(coordinator, definition.key, definition.name, definition.icon, definition.category)
        self.defn = definition
        self._optimistic = None

    @property
    def is_on(self):
        key = self.defn.state_key or self.defn.key
        value = self.coordinator.data.get(key)
        if value is None:
            return self._optimistic
        return str(value).strip().lower() in {str(self.defn.on).lower(), "true", "on"}

    async def async_turn_on(self, **kwargs):
        await async_send_control(self.hass, self.coordinator.entry, self.defn.key, self.defn.on)
        self._optimistic = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        await async_send_control(self.hass, self.coordinator.entry, self.defn.key, self.defn.off)
        self._optimistic = False
        self.async_write_ha_state()
