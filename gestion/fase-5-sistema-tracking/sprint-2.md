# Sprint 2 - Fase 5: Sistema de Tracking

**Fecha Inicio:** 2026-02-15
**Fecha Fin Estimada:** 2026-02-16
**Sprint:** 2 (Semana 2)
**Estado:** 📋 Planificado

---

## Objetivos de la Fase

Migrar y adaptar el sistema de tracking de tiempo desde `_work/from-simapp/tracking/` al directorio `tracking/` del proyecto, implementando los comandos `/track-*` como skills independientes y asegurando la integración con el skill `/implement-us`.

El sistema de tracking es **crítico** para el framework ya que permite medir con precisión el tiempo real de implementación de Historias de Usuario, identificar cuellos de botella, y mejorar estimaciones futuras.

---

## Tareas (Tickets)

### Pendientes 📋

- [ ] **TICKET-038**: Análisis del sistema de tracking y planificación de migración
- [ ] **TICKET-039**: Migrar módulo core time_tracker.py con modelos de datos
- [ ] **TICKET-040**: Crear skills de comandos de tracking (/track-pause, /track-resume, /track-status)
- [ ] **TICKET-041**: Crear skills de reporting (/track-report, /track-history)
- [ ] **TICKET-042**: Integración con implement-us y documentación

### Completados ✅

Ninguno aún.

### Desestimados ❌

Ninguno.

### En Progreso 🔄

Ninguno.

---

## Métricas

- **Total de Tickets:** 5
- **Completados:** 0 (0%)
- **Desestimados:** 0 (0%)
- **En Progreso:** 0 (0%)
- **Pendientes:** 5 (100%)
- **Bloqueados:** 0

**Estimación Total:** 6 horas
- Análisis y planificación: 1h
- Migración del core: 1.5h
- Skills de tracking: 1.5h
- Skills de reporting: 1h
- Integración y documentación: 1h

**Progreso:** ░░░░░░░░░░░░░░░░ 0% (0/5 tickets)

**Entregables Esperados:**
- Sistema de tracking funcional en `tracking/`
- 5 skills de tracking implementados
- Integración con skill /implement-us
- Documentación completa del sistema
- Ejemplos de uso y reportes

---

## Dependencias

**Depende de:**
- ✅ Fase 3: Generalización de Skills (completada)
  - Arquitectura modular de skills establecida
  - Sistema de variables funcional
- ✅ Fase 4: Generalización de Templates (completada)
  - Templates listos para usar en reportes

**Bloquea a:**
- Fase 6: Documentación (requiere sistema de tracking funcional)
- Fase 7: Ejemplos (requiere tracking para métricas reales)
- Sprint 3: No puede comenzar sin tracking operacional

---

## Criterios de Aceptación de la Fase

- [ ] Directorio `tracking/` creado con módulos funcionales
- [ ] Módulo `time_tracker.py` migrado y validado:
  - [ ] Clase `TimeTracker` funcional
  - [ ] Modelos de datos: `Task`, `Phase`, `Pause`
  - [ ] Persistencia en JSON funcional
- [ ] Skills de tracking implementados:
  - [ ] `/track-pause [razón]` - Pausar tracking con razón opcional
  - [ ] `/track-resume` - Reanudar tracking
  - [ ] `/track-status` - Ver estado actual del tracking
  - [ ] `/track-report [us_id]` - Generar reporte de una US
  - [ ] `/track-history [--last N]` - Ver historial de tracking
- [ ] Integración con `/implement-us`:
  - [ ] Auto-inicio de tracking al invocar skill
  - [ ] Auto-tracking de fases y tareas
  - [ ] Auto-finalización de tracking en Fase 9
- [ ] Documentación completa:
  - [ ] README.md en `tracking/`
  - [ ] Documentación de API del TimeTracker
  - [ ] Guías de uso de comandos
  - [ ] Ejemplos de reportes
- [ ] Tests unitarios del TimeTracker (opcional pero deseable)

---

## Análisis del Sistema de Tracking Existente

### Archivos a Migrar

#### 1. time_tracker.py (521 líneas)

**Contenido:**
- Dataclasses: `Task`, `Phase`, `Pause` (modelos de datos)
- Clase `TimeTracker` (gestor central)
- Métodos de tracking: `start_tracking()`, `end_tracking()`, `start_phase()`, `end_phase()`, `start_task()`, `end_task()`
- Métodos de pausas: `pause()`, `resume()`
- Métodos de reporting: `get_status()`, `_to_dict()`
- Persistencia: `_save()` (JSON automático)

