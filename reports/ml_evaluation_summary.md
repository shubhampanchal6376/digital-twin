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

The participant-level report indicates lower MAE than the persistence baseline for all five evaluated participants.

However, HUPA0027P contributes approximately 92.4% of the test rows. Consequently, the overall evaluation is heavily influenced by this participant.

Participant-level results should therefore be considered alongside overall metrics.

## 6. Limitations

- The model is an experimental prototype.
- The dataset contains historical glucose measurements from a limited set of participants.
- Performance may vary across participants.
- The evaluation does not establish clinical validity or safety.
- The model is not intended for diagnosis or treatment decisions.

## 7. Existing Reports

- `overall_model_evaluation.csv`
- `participant_model_evaluation.csv`

## 8. Conclusion

HistGradientBoosting outperforms the persistence baseline on the reported evaluation metrics.

Further validation on additional participants and more representative evaluation data is needed before making claims about generalization or clinical usefulness.