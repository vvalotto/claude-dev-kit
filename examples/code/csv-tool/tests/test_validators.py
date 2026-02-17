"""Unit tests for validators module."""

import os
import pytest
from csvtool.utils.validators import (
    validate_file_exists,
    validate_csv_extension,
    validate_output_path,
)


class TestValidateFileExists:
    """Tests for validate_file_exists."""

    def test_existing_file_passes(self, sample1_path):
        validate_file_exists(sample1_path)  # Should not raise

    def test_nonexistent_file_raises(self):
        with pytest.raises(FileNotFoundError, match="File not found"):
            validate_file_exists("nonexistent_file_xyz.csv")

    def test_directory_raises(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            validate_file_exists(str(tmp_path))


class TestValidateCsvExtension:
    """Tests for validate_csv_extension."""

    def test_csv_extension_passes(self):
        validate_csv_extension("data.csv")

    def test_csv_uppercase_passes(self):
        validate_csv_extension("DATA.CSV")

    def test_json_extension_raises(self):
        with pytest.raises(ValueError, match=".csv extension"):
            validate_csv_extension("data.json")

    def test_no_extension_raises(self):
        with pytest.raises(ValueError, match=".csv extension"):
            validate_csv_extension("data")

    def test_txt_extension_raises(self):
        with pytest.raises(ValueError, match=".csv extension"):
            validate_csv_extension("data.txt")


class TestValidateOutputPath:
    """Tests for validate_output_path."""

    def test_valid_output_path(self, tmp_path):
        output = str(tmp_path / "output.json")
        validate_output_path(output)  # Should not raise

    def test_nonexistent_directory_raises(self):
        with pytest.raises(ValueError, match="Output directory does not exist"):
            validate_output_path("/nonexistent_xyz_dir/output.json")