**Estado:** ✅ 100% genérico, listo para migrar sin modificaciones

**Variables parametrizables:**
- `storage_path`: Actualmente `.claude/tracking/{us_id}-tracking.json` (OK, genérico)
- Todos los campos usan nombres genéricos (us_id, phase, task, etc.)

**Funcionalidades:**
- Tracking automático de tiempo por fase (10 fases del skill)
- Tracking de tareas individuales dentro de cada fase
- Pausas manuales con tracking de razón y duración
- Cálculo de varianza (estimado vs. real)
- Reportes de estado en tiempo real
- Serialización completa a JSON

#### 2. commands.py (431 líneas)

**Contenido:**
- Comandos CLI para interactuar con el tracker
- Funciones: `track_pause()`, `track_resume()`, `track_status()`, `track_report()`, `track_history()`
- Formateo de output para consola
- Lectura de archivos de tracking existentes

**Estado:** ⚠️ Requiere adaptación a formato de skills

**Trabajo requerido:**
- Convertir funciones a skills individuales
- Adaptar output para formato markdown (en lugar de CLI plano)
- Mantener lógica de negocio intacta

#### 3. __init__.py (39 líneas)

**Contenido:**
- Exports del módulo
- Inicialización básica

**Estado:** ✅ Listo para migrar

---

## Arquitectura del Sistema de Tracking

### Componentes

```
tracking/
├── __init__.py              # Exports del módulo
├── time_tracker.py          # Core del sistema
│   ├── Task                 # Dataclass - tarea individual
│   ├── Phase                # Dataclass - fase del skill
│   ├── Pause                # Dataclass - pausa manual
│   └── TimeTracker          # Gestor central de tracking
├── reports.py               # (nuevo) Generación de reportes
└── README.md                # Documentación del módulo

.claude/
├── skills/
│   ├── track-pause/         # Skill /track-pause
│   │   └── skill.md
│   ├── track-resume/        # Skill /track-resume
│   │   └── skill.md
│   ├── track-status/        # Skill /track-status
│   │   └── skill.md
│   ├── track-report/        # Skill /track-report
│   │   └── skill.md
│   └── track-history/       # Skill /track-history
│       └── skill.md
└── tracking/                # Datos de tracking (runtime)
    ├── US-001-tracking.json
    ├── US-002-tracking.json
    └── ...
```

### Flujo de Tracking en /implement-us

```
Usuario ejecuta: /implement-us US-001

1. Fase 0: Validación de Contexto
   → TimeTracker.start_tracking()
   → TimeTracker.start_phase(0, "Validación de Contexto")
   → ... trabajo ...
   → TimeTracker.end_phase(0)

2. Fase 1: Generación de Escenarios BDD
   → TimeTracker.start_phase(1, "Generación de Escenarios BDD")
   → ... trabajo ...
   → TimeTracker.end_phase(1)

3-8. Fases 2-8: Similar
   → start_phase() → trabajo → end_phase()

9. Fase 9: Reporte Final
   → TimeTracker.start_phase(9, "Reporte Final")
   → TimeTracker.end_tracking()
   → Generar reporte completo con métricas
```

### Pausas Manuales

```
Durante cualquier fase:

Usuario: /track-pause "Reunión del equipo"
→ TimeTracker.pause("Reunión del equipo")
→ Timestamp de inicio de pausa guardado
→ Tracking actual PAUSADO

... tiempo pasa (reunión) ...

Usuario: /track-resume
→ TimeTracker.resume()
→ Timestamp de fin de pausa guardado
→ Duración calculada y guardada
→ Tracking reanudado
```

---

## Estrategia de Migración

### Enfoque por Fases

**Fase 1: Migración del Core (TICKET-038, TICKET-039)**
1. Crear directorio `tracking/`
2. Copiar `time_tracker.py` (sin modificaciones)
3. Copiar `__init__.py`
4. Validar importaciones
5. Crear tests básicos (opcional)

**Fase 2: Skills de Tracking Básico (TICKET-040)**
1. Crear skill `/track-pause`
   - Input: razón (opcional)
   - Lógica: `TimeTracker.pause(razón)`
   - Output: Confirmación con timestamp
