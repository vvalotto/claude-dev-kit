"""CLI entry point for CSV Tool."""

import argparse
import sys
from typing import List, Optional

from csvtool.commands.convert import convert_csv_to_json
from csvtool.commands.filter_cmd import filter_csv
from csvtool.commands.merge import merge_csv_files
from csvtool.commands.stats import calculate_stats, format_stats


def create_parser() -> argparse.ArgumentParser:
    """Create and return the argument parser for csvtool.

    Returns:
        Configured ArgumentParser with all subcommands.
    """
    parser = argparse.ArgumentParser(
        prog="csvtool",
        description="CSV manipulation utility — convert, filter, merge and analyze CSV files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  csvtool convert data.csv data.json\n"
            "  csvtool filter data.csv city Madrid\n"
            "  csvtool merge file1.csv file2.csv merged.csv\n"
            "  csvtool stats data.csv\n"
        ),
    )

    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")

    # convert
    convert_parser = subparsers.add_parser(
        "convert", help="Convert a CSV file to JSON format"
    )
    convert_parser.add_argument("input", help="Input CSV file path")
    convert_parser.add_argument("output", help="Output JSON file path")

    # filter
    filter_parser = subparsers.add_parser(
        "filter", help="Filter CSV rows where COLUMN equals VALUE"
    )
    filter_parser.add_argument("input", help="Input CSV file path")
    filter_parser.add_argument("column", help="Column name to filter on")
    filter_parser.add_argument("value", help="Value to match (case-sensitive)")

    # merge
    merge_parser = subparsers.add_parser(
        "merge", help="Merge two or more CSV files into one"
    )
    merge_parser.add_argument("files", nargs="+", help="Input CSV files (minimum 2)")
    merge_parser.add_argument("output", help="Output merged CSV file path")

    # stats
    stats_parser = subparsers.add_parser(
        "stats", help="Show statistics for a CSV file"
    )
    stats_parser.add_argument("input", help="Input CSV file path")

    return parser


def run(args: Optional[List[str]] = None) -> int:
    """Parse arguments and execute the requested command.

    Args:
        args: Argument list (uses sys.argv if None).

    Returns:
        Exit code: 0 on success, 1 on error.
    """
    parser = create_parser()
    parsed = parser.parse_args(args)

    if parsed.command is None:
        parser.print_help()
        return 1

    try:
        if parsed.command == "convert":
            count = convert_csv_to_json(parsed.input, parsed.output)
            print(f"Converted {count} rows from {parsed.input} to {parsed.output}")

        elif parsed.command == "filter":
            result = filter_csv(parsed.input, parsed.column, parsed.value)
            for row in result.rows:
                print(",".join(row.values()))
            print(
                f"Filtered {result.row_count} rows where "
                f"{parsed.column}={parsed.value}",
                file=sys.stderr,
            )

        elif parsed.command == "merge":
            # last positional arg is output, rest are input files
            *input_files, output_file = parsed.files + [parsed.output]
            count = merge_csv_files(input_files, output_file)
            print(f"Merged {count} rows from {len(input_files)} files into {output_file}")

        elif parsed.command == "stats":
            stats = calculate_stats(parsed.input)
            print(format_stats(stats))

    except (FileNotFoundError, ValueError, PermissionError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    return 0
