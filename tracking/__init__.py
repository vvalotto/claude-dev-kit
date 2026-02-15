"""
Sistema de Tracking de Tiempo para Claude Dev Kit.

Este módulo proporciona tracking automático de tiempo durante la implementación
de Historias de Usuario con el skill /implement-us.

Componentes:
    - TimeTracker: Gestor central de tracking
    - Task: Modelo de tarea individual
    - Phase: Modelo de fase del skill (0-9)
    - Pause: Modelo de pausa manual

Uso básico:
    >>> from tracking import TimeTracker
    >>> tracker = TimeTracker("US-001", "Implementar feature", 3, "mi_producto")
    >>> tracker.start_tracking()
    >>> tracker.start_phase(0, "Validación de Contexto")
    >>> # ... trabajo ...
    >>> tracker.end_phase(0)
    >>> tracker.end_tracking()

Skills de tracking disponibles:
    - /track-pause [razón]: Pausar tracking con razón opcional
    - /track-resume: Reanudar tracking después de pausa
    - /track-status: Ver estado actual del tracking
    - /track-report [us_id]: Generar reporte detallado
    - /track-history [--last N]: Ver historial de tracking

Persistencia:
    Los datos se guardan automáticamente en `.claude/tracking/{us_id}-tracking.json`
"""

__version__ = "1.0.0"

from .time_tracker import TimeTracker, Task, Phase, Pause

__all__ = [
    "TimeTracker",
    "Task",
    "Phase",
    "Pause"
]
