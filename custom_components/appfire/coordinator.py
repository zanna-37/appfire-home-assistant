"""Platform for number integration."""
from __future__ import annotations
from homeassistant.components.light import LightEntity
from homeassistant.core import callback
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)
from datetime import timedelta
import logging

from .const import DOMAIN

from .const import API_DATA_LOOKUP_STOVE_STATUS
from .const import API_DATA_LOOKUP_POWER_STATUS
from .const import API_DATA_LOOKUP_ECO_MODE
from .const import API_DATA_LOOKUP_AMBIENT_TEMPERATURE
from .const import API_DATA_LOOKUP_DESIRED_AMBIENT_TEMPERATURE
from .const import API_DATA_LOOKUP_DESIRED_AMBIENT_TEMPERATURE_MIN
from .const import API_DATA_LOOKUP_DESIRED_AMBIENT_TEMPERATURE_MAX
from .const import API_DATA_LOOKUP_SMOKE_TEMPERATURE
from .const import API_DATA_LOOKUP_POWER_PERCENTAGE
from .const import API_DATA_LOOKUP_SMOKE_FAN_RPM
from .const import API_DATA_LOOKUP_FAN1_PERCENTAGE

from .lib.appfire_client.appfire import AppFire

_LOGGER = logging.getLogger(__name__)


class MyCoordinator(DataUpdateCoordinator):
    """My custom coordinator."""

    def __init__(self, hass, stoveName, stoveSerial, appFireApi):
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name="AppFireCoordinator",
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(seconds=30),
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
            dataInfo2 = await self.hass.async_add_executor_job(
                self.appFireApi.getMessage2Info
            )

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

        # except ApiAuthError as err: # TODO zanna
        #     # Raising ConfigEntryAuthFailed will cancel future updates
        #     # and start a config flow with SOURCE_REAUTH (async_step_reauth)
        #     raise ConfigEntryAuthFailed from err
        # except ApiError as err: # TODO zanna
        #     raise UpdateFailed(f"Error communicating with API: {err}")
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err
