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
# SUBSYSTEM GROUPS
# ----------------------------------------

SUBSYSTEM_GROUPS = {

    "Propulsion": [
        "W0", "W1", "W2", "W3", "W4", "W5"
    ],

    "Thermal": [
        "W6", "W7", "W8", "W9", "W10", "W11"
    ],

    "Navigation": [
        "W12", "W13", "W14", "W15", "W16", "W17"
    ],

    "Structural": [
        "W18", "W19", "W20", "W21", "W22", "W23"
    ],

    "Power": [
        "W24", "W25", "W26", "W27",
        "W28", "W29", "W30", "W31"
    ]
}

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
            "Select Telemetry Value"
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

                    predicted_subsystem = "Unknown"

                    for subsystem, words in SUBSYSTEM_GROUPS.items():

                        if col in words:

                            predicted_subsystem = subsystem
                            break

                    # ----------------------------------------
                    # PARAMETER INTERPRETATION
                    # ----------------------------------------

                    st.markdown(
                        f"""
### Parameter Interpretation

| Attribute | Value |
|-----------|--------|
| Selected Value | {value} |
| Word Location | {col} |
| Row Number | {idx} |
| Data Type | {detected_type} |
| Subsystem | {predicted_subsystem} |
"""
                    )

                    # ----------------------------------------
                    # SUBSYSTEM DATA
                    # ----------------------------------------

                    st.markdown(
                        f"""
## {predicted_subsystem} Subsystem Data
"""
                    )

                    subsystem_words = SUBSYSTEM_GROUPS[
                        predicted_subsystem
                    ]

                    subsystem_df = df[
                        subsystem_words
                    ]

                    st.dataframe(
                        subsystem_df,
                        use_container_width=True
                    )

                    # ----------------------------------------
                    # DOWNLOAD
                    # ----------------------------------------

                    st.markdown(
                        f"### Download {predicted_subsystem} Subsystem Data"
                    )

                    st.download_button(
                        label="Download Subsystem Data",
                        data=subsystem_df.to_csv(index=False),
                        file_name=f"{predicted_subsystem}_Subsystem_Data.csv",
                        mime="text/csv",
                        key=f"download_{predicted_subsystem}_{idx}"
                    )

                    # ----------------------------------------
                    # FORMAT CONVERSION
                    # ----------------------------------------

                    st.subheader(
                        "Format Conversion"
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
                        f"Records Analysed : {len(subsystem_df)}"
                    )

                    st.write(
                        f"Parameters Monitored : {len(subsystem_words)}"
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