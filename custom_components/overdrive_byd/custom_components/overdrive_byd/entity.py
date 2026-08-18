from __future__ import annotations

from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, INVALID_VALUES


def clean_value(value):
    # Lists/dicts are valid telemetry containers but are unhashable, so do
    # not test them directly against the sentinel set.
    try:
        if value in INVALID_VALUES:
            return None
    except TypeError:
        pass

    if isinstance(value, float):
        return round(value, 3)

    return value


def get_array_value(data: dict, key: str, index: int):
    value = data.get(key)

    if not isinstance(value, list):
        return None

    if index >= len(value):
        return None

    return clean_value(value[index])


class OverdriveBYDEntity(CoordinatorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator, description=None) -> None:
        super().__init__(coordinator)

        self.entity_description = description

        vin = coordinator.data.get("vin", "unknown")
        self._attr_device_info = {
            "identifiers": {(DOMAIN, vin)},
            "name": coordinator.entry.data.get("name", "BYD Vehicle"),
            "manufacturer": "BYD",
            "model": "Yuan Plus / Atto 3",
        }

    @property
    def available(self) -> bool:
        # Any received telemetry is positive proof that the vehicle feed is
        # alive. This prevents an absent/non-retained or differently encoded
        # availability topic from making every Home Assistant entity
        # unavailable at once. Explicit offline is still respected until new
        # telemetry arrives, at which point the coordinator sets available
        # back to True.
        return self.coordinator.available or bool(self.coordinator.data)
