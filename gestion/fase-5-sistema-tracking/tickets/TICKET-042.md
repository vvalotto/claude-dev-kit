# TICKET-042: Integración con implement-us y Documentación

**Fase:** 5 - Sistema de Tracking
**Sprint:** 2
**Estado:** 📋 Pendiente
**Prioridad:** Alta
**Estimación:** 1 hora
**Asignado a:** Claude Code

---

## Descripción

Integrar el sistema de tracking con el skill `/implement-us` para que el tracking sea completamente automático, y crear la documentación completa del sistema de tracking.

Esta integración es el paso final que hace que el sistema de tracking sea transparente para el usuario y completamente automático durante la implementación de Historias de Usuario.

---

## Criterios de Aceptación

- [ ] Skill `/implement-us` modificado para usar TimeTracker:
  - [ ] Inicializa tracker al inicio del skill
  - [ ] Inicia/finaliza fases automáticamente en cada phase
  - [ ] Finaliza tracking en Fase 9
  - [ ] Incluye métricas de tracking en reporte final
- [ ] Documentación completa creada:
  - [ ] Guía de uso de skills de tracking
  - [ ] Arquitectura del sistema documentada
  - [ ] Ejemplos end-to-end
  - [ ] FAQ de tracking
- [ ] README.md principal actualizado con sección de tracking
- [ ] CHANGELOG.md actualizado con Fase 5
- [ ] session-current.md actualizado

---

## Dependencias

**Depende de:**
- ✅ TICKET-038: Análisis completado
- ✅ TICKET-039: Módulo core migrado
- ✅ TICKET-040: Skills básicos creados
- ✅ TICKET-041: Skills de reporting creados

**Bloquea a:**
- Fase 6: Documentación
- Sprint 3: Inicio

---

## Integración con /implement-us

### Modificaciones Requeridas

#### 1. skill.md (Orquestador)

**Ubicación:** `skills/implement-us/skill.md`

**Modificaciones:**

##### Al inicio del skill (después de parsear argumentos):

```markdown
## 1. Inicializar Tracking

```python
from tracking import TimeTracker

# Crear tracker
tracker = TimeTracker(
    us_id=us_id,
    us_title=us_title,  # Del argumento o prompt
    us_points=us_points,  # Del argumento o prompt
    producto=producto  # Del argumento o prompt
)

# Iniciar tracking
tracker.start_tracking()

# Guardar referencia en contexto (variable global o similar)
_current_tracker = tracker
```

**Nota:** El tracker se guardará automáticamente en `.claude/tracking/{us_id}-tracking.json`
```

##### Al invocar cada fase:

```markdown
## 2. Ejecutar Fase {N}

```python
# Iniciar tracking de la fase
_current_tracker.start_phase({N}, "{PHASE_NAME}")
```

**Invocar agente de fase:** `phases/phase-{N}-{name}.md`

```python
# Finalizar tracking de la fase
_current_tracker.end_phase({N})
```
```

##### Al finalizar el skill (Fase 9):

```markdown
## 10. Finalizar Tracking y Generar Reporte

```python
# Finalizar tracking
_current_tracker.end_tracking()

# Generar reporte de tracking
from tracking.reports import generate_full_report

tracking_data = _current_tracker._to_dict()
tracking_report = generate_full_report(tracking_data)
```

### Incluir métricas de tracking en el reporte final de implementación

**Agregar sección al template `templates/reporting/implementation-report.md`:**

```markdown
## ⏱️ Métricas de Tiempo

{tracking_report}
```
```

#### 2. Phases (Opcional - Tracking de Tareas)

Para tracking más granular, las phases pueden trackear tareas individuales:

**Ejemplo en phase-3-implementation.md:**

```markdown
### Implementar Modelo

```python
# Iniciar tarea
_current_tracker.start_task(
    task_id="task_001",
    task_name="Implementar {COMPONENT_NAME}Modelo",
    task_type="modelo",
    estimated_minutes=10
)
```

**Instrucciones para Claude:**
- Implementar modelo...
- (trabajo de implementación)

```python
# Finalizar tarea
_current_tracker.end_task(
    task_id="task_001",
    file_created="{COMPONENT_PATH}/modelo.py"
)
```
```

