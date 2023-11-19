"""The AppFire integration."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .lib.appfire_client.appfire import AppFire
from .coordinator import MyCoordinator

from .const import DOMAIN
from .const import CONF_IP
from .const import CONF_PORT
from .const import CONF_STOVE_NAME
from .const import CONF_SERIAL

# TODO List the platforms that you want to support.
# For your initial PR, limit it to 1 platform.
PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.NUMBER, Platform.SWITCH]

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up AppFire from a config entry."""

    _LOGGER.debug(f"[.] Entering async_setup_entry with entry_id: {entry.entry_id}")

    # 1. Create API instance
    appFireApi = AppFire(entry.data.get(CONF_IP), entry.data.get(CONF_PORT))
    stoveName = entry.data.get(CONF_STOVE_NAME)
    stoveSerial = entry.data.get(CONF_SERIAL)

    # TODO 2. Validate the API connection (and authentication)
    # ...

    # 3. Create data coordinator
    coordinator = MyCoordinator(hass, stoveName, stoveSerial, appFireApi)

    # 4. Store the coordinator for your platforms to access
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator




    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True



# async def async_setup_entry(hass, entry, async_add_entities):
#     """Config entry example."""
#     # assuming API object stored here by __init__.py
#     my_api = hass.data[DOMAIN][entry.entry_id]
#     coordinator = MyCoordinator(hass, my_api)

#     # Fetch initial data so we have data when entities subscribe
#     #
#     # If the refresh fails, async_config_entry_first_refresh will
#     # raise ConfigEntryNotReady and setup will try again later
#     #
#     # If you do not want to retry setup on failure, use
#     # coordinator.async_refresh() instead
#     #
#     await coordinator.async_config_entry_first_refresh()

#     async_add_entities(
#         MyEntity(coordinator, idx) for idx, ent in enumerate(coordinator.data)
#     )



async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
