import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="📊",
    layout="wide"
)


# --------------------------------------------------
# Load data
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "cleaned_data.csv"

from src.data_loader import load_processed_data

df = load_processed_data()


# --------------------------------------------------
# Dashboard title
# --------------------------------------------------

st.title("📊 Student Performance Dashboard")
st.markdown(
    "📚 **Data source:** "
    "[UCI Machine Learning Repository — Student Performance Dataset]"
    "(https://archive.ics.uci.edu/dataset/320/student+performance)"
)

st.info(
    "Note: These visualizations show associations between variables. "
    "Association does not prove causation."
)

st.divider()


# --------------------------------------------------
# Sidebar filters
# --------------------------------------------------

st.sidebar.header("Filters")

filtered_df = df.copy()

# School filter
if "school" in df.columns:
    school_options = sorted(df["school"].dropna().unique())
    selected_school = st.sidebar.multiselect(
        "School",
        school_options,
        default=school_options
    )

    filtered_df = filtered_df[
        filtered_df["school"].isin(selected_school)
    ]


# Sex filter
if "sex" in df.columns:
    sex_options = sorted(df["sex"].dropna().unique())
    selected_sex = st.sidebar.multiselect(
        "Sex",
        sex_options,
        default=sex_options
    )

    filtered_df = filtered_df[
        filtered_df["sex"].isin(selected_sex)
    ]


# Higher education intention

if "higher" in df.columns:
    higher_options = sorted(df["higher"].dropna().unique())
    selected_higher = st.sidebar.multiselect(
        "Higher education intention",
        higher_options,
        default=higher_options
    )

    filtered_df = filtered_df[
        filtered_df["higher"].isin(selected_higher)
    ]


# Study time filter

if "studytime" in df.columns:
    studytime_options = sorted(df["studytime"].dropna().unique())
    selected_studytime = st.sidebar.multiselect(
        "Study Time",
        studytime_options,
        default=studytime_options
    )

    filtered_df = filtered_df[
        filtered_df["studytime"].isin(selected_studytime)
    ]


# Failures filter

if "failures" in df.columns:
    failures_options = sorted(df["failures"].dropna().unique())
    selected_failures = st.sidebar.multiselect(
        "Previous Failures",
        failures_options,
        default=failures_options
    )

    filtered_df = filtered_df[
        filtered_df["failures"].isin(selected_failures)
    ]


# Internet filter

if "internet" in df.columns:
    internet_options = sorted(df["internet"].dropna().unique())
    selected_internet = st.sidebar.multiselect(
        "Internet Access",
        internet_options,
        default=internet_options
    )

    filtered_df = filtered_df[
        filtered_df["internet"].isin(selected_internet)
    ]


# Zero-student safety check

if filtered_df.empty:
    st.warning("No students match the selected filters.")
    st.stop()


# --------------------------------------------------
# Key statistics
# --------------------------------------------------

st.subheader("Key Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Students",
        len(filtered_df)
    )

with col2:
    st.metric(
        "Average Final Grade",
        f"{filtered_df['G3'].mean():.2f}"
    )

with col3:
    st.metric(
        "Median Final Grade",
        f"{filtered_df['G3'].median():.0f}"
    )

with col4:
    st.metric(
        "Average Absences",
        f"{filtered_df['absences'].mean():.2f}"
    )


st.divider()


# --------------------------------------------------
# Final grade distribution
# --------------------------------------------------

st.subheader("Final Grade Distribution")

fig, ax = plt.subplots(figsize=(10, 5))

sns.histplot(
    filtered_df["G3"].dropna(),
    bins=12,
    kde=True,
    ax=ax
)

ax.axvline(
    filtered_df["G3"].mean(),
    linestyle="--",
    label=f"Mean = {filtered_df['G3'].mean():.2f}"
)

ax.axvline(
    filtered_df["G3"].median(),
    linestyle=":",
    label=f"Median = {filtered_df['G3'].median():.0f}"
)

ax.set_title("Distribution of Final Grades")
ax.set_xlabel("Final Grade (G3)")
ax.set_ylabel("Number of Students")
ax.legend()

st.pyplot(fig)


# --------------------------------------------------
# Grade progression
# --------------------------------------------------

st.subheader("Grade Progression: G1 → G2 → G3")

grade_means = pd.DataFrame({
    "Assessment": ["G1", "G2", "G3"],
    "Average Grade": [
        filtered_df["G1"].mean(),
        filtered_df["G2"].mean(),
        filtered_df["G3"].mean()
    ]
})

st.line_chart(
    grade_means.set_index("Assessment")
)


# --------------------------------------------------
# Study time vs final grade
# --------------------------------------------------

st.subheader("Study Time vs Final Grade")

fig, ax = plt.subplots(figsize=(10, 5))

sns.boxplot(
    data=filtered_df,
    x="studytime",
    y="G3",
    ax=ax
)

ax.set_title("Final Grade by Study Time")
ax.set_xlabel("Study Time Level")
ax.set_ylabel("Final Grade (G3)")

st.pyplot(fig)


# --------------------------------------------------
# Failures vs final grade
# --------------------------------------------------

st.subheader("Previous Failures vs Final Grade")

fig, ax = plt.subplots(figsize=(10, 5))

sns.boxplot(
    data=filtered_df,
    x="failures",
    y="G3",
    ax=ax
)

ax.set_title("Final Grade by Number of Previous Failures")
ax.set_xlabel("Number of Previous Failures")
ax.set_ylabel("Final Grade (G3)")

st.pyplot(fig)


# --------------------------------------------------
# Absences vs final grade
# --------------------------------------------------

st.subheader("Absences vs Final Grade")

fig, ax = plt.subplots(figsize=(10, 5))

sns.scatterplot(
    data=filtered_df,
    x="absences",
    y="G3",
    alpha=0.6,
    ax=ax
)

ax.set_title("Relationship Between Absences and Final Grade")
ax.set_xlabel("Number of Absences")
ax.set_ylabel("Final Grade (G3)")

st.pyplot(fig)


# --------------------------------------------------
# Data preview
# --------------------------------------------------

with st.expander("View filtered data"):
    st.dataframe(
        filtered_df,
        width="stretch"
    )


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.divider()

st.caption(
    "Statistics Superstars — Exploratory Visualization Dashboard"
)
