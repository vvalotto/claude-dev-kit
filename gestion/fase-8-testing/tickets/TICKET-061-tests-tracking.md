# TICKET-061: Tests del Sistema de Tracking ⏱️

**Fase:** 8 - Testing del Framework
**Sprint:** 5
**Estado:** ⏳ Pendiente
**Prioridad:** Alta
**Estimación:** 2.5 horas
**Asignado a:** Claude Code

---

## 🎯 Objetivo

Crear `tests/test_tracking.py` con cobertura completa de los modelos y la clase `TimeTracker` en `tracking/time_tracker.py`.

**Cobertura objetivo: ≥ 95%** (requerimiento del CLAUDE.md)

---

## 📋 Casos de Test

### Clase: `Task` (dataclass + properties)

| # | Test | Caso | Resultado Esperado |
|---|------|------|--------------------|
| 1 | `test_task_actual_minutes` | elapsed_seconds=120 | actual_minutes == 2.0 |
| 2 | `test_task_actual_minutes_zero` | elapsed_seconds=0 | actual_minutes == 0.0 |
| 3 | `test_task_variance_minutes_positive` | actual=10min, estimated=8min | variance_minutes == 2.0 |
| 4 | `test_task_variance_minutes_negative` | actual=5min, estimated=8min | variance_minutes == -3.0 |
| 5 | `test_task_variance_percent` | variance=2min, estimated=8min | variance_percent == 25.0 |
| 6 | `test_task_variance_percent_zero_estimated` | estimated=0 | variance_percent == 0.0 (no division by zero) |

### Clase: `Phase` (dataclass + property)

| # | Test | Caso | Resultado Esperado |
|---|------|------|--------------------|
| 7 | `test_phase_elapsed_minutes` | elapsed_seconds=300 | elapsed_minutes == 5.0 |
| 8 | `test_phase_default_values` | Phase(0, "nombre") | status="pending", tasks=[], auto_approved=True |

### Clase: `Pause` (dataclass + properties)

| # | Test | Caso | Resultado Esperado |
|---|------|------|--------------------|
| 9 | `test_pause_duration_minutes` | duration_seconds=90 | duration_minutes == 1.5 |
| 10 | `test_pause_is_active_true` | resumed_at=None | is_active == True |
| 11 | `test_pause_is_active_false` | resumed_at set | is_active == False |

### Clase: `TimeTracker` — Lifecycle

| # | Test | Caso | Resultado Esperado |
|---|------|------|--------------------|
| 12 | `test_start_tracking_sets_timestamp` | Llama start_tracking() | started_at is not None |
| 13 | `test_start_tracking_saves_json` | Llama start_tracking() | storage_path existe |
| 14 | `test_end_tracking_sets_timestamp` | start + end | completed_at is not None |

### Clase: `TimeTracker` — Fases

| # | Test | Caso | Resultado Esperado |
|---|------|------|--------------------|
| 15 | `test_start_phase_creates_phase` | start_phase(0, "Test") | phases tiene 1 elemento |
| 16 | `test_start_phase_sets_current` | start_phase(0, "Test") | current_phase.phase_number == 0 |
| 17 | `test_end_phase_completes_phase` | start + end_phase(0) | phases[0].status == "completed" |
| 18 | `test_end_phase_clears_current` | start + end_phase(0) | current_phase is None |
| 19 | `test_end_phase_calculates_elapsed` | start + sleep + end | elapsed_seconds > 0 |

### Clase: `TimeTracker` — Tareas

| # | Test | Caso | Resultado Esperado |
|---|------|------|--------------------|
| 20 | `test_start_task_creates_task` | Fase activa + start_task | current_phase.tasks tiene 1 tarea |
| 21 | `test_start_task_sets_current` | Fase activa + start_task | current_task.task_id correcto |
| 22 | `test_start_task_no_phase_raises` | Sin fase activa | Lanza `ValueError` |
| 23 | `test_end_task_completes_task` | start + end_task | task.status == "completed" |
| 24 | `test_end_task_with_file_created` | end_task(file_created="x.py") | task.file_created == "x.py" |
| 25 | `test_end_task_clears_current` | start + end_task | current_task is None |

### Clase: `TimeTracker` — Pausas

| # | Test | Caso | Resultado Esperado |
|---|------|------|--------------------|
| 26 | `test_pause_creates_pause` | pause("razón") | pauses tiene 1 elemento |
| 27 | `test_pause_sets_current_pause` | pause() | current_pause is not None |
| 28 | `test_pause_with_reason` | pause("almuerzo") | pause.reason == "almuerzo" |
| 29 | `test_pause_double_raises` | pause() + pause() | Lanza `ValueError` |
| 30 | `test_resume_clears_pause` | pause + resume | current_pause is None |
| 31 | `test_resume_calculates_duration` | pause + resume | pauses[0].duration_seconds > 0 |
| 32 | `test_resume_without_pause_raises` | resume() sin pausa activa | Lanza `ValueError` |

### Clase: `TimeTracker` — get_status

