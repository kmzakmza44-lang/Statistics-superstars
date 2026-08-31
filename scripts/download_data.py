from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

import pandas as pd
import requests


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"

DATASET_URLS = [
    "https://archive.ics.uci.edu/static/public/320/student+performance.zip",
    "https://archive.ics.uci.edu/ml/machine-learning-databases/00320/student.zip",
]


def download_dataset() -> bytes:
    """Download the dataset, using a fallback URL if necessary."""
    for url in DATASET_URLS:
        try:
            print(f"Trying: {url}")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            print("Download successful.")
            return response.content
        except requests.RequestException as error:
            print(f"Download failed: {error}")

    raise RuntimeError("Could not download the dataset from UCI.")


def safe_extract(zip_file: ZipFile, destination: Path) -> None:
    """Extract files while preventing unsafe paths."""
    destination = destination.resolve()

    for member in zip_file.infolist():
        output_path = (destination / member.filename).resolve()

        if destination not in output_path.parents and output_path != destination:
            raise ValueError(f"Unsafe ZIP path: {member.filename}")

    zip_file.extractall(destination)


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    zip_content = download_dataset()
    zip_path = RAW_DIR / "student_performance.zip"
    zip_path.write_bytes(zip_content)

    with ZipFile(BytesIO(zip_content)) as zip_file:
        safe_extract(zip_file, RAW_DIR)

    # Use the Portuguese subject dataset because it has more observations.
    source_file = RAW_DIR / "student-por.csv"
    output_file = RAW_DIR / "student_performance.csv"

    if not source_file.exists():
        raise FileNotFoundError(f"Expected file was not found: {source_file}")

    data = pd.read_csv(source_file, sep=";")
    data.to_csv(output_file, index=False)

    print(f"Primary dataset: {source_file.name}")
    print(f"Dataset shape: {data.shape}")
    print(f"Standardized file: {output_file}")
    print("Dataset preparation completed.")


if __name__ == "__main__":
    main()