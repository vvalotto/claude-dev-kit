#!/usr/bin/env python3
"""
tracker_cli.py — CLI wrapper para TimeTracker.

Permite usar TimeTracker desde Bash entre fases del skill /implement-us.
Carga el estado desde JSON en cada llamada y lo persiste al finalizar.

Uso:
    python .claude/tracking/tracker_cli.py init US-1.0.0 "Título" 3 producto
    python .claude/tracking/tracker_cli.py start-phase 0 "Validación de Contexto"
    python .claude/tracking/tracker_cli.py end-phase 0
    python .claude/tracking/tracker_cli.py start-task task_001 "Nombre" dominio 20
    python .claude/tracking/tracker_cli.py end-task task_001 src/modulo.py
    python .claude/tracking/tracker_cli.py status
    python .claude/tracking/tracker_cli.py end [us_id]
"""
import sys
import json
import argparse
from glob import glob
from pathlib import Path

# Hacer importable el módulo tracking desde el directorio del proyecto
sys.path.insert(0, str(Path(__file__).parent.parent))

from tracking.time_tracker import TimeTracker


# =============================================================================
# Lookup del tracker activo
# =============================================================================

def _find_active_us_id() -> str:
    """Busca el us_id del tracker activo (completed_at == null).

    Returns:
        us_id del tracker activo

    Raises:
        RuntimeError: Si hay 0 o más de 1 tracker activo
    """
    files = glob(".claude/tracking/*-tracking.json")
    activos = []
    for f in files:
        try:
            data = json.loads(Path(f).read_text())
            if data["timeline"]["completed_at"] is None:
                activos.append(data["metadata"]["us_id"])
        except (json.JSONDecodeError, KeyError):
            continue

    if len(activos) == 0:
        raise RuntimeError(
            "No hay trackers activos.\n"
            "Inicializar con: tracker_cli.py init <us_id> <title> <points> <product>"
        )
    if len(activos) > 1:
        lista = ", ".join(activos)
        raise RuntimeError(
            f"Múltiples trackers activos: {lista}\n"
            "Cerrar los huérfanos antes de continuar:\n"
            "  tracker_cli.py end <us_id>"
        )
    return activos[0]


# =============================================================================
# Subcomandos
# =============================================================================

def cmd_init(args: argparse.Namespace) -> None:
    """Inicializa un nuevo tracker para una US."""
    tracker = TimeTracker(
        us_id=args.us_id,
        us_title=args.title,
        us_points=args.points,
        producto=args.product,
    )
    tracker.start_tracking()
    print(f"✅ Tracker iniciado: {args.us_id} — {args.title}")
    print(f"   Archivo: .claude/tracking/{args.us_id}-tracking.json")


def cmd_start_phase(args: argparse.Namespace) -> None:
    """Inicia una fase en el tracker activo."""
    us_id = args.us_id or _find_active_us_id()
    tracker = TimeTracker.load(us_id)
    tracker.start_phase(args.phase_number, args.phase_name)
    print(f"▶️  Fase {args.phase_number} iniciada: {args.phase_name} [{us_id}]")


def cmd_end_phase(args: argparse.Namespace) -> None:
    """Cierra una fase en el tracker activo."""
    us_id = args.us_id or _find_active_us_id()
    tracker = TimeTracker.load(us_id)
    tracker.end_phase(args.phase_number)
    phase = tracker._get_phase(args.phase_number)
    elapsed = f"{phase.elapsed_seconds}s" if phase else "?"
    print(f"✅ Fase {args.phase_number} completada [{us_id}] — {elapsed}")


def cmd_start_task(args: argparse.Namespace) -> None:
    """Inicia una tarea dentro de la fase activa."""
    us_id = args.us_id or _find_active_us_id()
    tracker = TimeTracker.load(us_id)
    tracker.start_task(args.task_id, args.task_name, args.task_type, args.estimated_minutes)
    print(f"▶️  Tarea iniciada: {args.task_id} — {args.task_name} [{us_id}]")


def cmd_end_task(args: argparse.Namespace) -> None:
    """Cierra una tarea en la fase activa."""
    us_id = args.us_id or _find_active_us_id()
    tracker = TimeTracker.load(us_id)
    tracker.end_task(args.task_id, args.file_created)
    print(f"✅ Tarea completada: {args.task_id} [{us_id}]")
    if args.file_created:
        print(f"   Archivo: {args.file_created}")


