from pathlib import Path
import logging

import pandas as pd


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DIR = PROJECT_ROOT / "data" / "ehr"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed" / "ehr"
REPORTS_DIR = PROJECT_ROOT / "reports"

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)


def load_ehr_csv(file_path):
    """Load an EHR CSV without modifying the original file."""
    return pd.read_csv(file_path, low_memory=False)


def inspect_data(df, table_name):
    """Generate data-quality information for a table."""

    summary = {
        "table": table_name,
        "rows": len(df),
        "columns": len(df.columns),
        "exact_duplicates": int(df.duplicated().sum()),
        "total_missing_cells": int(df.isna().sum().sum()),
    }

    column_report = []

    for column in df.columns:
        series = df[column]

        column_report.append({
            "table": table_name,
            "column": column,
            "dtype": str(series.dtype),
            "missing_count": int(series.isna().sum()),
            "missing_percent": (
                round(series.isna().mean() * 100, 2)
                if len(series) else 0
            ),
            "unique_values": int(series.nunique(dropna=True)),
        })

    return summary, column_report


def clean_ehr_table(df, table_name):
    """
    Conservative EHR cleaning:
    1. Remove exact duplicate rows.
    2. Replace the known TODATE epoch placeholder
       in claims_transactions.csv with NaT.

    The original raw files are never modified.
    """

    cleaned_df = df.copy()

    # Track cleaning operations
    duplicates_removed = int(cleaned_df.duplicated().sum())
    date_placeholders_replaced = 0

    # Rule applies only to claims_transactions.csv
    if (
        table_name.replace("\\", "/")
        == "claims_transactions.csv"
    ):
        placeholder = (
            cleaned_df["TODATE"].astype(str).str.strip()
            == "1970-01-01T00:00:00Z"
        )

        date_placeholders_replaced = int(placeholder.sum())

        cleaned_df.loc[placeholder, "TODATE"] = pd.NA

    # Remove exact duplicate rows from the processed copy
    cleaned_df = cleaned_df.drop_duplicates().copy()

    cleaning_info = {
        "exact_duplicate_rows_removed": duplicates_removed,
        "date_placeholders_replaced": date_placeholders_replaced,
        "rows_before": int(len(df)),
        "rows_after": int(len(cleaned_df)),
        "missing_values_imputed": 0,
        "raw_data_modified": False,
    }

    return cleaned_df, cleaning_info


def process_ehr():
    """Inspect and preprocess every CSV under data/ehr."""

    if not RAW_DIR.exists():
        raise FileNotFoundError(
            f"EHR directory not found: {RAW_DIR}"
        )

    csv_files = sorted(RAW_DIR.rglob("*.csv"))

    if not csv_files:
        raise FileNotFoundError(
            f"No CSV files found in {RAW_DIR}"
        )

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    table_reports = []
    column_reports = []
    cleaning_logs = []

    for file_path in csv_files:

        relative_path = file_path.relative_to(RAW_DIR)
        table_name = str(relative_path).replace("\\", "/")

        logging.info("Processing %s", table_name)

        try:
            # Load original data into memory
            df = load_ehr_csv(file_path)

            # Inspect before cleaning
            summary, columns = inspect_data(
                df, table_name
            )

            # Clean a separate DataFrame
            cleaned_df, cleaning_info = clean_ehr_table(
                df, file_path.name
            )

            # Save a separate processed copy
            output_path = PROCESSED_DIR / relative_path
            output_path.parent.mkdir(
                parents=True, exist_ok=True
            )

            cleaned_df.to_csv(
                output_path,
                index=False
            )

            table_reports.append(summary)
            column_reports.extend(columns)

            cleaning_logs.append({
                "table": table_name,
                "status": "success",
                "rows_before": cleaning_info["rows_before"],
                "rows_after": cleaning_info["rows_after"],
                "duplicates_removed": (
                    cleaning_info["exact_duplicate_rows_removed"]
                ),
                "date_placeholders_replaced": (
                    cleaning_info["date_placeholders_replaced"]
                ),
                "missing_values_imputed": 0,
                "raw_data_modified": False,
            })

            logging.info(
                "Rows: %s -> %s",
                len(df),
                len(cleaned_df)
            )

        except Exception as error:
            logging.exception(
                "Failed to process %s", table_name
            )

            cleaning_logs.append({
                "table": table_name,
                "status": "failed",
                "error": str(error),
                "raw_data_modified": False,
            })

    # Save quality reports
    pd.DataFrame(table_reports).to_csv(
        REPORTS_DIR / "ehr_data_quality_summary.csv",
        index=False
    )

    pd.DataFrame(column_reports).to_csv(
        REPORTS_DIR / "ehr_column_quality_summary.csv",
        index=False
    )

    pd.DataFrame(cleaning_logs).to_csv(
        REPORTS_DIR / "ehr_cleaning_log.csv",
        index=False
    )

    successful = sum(
        row["status"] == "success"
        for row in cleaning_logs
    )

    failed = len(cleaning_logs) - successful

    print("\n========== EHR PIPELINE SUMMARY ==========")
    print(f"CSV files found: {len(csv_files)}")
    print(f"Successfully processed: {successful}")
    print(f"Failed: {failed}")
    print(f"Processed data: {PROCESSED_DIR}")
    print(f"Reports: {REPORTS_DIR}")
    print("Original EHR files were not modified.")
    print("==========================================")

    if failed:
        raise RuntimeError(
            f"{failed} table(s) failed. Check the logs."
        )


if __name__ == "__main__":
    process_ehr()