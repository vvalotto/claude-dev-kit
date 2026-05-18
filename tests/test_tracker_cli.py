"""
Tests del módulo tracking/tracker_cli.py

Cubre: _find_active_us_id, cmd_init, cmd_start_phase, cmd_end_phase,
       cmd_start_task, cmd_end_task, cmd_status, cmd_end, TimeTracker.load
"""
import json
import sys
import pytest
from pathlib import Path
from unittest.mock import patch

# Asegurar que tracking/ es importable
sys.path.insert(0, str(Path(__file__).parent.parent))

from tracking.time_tracker import TimeTracker
from tracking.tracker_cli import (
    _find_active_us_id,
    cmd_init,
    cmd_start_phase,
    cmd_end_phase,
    cmd_start_task,
    cmd_end_task,
    cmd_status,
    cmd_end,
    build_parser,
)


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture(autouse=True)
def chdir_tmp(tmp_path, monkeypatch):
    """Todos los tests corren con cwd = tmp_path para aislar .claude/tracking/."""
    monkeypatch.chdir(tmp_path)


@pytest.fixture
def active_tracker(tmp_path):
    """TimeTracker iniciado, activo (completed_at=None)."""
    t = TimeTracker("US-1.0.0", "Historia de prueba", 3, "test_prod")
    t.start_tracking()
    return t


@pytest.fixture
def parser():
    return build_parser()


# =============================================================================
# Tests: TimeTracker.load
# =============================================================================

class TestTimeTrackerLoad:

    def test_load_existing(self, active_tracker):
        loaded = TimeTracker.load("US-1.0.0")
        assert loaded.us_id == "US-1.0.0"
        assert loaded.us_title == "Historia de prueba"

    def test_load_restores_started_at(self, active_tracker):
        loaded = TimeTracker.load("US-1.0.0")
        assert loaded.started_at is not None

    def test_load_missing_raises(self):
        with pytest.raises(FileNotFoundError, match="US-INEXISTENTE"):
            TimeTracker.load("US-INEXISTENTE")

    def test_load_non_us_prefix(self):
        t = TimeTracker("INC-2.0", "Incremento técnico", 2, "prod")
        t.start_tracking()
        loaded = TimeTracker.load("INC-2.0")
        assert loaded.us_id == "INC-2.0"


# =============================================================================
# Tests: _find_active_us_id
# =============================================================================

class TestFindActiveUsId:

    def test_finds_active_tracker(self, active_tracker):
        assert _find_active_us_id() == "US-1.0.0"

    def test_finds_non_us_prefix(self):
        t = TimeTracker("INC-2.0", "Incremento", 2, "prod")
        t.start_tracking()
        assert _find_active_us_id() == "INC-2.0"

    def test_no_active_raises(self):
        with pytest.raises(RuntimeError, match="No hay trackers activos"):
            _find_active_us_id()

    def test_multiple_active_raises(self, active_tracker):
        t2 = TimeTracker("US-2.0.0", "Segunda US", 2, "prod")
        t2.start_tracking()
        with pytest.raises(RuntimeError, match="Múltiples trackers activos"):
            _find_active_us_id()

    def test_completed_tracker_ignored(self, active_tracker):
        active_tracker.end_tracking()
        # Sin trackers activos ahora
        with pytest.raises(RuntimeError, match="No hay trackers activos"):
            _find_active_us_id()

    def test_multiple_active_lists_both_ids(self, active_tracker):
        t2 = TimeTracker("TEC-1.0", "Técnico", 1, "prod")
        t2.start_tracking()
        with pytest.raises(RuntimeError) as exc:
            _find_active_us_id()
        msg = str(exc.value)
        assert "US-1.0.0" in msg
        assert "TEC-1.0" in msg


# =============================================================================
# Tests: cmd_init
# =============================================================================

class TestCmdInit:

    def test_creates_tracking_file(self, parser, capsys):
        args = parser.parse_args(["init", "US-3.0.0", "Mi historia", "5", "mi_prod"])
        cmd_init(args)
        assert Path(".claude/tracking/US-3.0.0-tracking.json").exists()

    def test_tracking_file_is_valid_json(self, parser):
        args = parser.parse_args(["init", "US-3.0.0", "Mi historia", "5", "mi_prod"])
        cmd_init(args)
        data = json.loads(Path(".claude/tracking/US-3.0.0-tracking.json").read_text())
        assert data["metadata"]["us_id"] == "US-3.0.0"

    def test_prints_confirmation(self, parser, capsys):
        args = parser.parse_args(["init", "US-3.0.0", "Mi historia", "5", "mi_prod"])
        cmd_init(args)
        out = capsys.readouterr().out
        assert "US-3.0.0" in out


# =============================================================================
# Tests: cmd_start_phase / cmd_end_phase
# =============================================================================

