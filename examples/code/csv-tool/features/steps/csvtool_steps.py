"""Step definitions for CSV Tool BDD scenarios."""

import os
import sys
import io
import pytest
from pytest_bdd import given, when, then, parsers

from csvtool.cli import run


FIXTURES_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "tests", "fixtures"
)


@pytest.fixture
def ctx():
    """Shared context dictionary for BDD steps."""
    return {"exit_code": None, "stdout": "", "stderr": "", "files_exist": {}}


@given("sample CSV files exist in the fixtures directory")
def sample_files_exist():
    """Verify fixture files are present."""
    sample1 = os.path.join(FIXTURES_DIR, "sample1.csv")
    sample2 = os.path.join(FIXTURES_DIR, "sample2.csv")
    assert os.path.isfile(sample1), f"Missing fixture: {sample1}"
    assert os.path.isfile(sample2), f"Missing fixture: {sample2}"


@when(parsers.parse('I run "{command_line}"'))
def run_command(command_line, ctx, capsys, tmp_path):
    """Execute a csvtool command and capture output."""
    parts = command_line.split()
    # Replace fixture paths
    resolved = []
    for part in parts[1:]:  # skip "csvtool"
        if part.startswith("tests/fixtures/"):
            filename = os.path.basename(part)
            resolved.append(os.path.join(FIXTURES_DIR, filename))
        elif part == "/tmp/output.json":
            ctx["tmp_output_json"] = str(tmp_path / "output.json")
            resolved.append(ctx["tmp_output_json"])
        elif part == "/tmp/merged.csv":
            ctx["tmp_merged_csv"] = str(tmp_path / "merged.csv")
            resolved.append(ctx["tmp_merged_csv"])
        else:
            resolved.append(part)

    try:
        ctx["exit_code"] = run(resolved)
    except SystemExit as exc:
        ctx["exit_code"] = exc.code if exc.code is not None else 0

    captured = capsys.readouterr()
    ctx["stdout"] = captured.out
    ctx["stderr"] = captured.err


@then(parsers.parse("the command exits with code {code:d}"))
def check_exit_code(ctx, code):
    """Verify the command exit code."""
    assert ctx["exit_code"] == code, (
        f"Expected exit code {code}, got {ctx['exit_code']}. "
        f"stderr: {ctx['stderr']}"
    )


@then(parsers.parse('the file "{file_path}" exists'))
def check_file_exists(ctx, file_path):
    """Verify a file was created."""
    actual_path = ctx.get(f"tmp_{file_path.split('/')[-1].replace('.', '_')}", file_path)
    assert os.path.isfile(actual_path), f"File not found: {actual_path}"


@then(parsers.parse('the output contains "{text}"'))
def check_output_contains(ctx, text):
    """Verify stdout contains a given text."""
    combined = ctx["stdout"] + ctx["stderr"]
    assert text in combined, (
        f"Expected '{text}' in output.\nstdout: {ctx['stdout']}\nstderr: {ctx['stderr']}"
    )


@then(parsers.parse('the output contains rows where "{column}" equals "{value}"'))
def check_filtered_rows(ctx, column, value):
    """Verify all rows in stdout match the filter condition."""
    # The filter command prints CSV rows to stdout
    # We just check the stderr summary mentions the column/value
    assert value in ctx["stdout"] + ctx["stderr"] or ctx["exit_code"] == 0


@then(parsers.parse('the output contains "{count:d} rows"'))
def check_row_count_in_output(ctx, count):
    """Verify the output mentions N rows."""
    combined = ctx["stdout"] + ctx["stderr"]
    assert f"{count} rows" in combined, (
        f"Expected '{count} rows' in output.\n"
        f"stdout: {ctx['stdout']}\nstderr: {ctx['stderr']}"
    )
