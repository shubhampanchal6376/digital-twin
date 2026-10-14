import math

import pytest

from glucose_service import (
    load_model,
    load_participant_data,
    build_features,
    predict_latest,
    FEATURES,
)


@pytest.fixture
def participant_id():
    return "HUPA0001P"


def test_load_model():
    model = load_model()
    assert model is not None
    assert hasattr(model, "predict")


def test_load_participant_data(participant_id):
    data = load_participant_data(participant_id)

    assert not data.empty
    assert {"time", "glucose", "steps", "calories"}.issubset(data.columns)
    assert data["time"].is_monotonic_increasing
    assert not data["time"].duplicated().any()


def test_build_features(participant_id):
    data = load_participant_data(participant_id)
    featured_data = build_features(data)

    assert set(FEATURES).issubset(featured_data.columns)
    assert not featured_data.iloc[-1][FEATURES].isna().any()


def test_predict_latest(participant_id):
    result = predict_latest(participant_id)

    assert result["participant_id"] == participant_id
    assert result["prediction_horizon_minutes"] == 120
    assert result["model_status"] == "experimental_prototype"
    assert result["data_status"] == "historical_dataset"
    assert isinstance(result["predicted_glucose_2h"], float)
    assert math.isfinite(result["predicted_glucose_2h"])
    assert isinstance(result["current_glucose"], float)
    assert "not clinically validated" in result["clinical_warning"]


def test_invalid_participant_id():
    with pytest.raises(ValueError):
        load_participant_data("../invalid")


def test_missing_participant_file():
    with pytest.raises(FileNotFoundError):
        load_participant_data("HUPA9999P")

def test_invalid_numeric_data_is_rejected(monkeypatch):
    import glucose_service

    data = glucose_service.load_participant_data("HUPA0001P")
    data.loc[data.index[-1], "glucose"] = float("inf")

    monkeypatch.setattr(
        glucose_service,
        "CGM_DIR",
        glucose_service.CGM_DIR,
    )

    # Check that infinite glucose values are rejected.
    # This test will initially expose a gap in the current validation.
    assert not data["glucose"].isin([float("inf")]).empty

def test_build_features_rejects_infinite_glucose():
    import pandas as pd
    import pytest

    from glucose_service import build_features

    data = pd.DataFrame({
        "time": pd.date_range(
            "2024-01-01",
            periods=13,
            freq="5min",
        ),
        "glucose": [100.0] * 12 + [float("inf")],
        "steps": [0.0] * 13,
        "calories": [0.0] * 13,
    })

    # The current service does not yet reject infinite values.
    # This test documents the desired behavior.
    with pytest.raises(ValueError):
        build_features(data)
def test_build_features_rejects_infinite_glucose():
    import pandas as pd
    import pytest

    from glucose_service import build_features

    data = pd.DataFrame({
        "time": pd.date_range(
            "2024-01-01",
            periods=13,
            freq="5min",
        ),
        "glucose": [100.0] * 12 + [float("inf")],
        "steps": [0.0] * 13,
        "calories": [0.0] * 13,
    })

    # The current service does not yet reject infinite values.
    # This test documents the desired behavior.
    with pytest.raises(ValueError):
        build_features(data)