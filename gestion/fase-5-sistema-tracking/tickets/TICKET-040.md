# TICKET-040: Crear Skills de Comandos de Tracking

**Fase:** 5 - Sistema de Tracking
**Sprint:** 2
**Estado:** 📋 Pendiente
**Prioridad:** Alta
**Estimación:** 1.5 horas
**Asignado a:** Claude Code

---

## Descripción

Crear los 3 skills básicos de tracking que permiten a los usuarios pausar, reanudar y ver el estado del tracking durante la implementación de una Historia de Usuario:

1. `/track-pause [razón]` - Pausar el tracking con razón opcional
2. `/track-resume` - Reanudar el tracking después de una pausa
3. `/track-status` - Ver el estado actual del tracking

Estos skills son fundamentales para el control manual del tracking y deben seguir las convenciones establecidas en el framework (similar a `/resume`, `/keybindings-help`).

---

## Criterios de Aceptación

- [ ] Skill `/track-pause` creado y funcional:
  - [ ] Acepta parámetro opcional `razón`
  - [ ] Valida que existe tracking activo
  - [ ] Llama `TimeTracker.pause(razón)`
  - [ ] Muestra confirmación con timestamp
- [ ] Skill `/track-resume` creado y funcional:
  - [ ] Valida que existe pausa activa
  - [ ] Llama `TimeTracker.resume()`
  - [ ] Muestra duración de la pausa
- [ ] Skill `/track-status` creado y funcional:
  - [ ] Lee estado actual del tracker
  - [ ] Formatea output en markdown legible
  - [ ] Muestra fase, tarea, tiempos, progreso
- [ ] Output de cada skill formateado en markdown
- [ ] Manejo de errores robusto (tracker no existe, pausa activa, etc.)
- [ ] Documentación inline en cada skill

---

## Dependencias

**Depende de:**
- ✅ TICKET-038: Análisis completado
- ✅ TICKET-039: Módulo core migrado

**Bloquea a:**
- TICKET-041: Skills de reporting
- TICKET-042: Integración con implement-us

---

## Estructura de Skills

```
.claude/
└── skills/
    ├── track-pause/
    │   └── skill.md
    ├── track-resume/
    │   └── skill.md
    └── track-status/
        └── skill.md
```

---

## Skill 1: /track-pause

### Archivo: .claude/skills/track-pause/skill.md

```markdown
# Pausar Tracking de Tiempo

Pausa temporalmente el tracking de tiempo de la Historia de Usuario actual.

Útil cuando necesitas interrumpir el trabajo por:
- Reuniones
- Revisiones de código
- Breaks
- Atender otras prioridades

## Uso

```bash
/track-pause [razón]
```

**Parámetros:**
- `razón` (opcional): Motivo de la pausa (ej: "Reunión del equipo", "Break")

## Ejemplos

```bash
# Pausar con razón
/track-pause "Reunión de planning"

# Pausar sin razón
/track-pause
```

## Instrucciones

Cuando este skill es invocado:

1. **Verificar tracking activo**
   - Buscar archivos de tracking en `.claude/tracking/`
   - Verificar que existe al menos un tracking con `started_at` pero sin `completed_at`
   - Si no hay tracking activo, mostrar error

2. **Verificar que no haya pausa activa**
   - Leer el archivo de tracking actual
   - Verificar que `current_pause` es None
   - Si ya hay pausa activa, mostrar error con razón de la pausa existente

3. **Ejecutar pausa**
   ```python
   from tracking import TimeTracker
   from pathlib import Path
   import json

   # Leer tracking actual (el más reciente sin completed_at)
   tracking_files = sorted(Path(".claude/tracking").glob("*.json"))
   # ... leer archivo, deserializar TimeTracker ...

   # Pausar
   tracker.pause(razón or "")
   ```

4. **Mostrar confirmación**
   ```markdown
   # ⏸️ Tracking Pausado

   **Historia de Usuario:** {us_id} - {us_title}
   **Razón:** {razón o "Sin razón especificada"}
   **Pausado en:** {timestamp}

   El tracking está pausado. El tiempo transcurrido durante la pausa NO se contabilizará.

   **Para reanudar el trabajo, ejecuta:** `/track-resume`
   ```

## Manejo de Errores

**Si no hay tracking activo:**
```markdown
# ❌ Error: No hay tracking activo

