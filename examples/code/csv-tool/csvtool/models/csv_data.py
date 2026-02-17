"""Data model for CSV content."""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class CsvData:
    """Represents the content of a CSV file.

    Attributes:
        headers: List of column names.
        rows: List of rows, each row is a dict mapping header -> value.

    Examples:
        >>> data = CsvData(headers=["name", "age"], rows=[{"name": "Ana", "age": "30"}])
        >>> data.row_count
        1
        >>> data.column_count
        2
    """

    headers: List[str]
    rows: List[Dict[str, str]] = field(default_factory=list)

    @property
    def row_count(self) -> int:
        """Return the number of data rows."""
        return len(self.rows)

    @property
    def column_count(self) -> int:
        """Return the number of columns."""
        return len(self.headers)

    @property
    def numeric_columns(self) -> Dict[str, List[float]]:
        """Return columns whose values are all numeric.

        Returns:
            Dict mapping column name to list of float values.
        """
        result: Dict[str, List[float]] = {}
        for header in self.headers:
            values = []
            all_numeric = True
            for row in self.rows:
                val = row.get(header, "")
                try:
                    values.append(float(val))
                except ValueError:
                    all_numeric = False
                    break
            if all_numeric and values:
                result[header] = values
        return result
