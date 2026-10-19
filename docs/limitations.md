# Limitations and Validation Status

## 1. Experimental Status

This project is an experimental glucose forecasting prototype. Its predictions
have not been clinically validated and must not be used for diagnosis,
treatment decisions or as a substitute for professional medical advice.

## 2. Dataset Limitations

The reported audit covers 25 participants. The limited participant count does
not establish that the model will generalize to other populations or datasets.

The reported test rows are imbalanced: HUPA0027P contributes approximately
92.4% of the test set. Aggregate metrics may therefore be strongly influenced
by that participant.

## 3. Evaluation Limitations

The evaluation report compares HistGradientBoostingRegressor with a
persistence baseline and reports improved MAE, RMSE and R².

However, the exact participant-level split used to fit the saved estimator
has not been independently verified. The intended split was reconstructed,
but that alone does not establish the saved model's training history.

## 4. Leakage Checks

Feature values were independently recomputed and compared, the future target
was excluded from the configured input feature list, and participant split
overlap was checked in a reconstructed split.

These checks support feature consistency but do not establish the absence of
every possible source of data leakage.

## 5. Further Work

- Verify the exact training workflow and split associated with the saved model.
- Review participant-level evaluation alongside aggregate metrics.
- Perform additional independent validation before making generalization claims.
- Complete final end-to-end verification of the frontend, Flask API and prediction service.

## 6. Safe Interpretation

Reported performance is evidence from the documented experimental evaluation
only. It does not demonstrate clinical validity, safety or clinical usefulness.
