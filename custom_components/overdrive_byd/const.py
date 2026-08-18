from homeassistant.const import Platform

DOMAIN = "overdrive_byd"

DEFAULT_NAME = "BYD Vehicle"
DEFAULT_TELEMETRY_TOPIC = "overdrive/vehicle/telemetry"
DEFAULT_AVAILABILITY_TOPIC = "overdrive/vehicle/telemetry/availability"
DEFAULT_CONTROL_TOPIC = "overdrive/vehicle/telemetry"

CONF_TELEMETRY_TOPIC = "telemetry_topic"
CONF_AVAILABILITY_TOPIC = "availability_topic"
CONF_CONTROL_TOPIC = "control_topic"

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.DEVICE_TRACKER,
]

INVALID_VALUES = {
    65535,
    1048575,
    104857.5,
    -10011,
    -2147482648,
}
