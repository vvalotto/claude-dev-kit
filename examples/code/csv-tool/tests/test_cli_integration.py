"""Integration tests for CLI end-to-end behavior."""

import csv
import json
import os
import pytest
from csvtool.cli import run


class TestCliConvert:
    """Integration tests for the convert subcommand."""

    def test_convert_exit_code_zero(self, sample1_path, tmp_json):
        code = run(["convert", sample1_path, tmp_json])
        assert code == 0

    def test_convert_creates_json_file(self, sample1_path, tmp_json):
        run(["convert", sample1_path, tmp_json])
        assert os.path.isfile(tmp_json)

    def test_convert_json_content_correct(self, sample1_path, tmp_json):
        run(["convert", sample1_path, tmp_json])
        with open(tmp_json, encoding="utf-8") as f:
            data = json.load(f)
        assert len(data) == 5
        assert data[0]["name"] == "Juan Pérez"

    def test_convert_nonexistent_file_returns_1(self, tmp_json):
        code = run(["convert", "nonexistent.csv", tmp_json])
        assert code == 1

    def test_convert_second_sample(self, sample2_path, tmp_json):
        code = run(["convert", sample2_path, tmp_json])
        assert code == 0
        with open(tmp_json, encoding="utf-8") as f:
            data = json.load(f)
        assert len(data) == 3


class TestCliFilter:
    """Integration tests for the filter subcommand."""

    def test_filter_exit_code_zero(self, sample1_path, capsys):
        code = run(["filter", sample1_path, "city", "Madrid"])
        assert code == 0

    def test_filter_invalid_column_returns_1(self, sample1_path):
        code = run(["filter", sample1_path, "nonexistent_col", "value"])
        assert code == 1

    def test_filter_nonexistent_file_returns_1(self):
        code = run(["filter", "nonexistent.csv", "city", "Madrid"])
        assert code == 1

    def test_filter_empty_result_exit_zero(self, sample1_path):
        code = run(["filter", sample1_path, "city", "ZZZ_nonexistent"])
        assert code == 0


class TestCliMerge:
    """Integration tests for the merge subcommand."""

    def test_merge_exit_code_zero(self, sample1_path, sample2_path, tmp_csv):
        code = run(["merge", sample1_path, sample2_path, tmp_csv])
        assert code == 0

    def test_merge_creates_output_file(self, sample1_path, sample2_path, tmp_csv):
        run(["merge", sample1_path, sample2_path, tmp_csv])
        assert os.path.isfile(tmp_csv)

    def test_merge_correct_row_count(self, sample1_path, sample2_path, tmp_csv):
        run(["merge", sample1_path, sample2_path, tmp_csv])
        with open(tmp_csv, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        assert len(rows) == 8

    def test_merge_nonexistent_file_returns_1(self, sample1_path, tmp_csv):
        code = run(["merge", sample1_path, "nonexistent.csv", tmp_csv])
        assert code == 1


class TestCliStats:
    """Integration tests for the stats subcommand."""

    def test_stats_exit_code_zero(self, sample1_path):
        code = run(["stats", sample1_path])
        assert code == 0

    def test_stats_nonexistent_file_returns_1(self):
        code = run(["stats", "nonexistent.csv"])
        assert code == 1

    def test_stats_output_has_rows(self, sample1_path, capsys):
        run(["stats", sample1_path])
        captured = capsys.readouterr()
        assert "Rows: 5" in captured.out

    def test_stats_output_has_columns(self, sample1_path, capsys):
        run(["stats", sample1_path])
        captured = capsys.readouterr()
        assert "Columns: 5" in captured.out

    def test_stats_output_has_age(self, sample1_path, capsys):
        run(["stats", sample1_path])
        captured = capsys.readouterr()
        assert "age" in captured.out


class TestCliGeneral:
    """Integration tests for general CLI behavior."""

    def test_no_command_returns_1(self):
        code = run([])
        assert code == 1

    def test_help_exits_cleanly(self):
        with pytest.raises(SystemExit) as exc_info:
            run(["--help"])
        assert exc_info.value.code == 0
