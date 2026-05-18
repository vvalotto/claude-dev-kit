"""
Fixtures compartidos para la suite de tests de Claude Dev Kit.

Proporciona:
- config_json_path: Path al install/config.json real
- kit_root: Path al directorio raíz del kit
- installer: Instancia de ClaudeDevKitInstaller con config real
- mock_project_dir: Directorio temporal vacío (tmp_path)
- tracker: TimeTracker con storage en tmp_path (aislado del filesystem real)
- sample_tracking_data: Dict con datos de tracking completos para tests de serialización
"""
import sys
import json
import pytest
from pathlib import Path
from datetime import datetime, timezone, timedelta

# Paths del proyecto
REPO_ROOT = Path(__file__).parent.parent
INSTALL_DIR = REPO_ROOT / "install"

# Hacer importable el módulo install/
sys.path.insert(0, str(INSTALL_DIR))

from installer import ClaudeDevKitInstaller  # noqa: E402
from tracking.time_tracker import TimeTracker  # noqa: E402


# =============================================================================
# FIXTURES: Instalador
# =============================================================================

@pytest.fixture(scope="session")
def config_json_path() -> Path:
    """Path al install/config.json real del repositorio."""
    path = INSTALL_DIR / "config.json"
    assert path.exists(), f"config.json no encontrado en {path}"
    return path


@pytest.fixture(scope="session")
def kit_root() -> Path:
    """Path al directorio raíz del kit."""
    return REPO_ROOT


@pytest.fixture(scope="session")
def installer(config_json_path, kit_root) -> ClaudeDevKitInstaller:
    """
    Instancia de ClaudeDevKitInstaller con la config real.

    Scope=session para no recargar config.json en cada test.
    """
    return ClaudeDevKitInstaller(config_json_path, kit_root)


@pytest.fixture
def mock_project_dir(tmp_path) -> Path:
    """
    Directorio temporal vacío que simula un proyecto de usuario.

    Cada test recibe un directorio fresco e independiente.
    """
    return tmp_path


# =============================================================================
# FIXTURES: Tracking
# =============================================================================

@pytest.fixture
def tracker(tmp_path, monkeypatch) -> TimeTracker:
    """
    TimeTracker aislado con storage_path en directorio temporal.

    Usa monkeypatch.chdir para que el mkdir interno de TimeTracker
    opere dentro de tmp_path y no en el directorio real del proyecto.
    """
    monkeypatch.chdir(tmp_path)
    t = TimeTracker(
        us_id="US-TEST-001",
        us_title="Test Historia de Usuario",
        us_points=3,
        producto="test_producto",
    )
    return t


@pytest.fixture
def started_tracker(tracker) -> TimeTracker:
    """TimeTracker ya iniciado (start_tracking llamado)."""
    tracker.start_tracking()
    return tracker


@pytest.fixture
def tracker_with_phase(started_tracker) -> TimeTracker:
    """TimeTracker con una fase activa (fase 0 iniciada)."""
    started_tracker.start_phase(0, "Fase de Validación")
    return started_tracker


@pytest.fixture
def sample_tracking_data() -> dict:
    """
    Dict con datos de tracking completos para tests de serialización.

    Refleja la estructura generada por TimeTracker._to_dict().
    """
    now = datetime.now(timezone.utc)
    started = now - timedelta(minutes=10)
    completed = now - timedelta(minutes=1)

    return {
        "metadata": {
            "us_id": "US-SAMPLE-001",
            "us_title": "Historia de Ejemplo",
            "us_points": 5,
            "producto": "sample_producto",
            "tracking_version": "1.0",
        },
        "timeline": {
            "started_at": started.isoformat(),
            "completed_at": completed.isoformat(),
            "total_elapsed_seconds": 540,
            "effective_seconds": 480,
            "paused_seconds": 60,
        },
        "phases": [
            {
                "phase_number": 0,
                "phase_name": "Validación de Contexto",
                "started_at": started.isoformat(),
                "completed_at": (started + timedelta(minutes=2)).isoformat(),
                "elapsed_seconds": 120,
                "status": "completed",
                "tasks": [
                    {
                        "task_id": "task_001",
                        "task_name": "Revisar contexto",
                        "task_type": "análisis",
                        "estimated_minutes": 2.0,
                        "started_at": started.isoformat(),
                        "completed_at": (started + timedelta(minutes=2)).isoformat(),
                        "elapsed_seconds": 120,
                        "actual_minutes": 2.0,
                        "variance_minutes": 0.0,
                        "file_created": None,
                        "status": "completed",
                    }
                ],
                "auto_approved": True,
                "user_approval_time_seconds": 0,
            }
        ],
        "pauses": [
            {
                "pause_id": "pause_001",
                "started_at": (started + timedelta(minutes=3)).isoformat(),
                "resumed_at": (started + timedelta(minutes=4)).isoformat(),
                "duration_seconds": 60,
                "reason": "pausa de café",
            }
        ],
        "summary": {
            "total_tasks": 1,
            "completed_tasks": 1,
            "total_phases": 1,
            "estimated_total_minutes": 2.0,
            "actual_total_minutes": 2.0,
            "variance_minutes": 0.0,
            "variance_percent": 0.0,
        },
    }