No se encontró ninguna Historia de Usuario en progreso.

**Para iniciar tracking, ejecuta:**
```bash
/implement-us US-XXX
```
```

**Si ya hay pausa activa:**
```markdown
# ⚠️ Error: Ya hay una pausa activa

**Pausa actual:**
- **Razón:** {razón de pausa actual}
- **Desde:** {timestamp de pausa}
- **Duración:** {duración hasta ahora}

**Para reanudar el trabajo, ejecuta:** `/track-resume`
```
```

---

## Skill 2: /track-resume

### Archivo: .claude/skills/track-resume/skill.md

```markdown
# Reanudar Tracking de Tiempo

Reanuda el tracking después de una pausa con `/track-pause`.

## Uso

```bash
/track-resume
```

## Instrucciones

Cuando este skill es invocado:

1. **Verificar tracking activo**
   - Buscar tracking actual (sin `completed_at`)
   - Si no hay tracking activo, mostrar error

2. **Verificar que haya pausa activa**
   - Verificar que `current_pause` existe y `resumed_at` es None
   - Si no hay pausa activa, mostrar error

3. **Reanudar tracking**
   ```python
   from tracking import TimeTracker

   # ... leer tracker ...

   # Reanudar
   tracker.resume()
   ```

4. **Mostrar confirmación**
   ```markdown
   # ▶️ Tracking Reanudado

   **Historia de Usuario:** {us_id} - {us_title}

   ## Pausa Finalizada

   - **Razón:** {razón}
   - **Inicio:** {started_at}
   - **Fin:** {resumed_at}
   - **Duración:** {duration_minutes} minutos

   El trabajo se ha reanudado. El tracking está activo nuevamente.

   **Para ver el estado actual, ejecuta:** `/track-status`
   ```

## Manejo de Errores

**Si no hay tracking activo:**
```markdown
# ❌ Error: No hay tracking activo

No se encontró ninguna Historia de Usuario en progreso.
```

**Si no hay pausa activa:**
```markdown
# ⚠️ Error: No hay pausa activa

El tracking está actualmente en ejecución, no pausado.

**Para pausar el tracking, ejecuta:** `/track-pause [razón]`
**Para ver el estado actual, ejecuta:** `/track-status`
```
```

---

## Skill 3: /track-status

### Archivo: .claude/skills/track-status/skill.md

```markdown
# Ver Estado del Tracking

Muestra el estado actual del tracking de tiempo para la Historia de Usuario en progreso.

Incluye:
- Información de la US
- Tiempos (total, efectivo, pausado)
- Progreso actual (fase, tarea)
- Tareas completadas

## Uso

```bash
/track-status
```

## Instrucciones

Cuando este skill es invocado:

1. **Verificar tracking activo**
   - Buscar tracking actual (sin `completed_at`)
   - Si no hay tracking activo, mostrar mensaje informativo

2. **Obtener estado**
   ```python
   from tracking import TimeTracker

   # ... leer tracker ...

   # Obtener status
   status = tracker.get_status()
   ```

3. **Formatear output**
   ```markdown
   # 📊 Estado del Tracking - {us_id}

   **Historia de Usuario:** {us_id} - {us_title}
   **Producto:** {producto}
   **Puntos:** {us_points}
   **Estado:** {emoji} {status_text}

   ## ⏱️ Tiempo

   | Métrica | Valor |
   |---------|-------|
   | **Inicio** | {started_at} |
   | **Tiempo transcurrido** | {elapsed_time} |
   | **Tiempo efectivo** | {effective_time} |
   | **Tiempo pausado** | {paused_time} |

   ## 📍 Progreso Actual

   {if current_phase}
   - **Fase actual:** Fase {phase_number} - {phase_name}
   - **Tarea actual:** {task_name or "Sin tarea activa"}
   - **Tareas completadas:** {completed_tasks}/{total_tasks} ({percentage}%)
   {else}
   - **Estado:** Entre fases
   {endif}

   {if current_pause}
   ## ⏸️ Pausa Activa

   - **Razón:** {pause_reason}
   - **Desde:** {pause_started_at}
   - **Duración:** {pause_duration}

   **Para reanudar:** `/track-resume`
   {endif}

   ---

   **Ver reporte completo:** `/track-report {us_id}`
   ```

## Cálculo de Emojis y Estados

```python
if current_pause:
    emoji = "⏸️"
    status_text = "Pausado"
