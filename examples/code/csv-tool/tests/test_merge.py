"""Unit tests for merge command."""

import csv
import pytest
from csvtool.commands.merge import merge_csv_files


class TestMergeCsvFiles:
    """Tests for merge_csv_files function."""

    def test_merges_two_files(self, sample1_path, sample2_path, tmp_csv):
        count = merge_csv_files([sample1_path, sample2_path], tmp_csv)
        assert count == 8  # 5 + 3

    def test_output_file_created(self, sample1_path, sample2_path, tmp_csv):
        import os
        merge_csv_files([sample1_path, sample2_path], tmp_csv)
        assert os.path.isfile(tmp_csv)

    def test_merged_headers_correct(self, sample1_path, sample2_path, tmp_csv):
        merge_csv_files([sample1_path, sample2_path], tmp_csv)
        with open(tmp_csv, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            headers = list(reader.fieldnames or [])
        assert headers == ["name", "age", "city", "score", "active"]

    def test_merged_row_count(self, sample1_path, sample2_path, tmp_csv):
        merge_csv_files([sample1_path, sample2_path], tmp_csv)
        with open(tmp_csv, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        assert len(rows) == 8

    def test_less_than_two_files_raises(self, sample1_path, tmp_csv):
        with pytest.raises(ValueError, match="At least 2 files"):
            merge_csv_files([sample1_path], tmp_csv)

    def test_file_not_found_raises(self, sample1_path, tmp_csv):
        with pytest.raises(FileNotFoundError):
            merge_csv_files([sample1_path, "nonexistent.csv"], tmp_csv)

    def test_incompatible_headers_raises(self, sample1_path, tmp_csv, tmp_path):
        different = str(tmp_path / "different.csv")
        with open(different, "w", encoding="utf-8") as f:
            f.write("col_a,col_b\nval1,val2\n")
        with pytest.raises(ValueError, match="different headers"):
            merge_csv_files([sample1_path, different], tmp_csv)

    def test_merged_preserves_order(self, sample1_path, sample2_path, tmp_csv):
        merge_csv_files([sample1_path, sample2_path], tmp_csv)
        with open(tmp_csv, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        # First 5 from sample1, next 3 from sample2
        assert rows[0]["name"] == "Juan Pérez"
        assert rows[5]["name"] == "Laura Sánchez"
