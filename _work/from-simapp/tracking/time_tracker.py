"""
TimeTracker - Sistema de tracking de tiempo para implementación de USs.

Este módulo implementa el tracking automático de tiempo durante la ejecución
del skill /implement-us.
"""
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List, Dict, Any
import json


@dataclass
class Task:
    """Representa una tarea individual dentro de una fase.

    Attributes:
        task_id: Identificador único de la tarea (ej: "task_001")
        task_name: Nombre descriptivo (ej: "Implementar DisplayModelo")
        task_type: Tipo de tarea (modelo, vista, controlador, test)
        estimated_minutes: Estimación en minutos del plan
        started_at: Timestamp de inicio
        completed_at: Timestamp de finalización
        elapsed_seconds: Duración total en segundos
        file_created: Path del archivo creado (opcional)
        status: Estado actual (pending, in_progress, completed)
    """
    task_id: str
    task_name: str
    task_type: str
    estimated_minutes: float
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    elapsed_seconds: int = 0
    file_created: Optional[str] = None
    status: str = "pending"

    @property
    def actual_minutes(self) -> float:
        """Retorna duración en minutos."""
        return self.elapsed_seconds / 60.0

    @property
    def variance_minutes(self) -> float:
        """Retorna varianza en minutos (real - estimado)."""
        return self.actual_minutes - self.estimated_minutes

    @property
    def variance_percent(self) -> float:
        """Retorna varianza porcentual."""
        if self.estimated_minutes == 0:
            return 0.0
        return (self.variance_minutes / self.estimated_minutes) * 100


@dataclass
class Phase:
    """Representa una fase del skill implement-us.

    Attributes:
        phase_number: Número de fase (0-9)
        phase_name: Nombre descriptivo (ej: "Validación de Contexto")
        started_at: Timestamp de inicio
        completed_at: Timestamp de finalización
        elapsed_seconds: Duración total en segundos
        status: Estado actual (pending, in_progress, completed)
        tasks: Lista de tareas de esta fase
        auto_approved: Si la fase se completó sin aprobación manual
        user_approval_time_seconds: Tiempo esperando aprobación del usuario
    """
    phase_number: int
    phase_name: str
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    elapsed_seconds: int = 0
    status: str = "pending"
    tasks: List[Task] = field(default_factory=list)
    auto_approved: bool = True
    user_approval_time_seconds: int = 0

    @property
    def elapsed_minutes(self) -> float:
        """Retorna duración en minutos."""
        return self.elapsed_seconds / 60.0


@dataclass
class Pause:
    """Representa una pausa manual del tracking.

    Attributes:
        pause_id: Identificador único (ej: "pause_001")
        started_at: Timestamp de inicio de la pausa
        resumed_at: Timestamp de reanudación
        duration_seconds: Duración de la pausa en segundos
        reason: Motivo de la pausa (opcional)
    """
    pause_id: str
    started_at: datetime
    resumed_at: Optional[datetime] = None
    duration_seconds: int = 0
    reason: str = ""

    @property
    def duration_minutes(self) -> float:
        """Retorna duración en minutos."""
        return self.duration_seconds / 60.0

    @property
    def is_active(self) -> bool:
        """True si la pausa está activa (no resumida)."""
        return self.resumed_at is None


