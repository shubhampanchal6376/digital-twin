# Glucose Forecasting — ML Methodology

## 1. Project Objective

The objective is to develop an experimental machine-learning prototype that
forecasts glucose approximately two hours into the future using historical
glucose readings and selected wearable signals.

The prototype is intended for technical evaluation and research, not clinical
diagnosis or treatment decisions.

## 2. EHR Data Preprocessing

### Input data
The project contains EHR CSV files under `data/ehr/`.

### Processing
- Raw EHR files are preserved.
- Processed copies are stored under `data/processed/ehr/`.
- Data-quality summaries and cleaning logs are generated.
- Exact duplicate rows are removed from processed copies where applicable.
- Placeholder dates are handled in processed data where identified.
- Missing values and column-level quality are documented in reports.

### Reports
- `reports/ehr_data_quality_summary.csv`
- `reports/ehr_column_quality_summary.csv`
- `reports/ehr_cleaning_log.csv`

EHR preprocessing is documented separately from the wearable glucose model.
The current glucose forecasting model uses the selected wearable features
described below.

## 3. Wearable Data

### Source
The wearable dataset is located under:

`data/wearable/HUPA-UCM/HUPA-UCM Diabetes Dataset/Preprocessed/`

The source files are semicolon-delimited CSV files containing time, glucose,
and wearable or treatment-related measurements.

### Processing
The preprocessing pipeline is implemented in:

`scripts/prepare_glucose_features.py`

Processed participant files are written to:

`data/processed/wearable/`

The pipeline:
- Parses timestamps and numeric columns.
- Removes rows with invalid timestamps or missing glucose values.
- Sorts observations by time.
- Removes duplicate timestamps when encountered.
- Checks the expected five-minute sampling interval.
- Generates historical glucose features and a future prediction target.
- Writes a participant-level preprocessing summary.

Raw source files are preserved.

### Initial quality findings
The completed quality audit covered 25 participant files and 309,392
observations.

The audit found:
- No missing glucose values in the initial dataset audit.
- No invalid timestamps.
- No duplicate timestamps.
- A median sampling interval of five minutes.
- No observed intervals greater than 15 minutes in the initial audit.

Subsequent validation of the processed files also found no invalid numeric
values in the audited numeric columns, no infinite values, and no intervals
that differed from the expected five-minute spacing.

### Quality reports
- `reports/wearable_glucose_quality_summary.csv`
- `reports/wearable_glucose_episode_summary.csv`
- `reports/wearable_preprocessing_summary.csv`

## 4. Feature Engineering

The model uses 12 input features.

| Feature | Description |
|---|---|
| `glucose` | Current glucose reading |
| `glucose_lag_1` | Glucose one reading earlier |
| `glucose_lag_3` | Glucose three readings earlier |
| `glucose_lag_6` | Glucose six readings earlier |
| `glucose_lag_12` | Glucose twelve readings earlier |
| `glucose_mean_3` | Mean of the previous three readings |
| `glucose_mean_6` | Mean of the previous six readings |
| `glucose_std_6` | Standard deviation of the previous six readings |
| `glucose_change_15m` | Current glucose minus glucose three readings earlier |
| `glucose_change_30m` | Current glucose minus glucose six readings earlier |
| `steps` | Step-count signal |
| `calories` | Calorie signal |

Rolling statistics use historical readings rather than future readings.

The target is:

`glucose_future_2h = glucose.shift(-24)`

At five-minute sampling intervals, 24 readings correspond to 120 minutes.

Rows without sufficient historical readings or a valid future target cannot
supply all required model inputs and are excluded from model-ready evaluation
data where appropriate.

### Feature validation
All 10 engineered feature columns were checked against independently
recomputed expected values across 25 processed participant files.

Results:
- Participant files checked: 25
- Feature comparisons: 250
- Failed comparisons: 0

A numerical tolerance was used to account for small floating-point
differences in stored values.

## 5. Model Training

The selected estimator is:

`HistGradientBoostingRegressor`

The recorded configuration uses:
- `max_iter = 150`
- `max_leaf_nodes = 31`
- `learning_rate = 0.1`
- `l2_regularization = 1.0`
- `random_state = 42`

The model is stored at:

`models/glucose_forecaster.joblib`

Its configuration is stored at:

`models/glucose_forecaster_config.json`

