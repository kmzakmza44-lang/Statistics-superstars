# Week 2 Report Statistical Analysis

## Team Statistics Superstars

**Date:** September 10, 2026

## 1 Analysis approach and assumptions

The analysis uses a significance level of 0.05 and treats each row as an
independent student observation. The outcome `G3` is quantitative but discrete.
Week 1 Shapiro-Wilk tests showed that `G1`, `G2`, and `G3` are non-normal. The
large sample of 649 students makes t-tests and ANOVA reasonably robust for mean
comparisons, but their conclusions should still be interpreted cautiously.

The one-sample t-test assumes independent observations and an approximately
normal sampling distribution of the mean. The independent comparison uses
Welch's t-test, so it does not require equal group variances. One-way ANOVA
assumes independent observations, approximately normal within-group residuals,
and similar variances across groups. The chi-square test assumes independent,
mutually exclusive categories and sufficiently large expected cell counts; the
selected `sex` by `higher` table satisfies the expected-count condition.

## 2 Hypothesis testing results

### 2.1 One-sample t-test

The test examined $H_0: \mu_{G3}=10$ against the two-sided alternative that the
mean differs from 10.

- Sample mean: 11.906
- T-statistic: 15.030
- P-value: 5.068e-44
- Significant: Yes

The null hypothesis was rejected. The average `G3` grade was significantly
different from 10.

### 2.2 Independent t-test

Welch's independent t-test examined whether female and male students had the
same mean `G3` grade.

- Female mean: 12.253
- Male mean: 11.406
- T-statistic: 3.275
- P-value: 0.0011
- Significant: Yes

The null hypothesis was rejected. Female students had a higher sample mean than
male students, and the difference was statistically significant. This is an
association and does not show that sex causes the grade difference.

### 2.3 One-way ANOVA and Tukey HSD

The ANOVA examined whether all four study-time groups had the same mean `G3`.

- F-statistic: 15.876
- P-value: 5.706e-10
- Significant: Yes

The null hypothesis was rejected, so Tukey HSD pairwise comparisons were
performed while controlling family-wise error.

| Group 1 | Group 2 | Mean difference | Adjusted p-value | Significant |
|---:|---:|---:|---:|:---:|
| 1 | 2 | 1.2475 | 0.0001 | Yes |
| 1 | 3 | 2.3825 | <0.0001 | Yes |
| 1 | 4 | 2.2128 | 0.0007 | Yes |
| 2 | 3 | 1.1350 | 0.0103 | Yes |
| 2 | 4 | 0.9653 | 0.3084 | No |
| 3 | 4 | -0.1697 | 0.9927 | No |

Groups 1-2, 1-3, 1-4, and 2-3 differed significantly. Groups 2-4 and
3-4 did not. These results identify differences in this observational dataset,
not causal effects of study time.

### 2.4 Chi-square test

The test examined whether `sex` and intention to pursue higher education
(`higher`) were independent.

- Chi-square statistic: 1.827
- Degrees of freedom: 1
- P-value: 0.1765
- Significant: No

The null hypothesis was not rejected. No statistically significant association
was found between sex and intention to pursue higher education.

## 3 Distribution fitting

Normal, Exponential, Gamma, Lognormal, and Uniform distributions were fitted.

| Column | Best tested distribution | P-value | Good fit |
|---|---:|---:|:---:|
| age | Normal | 8.029e-18 | No |
| absences | Normal | 8.176e-27 | No |
| G1 | Lognormal | 4.932e-04 | No |
| G2 | Gamma | 3.802e-04 | No |
| G3 | Normal | 4.564e-09 | No |

Every p-value was below 0.05, so none of the candidates was a statistically
good fit. “Best tested distribution” means only the candidate with the largest
p-value. These fits are exploratory because the variables are discrete and the
ordinary Kolmogorov-Smirnov p-values do not adjust for parameters estimated
from the same observations.

![Observed G3 grades and best tested distribution](figures/distribution_fit_G3.png)

## 4 Confidence intervals

| Column | Mean | Traditional 95% CI | Bootstrap 95% CI |
|---|---:|---:|---:|
| age | 16.744 | 16.651 to 16.838 | 16.652 to 16.840 |
| absences | 3.659 | 3.302 to 4.017 | 3.307 to 4.032 |
| G1 | 11.399 | 11.188 to 11.610 | 11.186 to 11.609 |
| G2 | 11.570 | 11.346 to 11.794 | 11.339 to 11.797 |
| G3 | 11.906 | 11.657 to 12.155 | 11.652 to 12.151 |

The traditional and bootstrap intervals were very similar. For `G3`, both
methods estimated the population mean to be approximately 11.65 to 12.15.
Bootstrap intervals provide a useful robustness check given the non-normal raw
variables, although neither approach corrects sampling bias or dependence.

![Traditional and bootstrap confidence intervals](figures/confidence_intervals_comparison.png)

## 5 Key findings and limitations

1. Mean `G3` was significantly different from 10.
2. Female and male students had significantly different mean `G3` grades.
3. ANOVA and Tukey HSD identified specific study-time group differences.
4. `sex` and `higher` did not have a significant association.
5. None of the tested continuous distributions adequately fitted the selected
   discrete variables.
6. Traditional and bootstrap confidence intervals produced similar estimates.

The analyses identify associations rather than causation. Grade non-normality,
discrete measurement, possible confounding, and the observational study design
limit the conclusions. The ANOVA should be supplemented with a nonparametric
sensitivity analysis if stronger distributional robustness is required.

## 6 Recommendations for Week 3

- Highlight the significant study-time comparisons without implying causation.
- Add interactive filters for sex and study-time group to the dashboard.
- Display sample sizes and confidence intervals beside reported means.
- Use observed histograms or count plots rather than assuming normality.
- Consider a Kruskal-Wallis sensitivity analysis for `G3` by study time.
- Add plain-language notes explaining p-values, uncertainty, and limitations.

## 7 Team contributions

| Team member | Tasks completed | Approximate hours |
|---|---|---:|
| Student A | Data preparation, environment management, repository updates, and report structure | 2 |
| Student B | Statistical functions, automated tests, hypothesis tests, Tukey HSD, distribution fitting, confidence intervals, bootstrap analysis, and Week 2 documentation | 8 |
| Student C | Statistical visualizations, distribution plots, confidence-interval plot support, and dashboard work | 3 |
| All team members | Reviewed interpretations, checked calculations, discussed limitations, and prepared Week 3 questions | Shared |

## 8 Files generated

- `reports/hypothesis_tests_summary.csv`
- `reports/anova_tukey_hsd.csv`
- `reports/distribution_fitting_summary.csv`
- `reports/ci_comparison.csv`
- `reports/figures/distribution_fit_*.png`
- `reports/figures/confidence_intervals_comparison.png`
- `notebooks/02_hypothesis_testing.ipynb`
- `notebooks/03_distribution_fitting.ipynb`
- `notebooks/04_confidence_intervals.ipynb`
- `src/statistics.py`
- `tests/test_statistics.py`
