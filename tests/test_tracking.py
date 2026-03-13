"""
Tests del módulo tracking/time_tracker.py

Cubre: Task, Phase, Pause (dataclasses + properties)
       TimeTracker (lifecycle, fases, tareas, pausas, persistencia)
"""
import json
import pytest
from datetime import datetime, timezone, timedelta
from pathlib import Path

from tracking.time_tracker import Task, Phase, Pause, TimeTracker


# ─────────────────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture
def tracker(tmp_path, monkeypatch):
    """TimeTracker aislado: crea .claude/tracking/ dentro de tmp_path."""
    monkeypatch.chdir(tmp_path)
    return TimeTracker("US-TEST", "Test US Title", 3, "test_prod")


@pytest.fixture
def started_tracker(tracker):
    """Tracker con start_tracking() ya llamado."""
    tracker.start_tracking()
    return tracker


@pytest.fixture
def tracker_with_phase(started_tracker):
    """Tracker con una fase activa."""
    started_tracker.start_phase(0, "Fase de Prueba")
    return started_tracker


# ─────────────────────────────────────────────────────────────────────────────
# Tests: Task
# ─────────────────────────────────────────────────────────────────────────────

class TestTask:
    def test_task_actual_minutes(self):
        task = Task("t1", "Nombre", "tipo", 10.0, elapsed_seconds=120)
        assert task.actual_minutes == 2.0

    def test_task_actual_minutes_zero(self):
        task = Task("t1", "Nombre", "tipo", 10.0, elapsed_seconds=0)
        assert task.actual_minutes == 0.0

    def test_task_variance_minutes_positive(self):
        # actual=10min, estimated=8min → varianza=+2min
        task = Task("t1", "Nombre", "tipo", 8.0, elapsed_seconds=600)
        assert task.variance_minutes == pytest.approx(2.0)

    def test_task_variance_minutes_negative(self):
        # actual=5min, estimated=8min → varianza=-3min
        task = Task("t1", "Nombre", "tipo", 8.0, elapsed_seconds=300)
        assert task.variance_minutes == pytest.approx(-3.0)

    def test_task_variance_percent(self):
        # actual=10min, estimated=8min → varianza%=25%
        task = Task("t1", "Nombre", "tipo", 8.0, elapsed_seconds=600)
        assert task.variance_percent == pytest.approx(25.0)

    def test_task_variance_percent_zero_estimated(self):
        # No división por cero cuando estimated=0
        task = Task("t1", "Nombre", "tipo", 0.0, elapsed_seconds=120)
        assert task.variance_percent == 0.0


# ─────────────────────────────────────────────────────────────────────────────
# Tests: Phase
# ─────────────────────────────────────────────────────────────────────────────

class TestPhase:
    def test_phase_elapsed_minutes(self):
        phase = Phase(0, "Nombre", elapsed_seconds=300)
        assert phase.elapsed_minutes == 5.0

    def test_phase_default_values(self):
        phase = Phase(0, "Nombre")
        assert phase.status == "pending"
        assert phase.tasks == []
        assert phase.auto_approved is True


# ─────────────────────────────────────────────────────────────────────────────
# Tests: Pause
# ─────────────────────────────────────────────────────────────────────────────

class TestPause:
    def test_pause_duration_minutes(self):
        pause = Pause("p1", datetime.now(timezone.utc), duration_seconds=90)
        assert pause.duration_minutes == 1.5

    def test_pause_is_active_true(self):
        pause = Pause("p1", datetime.now(timezone.utc), resumed_at=None)
        assert pause.is_active is True

    def test_pause_is_active_false(self):
        now = datetime.now(timezone.utc)
        pause = Pause("p1", now, resumed_at=now)
        assert pause.is_active is False


# ─────────────────────────────────────────────────────────────────────────────
# Tests: TimeTracker — Lifecycle
# ─────────────────────────────────────────────────────────────────────────────

class TestTimeTrackerLifecycle:
    def test_start_tracking_sets_timestamp(self, tracker):
        assert tracker.started_at is None
        tracker.start_tracking()
        assert tracker.started_at is not None

    def test_start_tracking_saves_json(self, tracker):
        tracker.start_tracking()
        assert tracker.storage_path.exists()

    def test_end_tracking_sets_timestamp(self, tracker):
        tracker.start_tracking()
        assert tracker.completed_at is None
        tracker.end_tracking()
        assert tracker.completed_at is not None


