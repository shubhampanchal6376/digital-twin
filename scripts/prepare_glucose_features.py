from pathlib import Path

import pandas as pd


# --------------------------------------------------
# 1. PROJECT CONFIGURATION
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent

WEARABLE_DIR = (
    PROJECT_DIR
    / "data"
    / "wearable"
    / "HUPA-UCM"
    / "HUPA-UCM Diabetes Dataset"
    / "Preprocessed"
)

OUTPUT_DIR = PROJECT_DIR / "data" / "processed" / "wearable"
REPORT_DIR = PROJECT_DIR / "reports"

REQUIRED_COLUMNS = [
    "time",
    "glucose",
    "calories",
    "heart_rate",
    "steps",
    "basal_rate",
    "bolus_volume_delivered",
    "carb_input",
]


# --------------------------------------------------
# 2. PREPARE ONE PARTICIPANT
# --------------------------------------------------

def prepare_participant(file_path: Path) -> tuple[pd.DataFrame, int]:
    """Validate and prepare one participant's wearable data."""

    data = pd.read_csv(file_path, sep=";")

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"{file_path.name}: missing columns {missing_columns}"
        )

    data = data[REQUIRED_COLUMNS].copy()

    data["time"] = pd.to_datetime(
        data["time"],
        errors="coerce",
    )

    numeric_columns = [
        column for column in REQUIRED_COLUMNS
        if column != "time"
    ]

    for column in numeric_columns:
        data[column] = pd.to_numeric(
            data[column],
            errors="coerce",
        )

    data = data.dropna(subset=["time", "glucose"])

    data = data.sort_values("time").reset_index(drop=True)

    duplicate_timestamps_removed = int(
        data["time"].duplicated().sum()
    )

    data = (
        data.drop_duplicates(subset=["time"], keep="first")
        .reset_index(drop=True)
    )
    # Check whether readings are consistently spaced at five-minute intervals.
    intervals = data["time"].diff().dropna()

    if not intervals.eq(pd.Timedelta(minutes=5)).all():
        raise ValueError(
            f"{file_path.name}: readings are not consistently "
            "five minutes apart."
        )
    # Generate historical features independently per participant.
    glucose = data["glucose"]

    data["glucose_lag_1"] = glucose.shift(1)
    data["glucose_lag_3"] = glucose.shift(3)
    data["glucose_lag_6"] = glucose.shift(6)
    data["glucose_lag_12"] = glucose.shift(12)

    data["glucose_mean_3"] = (
        glucose.shift(1).rolling(3).mean()
    )

    data["glucose_mean_6"] = (
        glucose.shift(1).rolling(6).mean()
    )

    data["glucose_std_6"] = (
        glucose.shift(1).rolling(6).std()
    )

    data["glucose_change_15m"] = (
        glucose - data["glucose_lag_3"]
    )

    data["glucose_change_30m"] = (
        glucose - data["glucose_lag_6"]
    )

    # Forecast target: glucose approximately 2 hours later.
    data["glucose_future_2h"] = glucose.shift(-24)

    return data, duplicate_timestamps_removed


# --------------------------------------------------
# 3. PROCESS ALL PARTICIPANTS
# --------------------------------------------------

def main():
    if not WEARABLE_DIR.exists():
        raise FileNotFoundError(
            f"Wearable data directory not found: {WEARABLE_DIR}"
        )

    files = sorted(WEARABLE_DIR.glob("*.csv"))

    if not files:
        raise FileNotFoundError(
            f"No participant CSV files found in {WEARABLE_DIR}"
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    quality_results = []
    processed_count = 0

    for file_path in files:
        try:
            data, duplicate_timestamps_removed = prepare_participant(file_path)
            output_path = OUTPUT_DIR / file_path.name
            data.to_csv(output_path, index=False)

            quality_results.append({
                "participant": file_path.stem,
                "input_rows": len(pd.read_csv(file_path, sep=";")),
                "processed_rows": len(data),
                "missing_glucose": int(data["glucose"].isna().sum()),
                "missing_future_target": int(
                    data["glucose_future_2h"].isna().sum()
                ),
                "duplicate_timestamps_removed": duplicate_timestamps_removed,
                "status": "success",
            })
            processed_count += 1
            print(
                f"Processed {file_path.name}: "
                f"{len(data)} rows"
            )

        except Exception as exc:
            quality_results.append({
                "participant": file_path.stem,
                "input_rows": None,
                "processed_rows": None,
                "missing_glucose": None,
                "missing_future_target": None,
                "duplicate_timestamps_removed": None,
                "status": f"failed: {exc}",
            })

    report_path = REPORT_DIR / "wearable_preprocessing_summary.csv"

    pd.DataFrame(quality_results).to_csv(
        report_path,
        index=False,
    )

    print(f"\nParticipants processed successfully: {processed_count}")
    print(f"Participants found: {len(files)}")
    print(f"Summary report: {report_path}")


if __name__ == "__main__":
    main()