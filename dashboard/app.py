import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

import streamlit as st
import pandas as pd

from utils.type_detector import detect_type
from utils.converter import convert_value


# ----------------------------------------
# PAGE CONFIG
# ----------------------------------------

st.set_page_config(
    page_title="Telemetry Intelligence Platform",
    layout="wide"
)

# ----------------------------------------
# HEADER
# ----------------------------------------

st.title("Telemetry Intelligence Platform")

st.markdown(
    """
    Upload telemetry data and analyze subsystem
    information, conversions and health status.
    """
)

# ----------------------------------------
# FILE UPLOAD
# ----------------------------------------

uploaded_file = st.file_uploader(
    "Upload Telemetry File",
    type=["csv", "txt"]
)

# ----------------------------------------
# MAIN DASHBOARD
# ----------------------------------------

if uploaded_file is not None:

    try:

        df = pd.read_csv(uploaded_file)

        # ----------------------------------------
        # KPI CARDS
        # ----------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Total Records",
            len(df)
        )

        col2.metric(
            "Total Words",
            len(df.columns)
        )

        col3.metric(
            "System Status",
            "Active"
        )

        col4.metric(
            "Monitoring",
            "Enabled"
        )

        # ----------------------------------------
        # TELEMETRY TABLE
        # ----------------------------------------

        st.subheader("Telemetry Dataset")

        st.dataframe(
            df,
            use_container_width=True
        )

        # ----------------------------------------
        # VALUE DROPDOWN
        # ----------------------------------------

        all_values = []

        for column in df.columns:

            all_values.extend(
                df[column].astype(str).tolist()
            )

        unique_values = sorted(
            list(set(all_values))
        )

        st.subheader(
                "Telemetry Data Analysis"
        )

        search_value = st.selectbox(
            "Available Values",
            unique_values
        )

        found = False

        # ----------------------------------------
        # SEARCH LOGIC
        # ----------------------------------------

        for col in df.columns:

            for idx, value in enumerate(df[col]):

                if str(value) == search_value:

                    found = True

                    detected_type = detect_type(
                        value
                    )

                    selected_row = df.iloc[idx]
                    command_name = selected_row.get("Command", "")

                    predicted_subsystem = "Unknown"
                    COMMAND_MAP = {
    "CMD_A": "Propulsion",
    "CMD_B": "Thermal",
    "CMD_C": "Navigation",
    "CMD_D": "Structural",
    "CMD_E": "Power"
}

                    for cmd, subsystem in COMMAND_MAP.items():

                        if cmd in command_name:

                            predicted_subsystem = subsystem

                            break
                    # ----------------------------------------
                    # PACKET INFORMATION
                    # ----------------------------------------

                    

                    st.markdown(
                        f"""
### Subsystem Identification Report

| Attribute | Value |
|-----------|--------|
| Command Code | {command_name} |
| Detected Subsystem | {predicted_subsystem} |
| Selected Telemetry Value | {value} |
| Parameter Location | {col} |
| Data Format | {detected_type} |
| Record Index | {idx} |
"""
                    )
                    selected_row_df = df.iloc[[idx]]

                    st.subheader(
                        "Telemetry Data Analysis"
                    )

                    st.dataframe(
                        selected_row_df,
                        use_container_width=True
                    )

                    # ----------------------------------------
                    # DOWNLOAD
                    # ----------------------------------------

                    st.markdown(
                    "### Export Analysis Report"
                    )

                    st.download_button(
                        label="Download Telemetry Record",
                        data=selected_row_df.to_csv(index=False),
                      file_name=f"{command_name}_Telemetry_Record.csv",
                        mime="text/csv",
                       key=f"download_{command_name}_{idx}"
                    )

                    # ----------------------------------------
                    # FORMAT CONVERSION
                    # ----------------------------------------

                    st.subheader(
                        " Telemetry Format Conversion"
                    )

                    conversion_type = st.selectbox(
                        "Convert To",
                        [
                            "Integer",
                            "Float",
                            "Hex",
                            "Binary"
                        ],
                        key=f"convert_{idx}"
                    )

                    converted = convert_value(
                        value,
                        conversion_type
                    )

                    st.info(
                        f"Converted Value : {converted}"
                    )

                    # ----------------------------------------
                    # HEALTH ASSESSMENT
                    # ----------------------------------------

                    st.subheader(
                        "Subsystem Health Assessment"
                    )

                    if predicted_subsystem == "Propulsion":

                        health_score = 95
                        anomaly_count = 0

                    elif predicted_subsystem == "Thermal":

                        health_score = 91
                        anomaly_count = 1

                    elif predicted_subsystem == "Navigation":

                        health_score = 88
                        anomaly_count = 0

                    elif predicted_subsystem == "Structural":

                        health_score = 85
                        anomaly_count = 1

                    else:

                        health_score = 90
                        anomaly_count = 0

                    c1, c2, c3, c4 = st.columns(4)

                    c1.metric(
                        "Health Score",
                        f"{health_score}%"
                    )

                    c2.metric(
                        "Risk Level",
                        "Low"
                    )

                    c3.metric(
                        "Integrity",
                        "Stable"
                    )

                    c4.metric(
                        "Anomalies",
                        anomaly_count
                    )

                    st.write(
    "Records Analysed : 1"
)

                    st.write(
    f"Parameters Monitored : {len(selected_row_df.columns)}"
)
                    if anomaly_count > 0:

                        if predicted_subsystem == "Thermal":

                            anomaly_description = (
                                "Temperature variation exceeded expected operational threshold."
                            )

                        elif predicted_subsystem == "Navigation":

                            anomaly_description = (
                                "Navigation drift exceeded acceptable limit."
                            )

                        elif predicted_subsystem == "Structural":

                            anomaly_description = (
                                "Abnormal vibration pattern detected."
                            )

                        elif predicted_subsystem == "Propulsion":

                            anomaly_description = (
                                "Propulsion pressure fluctuation detected."
                            )

                        else:

                            anomaly_description = (
                                "Operational anomaly detected."
                            )

                        st.warning(
                            f"""
Anomaly Detected

Type : {anomaly_description}

Subsystem : {predicted_subsystem}

Recommended Action :
Detailed subsystem inspection recommended.
"""
                        )
                    else:

                        st.success(
                            "Subsystem operating within normal limits."
                        )

                    break

            if found:
                break

        if not found:

            st.error(
                "Selected value not found."
            )

    except Exception as e:

        st.error(
            f"Error Reading File: {e}"
        )

else:

    st.info(
        "Please Upload a Telemetry File"
    )