2. Crear skill `/track-resume`
   - Input: ninguno
   - Lógica: `TimeTracker.resume()`
   - Output: Duración de la pausa, trabajo reanudado
3. Crear skill `/track-status`
   - Input: ninguno (usa tracking actual)
   - Lógica: `TimeTracker.get_status()`
   - Output: Estado actual formateado (fase, tarea, tiempo, progreso)

**Fase 3: Skills de Reporting (TICKET-041)**
1. Crear módulo `reports.py`
   - Funciones de formateo de reportes
   - Lectura de archivos de tracking
   - Generación de tablas markdown
2. Crear skill `/track-report`
   - Input: us_id (opcional, usa actual si no se provee)
   - Lógica: Leer tracking JSON, formatear reporte
   - Output: Reporte completo con métricas
3. Crear skill `/track-history`
   - Input: --last N (opcional, muestra últimos N)
   - Lógica: Listar archivos de tracking, mostrar resumen
   - Output: Tabla con historial de USs

**Fase 4: Integración con implement-us (TICKET-042)**
1. Modificar `skills/implement-us/skill.md`
   - Agregar `TimeTracker.start_tracking()` en inicio
   - Agregar `start_phase()` / `end_phase()` en cada fase
   - Agregar `end_tracking()` en Fase 9
2. Documentar integración
3. Crear ejemplos de uso
4. Validar flujo completo end-to-end

---

## Modelo de Datos

### Task (Tarea Individual)

```python
@dataclass
class Task:
    task_id: str                    # Identificador único: "task_001"
    task_name: str                  # Nombre descriptivo
    task_type: str                  # Tipo: modelo, vista, controlador, test
    estimated_minutes: float        # Estimación del plan
    started_at: Optional[datetime]  # Timestamp de inicio
    completed_at: Optional[datetime] # Timestamp de fin
    elapsed_seconds: int            # Duración real
    file_created: Optional[str]     # Path del archivo creado
    status: str                     # pending, in_progress, completed

    # Propiedades calculadas
    actual_minutes: float           # elapsed_seconds / 60
    variance_minutes: float         # actual - estimated
    variance_percent: float         # (variance / estimated) * 100
```

### Phase (Fase del Skill)

```python
@dataclass
class Phase:
    phase_number: int               # 0-9
    phase_name: str                 # "Validación de Contexto", etc.
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    elapsed_seconds: int
    status: str                     # pending, in_progress, completed
    tasks: List[Task]               # Tareas de esta fase
    auto_approved: bool             # Si se completó automáticamente
    user_approval_time_seconds: int # Tiempo esperando aprobación

    # Propiedades calculadas
    elapsed_minutes: float          # elapsed_seconds / 60
```

### Pause (Pausa Manual)

```python
@dataclass
class Pause:
    pause_id: str                   # "pause_001"
    started_at: datetime
    resumed_at: Optional[datetime]
    duration_seconds: int
    reason: str                     # Motivo de la pausa

    # Propiedades calculadas
    duration_minutes: float         # duration_seconds / 60
    is_active: bool                 # resumed_at is None
```

### TimeTracker (Gestor Central)

```python
class TimeTracker:
    # Metadata de la US
    us_id: str
    us_title: str
    us_points: int
    producto: str

    # Timeline
    started_at: Optional[datetime]
    completed_at: Optional[datetime]

    # Tracking
    phases: List[Phase]
    pauses: List[Pause]
    current_phase: Optional[Phase]
    current_task: Optional[Task]
    current_pause: Optional[Pause]

    # Storage
    storage_path: Path              # .claude/tracking/{us_id}-tracking.json
```

---

## Formato de Persistencia (JSON)

