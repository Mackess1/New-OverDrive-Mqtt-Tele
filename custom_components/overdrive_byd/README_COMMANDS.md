# OverDrive MQTT controls

v1.2.0 uses the current OverDrive vehicle-control protocol implemented by `VehicleControlCatalog` and `MqttCommandRouter`.

## Topic format

For a telemetry base such as:

`overdrive/vehicle/telemetry`

controls publish to:

`overdrive/vehicle/telemetry/<control_key>/set`

Composite climate controls use:

- `overdrive/vehicle/telemetry/climate/mode/set`
- `overdrive/vehicle/telemetry/climate/temperature/set`
- `overdrive/vehicle/telemetry/climate/fan_mode/set`

Messages are not retained.

## Required OverDrive option

Enable both **Home Assistant Discovery** and **Allow vehicle control** for the MQTT connection in OverDrive. The app intentionally does not enable the MQTT control router unless both options are enabled.

## Examples

- Windows down: `.../windows_all/set` → `OPEN`
- Windows up: `.../windows_all/set` → `CLOSE`
- Stop a cover: `.../tailgate/set` → `STOP`
- Vent windows: `.../windows_vent/set` → `PRESS`
- Climate on: `.../climate/mode/set` → `auto`
- Climate off: `.../climate/mode/set` → `off`
- Climate target: `.../climate/temperature/set` → `22`
- Fan: `.../climate/fan_mode/set` → `1` through `7`
- Driver seat heat: `.../seat_heat_driver/set` → `off`, `low`, or `high`
- Fold mirrors: `.../mirror_fold/set` → `1`; unfold → `0`
- Drive mode: `.../drive_mode/set` → `normal`, `eco`, or `sport`
- Regen: `.../regen_level/set` → `standard` or `high`

OverDrive remains responsible for capability checks, motion/safety gates, and SDK/cloud routing.