**Nota:** El tracking de tareas es opcional. Para MVP, solo trackear fases es suficiente.

---

## Documentación

### 1. Guía de Usuario: docs/tracking/user-guide.md

**Contenido:**

```markdown
# Guía de Usuario - Sistema de Tracking

## Introducción

El sistema de tracking de tiempo registra automáticamente el tiempo invertido en implementar Historias de Usuario con el skill `/implement-us`.

## Tracking Automático

El tracking se inicia automáticamente al ejecutar:

```bash
/implement-us US-001
```

**No requiere acción manual del usuario.**

## Comandos de Control Manual

### Pausar Tracking

Cuando necesites interrumpir el trabajo:

```bash
/track-pause "Reunión del equipo"
```

**Casos de uso:**
- Reuniones
- Breaks
- Code reviews
- Atender otras prioridades

### Reanudar Tracking

Para continuar el trabajo:

```bash
/track-resume
```

### Ver Estado Actual

Para ver el progreso y tiempo transcurrido:

```bash
/track-status
```

**Muestra:**
- Fase y tarea actual
- Tiempo transcurrido y efectivo
- Progreso de tareas
- Pausa activa (si existe)

## Reportes

### Reporte de una US

Ver reporte detallado de implementación:

```bash
# Tracking actual
/track-report

# US específica
/track-report US-001
```

**Incluye:**
- Resumen de tiempo
- Fases ejecutadas
- Detalle de tareas
- Pausas registradas
- Métricas y varianza

### Historial de Tracking

Ver todas las USs trackeadas:

```bash
# Todo el historial
/track-history

# Últimas 10 USs
/track-history --last 10
```

## Persistencia

Los datos se guardan en:
```
.claude/tracking/{us_id}-tracking.json
```

**Formato:** JSON estructurado con toda la información del tracking.

## FAQ

### ¿El tracking funciona si cierro Claude Code?

Sí, los datos se guardan automáticamente. Al reabrir y continuar con `/implement-us`, el tracking se reanuda.

### ¿Puedo editar manualmente los archivos JSON?

Sí, pero no se recomienda. Los archivos siguen un esquema específico.

### ¿Qué pasa si olvido hacer /track-resume?

El tiempo pausado se contabiliza como "tiempo no efectivo" en las métricas. Puedes editar el JSON manualmente si fue un error.

### ¿Cómo se calcula la varianza?

```
Varianza = Tiempo Real - Tiempo Estimado
Varianza % = (Varianza / Tiempo Estimado) * 100
```

### ¿Puedo desactivar el tracking?

Actualmente no. El tracking es parte integral del skill `/implement-us`. Los datos son útiles para mejorar estimaciones futuras.
```

### 2. Arquitectura Técnica: docs/tracking/architecture.md

**Contenido:**

```markdown
# Arquitectura del Sistema de Tracking

## Visión General

Sistema de tracking automático de tiempo basado en dataclasses y persistencia JSON.

## Componentes

### Core (tracking/)

#### time_tracker.py
- **Task**: Dataclass para tareas individuales
- **Phase**: Dataclass para fases del skill
- **Pause**: Dataclass para pausas manuales
- **TimeTracker**: Gestor central

#### reports.py
- **format_duration()**: Formateo de duraciones
- **format_timestamp()**: Formateo de timestamps
- **generate_full_report()**: Reporte completo de una US
- **generate_history_table()**: Tabla de historial

#### __init__.py
- Exports del módulo

### Skills (.claude/skills/)

- **track-pause/**: Pausar tracking
- **track-resume/**: Reanudar tracking
- **track-status/**: Ver estado
- **track-report/**: Generar reporte
- **track-history/**: Ver historial

### Persistencia (.claude/tracking/)

Archivos JSON con formato:
```json
{
  "metadata": {...},
  "timeline": {...},
  "phases": [...],
  "pauses": [...],
  "summary": {...}
}
```

## Flujo de Datos

```
Usuario ejecuta /implement-us US-001
    ↓
