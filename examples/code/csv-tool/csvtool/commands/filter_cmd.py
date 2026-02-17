"""Filter command: filter CSV rows by column value."""

import csv
from typing import List

from csvtool.models.csv_data import CsvData
from csvtool.utils.validators import validate_file_exists, validate_csv_extension


def filter_csv(input_path: str, column: str, value: str) -> CsvData:
    """Filter rows of a CSV file where column equals value.

    Args:
        input_path: Path to the input CSV file.
        column: Column name to filter on.
        value: Value to match (case-sensitive).

    Returns:
        CsvData with only the matching rows.

    Raises:
        FileNotFoundError: If the input file does not exist.
        ValueError: If the column does not exist in the CSV headers.

    Examples:
        >>> result = filter_csv("data.csv", "city", "Madrid")
        >>> result.row_count
        3
    """
    validate_file_exists(input_path)
    validate_csv_extension(input_path)

    with open(input_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        headers: List[str] = list(reader.fieldnames or [])
        rows = list(reader)

    if column not in headers:
        raise ValueError(
            f"Column '{column}' not found. Available columns: {', '.join(headers)}"
        )

    filtered = [row for row in rows if row.get(column) == value]
    return CsvData(headers=headers, rows=filtered)
