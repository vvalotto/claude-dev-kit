# TICKET-041: Crear Skills de Reporting

**Fase:** 5 - Sistema de Tracking
**Sprint:** 2
**Estado:** 📋 Pendiente
**Prioridad:** Media
**Estimación:** 1 hora
**Asignado a:** Claude Code

---

## Descripción

Crear los 2 skills de reporting que permiten generar reportes detallados del tracking y ver el historial de Historias de Usuario completadas:

1. `/track-report [us_id]` - Generar reporte detallado de una US (actual o especificada)
2. `/track-history [--last N]` - Ver historial de tracking de USs completadas

Estos skills son esenciales para:
- Análisis retrospectivo de implementaciones
- Identificación de patrones de estimación
- Mejora continua de velocidad
- Auditoría de tiempo invertido

---

## Criterios de Aceptación

- [ ] Módulo `tracking/reports.py` creado con funciones de formateo
- [ ] Skill `/track-report` creado y funcional:
  - [ ] Acepta parámetro opcional `us_id`
  - [ ] Si no se especifica us_id, usa el tracking actual
  - [ ] Lee archivo JSON de tracking
  - [ ] Genera reporte completo en markdown
  - [ ] Incluye: resumen, fases, tareas, pausas, métricas
- [ ] Skill `/track-history` creado y funcional:
  - [ ] Lista todos los archivos de tracking en `.claude/tracking/`
  - [ ] Acepta parámetro opcional `--last N`
  - [ ] Formatea tabla con historial
  - [ ] Muestra estadísticas agregadas
- [ ] Reportes formateados en markdown legible
- [ ] Tablas con alineación correcta
- [ ] Cálculos de métricas precisos (varianza, porcentajes)

---

## Dependencias

**Depende de:**
- ✅ TICKET-038: Análisis completado
- ✅ TICKET-039: Módulo core migrado
- ✅ TICKET-040: Skills básicos creados

**Bloquea a:**
- TICKET-042: Integración con implement-us

---

## Estructura de Archivos

```
tracking/
├── time_tracker.py          # Ya existe
├── __init__.py              # Ya existe
├── reports.py               # NUEVO - funciones de reporting
└── README.md                # Ya existe

.claude/
└── skills/
    ├── track-report/
    │   └── skill.md         # NUEVO
    └── track-history/
        └── skill.md         # NUEVO
```

---

## Módulo: tracking/reports.py

### Contenido del Módulo

