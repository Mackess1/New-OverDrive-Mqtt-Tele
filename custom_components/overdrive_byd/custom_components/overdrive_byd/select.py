from __future__ import annotations

from homeassistant.components.select import SelectEntity

from .command import async_send_control
from .control_definitions import SELECTS
from .control_entity import OverdriveBYDControlEntity


def decode_value(decoder, value):
    if value is None:
        return None
    text = str(value).strip().lower()
    if decoder == "drive_mode":
        return {"1": "normal", "2": "eco", "3": "sport", "4": "snow"}.get(text, text)
    if decoder == "powertrain_mode":
        return {"1": "ev", "2": "force_ev", "3": "hev", "4": "fuel", "5": "keep"}.get(text, text)
    if decoder == "hold_battery":
        return "on" if text in {"3", "hev"} else None
    return text


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data["overdrive_byd"][entry.entry_id]
    async_add_entities([OverdriveBYDSelect(coordinator, d) for d in SELECTS])


class OverdriveBYDSelect(OverdriveBYDControlEntity, SelectEntity):
    def __init__(self, coordinator, definition):
        super().__init__(coordinator, definition.key, definition.name, definition.icon, definition.category)
        self.defn = definition
        self._attr_options = list(definition.options)
        self._optimistic = None

    @property
    def current_option(self):
        key = self.defn.state_key or self.defn.key
        value = decode_value(self.defn.decoder, self.coordinator.data.get(key))
        if value in self.options:
            return value
        return self._optimistic if self._optimistic in self.options else None

    async def async_select_option(self, option: str):
        if option not in self.options:
            return
        await async_send_control(self.hass, self.coordinator.entry, self.defn.key, option)
        self._optimistic = option
        self.async_write_ha_state()
