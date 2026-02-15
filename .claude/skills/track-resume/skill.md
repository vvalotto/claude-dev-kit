# Reanudar Tracking de Tiempo

Reanuda el tracking después de una pausa con `/track-pause`.

## Uso

```bash
/track-resume
```

## Instrucciones

Cuando este skill es invocado:

### 1. Buscar tracking activo

```python
from pathlib import Path
import json

tracking_dir = Path(".claude/tracking")
if not tracking_dir.exists():
    # Mostrar error: no hay tracking activo
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
    # Mostrar error: no hay tracking activo
    return
```

### 2. Cargar tracker y reanudar

```python
from tracking import TimeTracker
from datetime import datetime, timezone

# Leer metadata
with open(active_file, 'r') as f:
    data = json.load(f)

metadata = data["metadata"]
tracker = TimeTracker(
    us_id=metadata["us_id"],
    us_title=metadata["us_title"],
    us_points=metadata["us_points"],
    producto=metadata["producto"]
)

# Verificar pausa activa
if not tracker.current_pause:
    # Mostrar error: no hay pausa activa
    return

# Calcular duración antes de resumir
now = datetime.now(timezone.utc)
pause_seconds = int((now - tracker.current_pause.started_at).total_seconds())
pause_mins = pause_seconds // 60
pause_reason = tracker.current_pause.reason

# Reanudar
tracker.resume()
```

### 3. Mostrar confirmación

```markdown
# ▶️ Tracking Reanudado

**Historia de Usuario:** {us_id} - {us_title}

## Pausa Finalizada

- **Razón:** {pause_reason o "Sin razón"}
- **Duración:** {pause_mins} minutos

El trabajo se ha reanudado. El tracking está activo nuevamente.

**Ver estado actual:** `/track-status`
```

## Manejo de Errores

**Si no hay tracking activo:**

```markdown
# ❌ Error: No hay tracking activo

No se encontró ninguna Historia de Usuario en progreso.
```

**Si no hay pausa activa:**

```markdown
# ⚠️ Error: No hay pausa activa

El tracking está actualmente en ejecución, no pausado.

**Para pausar:** `/track-pause [razón]`
**Ver estado:** `/track-status`
```
