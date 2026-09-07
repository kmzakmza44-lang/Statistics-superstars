from pathlib import Path
import sys
import pandas as pd
from scipy import stats

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.data_loader import load_processed_data

df = load_processed_data()

REPORTS_DIR = PROJECT_ROOT / "reports"



print(df.head())
numeric_cols = df.select_dtypes(include=['number']).columns

print("\nNumeric columns:")
print(numeric_cols)

print("\nSummary Statistics:")
print(df[numeric_cols].describe())
summary = pd.DataFrame()

summary["Mean"] = df[numeric_cols].mean()
summary["Median"] = df[numeric_cols].median()
summary["Mode"] = df[numeric_cols].mode().iloc[0]
summary["Std"] = df[numeric_cols].std()
summary["Variance"] = df[numeric_cols].var()
summary["Skewness"] = df[numeric_cols].skew()
summary["Kurtosis"] = df[numeric_cols].kurt()

summary["Q1"] = df[numeric_cols].quantile(0.25)
summary["Q3"] = df[numeric_cols].quantile(0.75)

summary["Range"] = df[numeric_cols].max() - df[numeric_cols].min()
summary["IQR"] = summary["Q3"] - summary["Q1"]

summary["CV"] = summary["Std"] / summary["Mean"] * 100

summary["Missing %"] = df[numeric_cols].isnull().mean() * 100

print("\nFull Summary Statistics:")
print(summary)
summary.to_csv(REPORTS_DIR / "summary_statistics.csv")

results = {
    "Column": [],
    "Statistic": [],
    "P-value": [],
    "Normal?": []
}

normality_cols = ["age", "absences", "G1", "G2", "G3"]
for col in normality_cols:
    data = df[col].dropna()
    stat, p_value = stats.shapiro(data)

    results["Column"].append(col)
    results["Statistic"].append(stat)
    results["P-value"].append(p_value)
    results["Normal?"].append(p_value > 0.05)

normality_df = pd.DataFrame(results)

print("\nNormality Tests:")
print(normality_df)

normality_df.to_csv(
    REPORTS_DIR / "normality_tests.csv",
    index=False
)
# Correlation analysis

pearson = df[numeric_cols].corr()
spearman = df[numeric_cols].corr(method="spearman")

print("\nPearson Correlation:")
print(pearson)

print("\nSpearman Correlation:")
print(spearman)

pearson.to_csv(REPORTS_DIR / "pearson_correlation.csv")
spearman.to_csv(REPORTS_DIR / "spearman_correlation.csv")
corr_pairs = []

for i in range(len(pearson.columns)):
    for j in range(i + 1, len(pearson.columns)):
        corr_value = pearson.iloc[i, j]

        corr_pairs.append({
            "Variable 1": pearson.columns[i],
            "Variable 2": pearson.columns[j],
            "Correlation": corr_value,
            "Strength": abs(corr_value)
        })

corr_pairs = sorted(
    corr_pairs,
    key=lambda x: x["Strength"],
    reverse=True
)

print("\nTop 5 Pearson Correlations:")

for i in range(5):
    pair = corr_pairs[i]

    print(
        i + 1,
        pair["Variable 1"],
        "<->",
        pair["Variable 2"],
        ":",
        round(pair["Correlation"], 3)
    )
    
spearman_pairs = []

for i in range(len(spearman.columns)):
    for j in range(i + 1, len(spearman.columns)):
        corr_value = spearman.iloc[i, j]

        spearman_pairs.append({
            "Variable 1": spearman.columns[i],
            "Variable 2": spearman.columns[j],
            "Correlation": corr_value,
            "Strength": abs(corr_value)
        })

spearman_pairs = sorted(
    spearman_pairs,
    key=lambda x: x["Strength"],
    reverse=True
)

print("\nTop 5 Spearman Correlations:")

for i in range(5):
    pair = spearman_pairs[i]

    print(
        i + 1,
        pair["Variable 1"],
        "<->",
        pair["Variable 2"],
        ":",
        round(pair["Correlation"], 3)
    )
    
print("\n--- Statistical Interpretation ---")

print("""
1. Summary Statistics:
The average final grade (G3) is approximately 11.91, with a median of 12.
The average first-period grade (G1) is approximately 11.40, while the
average second-period grade (G2) is approximately 11.57.

Student absences have a mean of approximately 3.66 and a median of 2.
The positive skewness of absences indicates that most students have
relatively few absences, while a smaller number of students have many absences.

The failures variable is also strongly positively skewed. Its median and
mode are both 0, meaning most students have no previous class failures.

There are no missing values in the numeric variables.

2. Normality Tests:
The Shapiro-Wilk tests for age, absences, G1, G2, and G3 produced
p-values below 0.05. Therefore, these variables show statistically
significant departures from a normal distribution.

Ordinal variables such as studytime, health, Dalc, Walc, Medu, and Fedu
were not included in the normality test because they represent ordered
categories rather than continuous measurements.

3. Correlation Analysis:
G2 and G3 have the strongest positive Pearson correlation, approximately
0.919. This means students with higher second-period grades tend to have
higher final grades.

G1 and G2 also have a strong positive correlation of approximately 0.865,
while G1 and G3 have a strong positive correlation of approximately 0.826.

For ordinal variables, Spearman correlation is more appropriate.
Medu and Fedu show a positive Spearman relationship, meaning higher
mother's education levels tend to be associated with higher father's
education levels.

Dalc and Walc also show a positive Spearman relationship, meaning students
who report higher workday alcohol consumption also tend to report higher
weekend alcohol consumption.

These correlations describe associations between variables and do not
prove that one variable causes another.
""")