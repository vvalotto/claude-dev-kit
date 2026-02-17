"""File and path validators for CSV Tool."""

import os


def validate_file_exists(path: str) -> None:
    """Verify that a file exists and is readable.

    Args:
        path: Path to the file to validate.

    Raises:
        FileNotFoundError: If the file does not exist.

    Examples:
        >>> validate_file_exists("nonexistent.csv")
        Traceback (most recent call last):
            ...
        FileNotFoundError: File not found: nonexistent.csv
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File not found: {path}")


def validate_csv_extension(path: str) -> None:
    """Verify that a file has a .csv extension.

    Args:
        path: Path to the file to validate.

    Raises:
        ValueError: If the file does not have a .csv extension.

    Examples:
        >>> validate_csv_extension("data.txt")
        Traceback (most recent call last):
            ...
        ValueError: File must have .csv extension: data.txt
    """
    if not path.lower().endswith(".csv"):
        raise ValueError(f"File must have .csv extension: {path}")


def validate_output_path(path: str) -> None:
    """Verify that the output path's parent directory exists and is writable.

    Args:
        path: Output file path to validate.

    Raises:
        ValueError: If the parent directory does not exist or is not writable.

    Examples:
        >>> validate_output_path("/nonexistent/dir/output.json")
        Traceback (most recent call last):
            ...
        ValueError: Output directory does not exist: /nonexistent/dir
    """
    parent = os.path.dirname(os.path.abspath(path))
    if not os.path.isdir(parent):
        raise ValueError(f"Output directory does not exist: {parent}")
    if not os.access(parent, os.W_OK):
        raise ValueError(f"Output directory is not writable: {parent}")
