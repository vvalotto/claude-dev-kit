#!/usr/bin/env python3
"""
CLI de tracking para el skill /implement-us.

Uso:
    python .claude/tracking/track.py start-phase <N> "<nombre>" --us <US_ID>
    python .claude/tracking/track.py end-phase <N> [--us <US_ID>]
    python .claude/tracking/track.py start-task "<nombre>" [--us <US_ID>]
    python .claude/tracking/track.py end-task "<nombre>" [--us <US_ID>]
    python .claude/tracking/track.py end-tracking [--us <US_ID>]
"""
import argparse
import json
import sys
from pathlib import Path

# Asegurar que el directorio raíz del proyecto esté en el path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tracking.time_tracker import TimeTracker


def _find_active_tracking() -> Path | None:
    """Busca el archivo de tracking activo (sin completed_at)."""
    tracking_dir = Path(".claude/tracking")
    if not tracking_dir.exists():
        return None
    for json_file in sorted(tracking_dir.glob("*-tracking.json")):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if data.get("timeline", {}).get("completed_at") is None:
                return json_file
        except (json.JSONDecodeError, OSError):
            continue
    return None


def _load_tracker(us_id: str | None) -> TimeTracker | None:
    """Carga el tracker activo o el correspondiente al US_ID dado."""
    if us_id:
        path = Path(f".claude/tracking/{us_id}-tracking.json")
        if path.exists():
            return TimeTracker.from_json(path)
        return None
    tracking_file = _find_active_tracking()
    if tracking_file:
        return TimeTracker.from_json(tracking_file)
    return None


def cmd_start_phase(args: argparse.Namespace) -> None:
    phase_num: int = args.phase
    phase_name: str = args.name
    us_id: str | None = args.us

    tracker = _load_tracker(us_id)

    if tracker is None:
        if phase_num != 0:
            print(
                f"ERROR: No hay tracking activo. Usá --us <US_ID> para especificar la US.",
                file=sys.stderr,
            )
            sys.exit(1)
        if not us_id:
            print(
                "ERROR: Para iniciar tracking en fase 0 usá --us <US_ID>.",
                file=sys.stderr,
            )
            sys.exit(1)
        # Crear tracking nuevo para la fase 0
        tracker = TimeTracker(
            us_id=us_id,
            us_title=us_id,
            us_points=0,
            producto="",
        )
        tracker.start_tracking()

    tracker.start_phase(phase_num, phase_name)
    print(f"▶  Fase {phase_num} iniciada: {phase_name}")


def cmd_end_phase(args: argparse.Namespace) -> None:
    tracker = _load_tracker(args.us)
    if tracker is None:
        print("ERROR: No hay tracking activo.", file=sys.stderr)
        sys.exit(1)
    tracker.end_phase(args.phase)
    print(f"✓  Fase {args.phase} finalizada")


def cmd_start_task(args: argparse.Namespace) -> None:
    tracker = _load_tracker(args.us)
    if tracker is None:
        print("ERROR: No hay tracking activo.", file=sys.stderr)
        sys.exit(1)
    if tracker.current_phase is None:
        print("ERROR: No hay fase activa.", file=sys.stderr)
        sys.exit(1)
    task_id = f"task_{len(tracker.current_phase.tasks) + 1:03d}"
    tracker.start_task(task_id, args.name, "generic", 0)
    print(f"▶  Tarea iniciada: {args.name}")


def cmd_end_task(args: argparse.Namespace) -> None:
    tracker = _load_tracker(args.us)
    if tracker is None:
        print("ERROR: No hay tracking activo.", file=sys.stderr)
        sys.exit(1)
    if tracker.current_task is None:
        print("WARN: No hay tarea activa.", file=sys.stderr)
        return
    tracker.end_task(tracker.current_task.task_id)
    print(f"✓  Tarea finalizada: {args.name}")


def cmd_end_tracking(args: argparse.Namespace) -> None:
    tracker = _load_tracker(args.us)
    if tracker is None:
        print("ERROR: No hay tracking activo.", file=sys.stderr)
        sys.exit(1)
    tracker.end_tracking()
    print(f"✓  Tracking finalizado: {tracker.us_id}")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="track.py",
        description="CLI de tracking para /implement-us",
    )
    sub = parser.add_subparsers(dest="command", metavar="COMANDO")

    sp = sub.add_parser("start-phase", help="Iniciar una fase")
    sp.add_argument("phase", type=int, metavar="N", help="Número de fase (0-9)")
    sp.add_argument("name", metavar="NOMBRE", help="Nombre de la fase")
    sp.add_argument("--us", metavar="US_ID", help="ID de la Historia de Usuario")

    ep = sub.add_parser("end-phase", help="Finalizar una fase")
    ep.add_argument("phase", type=int, metavar="N")
    ep.add_argument("--us", metavar="US_ID")

    st = sub.add_parser("start-task", help="Iniciar una tarea")
    st.add_argument("name", metavar="NOMBRE")
    st.add_argument("--us", metavar="US_ID")

    et = sub.add_parser("end-task", help="Finalizar una tarea")
    et.add_argument("name", metavar="NOMBRE")
    et.add_argument("--us", metavar="US_ID")

    etk = sub.add_parser("end-tracking", help="Finalizar el tracking completo")
    etk.add_argument("--us", metavar="US_ID")

    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    commands = {
        "start-phase": cmd_start_phase,
        "end-phase": cmd_end_phase,
        "start-task": cmd_start_task,
        "end-task": cmd_end_task,
        "end-tracking": cmd_end_tracking,
    }

    if args.command not in commands:
        parser.print_help()
        sys.exit(1)

    commands[args.command](args)


if __name__ == "__main__":
    main()
