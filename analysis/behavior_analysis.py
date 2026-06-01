import numpy as np
import pandas as pd

from tensorflow.keras.models import load_model


ANOMALY_THRESHOLD = 0.01


def load_files():

    model = load_model(
        "hybrid_missile_ai_model.keras"
    )

    X_test = np.load("X_test.npy")

    y_test = np.load("y_test.npy")

    telemetry_df = pd.read_csv(
        "missile_telemetry_data.csv"
    )

    return model, X_test, y_test, telemetry_df


def detect_anomalies(model, X_test, y_test):

    predictions = model.predict(X_test)

    mse = np.mean(
        np.square(y_test - predictions),
        axis=1
    )

    anomaly_flags = (
        mse > ANOMALY_THRESHOLD
    )

    return mse, anomaly_flags


def generate_ai_insights(df, anomaly_flags):

    insights = []

    anomaly_count = np.sum(anomaly_flags)

    insights.append(
        f"Total anomalies detected: {anomaly_count}"
    )

    avg_temperature = df[
        "thermal_temperature"
    ].mean()

    avg_vibration = df[
        "structural_vibration"
    ].mean()

    avg_navigation_drift = df[
        "navigation_drift"
    ].mean()

    # Thermal analysis

    if avg_temperature > 520:

        insights.append(
            "Elevated thermal activity observed during propulsion operation."
        )

    # Vibration analysis

    if avg_vibration > 0.6:

        insights.append(
            "Structural vibration strongly correlates with propulsion instability."
        )

    # Navigation analysis

    if avg_navigation_drift > 0.08:

        insights.append(
            "Navigation drift increased during high dynamic loading."
        )

    # Mission health analysis

    health_score = df[
        "system_health_score"
    ].mean()

    if health_score < 70:

        insights.append(
            "Overall subsystem health degradation detected."
        )

    return insights


def subsystem_risk_analysis(df):

    risks = {}

    risks["Thermal Risk"] = round(

        df["thermal_temperature"].mean() / 10,

        2
    )

    risks["Structural Risk"] = round(

        df["structural_vibration"].mean() * 100,

        2
    )

    risks["Navigation Risk"] = round(

        df["navigation_drift"].mean() * 1000,

        2
    )

    risks["Power Risk"] = round(

        300 - df["power_voltage"].mean(),

        2
    )

    return risks


def main():

    print("\nLoading AI Assets...\n")

    model, X_test, y_test, telemetry_df = load_files()

    print("AI Assets Loaded Successfully.\n")

    print("Running Behavioral Analysis...\n")

    mse, anomaly_flags = detect_anomalies(

        model,

        X_test,

        y_test
    )

    print("Anomaly Detection Completed.\n")

    insights = generate_ai_insights(

        telemetry_df,

        anomaly_flags
    )

    risks = subsystem_risk_analysis(
        telemetry_df
    )

    print("\n========== AI INSIGHTS ==========\n")

    for insight in insights:

        print(f"- {insight}")

    print("\n========== SUBSYSTEM RISKS ==========\n")

    for key, value in risks.items():

        print(f"{key}: {value}")

    print("\n========== ANOMALY SUMMARY ==========\n")

    print(f"Total Detected Anomalies: {np.sum(anomaly_flags)}")

    print(f"Average Reconstruction Error: {np.mean(mse):.5f}")

    analysis_results = pd.DataFrame({

        "reconstruction_error": mse,

        "anomaly_flag": anomaly_flags
    })

    analysis_results.to_csv(

        "behavior_analysis_results.csv",

        index=False
    )

    print("\nBehavior analysis results saved successfully.\n")


if __name__ == "__main__":

    main()