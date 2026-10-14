import pandas as pd
from pathlib import Path

# Processed EHR data folder
data_dir = Path("data/processed/ehr")

csv_files = sorted(data_dir.glob("*.csv"))

print(f"Total EHR tables: {len(csv_files)}")

for file in csv_files:
    df = pd.read_csv(file, low_memory=False)

    missing = df.isna().sum()
    missing = missing[missing > 0].sort_values(ascending=False)

    if not missing.empty:
        report = pd.DataFrame({
            "missing_count": missing,
            "missing_percent": (
                missing / len(df) * 100
            ).round(2)
        })

        print(f"\n{'=' * 60}")
        print(f"TABLE: {file.name}")
        print(f"Rows: {len(df)}")
        print(report.to_string())
# Inspect devices.csv and payers.csv for reporting anomalies

for name in ["devices.csv", "payers.csv"]:
    file_path = Path("data/processed/ehr") / name
    df = pd.read_csv(file_path, low_memory=False)

    print(f"\n{'=' * 50}")
    print("TABLE:", name)
    print("Shape:", df.shape)
    print("Columns:", df.columns.tolist())
    print(
        "Duplicate column names:",
        df.columns[df.columns.duplicated()].tolist()
    )
    print("\nMissing values by column:")
    print(df.isna().sum().to_string())