# Happiest Health Digital Twin Challenge 2026

## Project Title
**AI-Based Digital Twin Prototype for Two-Hour Glucose Forecasting**

## 1. Project Overview

This project develops an experimental Digital Twin proof of concept (PoC) for exploring glucose forecasting using historical wearable glucose-monitoring data and a separate Electronic Health Record (EHR) data-processing pipeline.

The prototype includes:

- EHR data quality assessment and preprocessing.
- Wearable glucose data inspection and preprocessing.
- Time-series feature engineering.
- Machine learning-based glucose forecasting.
- A Flask API for serving predictions.
- A dashboard for visualizing historical glucose readings and forecast results.

**Important limitation:** The EHR and wearable datasets are processed through separate pipelines. Individual-level mapping between the two datasets has not been established. Therefore, this prototype does not claim patient-level integration of EHR and wearable data.

The project is experimental and has not been clinically validated. Its predictions must not be used for medical diagnosis, treatment, or other clinical decisions.

## 2. Problem Statement

Electronic Health Records and wearable devices contain different types of health information. EHR data provides historical healthcare information, while wearable devices can provide time-series measurements such as glucose readings.

The objective of this project is to develop a proof of concept that explores:

1. How healthcare datasets can be inspected and cleaned.
2. How wearable glucose readings can be transformed into time-series features.
3. How machine learning can forecast glucose levels approximately two hours ahead.
4. How prediction results can be presented through an interactive dashboard.

## 3. Healthcare Use Case

The prototype demonstrates a research workflow for examining historical glucose measurements and generating an experimental two-hour glucose forecast.

The dashboard allows users to select a wearable participant, inspect historical glucose readings, and view the forecast returned by the prediction service.

This is a technical demonstration, not a clinically validated healthcare decision-support system.

## 4. Team Details

- **Team Name:** Transcendental-Coders
- **College/Institution:** Kamla Nehru Institute of Technology
- **Team Leader:** Madhav Kumar
- **Team Members:** Madhav Kumar, Sunny Kumar, Shubham Panchal
- **Incubator:** N/A

## 5. Dataset and Preprocessing

### Electronic Health Record (EHR) Data

The EHR preprocessing workflow includes:

- Dataset inspection and missing-value analysis.
- Duplicate record identification and removal.
- Column-level data quality assessment.
- Generation of preprocessing and quality reports.
- Preservation of raw source data.

The preprocessing script processed 18 EHR CSV files, with zero processing failures in the recorded run.

Recorded duplicate removals include:
- Observations: 18 rows.
- Supplies: 11 rows.

Detailed reports are available in the `reports/` directory.

### Wearable Glucose Data

The wearable workflow uses time-series glucose readings and related features.

The feature preparation pipeline includes:

- Glucose history and lag features.
- Rolling glucose statistics.
- Recent glucose changes.
- Available activity-related features, including steps and calories.
- A future glucose target approximately two hours ahead.

The forecasting target is created using a 24-step shift, corresponding to 120 minutes for five-minute sampling intervals.

The preprocessing reports contain different dataset counts from different processing and audit stages. These counts have not been fully reconciled; refer to the reports for their respective contexts.

**Dataset limitation:** The EHR and wearable records do not currently have an established individual-level mapping.

## 6. Technology Stack

- **Language:** Python
- **Data Processing:** Pandas, NumPy
- **Machine Learning:** Scikit-learn
- **Model Persistence:** Joblib
- **Backend API:** Flask
- **Visualization:** Matplotlib, Seaborn
- **Testing:** Pytest
- **Development and Analysis:** Jupyter Notebook
- **Frontend:** HTML, CSS, JavaScript

## 7. Machine Learning Methodology

The wearable forecasting pipeline uses a `HistGradientBoostingRegressor` to predict glucose levels approximately two hours into the future.

### Feature Engineering

The engineered features include:

- Current glucose measurement.
- Historical glucose lag values.
- Rolling glucose mean and standard deviation.
- Recent glucose changes.
- Available steps and calorie measurements.

The future glucose target is excluded from the model input features.

### Baseline Comparison

The model is evaluated against a persistence baseline, which uses the current glucose measurement as the forecast.

### Recorded Overall Evaluation Results

| Metric | Persistence Baseline | HistGradientBoostingRegressor |
|---|---:|---:|
| MAE | 33.474 | 30.234 |
| RMSE | 46.229 | 39.879 |
| RÂ² | 0.1376 | 0.3583 |

In the recorded evaluation, the machine learning model achieved approximately 9.7% lower MAE than the persistence baseline.

These results are experimental and should be interpreted with the evaluation methodology and dataset limitations in mind. They do not establish clinical effectiveness or generalization to new populations.

## 8. System Architecture

The prototype contains the following major components:

1. **EHR Data Pipeline:** Inspects, cleans, and summarizes EHR datasets.
2. **Wearable Data Pipeline:** Prepares glucose time-series data and engineered forecasting features.
3. **Forecasting Model:** Generates an experimental two-hour glucose prediction.
4. **Flask API:** Exposes the prediction service.
5. **Dashboard:** Displays historical glucose readings and forecast results.

The EHR and wearable pipelines are separate. The current architecture does not establish individual-level data integration between them.

See the architecture diagram included with the project submission.

## 9. Project Structure

```text
digital-twin/
â”œâ”€â”€ app.py
â”œâ”€â”€ dashboard/
â”‚   â”œâ”€â”€ glucose_service.py
â”‚   â””â”€â”€ test_glucose_service.py
â”œâ”€â”€ data/
â”œâ”€â”€ docs/
â”œâ”€â”€ models/
â”‚   â”œâ”€â”€ glucose_forecaster.joblib
â”‚   â””â”€â”€ glucose_forecaster_config.json
â”œâ”€â”€ notebooks/
â”‚   â””â”€â”€ 01_data_inspection.ipynb
â”œâ”€â”€ reports/
â”œâ”€â”€ scripts/
â”‚   â”œâ”€â”€ ehr_preprocessing.py
â”‚   â”œâ”€â”€ inspect_missing_values.py
â”‚   â”œâ”€â”€ inspect_wearable_data.py
â”‚   â””â”€â”€ prepare_glucose_features.py
â”œâ”€â”€ requirements.txt
â””â”€â”€ requirements-lock.txt

## Prototype Demonstration Video

Duration: 29 minutes

[Watch the Happiest Health Digital Twin prototype](https://youtu.be/hDqdTFLCu8c)