```python
"""
Funciones de generación de reportes de tracking.

Este módulo proporciona funciones para formatear reportes de tracking
en formato markdown para visualización en Claude Code.
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
import json
from datetime import datetime


def format_duration(seconds: int) -> str:
    """Formatea duración en segundos a formato legible.

    Args:
        seconds: Duración en segundos

    Returns:
        String formateado (ej: "2h 15m 30s")
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if secs > 0 or not parts:
        parts.append(f"{secs}s")

    return " ".join(parts)


def format_timestamp(iso_timestamp: Optional[str]) -> str:
    """Formatea timestamp ISO a formato legible.

    Args:
        iso_timestamp: Timestamp en formato ISO 8601 o None

    Returns:
        String formateado (ej: "2026-02-15 10:30:00 UTC") o "-"
    """
    if not iso_timestamp:
        return "-"

    try:
        dt = datetime.fromisoformat(iso_timestamp.replace('Z', '+00:00'))
        return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
    except Exception:
        return iso_timestamp


def generate_full_report(tracking_data: Dict[str, Any]) -> str:
    """Genera reporte completo de tracking.

    Args:
        tracking_data: Diccionario con datos de tracking (desde JSON)

    Returns:
        String con reporte completo en formato markdown
    """
    metadata = tracking_data["metadata"]
    timeline = tracking_data["timeline"]
    phases = tracking_data["phases"]
    pauses = tracking_data.get("pauses", [])
    summary = tracking_data["summary"]

    # Header
    report = f"# 📈 Reporte de Tracking - {metadata['us_id']}\n\n"
    report += f"**Historia de Usuario:** {metadata['us_id']} - {metadata['us_title']}\n"
    report += f"**Producto:** {metadata['producto']}\n"
    report += f"**Puntos:** {metadata['us_points']} puntos\n"

    # Estado
    if timeline['completed_at']:
        report += f"**Estado:** ✅ Completado\n"
    else:
        report += f"**Estado:** ▶️ En progreso\n"

    report += "\n---\n\n"

    # Resumen de Tiempo
    report += "## ⏱️ Resumen de Tiempo\n\n"
    report += "| Métrica | Valor |\n"
    report += "|---------|-------|\n"
    report += f"| **Inicio** | {format_timestamp(timeline['started_at'])} |\n"
    report += f"| **Fin** | {format_timestamp(timeline['completed_at'])} |\n"
    report += f"| **Tiempo total** | {format_duration(timeline['total_elapsed_seconds'])} |\n"
    report += f"| **Tiempo efectivo** | {format_duration(timeline['effective_seconds'])} |\n"
    report += f"| **Tiempo pausado** | {format_duration(timeline['paused_seconds'])} |\n"

    report += "\n---\n\n"

    # Fases Ejecutadas
    report += "## 📊 Fases Ejecutadas\n\n"
    report += "| Fase | Nombre | Duración | Tareas | Estado |\n"
    report += "|------|--------|----------|--------|--------|\n"

    for phase in phases:
        status_emoji = "✅" if phase['status'] == "completed" else "▶️"
        duration = format_duration(phase['elapsed_seconds'])
        report += f"| {phase['phase_number']} | {phase['phase_name']} | "
        report += f"{duration} | {len(phase['tasks'])} | {status_emoji} {phase['status'].title()} |\n"

    report += f"\n**Total:** {len(phases)} fases | "
    report += f"{format_duration(timeline['effective_seconds'])} | "
    report += f"{summary['total_tasks']} tareas\n"

    # Detalle de Tareas por Fase
    for phase in phases:
        if phase['tasks']:
            report += f"\n---\n\n## 📝 Detalle de Tareas (Fase {phase['phase_number']}: {phase['phase_name']})\n\n"
            report += "| ID | Nombre | Tipo | Estimado | Real | Varianza | Archivo |\n"
            report += "|----|--------|------|----------|------|----------|---------|\n"

            for task in phase['tasks']:
                variance_sign = "+" if task.get('variance_minutes', 0) >= 0 else ""
                variance_pct = task.get('variance_percent', 0)
                report += f"| {task['task_id']} | {task['task_name']} | {task['task_type']} | "
                report += f"{task['estimated_minutes']}m | {task.get('actual_minutes', 0)}m | "
                report += f"{variance_sign}{task.get('variance_minutes', 0)}m ({variance_sign}{variance_pct:.1f}%) | "
                report += f"{task.get('file_created', '-')} |\n"

    # Pausas
    if pauses:
        report += "\n---\n\n## ⏸️ Pausas Registradas\n\n"
        report += "| ID | Inicio | Fin | Duración | Razón |\n"
        report += "|----|--------|-----|----------|-------|\n"

        for pause in pauses:
            report += f"| {pause['pause_id']} | {format_timestamp(pause['started_at'])} | "
            report += f"{format_timestamp(pause['resumed_at'])} | "
            report += f"{format_duration(pause['duration_seconds'])} | "
            report += f"{pause.get('reason', '-')} |\n"

        report += f"\n**Total pausado:** {format_duration(timeline['paused_seconds'])}\n"

    # Métricas Finales
    report += "\n---\n\n## 📊 Métricas Finales\n\n"
    report += "| Métrica | Estimado | Real | Varianza |\n"
    report += "|---------|----------|------|----------|\n"

    est_total = summary['estimated_total_minutes']
    act_total = summary['actual_total_minutes']
    var_total = summary['variance_minutes']
    var_pct = summary['variance_percent']

    report += f"| **Tiempo total** | {est_total}m ({est_total/60:.1f}h) | "
    report += f"{act_total}m ({act_total/60:.1f}h) | "
    variance_sign = "+" if var_total >= 0 else ""
    report += f"{variance_sign}{var_total}m ({variance_sign}{var_pct:.1f}%) |\n"

    if metadata['us_points'] > 0:
        est_per_point = est_total / metadata['us_points']
        act_per_point = act_total / metadata['us_points']
        var_per_point = act_per_point - est_per_point
        report += f"| **Por punto** | {est_per_point:.1f}m/punto | "
        report += f"{act_per_point:.1f}m/punto | "
        variance_sign = "+" if var_per_point >= 0 else ""
        report += f"{variance_sign}{var_per_point:.1f}m/punto |\n"

    report += f"| **Tareas totales** | {summary['total_tasks']} | {summary['completed_tasks']} | - |\n"

    # Insights (opcional)
    report += "\n---\n\n## 💡 Insights\n\n"
    if timeline['completed_at']:
        report += "- ✅ Implementación completada exitosamente\n"
    if var_pct > 25:
        report += f"- ⚠️ Varianza de +{var_pct:.1f}% sobre estimado (considerar para futuras USs de {metadata['us_points']} puntos)\n"
    elif var_pct < -10:
        report += f"- ✅ Implementación más rápida de lo estimado ({var_pct:.1f}%)\n"

    return report


def generate_history_table(tracking_dir: Path, last_n: Optional[int] = None) -> str:
    """Genera tabla de historial de tracking.

    Args:
        tracking_dir: Path al directorio .claude/tracking/
        last_n: Número de últimos registros a mostrar (None = todos)

    Returns:
        String con tabla de historial en markdown
    """
    # Leer todos los archivos de tracking
    tracking_files = sorted(
        tracking_dir.glob("*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True  # Más recientes primero
    )

    if last_n:
        tracking_files = tracking_files[:last_n]

    if not tracking_files:
        return "No se encontraron registros de tracking.\n"

    # Header
    history = "# 📚 Historial de Tracking\n\n"
    history += f"**Últimos {len(tracking_files)} registros**\n\n"
    history += "---\n\n## Historias de Usuario\n\n"
    history += "| US ID | Título | Puntos | Fecha | Duración | Estado |\n"
    history += "|-------|--------|--------|-------|----------|--------|\n"

    total_points = 0
    total_time = 0

    for file_path in tracking_files:
        with open(file_path, 'r') as f:
            data = json.load(f)

        metadata = data["metadata"]
        timeline = data["timeline"]

        us_id = metadata["us_id"]
        title = metadata["us_title"][:40] + "..." if len(metadata["us_title"]) > 40 else metadata["us_title"]
        points = metadata["us_points"]
        date = format_timestamp(timeline["started_at"]).split()[0]
        duration = format_duration(timeline["effective_seconds"])
        status = "✅ Completado" if timeline["completed_at"] else "▶️ En progreso"

        history += f"| {us_id} | {title} | {points} | {date} | {duration} | {status} |\n"

        total_points += points
        total_time += timeline["effective_seconds"]

    # Estadísticas
    history += "\n---\n\n## 📊 Estadísticas Generales\n\n"
    history += "| Métrica | Valor |\n"
    history += "|---------|-------|\n"
    history += f"| **Total USs** | {len(tracking_files)} |\n"
    history += f"| **Puntos totales** | {total_points} puntos |\n"
    history += f"| **Tiempo total** | {format_duration(total_time)} |\n"

    if total_points > 0:
        avg_per_point = total_time / total_points / 60
        history += f"| **Promedio por punto** | {avg_per_point:.1f}m/punto |\n"

    return history
```

