# Glucose Forecasting — ML Evaluation Summary

## 1. Objective

Evaluate the experimental glucose forecasting model against a persistence baseline for a two-hour prediction horizon.

## 2. Evaluation Metrics

- **MAE:** Mean Absolute Error; lower is better.
- **RMSE:** Root Mean Squared Error; lower is better.
- **R²:** Coefficient of determination; higher is generally better.

## 3. Overall Results

| Model | MAE (mg/dL) | RMSE (mg/dL) | R² |
|---|---:|---:|---:|
| Persistence Baseline | 33.474 | 46.229 | 0.1376 |
| HistGradientBoosting | 30.234 | 39.879 | 0.3583 |

## 4. Interpretation

HistGradientBoosting improves on the persistence baseline across all three reported metrics.

The model's MAE is approximately 9.7% lower than the baseline MAE.

The R² score of 0.3583 indicates that the model explains approximately 35.83% of the variance in the evaluated target.

## 5. Participant-Level Evaluation

The model achieved lower MAE than the persistence baseline for all five held-out participants.

However, HUPA0027P contributes approximately 92.4% of all test rows. Therefore, the overall metrics are heavily influenced by this participant. Participant-level results should also be considered when interpreting performance.

## 6. Limitations

- This is an experimental forecasting prototype, not a clinically validated model.
- The exact training split used for the saved estimator has not been independently verified.
- Results on these participants do not establish generalization to other populations or clinical usefulness.
- Predictions must not be used as a substitute for professional medical advice.
