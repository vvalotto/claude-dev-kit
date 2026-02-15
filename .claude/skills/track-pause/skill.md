# Pausar Tracking de Tiempo

Pausa temporalmente el tracking de tiempo de la Historia de Usuario actual.

## Uso

```bash
/track-pause [razón]
```

**Parámetros:**
- `razón` (opcional): Motivo de la pausa

**Ejemplos:**
```bash
/track-pause "Reunión de planning"
/track-pause
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

### 2. Cargar tracker y pausar

```python
from tracking import TimeTracker

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

# Pausar
try:
    tracker.pause(reason=razón or "")
except ValueError as e:
    # Mostrar error: ya hay pausa activa
    return
```

### 3. Mostrar confirmación

```markdown
# ⏸️ Tracking Pausado

**Historia de Usuario:** {us_id} - {us_title}
**Razón:** {razón o "Sin razón especificada"}
**Pausado en:** {timestamp actual}

El tracking está pausado. El tiempo transcurrido durante la pausa NO se contabilizará.

**Para reanudar el trabajo:** `/track-resume`
```

## Manejo de Errores

**Si no hay tracking activo:**

```markdown
# ❌ Error: No hay tracking activo

No se encontró ninguna Historia de Usuario en progreso.

**Para iniciar tracking:**
```bash
/implement-us US-XXX
```
```

**Si ya hay pausa activa:**

```markdown
# ⚠️ Error: Ya hay una pausa activa

El tracking ya está pausado.

**Para reanudar:** `/track-resume`
```
