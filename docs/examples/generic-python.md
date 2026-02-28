# Tutorial: Python CLI — CSV Tool

**Stack:** Generic Python (`generic-python`)
**Tiempo Estimado:** 35-45 minutos
**Nivel:** Intermedio

---

## 📋 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Requisitos Previos](#requisitos-previos)
3. [Historia de Usuario](#historia-de-usuario)
4. [Setup del Proyecto](#setup-del-proyecto)
5. [Instalación del Framework](#instalación-del-framework)
6. [Walkthrough: Las 10 Fases](#walkthrough-las-10-fases)
7. [Validación Final](#validación-final)
8. [Troubleshooting](#troubleshooting)
9. [Próximos Pasos](#próximos-pasos)
10. [Recursos](#recursos)

---

## 🎯 Introducción

Este tutorial te guiará paso a paso en la creación de **CSV Tool**, una utilidad CLI
para manipular archivos CSV, utilizando el perfil **generic-python** del Claude Dev Kit.

Aprenderás:
- ✅ Cómo usar el skill `/implement-us` con el perfil genérico de Python
- ✅ Cómo el framework adapta las 10 fases a una herramienta de línea de comandos
- ✅ Cómo estructurar un paquete CLI modular y testeable
- ✅ Buenas prácticas Python: stdlib only, type hints, docstrings, argparse

Al finalizar, tendrás una CLI funcional con:
- 4 subcomandos: `convert`, `filter`, `merge`, `stats`
- Solo Python stdlib (sin dependencias externas)
- Suite completa de tests (unitarios, integración, BDD)
- Código que supera todos los quality gates (Pylint 10.00/10, Coverage 98%)

---

## ✅ Requisitos Previos

### Software Necesario

- **Python:** 3.10 o superior
- **Claude Code CLI:** Instalado y configurado
- **pytest + pytest-bdd:** Se instalarán en el setup
- **Git:** Para control de versiones

### Conocimientos

- Programación básica en Python
- Familiaridad con la terminal/línea de comandos
- (Opcional) Conocimiento básico de argparse

### Verificación

```bash
python --version   # Debe ser >= 3.10
claude --version
git --version
```

---

## 📖 Historia de Usuario

```gherkin
# US-057: Utilidad CLI de Archivos CSV

Como data analyst,
Quiero una utilidad CLI para manipular archivos CSV
Para automatizar tareas de procesamiento de datos
```

### Criterios de Aceptación

- ✅ `csvtool convert <input.csv> <output.json>` — Exportar CSV a JSON
- ✅ `csvtool filter <input.csv> <column> <value>` — Filtrar filas
- ✅ `csvtool merge <file1.csv> <file2.csv> <output.csv>` — Combinar archivos
- ✅ `csvtool stats <input.csv>` — Estadísticas del archivo
- ✅ Validación de archivos con mensajes de error descriptivos
- ✅ Help message con ejemplos
- ✅ Exit code correcto (0 = éxito, 1 = error)

### Alcance

**Componentes a Implementar:**
- **models/csv_data.py:** Dataclass `CsvData` con headers, rows y properties
- **utils/validators.py:** Validaciones de archivos y paths
- **commands/convert.py:** Lógica de conversión CSV → JSON
- **commands/filter_cmd.py:** Filtrado de filas por columna/valor
- **commands/merge.py:** Combinación de múltiples archivos
- **commands/stats.py:** Estadísticas con columnas numéricas
- **cli.py:** Parser argparse + dispatcher central

---

## 🚀 Setup del Proyecto

### 1. Crear Directorio del Proyecto

```bash
mkdir csv-tool
cd csv-tool
```

### 2. Inicializar Git

```bash
git init
git checkout -b develop
```

### 3. Crear Entorno Virtual

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

### 4. Instalar Dependencias

```bash
cat > requirements.txt << EOF
pytest>=8.0.0
pytest-bdd>=7.0.0
pytest-cov>=4.1.0
pylint>=3.0.0
radon>=6.0.0
EOF

pip install -r requirements.txt
```

### 5. Crear Estructura Base

```bash
mkdir -p csvtool/{commands,utils,models}
mkdir -p tests/fixtures
mkdir -p features/steps
mkdir -p historias-usuario
mkdir -p docs/{planning,architecture,reporting}
touch csvtool/__init__.py csvtool/commands/__init__.py
touch csvtool/utils/__init__.py csvtool/models/__init__.py
```

**Estructura del proyecto:**

```
csv-tool/
├── csvtool/
│   ├── __init__.py              # Versión del paquete (a crear)
│   ├── __main__.py              # Entry point (a crear)
│   ├── cli.py                   # Argparse + dispatcher (a crear)
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── convert.py           # CSV → JSON (a crear)
│   │   ├── filter_cmd.py        # Filtrar filas (a crear)
│   │   ├── merge.py             # Combinar archivos (a crear)
│   │   └── stats.py             # Estadísticas (a crear)
│   ├── models/
│   │   ├── __init__.py
│   │   └── csv_data.py          # Modelo de datos (a crear)
│   └── utils/
│       ├── __init__.py
│       └── validators.py        # Validaciones (a crear)
├── tests/
│   ├── conftest.py              # Fixtures (a crear)
│   ├── test_csv_data.py         # Unitarios modelo (a crear)
│   ├── test_validators.py       # Unitarios validadores (a crear)
│   ├── test_convert.py          # Unitarios convert (a crear)
│   ├── test_filter.py           # Unitarios filter (a crear)
│   ├── test_merge.py            # Unitarios merge (a crear)
│   ├── test_stats.py            # Unitarios stats (a crear)
│   ├── test_cli_integration.py  # Integración end-to-end (a crear)
│   ├── test_bdd_csvtool.py      # BDD runners (a crear)
│   └── fixtures/
│       ├── sample1.csv          # Datos de prueba (a crear)
│       └── sample2.csv          # Datos de prueba (a crear)
├── features/
│   ├── csvtool.feature          # Escenarios Gherkin (a crear)
│   └── steps/
│       └── csvtool_steps.py     # Step definitions (a crear)
├── historias-usuario/
├── docs/
├── pytest.ini
└── requirements.txt
```

### 6. Crear Datos de Prueba (Fixtures)

```bash
cat > tests/fixtures/sample1.csv << 'EOF'
name,age,city,score,active
Juan Pérez,28,Madrid,85.5,true
María García,34,Barcelona,92.0,true
Pedro López,22,Madrid,78.3,false
Ana Martínez,45,Valencia,88.7,true
Carlos Ruiz,31,Madrid,67.2,false
EOF

cat > tests/fixtures/sample2.csv << 'EOF'
name,age,city,score,active
Laura Sánchez,27,Sevilla,91.0,true
Miguel Torres,38,Madrid,73.5,false
Isabel Díaz,29,Barcelona,86.8,true
EOF
```

### 7. Crear pytest.ini

```ini
[pytest]
pythonpath = .
testpaths = tests
addopts = -v --tb=short
```

---

## 📦 Instalación del Framework

### 1. Clonar Claude Dev Kit

```bash
cd ~
git clone https://github.com/vvalotto/claude-dev-kit.git ~/.claude-dev-kit
```

### 2. Ejecutar Instalador

```bash
cd ~/csv-tool
python ~/.claude-dev-kit/install/installer.py --profile generic-python --yes
```

**Salida esperada:**

```
🚀 Claude Dev Kit - Installer
================================

📋 Selected Profile: generic-python
   - Architecture: Flexible — Sin patrón arquitectónico forzado
   - Component Types: Module, Class, Function, Package, Utility
   - Test Framework: pytest
   - Quality Gates: Pylint >= 8.0, Coverage >= 95%, CC < 10

✅ Framework instalado exitosamente en .claude/
✅ Perfil 'generic-python' configurado
✅ Skills disponibles: /implement-us, /track-*
✅ Templates instalados
✅ Tracking system initialized

🎉 Installation complete! Ready to use /implement-us
```

---

## 🎬 Walkthrough: Las 10 Fases

### Preparación: Crear Archivo US

```bash
cat > historias-usuario/US-057.md << 'EOF'
# US-057: Utilidad CLI de Archivos CSV

Como data analyst,
Quiero una utilidad CLI para manipular archivos CSV
Para automatizar tareas de procesamiento de datos

## Criterios de Aceptación

- csvtool convert <input.csv> <output.json>
- csvtool filter <input.csv> <column> <value>
- csvtool merge <file1.csv> <file2.csv> <output.csv>
- csvtool stats <input.csv>
- Validación de archivos existentes con errores descriptivos
- Help message con ejemplos de uso
- Exit code: 0 éxito, 1 error

## Notas Técnicas

- Solo Python stdlib (csv, json, argparse, statistics)
- Arquitectura modular: commands/ + models/ + utils/
- Tests: pytest + pytest-bdd
EOF
```

### Ejecutar el Skill

```bash
cd ~/csv-tool
claude
/implement-us US-057
```

---

### 🔍 Fase 0: Validación de Contexto

**Qué hace el framework:**
- ✅ Verifica que `historias-usuario/US-057.md` exista
- ✅ Lee el perfil `generic-python` desde `.claude/skills/implement-us/config.json`
- ✅ Confirma Python 3.10+ disponible
- ✅ Inicializa el tracking de tiempo

**Output:**

```
✅ Historia de usuario encontrada: US-057
✅ Perfil cargado: generic-python
✅ Configuración:
   - Arquitectura: Modular CLI
   - Component Types: Module, Package, Utility
   - Test Framework: pytest
   - Quality Gates: Pylint >= 8.0, Coverage >= 95%, CC < 10
⏱️  Tracking iniciado para US-057

🎯 Contexto validado. Procediendo a Fase 1...
```

---

### 📝 Fase 1: Generación de Escenarios BDD

**Qué hace el framework:**
- Genera escenarios Gherkin para cada subcomando CLI
- Cubre casos de éxito y error

**Archivo generado (`features/csvtool.feature`):**

```gherkin
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
```

---

### 📐 Fase 2: Plan de Implementación + ADR

**Documentos generados:**

- `docs/planning/US-057-plan.md` — Plan con contratos de módulos y tareas
- `docs/architecture/ADR-001-csvtool-modular-architecture.md` — Decision record

**ADR resumen:**

```markdown
## Decisión: Arquitectura Modular (un módulo por comando)

Opciones consideradas:
- Script monolítico: Rechazado (viola SRP, no testeable por partes)
- Paquete modular (ELEGIDA): SRP, testeable independientemente, extensible
- Click framework: Rechazado (dependencia externa, contra "stdlib only")

Consecuencias:
✅ cli.py solo hace parsing y dispatch
✅ Cada comando testeable sin CLI completo
✅ Fácil agregar nuevos comandos
✅ CsvData como tipo compartido entre comandos
```

---

### ⚙️ Fase 3: Implementación

**Código generado módulo por módulo:**

#### `csvtool/models/csv_data.py`

```python
"""Data model for CSV content."""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class CsvData:
    """Represents the content of a CSV file.

    Attributes:
        headers: List of column names.
        rows: List of rows, each row is a dict mapping header -> value.
    """
    headers: List[str]
    rows: List[Dict[str, str]] = field(default_factory=list)

    @property
    def row_count(self) -> int:
        """Return the number of data rows."""
        return len(self.rows)

    @property
    def column_count(self) -> int:
        """Return the number of columns."""
        return len(self.headers)

    @property
    def numeric_columns(self) -> Dict[str, List[float]]:
        """Return columns whose values are all numeric."""
        result: Dict[str, List[float]] = {}
        for header in self.headers:
            values = []
            all_numeric = True
            for row in self.rows:
                try:
                    values.append(float(row.get(header, "")))
                except ValueError:
                    all_numeric = False
                    break
            if all_numeric and values:
                result[header] = values
        return result
```

#### `csvtool/utils/validators.py`

```python
"""File and path validators for CSV Tool."""

import os


def validate_file_exists(path: str) -> None:
    """Verify that a file exists and is readable."""
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File not found: {path}")


def validate_csv_extension(path: str) -> None:
    """Verify that a file has a .csv extension."""
    if not path.lower().endswith(".csv"):
        raise ValueError(f"File must have .csv extension: {path}")


def validate_output_path(path: str) -> None:
    """Verify that the output path's parent directory exists and is writable."""
    parent = os.path.dirname(os.path.abspath(path))
    if not os.path.isdir(parent):
        raise ValueError(f"Output directory does not exist: {parent}")
    if not os.access(parent, os.W_OK):
        raise ValueError(f"Output directory is not writable: {parent}")
```

#### `csvtool/commands/convert.py`

```python
"""Convert command: CSV to JSON."""

import csv
import json
from csvtool.utils.validators import validate_csv_extension, validate_file_exists, validate_output_path


def convert_csv_to_json(input_path: str, output_path: str) -> int:
    """Convert a CSV file to JSON format. Returns number of rows converted."""
    validate_csv_extension(input_path)
    validate_file_exists(input_path)
    validate_output_path(output_path)

    with open(input_path, newline="", encoding="utf-8") as csv_file:
        rows = list(csv.DictReader(csv_file))

    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(rows, json_file, indent=2, ensure_ascii=False)

    return len(rows)
```

#### `csvtool/commands/filter_cmd.py`

```python
"""Filter command: filter CSV rows by column value."""

import csv
from csvtool.models.csv_data import CsvData
from csvtool.utils.validators import validate_file_exists, validate_csv_extension


def filter_csv(input_path: str, column: str, value: str) -> CsvData:
    """Filter rows where column equals value. Returns CsvData with matching rows."""
    validate_file_exists(input_path)
    validate_csv_extension(input_path)

    with open(input_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        headers = list(reader.fieldnames or [])
        rows = list(reader)

    if column not in headers:
        raise ValueError(
            f"Column '{column}' not found. Available columns: {', '.join(headers)}"
        )

    return CsvData(headers=headers, rows=[r for r in rows if r.get(column) == value])
```

#### `csvtool/commands/merge.py`

```python
"""Merge command: combine multiple CSV files."""

import csv
from typing import List
from csvtool.utils.validators import validate_file_exists, validate_csv_extension, validate_output_path


def merge_csv_files(file_paths: List[str], output_path: str) -> int:
    """Merge CSV files. All must share the same headers. Returns total rows written."""
    if len(file_paths) < 2:
        raise ValueError("At least 2 files are required for merge")

    for path in file_paths:
        validate_file_exists(path)
        validate_csv_extension(path)
    validate_output_path(output_path)

    all_rows, reference_headers = [], []
    for i, path in enumerate(file_paths):
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            headers = list(reader.fieldnames or [])
            rows = list(reader)
        if i == 0:
            reference_headers = headers
        elif headers != reference_headers:
            raise ValueError(f"File '{path}' has different headers.")
        all_rows.extend(rows)

    with open(output_path, "w", newline="", encoding="utf-8") as out_file:
        writer = csv.DictWriter(out_file, fieldnames=reference_headers)
        writer.writeheader()
        writer.writerows(all_rows)

    return len(all_rows)
```

#### `csvtool/commands/stats.py`

```python
"""Stats command: display statistics for a CSV file."""

import csv
import statistics
from typing import Any, Dict
from csvtool.models.csv_data import CsvData
from csvtool.utils.validators import validate_file_exists, validate_csv_extension


def calculate_stats(input_path: str) -> Dict[str, Any]:
    """Calculate statistics: rows, columns, numeric averages, missing values."""
    validate_file_exists(input_path)
    validate_csv_extension(input_path)

    with open(input_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        data = CsvData(headers=list(reader.fieldnames or []), rows=list(reader))

    numeric_stats = {
        col: {"avg": round(statistics.mean(vals), 2), "min": min(vals), "max": max(vals)}
        for col, vals in data.numeric_columns.items()
    }
    missing = sum(1 for row in data.rows for val in row.values() if val == "")

    return {
        "file": input_path, "rows": data.row_count,
        "columns": data.column_count, "column_names": data.headers,
        "numeric_stats": numeric_stats, "missing_values": missing,
    }


def format_stats(stats: Dict[str, Any]) -> str:
    """Format stats dict as human-readable string."""
    lines = [
        f"File: {stats['file']}",
        f"Rows: {stats['rows']}",
        f"Columns: {stats['columns']} ({', '.join(stats['column_names'])})",
    ]
    if stats["numeric_stats"]:
        lines.append("Numeric columns:")
        for col, v in stats["numeric_stats"].items():
            lines.append(f"  {col}: avg={v['avg']}, min={v['min']}, max={v['max']}")
    lines.append(f"Missing values: {stats['missing_values']}")
    return "\n".join(lines)
```

#### `csvtool/cli.py`

```python
"""CLI entry point for CSV Tool."""

import argparse
import sys
from typing import List, Optional
from csvtool.commands.convert import convert_csv_to_json
from csvtool.commands.filter_cmd import filter_csv
from csvtool.commands.merge import merge_csv_files
from csvtool.commands.stats import calculate_stats, format_stats


def create_parser() -> argparse.ArgumentParser:
    """Create and return the argument parser."""
    parser = argparse.ArgumentParser(
        prog="csvtool",
        description="CSV manipulation utility",
        epilog=(
            "Examples:\n"
            "  csvtool convert data.csv data.json\n"
            "  csvtool filter data.csv city Madrid\n"
            "  csvtool merge file1.csv file2.csv merged.csv\n"
            "  csvtool stats data.csv\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", metavar="COMMAND")

    c = sub.add_parser("convert", help="Convert CSV to JSON")
    c.add_argument("input"); c.add_argument("output")

    f = sub.add_parser("filter", help="Filter rows by column value")
    f.add_argument("input"); f.add_argument("column"); f.add_argument("value")

    m = sub.add_parser("merge", help="Merge CSV files")
    m.add_argument("files", nargs="+"); m.add_argument("output")

    s = sub.add_parser("stats", help="Show statistics")
    s.add_argument("input")

    return parser


def run(args: Optional[List[str]] = None) -> int:
    """Parse arguments and dispatch command. Returns exit code."""
    parser = create_parser()
    parsed = parser.parse_args(args)

    if parsed.command is None:
        parser.print_help(); return 1

    try:
        if parsed.command == "convert":
            count = convert_csv_to_json(parsed.input, parsed.output)
            print(f"Converted {count} rows from {parsed.input} to {parsed.output}")

        elif parsed.command == "filter":
            result = filter_csv(parsed.input, parsed.column, parsed.value)
            for row in result.rows:
                print(",".join(row.values()))
            print(f"Filtered {result.row_count} rows where "
                  f"{parsed.column}={parsed.value}", file=sys.stderr)

        elif parsed.command == "merge":
            *inputs, output = parsed.files + [parsed.output]
            count = merge_csv_files(inputs, output)
            print(f"Merged {count} rows from {len(inputs)} files into {output}")

        elif parsed.command == "stats":
            print(format_stats(calculate_stats(parsed.input)))

    except (FileNotFoundError, ValueError, PermissionError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    return 0
```

---

### 🧪 Fase 4: Tests Unitarios

**Estructura de tests unitarios:**

| Archivo | Tests | Qué prueba |
|---------|-------|------------|
| `test_csv_data.py` | 10 | `CsvData` properties y `numeric_columns` |
| `test_validators.py` | 10 | Validaciones de file, extensión y output path |
| `test_convert.py` | 7 | Conversión correcta, errores de archivo |
| `test_filter.py` | 10 | Filtrado por columna, resultado vacío, errores |
| `test_merge.py` | 8 | Merge correcto, headers incompatibles, errores |
| `test_stats.py` | 15 | Estadísticas numéricas, formato de salida |

**Ejemplo de test con parametrize:**

```python
class TestFilterCsv:
    def test_filter_by_city_madrid(self, sample1_path):
        result = filter_csv(sample1_path, "city", "Madrid")
        assert result.row_count == 3

    def test_filter_no_match_returns_empty(self, sample1_path):
        result = filter_csv(sample1_path, "city", "ZZZ_nonexistent")
        assert result.row_count == 0
        assert result.headers  # Headers still present

    def test_filter_invalid_column_raises(self, sample1_path):
        with pytest.raises(ValueError, match="Column 'nonexistent' not found"):
            filter_csv(sample1_path, "nonexistent", "value")
```

**Ejecutar tests unitarios:**

```bash
pytest tests/test_csv_data.py tests/test_validators.py \
       tests/test_convert.py tests/test_filter.py \
       tests/test_merge.py tests/test_stats.py -v
```

**Output esperado:** 60 passed

---

### 🔗 Fase 5: Tests de Integración

**`tests/test_cli_integration.py` — Tests end-to-end del CLI:**

```python
class TestCliConvert:
    def test_convert_exit_code_zero(self, sample1_path, tmp_json):
        code = run(["convert", sample1_path, tmp_json])
        assert code == 0

    def test_convert_creates_json_file(self, sample1_path, tmp_json):
        run(["convert", sample1_path, tmp_json])
        assert os.path.isfile(tmp_json)

    def test_convert_nonexistent_file_returns_1(self, tmp_json):
        code = run(["convert", "nonexistent.csv", tmp_json])
        assert code == 1

class TestCliStats:
    def test_stats_output_has_rows(self, sample1_path, capsys):
        run(["stats", sample1_path])
        assert "Rows: 5" in capsys.readouterr().out

class TestCliGeneral:
    def test_no_command_returns_1(self):
        assert run([]) == 1

    def test_help_exits_cleanly(self):
        with pytest.raises(SystemExit) as exc:
            run(["--help"])
        assert exc.value.code == 0
```

**Ejecutar:**

```bash
pytest tests/test_cli_integration.py -v
```

**Output esperado:** 20 passed

---

### ✅ Fase 6: Validación BDD

**`features/steps/csvtool_steps.py` (fragmento):**

```python
@given("sample CSV files exist in the fixtures directory")
def sample_files_exist():
    assert os.path.isfile(os.path.join(FIXTURES_DIR, "sample1.csv"))


@when(parsers.parse('I run "{command_line}"'))
def run_command(command_line, ctx, capsys, tmp_path):
    parts = command_line.split()
    # Resolver paths de fixtures y output temporales
    resolved = resolve_paths(parts[1:], FIXTURES_DIR, tmp_path)
    try:
        ctx["exit_code"] = run(resolved)
    except SystemExit as exc:
        ctx["exit_code"] = exc.code or 0
    captured = capsys.readouterr()
    ctx["stdout"] = captured.out
    ctx["stderr"] = captured.err


@then(parsers.parse("the command exits with code {code:d}"))
def check_exit_code(ctx, code):
    assert ctx["exit_code"] == code
```

**Ejecutar tests BDD:**

```bash
pytest tests/test_bdd_csvtool.py -v
```

**Output esperado:**
```
tests/test_bdd_csvtool.py::test_convert_csv_to_json_successfully PASSED
tests/test_bdd_csvtool.py::test_convert_file_not_found PASSED
tests/test_bdd_csvtool.py::test_filter_csv_by_column_value PASSED
tests/test_bdd_csvtool.py::test_filter_column_not_found PASSED
tests/test_bdd_csvtool.py::test_merge_two_csv_files PASSED
tests/test_bdd_csvtool.py::test_show_csv_statistics PASSED
tests/test_bdd_csvtool.py::test_show_help_message PASSED
tests/test_bdd_csvtool.py::test_no_command_provided PASSED
tests/test_bdd_csvtool.py::test_stats_numeric_columns PASSED
tests/test_bdd_csvtool.py::test_filter_empty_result PASSED

10 passed in 0.21s
```

---

### 📊 Fase 7: Quality Gates

**Ejecutar suite completa con coverage:**

```bash
pytest tests/ --cov=csvtool --cov-report=term-missing -q
```

**Output de coverage:**

```
Name                             Stmts   Miss  Cover
------------------------------------------------------
csvtool/__init__.py                  2      0   100%
csvtool/__main__.py                  3      3     0%   # Entry point - OK
csvtool/cli.py                      49      0   100%
csvtool/commands/__init__.py         5      0   100%
csvtool/commands/convert.py         13      0   100%
csvtool/commands/filter_cmd.py      15      0   100%
csvtool/commands/merge.py           27      0   100%
csvtool/commands/stats.py           29      0   100%
csvtool/models/__init__.py           2      0   100%
csvtool/models/csv_data.py          28      0   100%
csvtool/utils/__init__.py            2      0   100%
csvtool/utils/validators.py         13      1    92%
------------------------------------------------------
TOTAL                              188      4    98%

90 passed in 0.64s
```

> **Nota sobre `__main__.py`:** Los 3 statements no cubiertos son el entry point del módulo
> (`sys.exit(run())`). Solo se ejecuta cuando se corre `python -m csvtool`, nunca en tests.
> Esto es comportamiento esperado y aceptable.

**Ejecutar pylint:**

```bash
pylint csvtool/
```

**Output:** `Your code has been rated at 10.00/10`

**Ejecutar análisis de complejidad:**

```bash
radon cc csvtool/ -a
# Average complexity: A (3.47)

radon mi csvtool/
# Todos los módulos: A
```

**Resumen Quality Gates:**

| Métrica | Resultado | Objetivo | Estado |
|---------|-----------|----------|--------|
| Tests Passing | 90/90 (100%) | 100% | ✅ |
| Coverage | 98% | ≥ 95% | ✅ |
| Pylint | 10.00/10 | ≥ 8.0 | ✅ |
| Complejidad | A (3.47) | < 10 | ✅ |
| Maintainability | A (todos) | MI ≥ 20 | ✅ |

---

### 📚 Fase 8: Documentación

**README.md generado con secciones:**
- Instalación y uso rápido
- Tabla de comandos con sintaxis
- Arquitectura del paquete
- Quality gates
- Cómo ejecutar los tests

**Docstrings en todos los módulos:**

```python
def convert_csv_to_json(input_path: str, output_path: str) -> int:
    """Convert a CSV file to JSON format.

    Reads all rows from the CSV file and writes them as a JSON array,
    where each element is a dict mapping column name to value.

    Args:
        input_path: Path to the input CSV file.
        output_path: Path for the output JSON file.

    Returns:
        Number of rows converted.

    Raises:
        FileNotFoundError: If the input file does not exist.
        ValueError: If the input file is not a valid CSV.

    Examples:
        >>> convert_csv_to_json("data.csv", "data.json")
        5
    """
```

---

### 📋 Fase 9: Reporte Final

**Documento generado:** `docs/reporting/US-057-report.md`

**Contenido del reporte:**
- Estado de todos los criterios de aceptación
- Métricas de calidad completas
- Tabla de archivos generados con líneas
- Tiempo por fase
- Decisiones técnicas documentadas
- Limitaciones conocidas y próximos pasos

**Tiempo total registrado:** ~7 minutos (implementación real con el framework)

---

## 🏆 Validación Final

### Ejecutar Suite Completa

```bash
pytest tests/ -v
```

**Resultado esperado:**

```
tests/test_bdd_csvtool.py::test_convert_csv_to_json_successfully PASSED
tests/test_bdd_csvtool.py::test_convert_file_not_found PASSED
tests/test_bdd_csvtool.py::test_filter_csv_by_column_value PASSED
tests/test_bdd_csvtool.py::test_filter_column_not_found PASSED
tests/test_bdd_csvtool.py::test_merge_two_csv_files PASSED
tests/test_bdd_csvtool.py::test_show_csv_statistics PASSED
tests/test_bdd_csvtool.py::test_show_help_message PASSED
tests/test_bdd_csvtool.py::test_no_command_provided PASSED
tests/test_bdd_csvtool.py::test_stats_numeric_columns PASSED
tests/test_bdd_csvtool.py::test_filter_empty_result PASSED
tests/test_cli_integration.py::TestCliConvert::test_convert_exit_code_zero PASSED
tests/test_cli_integration.py::TestCliConvert::test_convert_creates_json_file PASSED
... (20 integration tests)
tests/test_convert.py::TestConvertCsvToJson::test_converts_successfully PASSED
... (7 convert tests)
tests/test_csv_data.py::TestCsvDataBasic::test_row_count_empty PASSED
... (10 csv_data tests)
tests/test_filter.py::TestFilterCsv::test_filter_by_city_madrid PASSED
... (10 filter tests)
tests/test_merge.py::TestMergeCsvFiles::test_merges_two_files PASSED
... (8 merge tests)
tests/test_stats.py::TestCalculateStats::test_returns_correct_row_count PASSED
... (15 stats tests)
tests/test_validators.py::TestValidateFileExists::test_existing_file_passes PASSED
... (10 validator tests)

============================== 90 passed in 0.68s ==============================
```

### Probar la CLI Manualmente

```bash
# Desde el directorio del proyecto
cd examples/code/csv-tool

# Convert
python -m csvtool convert tests/fixtures/sample1.csv /tmp/output.json
# Converted 5 rows from tests/fixtures/sample1.csv to /tmp/output.json

cat /tmp/output.json | python -m json.tool | head -10
# [
#   {
#     "name": "Juan Pérez",
#     "age": "28",
#     "city": "Madrid",
#     "score": "85.5",
#     "active": "true"
#   },
#   ...

# Filter (solo filas de Madrid)
python -m csvtool filter tests/fixtures/sample1.csv city Madrid
# Juan Pérez,28,Madrid,85.5,true
# Pedro López,22,Madrid,78.3,false
# Carlos Ruiz,31,Madrid,67.2,false
# (stderr): Filtered 3 rows where city=Madrid

# Merge
python -m csvtool merge tests/fixtures/sample1.csv tests/fixtures/sample2.csv /tmp/merged.csv
# Merged 8 rows from 2 files into /tmp/merged.csv

# Stats
python -m csvtool stats tests/fixtures/sample1.csv
# File: tests/fixtures/sample1.csv
# Rows: 5
# Columns: 5 (name, age, city, score, active)
# Numeric columns:
#   age: avg=32.0, min=22.0, max=45.0
#   score: avg=82.34, min=67.2, max=92.0
# Missing values: 0

# Error handling
python -m csvtool convert nonexistent.csv output.json
# (stderr): Error: File not found: nonexistent.csv
echo $?   # 1

# Help
python -m csvtool --help
```

---

## 🔧 Troubleshooting

### Error: ModuleNotFoundError

```
ModuleNotFoundError: No module named 'csvtool'
```

**Solución:** Verificar `pytest.ini` con pythonpath:

```ini
[pytest]
pythonpath = .
testpaths = tests
```

### Error: BDD steps no encontrados

```
pytest_bdd.exceptions.StepDefinitionNotFoundError
```

**Solución:** Verificar que `conftest.py` incluye el plugin:

```python
pytest_plugins = ["features.steps.csvtool_steps"]
```

### Error: Coverage no alcanza 95%

Si el coverage es menor al esperado, verificar que el `--cov` apunta al paquete correcto:

```bash
pytest tests/ --cov=csvtool --cov-report=term-missing
#                   ^^^^^^^ nombre del paquete, no del directorio
```

### Error: Pylint reporta wrong-import-order

El orden correcto de imports en Python:

```python
# 1. stdlib
import csv
import statistics

# 2. third-party (si existieran)

# 3. first-party (tu paquete)
from csvtool.models.csv_data import CsvData
```

### Error: BDD - file not found con paths relativos

Los step definitions deben resolver paths desde el directorio raíz del proyecto:

```python
FIXTURES_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "tests", "fixtures"
)
```

### Error: merge - "different headers"

Los archivos a combinar deben tener exactamente los mismos headers en el mismo orden:

```bash
# Verificar headers
head -1 file1.csv
head -1 file2.csv
```

---

## 🚀 Próximos Pasos

### Extensiones Naturales

```python
# Soporte para delimitadores alternativos
csvtool convert data.tsv output.json --delimiter "\t"

# Filter case-insensitive
csvtool filter data.csv city madrid --ignore-case

# Merge por columna clave
csvtool merge file1.csv file2.csv merged.csv --key id
```

### Integración con Pandas

```python
# Para datasets grandes, reemplazar la capa de datos:
import pandas as pd

def convert_csv_to_json(input_path: str, output_path: str) -> int:
    df = pd.read_csv(input_path)
    df.to_json(output_path, orient="records", indent=2)
    return len(df)
```

### Empaquetado como CLI instalable

```toml
# pyproject.toml
[project.scripts]
csvtool = "csvtool.cli:run"
```

```bash
pip install -e .
csvtool stats data.csv  # Sin "python -m"
```

### Explorar Otros Perfiles del Framework

- **flask-rest** → API REST JSON (ver `flask-rest-api-project.md`)
- **flask-webapp** → Fullstack con templates (ver `flask-webapp-project.md`)
- **fastapi-rest** → FastAPI async (ver `fastapi-project.md`)
- **pyqt-mvc** → Desktop GUI con PyQt6 (ver `pyqt-project.md`)

---

## 📚 Recursos

### Código Fuente del Ejemplo

```
examples/code/csv-tool/
```

### Documentación Relacionada

- `docs/user/getting-started.md` — Guía de inicio del framework
- `docs/user/installation.md` — Instalación detallada
- `docs/skills/implement-us/index.md` — Documentación del skill

### Artefactos Generados por el Framework

- `docs/planning/US-057-plan.md` — Plan completo
- `docs/architecture/ADR-001-csvtool-modular-architecture.md` — Decision record
- `docs/reporting/US-057-report.md` — Reporte final con métricas
- `features/csvtool.feature` — Escenarios Gherkin

### Python Resources

- [argparse Documentation](https://docs.python.org/3/library/argparse.html)
- [csv module Documentation](https://docs.python.org/3/library/csv.html)
- [pytest-bdd Documentation](https://pytest-bdd.readthedocs.io/)

---

**Generado con Claude Dev Kit** — Framework para desarrollo asistido con Claude Code

*Stack: generic-python | Tests: 90/90 | Coverage: 98% | Pylint: 10.00/10*

---

**[← Anterior: Flask WebApp](flask-webapp-project.md)** | **[Índice de Ejemplos](../README.md)**
