from __future__ import annotations

from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import ClimateEntityFeature, HVACMode
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature

from .command import async_send_control
from .control_entity import OverdriveBYDControlEntity


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data["overdrive_byd"][entry.entry_id]
    async_add_entities([OverdriveBYDClimate(coordinator)])


class OverdriveBYDClimate(OverdriveBYDControlEntity, ClimateEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator, "climate", "Climate", "mdi:air-conditioner")
        self._attr_temperature_unit = UnitOfTemperature.CELSIUS
        self._attr_hvac_modes = [HVACMode.OFF, HVACMode.AUTO]
        self._attr_fan_modes = [str(i) for i in range(1, 8)]
        self._attr_min_temp = 17
        self._attr_max_temp = 33
        self._attr_target_temperature_step = 1
        self._attr_supported_features = (
            ClimateEntityFeature.TARGET_TEMPERATURE | ClimateEntityFeature.FAN_MODE
        )
        self._optimistic_temp = 22.0
        self._optimistic_mode = HVACMode.OFF
        self._optimistic_fan = None

    @property
    def hvac_mode(self):
        raw = self.coordinator.data.get("ac_on")
        if raw is None:
            return self._optimistic_mode
        return HVACMode.AUTO if str(raw).strip().lower() not in {"0", "false", "off"} else HVACMode.OFF

    @property
    def target_temperature(self):
        raw = self.coordinator.data.get("climate_setpoint")
        try:
            return float(raw) if raw is not None else self._optimistic_temp
        except (TypeError, ValueError):
            return self._optimistic_temp

    @property
    def current_temperature(self):
        raw = self.coordinator.data.get("cabin_temp")
        try:
            return float(raw) if raw is not None else None
        except (TypeError, ValueError):
            return None

    @property
    def fan_mode(self):
        raw = self.coordinator.data.get("ac_fan")
        if raw is not None and str(raw) in self.fan_modes:
            return str(raw)
        return self._optimistic_fan

    async def async_set_hvac_mode(self, hvac_mode):
        payload = "off" if hvac_mode == HVACMode.OFF else "auto"
        await async_send_control(self.hass, self.coordinator.entry, "climate", payload, "mode")
        self._optimistic_mode = hvac_mode
        self.async_write_ha_state()

    async def async_set_temperature(self, **kwargs):
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is None:
            return
        await async_send_control(self.hass, self.coordinator.entry, "climate", temperature, "temperature")
        self._optimistic_temp = float(temperature)
        self.async_write_ha_state()

    async def async_set_fan_mode(self, fan_mode):
        if fan_mode not in self.fan_modes:
            return
        await async_send_control(self.hass, self.coordinator.entry, "climate", fan_mode, "fan_mode")
        self._optimistic_fan = fan_mode
        self.async_write_ha_state()
