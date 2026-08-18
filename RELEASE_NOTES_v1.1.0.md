# Overdrive BYD v1.1.0

## Vehicle controls

This release adds Home Assistant control entities using OverDrive's official MQTT control protocol from `VehicleControlCatalog`.

Commands are published to:

- `<telemetry_base>/<key>/set`
- `<telemetry_base>/<key>/<sub>/set` for composite climate controls

Control messages are QoS 0 and **never retained**, matching OverDrive's inbound command safety requirements.

### Added control platforms

- Climate: power/mode, target temperature 17–33 °C, fan 1–7
- Covers: all windows, tailgate, sunroof, sunshade, including STOP
- Buttons: vent windows, recall driver seat, start charging now
- Seat heating and ventilation for driver/passenger
- Steering wheel heat
- DRL, hazards, ambient lighting
- Charge limit enable and 50–100% setpoint
- Smart charging and charging schedule text control
- Child lock, mirror fold/auto-fold, wireless chargers
- Drive mode, powertrain mode, battery hold, regen, steering assist, brake feel
- Infotainment orientation and native camera view
- ADAS controls exposed by the official OverDrive catalog
- Curated BYD CAN-backed settings exposed by `BydCarSettings.registry()`

## Important protocol correction

Older custom-control files sent JSON to `.../command`. The official current OverDrive release does not use that path for Home Assistant vehicle controls. v1.1.0 uses the same `/set` topic layout as OverDrive's own Home Assistant discovery implementation.

## OverDrive setup

In OverDrive's MQTT connection settings, enable **Allow vehicle control**. If that option is disabled, telemetry will continue to work but OverDrive will not subscribe to or execute vehicle-control commands.

Some controls are trim/firmware dependent. OverDrive performs its own capability and safety checks and may refuse unsupported commands.