# ─────────────────────────────────────────────────────────────────────────────
# Tests: TimeTracker — from_json
# ─────────────────────────────────────────────────────────────────────────────

class TestTimeTrackerFromJson:
    def test_from_json_restores_metadata(self, tracker_with_phase):
        path = tracker_with_phase.storage_path
        restored = TimeTracker.from_json(path)
        assert restored.us_id == tracker_with_phase.us_id
        assert restored.us_title == tracker_with_phase.us_title
        assert restored.us_points == tracker_with_phase.us_points
        assert restored.producto == tracker_with_phase.producto

    def test_from_json_restores_started_at(self, started_tracker):
        path = started_tracker.storage_path
        restored = TimeTracker.from_json(path)
        assert restored.started_at is not None

    def test_from_json_restores_phases(self, tracker_with_phase):
        path = tracker_with_phase.storage_path
        restored = TimeTracker.from_json(path)
        assert len(restored.phases) == 1
        assert restored.phases[0].phase_number == 0

    def test_from_json_restores_current_phase(self, tracker_with_phase):
        path = tracker_with_phase.storage_path
        restored = TimeTracker.from_json(path)
        assert restored.current_phase is not None
        assert restored.current_phase.phase_number == 0

    def test_from_json_can_continue_phase(self, tracker_with_phase):
        """Tracker restaurado permite cerrar la fase activa."""
        path = tracker_with_phase.storage_path
        restored = TimeTracker.from_json(path)
        restored.end_phase(0)
        assert restored.phases[0].status == "completed"

    def test_from_json_completed_tracking(self, started_tracker):
        started_tracker.end_tracking()
        path = started_tracker.storage_path
        restored = TimeTracker.from_json(path)
        assert restored.completed_at is not None


# ─────────────────────────────────────────────────────────────────────────────
# Tests: TimeTracker — Fases
# ─────────────────────────────────────────────────────────────────────────────

class TestTimeTrackerPhases:
    def test_start_phase_creates_phase(self, started_tracker):
        started_tracker.start_phase(0, "Fase 0")
        assert len(started_tracker.phases) == 1

    def test_start_phase_sets_current(self, started_tracker):
        started_tracker.start_phase(0, "Fase 0")
        assert started_tracker.current_phase is not None
        assert started_tracker.current_phase.phase_number == 0

    def test_end_phase_completes_phase(self, started_tracker):
        started_tracker.start_phase(0, "Fase 0")
        started_tracker.end_phase(0)
        assert started_tracker.phases[0].status == "completed"

    def test_end_phase_clears_current(self, started_tracker):
        started_tracker.start_phase(0, "Fase 0")
        started_tracker.end_phase(0)
        assert started_tracker.current_phase is None

    def test_end_phase_calculates_elapsed(self, started_tracker):
        started_tracker.start_phase(0, "Fase 0")
        # Simular que pasó tiempo
        started_tracker.current_phase.started_at = (
            datetime.now(timezone.utc) - timedelta(seconds=5)
        )
        started_tracker.end_phase(0)
        assert started_tracker.phases[0].elapsed_seconds >= 5


# ─────────────────────────────────────────────────────────────────────────────
# Tests: TimeTracker — Tareas
# ─────────────────────────────────────────────────────────────────────────────

class TestTimeTrackerTasks:
    def test_start_task_creates_task(self, tracker_with_phase):
        tracker_with_phase.start_task("t1", "Tarea 1", "modelo", 5.0)
        assert len(tracker_with_phase.current_phase.tasks) == 1

    def test_start_task_sets_current(self, tracker_with_phase):
        tracker_with_phase.start_task("t1", "Tarea 1", "modelo", 5.0)
        assert tracker_with_phase.current_task is not None
        assert tracker_with_phase.current_task.task_id == "t1"

    def test_start_task_no_phase_raises(self, started_tracker):
        with pytest.raises(ValueError, match="No hay fase activa"):
            started_tracker.start_task("t1", "Tarea 1", "modelo", 5.0)

    def test_end_task_completes_task(self, tracker_with_phase):
        tracker_with_phase.start_task("t1", "Tarea 1", "modelo", 5.0)
        tracker_with_phase.end_task("t1")
        assert tracker_with_phase.current_phase.tasks[0].status == "completed"

    def test_end_task_with_file_created(self, tracker_with_phase):
        tracker_with_phase.start_task("t1", "Tarea 1", "modelo", 5.0)
        tracker_with_phase.end_task("t1", file_created="app/modelo.py")
        assert tracker_with_phase.current_phase.tasks[0].file_created == "app/modelo.py"

    def test_end_task_clears_current(self, tracker_with_phase):
        tracker_with_phase.start_task("t1", "Tarea 1", "modelo", 5.0)
        tracker_with_phase.end_task("t1")
        assert tracker_with_phase.current_task is None


