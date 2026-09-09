# Week 2 Report Statistical Analysis

## Team Statistics Superstars

## 1 Hypothesis Testing Results

### 1.1 One Sample T Test

A one-sample t-test was conducted to determine whether the average
final grade, G3, was significantly different from 10.

- Sample mean: 11.906
- T-statistic: 15.030
- P-value: 5.068e-44
- Significant: Yes

The p-value was below 0.05, so the null hypothesis was rejected.
The average G3 grade was significantly different from 10.

### 1.2 Independent T Test

An independent t-test was conducted to compare the average G3 grades
of female and male students.

- Female mean: 12.253
- Male mean: 11.406
- T-statistic: 3.275
- P-value: 0.0011
- Significant: Yes

The p-value was below 0.05, so the null hypothesis was rejected.
Female and male students had significantly different average final
grades in this dataset. Female students had the higher average grade.
This result shows an association but does not prove causation.

### 1.3 One Way ANOVA

A one-way ANOVA was conducted to compare average G3 grades across
the four study-time groups.

- F-statistic: 15.876
- P-value: 5.706e-10
- Significant: Yes

The p-value was below 0.05, so the null hypothesis was rejected.
At least one study-time group had a significantly different average
G3 grade. A post-hoc test would be required to identify exactly
which groups differed.

### 1.4 Chi Square Test

A chi-square test of independence was conducted to examine the
association between sex and intention to pursue higher education.

- Chi-square statistic: 1.827
- Degrees of freedom: 1
- P-value: 0.1765
- Significant: No

The p-value was greater than 0.05, so the null hypothesis was not
rejected. No statistically significant association was found between
sex and intention to pursue higher education.

## 2 Distribution Fitting

Five distributions were considered: Normal, Exponential, Gamma,
Lognormal, and Uniform.

| Column | Best Tested Distribution | P-value | Good Fit |
|---|---:|---:|---:|
| age | Normal | 8.029e-18 | No |
| absences | Normal | 8.176e-27 | No |
| G1 | Lognormal | 4.932e-04 | No |
| G2 | Gamma | 3.802e-04 | No |
| G3 | Normal | 4.564e-09 | No |

All p-values were below 0.05. Therefore, none of the tested
distributions provided a statistically good fit. The term best fit
means only that the distribution had the highest p-value among the
tested options.

## 3 Confidence Intervals

### 3.1 Traditional and Bootstrap Intervals

| Column | Mean | Traditional 95% CI | Bootstrap 95% CI |
|---|---:|---:|---:|
| age | 16.744 | 16.651 to 16.838 | 16.652 to 16.840 |
| absences | 3.659 | 3.302 to 4.017 | 3.307 to 4.032 |
| G1 | 11.399 | 11.188 to 11.610 | 11.186 to 11.609 |
| G2 | 11.570 | 11.346 to 11.794 | 11.339 to 11.797 |
| G3 | 11.906 | 11.657 to 12.155 | 11.652 to 12.151 |

The traditional and bootstrap confidence intervals were very similar.
This indicates that the estimated means were stable for this sample.
For G3, the population mean was estimated to be between approximately
11.65 and 12.15 with 95% confidence.

## 4 Key Findings

1. The average G3 grade was significantly different from 10.
2. Female and male students had significantly different average G3
   grades in this dataset.
3. At least one study-time group had a different average G3 grade.
4. Sex and intention to pursue higher education did not have a
   statistically significant association.
5. None of the tested continuous distributions provided a good fit
   for the five selected variables.
6. Traditional and bootstrap confidence intervals produced similar
   results.

## 5 Limitations

The analyses identify statistical associations and differences but
do not prove causation. Some variables, including grades, are discrete,
which can make continuous probability distributions fit poorly.
Additional post-hoc testing is needed to identify which study-time
groups differ after the significant ANOVA result.

## 6 Files Generated

- reports/hypothesis_tests_summary.csv
- reports/distribution_fitting_summary.csv
- reports/ci_comparison.csv
- reports/figures/distribution_fit_age.png
- reports/figures/distribution_fit_absences.png
- reports/figures/distribution_fit_G1.png
- reports/figures/distribution_fit_G2.png
- reports/figures/distribution_fit_G3.png
- reports/figures/confidence_intervals_comparison.png
- notebooks/02_hypothesis_testing.ipynb
- notebooks/03_distribution_fitting.ipynb
- notebooks/04_confidence_intervals.ipynb
- src/statistics.py

## 7 Student B Contribution

Student B implemented the statistical analysis module, conducted the
hypothesis tests, fitted probability distributions, calculated
traditional and bootstrap confidence intervals, generated statistical
figures, saved the result tables, and documented the Week 2 findings.