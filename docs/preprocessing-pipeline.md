# Preprocessing Pipeline

## 1. EHR Preprocessing

Implementation: `scripts/ehr_preprocessing.py`

### Input and output

- Input: `data/ehr/`
- Processed output: `data/processed/ehr/`
- Reports: `reports/`

The script recursively discovers EHR CSV files, reads each file into memory,
inspects its original contents, cleans a separate DataFrame, and saves a
processed copy.

### Cleaning operations

1. Count exact duplicate rows.
2. Replace the known `1970-01-01T00:00:00Z` placeholder in the `TODATE`
   column of `claims_transactions.csv` with a missing value.
3. Remove exact duplicate rows from the processed copy.
4. Record rows before and after cleaning and the number of duplicates and
   placeholders handled.

The script does not perform general missing-value imputation. Its cleaning
log records `missing_values_imputed` as zero and `raw_data_modified` as false.

The implementation also creates the following reports:

- `ehr_data_quality_summary.csv`
- `ehr_column_quality_summary.csv`
- `ehr_cleaning_log.csv`

A table-processing failure is logged. After all files have been attempted,
the script raises a RuntimeError if any table failed.

## 2. Wearable Preprocessing

Implementation: `scripts/prepare_glucose_features.py`

### Input and output

- Input: configured HUPA-UCM preprocessed dataset directory.
- Processed output: `data/processed/wearable/`
- Summary: `reports/wearable_preprocessing_summary.csv`

### Processing steps

1. Read participant CSV files using a semicolon delimiter.
2. Check that all required columns exist.
3. Parse timestamps and convert measurement columns to numeric values.
4. Remove rows with invalid timestamps or missing glucose.
5. Sort observations chronologically.
6. Remove duplicate timestamps, keeping the first observation.
7. Verify that consecutive timestamps are exactly five minutes apart.
8. Generate historical glucose features and the two-hour target.
9. Save the processed participant file and update the summary report.

If a participant file fails validation or processing, the error is recorded
in the participant summary.

The raw wearable source files are preserved.

## 3. Feature Generation

The script generates lag features at one, three, six and twelve readings,
rolling statistics, glucose changes over 15 and 30 minutes, and a target
shifted 24 readings into the future.

At five-minute sampling intervals, 24 readings represent 120 minutes.

The rolling means and standard deviation use preceding readings. The current
glucose value is also included as a feature.

Rows without the historical values or future target needed for model inputs
and evaluation cannot be used where those values are missing.

## 4. Validation Findings

The ML methodology reports that 10 engineered feature columns were checked
against independently recomputed values across 25 processed participant
files: 250 comparisons, with zero failed comparisons.

This supports feature consistency for those checks. It does not independently
prove that the full training workflow is free from every form of leakage.