class TimeTracker:
    """Gestor central de tracking de tiempo.

    Maneja el ciclo de vida completo del tracking durante la implementación
    de una Historia de Usuario con el skill /implement-us.

    Attributes:
        us_id: ID de la Historia de Usuario (ej: "US-001")
        us_title: Título de la US
        us_points: Puntos de estimación
        producto: Nombre del producto (ej: "ux_termostato")
        started_at: Timestamp de inicio del tracking
        completed_at: Timestamp de finalización
        phases: Lista de fases trackeadas
        pauses: Lista de pausas manuales
        current_phase: Fase actualmente en progreso
        current_task: Tarea actualmente en progreso
        current_pause: Pausa actualmente activa

    Example:
        >>> tracker = TimeTracker("US-001", "Ver temperatura", 3, "ux_termostato")
        >>> tracker.start_tracking()
        >>> tracker.start_phase(0, "Validación de Contexto")
        >>> # ... trabajo ...
        >>> tracker.end_phase(0)
        >>> tracker.end_tracking()
    """

    def __init__(
        self,
        us_id: str,
        us_title: str,
        us_points: int,
        producto: str
    ):
        """Inicializa el tracker.

        Args:
            us_id: ID de la Historia de Usuario
            us_title: Título descriptivo
            us_points: Puntos de estimación
            producto: Nombre del producto
        """
        self.us_id = us_id
        self.us_title = us_title
        self.us_points = us_points
        self.producto = producto

        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None

        self.phases: List[Phase] = []
        self.pauses: List[Pause] = []

        self.current_phase: Optional[Phase] = None
        self.current_task: Optional[Task] = None
        self.current_pause: Optional[Pause] = None

        # Path de almacenamiento
        self.storage_path = Path(f".claude/tracking/{us_id}-tracking.json")
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

    def start_tracking(self) -> None:
        """Inicia el tracking (al invocar /implement-us).

        Registra el timestamp de inicio y guarda el estado.
        """
        self.started_at = datetime.now(timezone.utc)
        self._save()

    def start_phase(self, phase_number: int, phase_name: str) -> None:
        """Inicia una nueva fase.

        Args:
            phase_number: Número de la fase (0-9)
            phase_name: Nombre descriptivo de la fase
        """
        phase = Phase(
            phase_number=phase_number,
            phase_name=phase_name,
            started_at=datetime.now(timezone.utc),
            status="in_progress"
        )
        self.phases.append(phase)
        self.current_phase = phase
        self._save()

    def end_phase(
        self,
        phase_number: int,
        auto_approved: bool = True
    ) -> None:
        """Finaliza una fase.

        Args:
            phase_number: Número de la fase a finalizar
            auto_approved: Si la fase se completó automáticamente
        """
        phase = self._get_phase(phase_number)
        if phase:
            phase.completed_at = datetime.now(timezone.utc)
            phase.elapsed_seconds = int(
                (phase.completed_at - phase.started_at).total_seconds()
            )
            phase.status = "completed"
            phase.auto_approved = auto_approved
            self.current_phase = None
            self._save()

    def start_task(
        self,
        task_id: str,
        task_name: str,
        task_type: str,
        estimated_minutes: float
    ) -> None:
        """Inicia una nueva tarea dentro de la fase actual.

        Args:
            task_id: Identificador único de la tarea
            task_name: Nombre descriptivo
            task_type: Tipo (modelo, vista, controlador, test)
            estimated_minutes: Estimación del plan

        Raises:
            ValueError: Si no hay fase activa
        """
        if not self.current_phase:
            raise ValueError("No hay fase activa")

        task = Task(
            task_id=task_id,
            task_name=task_name,
            task_type=task_type,
            estimated_minutes=estimated_minutes,
            started_at=datetime.now(timezone.utc),
            status="in_progress"
        )
        self.current_phase.tasks.append(task)
        self.current_task = task
        self._save()

    def end_task(
        self,
        task_id: str,
        file_created: Optional[str] = None
    ) -> None:
        """Finaliza una tarea.

        Args:
            task_id: ID de la tarea a finalizar
            file_created: Path del archivo creado (opcional)

        Raises:
            ValueError: Si no hay fase activa
        """
        if not self.current_phase:
            raise ValueError("No hay fase activa")

        task = self._get_task(task_id)
        if task:
            task.completed_at = datetime.now(timezone.utc)
            task.elapsed_seconds = int(
                (task.completed_at - task.started_at).total_seconds()
            )
            task.status = "completed"
            task.file_created = file_created
            self.current_task = None
            self._save()

    def pause(self, reason: str = "") -> None:
        """Pausa el tracking (invocado por /track-pause).

        Args:
            reason: Motivo de la pausa (opcional)

        Raises:
            ValueError: Si ya hay una pausa activa
        """
        if self.current_pause:
            raise ValueError("Ya hay una pausa activa")

        pause = Pause(
            pause_id=f"pause_{len(self.pauses) + 1:03d}",
            started_at=datetime.now(timezone.utc),
            reason=reason
        )
        self.pauses.append(pause)
        self.current_pause = pause
        self._save()

    def resume(self) -> None:
        """Reanuda el tracking (invocado por /track-resume).

        Raises:
            ValueError: Si no hay pausa activa
        """
        if not self.current_pause:
            raise ValueError("No hay pausa activa")

        self.current_pause.resumed_at = datetime.now(timezone.utc)
        self.current_pause.duration_seconds = int(
            (self.current_pause.resumed_at - self.current_pause.started_at).total_seconds()
        )
        self.current_pause = None
        self._save()

    def end_tracking(self) -> None:
        """Finaliza el tracking (al completar Fase 9).

        Registra el timestamp de finalización y genera reportes.
        """
        self.completed_at = datetime.now(timezone.utc)
        self._save()
        # Los reportes se generarán en una fase posterior

    def get_status(self) -> Dict[str, Any]:
        """Retorna estado actual para /track-status.

        Returns:
            Dict con información del estado actual del tracking
        """
        if not self.started_at:
            return {"status": "not_started"}

        now = datetime.now(timezone.utc)
        elapsed = int((now - self.started_at).total_seconds())

        # Calcular tiempo pausado
        paused = sum(p.duration_seconds for p in self.pauses if p.resumed_at)
        if self.current_pause:
            paused += int((now - self.current_pause.started_at).total_seconds())

        effective = elapsed - paused

        # Contar tareas completadas
        completed_tasks = sum(
            len([t for t in p.tasks if t.status == "completed"])
            for p in self.phases
        )
        total_tasks = sum(len(p.tasks) for p in self.phases)

        return {
            "status": "paused" if self.current_pause else "running",
            "started_at": self.started_at.isoformat(),
            "elapsed_seconds": elapsed,
            "effective_seconds": effective,
            "paused_seconds": paused,
            "current_phase": self.current_phase.phase_name if self.current_phase else None,
            "current_task": self.current_task.task_name if self.current_task else None,
            "completed_tasks": completed_tasks,
            "total_tasks": total_tasks
        }

    def _get_phase(self, phase_number: int) -> Optional[Phase]:
        """Obtiene una fase por número.

        Args:
            phase_number: Número de la fase (0-9)

        Returns:
            La fase correspondiente o None si no existe
        """
        return next(
            (p for p in self.phases if p.phase_number == phase_number),
            None
        )

    def _get_task(self, task_id: str) -> Optional[Task]:
        """Obtiene una tarea por ID.

        Args:
            task_id: Identificador de la tarea

        Returns:
            La tarea correspondiente o None si no existe
        """
        if not self.current_phase:
            return None
        return next(
            (t for t in self.current_phase.tasks if t.task_id == task_id),
            None
        )

    def _save(self) -> None:
        """Guarda estado actual a JSON."""
        data = self._to_dict()
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _to_dict(self) -> Dict[str, Any]:
        """Convierte el tracker a diccionario JSON-serializable.

        Returns:
            Dict con toda la información del tracking
        """
        def serialize_datetime(dt: Optional[datetime]) -> Optional[str]:
            """Serializa datetime a ISO 8601."""
            return dt.isoformat() if dt else None

        def serialize_task(task: Task) -> Dict[str, Any]:
            """Serializa una Task a dict."""
            return {
                "task_id": task.task_id,
                "task_name": task.task_name,
                "task_type": task.task_type,
                "estimated_minutes": task.estimated_minutes,
                "started_at": serialize_datetime(task.started_at),
                "completed_at": serialize_datetime(task.completed_at),
                "elapsed_seconds": task.elapsed_seconds,
                "actual_minutes": round(task.actual_minutes, 2),
                "variance_minutes": round(task.variance_minutes, 2),
                "file_created": task.file_created,
                "status": task.status
            }

        def serialize_phase(phase: Phase) -> Dict[str, Any]:
            """Serializa una Phase a dict."""
            return {
                "phase_number": phase.phase_number,
                "phase_name": phase.phase_name,
                "started_at": serialize_datetime(phase.started_at),
                "completed_at": serialize_datetime(phase.completed_at),
                "elapsed_seconds": phase.elapsed_seconds,
                "status": phase.status,
                "tasks": [serialize_task(t) for t in phase.tasks],
                "auto_approved": phase.auto_approved,
                "user_approval_time_seconds": phase.user_approval_time_seconds
            }

        def serialize_pause(pause: Pause) -> Dict[str, Any]:
            """Serializa una Pause a dict."""
            return {
                "pause_id": pause.pause_id,
                "started_at": serialize_datetime(pause.started_at),
                "resumed_at": serialize_datetime(pause.resumed_at),
                "duration_seconds": pause.duration_seconds,
                "reason": pause.reason
            }

        # Calcular totales
        total_elapsed = 0
        total_paused = sum(p.duration_seconds for p in self.pauses if p.resumed_at)

        if self.started_at and self.completed_at:
            total_elapsed = int((self.completed_at - self.started_at).total_seconds())
        elif self.started_at:
            total_elapsed = int((datetime.now(timezone.utc) - self.started_at).total_seconds())

        # Si hay pausa activa, incluirla en el total pausado
        if self.current_pause:
            total_paused += int(
                (datetime.now(timezone.utc) - self.current_pause.started_at).total_seconds()
            )

        total_effective = total_elapsed - total_paused

        # Calcular summary
        completed_tasks = sum(
            len([t for t in p.tasks if t.status == "completed"])
            for p in self.phases
        )
        total_tasks = sum(len(p.tasks) for p in self.phases)

        estimated_total = sum(
            sum(t.estimated_minutes for t in p.tasks)
            for p in self.phases
        )
        actual_total = sum(
            sum(t.actual_minutes for t in p.tasks if t.status == "completed")
            for p in self.phases
        )

        # Construir diccionario completo
        return {
            "metadata": {
                "us_id": self.us_id,
                "us_title": self.us_title,
                "us_points": self.us_points,
                "producto": self.producto,
                "tracking_version": "1.0"
            },
            "timeline": {
                "started_at": serialize_datetime(self.started_at),
                "completed_at": serialize_datetime(self.completed_at),
                "total_elapsed_seconds": total_elapsed,
                "effective_seconds": total_effective,
                "paused_seconds": total_paused
            },
            "phases": [serialize_phase(p) for p in self.phases],
            "pauses": [serialize_pause(p) for p in self.pauses],
            "summary": {
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "total_phases": len(self.phases),
                "estimated_total_minutes": round(estimated_total, 2),
                "actual_total_minutes": round(actual_total, 2),
                "variance_minutes": round(actual_total - estimated_total, 2),
                "variance_percent": round(
                    ((actual_total - estimated_total) / estimated_total * 100)
                    if estimated_total > 0 else 0.0,
                    2
                )
            }
        }
