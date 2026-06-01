import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


# ----------------------------------------
# PAGE CONFIG
# ----------------------------------------

st.set_page_config(

    page_title="Missile AI Intelligence Dashboard",

    layout="wide"
)


# ----------------------------------------
# LOAD DATA
# ----------------------------------------

telemetry_df = pd.read_csv(
    "missile_telemetry_data.csv"
)

analysis_df = pd.read_csv(
    "behavior_analysis_results.csv"
)


# ----------------------------------------
# HEADER
# ----------------------------------------

st.title("🚀 Missile AI Intelligence Dashboard")

st.markdown("""
Advanced AI-Driven Missile Subsystem
Telemetry & Behavioral Intelligence Platform
""")


# ----------------------------------------
# KPI CARDS
# ----------------------------------------

avg_health = round(
    telemetry_df["system_health_score"].mean(),
    2
)

max_temp = round(
    telemetry_df["thermal_temperature"].max(),
    2
)

avg_vibration = round(
    telemetry_df["structural_vibration"].mean(),
    3
)

total_anomalies = int(
    analysis_df["anomaly_flag"].sum()
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "System Health Score",
    avg_health
)

col2.metric(
    "Maximum Temperature",
    max_temp
)

col3.metric(
    "Avg Structural Vibration",
    avg_vibration
)

col4.metric(
    "Detected Anomalies",
    total_anomalies
)


# ----------------------------------------
# OPERATIONAL PHASE DISTRIBUTION
# ----------------------------------------

st.subheader("Operational Phase Distribution")

phase_counts = telemetry_df[
    "operational_phase"
].value_counts()

fig_phase = px.pie(

    names=phase_counts.index,

    values=phase_counts.values,

    title="Mission Operational Phases"
)

st.plotly_chart(
    fig_phase,
    use_container_width=True
)


# ----------------------------------------
# TEMPERATURE GRAPH
# ----------------------------------------

st.subheader("Thermal Temperature Monitoring")

fig_temp = px.line(

    telemetry_df,

    y="thermal_temperature",

    title="Thermal Temperature Variation"
)

st.plotly_chart(
    fig_temp,
    use_container_width=True
)


# ----------------------------------------
# PROPULSION PRESSURE GRAPH
# ----------------------------------------

st.subheader("Propulsion Pressure Monitoring")

fig_pressure = px.line(

    telemetry_df,

    y="propulsion_pressure",

    title="Propulsion Pressure Dynamics"
)

st.plotly_chart(
    fig_pressure,
    use_container_width=True
)


# ----------------------------------------
# STRUCTURAL VIBRATION
# ----------------------------------------

st.subheader("Structural Vibration Analysis")

fig_vibration = px.line(

    telemetry_df,

    y="structural_vibration",

    title="Structural Vibration Behavior"
)

st.plotly_chart(
    fig_vibration,
    use_container_width=True
)


# ----------------------------------------
# NAVIGATION DRIFT
# ----------------------------------------

st.subheader("Navigation Drift Monitoring")

fig_nav = px.line(

    telemetry_df,

    y="navigation_drift",

    title="Navigation Drift Analysis"
)

st.plotly_chart(
    fig_nav,
    use_container_width=True
)


# ----------------------------------------
# ANOMALY VISUALIZATION
# ----------------------------------------

st.subheader("AI Anomaly Detection")

anomaly_indices = analysis_df[
    analysis_df["anomaly_flag"] == True
].index

fig_anomaly = go.Figure()

fig_anomaly.add_trace(

    go.Scatter(

        y=analysis_df[
            "reconstruction_error"
        ],

        mode="lines",

        name="Reconstruction Error"
    )
)

fig_anomaly.add_trace(

    go.Scatter(

        x=anomaly_indices,

        y=analysis_df.loc[
            anomaly_indices,
            "reconstruction_error"
        ],

        mode="markers",

        marker=dict(

            color="red",

            size=8
        ),

        name="Detected Anomalies"
    )
)

fig_anomaly.update_layout(

    title="AI-Based Anomaly Detection",

    xaxis_title="Sequence Index",

    yaxis_title="Reconstruction Error"
)

st.plotly_chart(
    fig_anomaly,
    use_container_width=True
)


# ----------------------------------------
# CORRELATION HEATMAP
# ----------------------------------------

st.subheader("Subsystem Correlation Heatmap")

numeric_df = telemetry_df.select_dtypes(
    include=np.number
)

corr_matrix = numeric_df.corr()

fig_heatmap = px.imshow(

    corr_matrix,

    text_auto=True,

    aspect="auto",

    title="Subsystem Correlation Matrix"
)

st.plotly_chart(
    fig_heatmap,
    use_container_width=True
)


# ----------------------------------------
# AI INSIGHTS
# ----------------------------------------

st.subheader("AI Behavioral Insights")

insights = [

    "Thermal subsystem exhibits elevated operational activity.",

    "Structural vibration strongly correlates with propulsion instability.",

    "Navigation drift increased under dynamic load conditions.",

    "AI model detected multiple abnormal subsystem behaviors.",

    "Subsystem risk levels indicate moderate operational instability."
]

for insight in insights:

    st.success(insight)


# ----------------------------------------
# RAW DATA VIEW
# ----------------------------------------

st.subheader("Telemetry Dataset Preview")

st.dataframe(
    telemetry_df.head(50)
)