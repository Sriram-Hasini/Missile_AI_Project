# Advanced Synthetic Missile Telemetry Generator
# DRDL-Style Aerospace Defense Telemetry Intelligence Simulation

from __future__ import annotations

import json
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd


@dataclass
class TelemetryConfig:
    seed: int = 42
    steps: int = 2000
    dt: float = 0.1

    phases: int = 5

    base_noise_std: float = 0.02

    corr_prop_to_therm: float = 0.85
    corr_prop_to_struct: float = 0.75
    corr_struct_to_nav: float = 0.65
    corr_therm_to_control: float = 0.55
    corr_sensors_to_nav: float = 0.45

    anomaly_probability: float = 0.40

    anomaly_min_frac: float = 0.05
    anomaly_max_frac: float = 0.18

    clip: bool = True


def _sigmoid(x):
    return 1 / (1 + np.exp(-x))


def _phase_schedule(steps, phases):
    phase_boundaries = np.linspace(0, steps, phases + 1, dtype=int)

    phase_vector = np.zeros(steps)

    for i in range(phases):
        phase_vector[phase_boundaries[i]:phase_boundaries[i + 1]] = i

    return phase_vector


def generate_synthetic_telemetry(cfg: TelemetryConfig):

    np.random.seed(cfg.seed)

    steps = cfg.steps

    t = np.arange(steps) * cfg.dt

    timestamps = [
        datetime.now() + timedelta(seconds=float(i * cfg.dt))
        for i in range(steps)
    ]

    phase_vector = _phase_schedule(steps, cfg.phases)

    phase_map = {
        0: "Launch",
        1: "Boost",
        2: "Midcourse",
        3: "Guidance",
        4: "Terminal"
    }

    operational_phase = [
        phase_map[int(p)] for p in phase_vector
    ]

    load = (phase_vector + 1) / cfg.phases

    propulsion_osc = (
        1 + 0.15 * np.sin(2 * np.pi * t / 15)
    )

    thermal_spool = _sigmoid(
        (t - t.mean()) / 20
    )

    # ----------------------------
    # Propulsion
    # ----------------------------

    propulsion_pressure = (
        120 + 60 * load * propulsion_osc
    )

    propulsion_thrust = (
        300 + 900 * load * propulsion_osc
    )

    propulsion_fuel_flow = (
        20 + 10 * load + propulsion_pressure * 0.05
    )

    # ----------------------------
    # Thermal
    # ----------------------------

    thermal_temperature = (
        450
        + cfg.corr_prop_to_therm * propulsion_pressure
        + 25 * thermal_spool
    )

    thermal_surface_heat = (
        0.65 * thermal_temperature
    )

    # ----------------------------
    # Structural
    # ----------------------------

    structural_vibration = (
        0.15
        + cfg.corr_prop_to_struct
        * propulsion_pressure / 250
    )

    structural_stress = (
        20
        + structural_vibration * 80
    )

    # ----------------------------
    # Navigation
    # ----------------------------

    navigation_altitude = (
        1000 + 15000 * load
    )

    navigation_velocity = (
        300 + 1200 * load
    )

    navigation_drift = (
        0.02
        + cfg.corr_struct_to_nav
        * structural_vibration * 0.08
    )

    # ----------------------------
    # Guidance
    # ----------------------------

    guidance_trajectory_deviation = (
        0.02
        + thermal_temperature / 10000
    )

    # ----------------------------
    # Control
    # ----------------------------

    control_actuator_latency = (
        0.01
        + cfg.corr_therm_to_control
        * thermal_temperature / 10000
    )

    control_fin_angle = (
        5
        + 10 * np.sin(t / 10)
    )

    # ----------------------------
    # Sensors
    # ----------------------------

    sensors_signal_strength = (
        0.95
        - navigation_drift * 0.3
    )

    sensors_radar_noise = (
        0.1
        + structural_vibration * 0.4
    )

    # ----------------------------
    # Power
    # ----------------------------

    power_voltage = (
        280
        - structural_vibration * 8
    )

    power_current = (
        2
        + load * 4
    )

    # ----------------------------
    # Add Random Noise
    # ----------------------------

    def add_noise(signal, scale=1):
        return signal + np.random.normal(
            0,
            cfg.base_noise_std * scale,
            size=steps
        )

    propulsion_pressure = add_noise(propulsion_pressure, 4)
    propulsion_thrust = add_noise(propulsion_thrust, 10)
    propulsion_fuel_flow = add_noise(propulsion_fuel_flow, 1)

    thermal_temperature = add_noise(thermal_temperature, 6)
    thermal_surface_heat = add_noise(thermal_surface_heat, 4)

    structural_vibration = add_noise(structural_vibration, 0.08)
    structural_stress = add_noise(structural_stress, 2)

    navigation_altitude = add_noise(navigation_altitude, 50)
    navigation_velocity = add_noise(navigation_velocity, 10)
    navigation_drift = add_noise(navigation_drift, 0.01)

    guidance_trajectory_deviation = add_noise(
        guidance_trajectory_deviation,
        0.01
    )

    control_actuator_latency = add_noise(
        control_actuator_latency,
        0.005
    )

    control_fin_angle = add_noise(control_fin_angle, 0.5)

    sensors_signal_strength = add_noise(
        sensors_signal_strength,
        0.02
    )

    sensors_radar_noise = add_noise(
        sensors_radar_noise,
        0.03
    )

    power_voltage = add_noise(power_voltage, 1)
    power_current = add_noise(power_current, 0.2)

    # ----------------------------
    # Mission Status
    # ----------------------------

    mission_status = np.array(
        ["Stable"] * steps
    )

    anomaly_label = np.zeros(steps)

    anomalies = []

    # ----------------------------
    # Inject Anomalies
    # ----------------------------

    if np.random.random() < cfg.anomaly_probability:

        anomaly_types = [
            "Thermal Escalation",
            "Navigation Instability",
            "Power Failure",
            "Propulsion Oscillation"
        ]

        num_anomalies = np.random.randint(1, 3)

        for _ in range(num_anomalies):

            anomaly_type = np.random.choice(anomaly_types)

            width = np.random.randint(
                int(steps * cfg.anomaly_min_frac),
                int(steps * cfg.anomaly_max_frac)
            )

            start = np.random.randint(
                0,
                steps - width
            )

            end = start + width

            anomaly_label[start:end] = 1

            mission_status[start:end] = "Anomaly Detected"

            if anomaly_type == "Thermal Escalation":

                thermal_temperature[start:end] *= 1.25

                structural_vibration[start:end] *= 1.15

                control_actuator_latency[start:end] *= 1.20

            elif anomaly_type == "Navigation Instability":

                navigation_drift[start:end] *= 1.8

                sensors_radar_noise[start:end] *= 1.5

            elif anomaly_type == "Power Failure":

                power_voltage[start:end] *= 0.82

                sensors_signal_strength[start:end] *= 0.75

            elif anomaly_type == "Propulsion Oscillation":

                propulsion_pressure[start:end] *= (
                    1 + 0.15 * np.sin(
                        np.linspace(0, np.pi * 6, width)
                    )
                )

                structural_vibration[start:end] *= 1.25

            anomalies.append({
                "type": anomaly_type,
                "start": int(start),
                "end": int(end)
            })

    # ----------------------------
    # System Health Score
    # ----------------------------

    system_health_score = (
        100
        - structural_vibration * 15
        - navigation_drift * 120
        - thermal_temperature / 40
    )

    system_health_score = np.clip(
        system_health_score,
        0,
        100
    )

    # ----------------------------
    # AI Insight Generation
    # ----------------------------

    ai_insights = []

    if thermal_temperature.mean() > 520:
        ai_insights.append(
            "Thermal escalation detected during propulsion stabilization."
        )

    if structural_vibration.mean() > 0.6:
        ai_insights.append(
            "Structural vibration strongly correlates with propulsion pressure oscillation."
        )

    if navigation_drift.mean() > 0.08:
        ai_insights.append(
            "Navigation drift increased under elevated vibration conditions."
        )

    if power_voltage.mean() < 250:
        ai_insights.append(
            "Power subsystem degradation affecting sensor reliability."
        )

    # ----------------------------
    # Create DataFrame
    # ----------------------------

    df = pd.DataFrame({

        "timestamp": timestamps,
        "operational_phase": operational_phase,

        "propulsion_pressure": propulsion_pressure,
        "propulsion_thrust": propulsion_thrust,
        "propulsion_fuel_flow": propulsion_fuel_flow,

        "thermal_temperature": thermal_temperature,
        "thermal_surface_heat": thermal_surface_heat,

        "structural_vibration": structural_vibration,
        "structural_stress": structural_stress,

        "navigation_altitude": navigation_altitude,
        "navigation_velocity": navigation_velocity,
        "navigation_drift": navigation_drift,

        "guidance_trajectory_deviation":
            guidance_trajectory_deviation,

        "control_actuator_latency":
            control_actuator_latency,

        "control_fin_angle":
            control_fin_angle,

        "sensors_signal_strength":
            sensors_signal_strength,

        "sensors_radar_noise":
            sensors_radar_noise,

        "power_voltage":
            power_voltage,

        "power_current":
            power_current,

        "system_health_score":
            system_health_score,

        "mission_status":
            mission_status,

        "anomaly_label":
            anomaly_label
    })

    # ----------------------------
    # Metadata
    # ----------------------------

    metadata = {

        "anomalies": anomalies,

        "ai_insights": ai_insights,

        "config": cfg.__dict__
    }

    return df, metadata


def main():

    cfg = TelemetryConfig()

    df, metadata = generate_synthetic_telemetry(cfg)

    # Save CSV
    df.to_csv(
        "missile_telemetry_data.csv",
        index=False
    )

    # Save metadata
    with open(
        "telemetry_metadata.json",
        "w"
    ) as f:

        json.dump(
            metadata,
            f,
            indent=4
        )

    print("\nTelemetry Dataset Generated Successfully.\n")

    print(df.head())

    print("\nAI Insights:\n")

    for insight in metadata["ai_insights"]:
        print(f"- {insight}")

    print("\nAnomalies:\n")

    print(metadata["anomalies"])


if __name__ == "__main__":
    main()