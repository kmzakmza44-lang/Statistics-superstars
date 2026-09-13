"""Reusable statistical analysis functions for the student dataset."""

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd


class StatisticalAnalyzer:
    """Perform statistical analysis on a pandas DataFrame."""

    def __init__(self, data):
        self.data = data.copy()

        self.numeric_cols = self.data.select_dtypes(
            include="number"
        ).columns

        self.categorical_cols = self.data.columns[
            [
                pd.api.types.is_string_dtype(dtype)
                or isinstance(dtype, pd.CategoricalDtype)
                for dtype in self.data.dtypes
            ]
        ]

    def descriptive_stats(self, column):
        """Calculate descriptive statistics for one numeric column."""

        data = self.data[column].dropna()

        if len(data) == 0:
            return {
                "column": column,
                "error": "The column has no valid data"
            }

        mode_values = data.mode()

        if len(mode_values) > 0:
            mode = mode_values.iloc[0]
        else:
            mode = np.nan

        results = {
            "column": column,
            "n": len(data),
            "mean": data.mean(),
            "median": data.median(),
            "mode": mode,
            "std": data.std(),
            "variance": data.var(),
            "minimum": data.min(),
            "maximum": data.max(),
            "range": data.max() - data.min(),
            "q1": data.quantile(0.25),
            "q3": data.quantile(0.75),
            "iqr": data.quantile(0.75) - data.quantile(0.25),
            "skewness": data.skew(),
            "kurtosis": data.kurtosis(),
            "cv": data.std() / data.mean() if data.mean() != 0 else np.nan,
            "missing": self.data[column].isnull().sum()
        }

        return results

    def all_descriptive_stats(self):
        """Calculate descriptive statistics for every numeric column."""

        results = []

        for column in self.numeric_cols:
            column_results = self.descriptive_stats(column)
            results.append(column_results)

        return pd.DataFrame(results)

    def shapiro_wilk_test(self, column, alpha=0.05):
        """Perform the Shapiro-Wilk normality test."""

        data = self.data[column].dropna()

        if len(data) < 3:
            return {
                "column": column,
                "statistic": np.nan,
                "p_value": np.nan,
                "normal": False,
                "interpretation": "Sample size is too small"
            }

        statistic, p_value = stats.shapiro(data)
        normal = p_value > alpha

        if normal:
            interpretation = "Data appears normally distributed"
        else:
            interpretation = "Data does not appear normally distributed"

        return {
            "column": column,
            "statistic": statistic,
            "p_value": p_value,
            "normal": normal,
            "interpretation": interpretation
        }
    def kolmogorov_smirnov_test(self, column, dist="norm", alpha=0.05):
        """Perform the Kolmogorov-Smirnov goodness-of-fit test."""

        data = self.data[column].dropna()

        if dist == "norm":
            data_std = (data - data.mean()) / data.std()
            statistic, p_value = stats.kstest(data_std, "norm")

        elif dist == "expon":
            loc, scale = stats.expon.fit(data)
            statistic, p_value = stats.kstest(
                data,
                "expon",
                args=(loc, scale)
            )

        elif dist == "uniform":
            statistic, p_value = stats.kstest(
                data,
                "uniform",
                args=(data.min(), data.max() - data.min())
            )

        else:
            raise ValueError(f"Unsupported distribution: {dist}")

        fit_good = p_value > alpha

        return {
            "column": column,
            "distribution": dist,
            "statistic": statistic,
            "p_value": p_value,
            "good_fit": fit_good,
            "interpretation": "Good fit" if fit_good else "Poor fit"
        }
    def tukey_hsd_test(
        self,
        numeric_column,
        group_column,
        alpha=0.05
    ):
        """Run Tukey HSD pairwise comparisons after a significant ANOVA."""

        analysis_data = self.data[
            [numeric_column, group_column]
        ].dropna()

        if analysis_data[group_column].nunique() < 2:
            return pd.DataFrame({
                "error": ["At least two valid groups are required"]
            })

        result = pairwise_tukeyhsd(
            endog=analysis_data[numeric_column],
            groups=analysis_data[group_column],
            alpha=alpha
        )

        return pd.DataFrame(
            result._results_table.data[1:],
            columns=result._results_table.data[0]
        )

    def all_normality_tests(self, alpha=0.05):
        """Run the Shapiro-Wilk test on every numeric column."""

        results = []

        for column in self.numeric_cols:
            result = self.shapiro_wilk_test(column, alpha)
            results.append(result)

        return pd.DataFrame(results)

    def one_sample_t_test(
        self,
        column,
        expected_mean,
        alpha=0.05,
        alternative="two-sided"
    ):
        """Test a column mean against an expected mean."""

        data = self.data[column].dropna()

        statistic, p_value = stats.ttest_1samp(
            data,
            expected_mean,
            alternative=alternative
        )

        significant = p_value < alpha

        if alternative == "less":
            comparison = "less than"
        elif alternative == "greater":
            comparison = "greater than"
        else:
            comparison = "different from"

        if significant:
            interpretation = (
                f"The mean of {column} is significantly "
                f"{comparison} {expected_mean}"
            )
        else:
            interpretation = (
                f"There is insufficient evidence that the mean "
                f"of {column} is {comparison} {expected_mean}"
            )

        return {
            "test": "One-sample t-test",
            "variable": column,
            "sample_mean": data.mean(),
            "expected_mean": expected_mean,
            "statistic": statistic,
            "p_value": p_value,
            "df": len(data) - 1,
            "significant": significant,
            "interpretation": interpretation
        }
    def independent_t_test(
        self,
        numeric_column,
        group_column,
        group1,
        group2,
        alpha=0.05,
        alternative="two-sided"
    ):
        """Compare the means of two independent groups."""

        data1 = self.data[
            self.data[group_column] == group1
        ][numeric_column].dropna()

        data2 = self.data[
            self.data[group_column] == group2
        ][numeric_column].dropna()

        if len(data1) < 2 or len(data2) < 2:
            return {
                "test": "Independent t-test",
                "error": "Each group must contain at least two values"
            }

        statistic, p_value = stats.ttest_ind(
            data1,
            data2,
            equal_var=False,
            alternative=alternative
        )

        significant = p_value < alpha

        if alternative == "less":
            comparison = "less than"
        elif alternative == "greater":
            comparison = "greater than"
        else:
            comparison = "different from"

        if significant:
            interpretation = (
                f"The mean {numeric_column} for {group1} is significantly "
                f"{comparison} the mean for {group2}"
            )
        else:
            interpretation = (
                f"There is insufficient evidence that the mean "
                f"{numeric_column} for {group1} is "
                f"{comparison} the mean for {group2}"
            )

        return {
            "test": "Independent t-test",
            "numeric_variable": numeric_column,
            "group_variable": group_column,
            "group1": group1,
            "group2": group2,
            "group1_mean": data1.mean(),
            "group2_mean": data2.mean(),
            "mean_diff": data1.mean() - data2.mean(),
            "df": len(data1) + len(data2) - 2,
            "statistic": statistic,
            "p_value": p_value,
            "significant": significant,
            "interpretation": interpretation
        }
    def paired_t_test(
        self,
        column1,
        column2,
        alpha=0.05,
        alternative="two-sided"
    ):
        """Compare two measurements from the same observations."""

        paired_data = self.data[[column1, column2]].dropna()
        data1 = paired_data[column1]
        data2 = paired_data[column2]
        n = len(paired_data)

        if n < 2:
            return {
                "test": "Paired t-test",
                "error": "At least two complete pairs are required"
            }

        statistic, p_value = stats.ttest_rel(
            data1,
            data2,
            alternative=alternative
        )

        significant = p_value < alpha

        if alternative == "less":
            comparison = "less than"
        elif alternative == "greater":
            comparison = "greater than"
        else:
            comparison = "different from"

        if significant:
            interpretation = (
                f"The mean of {column1} is significantly "
                f"{comparison} the mean of {column2}"
            )
        else:
            interpretation = (
                f"There is insufficient evidence that the mean "
                f"of {column1} is {comparison} the mean of {column2}"
            )

        return {
            "test": "Paired t-test",
            "variable1": column1,
            "variable2": column2,
            "mean1": data1.mean(),
            "mean2": data2.mean(),
            "mean_diff": data1.mean() - data2.mean(),
            "statistic": statistic,
            "p_value": p_value,
            "df": n - 1,
            "significant": significant,
            "interpretation": interpretation
        }
    def anova_test(
        self,
        numeric_column,
        group_column,
        alpha=0.05
    ):
        """Compare a numeric variable across multiple groups."""

        groups = []
        group_names = []

        for group_name in self.data[group_column].dropna().unique():
            group_data = self.data[
                self.data[group_column] == group_name
            ][numeric_column].dropna()

            if len(group_data) >= 2:
                groups.append(group_data)
                group_names.append(group_name)

        if len(groups) < 2:
            return {
                "test": "One-way ANOVA",
                "error": "At least two valid groups are required"
            }

        statistic, p_value = stats.f_oneway(*groups)
        significant = p_value < alpha

        if significant:
            interpretation = (
                "At least one group has a significantly different mean"
            )
        else:
            interpretation = (
                "No significant difference was found among the groups"
            )

        return {
            "test": "One-way ANOVA",
            "numeric_variable": numeric_column,
            "group_variable": group_column,
            "groups": group_names,
            "statistic": statistic,
            "p_value": p_value,
            "significant": significant,
            "interpretation": interpretation
        }

    def chi_square_test(self, column1, column2, alpha=0.05):
        """Test whether two categorical variables are associated."""

        table = pd.crosstab(
            self.data[column1],
            self.data[column2]
        )

        statistic, p_value, degrees_of_freedom, expected = (
            stats.chi2_contingency(table)
        )

        significant = p_value < alpha

        if significant:
            interpretation = (
                f"{column1} and {column2} have a significant association"
            )
        else:
            interpretation = (
                f"No significant association was found between "
                f"{column1} and {column2}"
            )

        return {
            "test": "Chi-square test of independence",
            "variable1": column1,
            "variable2": column2,
            "statistic": statistic,
            "p_value": p_value,
            "degrees_of_freedom": degrees_of_freedom,
            "significant": significant,
            "interpretation": interpretation
        }

    def confidence_interval(self, column, confidence=0.95):
        """Calculate a confidence interval for a column mean."""

        data = self.data[column].dropna()
        n = len(data)

        if n < 2:
            return {
                "column": column,
                "error": "At least two values are required"
            }

        mean = data.mean()
        standard_deviation = data.std()
        standard_error = standard_deviation / np.sqrt(n)

        if n >= 30:
            critical_value = stats.norm.ppf(
                (1 + confidence) / 2
            )
            distribution = "Normal distribution"
        else:
            critical_value = stats.t.ppf(
                (1 + confidence) / 2,
                df=n - 1
            )
            distribution = "Student's t-distribution"

        margin_of_error = critical_value * standard_error
        lower_bound = mean - margin_of_error
        upper_bound = mean + margin_of_error

        return {
            "column": column,
            "n": n,
            "mean": mean,
            "standard_deviation": standard_deviation,
            "standard_error": standard_error,
            "confidence_level": confidence,
            "distribution": distribution,
            "lower_bound": lower_bound,
            "upper_bound": upper_bound,
            "margin_of_error": margin_of_error
        }

    def all_confidence_intervals(self, confidence=0.95):
        """Calculate confidence intervals for every numeric column."""

        results = []

        for column in self.numeric_cols:
            result = self.confidence_interval(
                column,
                confidence
            )
            results.append(result)

        return pd.DataFrame(results)

    def bootstrap_ci(
        self,
        column,
        statistic=np.mean,
        n_bootstrap=10000,
        confidence=0.95,
        random_seed=42
    ):
        """Calculate a bootstrap confidence interval for a statistic."""

        data = self.data[column].dropna().to_numpy()
        n = len(data)

        if n < 2:
            return {
                "column": column,
                "error": "At least two values are required"
            }

        random_generator = np.random.default_rng(random_seed)
        bootstrap_stats = []

        for repeat in range(n_bootstrap):
            sample = random_generator.choice(
                data,
                size=n,
                replace=True
            )

            bootstrap_stats.append(statistic(sample))

        alpha = 1 - confidence
        lower_percentile = (alpha / 2) * 100
        upper_percentile = (1 - alpha / 2) * 100

        lower_bound = np.percentile(
            bootstrap_stats,
            lower_percentile
        )

        upper_bound = np.percentile(
            bootstrap_stats,
            upper_percentile
        )

        return {
            "column": column,
            "statistic": statistic.__name__,
            "original_value": statistic(data),
            "n_bootstrap": n_bootstrap,
            "confidence_level": confidence,
            "lower_bound": lower_bound,
            "upper_bound": upper_bound,
            "bootstrap_mean": np.mean(bootstrap_stats),
            "bootstrap_std": np.std(bootstrap_stats)
        }
    
    def fit_distribution(self, column):
        """Fit several distributions and identify the best fit."""

        data = self.data[column].dropna().to_numpy()

        if len(data) < 3:
            return {
                "column": column,
                "error": "At least three values are required"
            }

        distributions = {
            "Normal": stats.norm,
            "Exponential": stats.expon,
            "Gamma": stats.gamma,
            "Lognormal": stats.lognorm,
            "Uniform": stats.uniform
        }

        fitting_results = {}

        for distribution_name, distribution in distributions.items():
            try:
                parameters = distribution.fit(data)

                statistic, p_value = stats.kstest(
                    data,
                    distribution.cdf,
                    args=parameters
                )

                fitting_results[distribution_name] = {
                    "parameters": parameters,
                    "ks_statistic": statistic,
                    "p_value": p_value,
                    "good_fit": p_value > 0.05
                }

            except Exception as error:
                fitting_results[distribution_name] = {
                    "error": str(error)
                }

        best_distribution = None
        best_p_value = -1

        for distribution_name, result in fitting_results.items():
            if "p_value" in result:
                if result["p_value"] > best_p_value:
                    best_p_value = result["p_value"]
                    best_distribution = distribution_name

        return {
            "column": column,
            "results": fitting_results,
            "best_fit": best_distribution,
            "best_p_value": best_p_value,
            "good_fit": best_p_value > 0.05
        }
