# TICKET-057: Tutorial Python Genérico Completo 🐍

**Fase:** 7 - Ejemplos por Stack
**Sprint:** 4
**Estado:** ⏳ Pendiente
**Prioridad:** Alta
**Estimación:** 2 horas
**Asignado a:** Claude Code

## Descripción

Crear tutorial end-to-end completo para el stack **Generic-Python**, demostrando el uso del framework Claude Dev Kit para implementar una utilidad CLI o librería Python sin framework específico.

**Historia de Usuario:**
```
US-005: Utilidad CLI de Archivos CSV

Como data analyst,
Quiero una utilidad CLI para manipular archivos CSV
Para automatizar tareas de procesamiento de datos

Criterios de Aceptación:
- Comando: csvtool convert <input.csv> <output.json>
- Comando: csvtool filter <input.csv> <column> <value> > output.csv
- Comando: csvtool merge <file1.csv> <file2.csv> > merged.csv
- Comando: csvtool stats <input.csv> - Mostrar estadísticas
- Validación de archivos existentes
- Manejo de errores claro
- Help message con ejemplos
```

## Criterios de Aceptación

### Contenido del Tutorial

- [ ] **Introducción clara** - CLI tool con Python stdlib
- [ ] **Requisitos** - Python 3.9+, pytest, argparse
- [ ] **Setup del proyecto** - Estructura de librería
- [ ] **Instalación del framework** - Comando con perfil generic-python
- [ ] **Historia de usuario completa** - US-005 documentada

### Walkthrough de las 10 Fases

- [ ] **Fase 0: Validación** - Verificar prerequisitos
- [ ] **Fase 1: BDD** - Escenarios para comandos CLI
- [ ] **Fase 2: Planning** - Plan con arquitectura modular
- [ ] **Fase 3: Implementación** - Código de:
  - CLI parser (argparse)
  - Módulos: converter, filter, merger, stats
  - Utils: file validation, error handling
  - Entry point (main.py)
- [ ] **Fase 4: Tests Unitarios** - Tests de cada módulo
- [ ] **Fase 5: Tests Integración** - Tests end-to-end CLI
- [ ] **Fase 6: Validación BDD** - Ejecutar escenarios
- [ ] **Fase 7: Quality Gates** - Pylint, cobertura
- [ ] **Fase 8: Documentación** - Docstrings + README
- [ ] **Fase 9: Reporte** - Métricas finales

### Código y Ejemplos

- [ ] **Código ejecutable** - CLI funcional
- [ ] **Ejemplos de uso** - Comandos reales con output
- [ ] **Sample CSV files** - Datos de prueba
- [ ] **Error handling** - Ejemplos de errores

### Calidad

- [ ] **Troubleshooting** - 5+ problemas comunes
- [ ] **Próximos pasos** - Pandas, formatos adicionales, etc.
- [ ] **Tiempo realista** - Completable en 35-45 minutos
- [ ] **Links funcionando** - Referencias correctas

## Dependencias

- **Depende de:** TICKET-052 (análisis y template)
- **Bloquea a:** TICKET-058 (validación)

## Notas Técnicas

### Estructura del Proyecto

```
csvtool/
├── csvtool/
│   ├── __init__.py
│   ├── __main__.py           # Entry point
│   ├── cli.py                # Argparse setup
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── convert.py        # CSV → JSON
│   │   ├── filter.py         # Filter rows
│   │   ├── merge.py          # Merge files
│   │   └── stats.py          # Statistics
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── validators.py     # File validation
│   │   └── errors.py         # Custom exceptions
│   └── models/
│       ├── __init__.py
│       └── csv_data.py       # Data model
├── tests/
│   ├── test_convert.py
│   ├── test_filter.py
│   ├── test_merge.py
│   ├── test_stats.py
│   └── fixtures/
│       ├── sample1.csv
│       └── sample2.csv
├── features/
│   ├── csvtool.feature
│   └── steps/
│       └── csvtool_steps.py
└── README.md
```

### Comandos

**Convert:**
```bash
$ csvtool convert input.csv output.json
Converted 100 rows from input.csv to output.json
```

**Filter:**
```bash
$ csvtool filter data.csv age 25 > filtered.csv
Filtered 15 rows where age=25
```

**Merge:**
```bash
$ csvtool merge file1.csv file2.csv > merged.csv
Merged 250 rows from 2 files
```

**Stats:**
```bash
$ csvtool stats data.csv
File: data.csv
Rows: 100
Columns: 5 (name, age, city, score, active)
Numeric columns: age (avg: 32.5), score (avg: 78.2)
Missing values: 3
```

### Componentes Clave

**CLI Parser:**
```python
import argparse

def create_parser():
    parser = argparse.ArgumentParser(
        prog='csvtool',
        description='CSV manipulation utility'
    )
    subparsers = parser.add_subparsers(dest='command')

    # Convert
    convert_parser = subparsers.add_parser('convert')
    convert_parser.add_argument('input')
    convert_parser.add_argument('output')

    # Filter
    filter_parser = subparsers.add_parser('filter')
    filter_parser.add_argument('input')
    filter_parser.add_argument('column')
    filter_parser.add_argument('value')

    return parser
```

**Convert Module:**
```python
import csv
import json

def convert_csv_to_json(input_path, output_path):
    with open(input_path) as f:
        reader = csv.DictReader(f)
        data = list(reader)

    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)

    return len(data)
```

**Validators:**
- validate_file_exists(path: str) -> bool
- validate_csv_format(path: str) -> bool

### Ejemplos de Output

1. **Help message** - Mostrar ayuda completa
2. **Convert success** - CSV → JSON
3. **Filter output** - Rows filtradas
4. **Stats table** - Estadísticas formateadas
5. **Error handling** - Archivo no existe

## Checklist de Implementación

### Preparación (10 min)
- [ ] Leer template de TICKET-052
- [ ] Definir estructura del tutorial
- [ ] Crear CSV samples

### Escritura del Tutorial (1.25h)
- [ ] Sección: Introducción y requisitos
- [ ] Sección: Setup del proyecto
- [ ] Sección: Instalación del framework
- [ ] Sección: Historia de usuario US-005
- [ ] Sección: Fases 0-2
- [ ] Sección: Fase 3 - CLI + comandos
- [ ] Sección: Fases 4-5 - Tests
- [ ] Sección: Fases 6-9
- [ ] Sección: Ejemplos de uso
- [ ] Sección: Troubleshooting
- [ ] Sección: Próximos pasos

### Validación (25 min)
- [ ] Crear CLI tool y probar comandos
- [ ] Verificar código ejecutable
- [ ] Verificar help y error messages
- [ ] Verificar tiempo <45 min

### Finalización (20 min)
- [ ] Agregar navegación
- [ ] Commit del archivo
- [ ] Actualizar sprint-4.md

## Resultado

_Se completará cuando el ticket esté DONE_

**Archivo generado:** `docs/examples/generic-python.md`

**Estado:** ⏳ Pendiente
