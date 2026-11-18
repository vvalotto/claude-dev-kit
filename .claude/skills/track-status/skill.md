# Ver Estado del Tracking

Muestra el estado actual del tracking de tiempo para la Historia de Usuario en progreso.

## Uso

```bash
/track-status
```

## Instrucciones

Cuando este skill es invocado:

### 1. Buscar tracking activo

```python
from pathlib import Path
import json

tracking_dir = Path(".claude/tracking")
if not tracking_dir.exists():
    # Mostrar mensaje: no hay tracking activo
    return

# Buscar archivo sin completed_at
active_file = None
for json_file in tracking_dir.glob("*-tracking.json"):
    with open(json_file, 'r') as f:
        data = json.load(f)
        if data.get("timeline", {}).get("completed_at") is None:
            active_file = json_file
            break

if not active_file:
    # Mostrar mensaje: no hay tracking activo
    return
```

### 2. Cargar tracker y obtener estado

```python
from tracking import TimeTracker

# Restaurar el estado completo (fases, tareas, pausas) desde el JSON activo
tracker = TimeTracker.from_json(active_file)

# Obtener status
status = tracker.get_status()
```

### 3. Formatear output

```python
# Calcular duraciones
elapsed_h = status["elapsed_seconds"] // 3600
elapsed_m = (status["elapsed_seconds"] % 3600) // 60
elapsed_s = status["elapsed_seconds"] % 60

effective_h = status["effective_seconds"] // 3600
effective_m = (status["effective_seconds"] % 3600) // 60

paused_m = status["paused_seconds"] // 60

# Determinar emoji y estado
if status["status"] == "paused":
    emoji = "⏸️"
    status_text = "Pausado"
elif status.get("current_phase"):
    emoji = "▶️"
    status_text = "En progreso"
else:
    emoji = "⏹️"
    status_text = "Detenido"
```

### 4. Mostrar resultado

```markdown
# 📊 Estado del Tracking - {us_id}

**Historia de Usuario:** {us_id} - {us_title}
**Producto:** {producto}
**Puntos:** {us_points}
**Estado:** {emoji} {status_text}

## ⏱️ Tiempo

| Métrica | Valor |
|---------|-------|
| **Inicio** | {started_at formateado} |
| **Tiempo transcurrido** | {elapsed_h}h {elapsed_m}m {elapsed_s}s |
| **Tiempo efectivo** | {effective_h}h {effective_m}m |
| **Tiempo pausado** | {paused_m}m |

## 📍 Progreso Actual

{if current_phase}
- **Fase actual:** Fase {phase_number} - {phase_name}
- **Tarea actual:** {task_name o "Sin tarea activa"}
- **Tareas completadas:** {completed_tasks}/{total_tasks} ({percentage}%)
{else}
- **Estado:** Entre fases
{endif}

{if current_pause}
## ⏸️ Pausa Activa

- **Razón:** {pause_reason o "Sin razón"}
- **Desde:** {pause_started_at}
- **Duración:** {pause_duration} minutos

**Para reanudar:** `/track-resume`
{endif}

---

**Ver reporte completo:** `/track-report {us_id}`
```

## Caso Sin Tracking

Si no hay tracking activo:

```markdown
# ℹ️ No hay tracking activo

No se encontró ninguna Historia de Usuario en progreso.

**Para iniciar tracking:**
```bash
/implement-us US-XXX
```

**Ver historial:**
```bash
/track-history
```
```
