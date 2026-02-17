# TICKET-062: Tests de Fusión de Configuración ⚙️

**Fase:** 8 - Testing del Framework
**Sprint:** 5
**Estado:** ⏳ Pendiente
**Prioridad:** Alta
**Estimación:** 1.5 horas
**Asignado a:** Claude Code

---

## 🎯 Objetivo

Crear `tests/test_config_merge.py` con cobertura completa del proceso de fusión de configuración: `merge_configs()`, `generate_config_json()` y `generate_claude_md()` para los 4 perfiles soportados.

Este ticket verifica que **cada perfil genera la configuración exactamente correcta**, separando estos tests de los tests de flujo del instalador (TICKET-060).

---

## 📋 Casos de Test

### Método: `merge_configs` — Campos comunes

| # | Test | Caso | Resultado Esperado |
|---|------|------|--------------------|
| 1 | `test_merge_has_required_keys` | Cualquier perfil | Dict tiene: version, profile, profile_name, installed_at, architecture_pattern, test_framework, component_types, patterns, variables |
| 2 | `test_merge_profile_name_matches` | "pyqt-mvc" | profile == "pyqt-mvc" |
| 3 | `test_merge_installed_at_is_iso` | Cualquier perfil | installed_at parseable como datetime ISO 8601 |

### Método: `merge_configs` — Perfil `pyqt-mvc`

| # | Test | Caso | Resultado Esperado |
|---|------|------|--------------------|
| 4 | `test_merge_pyqt_architecture` | merge_configs("pyqt-mvc") | architecture_pattern == "mvc" |
| 5 | `test_merge_pyqt_test_framework` | merge_configs("pyqt-mvc") | test_framework == "pytest-qt" |
| 6 | `test_merge_pyqt_component_types` | merge_configs("pyqt-mvc") | component_types contiene "Panel", "Model", "Controller" |
| 7 | `test_merge_pyqt_variables` | merge_configs("pyqt-mvc") | variables["base_class"] == "ModeloBase" |

### Método: `merge_configs` — Perfil `fastapi-rest`

| # | Test | Caso | Resultado Esperado |
|---|------|------|--------------------|
| 8 | `test_merge_fastapi_architecture` | merge_configs("fastapi-rest") | architecture_pattern == "layered" |
| 9 | `test_merge_fastapi_test_framework` | merge_configs("fastapi-rest") | test_framework == "pytest" |
| 10 | `test_merge_fastapi_component_types` | merge_configs("fastapi-rest") | component_types contiene "Router", "Service", "Repository" |
| 11 | `test_merge_fastapi_variables` | merge_configs("fastapi-rest") | variables["base_class"] == "BaseModel" |

### Método: `merge_configs` — Perfil `django-mvt`

| # | Test | Caso | Resultado Esperado |
|---|------|------|--------------------|
| 12 | `test_merge_django_architecture` | merge_configs("django-mvt") | architecture_pattern == "mvt" |
| 13 | `test_merge_django_test_framework` | merge_configs("django-mvt") | test_framework == "pytest-django" |
| 14 | `test_merge_django_component_types` | merge_configs("django-mvt") | component_types contiene "Model", "View", "Template" |

### Método: `merge_configs` — Perfil `generic-python`

| # | Test | Caso | Resultado Esperado |
|---|------|------|--------------------|
| 15 | `test_merge_generic_architecture` | merge_configs("generic-python") | architecture_pattern == "modular" |
| 16 | `test_merge_generic_test_framework` | merge_configs("generic-python") | test_framework == "pytest" |
| 17 | `test_merge_generic_component_types` | merge_configs("generic-python") | component_types contiene "Module", "Class", "Function" |

### Método: `generate_config_json` — Contenido del JSON

| # | Test | Caso | Resultado Esperado |
|---|------|------|--------------------|
| 18 | `test_config_json_is_valid_json` | generate_config_json con perfil válido | Archivo parseable con `json.loads()` |
| 19 | `test_config_json_has_profile_key` | generate_config_json("fastapi-rest") | json["profile"] == "fastapi-rest" |
| 20 | `test_config_json_has_version` | generate_config_json(any) | json["version"] existe y no está vacío |

### Método: `generate_claude_md` — Contenido por perfil