---

## Skill 1: /track-report

### Archivo: .claude/skills/track-report/skill.md

```markdown
# Generar Reporte de Tracking

Genera un reporte detallado del tracking de tiempo para una Historia de Usuario.

Incluye:
- Resumen de tiempo (total, efectivo, pausado)
- Fases ejecutadas con duraciones
- Detalle de tareas por fase
- Pausas registradas
- Métricas finales y varianza
- Insights automáticos

## Uso

```bash
/track-report [us_id]
```

**Parámetros:**
- `us_id` (opcional): ID de la US (ej: US-001). Si no se especifica, usa el tracking actual.

## Ejemplos

```bash
# Reporte de tracking actual
/track-report

# Reporte de US específica
/track-report US-001
```

## Instrucciones

Cuando este skill es invocado:

1. **Determinar qué tracking reportar**
   - Si se proporciona `us_id`, buscar archivo `.claude/tracking/{us_id}-tracking.json`
   - Si no se proporciona `us_id`, buscar tracking actual (sin `completed_at`)
   - Si no existe el archivo, mostrar error

2. **Leer archivo de tracking**
   ```python
   from pathlib import Path
   import json

   tracking_path = Path(f".claude/tracking/{us_id}-tracking.json")
   with open(tracking_path, 'r') as f:
       tracking_data = json.load(f)
   ```

3. **Generar reporte**
   ```python
   from tracking.reports import generate_full_report

   report = generate_full_report(tracking_data)
   ```

4. **Mostrar reporte**
   - Imprimir el markdown generado por `generate_full_report()`

## Manejo de Errores

**Si no se encuentra el archivo:**
```markdown
# ❌ Error: Tracking no encontrado

No se encontró tracking para **{us_id}**.

