# 🚀 Missile AI Intelligence Dashboard

## Overview

Missile AI Intelligence Dashboard is an AI-powered telemetry analysis framework designed to monitor missile subsystems, detect anomalies, assess subsystem health, and generate behavioral insights through an interactive dashboard.

The project utilizes a Hybrid LSTM-Transformer architecture to analyze telemetry data from multiple subsystems and identify abnormal operational patterns.

---

## Features

* Telemetry Data Simulation
* Data Preprocessing Pipeline
* Hybrid LSTM + Transformer Deep Learning Model
* AI-Based Anomaly Detection
* Behavioral Analysis Engine
* Subsystem Risk Assessment
* Interactive Streamlit Dashboard
* Real-Time Telemetry Visualization
* Operational Phase Monitoring

---

## Project Architecture

Telemetry Data Generation

↓

Data Preprocessing

↓

Hybrid LSTM-Transformer Model

↓

Behavioral Analysis

↓

Anomaly Detection

↓

Risk Assessment

↓

Interactive Dashboard

---

## Subsystems Monitored

### Propulsion System

* Pressure Monitoring
* Thrust Analysis

### Thermal System

* Temperature Monitoring
* Thermal Escalation Detection

### Structural System

* Vibration Analysis
* Structural Health Monitoring

### Navigation System

* Navigation Drift Analysis
* Guidance Monitoring

### Power System

* Voltage Monitoring
* Current Consumption Analysis

---

## Technologies Used

* Python
* TensorFlow
* NumPy
* Pandas
* Scikit-Learn
* Plotly
* Streamlit

---

## Project Structure

Missile_AI_Project/

├── analysis/

├── dashboard/

├── data/

├── models/

├── preprocessing/

├── training/

├── utils/

├── visualization/

├── main.py

├── requirements.txt

└── README.md

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Sriram-Hasini/Missile_AI_Project.git
```

Navigate to project directory:

```bash
cd Missile_AI_Project
```

Create virtual environment:

```bash
python -m venv venv
```

Activate virtual environment:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Project

Generate telemetry data:

```bash
python data/generator.py
```

Train the AI model:

```bash
python training/train.py
```

Run behavioral analysis:

```bash
python analysis/behavior_analysis.py
```

Launch dashboard:

```bash
streamlit run dashboard/app.py
```

---

## Dashboard Capabilities

* System Health Monitoring
* Operational Phase Visualization
* Thermal Analysis
* Propulsion Monitoring
* Structural Vibration Analysis
* Navigation Drift Monitoring
* AI-Based Anomaly Detection
* Correlation Heatmaps
* Behavioral Insights

---

## Future Enhancements

* Real-Time Telemetry Streaming
* Predictive Maintenance
* Failure Forecasting
* Advanced Risk Prediction
* Automated Report Generation
* Cloud Deployment

---

## Disclaimer

This project uses synthetic telemetry data generated for educational and research purposes. No confidential or real-world defense data is included.

---

## Author

Sriram Hasini

AI-Powered Missile Telemetry Intelligence System
