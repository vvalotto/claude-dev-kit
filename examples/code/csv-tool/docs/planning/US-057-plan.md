# US-057: CSV Tool CLI — Plan de Implementación

**Stack:** generic-python
**Perfil:** generic-python.json
**Arquitectura:** Modular CLI (Commands + Models + Utils)
**Fecha:** 2026-02-17

---

## 1. Contexto

Historia de usuario US-057 solicita una herramienta CLI para manipular archivos CSV.
El perfil `generic-python` indica:
- Arquitectura modular sin framework forzado
- Python stdlib únicamente
- pytest como framework de testing
- Quality Gates: Pylint ≥ 8.0, Coverage ≥ 95%, CC ≤ 10, MI ≥ 20

## 2. Arquitectura Seleccionada

```
csvtool/               ← Paquete instalable
├── __init__.py        ← Exports públicos
├── __main__.py        ← Entry point (python -m csvtool)
├── cli.py             ← Parser argparse + despachador
├── commands/          ← Un módulo por comando
│   ├── convert.py     ← CSV → JSON
│   ├── filter_cmd.py  ← Filtrar filas
│   ├── merge.py       ← Combinar archivos
│   └── stats.py       ← Estadísticas
├── models/
│   └── csv_data.py    ← Dataclass CsvData
└── utils/
    └── validators.py  ← Validación de archivos
```

**Justificación:** Ver ADR-001.

## 3. Contratos de Módulos

### models/csv_data.py
```python
@dataclass
class CsvData:
    headers: List[str]
    rows: List[Dict[str, str]]

    row_count: int          # property
    column_count: int       # property
    numeric_columns: dict   # property — columnas con valores numéricos
```

### utils/validators.py
```python
def validate_file_exists(path: str) -> None     # raise FileNotFoundError
def validate_csv_extension(path: str) -> None   # raise ValueError
def validate_output_path(path: str) -> None     # raise ValueError
```

### commands/convert.py
```python
def convert_csv_to_json(input_path: str, output_path: str) -> int  # rows converted
```

### commands/filter_cmd.py
```python
def filter_csv(input_path: str, column: str, value: str) -> CsvData
```

### commands/merge.py
```python
def merge_csv_files(files: List[str], output_path: str) -> int  # rows merged
```

### commands/stats.py
```python
def calculate_stats(input_path: str) -> dict
def format_stats(stats: dict) -> str
```

### cli.py
```python
def create_parser() -> argparse.ArgumentParser
def run(args: Optional[List[str]] = None) -> int  # exit code
```

## 4. Tareas de Implementación

### Fase 3 — Implementación

| Archivo | Descripción | Estimación |
|---------|-------------|------------|
| models/csv_data.py | Dataclass CsvData con properties | 10 min |
| utils/validators.py | Validación de paths y archivos | 10 min |
| commands/convert.py | CSV → JSON | 10 min |
| commands/filter_cmd.py | Filtrado por columna/valor | 10 min |
| commands/merge.py | Merge de archivos CSV | 10 min |
| commands/stats.py | Estadísticas + formato | 15 min |
| cli.py | Argparse + dispatcher | 15 min |
| __init__.py, __main__.py | Wiring | 5 min |
| fixtures (sample CSVs) | Datos de prueba | 5 min |

**Total estimado Fase 3:** ~90 min

### Fase 4 — Tests Unitarios

| Archivo | Tests |
|---------|-------|
| test_csv_data.py | CsvData properties |
| test_validators.py | Validaciones |
| test_convert.py | Conversión CSV → JSON |
| test_filter.py | Filtrado con múltiples casos |
| test_merge.py | Merge de archivos |
| test_stats.py | Estadísticas numéricas |

### Fase 5 — Tests de Integración

| Archivo | Tests |
|---------|-------|
| test_cli_integration.py | End-to-end por cada subcomando |

### Fase 6 — Tests BDD

| Archivo | Tests |
|---------|-------|
| features/steps/csvtool_steps.py | Step definitions |
| tests/test_bdd_csvtool.py | Scenario runners |

## 5. Datos de Prueba (fixtures)

**tests/fixtures/sample1.csv:**
```
name,age,city,score,active
Juan Pérez,28,Madrid,85.5,true
María García,34,Barcelona,92.0,true
Pedro López,22,Madrid,78.3,false
Ana Martínez,45,Valencia,88.7,true
Carlos Ruiz,31,Madrid,67.2,false
```

**tests/fixtures/sample2.csv:**
```
name,age,city,score,active
Laura Sánchez,27,Sevilla,91.0,true
Miguel Torres,38,Madrid,73.5,false
Isabel Díaz,29,Barcelona,86.8,true
```

## 6. Criterios de Aceptación Técnicos

- Todos los comandos CLI funcionan con flags `--help`
- Exit code 0 en éxito, 1 en error
- Mensajes de error descriptivos con prefijo "Error:"
- 100% de comandos documentados del ticket implementados
- Tests: ≥ 95% coverage
- Pylint: ≥ 8.0/10

---

**Documento generado:** Fase 2 - /implement-us US-057
**Perfil aplicado:** generic-python
