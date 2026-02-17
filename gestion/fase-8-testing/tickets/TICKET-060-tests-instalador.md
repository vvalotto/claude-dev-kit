# TICKET-060: Tests del Instalador 🔧

**Fase:** 8 - Testing del Framework
**Sprint:** 5
**Estado:** ⏳ Pendiente
**Prioridad:** Alta
**Estimación:** 2 horas
**Asignado a:** Claude Code

---

## 🎯 Objetivo

Crear `tests/test_installer.py` con cobertura completa de la clase `ClaudeDevKitInstaller` en `install/installer.py`.

---

## 📋 Casos de Test

### Clase: `ClaudeDevKitInstaller.__init__` + `load_config`

| # | Test | Caso | Resultado Esperado |
|---|------|------|--------------------|
| 1 | `test_load_config_valid` | config.yaml real existe | Retorna dict con claves 'profiles', 'installation', 'messages' |
| 2 | `test_load_config_missing_file` | Path inexistente | Lanza `FileNotFoundError` |
| 3 | `test_load_config_invalid_yaml` | Archivo YAML inválido | Lanza `yaml.YAMLError` |

### Método: `validate_profile`

| # | Test | Caso | Resultado Esperado |
|---|------|------|--------------------|
| 4 | `test_validate_profile_valid` | "pyqt-mvc" (existe) | Retorna `True` |
| 5 | `test_validate_profile_invalid` | "nonexistent-profile" | Retorna `False` |
| 6 | `test_validate_profile_all_profiles` | 4 perfiles del config | Todos retornan `True` |

### Método: `check_target_dir`

| # | Test | Caso | Resultado Esperado |
|---|------|------|--------------------|
| 7 | `test_check_target_dir_not_exists` | Directorio no existe | Retorna `True` |
| 8 | `test_check_target_dir_exists_force` | Existe + force=True | Retorna `True` |
| 9 | `test_check_target_dir_exists_no_force` | Existe + force=False + user dice "s" | Retorna `True` (mock input) |
| 10 | `test_check_target_dir_exists_denied` | Existe + force=False + user dice "n" | Retorna `False` |

### Método: `copy_framework_files`

| # | Test | Caso | Resultado Esperado |
|---|------|------|--------------------|
| 11 | `test_copy_framework_files_dry_run` | dry_run=True | No crea archivos, no lanza error |
| 12 | `test_copy_framework_files_copies_dirs` | Fuentes existen | Directorios copiados en target |
| 13 | `test_copy_framework_files_missing_source` | Fuente no existe | Log warning, continúa sin error |

### Método: `generate_config_json`

| # | Test | Caso | Resultado Esperado |
|---|------|------|--------------------|
| 14 | `test_generate_config_json_creates_file` | dry_run=False | Archivo config.json creado |
| 15 | `test_generate_config_json_dry_run` | dry_run=True | No crea archivo |
| 16 | `test_generate_config_json_valid_json` | Ejecuta generate | JSON parseable con claves requeridas |

### Método: `generate_claude_md`

| # | Test | Caso | Resultado Esperado |
|---|------|------|--------------------|
| 17 | `test_generate_claude_md_creates_when_missing` | CLAUDE.md no existe | Crea archivo con contenido del perfil |
| 18 | `test_generate_claude_md_skips_existing` | CLAUDE.md ya existe | No sobreescribe, log info |
| 19 | `test_generate_claude_md_dry_run` | dry_run=True | No crea archivo |

### Método: `run_validation`

| # | Test | Caso | Resultado Esperado |
|---|------|------|--------------------|
| 20 | `test_run_validation_dry_run` | dry_run=True | Retorna `True`, no ejecuta script |
| 21 | `test_run_validation_script_missing` | Script no existe | Retorna `True` (warning, no error) |

### Método: `install` (integración)

| # | Test | Caso | Resultado Esperado |
|---|------|------|--------------------|
| 22 | `test_install_dry_run_success` | dry_run=True, perfil válido | Retorna `True`, no modifica filesystem |
| 23 | `test_install_invalid_profile` | Perfil inválido | Retorna `False` |

**Total: 23 tests**

---

## 📋 Estructura del Archivo

```python
# tests/test_installer.py
"""
Tests del módulo install/installer.py

Cubre: ClaudeDevKitInstaller - load_config, validate_profile,
check_target_dir, copy_framework_files, generate_config_json,
generate_claude_md, run_validation, install
"""
import json
import pytest
import yaml
from pathlib import Path
from unittest.mock import patch, MagicMock

# Importar desde install/
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'install'))
from installer import ClaudeDevKitInstaller


# ─────────────────────────────────────────────
# Tests: load_config
# ─────────────────────────────────────────────
class TestLoadConfig:
    def test_load_config_valid(self, installer): ...
    def test_load_config_missing_file(self, kit_root, tmp_path): ...
    def test_load_config_invalid_yaml(self, kit_root, tmp_path): ...


# ─────────────────────────────────────────────
# Tests: validate_profile
# ─────────────────────────────────────────────
class TestValidateProfile:
    def test_validate_profile_valid(self, installer): ...
    def test_validate_profile_invalid(self, installer): ...
    def test_validate_profile_all_profiles(self, installer): ...


# ... (demás clases)
```

---

## 🎯 Criterios de Aceptación

- [ ] **23 tests implementados** — Todos los casos de la tabla cubiertos
- [ ] **Todos los tests pasan** — `pytest tests/test_installer.py` → 23 passed
- [ ] **Cobertura ≥ 90%** — `pytest --cov=install tests/test_installer.py`
- [ ] **Sin side effects** — Todos los tests usan `tmp_path`, no tocan el filesystem real
- [ ] **Pylint ≥ 8.0** — En el archivo de tests

---

## 📤 Output

1. `tests/test_installer.py` — Suite de tests (~200-250 líneas)

---

## 🔗 Dependencias

- **Depende de:** TICKET-059 (conftest.py con fixtures base)
- **Bloquea a:** TICKET-063 (validación final)

---

## 📝 Notas Técnicas

### Import del instalador

El instalador está en `install/installer.py`, no en el root. Usar:
```python
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'install'))
from installer import ClaudeDevKitInstaller
```

### Mock de `input()` para `check_target_dir`

```python
with patch('builtins.input', return_value='s'):
    result = installer.check_target_dir(existing_dir, force=False)
assert result is True
```

### Test de `copy_framework_files` con fuentes reales

El kit_root real tiene los directorios `skills/`, `templates/`, `tracking/`.
Se puede copiar a `tmp_path` sin problemas:
```python
def test_copy_framework_files_copies_dirs(installer, tmp_path):
    installer.copy_framework_files(tmp_path, dry_run=False)
    assert (tmp_path / 'skills').exists()
```

---

## ✅ Resultado

_Se completará cuando el ticket esté DONE_

**Estado:** ⏳ Pendiente

---

**Creado:** 2026-02-17
**Depende de:** TICKET-059
**Bloquea a:** TICKET-063
