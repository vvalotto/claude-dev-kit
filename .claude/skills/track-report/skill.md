# Generar Reporte de Tracking

Genera un reporte detallado del tracking de tiempo para una Historia de Usuario.

## Uso

```bash
/track-report [us_id]
```

**Parámetros:**
- `us_id` (opcional): ID de la US. Si no se especifica, usa el tracking actual.

**Ejemplos:**
```bash
/track-report
/track-report US-001
```

## Instrucciones

Cuando este skill es invocado:

### 1. Determinar archivo de tracking

```python
from pathlib import Path
import json

tracking_dir = Path(".claude/tracking")

if us_id:
    # US específica
    tracking_file = tracking_dir / f"{us_id}-tracking.json"
    if not tracking_file.exists():
        # Mostrar error: tracking no encontrado
        return
else:
    # Tracking actual (sin completed_at)
    tracking_file = None
    if tracking_dir.exists():
        for json_file in tracking_dir.glob("*-tracking.json"):
            with open(json_file, 'r') as f:
                data = json.load(f)
                if data.get("timeline", {}).get("completed_at") is None:
                    tracking_file = json_file
                    break

    if not tracking_file:
        # Mostrar error: no hay tracking activo
        return
```

### 2. Generar reporte

```python
from tracking.reports import generate_full_report

# Leer datos de tracking
with open(tracking_file, 'r') as f:
    tracking_data = json.load(f)

# Generar reporte completo
report = generate_full_report(tracking_data)
```

### 3. Mostrar reporte

Imprimir el reporte generado por `generate_full_report()`.

El reporte incluye:
- Resumen de tiempo (total, efectivo, pausado)
- Fases ejecutadas con duraciones
- Pausas registradas
- Métricas finales con varianza
- Insights automáticos

## Manejo de Errores

**Si no se encuentra el archivo:**

```markdown
# ❌ Error: Tracking no encontrado

No se encontró tracking para **{us_id}**.

**Ver historial:** `/track-history`
```

**Si no hay tracking activo:**

```markdown
# ℹ️ No hay tracking activo

No se encontró ninguna Historia de Usuario en progreso.

**Para iniciar tracking:**
```bash
/implement-us US-XXX
```
```
