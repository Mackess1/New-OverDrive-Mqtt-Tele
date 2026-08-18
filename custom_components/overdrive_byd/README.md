# Overdrive BYD MQTT

## Current release: v1.4.0

Home Assistant custom integration for BYD vehicle telemetry and controls through OverDrive MQTT.

## What v1.4.0 does

- Reads OverDrive telemetry from individual MQTT subtopics under `overdrive/vehicle/telemetry`.
- Keeps compatibility with aggregate JSON telemetry payloads.
- Creates Home Assistant sensors, binary sensors, and a device tracker.
- Filters known BYD/OverDrive invalid sentinel values instead of exposing them as real readings.
- Adds an explicit **Control topic** during setup.
- Publishes vehicle command buttons through native Home Assistant MQTT Discovery.
- Adds a safe **MQTT Control Test** button and result sensor for diagnostics.

## Default configuration

When adding the integration, use:

- **Name:** `BYD Vehicle`
- **Telemetry topic:** `overdrive/vehicle/telemetry`
- **Availability topic:** `overdrive/vehicle/telemetry/availability`
- **Control topic:** `overdrive/vehicle/telemetry`

The control topic is the base used to build OverDrive command topics such as:

```text
overdrive/vehicle/telemetry/windows_all/set
overdrive/vehicle/telemetry/climate/mode/set
overdrive/vehicle/telemetry/tailgate/set
```

## Controls

v1.4.0 publishes controls as native Home Assistant MQTT Discovery button entities. They appear on the MQTT integration as the device **BYD Vehicle Controls**.

Examples include climate on/off, windows, tailgate, sunroof, sunshade, charging, mirrors, steering-wheel heat, lights, child lock, wireless charging, seat heat/ventilation, drive mode, regeneration, steering mode, and brake feel.

## MQTT Control Test

The **MQTT Control Test** button does not command the vehicle. It publishes `PING` to an integration-local MQTT loopback topic.

After pressing it, the **MQTT Control Test Result** sensor should show:

```text
received: PING
```

If this works but vehicle controls do not, Home Assistant and the MQTT broker are working and the remaining issue is the OverDrive command topic/payload or OverDrive vehicle-control configuration.

## Installation

### HACS

Add the repository as a custom **Integration**, install it, and restart Home Assistant.

### Manual

Copy:

```text
custom_components/overdrive_byd
```

into:

```text
/config/custom_components/
```

Then restart Home Assistant.

If upgrading from an older version and the setup form does not show **Control topic**, remove and re-add the integration after restarting.

## OverDrive requirements

For vehicle commands, enable the relevant MQTT/Home Assistant discovery and vehicle-control options in OverDrive so it subscribes to the `/set` command topics.

## License

MIT.
