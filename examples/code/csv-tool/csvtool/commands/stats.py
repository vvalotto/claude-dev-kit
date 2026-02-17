"""Stats command: display statistics for a CSV file."""

import csv
import statistics
from typing import Any, Dict

from csvtool.models.csv_data import CsvData
from csvtool.utils.validators import validate_file_exists, validate_csv_extension


def _load_csv_data(input_path: str) -> CsvData:
    """Load a CSV file into a CsvData object.

    Args:
        input_path: Path to the CSV file.

    Returns:
        CsvData instance with headers and rows.
    """
    with open(input_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        headers = list(reader.fieldnames or [])
        rows = list(reader)
    return CsvData(headers=headers, rows=rows)


def calculate_stats(input_path: str) -> Dict[str, Any]:
    """Calculate statistics for a CSV file.

    Computes row/column counts, numeric column averages and ranges,
    and total missing (empty) values.

    Args:
        input_path: Path to the CSV file.

    Returns:
        Dictionary with keys: file, rows, columns, column_names,
        numeric_stats, missing_values.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is not a valid CSV.

    Examples:
        >>> stats = calculate_stats("data.csv")
        >>> stats["rows"]
        5
    """
    validate_file_exists(input_path)
    validate_csv_extension(input_path)

    data = _load_csv_data(input_path)
    numeric = data.numeric_columns

    numeric_stats: Dict[str, Dict[str, float]] = {}
    for col, values in numeric.items():
        numeric_stats[col] = {
            "avg": round(statistics.mean(values), 2),
            "min": min(values),
            "max": max(values),
        }

    missing = sum(
        1 for row in data.rows for val in row.values() if val == "" or val is None
    )

    return {
        "file": input_path,
        "rows": data.row_count,
        "columns": data.column_count,
        "column_names": data.headers,
        "numeric_stats": numeric_stats,
        "missing_values": missing,
    }


def format_stats(stats: Dict[str, Any]) -> str:
    """Format a stats dictionary as a human-readable string.

    Args:
        stats: Dictionary returned by calculate_stats().

    Returns:
        Formatted multi-line string.

    Examples:
        >>> stats = {"file": "data.csv", "rows": 5, "columns": 3, ...}
        >>> print(format_stats(stats))
        File: data.csv
        Rows: 5
        ...
    """
    lines = [
        f"File: {stats['file']}",
        f"Rows: {stats['rows']}",
        f"Columns: {stats['columns']} ({', '.join(stats['column_names'])})",
    ]

    if stats["numeric_stats"]:
        lines.append("Numeric columns:")
        for col, values in stats["numeric_stats"].items():
            lines.append(
                f"  {col}: avg={values['avg']}, min={values['min']}, max={values['max']}"
            )

    lines.append(f"Missing values: {stats['missing_values']}")
    return "\n".join(lines)
