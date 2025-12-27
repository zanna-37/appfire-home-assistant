"""Base entity for AppFire integration."""
from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import MyCoordinator


class AppFireEntity(CoordinatorEntity[MyCoordinator]):
    """Base class for AppFire entities."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: MyCoordinator, context: str) -> None:
        """Initialize the entity."""
        super().__init__(coordinator, context=context)

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information about this AppFire stove."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.stoveSerial)},
            name=self.coordinator.getStoveNameOrSerial(),
            manufacturer="AppFire",
            model="Pellet Stove",
        )
