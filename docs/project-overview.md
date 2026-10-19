# Project Overview

## 1. Objective

Happiest Health Digital Twin is an experimental healthcare analytics project
that explores glucose forecasting using Electronic Health Record (EHR) data
and wearable glucose-monitoring data.

The current prototype predicts glucose approximately 120 minutes into the
future using historical glucose readings and selected wearable features.

The prototype is intended for technical evaluation and research, not clinical
diagnosis, treatment, or medical decision-making.

## 2. Main Components

- EHR inspection and preprocessing.
- Wearable time-series preprocessing.
- Historical feature engineering and future-target generation.
- A HistGradientBoostingRegressor forecasting model.
- Model evaluation against a persistence baseline.
- A Flask application and glucose prediction service.

## 3. Technology Stack

The project README identifies the following technologies:

- Python, Pandas and NumPy
- Scikit-learn and Joblib
- Flask
- Matplotlib and Seaborn
- Pytest and Jupyter Notebook

## 4. Workflow

1. Inspect source EHR and wearable data.
2. Generate processed copies and data-quality reports.
3. Construct historical glucose features and a two-hour future target.
4. Evaluate the forecasting model against a persistence baseline.
5. Load the saved model through the prediction service.
6. Expose predictions through the Flask API.

EHR preprocessing and wearable glucose forecasting are separate pipelines.
The documented forecasting features come from the wearable dataset.

## 5. Main Implementation Files

- `app.py` — Flask application.
- `dashboard/glucose_service.py` — prediction service.
- `dashboard/test_glucose_service.py` — service tests.
- `scripts/ehr_preprocessing.py` — EHR inspection and cleaning.
- `scripts/prepare_glucose_features.py` — wearable preprocessing and features.
- `scripts/inspect_missing_values.py` — missing-value inspection.
- `scripts/inspect_wearable_data.py` — wearable-data inspection.
- `notebooks/01_data_inspection.ipynb` — data inspection notebook.

## 6. Model Artifacts

- `models/glucose_forecaster.joblib`
- `models/glucose_forecaster_config.json`

## 7. Reports

The `reports/` directory contains EHR quality summaries, cleaning logs,
wearable quality and preprocessing summaries, and ML evaluation reports.

See [ML Methodology and Evaluation](ml-methodology-and-evaluation.md)
for the model configuration and reported metrics.
