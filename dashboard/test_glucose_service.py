from glucose_service import (
    load_model,
    load_participant_data,
    build_features,
    predict_latest,
    FEATURES,
)


# --------------------------------------------------
# TEST 1: LOAD MODEL
# --------------------------------------------------

model = load_model()

print("TEST 1 PASSED: Model loaded successfully.")


# --------------------------------------------------
# TEST 2: LOAD PARTICIPANT DATA
# --------------------------------------------------

participant_id = "HUPA0001P"

data = load_participant_data(participant_id)

print("\nTEST 2 PASSED: Participant data loaded.")

print("Participant:", participant_id)
print("Number of readings:", len(data))
print("First timestamp:", data["time"].min())
print("Last timestamp:", data["time"].max())


# --------------------------------------------------
# TEST 3: GENERATE FEATURES
# --------------------------------------------------

featured_data = build_features(data)

latest_features = featured_data.iloc[-1][FEATURES]

print("\nTEST 3 PASSED: Features generated.")

print("Number of features:", len(FEATURES))
print(latest_features)


# --------------------------------------------------
# TEST 4: GENERATE FORECAST
# --------------------------------------------------

result = predict_latest(participant_id)

print("\nTEST 4 PASSED: Forecast generated.")

for key, value in result.items():
    print(f"{key}: {value}")


# --------------------------------------------------
# TEST 5: BASIC OUTPUT VALIDATION
# --------------------------------------------------

assert result["participant_id"] == participant_id

assert result["prediction_horizon_minutes"] == 120

assert isinstance(
    result["predicted_glucose_2h"],
    float,
)

assert result["model_status"] == "experimental_prototype"

print("\nALL BASIC TESTS PASSED.")