The saved configuration identifies the target as `glucose_future_2h`,
records a 120-minute horizon, and lists the 12 input features.

The target is not included in the configured feature list.

## 6. Evaluation Methodology

The model is evaluated against a persistence baseline.

The baseline predicts that future glucose will equal the current glucose
reading.

The reported metrics are:

- **MAE:** Mean Absolute Error; lower is better.
- **RMSE:** Root Mean Squared Error; lower is better.
- **R²:** Coefficient of determination; interpretation depends on the
  evaluation data and target distribution.

The notebook uses `GroupShuffleSplit` with a test size of 20% and
`random_state=42` for participant-level separation.

An independent reconstruction of the intended split produced:
- 25 participants in total.
- 20 training participants.
- 5 testing participants.
- No participant overlap.
- 129,640 training rows.
- 178,852 testing rows.

This independently reconstructed split does not, by itself, prove that the
saved model was fitted using precisely the same split. That connection
remains to be verified.

### Reported evaluation results

| Model | MAE (mg/dL) | RMSE (mg/dL) | R² |
|---|---:|---:|---:|
| Persistence Baseline | 33.474 | 46.229 | 0.1376 |
| HistGradientBoosting | 30.234 | 39.879 | 0.3583 |

The reported model improves on the persistence baseline across all three
metrics.

The model's MAE is approximately 9.7% lower than the baseline MAE.

### Evaluation limitation
One held-out participant, HUPA0027P, contributes approximately 92.4% of
the reported test rows. Consequently, aggregate metrics are strongly
influenced by this participant. Participant-level results should also be
considered when interpreting model performance.

## 7. Prediction Service

The prediction service is implemented in:

`dashboard/glucose_service.py`

The Flask application is implemented in:

`app.py`

The prediction endpoint is:

`/api/predict/<participant_id>`

The service loads participant data, constructs the required historical
features, and uses the saved model to generate a forecast.

The service's configured feature names and order were checked against the
saved model configuration. Both contain the same 12 features in the same
order.

The endpoint returns prediction information, including the participant,
timestamp, current glucose, forecast, prediction horizon, and an
experimental-use disclaimer.

The service has an existing automated test suite. A previous test run
completed with eight tests passing.

## 8. Leakage Review and Validation Status

Completed checks:
- Historical lag and rolling features were compared against independently
  recomputed values.
- The future target was excluded from the configured input features.
- The intended participant split was independently reconstructed without
  participant overlap.
- The saved model reports 12 input features.
- The saved model configuration and prediction service use matching feature
  names and order.

Remaining verification:
- Confirm that the saved model was fitted using the exact intended
  participant-level split.
- Review the complete training workflow and its relationship to the saved
  estimator before making stronger claims about the evaluation.

The completed checks support feature consistency but do not rule out every
possible source of data leakage.

## 9. Limitations

- The model is an experimental prototype.
- Evaluation uses a limited set of participants.
- Test-row counts are highly imbalanced across participants.
- Performance may vary between participants and datasets.
- The reported evaluation does not establish clinical validity or safety.
- The model is not intended for diagnosis, treatment, or medical decision-making.
- Additional independent validation is required before making claims about
  generalization or clinical usefulness.

## 10. Reproducibility and Related Files

Key implementation files:
- `scripts/prepare_glucose_features.py`
- `dashboard/glucose_service.py`
- `dashboard/test_glucose_service.py`
- `app.py`

Key model files:
- `models/glucose_forecaster.joblib`
- `models/glucose_forecaster_config.json`

Key reports:
- `reports/ml_evaluation_summary.md`
- `reports/overall_model_evaluation.csv`
- `reports/participant_model_evaluation.csv`
- `reports/wearable_preprocessing_summary.csv`
- `reports/wearable_glucose_quality_summary.csv`
- `reports/wearable_glucose_episode_summary.csv`
- `reports/ehr_data_quality_summary.csv`
- `reports/ehr_column_quality_summary.csv`
- `reports/ehr_cleaning_log.csv`

## 11. Conclusion

The project has a working experimental glucose forecasting pipeline, wearable
preprocessing, feature engineering, evaluation reports, and a Flask prediction
API.

Feature consistency checks passed across all 25 processed participant files.
The model outperformed the persistence baseline on the reported evaluation.

The exact training split used for the saved estimator still requires
confirmation. Further validation and frontend integration remain part of the
project's outstanding work.
