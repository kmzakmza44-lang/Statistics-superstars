"""Tests for data loading, validation, and cleaning."""

import pandas as pd
import pytest

from scripts.clean_data import clean_student_data, validate_values
from src.data_loader import (
    load_processed_data,
    load_raw_data,
    save_processed_data,
)


def test_raw_dataset_quality() -> None:
    data = load_raw_data()

    assert data.shape == (649, 33)
    assert data.isna().sum().sum() == 0
    assert data.duplicated().sum() == 0


def test_cleaning_preserves_valid_observations() -> None:
    raw = load_raw_data()
    cleaned, _ = clean_student_data(raw)

    assert cleaned.shape == raw.shape
    assert cleaned["absences"].equals(raw["absences"])
    assert cleaned["G3"].equals(raw["G3"])
    assert (cleaned["G3"] == 0).sum() == 15


def test_cleaning_is_idempotent() -> None:
    raw = load_raw_data()

    cleaned_once, _ = clean_student_data(raw)
    cleaned_twice, _ = clean_student_data(cleaned_once)

    pd.testing.assert_frame_equal(cleaned_once, cleaned_twice)


def test_invalid_grade_is_rejected() -> None:
    data = load_raw_data()
    data.loc[0, "G3"] = 21

    with pytest.raises(ValueError, match="G3"):
        validate_values(data)


def test_processed_data_round_trip(tmp_path) -> None:
    original = load_raw_data()
    temporary_path = tmp_path / "cleaned_data.csv"

    save_processed_data(original, temporary_path)
    reloaded = load_processed_data(temporary_path)

    pd.testing.assert_frame_equal(original, reloaded)