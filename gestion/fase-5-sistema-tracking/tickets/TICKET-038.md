# TICKET-038: Análisis del Sistema de Tracking y Planificación de Migración

**Fase:** 5 - Sistema de Tracking
**Sprint:** 2
**Estado:** 📋 Pendiente
**Prioridad:** Alta
**Estimación:** 1 hora
**Asignado a:** Claude Code

---

## Descripción

Analizar en profundidad el sistema de tracking existente en `_work/from-simapp/tracking/`, comprender su arquitectura, identificar dependencias, y crear un plan detallado de migración al directorio `tracking/` del proyecto.

Este análisis es crítico para asegurar que:
1. No se pierda funcionalidad en la migración
2. El código sea 100% genérico (sin referencias específicas)
3. La integración con `/implement-us` sea clara y bien definida
4. Los skills de tracking sigan las convenciones establecidas

---

## Criterios de Aceptación

- [ ] Lectura completa de los 3 archivos del sistema:
  - [ ] `time_tracker.py` (521 líneas)
  - [ ] `commands.py` (431 líneas)
  - [ ] `__init__.py` (39 líneas)
- [ ] Análisis de dataclasses: `Task`, `Phase`, `Pause`
- [ ] Análisis de clase `TimeTracker`:
  - [ ] Métodos de tracking (start/end phase/task/tracking)
  - [ ] Métodos de pausas (pause/resume)
  - [ ] Método de persistencia (_save, _to_dict)
  - [ ] Método de status (get_status)
- [ ] Identificación de referencias específicas (si existen)
- [ ] Verificación de genericidad del código (100%)
- [ ] Mapeo de comandos CLI a skills de Claude Code
- [ ] Plan detallado de migración documentado
- [ ] Definición de estructura de skills de tracking

---

## Dependencias

**Depende de:**
- ✅ Fase 4: Generalización de Templates (completada)
- ✅ Branch feature/tracking-system creado

**Bloquea a:**
- TICKET-039: Migrar módulo core
- TICKET-040: Crear skills de comandos de tracking
- TICKET-041: Crear skills de reporting
- TICKET-042: Integración con implement-us

---

## Análisis Requerido

### 1. Análisis de Arquitectura

**Dataclasses (Modelos de Datos):**
- [ ] `Task`: Analizar campos, propiedades calculadas, validaciones
- [ ] `Phase`: Analizar relación con Task, campos de aprobación
- [ ] `Pause`: Analizar estados activo/inactivo, tracking de razón

**Clase TimeTracker:**
- [ ] Constructor: Parámetros requeridos, inicialización
- [ ] Ciclo de vida: start_tracking → fases → end_tracking
- [ ] Gestión de estado: current_phase, current_task, current_pause
- [ ] Persistencia: Formato JSON, path de storage, auto-save

### 2. Análisis de Genericidad

Verificar que NO existan referencias a:
- [ ] PyQt/MVC/Factory/Coordinator
- [ ] Rutas hardcodeadas específicas de simapp
- [ ] Nombres de productos o proyectos específicos
- [ ] Tecnologías específicas (más allá de Python stdlib)

Confirmar que SÍ use:
- [ ] Nombres genéricos: us_id, phase_name, task_type
- [ ] Paths configurables: storage_path parametrizado
- [ ] Tipos de datos estándar: datetime, dataclasses

### 3. Análisis de Comandos → Skills

Mapeo de funciones CLI a skills de Claude Code:

| Comando CLI | Skill Equivalente | Función Actual | Adaptación Requerida |
|-------------|-------------------|----------------|----------------------|
| `track_pause(reason)` | `/track-pause [razón]` | `commands.py:track_pause()` | Convertir a skill.md con output markdown |
| `track_resume()` | `/track-resume` | `commands.py:track_resume()` | Convertir a skill.md |
| `track_status()` | `/track-status` | `commands.py:track_status()` | Formatear output como tabla markdown |
| `track_report(us_id)` | `/track-report [us_id]` | `commands.py:track_report()` | Generar reporte completo markdown |
| `track_history(last)` | `/track-history [--last N]` | `commands.py:track_history()` | Listar historial en tabla markdown |

