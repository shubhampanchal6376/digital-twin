# Dataset Structure

## 1. EHR Dataset

The EHR preprocessing script reads CSV files recursively from:

`data/ehr/`

It writes processed copies to:

`data/processed/ehr/`

The relative directory structure is preserved when processed files are
written. Original source files are not modified by the preprocessing script.

The code inspects each table for:

- Number of rows and columns.
- Exact duplicate rows.
- Total missing cells.
- Column data types.
- Missing counts and percentages per column.
- Number of distinct non-missing values.

The quality report includes tables such as patients, observations, encounters,
conditions, medications, claims and claims transactions.

The inspected EHR summary reports 108 rows in `patients.csv` and 68,648
rows in `observations.csv`. These figures describe the supplied report and
may change if the dataset changes.

## 2. Wearable Dataset

The configured source directory is:

`data/wearable/HUPA-UCM/HUPA-UCM Diabetes Dataset/Preprocessed/`

The source consists of semicolon-delimited participant CSV files.

The preprocessing script requires these columns:

| Column | Description |
|---|---|
| `time` | Observation timestamp |
| `glucose` | Glucose measurement |
| `calories` | Calorie signal |
| `heart_rate` | Heart-rate signal |
| `steps` | Step-count signal |
| `basal_rate` | Basal insulin-rate signal |
| `bolus_volume_delivered` | Delivered bolus volume |
| `carb_input` | Carbohydrate input signal |

Processed participant files are written to:

`data/processed/wearable/`

## 3. Reported Dataset Quality

The ML methodology documents an initial wearable audit covering 25 participant
files and 309,392 observations.

That audit reported no missing glucose values, invalid timestamps, or duplicate
timestamps, and a median sampling interval of five minutes. Subsequent checks
reported consistent five-minute spacing and no invalid or infinite values
in the audited numeric columns.

These findings describe the audited data and should not be treated as a
guarantee for future datasets.

## 4. Related Reports

- `reports/ehr_data_quality_summary.csv`
- `reports/ehr_column_quality_summary.csv`
- `reports/ehr_cleaning_log.csv`
- `reports/wearable_glucose_quality_summary.csv`
- `reports/wearable_glucose_episode_summary.csv`
- `reports/wearable_preprocessing_summary.csv`

## 5. Data Availability

The repository README lists `data/.gitkeep` in its project tree. Confirm
dataset availability in the working environment before running preprocessing.
Do not assume that all raw datasets are tracked in Git.
