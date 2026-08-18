# Overdrive BYD v1.2.0

## Home Assistant control UX rebuild

This release uses the Home Assistant entity pattern from `hass-byd-vehicle` while keeping the official OverDrive MQTT `/set` protocol as the command transport.

### New visible command buttons

- Open / Close / Stop Windows
- Vent Windows
- Open / Close / Stop Tailgate
- Climate On / Off
- Start Charging Now
- Fold / Unfold Mirrors
- Open / Close / Stop Sunroof
- Open / Close / Stop Sunshade

These are normal Home Assistant button entities and should appear directly in the BYD Vehicle device page under Controls.

### Existing rich controls retained

- Climate entity with target temperature and fan speed
- Window, tailgate, sunroof and sunshade cover entities
- Seat heating / ventilation selects
- Steering-wheel heating and vehicle switches
- Drive mode, regen, steering and brake selects
- Charge-limit and ambient-light number entities
- ADAS and vehicle-setting controls

### MQTT protocol

Commands use the official OverDrive topics:

- `<base>/<key>/set`
- `<base>/climate/<subcommand>/set`

with QoS 0 and retain disabled.

### Required OverDrive settings

For OverDrive to accept MQTT commands, enable both **Home Assistant Discovery** and **Allow vehicle control** on the MQTT connection.

### Lock / unlock

The uploaded `hass-byd-vehicle` project supports lock/unlock through BYD cloud APIs. The current OverDrive MQTT `VehicleControlCatalog` does not register a lock/unlock entity, even though OverDrive itself contains lock/unlock commands elsewhere. v1.2.0 therefore does not publish an unsupported MQTT lock command.
