"""Reproducible cleaning pipeline for the Student Performance dataset."""

from pathlib import Path

import pandas as pd
from pandas.api.types import is_numeric_dtype

from src.data_loader import load_raw_data, save_processed_data


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = PROJECT_ROOT / "reports"
CLEANING_LOG_PATH = REPORTS_DIR / "cleaning_log.txt"

NUMERIC_RANGES = {
    "age": (15, 22),
    "Medu": (0, 4),
    "Fedu": (0, 4),
    "traveltime": (1, 4),
    "studytime": (1, 4),
    "failures": (0, 3),
    "famrel": (1, 5),
    "freetime": (1, 5),
    "goout": (1, 5),
    "Dalc": (1, 5),
    "Walc": (1, 5),
    "health": (1, 5),
    "absences": (0, None),
    "G1": (0, 20),
    "G2": (0, 20),
    "G3": (0, 20),
}

ALLOWED_VALUES = {
    "school": {"GP", "MS"},
    "sex": {"F", "M"},
    "address": {"U", "R"},
    "famsize": {"LE3", "GT3"},
    "Pstatus": {"T", "A"},
    "Mjob": {"teacher", "health", "services", "at_home", "other"},
    "Fjob": {"teacher", "health", "services", "at_home", "other"},
    "reason": {"home", "reputation", "course", "other"},
    "guardian": {"mother", "father", "other"},
}

YES_NO_COLUMNS = [
    "schoolsup",
    "famsup",
    "paid",
    "activities",
    "nursery",
    "higher",
    "internet",
    "romantic",
]


def validate_values(data: pd.DataFrame) -> None:
    """Validate numeric ranges and documented categorical values."""
    for column, (minimum, maximum) in NUMERIC_RANGES.items():
        if not is_numeric_dtype(data[column]):
            raise TypeError(f"Column '{column}' must be numeric.")

        invalid = data[column].lt(minimum)

        if maximum is not None:
            invalid = invalid | data[column].gt(maximum)

        if invalid.any():
            values = sorted(data.loc[invalid, column].unique())
            raise ValueError(
                f"Column '{column}' contains invalid values: {values}"
            )

    categorical_rules = ALLOWED_VALUES.copy()

    for column in YES_NO_COLUMNS:
        categorical_rules[column] = {"yes", "no"}

    for column, allowed in categorical_rules.items():
        actual = set(data[column].dropna().unique())
        invalid_values = sorted(actual - allowed)

        if invalid_values:
            raise ValueError(
                f"Column '{column}' contains invalid values: "
                f"{invalid_values}"
            )


def clean_student_data(
    data: pd.DataFrame,
) -> tuple[pd.DataFrame, list[str]]:
    """Clean the dataset without altering valid unusual observations."""
    cleaned = data.copy()
    log_entries = []

    original_rows, original_columns = cleaned.shape

    string_columns = cleaned.select_dtypes(
        include=["object", "string"]
    ).columns

    whitespace_changes = 0

    for column in string_columns:
        stripped = cleaned[column].str.strip()
        whitespace_changes += int(cleaned[column].ne(stripped).sum())
        cleaned[column] = stripped

    log_entries.append(
        f"Whitespace-normalized categorical cells: {whitespace_changes}"
    )

    missing_values = int(cleaned.isna().sum().sum())

    if missing_values:
        raise ValueError(
            f"Cleaning stopped: found {missing_values} missing values."
        )

    log_entries.append(
        "Missing values found: 0; no imputation was required."
    )

    duplicate_rows = int(cleaned.duplicated().sum())

    if duplicate_rows:
        cleaned = cleaned.drop_duplicates().reset_index(drop=True)

    log_entries.append(
        f"Completely duplicated rows removed: {duplicate_rows}"
    )

    validate_values(cleaned)
    log_entries.append(
        "All numeric and categorical values passed documented-range checks."
    )

    q1 = cleaned["absences"].quantile(0.25)
    q3 = cleaned["absences"].quantile(0.75)
    iqr = q3 - q1
    lower_limit = q1 - (1.5 * iqr)
    upper_limit = q3 + (1.5 * iqr)

    absence_flags = (
        cleaned["absences"].lt(lower_limit)
        | cleaned["absences"].gt(upper_limit)
    )
    absence_flag_count = int(absence_flags.sum())
    zero_g3_count = int(cleaned["G3"].eq(0).sum())

    log_entries.append(
        f"IQR-flagged absence records retained: {absence_flag_count}"
    )
    log_entries.append(
        f"G3 zero-grade records retained: {zero_g3_count}"
    )
    log_entries.append(
        "No valid observations were capped or removed as outliers."
    )
    log_entries.append(
        f"Original shape: {original_rows} rows x "
        f"{original_columns} columns"
    )
    log_entries.append(
        f"Cleaned shape: {cleaned.shape[0]} rows x "
        f"{cleaned.shape[1]} columns"
    )

    return cleaned, log_entries


def write_cleaning_log(log_entries: list[str]) -> Path:
    """Write a deterministic record of all cleaning decisions."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    report = [
        "DATA CLEANING LOG",
        "=================",
        "",
        "Dataset: UCI Student Performance - Portuguese course",
        "Pipeline: scripts/clean_data.py",
        "",
        *log_entries,
        "",
        "Result: Cleaning and validation completed successfully.",
    ]

    CLEANING_LOG_PATH.write_text(
        "\n".join(report) + "\n",
        encoding="utf-8",
    )

    return CLEANING_LOG_PATH


def main() -> None:
    """Run the complete cleaning pipeline."""
    raw_data = load_raw_data()
    cleaned_data, log_entries = clean_student_data(raw_data)

    output_path = save_processed_data(cleaned_data)
    log_path = write_cleaning_log(log_entries)

    print("Cleaning completed successfully.")
    print(f"Cleaned dataset: {output_path}")
    print(f"Cleaning log: {log_path}")
    print(f"Final shape: {cleaned_data.shape}")


if __name__ == "__main__":
    main()