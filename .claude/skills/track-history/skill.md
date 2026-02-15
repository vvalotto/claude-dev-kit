# Ver Historial de Tracking

Muestra el historial de todas las Historias de Usuario trackeadas.

## Uso

```bash
/track-history [--last N]
```

**Parámetros:**
- `--last N` (opcional): Mostrar solo los últimos N registros

**Ejemplos:**
```bash
/track-history
/track-history --last 5
/track-history --last 10
```

## Instrucciones

Cuando este skill es invocado:

### 1. Parsear parámetros

```python
import re

last_n = None
if "--last" in args:
    match = re.search(r'--last\s+(\d+)', args)
    if match:
        last_n = int(match.group(1))
```

### 2. Generar historial

```python
from pathlib import Path
from tracking.reports import generate_history_table

tracking_dir = Path(".claude/tracking")

if not tracking_dir.exists():
    # Mostrar error: no hay historial
    return

# Generar tabla de historial
history = generate_history_table(tracking_dir, last_n)
```

### 3. Mostrar historial

Imprimir el historial generado por `generate_history_table()`.

El historial incluye:
- Tabla con últimas USs completadas
- Estadísticas agregadas (total USs, puntos, tiempo)
- Promedio de tiempo por punto

## Manejo de Errores

**Si .claude/tracking/ no existe:**

```markdown
# ℹ️ No hay historial disponible

El directorio de tracking no existe aún.

**Para iniciar tracking:**
```bash
/implement-us US-XXX
```
```

**Si .claude/tracking/ está vacío:**

```markdown
# ℹ️ No hay registros de tracking

No se encontraron archivos de tracking.

**Para iniciar tracking:**
```bash
/implement-us US-XXX
```
```
