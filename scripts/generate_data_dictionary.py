"""Generate a documented data dictionary for the processed dataset."""

from pathlib import Path

import pandas as pd

from src.data_loader import load_processed_data


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = PROJECT_ROOT / "reports" / "data_dictionary.csv"

METADATA = {
    "school": (
        "Predictor", "Nominal", "Student's school",
        "GP = Gabriel Pereira; MS = Mousinho da Silveira",
    ),
    "sex": (
        "Predictor", "Nominal", "Student's sex",
        "F = female; M = male",
    ),
    "age": (
        "Predictor", "Ratio", "Student's age in years",
        "Integer from 15 to 22",
    ),
    "address": (
        "Predictor", "Nominal", "Student's home address type",
        "U = urban; R = rural",
    ),
    "famsize": (
        "Predictor", "Ordinal", "Family size",
        "LE3 = three or fewer; GT3 = more than three",
    ),
    "Pstatus": (
        "Predictor", "Nominal", "Parents' cohabitation status",
        "T = living together; A = living apart",
    ),
    "Medu": (
        "Predictor", "Ordinal", "Mother's education level",
        "0 = none; 1 = primary; 2 = grades 5-9; "
        "3 = secondary; 4 = higher education",
    ),
    "Fedu": (
        "Predictor", "Ordinal", "Father's education level",
        "0 = none; 1 = primary; 2 = grades 5-9; "
        "3 = secondary; 4 = higher education",
    ),
    "Mjob": (
        "Predictor", "Nominal", "Mother's occupation",
        "teacher, health, services, at_home, or other",
    ),
    "Fjob": (
        "Predictor", "Nominal", "Father's occupation",
        "teacher, health, services, at_home, or other",
    ),
    "reason": (
        "Predictor", "Nominal", "Reason for choosing the school",
        "home, reputation, course, or other",
    ),
    "guardian": (
        "Predictor", "Nominal", "Student's guardian",
        "mother, father, or other",
    ),
    "traveltime": (
        "Predictor", "Ordinal", "Home-to-school travel time",
        "1 = under 15 min; 2 = 15-30 min; "
        "3 = 30-60 min; 4 = over 60 min",
    ),
    "studytime": (
        "Predictor", "Ordinal", "Weekly study time",
        "1 = under 2 hr; 2 = 2-5 hr; "
        "3 = 5-10 hr; 4 = over 10 hr",
    ),
    "failures": (
        "Predictor", "Ratio", "Number of previous class failures",
        "Integer from 0 to 3",
    ),
    "schoolsup": (
        "Predictor", "Nominal", "Extra educational support",
        "yes or no",
    ),
    "famsup": (
        "Predictor", "Nominal", "Family educational support",
        "yes or no",
    ),
    "paid": (
        "Predictor", "Nominal", "Extra paid classes",
        "yes or no",
    ),
    "activities": (
        "Predictor", "Nominal", "Extracurricular activities",
        "yes or no",
    ),
    "nursery": (
        "Predictor", "Nominal", "Attended nursery school",
        "yes or no",
    ),
    "higher": (
        "Predictor", "Nominal", "Wants higher education",
        "yes or no",
    ),
    "internet": (
        "Predictor", "Nominal", "Internet access at home",
        "yes or no",
    ),
    "romantic": (
        "Predictor", "Nominal", "Currently in a romantic relationship",
        "yes or no",
    ),
    "famrel": (
        "Predictor", "Ordinal", "Quality of family relationships",
        "1 = very bad to 5 = excellent",
    ),
    "freetime": (
        "Predictor", "Ordinal", "Free time after school",
        "1 = very low to 5 = very high",
    ),
    "goout": (
        "Predictor", "Ordinal", "Frequency of going out with friends",
        "1 = very low to 5 = very high",
    ),
    "Dalc": (
        "Predictor", "Ordinal", "Workday alcohol consumption",
        "1 = very low to 5 = very high",
    ),
    "Walc": (
        "Predictor", "Ordinal", "Weekend alcohol consumption",
        "1 = very low to 5 = very high",
    ),
    "health": (
        "Predictor", "Ordinal", "Current health status",
        "1 = very bad to 5 = very good",
    ),
    "absences": (
        "Predictor", "Ratio", "Number of school absences",
        "Non-negative integer",
    ),
    "G1": (
        "Predictor", "Interval", "First-period grade",
        "Integer from 0 to 20",
    ),
    "G2": (
        "Predictor", "Interval", "Second-period grade",
        "Integer from 0 to 20",
    ),
    "G3": (
        "Outcome", "Interval", "Final grade",
        "Integer from 0 to 20",
    ),
}


def create_data_dictionary(data: pd.DataFrame) -> pd.DataFrame:
    """Create metadata and observed-value summaries for every column."""
    missing_metadata = set(data.columns) - set(METADATA)

    if missing_metadata:
        raise ValueError(
            f"Missing metadata for columns: {sorted(missing_metadata)}"
        )

    records = []

    for column in data.columns:
        role, scale, description, coding = METADATA[column]
        observed = data[column].dropna()
        examples = sorted(observed.unique().tolist())[:5]

        if pd.api.types.is_numeric_dtype(data[column]):
            minimum = data[column].min()
            maximum = data[column].max()
        else:
            minimum = ""
            maximum = ""

        records.append(
            {
                "column": column,
                "role": role,
                "measurement_scale": scale,
                "pandas_dtype": str(data[column].dtype),
                "description": description,
                "coding": coding,
                "missing_count": int(data[column].isna().sum()),
                "missing_percent": round(
                    data[column].isna().mean() * 100,
                    2,
                ),
                "unique_count": int(data[column].nunique()),
                "minimum": minimum,
                "maximum": maximum,
                "example_values": " | ".join(map(str, examples)),
            }
        )

    return pd.DataFrame(records)


def main() -> None:
    """Generate and save the data dictionary."""
    data = load_processed_data()
    dictionary = create_data_dictionary(data)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    dictionary.to_csv(OUTPUT_PATH, index=False)

    print("Data dictionary created successfully.")
    print(f"Output: {OUTPUT_PATH}")
    print(f"Documented variables: {len(dictionary)}")


if __name__ == "__main__":
    main()