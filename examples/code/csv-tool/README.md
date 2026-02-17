# CSV Tool

Utilidad CLI para manipular archivos CSV, construida con Python stdlib y siguiendo
las mejores prácticas del Claude Dev Kit framework (perfil `generic-python`).

## Características

- **convert** — Convierte CSV a JSON
- **filter** — Filtra filas por valor de columna
- **merge** — Combina múltiples archivos CSV
- **stats** — Muestra estadísticas del archivo
- Solo Python stdlib (csv, json, argparse, statistics, pathlib)
- **90/90 tests passing** (unitarios, integración, BDD)
- **Coverage: 98%** | **Pylint: 10.00/10** | **Complejidad: A**

## Requisitos

- Python 3.10+
- pytest, pytest-bdd, pytest-cov (solo para tests)

## Instalación

```bash
cd examples/code/csv-tool/
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Uso

```bash
# Ejecutar como módulo
python -m csvtool <command> [args]

# Convertir CSV a JSON
python -m csvtool convert data.csv data.json
# Output: Converted 5 rows from data.csv to data.json

# Filtrar filas por columna=valor
python -m csvtool filter data.csv city Madrid
# Output (stdout): filas CSV filtradas
# Output (stderr): Filtered 3 rows where city=Madrid

# Combinar archivos CSV
python -m csvtool merge file1.csv file2.csv merged.csv
# Output: Merged 8 rows from 2 files into merged.csv

# Mostrar estadísticas
python -m csvtool stats data.csv
# Output:
# File: data.csv
# Rows: 5
# Columns: 5 (name, age, city, score, active)
# Numeric columns:
#   age: avg=32.0, min=22.0, max=45.0
#   score: avg=82.34, min=67.2, max=92.0
# Missing values: 0

# Mostrar ayuda
python -m csvtool --help
python -m csvtool convert --help
```

## Comandos

| Comando | Sintaxis | Descripción |
|---------|----------|-------------|
| convert | `csvtool convert <input.csv> <output.json>` | Exporta CSV a JSON |
| filter | `csvtool filter <input.csv> <column> <value>` | Filtra filas por columna |
| merge | `csvtool merge <file1.csv> <file2.csv> <output.csv>` | Combina archivos |
| stats | `csvtool stats <input.csv>` | Estadísticas del archivo |

## Testing

```bash
# Todos los tests
pytest tests/ -v

# Con coverage
pytest tests/ --cov=csvtool --cov-report=term-missing

# Solo BDD
pytest tests/test_bdd_csvtool.py -v

# Solo unitarios
pytest tests/test_csv_data.py tests/test_validators.py tests/test_convert.py \
       tests/test_filter.py tests/test_merge.py tests/test_stats.py -v
```

## Arquitectura

```
csvtool/
├── __init__.py              # Versión del paquete
├── __main__.py              # Entry point (python -m csvtool)
├── cli.py                   # Parser argparse + dispatcher
├── commands/
│   ├── convert.py           # CSV → JSON
│   ├── filter_cmd.py        # Filtrar filas por columna/valor
│   ├── merge.py             # Combinar archivos CSV
│   └── stats.py             # Estadísticas + formateo
├── models/
│   └── csv_data.py          # Dataclass CsvData
└── utils/
    └── validators.py        # Validación de archivos y paths
```

**Flujo de datos:** `CLI Input → cli.py (parser) → commands/*.py → utils/validators.py → models/CsvData → Output`

## Quality Gates

| Métrica | Resultado | Objetivo |
|---------|-----------|----------|
| Tests | 90/90 (100%) | 100% |
| Coverage | 98% | ≥ 95% |
| Pylint | 10.00/10 | ≥ 8.0 |
| Complejidad | A (3.47) | < 10 |
| Mantenibilidad | A (todos) | MI ≥ 20 |

## Artefactos del Framework

- `docs/planning/US-057-plan.md` — Plan de implementación
- `docs/architecture/ADR-001-csvtool-modular-architecture.md` — Decision record
- `docs/reporting/US-057-report.md` — Reporte final
- `features/csvtool.feature` — Escenarios BDD en Gherkin

## Generado con Claude Dev Kit

Framework para desarrollo asistido con Claude Code.
Perfil: `generic-python` | Stack: Python stdlib | Tests: 90/90 | Coverage: 98%
