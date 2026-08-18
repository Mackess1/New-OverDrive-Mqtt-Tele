from __future__ import annotations

from homeassistant.components.number import NumberEntity, NumberMode

from .command import async_send_control
from .control_definitions import NUMBERS
from .control_entity import OverdriveBYDControlEntity


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data["overdrive_byd"][entry.entry_id]
    async_add_entities([OverdriveBYDNumber(coordinator, d) for d in NUMBERS])


class OverdriveBYDNumber(OverdriveBYDControlEntity, NumberEntity):
    def __init__(self, coordinator, definition):
        super().__init__(coordinator, definition.key, definition.name, definition.icon, definition.category)
        self.defn = definition
        self._attr_native_min_value = definition.minimum
        self._attr_native_max_value = definition.maximum
        self._attr_native_step = definition.step
        self._attr_mode = NumberMode.SLIDER
        self._attr_native_unit_of_measurement = definition.unit
        self._optimistic = None

    @property
    def native_value(self):
        raw = self.coordinator.data.get(self.defn.state_key or self.defn.key)
        try:
            return float(raw) if raw is not None else self._optimistic
        except (TypeError, ValueError):
            return self._optimistic

    async def async_set_native_value(self, value: float):
        payload = int(value) if float(value).is_integer() else value
        await async_send_control(self.hass, self.coordinator.entry, self.defn.key, payload)
        self._optimistic = float(value)
        self.async_write_ha_state()
