"""Platform for switch integration."""
from __future__ import annotations

import logging

from homeassistant.components.switch import (
    SwitchEntity,
)
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.core import callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .const import API_DATA_LOOKUP_POWER_STATUS


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the switch entity."""

    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    async_add_entities([PowerStatus(coordinator)])


class PowerStatus(CoordinatorEntity, SwitchEntity):
    _attr_icon = "mdi:power"
    _attr_assumed_state = True

    def __init__(self, coordinator):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator, context=API_DATA_LOOKUP_POWER_STATUS)
        self._idx = API_DATA_LOOKUP_POWER_STATUS

        self._attr_name = self.coordinator.getStoveNameOrSerial() + " power status"
        self._attr_unique_id = (
            self.coordinator.stoveSerial + "_switch" + "_power_status"
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_is_on = self.coordinator.data[self._idx]
        self._attr_icon = "mdi:fire" if self._attr_is_on else "mdi:fire-off"
        self.async_write_ha_state()

    async def async_turn_on(self, **kwargs) -> None:
        """Turn the entity on."""
        await self.hass.async_add_executor_job(self.coordinator.appFireApi.turnOn)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the entity off."""
        await self.hass.async_add_executor_job(self.coordinator.appFireApi.turnOff)
        await self.coordinator.async_request_refresh()