| # | Test | Caso | Resultado Esperado |
|---|------|------|--------------------|
| 33 | `test_get_status_not_started` | Sin start_tracking | status == "not_started" |
| 34 | `test_get_status_running` | start_tracking() | status == "running" |
| 35 | `test_get_status_paused` | start + pause | status == "paused" |
| 36 | `test_get_status_with_tasks` | fases + tareas completadas | completed_tasks correcto |

### Persistencia JSON

| # | Test | Caso | Resultado Esperado |
|---|------|------|--------------------|
| 37 | `test_to_dict_complete_structure` | Tracker con datos completos | Dict tiene claves: metadata, timeline, phases, pauses, summary |

**Total: 37 tests**

---

## 📋 Estructura del Archivo

```python
# tests/test_tracking.py
"""
Tests del módulo tracking/time_tracker.py

Cubre: Task, Phase, Pause (dataclasses + properties)
       TimeTracker (lifecycle, fases, tareas, pausas, persistencia)
"""
import pytest
from datetime import datetime, timezone
from pathlib import Path
from tracking.time_tracker import Task, Phase, Pause, TimeTracker


# ─────────────────────────────────────────────
# Fixture: tracker aislado en tmp_path
# ─────────────────────────────────────────────
@pytest.fixture
def tracker(tmp_path, monkeypatch):
    """TimeTracker con storage_path en directorio temporal."""
    t = TimeTracker("US-TEST", "Test US", 1, "test_prod")
    monkeypatch.setattr(t, 'storage_path', tmp_path / 'tracking.json')
    return t


# ─────────────────────────────────────────────
# Tests: Task
# ─────────────────────────────────────────────
class TestTask:
    def test_task_actual_minutes(self): ...
    # ...

class TestPhase:
    def test_phase_elapsed_minutes(self): ...
    # ...

class TestPause:
    def test_pause_is_active(self): ...
    # ...

class TestTimeTrackerLifecycle:
    def test_start_tracking_sets_timestamp(self, tracker): ...
    # ...

class TestTimeTrackerPhases:
    def test_start_phase_creates_phase(self, tracker): ...
    # ...

class TestTimeTrackerTasks:
    def test_start_task_creates_task(self, tracker): ...
    # ...

class TestTimeTrackerPauses:
    def test_pause_creates_pause(self, tracker): ...
    # ...

class TestTimeTrackerStatus:
    def test_get_status_not_started(self, tracker): ...
    # ...

class TestTimeTrackerPersistence:
    def test_to_dict_complete_structure(self, tracker): ...
```

---

## 🎯 Criterios de Aceptación

- [ ] **37 tests implementados** — Todos los casos de la tabla cubiertos
- [ ] **Todos los tests pasan** — `pytest tests/test_tracking.py` → 37 passed
- [ ] **Cobertura ≥ 95%** — `pytest --cov=tracking tests/test_tracking.py`
- [ ] **Sin side effects** — Ningún test escribe en `.claude/tracking/` real
- [ ] **Tests rápidos** — Suite completa ejecuta en < 2 segundos (no usar `time.sleep`)

---

## 📤 Output

1. `tests/test_tracking.py` — Suite de tests (~300-350 líneas)

---

## 🔗 Dependencias

- **Depende de:** TICKET-059 (conftest.py con fixtures base)
- **Bloquea a:** TICKET-063 (validación final)

---

## 📝 Notas Técnicas

### Problema: `TimeTracker.__init__` crea `.claude/tracking/`

El constructor llama a `self.storage_path.parent.mkdir(parents=True, exist_ok=True)`.
Esto crea el directorio real. Solución:

```python
@pytest.fixture
def tracker(tmp_path, monkeypatch):
    # Monkeypatch ANTES de que __init__ use storage_path
    # No funciona - __init__ ya ejecutó el mkdir
    # Solución: patch Path.mkdir durante la construcción
    with patch.object(Path, 'mkdir'):
        t = TimeTracker("US-TEST", "Test", 1, "prod")
    t.storage_path = tmp_path / "tracking.json"
    return t
```

O alternativamente, crear el tracker con `tmp_path` como directorio de trabajo:
```python
@pytest.fixture
def tracker(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)  # Cambia cwd a tmp_path
    t = TimeTracker("US-TEST", "Test US", 1, "prod")
    return t
```
Con `monkeypatch.chdir`, el `.claude/tracking/` se crea dentro de `tmp_path`.

### Tests sin sleep real

Para verificar `elapsed_seconds > 0` sin esperar:
```python
from unittest.mock import patch
from datetime import datetime, timezone, timedelta

def test_end_phase_calculates_elapsed(self, tracker):
    tracker.start_tracking()
    tracker.start_phase(0, "Test")
    # Simular que pasó tiempo modificando started_at
    tracker.current_phase.started_at = datetime.now(timezone.utc) - timedelta(seconds=5)
    tracker.end_phase(0)
    assert tracker.phases[0].elapsed_seconds >= 5
```

---

## ✅ Resultado

_Se completará cuando el ticket esté DONE_

**Estado:** ⏳ Pendiente

---

**Creado:** 2026-02-17
**Depende de:** TICKET-059
**Bloquea a:** TICKET-063
