"""Platform for sensor integration."""
from __future__ import annotations

import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    API_DATA_LOOKUP_POWER_PERCENTAGE,
    API_DATA_LOOKUP_AMBIENT_TEMPERATURE,
    API_DATA_LOOKUP_STOVE_STATUS,
)
from .entity import AppFireEntity
from .lib.appfire_client.status.stove_status import StoveStatus as StoveStatusApi

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor entity."""

    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    async_add_entities(
        [
            StoveStatus(coordinator),
            PowerPercentage(coordinator),
            AmbientTemperature(coordinator),
        ]
    )


class StoveStatus(AppFireEntity, SensorEntity):
    """Sensor for stove status."""

    _attr_device_class = SensorDeviceClass.ENUM
    _attr_translation_key = "stove_status"

    def __init__(self, coordinator):
        """Initialize the sensor."""
        super().__init__(coordinator, context=API_DATA_LOOKUP_STOVE_STATUS)
        self._idx = API_DATA_LOOKUP_STOVE_STATUS
        self._attr_unique_id = f"{self.coordinator.stoveSerial}_sensor_status"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        status_code = self.coordinator.data[self._idx]
        self._attr_native_value = StoveStatusApi.statusToText(status_code)
        self.async_write_ha_state()


class PowerPercentage(AppFireEntity, SensorEntity):
    """Sensor for power percentage."""

    _attr_icon = "mdi:percent"
    _attr_native_unit_of_measurement = "%"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_suggested_display_precision = 0
    _attr_translation_key = "power_percentage"

    def __init__(self, coordinator):
        """Initialize the sensor."""
        super().__init__(coordinator, context=API_DATA_LOOKUP_POWER_PERCENTAGE)
        self._idx = API_DATA_LOOKUP_POWER_PERCENTAGE
        self._attr_unique_id = f"{self.coordinator.stoveSerial}_sensor_power_level"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.coordinator.data[self._idx]
        self.async_write_ha_state()


class AmbientTemperature(AppFireEntity, SensorEntity):
    """Sensor for ambient temperature."""

    _attr_icon = "mdi:home-thermometer"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_translation_key = "ambient_temperature"

    def __init__(self, coordinator):
        """Initialize the sensor."""
        super().__init__(coordinator, context=API_DATA_LOOKUP_AMBIENT_TEMPERATURE)
        self._idx = API_DATA_LOOKUP_AMBIENT_TEMPERATURE
        self._attr_unique_id = f"{self.coordinator.stoveSerial}_sensor_ambient_temperature"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.coordinator.data[self._idx]
        self.async_write_ha_state()