### 4. Análisis de Integración con /implement-us

Puntos de integración requeridos:

**Inicio del skill:**
- [ ] Crear instancia de `TimeTracker(us_id, title, points, producto)`
- [ ] Llamar `start_tracking()`
- [ ] Guardar referencia global o en contexto del skill

**Cada fase (0-9):**
- [ ] Al inicio: `start_phase(phase_number, phase_name)`
- [ ] Durante: Opcional `start_task()` / `end_task()` para tareas individuales
- [ ] Al finalizar: `end_phase(phase_number)`

**Fin del skill (Fase 9):**
- [ ] Llamar `end_tracking()`
- [ ] Generar reporte final con métricas
- [ ] Guardar archivo JSON final

**Pausas manuales (en cualquier momento):**
- [ ] Usuario ejecuta `/track-pause "razón"`
- [ ] Skill llama `tracker.pause("razón")`
- [ ] Usuario ejecuta `/track-resume`
- [ ] Skill llama `tracker.resume()`

---

## Plan de Migración a Documentar

Crear documento de análisis con:

### Sección 1: Resumen de Archivos

Tabla con:
- Nombre del archivo
- Líneas de código
- Componentes principales
- Estado de genericidad (✅ genérico / ⚠️ requiere adaptación)
- Destino de migración

### Sección 2: Arquitectura de Datos

Diagrama o descripción de:
- Relación Task → Phase → TimeTracker
- Flujo de estados: pending → in_progress → completed
- Cálculos de varianza y métricas

### Sección 3: Mapa de Migración

```
_work/from-simapp/tracking/          →  Destino
├── time_tracker.py                  →  tracking/time_tracker.py (copia directa)
├── __init__.py                      →  tracking/__init__.py (copia directa)
└── commands.py                      →  .claude/skills/track-*/skill.md (5 skills)
```

### Sección 4: Skills a Crear

Para cada skill:
- Nombre del skill
- Input esperado
- Lógica (qué métodos del TimeTracker llama)
- Output esperado (formato markdown)
- Ejemplo de uso

### Sección 5: Puntos de Integración

Para `/implement-us`:
- Modificaciones requeridas en skill.md
- Modificaciones en cada archivo de phase (phases/phase-X.md)
- Gestión del contexto del tracker (variable global o parámetro)

---

## Checklist de Implementación

- [ ] Leer completamente time_tracker.py
- [ ] Leer completamente commands.py
- [ ] Leer completamente __init__.py
- [ ] Verificar genericidad del código (100%)
- [ ] Crear tabla de mapeo comandos → skills
- [ ] Documentar plan de migración en formato markdown
- [ ] Guardar análisis en `docs/analysis/TICKET-038-tracking-analysis.md`
- [ ] Actualizar session-current.md con hallazgos
- [ ] Crear commits de documentación

---

## Comandos

```bash
# Leer archivos del sistema de tracking
cat _work/from-simapp/tracking/time_tracker.py
cat _work/from-simapp/tracking/commands.py
cat _work/from-simapp/tracking/__init__.py

# Contar líneas de código
wc -l _work/from-simapp/tracking/*.py

# Verificar imports (detectar dependencias)
grep -n "^import\|^from" _work/from-simapp/tracking/*.py

# Buscar referencias específicas (debería retornar vacío)
grep -i "pyqt\|mvc\|factory\|coordinator\|simapp" _work/from-simapp/tracking/*.py
```

---

## Entregable

**Archivo de análisis:** `docs/analysis/TICKET-038-tracking-analysis.md`

**Contenido esperado:**
- Resumen ejecutivo
- Análisis de arquitectura
- Verificación de genericidad
- Mapa de migración
- Definición de skills
- Puntos de integración
- Estimación de esfuerzo por ticket restante
- Riesgos identificados

**Tamaño estimado:** ~800-1000 líneas de documentación

---

## Resultado

⬜ **PENDIENTE**

_A completar al finalizar el ticket._
