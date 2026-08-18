from __future__ import annotations

from homeassistant.components.cover import CoverDeviceClass, CoverEntity, CoverEntityFeature

from .command import async_send_control
from .control_entity import OverdriveBYDControlEntity

COVERS = [
    ("windows_all", "Windows", "mdi:car-door", CoverDeviceClass.WINDOW),
    ("tailgate", "Tailgate", "mdi:car-back", CoverDeviceClass.DOOR),
    ("sunroof", "Sunroof", "mdi:window-shutter-open", CoverDeviceClass.WINDOW),
    ("sunshade", "Sunshade", "mdi:blinds", CoverDeviceClass.SHADE),
]


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data["overdrive_byd"][entry.entry_id]
    async_add_entities([OverdriveBYDCover(coordinator, *d) for d in COVERS])


class OverdriveBYDCover(OverdriveBYDControlEntity, CoverEntity):
    def __init__(self, coordinator, key, name, icon, device_class):
        super().__init__(coordinator, key, name, icon)
        self._attr_device_class = device_class
        self._attr_supported_features = (
            CoverEntityFeature.OPEN | CoverEntityFeature.CLOSE | CoverEntityFeature.STOP
        )

    # Official OverDrive discovery marks these covers optimistic because the
    # current control catalog does not provide reliable position readback.
    @property
    def is_closed(self):
        return None

    async def async_open_cover(self, **kwargs):
        await async_send_control(self.hass, self.coordinator.entry, self.key, "OPEN")

    async def async_close_cover(self, **kwargs):
        await async_send_control(self.hass, self.coordinator.entry, self.key, "CLOSE")

    async def async_stop_cover(self, **kwargs):
        await async_send_control(self.hass, self.coordinator.entry, self.key, "STOP")
