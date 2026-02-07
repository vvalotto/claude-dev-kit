"""
Sistema de tracking de tiempo para implementación de Historias de Usuario.

Este módulo provee tracking automático de tiempo durante la ejecución del
skill /implement-us, permitiendo medir la duración real de implementación
de cada Historia de Usuario.

Módulos:
    time_tracker: Clase principal TimeTracker y dataclasses relacionadas
    commands: Comandos manuales para control del tracking

Uso básico:
    >>> from .time_tracker import TimeTracker
    >>> tracker = TimeTracker("US-001", "Ver temperatura", 3, "ux_termostato")
    >>> tracker.start_tracking()
    >>> tracker.start_phase(0, "Validación")
    >>> # ... trabajo ...
    >>> tracker.end_phase(0)
    >>> tracker.end_tracking()

Comandos disponibles:
    >>> from .commands import track_pause, track_resume, track_status
    >>> from .commands import track_report, track_history
    >>> result = track_status()
    >>> print(result["message"])
"""

__version__ = "1.0.0"
__author__ = "Victor Valotto"

from .time_tracker import TimeTracker, Task, Phase, Pause
from .commands import (
    track_pause,
    track_resume,
    track_status,
    track_report,
    track_history
)

__all__ = [
    "TimeTracker",
    "Task",
    "Phase",
    "Pause",
    "track_pause",
    "track_resume",
    "track_status",
    "track_report",
    "track_history"
]
