"""Platform for number integration."""
from __future__ import annotations

import logging

from homeassistant.components.number import NumberDeviceClass, NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, API_DATA_LOOKUP_DESIRED_AMBIENT_TEMPERATURE
from .coordinator import AppFireCoordinator
from .entity import AppFireEntity


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the number entity."""

    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    async_add_entities([DesiredAmbientTemperature(coordinator)])


class DesiredAmbientTemperature(AppFireEntity, NumberEntity):
    """Number entity for desired ambient temperature."""

    _attr_device_class = NumberDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_native_step = 0.1
    _attr_translation_key = "desired_ambient_temperature"

    def __init__(self, coordinator: AppFireCoordinator):
        """Initialize the number entity."""
        super().__init__(coordinator, context=API_DATA_LOOKUP_DESIRED_AMBIENT_TEMPERATURE)
        self._idx = API_DATA_LOOKUP_DESIRED_AMBIENT_TEMPERATURE
        self._attr_unique_id = f"{self.coordinator.stove_serial}_number_desired_ambient_temperature"

    @property
    def native_min_value(self) -> float:
        """Return the minimum value."""
        return 10

    @property
    def native_max_value(self) -> float:
        """Return the maximum value."""
        return 50

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.coordinator.data[self._idx]
        self.async_write_ha_state()

    async def async_set_native_value(self, value: float) -> None:
        """Set the desired ambient temperature."""
        await self.hass.async_add_executor_job(
            self.coordinator.api.setDesiredAmbientTemperature, value
        )
        await self.coordinator.async_request_refresh()
