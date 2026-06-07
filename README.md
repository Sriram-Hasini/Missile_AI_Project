# AI-Based Telemetry Monitoring and Anomaly Detection System

## Overview

This project is an AI-powered Telemetry Monitoring and Anomaly Detection System developed for educational and research purposes. The system analyzes synthetically generated telemetry data and identifies abnormal operational patterns using machine learning techniques.

> **Note:** All telemetry data used in this project is synthetic and generated for demonstration purposes only.

---

## Features

- Synthetic telemetry data generation
- Data preprocessing and cleaning
- Machine learning-based anomaly detection
- Telemetry behavior analysis
- Interactive Streamlit dashboard
- Data visualization and monitoring

---

## Project Structure

```text
MISSILE_AI_PROJECT/
│
├── analysis/
│   └── behavior_analysis.py
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── generator.py
│   └── generate_sample_telemetry.py
│
├── models/
│   └── hybrid_model.py
│
├── preprocessing/
│   └── preprocessing.py
│
├── training/
│   └── train.py
│
├── utils/
│   ├── anomaly.py
│   ├── converter.py
│   ├── helpers.py
│   └── type_detector.py
│
├── sample_telemetry.csv
├── telemetry_metadata.json
├── requirements.txt
└── README.md
```

---

## Technologies Used

- Python
- Pandas
- NumPy
- Scikit-Learn
- TensorFlow / Keras
- Streamlit
- Plotly

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd MISSILE_AI_PROJECT
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Dashboard

```bash
streamlit run dashboard/app.py
```

---

## Workflow

1. Generate synthetic telemetry data
2. Preprocess and clean data
3. Train machine learning model
4. Detect anomalies
5. Visualize results using Streamlit dashboard

---

## Applications

- Telemetry Monitoring
- AI-Based Analytics
- Anomaly Detection
- Research Simulations
- Educational Machine Learning Projects

---

## Disclaimer

This project is intended solely for academic and educational purposes. No real-world defense, aerospace, or classified data is used.

---

## Author

**Hasini Sriram**

AI-Based Telemetry Monitoring and Anomaly Detection System