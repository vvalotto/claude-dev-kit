# language: en
Feature: CSV Tool CLI Utility
  As a data analyst
  I want a CLI utility to manipulate CSV files
  So that I can automate data processing tasks

  Background:
    Given sample CSV files exist in the fixtures directory

  Scenario: Convert CSV to JSON successfully
    When I run "csvtool convert tests/fixtures/sample1.csv /tmp/output.json"
    Then the command exits with code 0
    And the file "/tmp/output.json" exists
    And the output contains "Converted"

  Scenario: Convert CSV to JSON - file not found
    When I run "csvtool convert nonexistent.csv output.json"
    Then the command exits with code 1
    And the output contains "Error"

  Scenario: Filter CSV by column value
    When I run "csvtool filter tests/fixtures/sample1.csv city Madrid"
    Then the command exits with code 0
    And the output contains rows where "city" equals "Madrid"

  Scenario: Filter CSV - column not found
    When I run "csvtool filter tests/fixtures/sample1.csv nonexistent value"
    Then the command exits with code 1
    And the output contains "Error"

  Scenario: Merge two CSV files
    When I run "csvtool merge tests/fixtures/sample1.csv tests/fixtures/sample2.csv /tmp/merged.csv"
    Then the command exits with code 0
    And the file "/tmp/merged.csv" exists
    And the output contains "Merged"

  Scenario: Show CSV statistics
    When I run "csvtool stats tests/fixtures/sample1.csv"
    Then the command exits with code 0
    And the output contains "Rows"
    And the output contains "Columns"

  Scenario: Show help message
    When I run "csvtool --help"
    Then the command exits with code 0
    And the output contains "convert"
    And the output contains "filter"
    And the output contains "merge"
    And the output contains "stats"

  Scenario: No command provided
    When I run "csvtool"
    Then the command exits with code 1

  Scenario: Stats on file with numeric columns
    When I run "csvtool stats tests/fixtures/sample1.csv"
    Then the command exits with code 0
    And the output contains "age"

  Scenario: Filter returns empty result
    When I run "csvtool filter tests/fixtures/sample1.csv city ZZZ_nonexistent"
    Then the command exits with code 0
    And the output contains "0 rows"