# ─────────────────────────────────────────────────────────────────────────────
# Tests: TimeTracker — Pausas
# ─────────────────────────────────────────────────────────────────────────────

class TestTimeTrackerPauses:
    def test_pause_creates_pause(self, started_tracker):
        started_tracker.pause("almuerzo")
        assert len(started_tracker.pauses) == 1

    def test_pause_sets_current_pause(self, started_tracker):
        started_tracker.pause()
        assert started_tracker.current_pause is not None

    def test_pause_with_reason(self, started_tracker):
        started_tracker.pause("reunión")
        assert started_tracker.pauses[0].reason == "reunión"

    def test_pause_double_raises(self, started_tracker):
        started_tracker.pause("primera pausa")
        with pytest.raises(ValueError, match="Ya hay una pausa activa"):
            started_tracker.pause("segunda pausa")

    def test_resume_clears_pause(self, started_tracker):
        started_tracker.pause()
        started_tracker.resume()
        assert started_tracker.current_pause is None

    def test_resume_calculates_duration(self, started_tracker):
        started_tracker.pause()
        # Simular que pasó tiempo
        started_tracker.current_pause.started_at = (
            datetime.now(timezone.utc) - timedelta(seconds=3)
        )
        started_tracker.resume()
        assert started_tracker.pauses[0].duration_seconds >= 3

    def test_resume_without_pause_raises(self, started_tracker):
        with pytest.raises(ValueError, match="No hay pausa activa"):
            started_tracker.resume()


# ─────────────────────────────────────────────────────────────────────────────
# Tests: TimeTracker — get_status
# ─────────────────────────────────────────────────────────────────────────────

class TestTimeTrackerStatus:
    def test_get_status_not_started(self, tracker):
        status = tracker.get_status()
        assert status["status"] == "not_started"

    def test_get_status_running(self, started_tracker):
        status = started_tracker.get_status()
        assert status["status"] == "running"

    def test_get_status_paused(self, started_tracker):
        started_tracker.pause("break")
        status = started_tracker.get_status()
        assert status["status"] == "paused"

    def test_get_status_with_tasks(self, tracker_with_phase):
        tracker_with_phase.start_task("t1", "Tarea 1", "modelo", 5.0)
        tracker_with_phase.end_task("t1")
        status = tracker_with_phase.get_status()
        assert status["completed_tasks"] == 1
        assert status["total_tasks"] == 1


# ─────────────────────────────────────────────────────────────────────────────
# Tests: TimeTracker — Persistencia JSON
# ─────────────────────────────────────────────────────────────────────────────

class TestTimeTrackerPersistence:
    def test_to_dict_complete_structure(self, tracker_with_phase):
        tracker_with_phase.start_task("t1", "Tarea 1", "modelo", 5.0)
        tracker_with_phase.end_task("t1")
        tracker_with_phase.end_phase(0)
        tracker_with_phase.end_tracking()

        data = tracker_with_phase._to_dict()

        assert "metadata" in data
        assert "timeline" in data
        assert "phases" in data
        assert "pauses" in data
        assert "summary" in data

        assert data["metadata"]["us_id"] == "US-TEST"
        assert data["metadata"]["us_title"] == "Test US Title"
        assert len(data["phases"]) == 1
        assert data["summary"]["completed_tasks"] == 1

    def test_save_and_load_roundtrip(self, tracker_with_phase):
        """El JSON guardado es válido y parseable."""
        tracker_with_phase.start_task("t1", "Tarea 1", "modelo", 5.0)
        tracker_with_phase.end_task("t1")
        tracker_with_phase.end_phase(0)
        tracker_with_phase.end_tracking()

        assert tracker_with_phase.storage_path.exists()
        with open(tracker_with_phase.storage_path, encoding="utf-8") as f:
            loaded = json.load(f)

        assert loaded["metadata"]["us_id"] == "US-TEST"
        assert len(loaded["phases"]) == 1
