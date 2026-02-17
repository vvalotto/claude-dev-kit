"""Unit tests for CsvData model."""

import pytest
from csvtool.models.csv_data import CsvData


class TestCsvDataBasic:
    """Tests for CsvData basic properties."""

    def test_row_count_empty(self):
        data = CsvData(headers=["a", "b"])
        assert data.row_count == 0

    def test_row_count_with_rows(self):
        data = CsvData(headers=["a"], rows=[{"a": "1"}, {"a": "2"}, {"a": "3"}])
        assert data.row_count == 3

    def test_column_count(self):
        data = CsvData(headers=["name", "age", "city"])
        assert data.column_count == 3

    def test_column_count_empty(self):
        data = CsvData(headers=[])
        assert data.column_count == 0

    def test_headers_preserved(self):
        headers = ["x", "y", "z"]
        data = CsvData(headers=headers)
        assert data.headers == headers


class TestCsvDataNumericColumns:
    """Tests for numeric_columns property."""

    def test_all_numeric(self):
        data = CsvData(
            headers=["score"],
            rows=[{"score": "10.5"}, {"score": "20"}, {"score": "30.0"}],
        )
        assert "score" in data.numeric_columns
        assert data.numeric_columns["score"] == [10.5, 20.0, 30.0]

    def test_mixed_column_excluded(self):
        data = CsvData(
            headers=["val"],
            rows=[{"val": "10"}, {"val": "text"}, {"val": "30"}],
        )
        assert "val" not in data.numeric_columns

    def test_text_column_excluded(self):
        data = CsvData(
            headers=["name"],
            rows=[{"name": "Alice"}, {"name": "Bob"}],
        )
        assert "name" not in data.numeric_columns

    def test_multiple_numeric_columns(self):
        data = CsvData(
            headers=["age", "score"],
            rows=[
                {"age": "28", "score": "85.5"},
                {"age": "34", "score": "92.0"},
            ],
        )
        assert "age" in data.numeric_columns
        assert "score" in data.numeric_columns

    def test_empty_rows_returns_empty(self):
        data = CsvData(headers=["age"], rows=[])
        assert data.numeric_columns == {}