elif current_phase:
    emoji = "▶️"
    status_text = "En progreso"
else:
    emoji = "⏹️"
    status_text = "Detenido"
```

## Manejo de Caso Sin Tracking

```markdown
# ℹ️ No hay tracking activo

No se encontró ninguna Historia de Usuario en progreso.

**Para iniciar tracking:**
```bash
/implement-us US-XXX
```

**Para ver historial de tracking:**
```bash
/track-history
```
```
```

---

## Checklist de Implementación

### Skill /track-pause
- [ ] Crear directorio `.claude/skills/track-pause/`
- [ ] Crear `skill.md` con contenido completo
- [ ] Implementar lógica de validación de tracking activo
- [ ] Implementar lógica de validación de pausa existente
- [ ] Implementar llamada a `tracker.pause(razón)`
- [ ] Formatear output de confirmación
- [ ] Implementar manejo de errores
- [ ] Probar manualmente con tracking activo
- [ ] Probar error: sin tracking
- [ ] Probar error: pausa ya activa

### Skill /track-resume
- [ ] Crear directorio `.claude/skills/track-resume/`
- [ ] Crear `skill.md` con contenido completo
- [ ] Implementar lógica de validación de pausa activa
- [ ] Implementar llamada a `tracker.resume()`
- [ ] Formatear output con duración de pausa
- [ ] Implementar manejo de errores
- [ ] Probar manualmente después de /track-pause
- [ ] Probar error: sin pausa activa

### Skill /track-status
- [ ] Crear directorio `.claude/skills/track-status/`
- [ ] Crear `skill.md` con contenido completo
- [ ] Implementar lectura de estado con `tracker.get_status()`
- [ ] Implementar formateo de tabla de tiempos
- [ ] Implementar cálculo de porcentajes
- [ ] Implementar detección de pausa activa
- [ ] Implementar emojis según estado
- [ ] Probar con tracking en diferentes estados

---

## Tests Manuales

### Flujo Completo de Pausas

```bash
# 1. Iniciar tracking (simular)
python -c "
from tracking import TimeTracker
t = TimeTracker('US-001', 'Test', 3, 'test')
t.start_tracking()
t.start_phase(3, 'Implementación')
print('✅ Tracking iniciado')
"

# 2. Ver estado
/track-status
# Esperado: Mostrar fase 3, sin pausa

# 3. Pausar
/track-pause "Reunión importante"
# Esperado: Confirmación de pausa

# 4. Ver estado nuevamente
/track-status
# Esperado: Mostrar pausa activa

# 5. Intentar pausar de nuevo (error esperado)
/track-pause "Otra razón"
# Esperado: Error "ya hay pausa activa"

# 6. Reanudar
/track-resume
# Esperado: Confirmación con duración de pausa

# 7. Ver estado final
/track-status
# Esperado: Sin pausa activa, tracking normal
```

---

## Comandos

```bash
# Crear estructura de skills
mkdir -p .claude/skills/{track-pause,track-resume,track-status}

# Crear archivos de skills
touch .claude/skills/track-pause/skill.md
touch .claude/skills/track-resume/skill.md
touch .claude/skills/track-status/skill.md

# Verificar estructura
tree .claude/skills/track-*
```

---

## Resultado

⬜ **PENDIENTE**

_A completar al finalizar el ticket._

**Skills creados:**
- .claude/skills/track-pause/skill.md
- .claude/skills/track-resume/skill.md
- .claude/skills/track-status/skill.md

**Commits esperados:**
1. `feat(skills): crear skill /track-pause (TICKET-040)`
2. `feat(skills): crear skill /track-resume (TICKET-040)`
3. `feat(skills): crear skill /track-status (TICKET-040)`

O un commit consolidado:
- `feat(skills): crear skills de tracking básico (/track-pause, /track-resume, /track-status) (TICKET-040)`
