"""Regression checks for the visualization notebook and dashboard."""

import ast
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = (
    PROJECT_ROOT / "notebooks" / "03_exploratory_visualizations.ipynb"
)
DASHBOARD_PATH = PROJECT_ROOT / "dashboard" / "app.py"
README_PATH = PROJECT_ROOT / "README.md"


def _notebook_code() -> str:
    notebook = json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))
    return "\n".join(
        "".join(cell.get("source", []))
        for cell in notebook["cells"]
        if cell.get("cell_type") == "code"
    )


def test_visualization_notebook_is_portable() -> None:
    code = _notebook_code()

    assert "/Users/" not in code
    assert "C:\\\\Users\\\\" not in code
    assert "Path.cwd()" in code


def test_visualization_notebook_has_no_saved_errors() -> None:
    notebook = json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))
    errors = [
        output
        for cell in notebook["cells"]
        for output in cell.get("outputs", [])
        if output.get("output_type") == "error"
    ]

    assert not errors


def test_dashboard_source_is_valid_python() -> None:
    source = DASHBOARD_PATH.read_text(encoding="utf-8")
    ast.parse(source)

    assert "Path(__file__).resolve().parents[1]" in source
    assert "filtered_df.empty" in source


def test_dashboard_outputs_are_present() -> None:
    expected_files = {
        "distribution_plots.png",
        "boxplots.png",
        "correlation_heatmap.png",
        "qq_plots.png",
        "scatter_matrix.html",
        "3d_scatter.html",
        "pair_plot.html",
    }
    actual_files = {
        path.name for path in (PROJECT_ROOT / "reports" / "figures").iterdir()
    }

    assert expected_files <= actual_files


def test_readme_has_working_dashboard_command() -> None:
    readme = README_PATH.read_text(encoding="utf-8")

    assert "python -m streamlit run dashboard\\app.py" in readme
    assert "dashboard/app.pys" not in readme
    assert readme.count("```") % 2 == 0
