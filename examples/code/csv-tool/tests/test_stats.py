"""Unit tests for stats command."""

import pytest
from csvtool.commands.stats import calculate_stats, format_stats


class TestCalculateStats:
    """Tests for calculate_stats function."""

    def test_returns_correct_row_count(self, sample1_path):
        stats = calculate_stats(sample1_path)
        assert stats["rows"] == 5

    def test_returns_correct_column_count(self, sample1_path):
        stats = calculate_stats(sample1_path)
        assert stats["columns"] == 5

    def test_returns_column_names(self, sample1_path):
        stats = calculate_stats(sample1_path)
        assert "name" in stats["column_names"]
        assert "age" in stats["column_names"]
        assert "city" in stats["column_names"]

    def test_detects_numeric_columns(self, sample1_path):
        stats = calculate_stats(sample1_path)
        assert "age" in stats["numeric_stats"]
        assert "score" in stats["numeric_stats"]

    def test_numeric_avg_correct(self, sample1_path):
        stats = calculate_stats(sample1_path)
        # ages: 28, 34, 22, 45, 31 → avg = 32.0
        assert stats["numeric_stats"]["age"]["avg"] == 32.0

    def test_numeric_min_max(self, sample1_path):
        stats = calculate_stats(sample1_path)
        assert stats["numeric_stats"]["age"]["min"] == 22.0
        assert stats["numeric_stats"]["age"]["max"] == 45.0

    def test_file_not_found_raises(self):
        with pytest.raises(FileNotFoundError):
            calculate_stats("nonexistent.csv")

    def test_file_info_included(self, sample1_path):
        stats = calculate_stats(sample1_path)
        assert stats["file"] == sample1_path

    def test_missing_values_zero(self, sample1_path):
        stats = calculate_stats(sample1_path)
        assert stats["missing_values"] == 0


class TestFormatStats:
    """Tests for format_stats function."""

    def test_output_contains_rows(self, sample1_path):
        stats = calculate_stats(sample1_path)
        output = format_stats(stats)
        assert "Rows: 5" in output

    def test_output_contains_columns(self, sample1_path):
        stats = calculate_stats(sample1_path)
        output = format_stats(stats)
        assert "Columns: 5" in output

    def test_output_contains_numeric_columns(self, sample1_path):
        stats = calculate_stats(sample1_path)
        output = format_stats(stats)
        assert "age" in output
        assert "score" in output

    def test_output_contains_file_name(self, sample1_path):
        stats = calculate_stats(sample1_path)
        output = format_stats(stats)
        assert "File:" in output

    def test_output_contains_missing_values(self, sample1_path):
        stats = calculate_stats(sample1_path)
        output = format_stats(stats)
        assert "Missing values:" in output

    def test_output_is_multiline(self, sample1_path):
        stats = calculate_stats(sample1_path)
        output = format_stats(stats)
        assert output.count("\n") >= 3
