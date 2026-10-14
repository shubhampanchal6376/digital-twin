from pathlib import Path
import pandas as pd

DATA_DIR = Path(
    "data/wearable/HUPA-UCM/"
    "HUPA-UCM Diabetes Dataset/Preprocessed"
)

results = []

for file in sorted(DATA_DIR.glob("*.csv")):
    df = pd.read_csv(file, sep=";")

    timestamps = pd.to_datetime(
        df["time"].astype(str).str.strip(),
        errors="coerce"
    )

    valid = timestamps.dropna()
    intervals = (
        valid.sort_values()
        .diff()
        .dt.total_seconds()
        .div(60)
        .dropna()
    )

    results.append({
        "participant": file.stem,
        "invalid_timestamps": timestamps.isna().sum(),
        "duplicate_timestamps": timestamps.duplicated().sum(),
        "median_interval_min": intervals.median(),
        "intervals_over_15min": (intervals > 15).sum(),
    })

summary = pd.DataFrame(results)

print(summary.to_string(index=False))

print("\nTotal invalid timestamps:",
      summary["invalid_timestamps"].sum())

print("Total duplicate timestamps:",
      summary["duplicate_timestamps"].sum())

print("Total intervals over 15 minutes:",
      summary["intervals_over_15min"].sum())