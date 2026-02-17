"""Pytest configuration and shared fixtures."""

import os
import pytest

# Import BDD step definitions
pytest_plugins = ["features.steps.csvtool_steps"]

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
SAMPLE1 = os.path.join(FIXTURES_DIR, "sample1.csv")
SAMPLE2 = os.path.join(FIXTURES_DIR, "sample2.csv")


@pytest.fixture
def sample1_path():
    """Path to sample1.csv fixture."""
    return SAMPLE1


@pytest.fixture
def sample2_path():
    """Path to sample2.csv fixture."""
    return SAMPLE2


@pytest.fixture
def tmp_json(tmp_path):
    """Temporary JSON output file path."""
    return str(tmp_path / "output.json")


@pytest.fixture
def tmp_csv(tmp_path):
    """Temporary CSV output file path."""
    return str(tmp_path / "output.csv")


@pytest.fixture
def small_csv(tmp_path):
    """Create a small CSV for targeted unit tests."""
    path = str(tmp_path / "small.csv")
    content = "name,age,city\nAlice,30,Paris\nBob,25,Paris\nCarol,40,London\n"
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path
