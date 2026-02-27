# Skill: implement-us

**Versión:** 2.1.0 (v1.3.0 del framework)
**Última actualización:** 2026-02-27

Skill principal de Claude Dev Kit. Guía la implementación completa de una historia de usuario a través de 10 fases estructuradas, desde la validación del entorno hasta el reporte final.

---

## Tabla de Contenidos

- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Las 10 Fases](#las-10-fases)
- [Artefactos](#artefactos)
- [Configuración](#configuración)
- [Perfiles de Customización](#perfiles-de-customización)
- [Tracking de Tiempo](#tracking-de-tiempo)
- [Protocolo de Recuperación ante Fallas](#protocolo-de-recuperación-ante-fallas)
- [Referencia Técnica](#referencia-técnica)

---

## Requisitos

El entorno del proyecto destino debe satisfacer las siguientes precondiciones antes de invocar el skill:

| Precondición | Verificación | Quién la valida |
|---|---|---|
| Python 3.10+ disponible | `python --version` | Usuario / Fase 0 |
| Repositorio git inicializado | `git status` | Usuario |
| Framework instalado en `.claude/` | `ls .claude/skills/implement-us/config.json` | Fase 0 |
| Perfil de customización activo | Clave `active_profile` en `config.json` | Fase 0 |
| `pylint` instalado | `python -m pylint --version` | Fase 0 |
| `radon` instalado | `python -m radon --version` | Fase 0 |
| `pytest` instalado | `python -m pytest --version` | Fase 0 |
| `pytest-bdd` instalado (si aplica BDD) | `python -c "import pytest_bdd"` | Fase 0 |
| Historia de usuario accesible | Documento local / Issue / Ticket | Confirmado en Fase 0 |

La Fase 0 valida automáticamente estas condiciones al iniciar. Si alguna herramienta falta, el skill detiene la ejecución con un mensaje claro (fail-fast).

---

## Instalación

El skill se instala como parte del framework. Ver [Getting Started](../../../docs/user/getting-started.md) para instrucciones completas.

```bash
# Verificar que el skill está instalado correctamente
ls .claude/skills/implement-us/config.json
```

---

## Uso

### Invocación básica

```bash
/implement-us {US_ID}
```

### Opciones disponibles

| Opción | Descripción | Ejemplo |
|---|---|---|
| `{US_ID}` | ID de la historia de usuario (requerido) | `US-001` |
| `--producto {PRODUCT}` | Nombre del producto o módulo | `--producto mi_app` |
| `--skip-bdd` | Saltar la generación de escenarios BDD | `--skip-bdd` |

```bash
# Ejemplos
/implement-us US-001
/implement-us US-001 --producto mi_app
/implement-us US-001 --skip-bdd
/implement-us US-001 --producto auth --skip-bdd
```

> **Nota:** `--skip-bdd` se puede especificar en CLI o declarar en `config.json` (`"skip_bdd": true`). La Fase 0 confirma la decisión con el usuario antes de continuar.

---

## Las 10 Fases

El skill ejecuta las fases en orden estricto. Cada fase tiene un **gate de entrada** (verifica artefactos de fases previas) y un **checklist de salida** (verifica que sus artefactos están en disco antes de cerrar).

| Fase | Nombre | Aprobación requerida | Artefacto principal |
|---|---|---|---|
| 0 | Validación de Contexto | No | `docs/plans/{US_ID}-context.md` |
| 1 | Generación de Escenarios BDD | Sí | `tests/features/{US_ID}.feature` |
| 2 | Plan de Implementación | Sí | `docs/plans/{US_ID}-plan.md` |
| 3 | Implementación | No | Archivos en `src/` |
| 4 | Tests Unitarios | No | `tests/unit/test_*.py` |
| 5 | Tests de Integración | No | `tests/integration/test_*.py` |
| 6 | Validación BDD | No | Resultado de `pytest tests/features/` |
| 7 | Quality Gates | No | `quality/reports/{US_ID}-quality.json` |
| 8 | Documentación | Sí | Docstrings y comentarios en código |
| 9 | Reporte Final | No | `docs/reports/{US_ID}-report.md` |

Las fases 1 y 6 se saltan automáticamente si BDD no aplica (según la clasificación de la HU en Fase 0 o la opción `--skip-bdd`).

Para el detalle técnico de cada fase, ver los documentos individuales:
[Fase 0](phase-0.md) · [Fase 1](phase-1.md) · [Fase 2](phase-2.md) · [Fase 3](phase-3.md) · [Fase 4](phase-4.md) · [Fase 5](phase-5.md) · [Fase 6](phase-6.md) · [Fase 7](phase-7.md) · [Fase 8](phase-8.md) · [Fase 9](phase-9.md)

---

## Artefactos

Cada ejecución produce artefactos en rutas canónicas. Las rutas base se configuran en `documentation_config` dentro de `config.json`.

| Artefacto | Ruta canónica | Generado en |
|---|---|---|
| Contexto de ejecución | `docs/plans/{US_ID}-context.md` | Fase 0 |
| Escenarios BDD | `tests/features/{US_ID}.feature` | Fase 1 |
| Steps BDD | `tests/step_defs/{US_ID}_steps.py` | Fase 1 |
| Plan de implementación | `docs/plans/{US_ID}-plan.md` | Fase 2 |
| Código fuente | `src/` (estructura según perfil) | Fase 3 |
| Tests unitarios | `tests/unit/test_*.py` | Fase 4 |
| Tests de integración | `tests/integration/test_*.py` | Fase 5 |
| Reporte de calidad | `quality/reports/{US_ID}-quality.json` | Fase 7 |
| Reporte final | `docs/reports/{US_ID}-report.md` | Fase 9 |

---

## Configuración

La configuración vive en `.claude/skills/implement-us/config.json` dentro del proyecto destino.

### Variables principales

```json
{
  "variables": {
    "architecture_pattern": "mvc",
    "component_type": "Panel",
    "component_path": "app/presentacion/{name}/",
    "test_framework": "pytest",
    "product": "mi_app"
  }
}
```

### Quality Gates

Los umbrales se leen en Fase 0 y se registran en `context.md`. La Fase 7 los usa para validar.

```json
{
  "quality_gates": {
    "pylint":                 { "min_score": 8.0 },
    "cyclomatic_complexity":  { "max_per_function": 10 },
    "maintainability_index":  { "min_score": 20 },
    "coverage":               { "min_percent": 95.0 }
  }
}
```

Si no existe `.pylintrc` o `pytest.ini` en el proyecto, la Fase 0 los crea con valores por defecto tomados de `config.json`.

### Rutas de artefactos

```json
{
  "documentation_config": {
    "plan_path":   "docs/plans/",
    "report_path": "docs/reports/",
    "adr_path":    "docs/architecture/decisions/"
  },
  "test_framework_config": {
    "features_path":        "tests/features/",
    "steps_path":           "tests/step_defs/",
    "unit_test_path":       "tests/unit/",
    "integration_test_path":"tests/integration/"
  }
}
```

---

## Perfiles de Customización

Los perfiles sobrescriben valores de `config.json` para adaptarse al stack tecnológico del proyecto. Se definen en `.claude/skills/implement-us/customizations/`.

| Perfil | Stack | Archivo |
|---|---|---|
| `pyqt-mvc` | PyQt6 + MVC | `customizations/pyqt-mvc.json` |
| `fastapi-rest` | FastAPI + Layered | `customizations/fastapi-rest.json` |
| `flask-rest` | Flask REST + Layered | `customizations/flask-rest.json` |
| `flask-webapp` | Flask WebApp + BFF | `customizations/flask-webapp.json` |
| `generic-python` | Python genérico | `customizations/generic-python.json` |

El instalador fusiona `config.json` base + el perfil seleccionado al momento de instalar. Las claves del perfil tienen precedencia sobre la config base.

---

## Tracking de Tiempo

El skill integra tracking automático de tiempo. Cada fase registra su inicio y fin mediante directivas bash en el archivo de fase.

| Comando | Descripción |
|---|---|
| `/track-pause [razón]` | Pausar el tracking activo |
| `/track-resume` | Reanudar el tracking |
| `/track-status` | Ver estado actual y tiempo acumulado |
| `/track-report {US_ID}` | Generar reporte para la US |

El tracking acumula datos empíricos de performance del agente y no se compara con estimaciones humanas.

---

## Protocolo de Recuperación ante Fallas

Si una fase falla:

1. Leer el output completo del error sin asumir la causa
2. Identificar la fase donde se origina el problema
3. Aplicar la corrección en esa fase
4. Re-ejecutar la fase completa (no solo el paso que falló)
5. Verificar el checklist de salida antes de avanzar
6. Si después de 2 intentos autónomos la fase sigue fallando — informar al usuario y detener

Las fases de testing (4, 5, 6, 7) incluyen un árbol de decisión específico para clasificar el origen del fallo.

---

## Referencia Técnica

### Archivos del skill

```
.claude/skills/implement-us/
├── skill.md                   # Definición principal (entrada del skill)
├── config.json                # Configuración base
├── artifacts.md               # Contrato de artefactos del skill
├── conventions.md             # Convenciones globales de ejecución
├── phases/
│   ├── phase-0-validation.md
│   ├── phase-1-bdd.md
│   ├── phase-2-planning.md
│   ├── phase-3-implementation.md
│   ├── phase-4-unit-tests.md
│   ├── phase-5-integration-tests.md
│   ├── phase-6-bdd-validation.md
│   ├── phase-7-quality-gates.md
│   ├── phase-8-documentation.md
│   └── phase-9-final-report.md
├── templates/                 # Templates de artefactos
└── customizations/            # Perfiles por stack
```

### Flujo de datos entre fases

El archivo `docs/plans/{US_ID}-context.md` es la única fuente de verdad compartida entre fases. Se genera en Fase 0 y todas las fases siguientes lo leen como punto de partida. Evita dependencias de la memoria de conversación.

```
Fase 0 → genera context.md
Fase 1 → lee context.md → genera .feature
Fase 2 → lee context.md → genera plan.md
Fase 3 → lee plan.md    → genera src/
Fase 4 → lee plan.md    → genera tests/unit/
Fase 5 → lee plan.md    → genera tests/integration/
Fase 6 → lee context.md → ejecuta pytest features/
Fase 7 → lee context.md → ejecuta quality tools → genera quality.json
Fase 8 → lee plan.md    → documenta src/
Fase 9 → lee plan.md + quality.json → genera report.md
```

### Convenciones de ejecución

- El orden de los pasos dentro de cada fase es **estricto**.
- El **Paso 1 de cada fase es siempre imperativo** (`🔴`): iniciar tracking.
- Cada fase verifica que sus artefactos de entrada **existen en disco** antes de comenzar.
- Cada fase verifica que sus artefactos de salida **existen en disco** antes de cerrar.
- Las fases con `approval_required: true` incluyen un bloque STOP explícito antes de avanzar.

### Historial de versiones del skill

| Versión | Framework | Cambios principales |
|---|---|---|
| 2.1.0 | v1.3.0 | 24 discrepancias resueltas: umbrales desde config, rutas canónicas, instrucciones de templates, `steps_template` en Fase 6, mapeo quality.json en Fase 9 |
| 2.0.0 | v1.2.0 | 42 hallazgos corregidos: gates de entrada/salida, protocolo de recuperación, árbol de decisión de fallas, skip-bdd explícito |
| 1.0.0 | v1.0.0 | Versión inicial generalizada para 5 perfiles |
