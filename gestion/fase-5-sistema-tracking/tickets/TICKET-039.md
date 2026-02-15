# TICKET-039: Migrar Módulo Core time_tracker.py con Modelos de Datos

**Fase:** 5 - Sistema de Tracking
**Sprint:** 2
**Estado:** 📋 Pendiente
**Prioridad:** Alta
**Estimación:** 1.5 horas
**Asignado a:** Claude Code

---

## Descripción

Migrar el módulo core `time_tracker.py` desde `_work/from-simapp/tracking/` al directorio `tracking/` del proyecto, incluyendo los modelos de datos (Task, Phase, Pause) y la clase principal TimeTracker.

Esta migración es el corazón del sistema de tracking y debe realizarse con cuidado para asegurar que:
1. El código se copie sin modificaciones (ya es 100% genérico)
2. Las importaciones funcionen correctamente
3. El sistema de persistencia JSON funcione en la nueva ubicación
4. Se cree documentación básica del módulo

---

## Criterios de Aceptación

- [ ] Directorio `tracking/` creado en la raíz del proyecto
- [ ] Archivo `tracking/time_tracker.py` migrado (521 líneas)
- [ ] Archivo `tracking/__init__.py` migrado y actualizado
- [ ] Imports funcionando correctamente:
  - [ ] `from tracking import TimeTracker, Task, Phase, Pause`
  - [ ] Sin errores de importación
- [ ] Sistema de persistencia funcional:
  - [ ] Directorio `.claude/tracking/` se crea automáticamente
  - [ ] Archivos JSON se guardan correctamente
  - [ ] Formato JSON validado
- [ ] README.md básico creado en `tracking/`
- [ ] Tests manuales de funcionalidad básica ejecutados

---

## Dependencias

**Depende de:**
- ✅ TICKET-038: Análisis completado

**Bloquea a:**
- TICKET-040: Crear skills de comandos de tracking
- TICKET-041: Crear skills de reporting
- TICKET-042: Integración con implement-us

---

## Estructura a Crear

```
tracking/
├── __init__.py              # Exports del módulo
├── time_tracker.py          # Core del sistema (migrado)
│   ├── Task                 # Dataclass - tarea individual
│   ├── Phase                # Dataclass - fase del skill
│   ├── Pause                # Dataclass - pausa manual
│   └── TimeTracker          # Gestor central de tracking
└── README.md                # Documentación del módulo

.claude/
└── tracking/                # Directorio de datos (creado automáticamente)
    └── (archivos *.json en runtime)
```

---

## Migración de Archivos

### 1. time_tracker.py

**Origen:** `_work/from-simapp/tracking/time_tracker.py`
**Destino:** `tracking/time_tracker.py`
**Acción:** Copia directa sin modificaciones

**Contenido:**
- Dataclasses: `Task`, `Phase`, `Pause`
- Clase: `TimeTracker`
- Imports: `dataclasses`, `datetime`, `pathlib`, `typing`, `json`

**Verificación post-migración:**
- [ ] Sintaxis correcta (sin errores de Python)
- [ ] Imports estándar funcionan
- [ ] No hay referencias a paths absolutos
- [ ] storage_path usa `.claude/tracking/` (ya configurado en original)

### 2. __init__.py

**Origen:** `_work/from-simapp/tracking/__init__.py`
**Destino:** `tracking/__init__.py`
**Acción:** Copiar y verificar exports

**Contenido esperado:**
```python
"""
Sistema de Tracking de Tiempo para Claude Dev Kit.

Este módulo proporciona tracking automático de tiempo durante la implementación
de Historias de Usuario con el skill /implement-us.
"""

from .time_tracker import TimeTracker, Task, Phase, Pause

__all__ = [
    "TimeTracker",
    "Task",
    "Phase",
    "Pause"
]

__version__ = "1.0.0"
```

---

## README.md del Módulo

Crear `tracking/README.md` con:

### Contenido Requerido

```markdown
# Sistema de Tracking de Tiempo

Módulo core del sistema de tracking automático para el skill `/implement-us`.

## Componentes

### Modelos de Datos

#### Task
Representa una tarea individual dentro de una fase.

**Campos:**
- `task_id` (str): Identificador único
- `task_name` (str): Nombre descriptivo
- `task_type` (str): Tipo (modelo, vista, controlador, test)
- `estimated_minutes` (float): Estimación del plan
- `started_at` (datetime): Timestamp de inicio
- `completed_at` (datetime): Timestamp de fin
- `elapsed_seconds` (int): Duración real
- `file_created` (str): Path del archivo creado
- `status` (str): Estado (pending, in_progress, completed)

**Propiedades calculadas:**
- `actual_minutes`: Duración en minutos
- `variance_minutes`: Diferencia entre real y estimado
- `variance_percent`: Varianza porcentual

#### Phase
Representa una fase del skill implement-us (0-9).

**Campos:**
- `phase_number` (int): Número de fase (0-9)
- `phase_name` (str): Nombre descriptivo
- `started_at` (datetime): Timestamp de inicio
- `completed_at` (datetime): Timestamp de fin
- `elapsed_seconds` (int): Duración total
- `status` (str): Estado (pending, in_progress, completed)
- `tasks` (List[Task]): Tareas de esta fase
- `auto_approved` (bool): Si se completó automáticamente
- `user_approval_time_seconds` (int): Tiempo esperando aprobación

#### Pause
Representa una pausa manual del tracking.

**Campos:**
- `pause_id` (str): Identificador único
- `started_at` (datetime): Timestamp de inicio de pausa
- `resumed_at` (datetime): Timestamp de reanudación
- `duration_seconds` (int): Duración de la pausa
- `reason` (str): Motivo de la pausa

**Propiedades calculadas:**
- `duration_minutes`: Duración en minutos
- `is_active`: True si la pausa está activa

### TimeTracker

Gestor central de tracking de tiempo.

**Uso básico:**

```python
from tracking import TimeTracker

