# Overdrive BYD v1.3.0

## Control discovery architecture fix

v1.3.0 stops relying on custom Home Assistant control platforms for command visibility.
Instead, the integration publishes retained native Home Assistant MQTT Discovery button
entities which send commands directly to OverDrive's official `<telemetry>/<key>/set`
and `<telemetry>/<key>/<sub>/set` topics.

This release deliberately keeps the custom integration platforms limited to telemetry
(sensor, binary_sensor, device_tracker) so a failure in climate/cover/select/number/etc.
cannot prevent command controls from appearing.

### Requirements
- Home Assistant MQTT integration installed and connected to the same broker.
- MQTT Discovery enabled in Home Assistant (default discovery prefix: `homeassistant`).
- In OverDrive, Home Assistant Discovery enabled.
- In OverDrive, Allow vehicle control enabled.

### Added MQTT Discovery commands
Climate on/off; windows open/close/stop/vent; tailgate open/close/stop;
sunroof and sunshade open/close/stop; start charging; mirror toggle; steering wheel heat;
DRL; hazards; child lock; wireless charger; seat heating/ventilation cycle; drive mode,
regen, steering assist and brake-feel cycle buttons.
