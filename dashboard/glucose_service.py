from pathlib import Path

import joblib
import pandas as pd


# --------------------------------------------------
# 1. PROJECT CONFIGURATION
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent

CGM_DIR = (
    PROJECT_DIR
    / "data"
    / "wearable"
    / "HUPA-UCM"
    / "HUPA-UCM Diabetes Dataset"
    / "Preprocessed"
)

MODEL_PATH = PROJECT_DIR / "models" / "glucose_forecaster.joblib"

FEATURES = [
    "glucose",
    "glucose_lag_1",
    "glucose_lag_3",
    "glucose_lag_6",
    "glucose_lag_12",
    "glucose_mean_3",
    "glucose_mean_6",
    "glucose_std_6",
    "glucose_change_15m",
    "glucose_change_30m",
    "steps",
    "calories",
]


# --------------------------------------------------
# 2. LOAD TRAINED MODEL
# --------------------------------------------------

def load_model():
    """Load the saved glucose forecasting model."""

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found: {MODEL_PATH}"
        )

    return joblib.load(MODEL_PATH)


# --------------------------------------------------
# 3. LOAD PARTICIPANT DATA
# --------------------------------------------------

def load_participant_data(participant_id: str) -> pd.DataFrame:
    """Load and validate one participant's CGM data."""

    if not participant_id.isalnum():
        raise ValueError("Invalid participant ID.")

    file_path = CGM_DIR / f"{participant_id}.csv"

    if not file_path.exists():
        raise FileNotFoundError(
            f"Participant file not found: {file_path}"
        )

    data = pd.read_csv(file_path, sep=";")

    required_columns = [
        "time",
        "glucose",
        "steps",
        "calories",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    data["time"] = pd.to_datetime(
        data["time"],
        errors="coerce",
    )

    if data["time"].isna().any():
        raise ValueError("Invalid timestamps found.")

    data = data.sort_values("time").reset_index(drop=True)

    if data["time"].duplicated().any():
        raise ValueError("Duplicate timestamps found.")

    numeric_columns = [
        "glucose",
        "steps",
        "calories",
    ]

    for column in numeric_columns:
        data[column] = pd.to_numeric(
            data[column],
            errors="coerce",
        )

    if data[required_columns].isna().any().any():
        raise ValueError(
            "Missing or invalid required data found."
        )

    if len(data) < 13:
        raise ValueError(
            "Insufficient readings to calculate historical features."
        )

    return data


# --------------------------------------------------
# 4. FEATURE ENGINEERING
# --------------------------------------------------

def build_features(data: pd.DataFrame) -> pd.DataFrame:
    """Generate the historical features used during training."""

    data = data.copy()

    glucose = data["glucose"]

    data["glucose_lag_1"] = glucose.shift(1)
    data["glucose_lag_3"] = glucose.shift(3)
    data["glucose_lag_6"] = glucose.shift(6)
    data["glucose_lag_12"] = glucose.shift(12)

    data["glucose_mean_3"] = (
        glucose.shift(1)
        .rolling(3)
        .mean()
    )

    data["glucose_mean_6"] = (
        glucose.shift(1)
        .rolling(6)
        .mean()
    )

    data["glucose_std_6"] = (
        glucose.shift(1)
        .rolling(6)
        .std()
    )

    data["glucose_change_15m"] = (
        glucose - data["glucose_lag_3"]
    )

    data["glucose_change_30m"] = (
        glucose - data["glucose_lag_6"]
    )

    return data


# --------------------------------------------------
# 5. GENERATE TWO-HOUR FORECAST
# --------------------------------------------------

def predict_latest(participant_id: str) -> dict:
    """Predict glucose approximately two hours ahead."""

    data = load_participant_data(participant_id)

    featured_data = build_features(data)

    latest = featured_data.iloc[-1]

    X = featured_data.iloc[[-1]][FEATURES]

    if X.isna().any().any():
        raise ValueError(
            "Required historical features contain missing values."
        )

    model = load_model()

    prediction = float(model.predict(X)[0])

    return {
        "participant_id": participant_id,
        "latest_timestamp": latest["time"].isoformat(),
        "current_glucose": float(latest["glucose"]),
        "predicted_glucose_2h": prediction,
        "prediction_horizon_minutes": 120,
        "model_status": "experimental_prototype",
        "data_status": "historical_dataset",
        "clinical_warning": (
            "Experimental forecast; not clinically validated "
            "and not medical advice."
        ),
    }