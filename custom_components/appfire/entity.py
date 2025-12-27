"""Base entity for AppFire integration."""
from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import AppFireCoordinator


class AppFireEntity(CoordinatorEntity[AppFireCoordinator]):
    """Base class for AppFire entities."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: AppFireCoordinator, context: str) -> None:
        """Initialize the entity."""
        super().__init__(coordinator, context=context)

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information about this AppFire stove."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.stove_serial)},
            name=self.coordinator.get_stove_name_or_serial(),
            manufacturer="AppFire",
            model="Pellet Stove",
        )
