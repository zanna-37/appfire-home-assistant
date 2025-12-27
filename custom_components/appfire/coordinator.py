"""Data coordinator for AppFire integration."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import (
    API_DATA_LOOKUP_STOVE_STATUS,
    API_DATA_LOOKUP_POWER_STATUS,
    API_DATA_LOOKUP_ECO_MODE,
    API_DATA_LOOKUP_AMBIENT_TEMPERATURE,
    API_DATA_LOOKUP_DESIRED_AMBIENT_TEMPERATURE,
    API_DATA_LOOKUP_DESIRED_AMBIENT_TEMPERATURE_MIN,
    API_DATA_LOOKUP_DESIRED_AMBIENT_TEMPERATURE_MAX,
    API_DATA_LOOKUP_SMOKE_TEMPERATURE,
    API_DATA_LOOKUP_POWER_PERCENTAGE,
    API_DATA_LOOKUP_SMOKE_FAN_RPM,
    API_DATA_LOOKUP_FAN1_PERCENTAGE,
)

_LOGGER = logging.getLogger(__name__)


class AppFireCoordinator(DataUpdateCoordinator):
    """Coordinator for AppFire stove data updates."""

    def __init__(self, hass, stove_name, stove_serial, api, polling_interval: int):
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name="AppFireCoordinator",
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(seconds=polling_interval),
        )
        self.api = api
        self.stove_name = stove_name
        self.stove_serial = stove_serial

    def get_stove_name_or_serial(self):
        """Return stove name if set, otherwise serial."""
        if self.stove_name is not None:
            return self.stove_name
        return self.stove_serial

    async def _async_update_data(self):
        """Fetch data from API endpoint."""
        try:
            _LOGGER.debug("Fetching data from stove")

            primary_data = await self.hass.async_add_executor_job(
                self.api.getMessageInfo
            )
            if primary_data is None:
                raise UpdateFailed("Failed to get primary data from stove (checksum error or no response)")

            secondary_data = await self.hass.async_add_executor_job(
                self.api.getMessage2Info
            )
            if secondary_data is None:
                raise UpdateFailed("Failed to get secondary data from stove (checksum error or no response)")

            return {
                API_DATA_LOOKUP_STOVE_STATUS: primary_data.getStatus(),
                API_DATA_LOOKUP_POWER_STATUS: primary_data.isOn(),
                API_DATA_LOOKUP_ECO_MODE: primary_data.isEcoMode(),
                API_DATA_LOOKUP_AMBIENT_TEMPERATURE: primary_data.getAmbientTemperature(),
                API_DATA_LOOKUP_DESIRED_AMBIENT_TEMPERATURE: primary_data.getDesiredAmbientTemperature(),
                API_DATA_LOOKUP_DESIRED_AMBIENT_TEMPERATURE_MIN: primary_data.getDesiredAmbientTemperatureMin(),
                API_DATA_LOOKUP_DESIRED_AMBIENT_TEMPERATURE_MAX: primary_data.getDesiredAmbientTemperatureMax(),
                API_DATA_LOOKUP_SMOKE_TEMPERATURE: primary_data.getSmokeTemperature(),
                API_DATA_LOOKUP_POWER_PERCENTAGE: primary_data.getPowerPercentage(),
                API_DATA_LOOKUP_SMOKE_FAN_RPM: primary_data.getSmokeFanRpm(),
                API_DATA_LOOKUP_FAN1_PERCENTAGE: secondary_data.getFan1Percentage(),
            }

        except Exception as err:
            # Note: If authentication is added in the future, catch the auth error
            # and raise ConfigEntryAuthFailed to trigger a reauth flow.
            raise UpdateFailed(f"Error communicating with API: {err}") from err
