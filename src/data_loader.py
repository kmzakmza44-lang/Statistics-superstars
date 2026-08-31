"""Reusable data-loading and validation utilities."""

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RAW_PATH = PROJECT_ROOT / "data" / "raw" / "student_performance.csv"
DEFAULT_PROCESSED_PATH = (
    PROJECT_ROOT / "data" / "processed" / "cleaned_data.csv"
)

EXPECTED_COLUMNS = [
    "school", "sex", "age", "address", "famsize", "Pstatus",
    "Medu", "Fedu", "Mjob", "Fjob", "reason", "guardian",
    "traveltime", "studytime", "failures", "schoolsup", "famsup",
    "paid", "activities", "nursery", "higher", "internet",
    "romantic", "famrel", "freetime", "goout", "Dalc", "Walc",
    "health", "absences", "G1", "G2", "G3",
]


def validate_structure(data: pd.DataFrame) -> None:
    """Raise an error when required columns are missing or unexpected."""
    actual_columns = list(data.columns)

    missing_columns = [
        column for column in EXPECTED_COLUMNS
        if column not in actual_columns
    ]
    unexpected_columns = [
        column for column in actual_columns
        if column not in EXPECTED_COLUMNS
    ]

    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}")

    if unexpected_columns:
        raise ValueError(f"Unexpected columns: {unexpected_columns}")

    if actual_columns != EXPECTED_COLUMNS:
        raise ValueError("Dataset columns are in the wrong order.")


def load_raw_data(path: Path | str = DEFAULT_RAW_PATH) -> pd.DataFrame:
    """Load and validate the standardized raw dataset."""
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Raw dataset not found: {path}")

    data = pd.read_csv(path)
    validate_structure(data)

    return data


def load_processed_data(
    path: Path | str = DEFAULT_PROCESSED_PATH,
) -> pd.DataFrame:
    """Load the processed dataset."""
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Processed dataset not found: {path}")

    data = pd.read_csv(path)
    validate_structure(data)

    return data


def save_processed_data(
    data: pd.DataFrame,
    path: Path | str = DEFAULT_PROCESSED_PATH,
) -> Path:
    """Validate and save a processed dataset."""
    path = Path(path)
    validate_structure(data)

    path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(path, index=False)

    return path