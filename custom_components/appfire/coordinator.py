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

    def __init__(self, hass, stoveName, stoveSerial, appFireApi, polling_interval: int):
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name="AppFireCoordinator",
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(seconds=polling_interval),
        )
        self.appFireApi = appFireApi
        self.stoveName = stoveName
        self.stoveSerial = stoveSerial

    def getStoveNameOrSerial(self):
        if self.stoveName is not None:
            return self.stoveName
        else:
            return self.stoveSerial

    async def _async_update_data(self):
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        try:
            _LOGGER.debug("Entering _async_update_data")

            dataInfo = await self.hass.async_add_executor_job(
                self.appFireApi.getMessageInfo
            )
            if dataInfo is None:
                raise UpdateFailed("Failed to get primary data from stove (checksum error or no response)")

            dataInfo2 = await self.hass.async_add_executor_job(
                self.appFireApi.getMessage2Info
            )
            if dataInfo2 is None:
                raise UpdateFailed("Failed to get secondary data from stove (checksum error or no response)")

            data = {}
            data[API_DATA_LOOKUP_STOVE_STATUS] = dataInfo.getStatus()
            data[API_DATA_LOOKUP_POWER_STATUS] = dataInfo.isOn()
            data[API_DATA_LOOKUP_ECO_MODE] = dataInfo.isEcoMode()
            data[API_DATA_LOOKUP_AMBIENT_TEMPERATURE] = dataInfo.getAmbientTemperature()
            data[
                API_DATA_LOOKUP_DESIRED_AMBIENT_TEMPERATURE
            ] = dataInfo.getDesiredAmbientTemperature()
            data[
                API_DATA_LOOKUP_DESIRED_AMBIENT_TEMPERATURE_MIN
            ] = dataInfo.getDesiredAmbientTemperatureMin()
            data[
                API_DATA_LOOKUP_DESIRED_AMBIENT_TEMPERATURE_MAX
            ] = dataInfo.getDesiredAmbientTemperatureMax()
            data[API_DATA_LOOKUP_SMOKE_TEMPERATURE] = dataInfo.getSmokeTemperature()
            data[API_DATA_LOOKUP_POWER_PERCENTAGE] = dataInfo.getPowerPercentage()
            data[API_DATA_LOOKUP_SMOKE_FAN_RPM] = dataInfo.getSmokeFanRpm()
            data[API_DATA_LOOKUP_FAN1_PERCENTAGE] = dataInfo2.getFan1Percentage()

            _LOGGER.debug(f"Exiting _async_update_data")

            return data

        except Exception as err:
            # Note: If authentication is added in the future, catch the auth error
            # and raise ConfigEntryAuthFailed to trigger a reauth flow.
            raise UpdateFailed(f"Error communicating with API: {err}") from err
