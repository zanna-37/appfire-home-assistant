"""Platform for switch integration."""
from __future__ import annotations

import logging

from homeassistant.components.switch import SwitchDeviceClass, SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, API_DATA_LOOKUP_POWER_STATUS
from .entity import AppFireEntity


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the switch entity."""

    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    async_add_entities([PowerStatus(coordinator)])


class PowerStatus(AppFireEntity, SwitchEntity):
    """Switch to control stove power."""

    _attr_assumed_state = True
    _attr_device_class = SwitchDeviceClass.SWITCH
    _attr_translation_key = "power_status"

    def __init__(self, coordinator):
        """Initialize the switch."""
        super().__init__(coordinator, context=API_DATA_LOOKUP_POWER_STATUS)
        self._idx = API_DATA_LOOKUP_POWER_STATUS
        self._attr_unique_id = f"{self.coordinator.stove_serial}_switch_power_status"

    @property
    def icon(self) -> str:
        """Return the icon based on state."""
        return "mdi:fire" if self.is_on else "mdi:fire-off"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_is_on = self.coordinator.data[self._idx]
        self.async_write_ha_state()

    async def async_turn_on(self, **kwargs) -> None:
        """Turn the entity on."""
        await self.hass.async_add_executor_job(self.coordinator.api.turnOn)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the entity off."""
        await self.hass.async_add_executor_job(self.coordinator.api.turnOff)
        await self.coordinator.async_request_refresh()
