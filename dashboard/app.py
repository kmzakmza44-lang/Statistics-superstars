"""Interactive dashboard for the cleaned Student Performance dataset."""

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data_loader import load_processed_data  # noqa: E402


DATA_PATH = PROJECT_ROOT / "data" / "processed" / "cleaned_data.csv"
UCI_URL = "https://archive.ics.uci.edu/dataset/320/student%2Bperformance"

FILTER_LABELS = {
    "school": "School",
    "sex": "Sex",
    "higher": "Higher-education intention",
    "internet": "Internet access at home",
    "studytime": "Weekly study-time level",
    "failures": "Previous failures",
}

VALUE_LABELS = {
    "school": {
        "GP": "GP — Gabriel Pereira",
        "MS": "MS — Mousinho da Silveira",
    },
    "sex": {"F": "F — Female", "M": "M — Male"},
    "higher": {"yes": "Yes", "no": "No"},
    "internet": {"yes": "Yes", "no": "No"},
    "studytime": {
        1: "1 — Less than 2 hours",
        2: "2 — 2 to 5 hours",
        3: "3 — 5 to 10 hours",
        4: "4 — More than 10 hours",
    },
    "failures": {
        0: "0 — None",
        1: "1 failure",
        2: "2 failures",
        3: "3 or more failures",
    },
}


@st.cache_data(show_spinner=False)
def load_dashboard_data(path: str) -> pd.DataFrame:
    """Load and validate the processed dataset once per Streamlit session."""
    return load_processed_data(Path(path))


def format_filter_value(column: str, value: object) -> str:
    """Return a reader-friendly label while preserving the stored value."""
    return VALUE_LABELS.get(column, {}).get(value, str(value))


st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="📊",
    layout="wide",
)

sns.set_theme(style="whitegrid", palette="colorblind")
df = load_dashboard_data(str(DATA_PATH))

st.title("📊 Student Performance Dashboard")
st.markdown(
    "Explore academic, demographic, and study-related characteristics for "
    "**649 students in the Portuguese-language course dataset**."
)
st.caption(
    "The dashboard reports descriptive patterns and associations. "
    "It does not prove that any characteristic causes a change in grades."
)
st.divider()


st.sidebar.header("Filters")
st.sidebar.caption("Choose one or more values in every category.")

filtered_df = df.copy()
for column, label in FILTER_LABELS.items():
    options = sorted(df[column].dropna().unique().tolist())
    selected = st.sidebar.multiselect(
        label,
        options,
        default=options,
        format_func=lambda value, col=column: format_filter_value(col, value),
    )
    filtered_df = filtered_df[filtered_df[column].isin(selected)]

if filtered_df.empty:
    st.warning(
        "No students match the selected filters. Choose at least one value "
        "in every filter or broaden the selection."
    )
    st.stop()


st.subheader("Key statistics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Students", f"{len(filtered_df):,}")
col2.metric("Average final grade", f"{filtered_df['G3'].mean():.2f} / 20")
col3.metric("Median final grade", f"{filtered_df['G3'].median():.0f} / 20")
col4.metric("Average absences", f"{filtered_df['absences'].mean():.2f}")
st.caption(
    f"The filters currently include {len(filtered_df) / len(df):.1%} "
    "of the complete dataset."
)
st.divider()


left, right = st.columns(2)

with left:
    st.subheader("Final-grade distribution")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(filtered_df["G3"], bins=range(0, 22), kde=True, ax=ax)
    mean_grade = filtered_df["G3"].mean()
    median_grade = filtered_df["G3"].median()
    ax.axvline(mean_grade, color="#D55E00", linestyle="--", label=f"Mean = {mean_grade:.2f}")
    ax.axvline(median_grade, color="#0072B2", linestyle=":", label=f"Median = {median_grade:.0f}")
    ax.set(title="Distribution of Final Grades", xlabel="Final grade (G3, 0–20)", ylabel="Students")
    ax.legend()
    st.pyplot(fig, width="stretch")
    plt.close(fig)

with right:
    st.subheader("Average grade progression")
    grade_means = filtered_df[["G1", "G2", "G3"]].mean()
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(grade_means.index, grade_means.values, marker="o", color="#0072B2", linewidth=2)
    for assessment, value in grade_means.items():
        ax.annotate(f"{value:.2f}", (assessment, value), xytext=(0, 8), textcoords="offset points", ha="center")
    ax.set(title="Mean Grades Across Three Assessments", xlabel="Assessment", ylabel="Average grade (0–20)", ylim=(0, 20))
    st.pyplot(fig, width="stretch")
    plt.close(fig)


left, right = st.columns(2)

with left:
    st.subheader("Study time and final grade")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=filtered_df, x="studytime", y="G3", color="#56B4E9", ax=ax)
    ax.set(title="Final Grade by Weekly Study-Time Level", xlabel="Study-time level (1–4)", ylabel="Final grade (G3, 0–20)")
    st.pyplot(fig, width="stretch")
    plt.close(fig)

with right:
    st.subheader("Previous failures and final grade")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=filtered_df, x="failures", y="G3", color="#E69F00", ax=ax)
    ax.set(title="Final Grade by Previous Failures", xlabel="Previous failures", ylabel="Final grade (G3, 0–20)")
    st.pyplot(fig, width="stretch")
    plt.close(fig)


st.subheader("Absences and final grade")
fig, ax = plt.subplots(figsize=(11, 5))
sns.scatterplot(data=filtered_df, x="absences", y="G3", alpha=0.65, color="#009E73", ax=ax)
ax.set(title="Relationship Between Absences and Final Grade", xlabel="Number of absences", ylabel="Final grade (G3, 0–20)")
st.pyplot(fig, width="stretch")
plt.close(fig)
st.caption(
    "Each point represents one student. Visible patterns are associations and "
    "may be influenced by other variables in the dataset."
)


with st.expander("View and download filtered data"):
    st.dataframe(filtered_df, width="stretch")
    st.download_button(
        "Download filtered data as CSV",
        data=filtered_df.to_csv(index=False).encode("utf-8"),
        file_name="filtered_student_performance.csv",
        mime="text/csv",
    )


st.divider()
st.markdown(f"**Dataset source:** [UCI Student Performance Dataset]({UCI_URL})")
st.caption("Statistics Superstars — Exploratory Visualization Dashboard")