```json
{
  "metadata": {
    "us_id": "US-001",
    "us_title": "Implementar panel display",
    "us_points": 3,
    "producto": "ux_termostato",
    "tracking_version": "1.0"
  },
  "timeline": {
    "started_at": "2026-02-15T10:30:00Z",
    "completed_at": "2026-02-15T14:45:00Z",
    "total_elapsed_seconds": 15300,
    "effective_seconds": 13500,
    "paused_seconds": 1800
  },
  "phases": [
    {
      "phase_number": 0,
      "phase_name": "Validación de Contexto",
      "started_at": "2026-02-15T10:30:00Z",
      "completed_at": "2026-02-15T10:45:00Z",
      "elapsed_seconds": 900,
      "status": "completed",
      "tasks": [],
      "auto_approved": true,
      "user_approval_time_seconds": 0
    },
    {
      "phase_number": 3,
      "phase_name": "Implementación",
      "started_at": "2026-02-15T11:00:00Z",
      "completed_at": "2026-02-15T13:30:00Z",
      "elapsed_seconds": 9000,
      "status": "completed",
      "tasks": [
        {
          "task_id": "task_001",
          "task_name": "Implementar DisplayModelo",
          "task_type": "modelo",
          "estimated_minutes": 10.0,
          "started_at": "2026-02-15T11:00:00Z",
          "completed_at": "2026-02-15T11:15:00Z",
          "elapsed_seconds": 900,
          "actual_minutes": 15.0,
          "variance_minutes": 5.0,
          "file_created": "app/presentacion/paneles/display/modelo.py",
          "status": "completed"
        }
      ]
    }
  ],
  "pauses": [
    {
      "pause_id": "pause_001",
      "started_at": "2026-02-15T12:00:00Z",
      "resumed_at": "2026-02-15T12:30:00Z",
      "duration_seconds": 1800,
      "reason": "Reunión del equipo"
    }
  ],
  "summary": {
    "total_tasks": 15,
    "completed_tasks": 15,
    "total_phases": 10,
    "estimated_total_minutes": 120.0,
    "actual_total_minutes": 135.5,
    "variance_minutes": 15.5,
    "variance_percent": 12.92
  }
}
```

---

## Formato de Output de Skills

### /track-status

```markdown
# 📊 Estado del Tracking - US-001

**Historia de Usuario:** US-001 - Implementar panel display
**Producto:** ux_termostato
**Estado:** ▶️ En progreso (pausado)

## ⏱️ Tiempo

- **Inicio:** 2026-02-15 10:30:00 UTC
- **Tiempo transcurrido:** 2h 15m 30s
- **Tiempo efectivo:** 1h 45m 30s
- **Tiempo pausado:** 30m 0s (Reunión del equipo)

## 📍 Progreso

- **Fase actual:** Fase 3 - Implementación
- **Tarea actual:** Implementar DisplayModelo
- **Tareas completadas:** 8/15 (53%)

## ⏸️ Pausa Activa

- **Razón:** Reunión del equipo
- **Desde:** 2026-02-15 12:00:00 UTC (30 minutos)
- **Usar `/track-resume` para reanudar el trabajo**
```

### /track-report US-001

```markdown
# 📈 Reporte de Tracking - US-001

**Historia de Usuario:** US-001 - Implementar panel display
**Producto:** ux_termostato
**Puntos:** 3 puntos
**Estado:** ✅ Completado

---

## ⏱️ Resumen de Tiempo

| Métrica | Valor |
|---------|-------|
| **Inicio** | 2026-02-15 10:30:00 UTC |
| **Fin** | 2026-02-15 14:45:00 UTC |
| **Tiempo total** | 4h 15m 0s |
| **Tiempo efectivo** | 3h 45m 0s |
| **Tiempo pausado** | 30m 0s |

---

## 📊 Fases Ejecutadas

| Fase | Nombre | Duración | Tareas | Estado |
|------|--------|----------|--------|--------|
| 0 | Validación de Contexto | 15m | 0 | ✅ Completado |
| 1 | Generación de Escenarios BDD | 20m | 0 | ✅ Completado |
| 2 | Plan de Implementación | 25m | 0 | ✅ Completado |
| 3 | Implementación | 2h 30m | 10 | ✅ Completado |
| 4 | Tests Unitarios | 30m | 3 | ✅ Completado |
| 5 | Tests de Integración | 20m | 1 | ✅ Completado |
| 6 | Validación BDD | 15m | 1 | ✅ Completado |
| 7 | Quality Gates | 10m | 0 | ✅ Completado |
| 8 | Documentación | 10m | 0 | ✅ Completado |
| 9 | Reporte Final | 5m | 0 | ✅ Completado |

**Total:** 10 fases | 3h 45m | 15 tareas

---

## 📝 Detalle de Tareas (Fase 3: Implementación)

| ID | Nombre | Tipo | Estimado | Real | Varianza | Archivo |
|----|--------|------|----------|------|----------|---------|
| task_001 | DisplayModelo | modelo | 10m | 15m | +5m (+50%) | modelo.py |
| task_002 | DisplayVista | vista | 15m | 12m | -3m (-20%) | vista.py |
| ... | ... | ... | ... | ... | ... | ... |

**Total Fase 3:** 120m estimado | 135m real | +15m varianza (+12.5%)

---

## ⏸️ Pausas Registradas

| ID | Inicio | Fin | Duración | Razón |
|----|--------|-----|----------|-------|
| pause_001 | 12:00 | 12:30 | 30m | Reunión del equipo |

**Total pausado:** 30m

---

## 📊 Métricas Finales

| Métrica | Estimado | Real | Varianza |
|---------|----------|------|----------|
| **Tiempo total** | 180m (3h) | 225m (3h 45m) | +45m (+25%) |
| **Por punto** | 60m/punto | 75m/punto | +15m/punto |
| **Tareas totales** | 15 | 15 | - |
| **Archivos creados** | 10 | 10 | - |

---

## 💡 Insights

- ✅ Implementación completada exitosamente
- ⚠️ Varianza de +25% sobre estimado (considerar para futuras USs de 3 puntos)
- ⚠️ Fase 3 (Implementación) tuvo mayor varianza (+12.5%)
- ✅ Quality gates pasados sin problemas
```

