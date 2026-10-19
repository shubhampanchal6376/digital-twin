# ML Methodology and Evaluation

## 1. Forecasting Objective

The model estimates glucose approximately two hours into the future.

The configured target is:

`glucose_future_2h = glucose.shift(-24)`

With five-minute sampling, 24 readings correspond to 120 minutes.

## 2. Input Features

The saved model configuration identifies 12 input features.

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

The future target is not part of the configured input feature list.

## 3. Estimator Configuration

The selected estimator is `HistGradientBoostingRegressor`.

Reported configuration:

- `max_iter = 150`
- `max_leaf_nodes = 31`
- `learning_rate = 0.1`
- `l2_regularization = 1.0`
- `random_state = 42`

Model artifact: `models/glucose_forecaster.joblib`

Configuration: `models/glucose_forecaster_config.json`

## 4. Evaluation Design

The notebook uses `GroupShuffleSplit` with a test size of 20% and
`random_state=42` for participant-level separation.

An independent reconstruction of the intended split reported:

- 25 participants total.
- 20 training participants and five testing participants.
- No participant overlap.
- 129,640 training rows and 178,852 testing rows.

The reconstructed split does not prove that the saved estimator was trained
using exactly that split. This remains to be verified.

## 5. Baseline and Metrics

The persistence baseline predicts that future glucose equals current glucose.

- MAE: mean absolute error; lower is better.
- RMSE: root mean squared error; lower is better.
- R²: coefficient of determination; higher is generally better, subject to
  the evaluation data and target distribution.

### Reported results

| Model | MAE (mg/dL) | RMSE (mg/dL) | R² |
|---|---:|---:|---:|
| Persistence Baseline | 33.474 | 46.229 | 0.1376 |
| HistGradientBoosting | 30.234 | 39.879 | 0.3583 |

The evaluation report states that the model improves on the persistence
baseline across all three metrics. Its MAE is approximately 9.7% lower.

The reported R² of 0.3583 corresponds to approximately 35.83% of variance
explained on the evaluated data.

## 6. Participant-Level Caveat

The evaluation report states that HUPA0027P contributes approximately 92.4%
of all test rows. The aggregate metrics are therefore heavily influenced by
this participant.

The report also states that the model achieved lower MAE than the persistence
baseline for all five held-out participants. Participant-level metrics should
be considered alongside aggregate results.

## 7. Prediction Service

- Flask application: `app.py`
- Service: `dashboard/glucose_service.py`
- Endpoint: `/api/predict/<participant_id>`
- Tests: `dashboard/test_glucose_service.py`

The documented service loads participant data, constructs historical
features and uses the saved model to generate a forecast. Its response
includes prediction information such as participant, timestamp, current
glucose, forecast, horizon and an experimental-use disclaimer.

The methodology reports that service feature names and ordering match the
saved model configuration. A previous test run reportedly passed eight tests.

## 8. Leakage and Reproducibility Checks

Reported checks include:

- Comparing engineered features with independently recomputed values.
- Excluding the future target from configured model inputs.
- Reconstructing a participant split with no overlap.
- Comparing feature names and ordering in the model configuration and service.

Still to verify: whether the saved estimator was fitted using the exact
intended participant-level split. Feature consistency checks alone do not
rule out all possible leakage.

## 9. Source Reports

- `reports/ml_methodology.md`
- `reports/ml_evaluation_summary.md`
- `reports/overall_model_evaluation.csv`
- `reports/participant_model_evaluation.csv`
