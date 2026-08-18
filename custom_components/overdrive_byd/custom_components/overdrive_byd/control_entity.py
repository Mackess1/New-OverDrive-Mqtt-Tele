from __future__ import annotations

from homeassistant.helpers.entity import EntityCategory

from .entity import OverdriveBYDEntity


class OverdriveBYDControlEntity(OverdriveBYDEntity):
    def __init__(self, coordinator, key: str, name: str, icon: str, category: str | None = None):
        super().__init__(coordinator)
        self.key = key
        self._attr_name = name
        self._attr_unique_id = f"{coordinator.entry.entry_id}_control_{key}"
        self._attr_icon = icon
        if category == "config":
            self._attr_entity_category = EntityCategory.CONFIG
