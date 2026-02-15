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

    # Insights
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
