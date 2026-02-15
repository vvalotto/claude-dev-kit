"""Test manual del TimeTracker básico."""
from tracking import TimeTracker, Task, Phase, Pause
from datetime import datetime, timezone
import json
from pathlib import Path


def test_basic_flow():
    """Test del flujo básico de tracking."""
    
    print("🧪 Iniciando tests del TimeTracker...")
    print()
    
    # 1. Crear tracker
    tracker = TimeTracker(
        us_id="US-TEST-001",
        us_title="Test del sistema de tracking",
        us_points=1,
        producto="test_producto"
    )
    print("✅ Tracker creado")
    
    # 2. Iniciar tracking
    tracker.start_tracking()
    assert tracker.started_at is not None
    print("✅ Tracking iniciado")
    
    # 3. Iniciar fase
    tracker.start_phase(0, "Fase de Test")
    assert tracker.current_phase is not None
    assert tracker.current_phase.phase_number == 0
    print("✅ Fase 0 iniciada")
    
    # 4. Finalizar fase
    tracker.end_phase(0)
    assert tracker.phases[0].status == "completed"
    assert tracker.current_phase is None
    print("✅ Fase 0 finalizada")
    
    # 5. Finalizar tracking
    tracker.end_tracking()
    assert tracker.completed_at is not None
    print("✅ Tracking finalizado")
    
    # 6. Verificar archivo JSON
    json_path = Path(".claude/tracking/US-TEST-001-tracking.json")
    assert json_path.exists()
    print(f"✅ Archivo JSON creado: {json_path}")
    
    # 7. Leer y validar JSON
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    assert data["metadata"]["us_id"] == "US-TEST-001"
    assert len(data["phases"]) == 1
    print("✅ JSON válido")
    
    # 8. Limpiar
    json_path.unlink()
    print("✅ Limpieza completada")
    
    print()
    print("🎉 Todos los tests pasaron exitosamente")


if __name__ == "__main__":
    test_basic_flow()