| # | Test | Caso | Resultado Esperado |
|---|------|------|--------------------|
| 21 | `test_claude_md_contains_profile_name` | generate_claude_md("pyqt-mvc") | Contenido incluye "PyQt + MVC" |
| 22 | `test_claude_md_contains_architecture` | generate_claude_md("fastapi-rest") | Contenido incluye "layered" |
| 23 | `test_claude_md_contains_test_framework` | generate_claude_md("pyqt-mvc") | Contenido incluye "pytest-qt" |
| 24 | `test_claude_md_contains_skill_section` | Cualquier perfil | Contenido incluye "/implement-us" |
| 25 | `test_claude_md_does_not_overwrite` | Archivo ya existe con contenido X | Contenido sigue siendo X |

**Total: 25 tests**

---

## 📋 Estructura del Archivo

```python
# tests/test_config_merge.py
"""
Tests de fusión de configuración (merge_configs, generate_config_json, generate_claude_md)

Verifica que cada perfil genera la configuración correcta al instalar.
"""
import json
import pytest
from datetime import datetime
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'install'))
from installer import ClaudeDevKitInstaller


# ─────────────────────────────────────────────
# Tests: merge_configs - campos comunes
# ─────────────────────────────────────────────
class TestMergeConfigsCommon:
    def test_merge_has_required_keys(self, installer): ...
    def test_merge_profile_name_matches(self, installer): ...
    def test_merge_installed_at_is_iso(self, installer): ...


# ─────────────────────────────────────────────
# Tests: merge_configs - por perfil
# ─────────────────────────────────────────────
class TestMergeConfigsPyQt:
    def test_merge_pyqt_architecture(self, installer): ...
    # ...

class TestMergeConfigsFastAPI:
    def test_merge_fastapi_architecture(self, installer): ...
    # ...

class TestMergeConfigsDjango:
    def test_merge_django_architecture(self, installer): ...
    # ...

class TestMergeConfigsGeneric:
    def test_merge_generic_architecture(self, installer): ...
    # ...


# ─────────────────────────────────────────────
# Tests: generate_config_json
# ─────────────────────────────────────────────
class TestGenerateConfigJson:
    def test_config_json_is_valid_json(self, installer, tmp_path): ...
    def test_config_json_has_profile_key(self, installer, tmp_path): ...
    def test_config_json_has_version(self, installer, tmp_path): ...


# ─────────────────────────────────────────────
# Tests: generate_claude_md
# ─────────────────────────────────────────────
class TestGenerateClaudeMd:
    def test_claude_md_contains_profile_name(self, installer, tmp_path): ...
    def test_claude_md_does_not_overwrite(self, installer, tmp_path): ...
```

---

## 🎯 Criterios de Aceptación

- [ ] **25 tests implementados** — Todos los casos de la tabla cubiertos
- [ ] **Todos los tests pasan** — `pytest tests/test_config_merge.py` → 25 passed
- [ ] **Los 4 perfiles verificados** — pyqt-mvc, fastapi-rest, django-mvt, generic-python
- [ ] **Sin side effects** — Todos usan `tmp_path`

---

## 📤 Output

1. `tests/test_config_merge.py` — Suite de tests (~200 líneas)

---

## 🔗 Dependencias

- **Depende de:** TICKET-059 (conftest.py con fixtures base)
- **Bloquea a:** TICKET-063 (validación final)

---

## 📝 Notas Técnicas

### Patrón de test para `generate_config_json`

```python
def test_config_json_has_profile_key(self, installer, tmp_path):
    target_dir = tmp_path / ".claude"
    target_dir.mkdir()
    installer.generate_config_json(target_dir, "fastapi-rest")
    config_file = target_dir / "config.json"
    with open(config_file) as f:
        data = json.load(f)
    assert data["profile"] == "fastapi-rest"
```

### Patrón de test para `generate_claude_md` — no sobreescribe

```python
def test_claude_md_does_not_overwrite(self, installer, tmp_path):
    claude_md = tmp_path / "CLAUDE.md"
    original_content = "# Mi CLAUDE.md original"
    claude_md.write_text(original_content)
    installer.generate_claude_md(tmp_path, "pyqt-mvc")
    assert claude_md.read_text() == original_content
```

---

## ✅ Resultado

_Se completará cuando el ticket esté DONE_

**Estado:** ✅ Completado

## ✅ Resultado

- **31 tests implementados** (6 extras cubriendo flask-rest, flask-webapp — django-mvt eliminado)
- **31/31 passed** — `pytest tests/test_config_merge.py` ✅
- **Sin side effects** — todos usan `tmp_path` ✅
- **Tiempo:** 0.50s ✅
- **Nota:** El ticket referenciaba django-mvt (eliminado en esta sesión). Tests actualizados con los 5 perfiles reales.

---

**Creado:** 2026-02-17
**Completado:** 2026-02-17
**Depende de:** TICKET-059
**Bloquea a:** TICKET-063
