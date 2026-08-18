from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class SwitchDef:
    key: str
    name: str
    icon: str
    state_key: str | None = None
    on: str = "1"
    off: str = "0"
    category: str | None = None


@dataclass(frozen=True)
class SelectDef:
    key: str
    name: str
    icon: str
    options: Sequence[str]
    state_key: str | None = None
    category: str | None = None
    decoder: str | None = None


@dataclass(frozen=True)
class NumberDef:
    key: str
    name: str
    icon: str
    minimum: float
    maximum: float
    step: float
    state_key: str | None = None
    unit: str | None = None
    category: str | None = None


@dataclass(frozen=True)
class ButtonDef:
    key: str
    name: str
    icon: str


@dataclass(frozen=True)
class TextDef:
    key: str
    name: str
    icon: str
    category: str | None = None


SWITCHES = [
    SwitchDef("steering_heat", "Steering Wheel Heating", "mdi:steering", "steering_wheel_heat"),
    SwitchDef("drl", "Daytime Running Lights", "mdi:car-light-dimmed", "light_drl"),
    SwitchDef("hazard", "Hazard Lights", "mdi:car-light-alert", "light_hazard"),
    SwitchDef("ambient_power", "Ambient Lights", "mdi:track-light", "ambient_enabled", category="config"),
    SwitchDef("adas_slw", "Speed Limit Warning", "mdi:speedometer-slow", "speed_limit_warning", category="config"),
    SwitchDef("esp_control", "Stability Control (ESP)", "mdi:car-traction-control", "esp_state", category="config"),
    SwitchDef("itac", "iTAC (Torque Control)", "mdi:car-cog", category="config"),
    SwitchDef("adas_cpd", "Child Presence Detection", "mdi:car-child-seat", "child_presence_detection", category="config"),
    SwitchDef("adas_bsd", "Blind Spot Detection", "mdi:car-side", category="config"),
    SwitchDef("adas_tsr", "Traffic Sign Recognition", "mdi:sign-real-estate", category="config"),
    SwitchDef("adas_rcta", "Rear Cross Traffic Alert", "mdi:car-back", category="config"),
    SwitchDef("adas_fcta", "Front Cross Traffic Alert", "mdi:car", category="config"),
    SwitchDef("adas_tla", "Traffic Light Attention", "mdi:traffic-light", category="config"),
    SwitchDef("adas_dow", "Door Open Warning", "mdi:car-door", category="config"),
    SwitchDef("adas_rcw", "Rear Collision Warning", "mdi:car-back", category="config"),
    SwitchDef("adas_islc", "Speed Limit Control", "mdi:speedometer", category="config"),
    SwitchDef("adas_elka", "Emergency Lane Keeping", "mdi:road-variant", category="config"),
    SwitchDef("adas_rctb", "Rear Cross Traffic Brake", "mdi:car-brake-alert", category="config"),
    SwitchDef("adas_fctb", "Front Cross Traffic Brake", "mdi:car-brake-alert", category="config"),
    SwitchDef("adas_aeb", "Automatic Emergency Braking", "mdi:car-brake-abs", category="config"),
    SwitchDef("charge_cap_enabled", "Charge Limit", "mdi:battery-charging-100", "charge_cap_enabled", category="config"),
    SwitchDef("smart_charging", "Smart Charging", "mdi:battery-clock", category="config"),
    SwitchDef("child_lock", "Child Lock", "mdi:car-door-lock", category="config"),
    SwitchDef("mirror_fold", "Fold Mirrors", "mdi:car-side"),
    SwitchDef("mirror_auto_follow_up", "Auto Fold / Unfold Mirrors", "mdi:car-side", category="config"),
    SwitchDef("wireless_charging", "Phone Wireless Charger", "mdi:battery-charging-wireless"),
    SwitchDef("wireless_charging_left", "Wireless Charger (Left)", "mdi:battery-charging-wireless"),
    SwitchDef("wireless_charging_right", "Wireless Charger (Right)", "mdi:battery-charging-wireless"),
    # Curated CAN-backed BYD car settings from BydCarSettings.registry().
    SwitchDef("setting_children_lock", "Child Lock Setting", "mdi:car-door-lock", "setting_children_lock", category="config"),
    SwitchDef("setting_shut_window_after_locking", "Close Windows on Lock", "mdi:window-closed-variant", "setting_shut_window_after_locking", category="config"),
    SwitchDef("setting_auto_mirror_for_lock", "Fold Mirrors on Lock", "mdi:car-side", "setting_auto_mirror_for_lock", category="config"),
    SwitchDef("setting_rain_close_window", "Auto-close Windows in Rain", "mdi:weather-rainy", "setting_rain_close_window", category="config"),
    SwitchDef("setting_esp_assist", "ESP Setting", "mdi:car-traction-control", "setting_esp_assist", category="config"),
    SwitchDef("setting_avh_assist", "Auto Vehicle Hold", "mdi:car-brake-hold", "setting_avh_assist", category="config"),
    SwitchDef("setting_aeb", "AEB Setting", "mdi:car-emergency", "setting_aeb", category="config"),
    SwitchDef("setting_lane_keeping", "Lane Keeping Assist Setting", "mdi:road-variant", "setting_lane_keeping", category="config"),
    SwitchDef("setting_daytime_running_lamp", "Daytime Running Lights Setting", "mdi:car-light-dimmed", "setting_daytime_running_lamp", category="config"),
]