# Inicializar tracker
tracker = TimeTracker(
    us_id="US-001",
    us_title="Implementar panel display",
    us_points=3,
    producto="mi_producto"
)

# Iniciar tracking
tracker.start_tracking()

# Iniciar una fase
tracker.start_phase(0, "Validación de Contexto")

# Trabajar...

# Finalizar fase
tracker.end_phase(0)

# Finalizar tracking
tracker.end_tracking()
```

**Métodos principales:**

- `start_tracking()`: Inicia el tracking
- `end_tracking()`: Finaliza el tracking
- `start_phase(number, name)`: Inicia una fase
- `end_phase(number)`: Finaliza una fase
- `start_task(id, name, type, estimated)`: Inicia una tarea
- `end_task(id, file_created)`: Finaliza una tarea
- `pause(reason)`: Pausa el tracking
- `resume()`: Reanuda el tracking
- `get_status()`: Obtiene estado actual

## Persistencia

Los datos se guardan automáticamente en `.claude/tracking/{us_id}-tracking.json` en formato JSON.

**Ejemplo de archivo:**

```json
{
  "metadata": {
    "us_id": "US-001",
    "us_title": "Implementar panel display",
    "us_points": 3,
    "producto": "mi_producto"
  },
  "timeline": {
    "started_at": "2026-02-15T10:00:00Z",
    "completed_at": "2026-02-15T14:00:00Z",
    "total_elapsed_seconds": 14400,
    "effective_seconds": 13500,
    "paused_seconds": 900
  },
  "phases": [...],
  "pauses": [...],
  "summary": {
    "total_tasks": 15,
    "completed_tasks": 15,
    "estimated_total_minutes": 120,
    "actual_total_minutes": 135,
    "variance_minutes": 15,
    "variance_percent": 12.5
  }
}
```

## Skills de Tracking

Los siguientes skills interactúan con este módulo:

- `/track-pause [razón]`: Pausar tracking
- `/track-resume`: Reanudar tracking
- `/track-status`: Ver estado actual
- `/track-report [us_id]`: Generar reporte
- `/track-history [--last N]`: Ver historial

Ver documentación de cada skill para detalles de uso.

## Integración con /implement-us

El skill `/implement-us` usa este módulo automáticamente para trackear tiempo en cada fase de implementación.

No requiere intervención manual del usuario (excepto pausas).
```

---

## Checklist de Implementación

- [ ] Crear directorio `tracking/`
- [ ] Copiar `time_tracker.py` desde `_work/from-simapp/tracking/`
- [ ] Copiar `__init__.py` y actualizar si es necesario
- [ ] Verificar imports (ejecutar `python -c "from tracking import TimeTracker"`)
- [ ] Crear README.md con documentación completa
- [ ] Ejecutar tests manuales de funcionalidad

---

## Tests Manuales

Crear script de prueba `tests/manual/test_time_tracker_basic.py`:

```python
"""Test manual del TimeTracker básico."""
from tracking import TimeTracker, Task, Phase, Pause
from datetime import datetime, timezone
import json
from pathlib import Path

def test_basic_flow():
    """Test del flujo básico de tracking."""

    # 1. Crear tracker
    tracker = TimeTracker(
        us_id="US-TEST-001",
        us_title="Test del sistema de tracking",
        us_points=1,
        producto="test_producto"
    )

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

    print("\n🎉 Todos los tests pasaron exitosamente")

if __name__ == "__main__":
    test_basic_flow()
```

**Ejecutar:**
```bash
python tests/manual/test_time_tracker_basic.py
```

**Resultado esperado:**
```
✅ Tracking iniciado
✅ Fase 0 iniciada
✅ Fase 0 finalizada
✅ Tracking finalizado
✅ Archivo JSON creado: .claude/tracking/US-TEST-001-tracking.json
✅ JSON válido
✅ Limpieza completada

🎉 Todos los tests pasaron exitosamente
```

---

## Comandos

```bash
# Crear directorio
mkdir -p tracking

# Copiar archivos
cp _work/from-simapp/tracking/time_tracker.py tracking/
cp _work/from-simapp/tracking/__init__.py tracking/

# Verificar sintaxis Python
python -m py_compile tracking/time_tracker.py
python -m py_compile tracking/__init__.py

# Verificar imports
python -c "from tracking import TimeTracker, Task, Phase, Pause; print('✅ Imports OK')"

# Ejecutar test manual (después de crearlo)
python tests/manual/test_time_tracker_basic.py
```

---

## Resultado

⬜ **PENDIENTE**

_A completar al finalizar el ticket._

**Archivos creados:**
- tracking/time_tracker.py
- tracking/__init__.py
- tracking/README.md
- tests/manual/test_time_tracker_basic.py (opcional)

**Commits esperados:**
1. `feat(tracking): migrar módulo core time_tracker.py (TICKET-039)`
2. `docs(tracking): agregar README.md del módulo (TICKET-039)`
