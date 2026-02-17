"""Merge command: combine multiple CSV files."""

import csv
from typing import List

from csvtool.utils.validators import (
    validate_file_exists,
    validate_csv_extension,
    validate_output_path,
)


def merge_csv_files(file_paths: List[str], output_path: str) -> int:
    """Merge multiple CSV files into a single output file.

    All input files must share the same headers. The output file will
    contain all rows from all inputs in order.

    Args:
        file_paths: List of paths to input CSV files (minimum 2).
        output_path: Path for the merged output CSV file.

    Returns:
        Total number of rows written.

    Raises:
        FileNotFoundError: If any input file does not exist.
        ValueError: If files have incompatible headers or fewer than 2 files provided.

    Examples:
        >>> merge_csv_files(["a.csv", "b.csv"], "merged.csv")
        8
    """
    if len(file_paths) < 2:
        raise ValueError("At least 2 files are required for merge")

    for path in file_paths:
        validate_file_exists(path)
        validate_csv_extension(path)

    validate_output_path(output_path)

    all_rows: List[dict] = []
    reference_headers: List[str] = []

    for i, path in enumerate(file_paths):
        with open(path, newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            headers = list(reader.fieldnames or [])
            rows = list(reader)

        if i == 0:
            reference_headers = headers
        elif headers != reference_headers:
            raise ValueError(
                f"File '{path}' has different headers. "
                f"Expected: {reference_headers}, Got: {headers}"
            )

        all_rows.extend(rows)

    with open(output_path, "w", newline="", encoding="utf-8") as out_file:
        writer = csv.DictWriter(out_file, fieldnames=reference_headers)
        writer.writeheader()
        writer.writerows(all_rows)

    return len(all_rows)