SELECTS = [
    SelectDef("seat_heat_driver", "Driver Seat Heating", "mdi:car-seat-heater", ("off", "low", "high"), "seat_heat_driver"),
    SelectDef("seat_heat_passenger", "Passenger Seat Heating", "mdi:car-seat-heater", ("off", "low", "high"), "seat_heat_passenger"),
    SelectDef("seat_vent_driver", "Driver Seat Ventilation", "mdi:car-seat-cooler", ("off", "low", "high"), "seat_vent_driver"),
    SelectDef("seat_vent_passenger", "Passenger Seat Ventilation", "mdi:car-seat-cooler", ("off", "low", "high"), "seat_vent_passenger"),
    SelectDef("lane_assist", "Lane Assist", "mdi:road-variant", ("0", "1", "2", "3"), category="config"),
    SelectDef("adas_fcw", "Forward Collision Warning", "mdi:car-emergency", ("0", "1", "2", "3"), category="config"),
    SelectDef("infotainment_rotation", "Infotainment Orientation", "mdi:screen-rotation", ("horizontal", "vertical"), category="config"),
    SelectDef("native_camera_view", "Native Camera View", "mdi:camera-switch", ("front", "front_wide", "rear", "rear_wide", "left", "right", "left_right")),
    SelectDef("drive_mode", "Drive Mode", "mdi:car-shift-pattern", ("normal", "eco", "sport"), "op_mode", decoder="drive_mode"),
    SelectDef("powertrain_mode", "Powertrain Mode", "mdi:engine", ("ev", "hev"), "energy_mode", decoder="powertrain_mode"),
    SelectDef("hold_battery", "Engine Mode (HEV)", "mdi:engine", ("on",), "energy_mode", decoder="hold_battery"),
    SelectDef("battery_hold", "Battery Hold", "mdi:battery-lock", ("off", "at_current", "at_floor")),
    SelectDef("regen_level", "Energy Recuperation", "mdi:battery-charging-medium", ("standard", "high")),
    SelectDef("steering_mode", "Steering Assist", "mdi:steering", ("comfort", "sport")),
    SelectDef("brake_feel", "Brake Feel", "mdi:car-brake-alert", ("comfort", "sport")),
    SelectDef("setting_auto_lock_time", "Auto-lock Delay", "mdi:lock-clock", ("0", "10", "30", "60", "120"), "setting_auto_lock_time", category="config"),
    SelectDef("setting_energy_recycle_setting", "Regen Level Setting", "mdi:battery-charging", ("0", "1", "2", "3"), "setting_energy_recycle_setting", category="config"),
    SelectDef("setting_power_management", "Drive Mode Setting", "mdi:car-sports", ("0", "1", "2"), "setting_power_management", category="config"),
    SelectDef("setting_auto_wipe", "Auto Wiper Sensitivity", "mdi:wiper", ("0", "1", "2", "3"), "setting_auto_wipe", category="config"),
    SelectDef("setting_charge_limit", "Charge Limit Setting %", "mdi:battery-charging-80", ("50", "60", "70", "80", "90", "100"), "setting_charge_limit", category="config"),
    SelectDef("setting_unit_temperature", "Temperature Unit", "mdi:temperature-celsius", ("0", "1"), "setting_unit_temperature", category="config"),
]

NUMBERS = [
    NumberDef("ambient_colour", "Ambient Lights Colour", "mdi:format-color-fill", 1, 31, 1, "ambient_colour", category="config"),
    NumberDef("ambient_brightness", "Ambient Lights Brightness", "mdi:brightness-6", 0, 100, 1, "ambient_brightness", "%", "config"),
    NumberDef("charge_cap_percent", "Charge Limit %", "mdi:battery-charging-80", 50, 100, 5, "charge_cap_percent", "%", "config"),
    NumberDef("setting_lighting_ambient_brightness", "Ambient Light Brightness Setting", "mdi:track-light", 0, 10, 1, "setting_lighting_ambient_brightness", category="config"),
]

BUTTONS = [
    ButtonDef("windows_vent", "Vent Windows", "mdi:car-door"),
    ButtonDef("seat_memory_driver", "Recall Driver Seat", "mdi:seat-recline-extra"),
    ButtonDef("start_charging_now", "Start Charging Now", "mdi:battery-charging"),
]

TEXTS = [
    TextDef("remote_climate_start", "Remote Climate Start", "mdi:air-conditioner", "config"),
    TextDef("remote_climate_schedule", "Remote Climate Schedule", "mdi:calendar-clock", "config"),
    TextDef("smart_charge_schedule", "Smart Charging Schedule", "mdi:calendar-clock", "config"),
]