class TestCmdPhase:

    def test_start_phase_adds_phase(self, active_tracker, parser):
        args = parser.parse_args(["start-phase", "0", "Validación de Contexto"])
        cmd_start_phase(args)
        loaded = TimeTracker.load("US-1.0.0")
        assert len(loaded.phases) == 1
        assert loaded.phases[0].phase_name == "Validación de Contexto"

    def test_end_phase_completes_phase(self, active_tracker, parser):
        args_sp = parser.parse_args(["start-phase", "0", "Validación de Contexto"])
        cmd_start_phase(args_sp)
        args_ep = parser.parse_args(["end-phase", "0"])
        cmd_end_phase(args_ep)
        loaded = TimeTracker.load("US-1.0.0")
        assert loaded.phases[0].status == "completed"

    def test_start_phase_explicit_us_id(self, active_tracker, parser):
        args = parser.parse_args(["start-phase", "1", "BDD", "--us-id", "US-1.0.0"])
        cmd_start_phase(args)
        loaded = TimeTracker.load("US-1.0.0")
        assert loaded.phases[0].phase_number == 1

    def test_end_phase_sets_elapsed(self, active_tracker, parser):
        cmd_start_phase(parser.parse_args(["start-phase", "0", "Validación"]))
        cmd_end_phase(parser.parse_args(["end-phase", "0"]))
        loaded = TimeTracker.load("US-1.0.0")
        assert loaded.phases[0].elapsed_seconds >= 0


# =============================================================================
# Tests: cmd_start_task / cmd_end_task
# =============================================================================

class TestCmdTask:

    def test_start_task_adds_task(self, active_tracker, parser):
        cmd_start_phase(parser.parse_args(["start-phase", "3", "Implementación"]))
        cmd_start_task(parser.parse_args(["start-task", "t001", "Crear aggregate", "dominio", "20"]))
        loaded = TimeTracker.load("US-1.0.0")
        assert len(loaded.phases[0].tasks) == 1
        assert loaded.phases[0].tasks[0].task_id == "t001"

    def test_end_task_completes_task(self, active_tracker, parser):
        cmd_start_phase(parser.parse_args(["start-phase", "3", "Implementación"]))
        cmd_start_task(parser.parse_args(["start-task", "t001", "Crear aggregate", "dominio", "20"]))
        cmd_end_task(parser.parse_args(["end-task", "t001", "src/domain/aggregate.py"]))
        loaded = TimeTracker.load("US-1.0.0")
        assert loaded.phases[0].tasks[0].status == "completed"
        assert loaded.phases[0].tasks[0].file_created == "src/domain/aggregate.py"

    def test_end_task_without_file(self, active_tracker, parser):
        cmd_start_phase(parser.parse_args(["start-phase", "3", "Implementación"]))
        cmd_start_task(parser.parse_args(["start-task", "t001", "Tarea", "test", "5"]))
        cmd_end_task(parser.parse_args(["end-task", "t001"]))
        loaded = TimeTracker.load("US-1.0.0")
        assert loaded.phases[0].tasks[0].file_created is None


# =============================================================================
# Tests: cmd_status
# =============================================================================

class TestCmdStatus:

    def test_status_shows_us_id(self, active_tracker, parser, capsys):
        cmd_status(parser.parse_args(["status"]))
        out = capsys.readouterr().out
        assert "US-1.0.0" in out

    def test_status_shows_elapsed(self, active_tracker, parser, capsys):
        cmd_status(parser.parse_args(["status"]))
        out = capsys.readouterr().out
        assert "min" in out

    def test_status_shows_current_phase(self, active_tracker, parser, capsys):
        cmd_start_phase(parser.parse_args(["start-phase", "0", "Validación"]))
        cmd_status(parser.parse_args(["status"]))
        out = capsys.readouterr().out
        assert "Validación" in out


# =============================================================================
# Tests: cmd_end
# =============================================================================

class TestCmdEnd:

    def test_end_marks_completed(self, active_tracker, parser):
        cmd_end(parser.parse_args(["end"]))
        data = json.loads(Path(".claude/tracking/US-1.0.0-tracking.json").read_text())
        assert data["timeline"]["completed_at"] is not None

    def test_end_explicit_us_id(self, active_tracker, parser):
        cmd_end(parser.parse_args(["end", "US-1.0.0"]))
        loaded = TimeTracker.load("US-1.0.0")
        assert loaded.completed_at is not None

    def test_end_prints_summary(self, active_tracker, parser, capsys):
        cmd_end(parser.parse_args(["end"]))
        out = capsys.readouterr().out
        assert "US-1.0.0" in out
        assert "finalizado" in out.lower()


# =============================================================================
# Tests: ciclo completo init → phase → task → end
# =============================================================================

class TestFullCycle:

    def test_full_cycle(self, parser, capsys):
        """Ciclo completo: init → start-phase → start-task → end-task → end-phase → end."""
        cmd_init(parser.parse_args(["init", "US-9.9.9", "Ciclo completo", "5", "prod"]))
        cmd_start_phase(parser.parse_args(["start-phase", "0", "Validación", "--us-id", "US-9.9.9"]))
        cmd_start_task(parser.parse_args(["start-task", "t001", "Tarea A", "dominio", "10", "--us-id", "US-9.9.9"]))
        cmd_end_task(parser.parse_args(["end-task", "t001", "--us-id", "US-9.9.9"]))
        cmd_end_phase(parser.parse_args(["end-phase", "0", "--us-id", "US-9.9.9"]))
        cmd_end(parser.parse_args(["end", "US-9.9.9"]))

        loaded = TimeTracker.load("US-9.9.9")
        assert loaded.completed_at is not None
        assert len(loaded.phases) == 1
        assert loaded.phases[0].status == "completed"
        assert loaded.phases[0].tasks[0].status == "completed"
