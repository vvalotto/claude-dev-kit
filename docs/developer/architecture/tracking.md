# Arquitectura del Sistema de Tracking

## Visión General

Sistema de tracking automático de tiempo basado en dataclasses Python y persistencia JSON.

## Componentes

### Core (tracking/)

#### time_tracker.py
- **Task**: Dataclass para tareas individuales con métricas de varianza
- **Phase**: Dataclass para fases del skill (0-9) con lista de tareas
- **Pause**: Dataclass para pausas manuales con razón y duración
- **TimeTracker**: Gestor central con métodos de lifecycle y persistencia
  - `from_json(path)`: classmethod que restaura el estado completo desde un archivo JSON existente

#### track.py
CLI de tracking invocado por el skill `/implement-us` en cada fase:

| Comando | Descripción |
|---------|-------------|
| `start-phase N "nombre" --us US_ID` | Inicia una fase (crea tracking si es fase 0) |
| `end-phase N` | Finaliza la fase activa |
| `start-task "nombre"` | Inicia una tarea dentro de la fase activa |
| `end-task "nombre"` | Finaliza la tarea activa |
| `end-tracking` | Cierra el tracking de la US |

El argumento `--us US_ID` es requerido solo en `start-phase 0` (primera llamada, cuando aún no existe archivo de tracking). En el resto de comandos es opcional: si se omite, el CLI detecta automáticamente el archivo de tracking activo.

#### reports.py
- **format_duration()**: Formatea segundos a formato legible
- **format_timestamp()**: Formatea timestamps ISO a formato legible
- **generate_full_report()**: Genera reporte completo en markdown
- **generate_history_table()**: Genera tabla de historial

#### __init__.py
- Exports del módulo: TimeTracker, Task, Phase, Pause

### Skills (.claude/skills/)

- **track-pause/**: Pausar tracking con razón opcional
- **track-resume/**: Reanudar tracking después de pausa
- **track-status/**: Ver estado actual con métricas en tiempo real
- **track-report/**: Generar reporte detallado de una US
- **track-history/**: Ver historial completo de tracking

### Persistencia (.claude/tracking/)

Archivos JSON con formato:
```json
{
  "metadata": {...},
  "timeline": {...},
  "phases": [...],
  "pauses": [...],
  "summary": {...}
}
```

## Flujo de Datos

```
Usuario ejecuta /implement-us US-001
    ↓
TimeTracker.start_tracking()
    ↓
Para cada Fase (0-9):
    TimeTracker.start_phase(N, name)
    → Trabajo de implementación
    TimeTracker.end_phase(N)
    ↓
TimeTracker.end_tracking()
    ↓
Archivo JSON guardado en .claude/tracking/
    ↓
Accesible via /track-report, /track-history
```

## Modelo de Datos

### Task
```python
task_id: str
task_name: str
task_type: str
estimated_minutes: float
started_at: datetime
completed_at: datetime
elapsed_seconds: int
file_created: str
status: str
```

### Phase
```python
phase_number: int  # 0-9
phase_name: str
started_at: datetime
completed_at: datetime
elapsed_seconds: int
status: str
tasks: List[Task]
auto_approved: bool
user_approval_time_seconds: int
```

### Pause
```python
pause_id: str
started_at: datetime
resumed_at: datetime
duration_seconds: int
reason: str
```

### TimeTracker
```python
us_id: str
us_title: str
us_points: int
producto: str
started_at: datetime
completed_at: datetime
phases: List[Phase]
pauses: List[Pause]
current_phase: Phase
current_task: Task
current_pause: Pause
storage_path: Path
```

## Integración con implement-us

El skill `/implement-us` invoca el sistema de tracking mediante **directivas bash** al inicio y cierre de cada fase. Este es el mecanismo actual desde v1.1:

```bash
# Fase 0: crear tracking e iniciar fase (--us requerido)
python .claude/tracking/track.py start-phase 0 "Validación de Contexto" --us {US_ID}

# Fases 1-9: continuar tracking existente
python .claude/tracking/track.py start-phase N "Nombre de Fase"

# Al cerrar cada fase
python .claude/tracking/track.py end-phase N

# Al finalizar la US
python .claude/tracking/track.py end-tracking
```

Las instrucciones están en secciones `🔴 Acción Requerida` de cada archivo de fase, lo que garantiza que el agente las ejecuta en lugar de interpretarlas como documentación.

> **Nota histórica:** El diseño original contemplaba llamadas directas a la API Python (`tracker.start_phase(N)`, `tracker.end_phase(N)`). Ese enfoque fue reemplazado en v1.1 porque el agente interpretaba esos bloques de código como ejemplos de documentación y no los ejecutaba (OBS-001). En v1.3 se creó `track.py` como punto de entrada CLI dedicado, reemplazando la referencia errónea a `time_tracker.py` como CLI que nunca existió.

**API Python de referencia (para desarrollo de nuevos skills de tracking):**
```python
# Al inicio
tracker = TimeTracker(us_id, us_title, us_points, producto)
tracker.start_tracking()

# Cada fase
tracker.start_phase(N, phase_name)
# ... trabajo ...
tracker.end_phase(N)

# Al final
tracker.end_tracking()
```

## Extensibilidad

**Para agregar nuevos skills de tracking:**
1. Crear directorio `.claude/skills/track-{nombre}/`
2. Crear `skill.md` con instrucciones
3. Usar funciones de `tracking.reports` para formateo
4. Leer archivos JSON de `.claude/tracking/`

**Para modificar persistencia:**
- Actualmente: JSON local
- Futuro: SQLite, CSV, integración con APIs externas

## Decisiones de Diseño

**¿Por qué JSON y no base de datos?**
- Simplicidad: No requiere setup adicional
- Portabilidad: Los archivos son fáciles de compartir
- Debugging: JSON es legible por humanos
- Suficiente para ~100s de USs sin problemas de rendimiento

**¿Por qué dataclasses?**
- Type hints claros
- Propiedades calculadas automáticas
- Serialización simple con asdict()
- Código limpio y mantenible

**¿Por qué skills separados?**
- Modularidad: Cada comando es independiente
- Reutilización: Skills pueden invocarse desde otros skills
- Mantenibilidad: Fácil agregar/modificar comandos
