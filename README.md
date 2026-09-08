# Statistics Superstars

A Principles of Statistics team project analysing factors associated with secondary-school student performance.

## Team Members

- Khant Min Zaw — 6845028 — Project Lead and Data Curator
- Hsu Mon San — 6845030 — Statistical Analyst
- Min Khant Kyaw — 6845034 — Visualization and Dashboard Specialist

## Dataset

**Student Performance Dataset**

Source: UCI Machine Learning Repository  
Dataset page: https://archive.ics.uci.edu/dataset/320/student+performance

The dataset contains student grades and demographic, social, and school-related variables collected from two Portuguese schools.

## Project Structure

- `data/raw/` — Original dataset files
- `data/processed/` — Cleaned datasets
- `notebooks/` — Exploration and analysis notebooks
- `src/` — Reusable Python functions
- `tests/` — Unit tests
- `dashboard/` — Streamlit application
### Run the Streamlit Dashboard

From the project root, run:

```bash
streamlit run dashboard/app.pys
- `reports/` — Reports, tables, logs, and figures
- `scripts/` — Data download and utility scripts

## Windows Setup

```bash
py -3.14 -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Dataset Source

This project uses the Portuguese-language portion of the
[UCI Student Performance Dataset](https://archive.ics.uci.edu/dataset/320/student%2Bperformance).

The dataset was created by Paulo Cortez and is licensed under CC BY 4.0.
Complete citation and provenance information is available in
[DATA_SOURCES.md](DATA_SOURCES.md).

## Reproducing the Data Pipeline

From the repository root with the virtual environment activated:

```bash
python -m scripts.download_data
python -m scripts.clean_data
python -m scripts.generate_data_dictionary
python -m pytest -q
```

The pipeline validates the documented schema and value ranges, removes only
exact duplicate rows, and preserves valid unusual observations. IQR-flagged
absence records and valid zero grades are not automatically removed or capped.