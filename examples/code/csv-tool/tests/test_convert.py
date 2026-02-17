"""Unit tests for convert command."""

import json
import os
import pytest
from csvtool.commands.convert import convert_csv_to_json


class TestConvertCsvToJson:
    """Tests for convert_csv_to_json function."""

    def test_converts_successfully(self, sample1_path, tmp_json):
        count = convert_csv_to_json(sample1_path, tmp_json)
        assert count == 5
        assert os.path.isfile(tmp_json)

    def test_output_is_valid_json(self, sample1_path, tmp_json):
        convert_csv_to_json(sample1_path, tmp_json)
        with open(tmp_json, encoding="utf-8") as f:
            data = json.load(f)
        assert isinstance(data, list)
        assert len(data) == 5

    def test_json_has_correct_keys(self, sample1_path, tmp_json):
        convert_csv_to_json(sample1_path, tmp_json)
        with open(tmp_json, encoding="utf-8") as f:
            data = json.load(f)
        assert set(data[0].keys()) == {"name", "age", "city", "score", "active"}

    def test_json_preserves_values(self, sample1_path, tmp_json):
        convert_csv_to_json(sample1_path, tmp_json)
        with open(tmp_json, encoding="utf-8") as f:
            data = json.load(f)
        first_row = data[0]
        assert first_row["name"] == "Juan Pérez"
        assert first_row["city"] == "Madrid"

    def test_file_not_found_raises(self, tmp_json):
        with pytest.raises(FileNotFoundError):
            convert_csv_to_json("nonexistent.csv", tmp_json)

    def test_non_csv_extension_raises(self, tmp_json):
        with pytest.raises(ValueError):
            convert_csv_to_json("data.txt", tmp_json)

    def test_second_file_converts_correctly(self, sample2_path, tmp_json):
        count = convert_csv_to_json(sample2_path, tmp_json)
        assert count == 3
