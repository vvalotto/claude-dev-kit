# TICKET-059: Análisis y Setup de Testing 🔍

**Fase:** 8 - Testing del Framework
**Sprint:** 5
**Estado:** ✅ Completado
**Prioridad:** 🔴 Bloqueante (todos los demás tickets dependen de este)
**Estimación:** 0.5 horas
**Tiempo Real:** 0.25 horas
**Asignado a:** Claude Code

---

## 🎯 Objetivo

Analizar los módulos a testear, definir la estrategia de testing, crear la configuración de pytest y los fixtures compartidos en `conftest.py`.

---

## 📋 Tareas

### 1. Análisis de Módulos (10 min)

Para cada módulo, identificar:

- [ ] **`install/installer.py`**
  - Métodos públicos: `load_config`, `validate_profile`, `check_target_dir`, `copy_framework_files`, `merge_configs`, `generate_config_json`, `generate_claude_md`, `run_validation`, `install`
  - Dependencias externas: `shutil`, `yaml`, `json`, filesystem
  - Side effects: escritura en disco → usar `tmp_path`
  - Inputs que requieren mock: interacción de usuario (`input()`), `sys.exit()`

- [ ] **`tracking/time_tracker.py`**
  - Clases: `Task`, `Phase`, `Pause`, `TimeTracker`
  - Side effects: `TimeTracker.__init__` crea `.claude/tracking/` → monkeypatch `storage_path`
  - Properties a testear: `actual_minutes`, `variance_minutes`, `variance_percent`, `elapsed_minutes`, `duration_minutes`, `is_active`
  - Casos de error: `start_task` sin fase activa, `pause` con pausa activa, `resume` sin pausa

- [ ] **Config merge (parte de `installer.py`)**
  - `merge_configs()` — 4 perfiles × campos requeridos = casos cruzados
  - `generate_config_json()` — JSON generado válido
  - `generate_claude_md()` — Contenido correcto, no sobreescritura

### 2. Crear `pytest.ini` (5 min)

Archivo en la raíz del repositorio:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
```

### 3. Crear `tests/conftest.py` (15 min)

Fixtures compartidos:

- [ ] **`config_yaml_path`** — Retorna `Path` al `install/config.yaml` real
- [ ] **`kit_root`** — Retorna `Path` al directorio raíz del kit
- [ ] **`installer`** — Instancia de `ClaudeDevKitInstaller` con config real
- [ ] **`mock_project_dir`** — Directorio temporal vacío (usando `tmp_path`)
- [ ] **`tracker_in_tmp`** — `TimeTracker` con `storage_path` en `tmp_path` (via monkeypatch)
- [ ] **`sample_tracking_data`** — Dict con datos de tracking completos para tests de serialización

### 4. Verificar Dependencias (5 min)

- [ ] `pytest` instalado: `python -m pytest --version`
- [ ] `pytest-cov` instalado: `python -m pytest --co -q` (dry-run)
- [ ] Si faltan: documentar comando de instalación en el ticket

---

## 🎯 Criterios de Aceptación

- [ ] **`pytest.ini` creado** en raíz del repositorio
- [ ] **`tests/conftest.py` creado** con ≥ 5 fixtures funcionales
- [ ] **`pytest tests/` ejecuta sin errores** (aunque no haya tests aún)
- [ ] **Dependencias verificadas** — pytest y pytest-cov disponibles

---

## 📤 Output

1. `pytest.ini` — Configuración de pytest en raíz del repo
2. `tests/conftest.py` — Fixtures compartidos (~50 líneas)
3. Análisis documentado como comentario en este ticket (sección Resultado)

---

## 🔗 Dependencias

- **Depende de:** — (ninguno)
- **Bloquea a:** TICKET-060, TICKET-061, TICKET-062

---

## 📝 Notas Técnicas

### Estrategia de Aislamiento

El mayor desafío de estos tests es evitar side effects en el filesystem real:

**Para el instalador:**
```python
# ✅ Correcto: usar tmp_path de pytest
def test_generate_config_json(installer, tmp_path):
    installer.generate_config_json(tmp_path, "generic-python")
    config_file = tmp_path / "config.json"
    assert config_file.exists()

# ❌ Incorrecto: escribir en directorio real
def test_generate_config_json(installer):
    installer.generate_config_json(Path(".claude"), "generic-python")  # ¡Peligroso!
```

**Para el tracking:**
```python
# ✅ Correcto: monkeypatch storage_path
def test_start_tracking(tmp_path, monkeypatch):
    tracker = TimeTracker("US-001", "Test", 1, "prod")
    monkeypatch.setattr(tracker, "storage_path", tmp_path / "tracking.json")
    tracker.start_tracking()
    assert tracker.started_at is not None
```

### Herramientas

- **pytest** — Framework de testing
- **pytest-cov** — Cobertura de código
- **unittest.mock** — Mocking (stdlib, no requiere instalación)
- **tmp_path** — Fixture de pytest para directorio temporal

---

## ✅ Resultado

**Archivos Creados:**
- `pytest.ini` (raíz) — Configuración: testpaths=tests, -v --tb=short
- `tests/conftest.py` (~110 líneas) — 6 fixtures: config_yaml_path, kit_root, installer, mock_project_dir, tracker, started_tracker, tracker_with_phase, sample_tracking_data

**Dependencias Verificadas:**
- pytest 9.0.2 ✅
- pytest-cov 7.0.0 ✅
- pyyaml (instalado como dependencia del instalador) ✅

**Validación:**
- `pytest tests/ --co -q` → 1 test collected, 0 errors ✅
- conftest.py carga correctamente ✅

**Estado:** ✅ TICKET-059 COMPLETADO

---

**Creado:** 2026-02-17
**Bloqueante para:** TICKET-060, TICKET-061, TICKET-062
