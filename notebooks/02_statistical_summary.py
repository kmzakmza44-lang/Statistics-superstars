import os
import pandas as pd

os.chdir("/Users/hsumonsan/Statistics-superstars")

df = pd.read_csv("data/processed/cleaned_data.csv")

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
summary.to_csv("reports/summary_statistics.csv")
from scipy import stats

results = {
    "Column": [],
    "Statistic": [],
    "P-value": [],
    "Normal?": []
}

for col in numeric_cols:
    data = df[col].dropna()
    stat, p_value = stats.shapiro(data)

    results["Column"].append(col)
    results["Statistic"].append(stat)
    results["P-value"].append(p_value)
    results["Normal?"].append(p_value > 0.05)

normality_df = pd.DataFrame(results)

print("\nNormality Tests:")
print(normality_df)

normality_df.to_csv("reports/normality_tests.csv", index=False)
# Correlation analysis

pearson = df[numeric_cols].corr()
spearman = df[numeric_cols].corr(method="spearman")

print("\nPearson Correlation:")
print(pearson)

print("\nSpearman Correlation:")
print(spearman)

pearson.to_csv("reports/pearson_correlation.csv")
spearman.to_csv("reports/spearman_correlation.csv")
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