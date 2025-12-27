"""Config flow for AppFire integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow as BaseConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)
from homeassistant.core import callback
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from .const import (
    CONF_STOVE_NAME,
    CONF_SERIAL,
    CONF_IP,
    CONF_PORT,
    CONF_POLLING_INTERVAL,
    DEFAULT_PORT,
    DEFAULT_SCAN_INTERVAL_S,
    DOMAIN,
)
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


class ConfigFlow(BaseConfigFlow, domain=DOMAIN):
    """Handle a config flow for AppFire."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(_config_entry: ConfigEntry) -> OptionsFlow:
        """Get the options flow for this handler."""
        return AppFireOptionsFlow()

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
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


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> None:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_SCHEMA with values provided by the user.
    """
    appfire = AppFire(data[CONF_IP], data[CONF_PORT])

    if not await hass.async_add_executor_job(appfire.isOnline):
        raise CannotConnect

    # Note: If authentication is added in the future, validate credentials here
    # and raise InvalidAuth on failure.


class AppFireOptionsFlow(OptionsFlow):
    """Handle options flow for AppFire."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Manage the options."""
        errors: dict[str, str] = {}

        if user_input is not None:
            # Validate connection with new settings
            try:
                await validate_input(self.hass, {
                    CONF_IP: user_input[CONF_IP],
                    CONF_PORT: user_input[CONF_PORT],
                })
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                # Update the config entry with new data
                new_data = {**self.config_entry.data, **user_input}
                self.hass.config_entries.async_update_entry(
                    self.config_entry, data=new_data
                )
                # Reload the integration to apply changes
                await self.hass.config_entries.async_reload(self.config_entry.entry_id)
                return self.async_create_entry(title="", data={})

        # Show form with current values as defaults
        options_schema = vol.Schema(
            {
                vol.Required(
                    CONF_IP,
                    default=self.config_entry.data.get(CONF_IP),
                ): str,
                vol.Required(
                    CONF_PORT,
                    default=self.config_entry.data.get(CONF_PORT, DEFAULT_PORT),
                ): vol.All(vol.Coerce(int), vol.Clamp(min=1), vol.Clamp(max=65535)),
                vol.Required(
                    CONF_POLLING_INTERVAL,
                    default=self.config_entry.data.get(CONF_POLLING_INTERVAL, DEFAULT_SCAN_INTERVAL_S),
                ): vol.All(vol.Coerce(int), vol.Clamp(min=5)),
            }
        )

        return self.async_show_form(
            step_id="init", data_schema=options_schema, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
