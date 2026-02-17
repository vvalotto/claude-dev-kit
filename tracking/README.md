# Sistema de Tracking - Documentación Técnica

Documentación técnica de la arquitectura interna del sistema de tracking.

> **Para usuarios:** Ver [docs/tracking/user-guide.md](../docs/tracking/user-guide.md)

Módulo core del sistema de tracking automático para el skill `/implement-us`.

## Componentes

### Modelos de Datos

#### Task
Representa una tarea individual dentro de una fase.

**Campos:**
- `task_id` (str): Identificador único (ej: "task_001")
- `task_name` (str): Nombre descriptivo
- `task_type` (str): Tipo (modelo, vista, controlador, test)
- `estimated_minutes` (float): Estimación del plan en minutos
- `started_at` (datetime): Timestamp de inicio
- `completed_at` (datetime): Timestamp de finalización
- `elapsed_seconds` (int): Duración real en segundos
- `file_created` (str): Path del archivo creado (opcional)
- `status` (str): Estado actual (pending, in_progress, completed)

**Propiedades calculadas:**
- `actual_minutes`: Duración en minutos (elapsed_seconds / 60)
- `variance_minutes`: Diferencia entre real y estimado
- `variance_percent`: Varianza porcentual

#### Phase
Representa una fase del skill implement-us (0-9).

**Campos:**
- `phase_number` (int): Número de fase (0-9)
- `phase_name` (str): Nombre descriptivo
- `started_at` (datetime): Timestamp de inicio
- `completed_at` (datetime): Timestamp de finalización
- `elapsed_seconds` (int): Duración total en segundos
- `status` (str): Estado (pending, in_progress, completed)
- `tasks` (List[Task]): Lista de tareas de esta fase
- `auto_approved` (bool): Si se completó automáticamente
- `user_approval_time_seconds` (int): Tiempo esperando aprobación del usuario

**Propiedades calculadas:**
- `elapsed_minutes`: Duración en minutos

#### Pause
Representa una pausa manual del tracking.

**Campos:**
- `pause_id` (str): Identificador único (ej: "pause_001")
- `started_at` (datetime): Timestamp de inicio de la pausa
- `resumed_at` (datetime): Timestamp de reanudación
- `duration_seconds` (int): Duración de la pausa en segundos
- `reason` (str): Motivo de la pausa

**Propiedades calculadas:**
- `duration_minutes`: Duración en minutos
- `is_active`: True si la pausa está activa (resumed_at es None)

### TimeTracker

Gestor central de tracking de tiempo.

**Uso básico:**

```python
from tracking import TimeTracker

# Inicializar tracker
tracker = TimeTracker(
    us_id="US-001",
    us_title="Implementar panel display",
    us_points=3,
    producto="mi_producto"
)

# Iniciar tracking
tracker.start_tracking()

# Iniciar una fase
tracker.start_phase(0, "Validación de Contexto")

# Trabajar...

# Finalizar fase
tracker.end_phase(0)

# Finalizar tracking
tracker.end_tracking()
```

**Métodos principales:**

- `start_tracking()`: Inicia el tracking de la Historia de Usuario
- `end_tracking()`: Finaliza el tracking
- `start_phase(number, name)`: Inicia una fase (0-9)
- `end_phase(number)`: Finaliza una fase
- `start_task(id, name, type, estimated)`: Inicia una tarea dentro de la fase actual
- `end_task(id, file_created)`: Finaliza una tarea
- `pause(reason)`: Pausa el tracking con razón opcional
- `resume()`: Reanuda el tracking después de una pausa
- `get_status()`: Obtiene el estado actual del tracking

## Persistencia

Los datos se guardan automáticamente en `.claude/tracking/{us_id}-tracking.json` en formato JSON.

**Ejemplo de archivo:**

```json
{
  "metadata": {
    "us_id": "US-001",
    "us_title": "Implementar panel display",
    "us_points": 3,
    "producto": "mi_producto",
    "tracking_version": "1.0"
  },
  "timeline": {
    "started_at": "2026-02-15T10:00:00Z",
    "completed_at": "2026-02-15T14:00:00Z",
    "total_elapsed_seconds": 14400,
    "effective_seconds": 13500,
    "paused_seconds": 900
  },
  "phases": [
    {
      "phase_number": 0,
      "phase_name": "Validación de Contexto",
      "started_at": "2026-02-15T10:00:00Z",
      "completed_at": "2026-02-15T10:15:00Z",
      "elapsed_seconds": 900,
      "status": "completed",
      "tasks": [],
      "auto_approved": true
    }
  ],
  "pauses": [],
  "summary": {
    "total_tasks": 15,
    "completed_tasks": 15,
    "total_phases": 10,
    "estimated_total_minutes": 120,
    "actual_total_minutes": 135,
    "variance_minutes": 15,
    "variance_percent": 12.5
  }
}
```

## Skills de Tracking

Los siguientes skills interactúan con este módulo:

- `/track-pause [razón]`: Pausar tracking con razón opcional
- `/track-resume`: Reanudar tracking
- `/track-status`: Ver estado actual del tracking
- `/track-report [us_id]`: Generar reporte detallado
- `/track-history [--last N]`: Ver historial de tracking

Ver documentación de cada skill para detalles de uso.

## Integración con /implement-us

El skill `/implement-us` usa este módulo automáticamente para trackear tiempo en cada fase de implementación.

No requiere intervención manual del usuario (excepto para pausas).

## Ejemplo Avanzado

```python
from tracking import TimeTracker

# Crear y iniciar tracker
tracker = TimeTracker("US-001", "Nueva feature", 5, "mi_app")
tracker.start_tracking()

# Ejecutar múltiples fases
for phase_num, phase_name in [
    (0, "Validación"),
    (1, "Escenarios BDD"),
    (2, "Planning")
]:
    tracker.start_phase(phase_num, phase_name)

    # Simular trabajo con tareas
    if phase_num == 2:
        tracker.start_task("task_001", "Crear plan", "docs", 15)
        # ... trabajo ...
        tracker.end_task("task_001")

    tracker.end_phase(phase_num)

# Pausar manualmente
tracker.pause("Reunión del equipo")
# ... 30 minutos ...
tracker.resume()

# Continuar con más fases...

# Finalizar
tracker.end_tracking()

# Ver estado final
status = tracker.get_status()
print(f"Tiempo efectivo: {status['effective_seconds'] / 60} minutos")
```

## Documentación Adicional

- **Guía de Usuario**: `docs/tracking/user-guide.md`
- **Arquitectura**: `docs/developer/architecture/tracking.md`
- **Ejemplos**: `docs/tracking/examples.md`
