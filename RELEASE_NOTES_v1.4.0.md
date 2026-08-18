# Overdrive BYD v1.4.0

## Explicit command routing + MQTT diagnostics

This release makes the OverDrive command base a first-class configuration value instead of silently deriving it from the telemetry topic.

### New configuration field

- **Control topic** (default: `overdrive/vehicle/telemetry`)

The integration now builds all OverDrive command topics from this explicit base, for example:

- `overdrive/vehicle/telemetry/windows_all/set`
- `overdrive/vehicle/telemetry/climate/mode/set`
- `overdrive/vehicle/telemetry/tailgate/set`

### New MQTT Control Test

A safe **MQTT Control Test** diagnostic button is published through Home Assistant MQTT Discovery. It publishes only to an integration-local loopback topic and does not command the vehicle.

After pressing it, the integration's **MQTT Control Test Result** sensor should change to:

`received: PING`

This proves the command button can publish through Home Assistant to the MQTT broker and back to the integration. If this test works but the car commands do not, the remaining problem is between the command topic/payload and OverDrive vehicle control rather than Home Assistant MQTT itself.

### Other changes

- Config flow schema bumped to version 2.
- MQTT topic strings are normalized to remove trailing slashes.
- Control discovery logs the configured command base.
- Version bumped to 1.4.0.