### /track-history

```markdown
# 📚 Historial de Tracking

**Producto:** ux_termostato

---

## Últimas 5 Historias de Usuario

| US ID | Título | Puntos | Fecha | Duración | Estado |
|-------|--------|--------|-------|----------|--------|
| US-001 | Implementar panel display | 3 | 2026-02-15 | 3h 45m | ✅ Completado |
| US-002 | Agregar sensor temperatura | 2 | 2026-02-14 | 2h 30m | ✅ Completado |
| US-003 | Sistema de alertas | 5 | 2026-02-13 | 5h 15m | ✅ Completado |
| US-004 | Configuración avanzada | 3 | 2026-02-12 | 3h 00m | ✅ Completado |
| US-005 | Dashboard principal | 8 | 2026-02-11 | 8h 30m | ✅ Completado |

---

## 📊 Estadísticas Generales

| Métrica | Valor |
|---------|-------|
| **Total USs completadas** | 5 |
| **Puntos totales** | 21 puntos |
| **Tiempo total** | 23h 0m |
| **Promedio por punto** | 65.7m/punto |
| **Varianza promedio** | +18.5% |

---

## 🏆 Top 3 Fases más Costosas

1. **Fase 3 - Implementación**: 12h 30m (54% del tiempo)
2. **Fase 4 - Tests Unitarios**: 4h 15m (18% del tiempo)
3. **Fase 2 - Plan de Implementación**: 2h 30m (11% del tiempo)
```

---

## Riesgos Identificados

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| TimeTracker requiere modificaciones inesperadas | Baja | Medio | Código ya validado en simapp, es 100% genérico |
| Skills de tracking no integran bien con Claude Code | Media | Alto | Seguir estructura de skills existentes (resume, keybindings-help) |
| Formato de output no es óptimo para markdown | Media | Bajo | Iterar con ejemplos reales hasta encontrar formato claro |
| Pérdida de datos si tracking.json se corrompe | Baja | Alto | Validar JSON después de cada save, agregar backup automático |

---

## Checklist Pre-Commit

Antes de hacer commit de esta fase:
- [ ] Módulo `tracking/` creado y funcional
- [ ] `time_tracker.py` migrado y validado (importaciones funcionan)
- [ ] 5 skills de tracking implementados y probados
- [ ] Integración con `/implement-us` funcional
- [ ] Documentación completa (`tracking/README.md`)
- [ ] Al menos 1 ejemplo end-to-end validado
- [ ] Tests unitarios del TimeTracker (opcional)
- [ ] Actualizar CHANGELOG.md
- [ ] Actualizar session-current.md

---

## Retrospectiva (Al finalizar)

### ¿Qué salió bien?

_A completar al finalizar la fase._

### ¿Qué se puede mejorar?

_A completar al finalizar la fase._

### Lecciones Aprendidas

_A completar al finalizar la fase._

---

## Siguiente Fase

**Fase 6: Documentación** - Ver `gestion/fase-6-documentacion/sprint-3.md`

---

**Última Actualización:** 2026-02-15 (Planificación inicial creada)
