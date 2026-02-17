# Sprint 5 - Fase 8: Testing del Framework

**Inicio:** 2026-02-17
**Duración:** 1 semana
**Estado:** ✅ Completado
**Fin:** 2026-02-17

---

## 🎯 Objetivo

Crear una **suite de tests automatizados** para los componentes internos del Claude Dev Kit, garantizando que el framework es correcto, confiable y mantenible.

Los tests cubren los **3 componentes core** del kit:
1. `install/installer.py` — El instalador multiplataforma
2. `tracking/time_tracker.py` — El sistema de tracking de tiempo
3. Config merge — La fusión de config base + perfil

> **Nota:** Los ejemplos (PyQt, FastAPI, Flask, CLI) ya tienen sus propias suites de tests validadas en Fase 7. Esta fase testea el **framework mismo**, no los proyectos generados.

---

## 📋 Alcance

### Módulos a Testear

#### 1. `install/installer.py` → `tests/test_installer.py`

**Clase `ClaudeDevKitInstaller`:**
- `load_config()` — Carga config.yaml válido e inválido
- `validate_profile()` — Valida perfiles conocidos y desconocidos
- `check_target_dir()` — Lógica de sobrescritura con force/no-force
- `copy_framework_files()` — Copia dirs/archivos, dry-run, fuente faltante
- `merge_configs()` — Fusión correcta para cada perfil
- `generate_config_json()` — JSON generado con campos correctos
- `generate_claude_md()` — Genera cuando no existe, no sobrescribe existente
- `run_validation()` — Retorna True en dry-run y sin script de validación
- `install()` — Flujo completo con dry-run

**Cobertura objetivo:** ≥ 90%
**Tests estimados:** ~23

#### 2. `tracking/time_tracker.py` → `tests/test_tracking.py`

**Modelos (dataclasses):**
- `Task` — Properties: actual_minutes, variance_minutes, variance_percent
- `Phase` — Properties: elapsed_minutes
- `Pause` — Properties: duration_minutes, is_active

**Clase `TimeTracker`:**
- `start_tracking()` / `end_tracking()` — Lifecycle completo
- `start_phase()` / `end_phase()` — Creación y finalización de fases
- `start_task()` / `end_task()` — Tareas dentro de fases, error sin fase activa
- `pause()` / `resume()` — Pausas, cálculo de duración, errores de estado
- `get_status()` — Estado: not_started, running, paused, con tareas
- `_to_dict()` — Serialización completa y correcta
- Persistencia JSON — Round-trip: save → load → verificar

**Cobertura objetivo:** ≥ 95%
**Tests estimados:** ~37

#### 3. `install/installer.py` (merge) → `tests/test_config_merge.py`

**Fusión de configuración por perfil:**
- `merge_configs("pyqt-mvc")` — architecture_pattern, test_framework, variables
- `merge_configs("fastapi-rest")` — Idem
- `merge_configs("django-mvt")` — Idem
- `merge_configs("generic-python")` — Idem
- Campos requeridos siempre presentes: version, profile, profile_name, installed_at
- `generate_config_json()` — JSON guardado es correcto y parseable
- `generate_claude_md()` — Contenido correcto por perfil

**Cobertura objetivo:** 100% del flujo de merge
**Tests estimados:** ~18

---

## 📊 Tickets

### Planificación y Setup
- [TICKET-059](tickets/TICKET-059-analisis-testing.md) — Análisis, setup pytest y conftest (0.5h) 🔴 Bloqueante

### Implementación de Tests
- [TICKET-060](tickets/TICKET-060-tests-instalador.md) — Tests del instalador (2h)
- [TICKET-061](tickets/TICKET-061-tests-tracking.md) — Tests del sistema de tracking (2.5h)
- [TICKET-062](tickets/TICKET-062-tests-config-merge.md) — Tests de fusión de configuración (1.5h)

### Validación
- [TICKET-063](tickets/TICKET-063-validacion-quality-gates.md) — Validación y quality gates (1h)

**Total:** 5 tickets | **~7.5 horas estimadas**

---

## ✅ Criterios de Éxito

### Por Módulo

- [x] **Todos los tests pasan** — 107/107 passed, 0 failures ✅
- [x] **Cobertura mínima alcanzada** — installer 99%, tracking 99% ✅
- [x] **Sin tests frágiles** — Sin timing, rutas absolutas ni estado global ✅
- [x] **Fixtures reutilizables** — conftest.py con 8 fixtures compartidos ✅

### Global

- [x] **Suite ejecutable** — `pytest tests/` → 107 passed in 7.31s ✅
- [x] **Pylint ≥ 8.0/10** — 8.75/10 en código de tests ✅
- [x] **Tests aislados** — `tmp_path` + `monkeypatch.chdir` ✅
- [x] **Informe de cobertura** — VALIDATION-REPORT.md generado ✅

---

## 📈 Progreso

| Ticket | Título | Estado | Estimado | Real |
|--------|--------|--------|----------|------|
| TICKET-059 | Análisis y setup | ✅ Completado | 0.5h | 0.25h |
| TICKET-060 | Tests instalador | ✅ Completado | 2h | 0.75h |
| TICKET-061 | Tests tracking | ✅ Completado | 2.5h | 0.5h |
| TICKET-062 | Tests config merge | ✅ Completado | 1.5h | 0.5h |
| TICKET-063 | Validación y QG | ✅ Completado | 1h | 0.25h |

**Total:** 5/5 completados (100%)

---

## 🎯 Entregable

```
tests/
├── conftest.py              # Fixtures compartidos (tmp_path, mock config, etc.)
├── test_installer.py        # ~23 tests del instalador
├── test_tracking.py         # ~37 tests del sistema de tracking
└── test_config_merge.py     # ~18 tests de config merge

pytest.ini                   # Configuración de pytest (en raíz del repo)
```

**Documentación:**
- `gestion/fase-8-testing/VALIDATION-REPORT.md` — Resultados reales de pytest + cobertura + pylint

---

## 📝 Notas

- Los tests usan `tmp_path` (fixture de pytest) para evitar side effects en el filesystem
- El módulo `tracking` crea `.claude/tracking/` al instanciar — los tests deben usar `tmp_path` y monkeypatch el `storage_path`
- El instalador usa `shutil.copytree` — los tests de copia deben tener fuentes reales o mocks
- Herramientas requeridas: `pytest`, `pytest-cov`, `unittest.mock` (stdlib)
- No se requieren dependencias adicionales — todo con Python stdlib + pytest

---

**Última actualización:** 2026-02-17