TimeTracker.start_tracking()
    ↓
Para cada Fase (0-9):
    TimeTracker.start_phase(N, name)
    → Trabajo de implementación
    TimeTracker.end_phase(N)
    ↓
TimeTracker.end_tracking()
    ↓
Archivo JSON guardado en .claude/tracking/
    ↓
Accesible via /track-report, /track-history
```

## Modelo de Datos

Ver `tracking/README.md` para detalles completos de dataclasses.

## Integración con implement-us

El skill `/implement-us` crea una instancia de `TimeTracker` al inicio y la usa en cada fase.

**Variable global:** `_current_tracker`

**Lifecycle:**
1. start_tracking()
2. start_phase() × 10
3. end_phase() × 10
4. end_tracking()

## Extensibilidad

Para agregar nuevos comandos de tracking:
1. Crear skill en `.claude/skills/track-{nombre}/`
2. Usar funciones de `tracking.reports` para formateo
3. Leer archivos JSON de `.claude/tracking/`

Para modificar persistencia:
- Actualmente: JSON local
- Futuro: Base de datos SQLite, exportación a CSV, etc.
```

### 3. Ejemplos End-to-End: docs/tracking/examples.md

**Contenido:**

```markdown
# Ejemplos de Uso del Sistema de Tracking

## Ejemplo 1: Implementación Simple (Sin Pausas)

```bash
# Iniciar implementación
/implement-us US-001

# ... el skill ejecuta automáticamente ...
# Fase 0: Validación → tracking iniciado
# Fase 1-9: Implementación → cada fase trackeada
# Fase 9: Reporte final → tracking finalizado

# Ver reporte
/track-report US-001
```

**Resultado:** Reporte completo con tiempo por fase.

## Ejemplo 2: Implementación con Pausas

```bash
# Iniciar implementación
/implement-us US-002

# ... trabajando en Fase 3 ...

# Interrumpido por reunión
/track-pause "Daily standup"

# ... 15 minutos de reunión ...

# Continuar trabajo
/track-resume

# ... continuar con fases restantes ...

# Ver estado durante implementación
/track-status

# Al finalizar
/track-report US-002
```

**Resultado:** Reporte muestra pausa de 15m, tiempo efectivo correcto.

## Ejemplo 3: Análisis Retrospectivo

```bash
# Ver historial de última semana
/track-history --last 10

# Identificar US con mayor varianza
# Revisar reporte detallado
/track-report US-005

# Analizar qué fase tuvo mayor sobrecosto
# → Fase 3 (Implementación) +45m

# Conclusión: Mejorar estimaciones de implementación
```

## Ejemplo 4: Tracking Granular (Con Tareas)

Si las phases implementan tracking de tareas:

```bash
/implement-us US-003

# Durante Fase 3, el skill trackea:
# - task_001: Implementar Modelo (10m estimado → 12m real)
# - task_002: Implementar Vista (15m estimado → 18m real)
# - task_003: Implementar Controlador (12m estimado → 10m real)

# Reporte muestra varianza por tarea
/track-report US-003
```

**Resultado:** Análisis detallado de varianza por componente.
```

---

## Checklist de Implementación

### Integración con /implement-us
- [ ] Modificar `skills/implement-us/skill.md`
  - [ ] Agregar inicialización de tracker al inicio
  - [ ] Agregar start_phase/end_phase en cada fase
  - [ ] Agregar end_tracking en fase final
  - [ ] Agregar inclusión de reporte en output final
- [ ] Probar flujo completo end-to-end con US real
- [ ] Verificar que archivos JSON se crean correctamente
- [ ] Verificar que métricas son precisas

### Documentación
- [ ] Crear `docs/tracking/` directory
- [ ] Escribir `user-guide.md` (~500 líneas)
- [ ] Escribir `architecture.md` (~400 líneas)
- [ ] Escribir `examples.md` (~300 líneas)
- [ ] Actualizar README.md principal con sección de tracking
- [ ] Actualizar CHANGELOG.md con Fase 5 completada
- [ ] Actualizar session-current.md con progreso

