"""Automated tests for the reusable statistical analysis module."""

import numpy as np
import pandas as pd
import pytest

from src.statistics import StatisticalAnalyzer


@pytest.fixture
def analyzer():
    """Return a small deterministic dataset with numeric and group columns."""

    data = pd.DataFrame({
        "score": [8, 9, 10, 11, 12, 18, 19, 20, 21, 22, 28, 29, 30, 31, 32],
        "score_2": [7, 8, 9, 10, 11, 17, 18, 19, 20, 21, 27, 28, 29, 30, 31],
        "group": ["A"] * 5 + ["B"] * 5 + ["C"] * 5,
        "choice": ["yes", "yes", "no", "yes", "no"] * 3,
    })
    return StatisticalAnalyzer(data)


def test_descriptive_statistics(analyzer):
    result = analyzer.descriptive_stats("score")

    assert result["n"] == 15
    assert result["mean"] == pytest.approx(20.0)
    assert result["range"] == 24


def test_all_descriptive_statistics_contains_numeric_columns(analyzer):
    result = analyzer.all_descriptive_stats()

    assert set(result["column"]) == {"score", "score_2"}


def test_shapiro_wilk_returns_expected_fields(analyzer):
    result = analyzer.shapiro_wilk_test("score")

    assert 0 <= result["p_value"] <= 1
    assert isinstance(result["normal"], (bool, np.bool_))


def test_all_normality_tests_contains_numeric_columns(analyzer):
    result = analyzer.all_normality_tests()

    assert set(result["column"]) == {"score", "score_2"}


def test_one_sample_t_test_detects_difference(analyzer):
    result = analyzer.one_sample_t_test("score", 10)

    assert result["sample_mean"] == pytest.approx(20.0)
    assert result["significant"]


def test_independent_t_test_detects_group_difference(analyzer):
    result = analyzer.independent_t_test("score", "group", "A", "C")

    assert result["group1_mean"] == pytest.approx(10.0)
    assert result["group2_mean"] == pytest.approx(30.0)
    assert result["significant"]


def test_anova_and_tukey_identify_group_differences(analyzer):
    anova = analyzer.anova_test("score", "group")
    tukey = analyzer.tukey_hsd_test("score", "group")

    assert anova["significant"]
    assert len(tukey) == 3
    assert tukey["reject"].all()


def test_chi_square_returns_valid_probability(analyzer):
    result = analyzer.chi_square_test("group", "choice")

    assert 0 <= result["p_value"] <= 1
    assert result["degrees_of_freedom"] == 2


def test_confidence_interval_contains_mean(analyzer):
    result = analyzer.confidence_interval("score")

    assert result["lower_bound"] < result["mean"] < result["upper_bound"]
    assert result["confidence_level"] == 0.95


def test_all_confidence_intervals_contains_numeric_columns(analyzer):
    result = analyzer.all_confidence_intervals()

    assert set(result["column"]) == {"score", "score_2"}


def test_bootstrap_interval_is_reproducible(analyzer):
    first = analyzer.bootstrap_ci("score", n_bootstrap=500, random_seed=7)
    second = analyzer.bootstrap_ci("score", n_bootstrap=500, random_seed=7)

    assert first["lower_bound"] == second["lower_bound"]
    assert first["upper_bound"] == second["upper_bound"]


def test_distribution_fitting_returns_a_candidate(analyzer):
    result = analyzer.fit_distribution("score")

    assert result["best_fit"] in {
        "Normal", "Exponential", "Gamma", "Lognormal", "Uniform"
    }
    assert 0 <= result["best_p_value"] <= 1
