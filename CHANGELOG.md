# Changelog

All notable changes to Claude Dev Kit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-02-17

### Added

#### Installation System
- Cross-platform installer (`install/installer.py`) supporting Linux, macOS, and Windows
- YAML-based installation configuration (`install/config.yaml`) with profile selection
- Post-installation validator (`install/validate-setup.py`) with detailed diagnostics
- Interactive mode (guided profile selection) and non-interactive mode (`--profile`, `--yes`, `--dry-run`, `--force`)
- Shell wrapper for Unix/macOS (`install/install.sh`)

#### `implement-us` Skill
- Main skill `implement-us` that guides step-by-step implementation of user stories in Python projects
- Modular architecture with an orchestrator (`skill.md`) and 10 specialized phase agents (Phase 0–9):
  - Phase 0: Context Validation
  - Phase 1: BDD Scenario Generation
  - Phase 2: Implementation Planning
  - Phase 3: Implementation
  - Phase 4: Unit Tests
  - Phase 5: Integration Tests
  - Phase 6: BDD Validation
  - Phase 7: Quality Gates (Pylint, Cyclomatic Complexity, Maintainability Index, Coverage)
  - Phase 8: Documentation
  - Phase 9: Final Report
- 5 technology stack profiles, each with architecture-specific conventions and quality gates:
  - `pyqt-mvc` — PyQt6 desktop applications with MVC architecture
  - `fastapi-rest` — FastAPI REST APIs with layered architecture and async/await
  - `flask-rest` — Flask REST APIs with layered architecture (sync)
  - `flask-webapp` — Flask fullstack webapps with Jinja2 SSR and BFF pattern
  - `generic-python` — Generic Python projects (libraries, CLI tools, scripts, data science)
- Parametrized variable system (`{ARCHITECTURE_PATTERN}`, `{COMPONENT_TYPE}`, `{COMPONENT_PATH}`, etc.) enabling a single skill definition to adapt to any stack
- Base configuration file (`skills/implement-us/config.json`) with per-profile override system

#### Template System
- BDD scenario template (`templates/bdd/bdd-scenario.feature`) in Gherkin format
- Implementation plan template (`templates/planning/implementation-plan.md`) with task breakdown and time estimates
- Final report template (`templates/reporting/implementation-report.md`) with quality metrics
- Unit test template (`templates/testing/test-unit.py`) with fixtures and parametrized tests
- Snippet library: 35 code snippets organized by type (model, view, controller, service, repository, test, config) × 5 profiles

#### Time Tracking System
- Core tracking module (`tracking/time_tracker.py`) with automatic time measurement per phase and task
- Reports module (`tracking/reports.py`) for historical analysis
- 5 tracking skills for Claude Code:
  - `/track-pause [reason]` — Pause tracking with optional reason
  - `/track-resume` — Resume tracking after a pause
  - `/track-status` — Show current tracking status
  - `/track-report [us_id]` — Generate detailed report for a user story
  - `/track-history [--last N]` — View historical tracking data
- JSON persistence at `.claude/tracking/{us_id}-tracking.json`
- Variance tracking: estimated vs. actual time per phase and task

#### Documentation
- User documentation (8 documents, ~2,800 lines):
  - Quick start guide — from clone to first `/implement-us` in under 15 minutes
  - Detailed installation guide for all platforms
  - Customization guide — profiles, variables, creating custom profiles
  - Configuration reference — all available options with examples
  - `implement-us` skill reference with all phases documented
  - Time tracking user guide
  - Tracking usage examples
  - Main documentation index with navigation
- Developer documentation (5 documents, ~1,900 lines):
  - Guide for creating custom skills
  - Template system architecture
  - Tracking system architecture
  - Session memory system documentation
  - Document template for contributors
- GitHub Actions workflow for automatic Wiki synchronization (`.github/workflows/sync-wiki.yml`) — triggers on push to `main`, flattens directory structure to PascalCase page names

#### Code Examples by Stack
Five complete, working projects generated using the framework itself, each with full BDD scenarios, unit tests, integration tests, and quality gate validation:

- **PyQt6 MVC — Calculator** (`examples/code/pyqt-calculator/`): Desktop calculator with MVC architecture. 14 tests, 86% coverage. Full tutorial at `docs/examples/pyqt-project.md`.
- **FastAPI REST — TODO API** (`examples/code/fastapi-todo-api/`): Async REST API with layered architecture and dependency injection. 29 tests, 98% coverage. Full tutorial at `docs/examples/fastapi-project.md`.
- **Flask REST — Contacts API** (`examples/code/flask-contacts-api/`): Synchronous REST API with Repository + Mapper patterns. 38 tests, 94% coverage. Full tutorial at `docs/examples/flask-rest-api-project.md`.
- **Flask WebApp — Blog** (`examples/code/flask-blog-app/`): Fullstack web application with BFF pattern and Server-Side Rendering. 43 tests, 99% coverage. Full tutorial at `docs/examples/flask-webapp-project.md`.
- **Generic Python CLI — CSV Tool** (`examples/code/csv-tool/`): Data processing CLI tool with pandas. 90 tests, 98% coverage. Full tutorial at `docs/examples/generic-python.md`.

#### Framework Test Suite
- Comprehensive test suite for the framework itself: 107 tests, 99% overall coverage
- `tests/test_installer.py` (37 tests) — installer logic, profile merging, validation, CLI options
- `tests/test_tracking.py` (38 tests) — time tracking, pauses, variance calculation, JSON persistence
- `tests/test_config_merge.py` (31 tests) — base config + profile merge, variable resolution
- Shared pytest configuration (`pytest.ini`) and fixtures (`tests/conftest.py`)

### Changed

- Documentation status updated from "in development" to "stable v1.0"
- Framework profile set updated: removed `django-mvt`, added `flask-rest` and `flask-webapp` as production-ready profiles
- GitHub Wiki sync workflow updated with PascalCase flattened naming (no hyphens, no `.md` extension) for full compatibility with GitHub Wiki

### Fixed

- Internal documentation links updated to match new GitHub Wiki PascalCase naming convention
- Documentation references to removed `django-mvt` profile corrected throughout all docs and READMEs
- Phase agent references in `skill.md` updated from placeholder markers to correct file links
- Inconsistent phase count ("9 phases") corrected to the accurate "10 phases (Phase 0 to Phase 9)" across all documentation
- Broken internal links in `install/README.md` pointing to non-existent paths corrected
- `docs/examples/` directory added to Wiki sync (was missing from initial workflow)

### Removed

- `django-mvt` profile removed from `install/config.yaml` and `skills/implement-us/customizations/` — this profile was planned but not implemented; use `generic-python` as a starting point for Django projects

---

[Unreleased]: https://github.com/vvalotto/claude-dev-kit/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/vvalotto/claude-dev-kit/releases/tag/v1.0.0
