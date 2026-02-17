"""Convert command: CSV to JSON."""

import csv
import json

from csvtool.utils.validators import (
    validate_file_exists,
    validate_csv_extension,
    validate_output_path,
)


def convert_csv_to_json(input_path: str, output_path: str) -> int:
    """Convert a CSV file to JSON format.

    Reads all rows from the CSV file and writes them as a JSON array,
    where each element is a dict mapping column name to value.

    Args:
        input_path: Path to the input CSV file.
        output_path: Path for the output JSON file.

    Returns:
        Number of rows converted.

    Raises:
        FileNotFoundError: If the input file does not exist.
        ValueError: If the input file is not a valid CSV.

    Examples:
        >>> convert_csv_to_json("data.csv", "data.json")
        5
    """
    validate_csv_extension(input_path)
    validate_file_exists(input_path)
    validate_output_path(output_path)

    with open(input_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)

    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(rows, json_file, indent=2, ensure_ascii=False)

    return len(rows)
