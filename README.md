# Happiest Health Digital Twin

## Project Overview

Happiest Health Digital Twin is an experimental healthcare analytics project that combines Electronic Health Record (EHR) data and wearable glucose-monitoring data to explore personalized glucose forecasting.

The current prototype uses historical glucose readings and related wearable features to predict glucose levels approximately two hours into the future.

**Important:** This project is an experimental prototype. Its predictions have not been clinically validated and must not be used for medical diagnosis or treatment decisions.

## Problem Statement

Healthcare records and wearable devices provide different types of information about an individual's health. Analyzing these sources together can help explore patterns in glucose levels and support research into personalized health monitoring.

This project develops a prototype workflow for:

- Inspecting and preprocessing EHR datasets.
- Cleaning and validating wearable glucose data.
- Engineering time-series features.
- Training and evaluating a glucose forecasting model.
- Serving predictions through a Flask API.

## Technology Stack

- Python
- Pandas and NumPy
- Scikit-learn
- Joblib
- Flask
- Matplotlib and Seaborn
- Pytest
- Jupyter Notebook

## Project Structure

```text
digital-twin/
├── app.py
├── dashboard/
│   ├── glucose_service.py
│   └── test_glucose_service.py
├── data/
│   └── .gitkeep
├── models/
│   ├── glucose_forecaster.joblib
│   └── glucose_forecaster_config.json
├── notebooks/
│   └── 01_data_inspection.ipynb
├── reports/
│   ├── ehr_cleaning_log.csv
│   ├── ehr_column_quality_summary.csv
│   ├── ehr_data_quality_summary.csv
│   ├── ml_evaluation_summary.md
│   ├── ml_methodology.md
│   ├── wearable_glucose_episode_summary.csv
│   ├── wearable_glucose_quality_summary.csv
│   └── wearable_preprocessing_summary.csv
├── scripts/
│   ├── ehr_preprocessing.py
│   ├── inspect_missing_values.py
│   ├── inspect_wearable_data.py
│   └── prepare_glucose_features.py
├── requirements.txt
└── requirements-lock.txt