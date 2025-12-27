"""The AppFire integration."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .lib.appfire_client.appfire import AppFire
from .coordinator import MyCoordinator

from .const import (
    DOMAIN,
    CONF_IP,
    CONF_PORT,
    CONF_STOVE_NAME,
    CONF_SERIAL,
    CONF_POLLING_INTERVAL,
    DEFAULT_SCAN_INTERVAL_S,
)

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.NUMBER, Platform.SWITCH]

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up AppFire from a config entry."""

    _LOGGER.debug(f"[.] Entering async_setup_entry with entry_id: {entry.entry_id}")

    # 1. Create API instance
    appFireApi = AppFire(entry.data.get(CONF_IP), entry.data.get(CONF_PORT))
    stoveName = entry.data.get(CONF_STOVE_NAME)
    stoveSerial = entry.data.get(CONF_SERIAL)
    polling_interval = entry.data.get(CONF_POLLING_INTERVAL, DEFAULT_SCAN_INTERVAL_S)

    # 2. Create data coordinator
    coordinator = MyCoordinator(hass, stoveName, stoveSerial, appFireApi, polling_interval)

    # 3. Fetch initial data so we have data when entities subscribe
    #    If the refresh fails, async_config_entry_first_refresh will
    #    raise ConfigEntryNotReady and setup will try again later
    await coordinator.async_config_entry_first_refresh()

    # 4. Store the coordinator for your platforms to access
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
