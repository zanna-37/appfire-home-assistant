"""Constants for the AppFire integration."""

DOMAIN = "appfire"

INTEGRATION_VERSION = "v0.1.0"
MIN_REQUIRED_HA_VERSION = "2023.11.0"

CONF_STOVE_NAME = "stove_name"
CONF_SERIAL = "serial"
CONF_IP = "ip"
CONF_PORT = "port"
CONF_POLLING_INTERVAL = "polling_interval"

DEFAULT_SCAN_INTERVAL_S = 60
DEFAULT_PORT = 5001

API_DATA_LOOKUP_STOVE_STATUS = "status"
API_DATA_LOOKUP_POWER_STATUS = "power_status"
API_DATA_LOOKUP_ECO_MODE = "eco_mode"
# API_DATA_LOOKUP_CRONO_MODE = "crono_mode"
API_DATA_LOOKUP_AMBIENT_TEMPERATURE = "ambient_temperature"
API_DATA_LOOKUP_DESIRED_AMBIENT_TEMPERATURE = "desired_ambient_temperature"
API_DATA_LOOKUP_DESIRED_AMBIENT_TEMPERATURE_MIN = "desired_ambient_temperature_min"
API_DATA_LOOKUP_DESIRED_AMBIENT_TEMPERATURE_MAX = "desired_ambient_temperature_max"
API_DATA_LOOKUP_SMOKE_TEMPERATURE = "smoke_temperature"
API_DATA_LOOKUP_POWER_PERCENTAGE = "power_percentage"
API_DATA_LOOKUP_SMOKE_FAN_RPM = "smoke_fan_rpm"
API_DATA_LOOKUP_FAN1_PERCENTAGE = "fan1_percentage"
