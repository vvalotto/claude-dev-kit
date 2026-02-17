"""Unit tests for filter command."""

import pytest
from csvtool.commands.filter_cmd import filter_csv


class TestFilterCsv:
    """Tests for filter_csv function."""

    def test_filter_by_city_madrid(self, sample1_path):
        result = filter_csv(sample1_path, "city", "Madrid")
        assert result.row_count == 3

    def test_filter_by_city_barcelona(self, sample1_path):
        result = filter_csv(sample1_path, "city", "Barcelona")
        assert result.row_count == 1
        assert result.rows[0]["name"] == "María García"

    def test_filter_returns_csv_data_with_headers(self, sample1_path):
        result = filter_csv(sample1_path, "city", "Madrid")
        assert "name" in result.headers
        assert "city" in result.headers

    def test_filter_no_match_returns_empty(self, sample1_path):
        result = filter_csv(sample1_path, "city", "ZZZ_nonexistent")
        assert result.row_count == 0
        assert result.headers  # Headers still present

    def test_filter_invalid_column_raises(self, sample1_path):
        with pytest.raises(ValueError, match="Column 'nonexistent' not found"):
            filter_csv(sample1_path, "nonexistent", "value")

    def test_filter_file_not_found_raises(self):
        with pytest.raises(FileNotFoundError):
            filter_csv("nonexistent.csv", "col", "val")

    def test_filter_active_true(self, sample1_path):
        result = filter_csv(sample1_path, "active", "true")
        assert result.row_count == 3

    def test_filter_active_false(self, sample1_path):
        result = filter_csv(sample1_path, "active", "false")
        assert result.row_count == 2

    def test_filter_preserves_all_columns(self, sample1_path):
        result = filter_csv(sample1_path, "city", "Madrid")
        for row in result.rows:
            assert set(row.keys()) == {"name", "age", "city", "score", "active"}

    def test_filter_small_csv(self, small_csv):
        result = filter_csv(small_csv, "city", "Paris")
        assert result.row_count == 2
        names = [r["name"] for r in result.rows]
        assert "Alice" in names
        assert "Bob" in names