**Archivos de tracking disponibles:**
{lista de archivos en .claude/tracking/}

**Ver historial:** `/track-history`
```

**Si .claude/tracking/ está vacío:**
```markdown
# ℹ️ No hay tracking disponible

No se encontraron archivos de tracking.

**Para iniciar tracking:**
```bash
/implement-us US-XXX
```
```
```

---

## Skill 2: /track-history

### Archivo: .claude/skills/track-history/skill.md

```markdown
# Ver Historial de Tracking

Muestra el historial de todas las Historias de Usuario trackeadas.

Incluye:
- Tabla con últimas USs completadas
- Estadísticas agregadas (total USs, puntos, tiempo)
- Promedio de tiempo por punto

## Uso

```bash
/track-history [--last N]
```

**Parámetros:**
- `--last N` (opcional): Mostrar solo los últimos N registros

## Ejemplos

```bash
# Ver todo el historial
/track-history

# Ver últimas 5 USs
/track-history --last 5

# Ver últimas 10 USs
/track-history --last 10
```

## Instrucciones

Cuando este skill es invocado:

1. **Parsear parámetros**
   ```python
   import re

   last_n = None
   if "--last" in args:
       match = re.search(r'--last\s+(\d+)', args)
       if match:
           last_n = int(match.group(1))
   ```

2. **Generar historial**
   ```python
   from pathlib import Path
   from tracking.reports import generate_history_table

   tracking_dir = Path(".claude/tracking")
   if not tracking_dir.exists():
       # Mostrar error
       return

   history = generate_history_table(tracking_dir, last_n)
   ```

3. **Mostrar historial**
   - Imprimir el markdown generado por `generate_history_table()`

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
```

---

## Checklist de Implementación

### Módulo tracking/reports.py
- [ ] Crear archivo `tracking/reports.py`
- [ ] Implementar función `format_duration()`
- [ ] Implementar función `format_timestamp()`
- [ ] Implementar función `generate_full_report()`
- [ ] Implementar función `generate_history_table()`
- [ ] Agregar docstrings completos
- [ ] Probar con datos reales de tracking

### Skill /track-report
- [ ] Crear directorio `.claude/skills/track-report/`
- [ ] Crear `skill.md` con contenido completo
- [ ] Implementar lógica de selección de tracking (actual vs us_id)
- [ ] Implementar lectura de archivo JSON
- [ ] Implementar llamada a `generate_full_report()`
- [ ] Implementar manejo de errores
- [ ] Probar con tracking completado
- [ ] Probar con tracking en progreso
- [ ] Probar con us_id inexistente

### Skill /track-history
- [ ] Crear directorio `.claude/skills/track-history/`
- [ ] Crear `skill.md` con contenido completo
- [ ] Implementar parsing de parámetro `--last N`
- [ ] Implementar llamada a `generate_history_table()`
- [ ] Implementar manejo de errores
- [ ] Probar con múltiples archivos de tracking
- [ ] Probar parámetro `--last N`
- [ ] Probar con directorio vacío

---

## Tests Manuales

### Test de /track-report

```bash
# Crear tracking de prueba (si no existe)
# ... usar tracking real o crear uno manualmente ...

# Generar reporte
/track-report US-001

# Verificar:
# - Tablas bien formateadas
# - Cálculos de varianza correctos
# - Timestamps legibles
# - Insights coherentes
```

### Test de /track-history

```bash
# Ver historial completo
/track-history

# Ver últimas 3
/track-history --last 3

# Verificar:
# - Tabla ordenada (más recientes primero)
# - Estadísticas correctas
# - Formato de fechas consistente
```

---

## Comandos

```bash
# Crear módulo de reports
touch tracking/reports.py

# Crear skills
mkdir -p .claude/skills/{track-report,track-history}
touch .claude/skills/track-report/skill.md
touch .claude/skills/track-history/skill.md

# Validar sintaxis Python
python -m py_compile tracking/reports.py

# Probar imports
python -c "from tracking.reports import generate_full_report; print('✅ OK')"
```

---

## Resultado

⬜ **PENDIENTE**

_A completar al finalizar el ticket._

**Archivos creados:**
- tracking/reports.py
- .claude/skills/track-report/skill.md
- .claude/skills/track-history/skill.md

**Commits esperados:**
1. `feat(tracking): crear módulo reports.py con funciones de formateo (TICKET-041)`
2. `feat(skills): crear skills de reporting (/track-report, /track-history) (TICKET-041)`