### Validación Final
- [ ] Ejecutar `/implement-us` con tracking habilitado
- [ ] Pausar y reanudar durante implementación
- [ ] Ver estado con `/track-status`
- [ ] Generar reporte con `/track-report`
- [ ] Ver historial con `/track-history`
- [ ] Validar precisión de métricas
- [ ] Verificar formato de output

---

## Tests End-to-End

### Test Completo del Sistema

```bash
# 1. Iniciar implementación
/implement-us US-TEST-TRACKING

# 2. Durante Fase 3, pausar
/track-pause "Test de pausa"

# 3. Ver estado (debe mostrar pausa activa)
/track-status

# 4. Reanudar
/track-resume

# 5. Continuar hasta finalizar

# 6. Generar reporte
/track-report US-TEST-TRACKING

# 7. Verificar en reporte:
#    - 10 fases completadas
#    - 1 pausa registrada
#    - Métricas correctas
#    - Varianza calculada

# 8. Ver historial
/track-history

# 9. Verificar que US-TEST-TRACKING aparece en lista
```

**Criterio de éxito:** Todos los comandos funcionan, métricas son correctas, reportes son legibles.

---

## Actualización de Documentos

### README.md Principal

Agregar sección:

```markdown
## Sistema de Tracking

El framework incluye un sistema de tracking automático de tiempo.

**Características:**
- Tracking automático durante `/implement-us`
- Pausas manuales con razón
- Reportes detallados por US
- Historial completo de tracking
- Métricas de varianza (estimado vs. real)

**Comandos disponibles:**
- `/track-pause [razón]` - Pausar tracking
- `/track-resume` - Reanudar tracking
- `/track-status` - Ver estado actual
- `/track-report [us_id]` - Generar reporte
- `/track-history [--last N]` - Ver historial

**Documentación completa:** [docs/tracking/user-guide.md](docs/tracking/user-guide.md)
```

### CHANGELOG.md

Agregar entrada:

```markdown
## [Unreleased]

### Added - Fase 5: Sistema de Tracking

- Sistema de tracking automático de tiempo durante implementación de USs
- Módulo `tracking/` con TimeTracker, Task, Phase, Pause
- Skills de tracking:
  - `/track-pause` - Pausar tracking con razón
  - `/track-resume` - Reanudar tracking
  - `/track-status` - Ver estado actual
  - `/track-report` - Generar reporte detallado
  - `/track-history` - Ver historial de tracking
- Módulo `tracking/reports.py` con funciones de formateo
- Integración automática con skill `/implement-us`
- Documentación completa en `docs/tracking/`
- Persistencia en JSON en `.claude/tracking/`

**Métricas:**
- 5 tickets completados (TICKET-038 a TICKET-042)
- ~1,200 líneas de código (Python)
- ~1,200 líneas de documentación (Markdown)
- 5 skills de tracking
- 3 modelos de datos (Task, Phase, Pause)
```

---

## Comandos

```bash
# Crear directorio de documentación
mkdir -p docs/tracking

# Crear archivos de documentación
touch docs/tracking/user-guide.md
touch docs/tracking/architecture.md
touch docs/tracking/examples.md

# Validar estructura final
tree tracking/
tree .claude/skills/track-*
tree docs/tracking/
```

---

## Resultado

⬜ **PENDIENTE**

_A completar al finalizar el ticket._

**Archivos modificados:**
- skills/implement-us/skill.md (integración con tracking)

**Archivos creados:**
- docs/tracking/user-guide.md
- docs/tracking/architecture.md
- docs/tracking/examples.md

**Archivos actualizados:**
- README.md (sección de tracking)
- CHANGELOG.md (Fase 5)
- session-current.md (progreso actualizado)

**Commits esperados:**
1. `feat(implement-us): integrar sistema de tracking automático (TICKET-042)`
2. `docs(tracking): crear documentación completa del sistema (TICKET-042)`
3. `docs: actualizar README.md y CHANGELOG.md con Fase 5 (TICKET-042)`

O un commit consolidado:
- `feat(fase-5): completar integración y documentación del sistema de tracking (TICKET-042) ✅`