def cmd_status(args: argparse.Namespace) -> None:
    """Muestra el estado actual del tracker activo."""
    us_id = args.us_id or _find_active_us_id()
    tracker = TimeTracker.load(us_id)
    status = tracker.get_status()

    print(f"\n📊 Tracking: {us_id}")
    print(f"   Estado:   {status['status']}")
    if status.get("current_phase"):
        print(f"   Fase:     {status['current_phase']}")
    if status.get("current_task"):
        print(f"   Tarea:    {status['current_task']}")

    elapsed_min = status.get("elapsed_seconds", 0) // 60
    effective_min = status.get("effective_seconds", 0) // 60
    print(f"   Elapsed:  {elapsed_min} min  (efectivo: {effective_min} min)")

    total = status.get("total_tasks", 0)
    done = status.get("completed_tasks", 0)
    if total > 0:
        print(f"   Tareas:   {done}/{total} completadas")
    print()


def cmd_end(args: argparse.Namespace) -> None:
    """Cierra el tracker completo de una US."""
    us_id = args.us_id or _find_active_us_id()
    tracker = TimeTracker.load(us_id)
    tracker.end_tracking()

    elapsed = 0
    if tracker.started_at and tracker.completed_at:
        elapsed = int((tracker.completed_at - tracker.started_at).total_seconds()) // 60

    print(f"🏁 Tracking finalizado: {us_id}")
    print(f"   Fases completadas: {len(tracker.phases)}")
    print(f"   Tiempo total: {elapsed} min")
    print(f"   Archivo: {tracker.storage_path}")


# =============================================================================
# Parser principal
# =============================================================================

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tracker_cli.py",
        description="CLI wrapper para TimeTracker — usar desde phase files del skill /implement-us",
    )
    sub = parser.add_subparsers(dest="command", metavar="SUBCOMANDO")
    sub.required = True

    # init
    p_init = sub.add_parser("init", help="Inicializar tracker para una nueva US")
    p_init.add_argument("us_id", help="ID de la US (ej: US-1.0.0, INC-2.0)")
    p_init.add_argument("title", help="Título de la US")
    p_init.add_argument("points", type=int, help="Story points")
    p_init.add_argument("product", help="Nombre del producto")
    p_init.set_defaults(func=cmd_init)

    # start-phase
    p_sp = sub.add_parser("start-phase", help="Iniciar una fase")
    p_sp.add_argument("phase_number", type=int, help="Número de fase (0-9)")
    p_sp.add_argument("phase_name", help="Nombre descriptivo de la fase")
    p_sp.add_argument("--us-id", dest="us_id", default=None, help="us_id explícito (opcional)")
    p_sp.set_defaults(func=cmd_start_phase)

    # end-phase
    p_ep = sub.add_parser("end-phase", help="Cerrar una fase")
    p_ep.add_argument("phase_number", type=int, help="Número de fase (0-9)")
    p_ep.add_argument("--us-id", dest="us_id", default=None, help="us_id explícito (opcional)")
    p_ep.set_defaults(func=cmd_end_phase)

    # start-task
    p_st = sub.add_parser("start-task", help="Iniciar una tarea")
    p_st.add_argument("task_id", help="ID de la tarea (ej: task_001)")
    p_st.add_argument("task_name", help="Nombre de la tarea")
    p_st.add_argument("task_type", help="Tipo (dominio, infra, test, etc.)")
    p_st.add_argument("estimated_minutes", type=float, help="Estimación en minutos")
    p_st.add_argument("--us-id", dest="us_id", default=None, help="us_id explícito (opcional)")
    p_st.set_defaults(func=cmd_start_task)

    # end-task
    p_et = sub.add_parser("end-task", help="Cerrar una tarea")
    p_et.add_argument("task_id", help="ID de la tarea")
    p_et.add_argument("file_created", nargs="?", default=None, help="Archivo principal creado (opcional)")
    p_et.add_argument("--us-id", dest="us_id", default=None, help="us_id explícito (opcional)")
    p_et.set_defaults(func=cmd_end_task)

    # status
    p_status = sub.add_parser("status", help="Ver estado del tracker activo")
    p_status.add_argument("--us-id", dest="us_id", default=None, help="us_id explícito (opcional)")
    p_status.set_defaults(func=cmd_status)

    # end
    p_end = sub.add_parser("end", help="Finalizar el tracker completo")
    p_end.add_argument("us_id", nargs="?", default=None, help="us_id (opcional, detecta el activo)")
    p_end.set_defaults(func=cmd_end)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.func(args)
    except (FileNotFoundError, RuntimeError, ValueError) as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
