"""Config flow for AppFire integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import CONF_STOVE_NAME
from .const import CONF_SERIAL
from .const import CONF_IP
from .const import CONF_PORT
from .const import CONF_POLLING_INTERVAL
from .const import DEFAULT_PORT
from .const import DEFAULT_SCAN_INTERVAL_S
from .const import DOMAIN

from .lib.appfire_client.appfire import AppFire


_LOGGER = logging.getLogger(__name__)

STEP_USER_SCHEMA = vol.Schema(
    {
        vol.Optional(
            CONF_STOVE_NAME,
            description="The name of the stove",
        ): str,
        vol.Required(
            CONF_SERIAL,
            description="The serial number of the stove",
        ): str,
        vol.Required(
            CONF_IP,
            description="The IP address of the stove",
        ): str,
        vol.Optional(
            CONF_PORT,
            description="The port of the stove",
            default=DEFAULT_PORT,
        ): vol.All(vol.Coerce(int), vol.Clamp(min=1), vol.Clamp(max=65535)),
        vol.Optional(
            CONF_POLLING_INTERVAL,
            description="Polling interval in seconds",
            default=DEFAULT_SCAN_INTERVAL_S,
        ): vol.All(vol.Coerce(int), vol.Clamp(min=5)),
    }
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for AppFire."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(user_input[CONF_SERIAL])
                self._abort_if_unique_id_configured()

                if user_input.get(CONF_STOVE_NAME) == None:
                    title = f"Stove {user_input[CONF_SERIAL]}"
                else:
                    title = f"Stove {user_input[CONF_STOVE_NAME]} ({user_input[CONF_SERIAL]})"

                return self.async_create_entry(title=title, data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_SCHEMA, errors=errors
        )


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_SCHEMA with values provided by the user.
    """

    appfire = AppFire(data["ip"], data["port"])

    # If your PyPI package is not built with async, pass your methods
    # to the executor:
    if not await hass.async_add_executor_job(appfire.isOnline):
        raise CannotConnect

    # hub = PlaceholderHub(data["host"])

    # if not await hub.authenticate(data["username"], data["password"]):
    #     raise InvalidAuth

    # If you cannot connect:
    # throw CannotConnect
    # If the authentication is wrong:
    # InvalidAuth

    # Return info that you want to store in the config entry.
    return None


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
