# Plan de Mejoras — Claude Dev Kit v1.1

**Fecha:** 2026-02-23
**Completado:** 2026-02-24
**Basado en:** `docs/mejoras/registro de mejoras.md`
**Estado:** Completado — 11/11 tickets ejecutados · 4 PRs mergeados (#25–#28)

---

## Contexto

Este plan consolida las mejoras identificadas a partir del uso real del skill `/implement-us`
en un proyecto concreto (ejecución de HU-003), complementadas con análisis del código de las
fases y principios de diseño derivados del contexto de ejecución por agente digital.

**Observaciones base:**

| ID | Descripción breve |
|----|-------------------|
| OBS-001 | Instrucciones de tracking ignoradas por el agente |
| OBS-002 | Fase 2 no genera el plan ni solicita aprobación |
| OBS-003 | Decisión de BDD queda a cargo del usuario |
| OBS-004 | Comportamiento inconsistente entre ejecuciones |
| OBS-005 | Fase 9 no exige generar el archivo de reporte |
| OBS-006 | No existe definición centralizada de rutas de artefactos |
| PRIN-001 | Las estimaciones de esfuerzo humano no aplican a ejecución por agente |

---

## Resumen de Tickets

| Ticket | Título | Grupo | Complejidad | Depende de |
|--------|--------|-------|-------------|------------|
| TICKET-069 | Definir mapa centralizado de artefactos del skill | Fundaciones | M | — |
| TICKET-070 | Establecer convención estructural descriptivo vs. imperativo | Fundaciones | S | — |
| TICKET-071 | Agregar verificación de entorno y herramientas en Fase 0 | Fase 0 | S | TICKET-069 |
| TICKET-072 | Incorporar clasificación de HU y generación de archivo de contexto en Fase 0 | Fase 0 | M | TICKET-069 |
| TICKET-073 | Reescribir instrucciones de tracking como directivas imperativas (todas las fases) | Enforcement | M | TICKET-070 |
| TICKET-074 | Reforzar Fase 2 — plan obligatorio y aprobación bloqueante | Enforcement | S | TICKET-069, TICKET-070 |
| TICKET-075 | Reforzar Fase 3 — leer plan y criterios de HU al inicio de cada tarea | Enforcement | S | TICKET-069, TICKET-074 |
| TICKET-076 | Agregar gates de entrada y checklists de salida en todas las fases | Enforcement | L | TICKET-069, TICKET-070 |
| TICKET-077 | Reforzar Fase 9 — reporte obligatorio antes de cierre | Enforcement | S | TICKET-069, TICKET-070 |
| TICKET-078 | Definir protocolo de recuperación ante fallas de fase | Resiliencia | M | TICKET-076 |
| TICKET-079 | Remover estimaciones de tiempo de la ejecución del skill (PRIN-001) | Principios | S | — |

**Complejidad:** S = cambio acotado a 1-2 archivos · M = afecta 3-5 archivos · L = afecta todas las fases

---

## Diagrama de Dependencias

```
TICKET-069 (artefactos)  ──┬──► TICKET-071 (entorno Fase 0)
                           ├──► TICKET-072 (contexto Fase 0)
                           ├──► TICKET-074 (Fase 2)
                           ├──► TICKET-075 (Fase 3)
                           ├──► TICKET-076 (gates globales)
                           └──► TICKET-077 (Fase 9)

TICKET-070 (convención)  ──┬──► TICKET-073 (tracking)
                           ├──► TICKET-074 (Fase 2)
                           ├──► TICKET-076 (gates globales)
                           └──► TICKET-077 (Fase 9)

TICKET-076 (gates)       ──► TICKET-078 (recuperación)

TICKET-079 (PRIN-001)    — independiente, sin dependencias
```

**Orden de ejecución recomendado:**
1. TICKET-069 y TICKET-070 en paralelo (fundaciones, sin dependencias entre sí)
2. TICKET-079 en paralelo con los anteriores (independiente)
3. TICKET-071, TICKET-072, TICKET-073 en paralelo (dependen solo de fundaciones)
4. TICKET-074, TICKET-075, TICKET-076, TICKET-077 en paralelo
5. TICKET-078 al final (depende de TICKET-076)

---

## Tickets

---

### TICKET-069: Definir mapa centralizado de artefactos del skill

**Grupo:** Fundaciones
**Estado:** Pendiente
**Prioridad:** Bloqueante (TICKET-071 a TICKET-077 dependen de este)
**Complejidad:** M
**Observación base:** OBS-006

#### Objetivo

Crear un único lugar autoritativo que defina la estructura de directorios y convención
de nombres para todos los artefactos generados durante la ejecución del skill.
Actualmente cada fase define sus rutas de forma dispersa e inconsistente.

#### Archivos a crear o modificar

- **Crear:** `skills/implement-us/artifacts.md` — mapa completo de artefactos
- **Modificar:** `skills/implement-us/skill.md` — referenciar `artifacts.md` al inicio

#### Contenido de `artifacts.md`

Debe definir la estructura completa con descripción de cada artefacto, la fase que lo genera
y las fases que lo consumen:

```
docs/
  bdd/{US_ID}.feature              # Generado: Fase 1 · Consumido: Fase 6
  plans/{US_ID}-context.md         # Generado: Fase 0 · Consumido: Fases 1-9
  plans/{US_ID}-plan.md            # Generado: Fase 2 · Consumido: Fases 3, 9
  reports/{US_ID}-report.md        # Generado: Fase 9
quality/
  reports/{US_ID}-pylint.json      # Generado: Fase 7 · Consumido: Fase 9
  reports/{US_ID}-cc.json          # Generado: Fase 7 · Consumido: Fase 9
  reports/{US_ID}-coverage.json    # Generado: Fase 7 · Consumido: Fase 9
  reports/{US_ID}-quality.json     # Generado: Fase 7 · Consumido: Fase 9
```

#### Criterios de Aceptación

- [ ] `skills/implement-us/artifacts.md` existe con el mapa completo
- [ ] Cada entrada del mapa especifica: ruta, fase generadora, fases consumidoras
- [ ] `skill.md` referencia `artifacts.md` como fuente de verdad para rutas
- [ ] El mapa incluye todos los artefactos mencionados dispersamente en las fases actuales

#### Dependencias

- **Depende de:** —
- **Bloquea a:** TICKET-071, TICKET-072, TICKET-074, TICKET-075, TICKET-076, TICKET-077

---

### TICKET-070: Establecer convención estructural descriptivo vs. imperativo

**Grupo:** Fundaciones
**Estado:** Pendiente
**Prioridad:** Bloqueante (tickets de reescritura dependen de esta convención)
**Complejidad:** S
**Observación base:** OBS-001, OBS-002, OBS-004, OBS-005 (causa raíz común)

#### Objetivo

Definir y documentar una convención estructural que distinga claramente el contenido
**imperativo** (acciones que el agente DEBE ejecutar) del contenido **descriptivo**
(contexto, referencias y ejemplos que el agente puede leer pero no ejecutar).

Esta convención es la guía que deben seguir todos los tickets de reescritura posteriores.

#### Archivos a crear o modificar

- **Crear:** `skills/implement-us/conventions.md` — definición de la convención
- **Modificar:** `skills/implement-us/skill.md` — referenciar `conventions.md`

#### Contenido de `conventions.md`

Debe definir:

1. **Secciones imperativas** — marcadas con encabezado `## 🔴 Acción Requerida`.
   El agente DEBE ejecutar su contenido antes de avanzar.

2. **Secciones de referencia** — marcadas con encabezado `## 📖 Referencia`.
   El agente puede consultar su contenido pero no está obligado a ejecutarlo.

3. **Formato de instrucción imperativa** — texto en lenguaje natural directo,
   sin código Python embebido como ejemplo:
   > ✅ "Ejecutá el comando: `pylint src/ --output-format=json`"
   > ❌ `tracker.start_phase(7, "Quality Gates")` como bloque de código sin contexto

4. **Formato de checklist de salida** — sección `## ✅ Checklist de Salida` al final
   de cada fase con ítems que el agente debe confirmar antes de avanzar.

#### Criterios de Aceptación

- [ ] `skills/implement-us/conventions.md` creado con la convención completa
- [ ] La convención incluye ejemplos de antes/después para cada tipo de sección
- [ ] `skill.md` referencia `conventions.md` indicando que todos los archivos de fase deben seguirla

#### Dependencias

- **Depende de:** —
- **Bloquea a:** TICKET-073, TICKET-074, TICKET-076, TICKET-077

---

### TICKET-071: Agregar verificación de entorno y herramientas en Fase 0

**Grupo:** Fase 0
**Estado:** Pendiente
**Prioridad:** Alta
**Complejidad:** S
**Observación base:** Nueva (análisis del skill)

#### Objetivo

Agregar al inicio de `phase-0-validation.md` una verificación explícita de que las
herramientas requeridas por el skill están instaladas y operativas. Si alguna herramienta
falla, el proceso debe detenerse con un mensaje claro antes de comenzar la implementación
(fail-fast).

#### Archivos a modificar

- `skills/implement-us/phases/phase-0-validation.md`

#### Comportamiento esperado

Al inicio de Fase 0, antes de cualquier otra acción, ejecutar:

```bash
python -m pylint --version     # Requerido: Fase 7
python -m radon --version      # Requerido: Fase 7
python -m pytest --version     # Requerido: Fases 4, 5, 6, 7
python -m pytest_bdd --version # Requerido: Fase 6
```

Si alguno falla:
> **🚫 STOP — Herramienta `{nombre}` no disponible.**
> Instalala con `pip install {paquete}` antes de continuar.
> No se puede garantizar la ejecución completa del skill sin esta herramienta.

#### Criterios de Aceptación

- [ ] `phase-0-validation.md` incluye verificación de herramientas como primer paso
- [ ] La instrucción está en formato imperativo (según convención de TICKET-070)
- [ ] Incluye el comando de instalación correspondiente a cada herramienta faltante
- [ ] El proceso se detiene explícitamente si alguna herramienta no está disponible

#### Dependencias

- **Depende de:** TICKET-069 (para saber qué herramientas requiere cada fase), TICKET-070 (convención)
- **Bloquea a:** —

---

### TICKET-072: Incorporar clasificación de HU y generación de archivo de contexto en Fase 0

**Grupo:** Fase 0
**Estado:** Pendiente
**Prioridad:** Alta
**Complejidad:** M
**Observación base:** OBS-003, OBS-006

#### Objetivo

Extender `phase-0-validation.md` para que, además de validar el entorno, tome
**decisiones explícitas** sobre la ejecución del skill y las persista en un archivo
de contexto. Este archivo será la fuente de verdad que todas las fases siguientes
leen al inicio para conocer: qué fases ejecutar, dónde están los artefactos y
cuáles son los umbrales del perfil activo.

#### Archivos a modificar

- `skills/implement-us/phases/phase-0-validation.md`

#### Comportamiento esperado

**Paso nuevo — Clasificar tipo de HU:**

Analizar la descripción y criterios de aceptación de la HU para determinar su tipo:

| Tipo | ¿BDD aplica? |
|------|--------------|
| Nueva funcionalidad | ✅ Sí |
| Mejora de comportamiento existente | ✅ Sí |
| Refactorización (sin cambio de comportamiento) | ❌ No |
| Eliminación de code smells | ❌ No |
| Corrección de bug | ⚠️ Depende — informar al usuario |

Informar la decisión al usuario y permitir override antes de continuar.

**Paso nuevo — Generar `docs/plans/{US_ID}-context.md`:**

```markdown
# Contexto de Ejecución — {US_ID}

## Historia de Usuario
- **ID:** {US_ID}
- **Título:** {US_TITLE}
- **Tipo:** {HU_TYPE}

## Decisiones de Ejecución
- **BDD:** {Sí / No — justificación}
- **Fases a ejecutar:** 0, 1 (si BDD), 2, 3, 4, 5, 6 (si BDD), 7, 8, 9

## Perfil Activo
- **Perfil:** {PROFILE}
- **Umbrales de calidad:** pylint ≥ {X}, CC ≤ {Y}, MI ≥ {Z}, cobertura ≥ {W}%

## Rutas de Artefactos
- BDD feature: docs/bdd/{US_ID}.feature
- Plan: docs/plans/{US_ID}-plan.md
- Reporte: docs/reports/{US_ID}-report.md
- Quality report: quality/reports/{US_ID}-quality.json
```

**VERIFICACIÓN OBLIGATORIA:** Antes de avanzar a Fase 1, confirmá que el archivo
`docs/plans/{US_ID}-context.md` existe en disco: `ls docs/plans/{US_ID}-context.md`.

#### Criterios de Aceptación

- [ ] `phase-0-validation.md` incluye paso de clasificación de HU con la tabla de tipos
- [ ] La decisión de BDD se informa al usuario y permite override explícito
- [ ] Se genera `docs/plans/{US_ID}-context.md` con todas las secciones definidas
- [ ] Se verifica la existencia del archivo antes de avanzar
- [ ] Los umbrales de calidad se leen del perfil activo (no hardcodeados)

#### Dependencias

- **Depende de:** TICKET-069 (rutas de artefactos)
- **Bloquea a:** —

---

### TICKET-073: Reescribir instrucciones de tracking como directivas imperativas

**Grupo:** Enforcement
**Estado:** Pendiente
**Prioridad:** Alta
**Complejidad:** M
**Observación base:** OBS-001

#### Objetivo

Reescribir las instrucciones de tracking en todos los archivos de fase, convirtiendo
los bloques de código Python (que el agente interpreta como documentación) en
directivas imperativas en lenguaje natural que el agente reconoce como acciones a ejecutar.

#### Archivos a modificar

Todos los archivos de fase:
- `skills/implement-us/phases/phase-0-validation.md`
- `skills/implement-us/phases/phase-1-bdd.md`
- `skills/implement-us/phases/phase-2-planning.md`
- `skills/implement-us/phases/phase-3-implementation.md`
- `skills/implement-us/phases/phase-4-unit-tests.md`
- `skills/implement-us/phases/phase-5-integration-tests.md`
- `skills/implement-us/phases/phase-6-bdd-validation.md`
- `skills/implement-us/phases/phase-7-quality-gates.md`
- `skills/implement-us/phases/phase-8-documentation.md`
- `skills/implement-us/phases/phase-9-final-report.md`

#### Patrón de cambio (antes → después)

**Antes** (ignorado por el agente):
```python
tracker.start_phase(7, "Quality Gates")
```

**Después** (directiva imperativa):
> **🔴 Acción Requerida — Iniciar tracking de fase**
> Ejecutá el siguiente comando antes de cualquier otra acción en esta fase:
> `python .claude/tracking/time_tracker.py start --phase 7 --us {US_ID}`

El mismo patrón aplica para `end_phase` y `start_task`/`end_task` en Fase 3.

#### Criterios de Aceptación

- [ ] Ningún archivo de fase contiene bloques de código Python como única instrucción de tracking
- [ ] Todas las instrucciones de tracking están en secciones `## 🔴 Acción Requerida`
- [ ] El comando concreto a ejecutar está especificado en cada instrucción
- [ ] El patrón es consistente en los 10 archivos de fase

#### Dependencias

- **Depende de:** TICKET-070 (convención de secciones)
- **Bloquea a:** —

---

### TICKET-074: Reforzar Fase 2 — plan obligatorio y aprobación bloqueante

**Grupo:** Enforcement
**Estado:** Pendiente
**Prioridad:** Alta
**Complejidad:** S
**Observación base:** OBS-002

#### Objetivo

Agregar a `phase-2-planning.md` instrucciones imperativas que garanticen que:
1. El archivo `docs/plans/{US_ID}-plan.md` exista en disco antes de continuar
2. El usuario haya dado aprobación explícita antes de avanzar a Fase 3

#### Archivos a modificar

- `skills/implement-us/phases/phase-2-planning.md`

#### Contenido a agregar al final de la fase

**Sección: Verificación Obligatoria de Output**
> **🔴 Acción Requerida — Verificar existencia del plan**
> Antes de continuar, ejecutá: `ls docs/plans/{US_ID}-plan.md`
> Si el archivo no existe, generalo siguiendo el template de esta fase antes de avanzar.

**Sección: Checkpoint de Aprobación**
> **🚫 STOP — No avances a Fase 3 hasta que:**
> 1. El archivo `docs/plans/{US_ID}-plan.md` exista en disco ✅
> 2. El usuario haya respondido explícitamente con aprobación del plan
>
> Presentá el plan al usuario y esperá su respuesta antes de continuar.

**Checklist de Salida:**
- [ ] `docs/plans/{US_ID}-plan.md` existe en disco
- [ ] El plan fue presentado al usuario
- [ ] El usuario aprobó el plan explícitamente
- [ ] Tracking de Fase 2 cerrado

#### Criterios de Aceptación

- [ ] `phase-2-planning.md` incluye verificación imperativa de existencia del archivo
- [ ] Incluye bloque STOP explícito antes de avanzar a Fase 3
- [ ] El checklist de salida está completo y en formato verificable
- [ ] Las instrucciones siguen la convención de TICKET-070

#### Dependencias

- **Depende de:** TICKET-069 (ruta del artefacto), TICKET-070 (convención)
- **Bloquea a:** TICKET-075

---

### TICKET-075: Reforzar Fase 3 — leer plan y criterios de HU al inicio de cada tarea

**Grupo:** Enforcement
**Estado:** Pendiente
**Prioridad:** Media
**Complejidad:** S
**Observación base:** OBS-004

#### Objetivo

Agregar a `phase-3-implementation.md` instrucciones explícitas para que el agente:
1. Lea `docs/plans/{US_ID}-plan.md` al inicio de la fase (no lo reconstruya de memoria)
2. Lea los criterios de aceptación de la HU al inicio de la fase
3. Marque cada tarea como en progreso antes de implementarla y como completada al terminar

#### Archivos a modificar

- `skills/implement-us/phases/phase-3-implementation.md`

#### Instrucción a agregar al inicio de la fase

> **🔴 Acción Requerida — Establecer contexto antes de implementar**
>
> 1. Verificá que `docs/plans/{US_ID}-plan.md` existe: `ls docs/plans/{US_ID}-plan.md`
>    Si no existe, **no avances** — ejecutá Fase 2 primero.
>
> 2. Leé el plan completo para identificar la próxima tarea pendiente.
>    No inferir el estado del plan desde el contexto de la conversación.
>
> 3. Leé los criterios de aceptación de la HU en `{HU_PATH}`.
>    Antes de implementar cada tarea, verificá que contribuye a al menos un criterio.
>    Si encontrás criterios sin cobertura en el plan, informá al usuario antes de continuar.

#### Instrucción a agregar por tarea (paso 9 del flujo actual)

Reforzar la instrucción existente de actualización de checkboxes para hacerla imperativa:

> **🔴 Acción Requerida — Actualizar plan después de cada tarea**
> Inmediatamente después de completar la tarea, editá `docs/plans/{US_ID}-plan.md`
> y marcá el checkbox: `- [x] {TASK_NAME}`. No avances a la siguiente tarea sin
> haber actualizado el archivo en disco.

#### Criterios de Aceptación

- [ ] `phase-3-implementation.md` inicia con verificación imperativa de existencia del plan
- [ ] Incluye instrucción de lectura de criterios de HU
- [ ] La instrucción de actualización de checkboxes es imperativa y en sección `## 🔴 Acción Requerida`
- [ ] Incluye verificación de que cada tarea cubre al menos un criterio de aceptación

#### Dependencias

- **Depende de:** TICKET-069 (rutas), TICKET-074 (garantiza que el plan existe)
- **Bloquea a:** —

---

### TICKET-076: Agregar gates de entrada y checklists de salida en todas las fases

**Grupo:** Enforcement
**Estado:** Pendiente
**Prioridad:** Alta
**Complejidad:** L
**Observación base:** OBS-004, OBS-002, OBS-005 (patrón generalizado)

#### Objetivo

Agregar a cada archivo de fase:
1. **Gate de entrada:** verificación de que los artefactos de la fase anterior existen
2. **Checklist de salida:** lista de condiciones que deben cumplirse antes de avanzar

Esto garantiza que el proceso sea reproducible independientemente del contexto de sesión
en que se ejecute.

#### Archivos a modificar

Todos los archivos de fase (phase-1-bdd.md a phase-9-final-report.md).

#### Estructura a agregar en cada fase

**Al inicio — Gate de entrada:**
```markdown
## 🔴 Acción Requerida — Verificar precondiciones

Antes de comenzar esta fase, confirmá que existen los siguientes artefactos:
- `docs/plans/{US_ID}-context.md` — generado en Fase 0
- `{artefacto_fase_anterior}` — generado en Fase {N-1}

Ejecutá: `ls {ruta_artefacto}`
Si algún artefacto no existe, **no avances** — completá la fase correspondiente primero.
```

**Al final — Checklist de salida:**
```markdown
## ✅ Checklist de Salida

Antes de avanzar a Fase {N+1}, confirmá que:
- [ ] {artefacto_de_esta_fase} existe en disco (`ls {ruta}`)
- [ ] Tracking de esta fase cerrado
- [ ] {condición específica de la fase}
```

#### Mapa de precondiciones y outputs por fase

| Fase | Precondición (gate entrada) | Output a verificar |
|------|-----------------------------|--------------------|
| Fase 1 | `context.md` existe | `docs/bdd/{US_ID}.feature` |
| Fase 2 | `context.md` existe | `docs/plans/{US_ID}-plan.md` + aprobación usuario |
| Fase 3 | `plan.md` existe | Archivos de implementación + plan actualizado |
| Fase 4 | Archivos de implementación existen | Tests unitarios pasando |
| Fase 5 | Tests unitarios pasando | Tests de integración pasando |
| Fase 6 | `.feature` existe + implementación existe | Escenarios BDD pasando |
| Fase 7 | Tests pasando | `quality/reports/{US_ID}-quality.json` con estado APROBADO |
| Fase 8 | Quality gates APROBADO | Documentación generada |
| Fase 9 | Quality gates APROBADO | `docs/reports/{US_ID}-report.md` |

#### Criterios de Aceptación

- [ ] Cada archivo de fase (1-9) tiene sección de gate de entrada al inicio
- [ ] Cada archivo de fase (0-9) tiene checklist de salida al final
- [ ] Los artefactos referenciados usan las rutas del mapa de TICKET-069
- [ ] Ninguna fase puede avanzar sin confirmar su checklist de salida

#### Dependencias

- **Depende de:** TICKET-069 (rutas), TICKET-070 (convención)
- **Bloquea a:** TICKET-078

---

### TICKET-077: Reforzar Fase 9 — reporte obligatorio antes de cierre

**Grupo:** Enforcement
**Estado:** Pendiente
**Prioridad:** Alta
**Complejidad:** S
**Observación base:** OBS-005

#### Objetivo

Agregar a `phase-9-final-report.md` instrucciones imperativas que garanticen que
`docs/reports/{US_ID}-report.md` existe en disco antes de cerrar el tracking
y dar por finalizada la HU.

#### Archivos a modificar

- `skills/implement-us/phases/phase-9-final-report.md`

#### Contenido a agregar

**Al inicio de la fase — Verificación de insumos:**
> **🔴 Acción Requerida — Verificar insumos del reporte**
> El reporte final consolida datos de fases anteriores. Verificá que existen:
> - `docs/plans/{US_ID}-plan.md` (para listar tareas completadas)
> - `quality/reports/{US_ID}-quality.json` (para incluir métricas reales)

**Al final — Bloqueo de cierre:**
> **🚫 STOP — No cierres el tracking hasta que:**
> 1. `docs/reports/{US_ID}-report.md` exista en disco:
>    `ls docs/reports/{US_ID}-report.md`
> 2. El reporte incluya las métricas reales de `quality/reports/{US_ID}-quality.json`
> 3. El usuario haya recibido el link al reporte

#### Criterios de Aceptación

- [ ] `phase-9-final-report.md` incluye verificación de insumos al inicio
- [ ] Incluye bloque STOP antes de cerrar el tracking
- [ ] El reporte generado incluye métricas leídas desde los archivos de Fase 7 (no reconstruidas de memoria)
- [ ] Las instrucciones siguen la convención de TICKET-070

#### Dependencias

- **Depende de:** TICKET-069 (rutas), TICKET-070 (convención)
- **Bloquea a:** —

---

### TICKET-078: Definir protocolo de recuperación ante fallas de fase

**Grupo:** Resiliencia
**Estado:** Pendiente
**Prioridad:** Media
**Complejidad:** M
**Observación base:** Nueva (análisis del skill)

#### Objetivo

Definir qué debe hacer el agente cuando una fase falla: tests que no pasan, quality gates
que no se alcanzan, BDD que no se valida. Sin protocolo explícito, el agente improvisa
y puede avanzar a la siguiente fase con un estado inválido.

#### Archivos a modificar

- `skills/implement-us/skill.md` — sección de manejo de fallas (global)
- `skills/implement-us/phases/phase-4-unit-tests.md` — protocolo específico
- `skills/implement-us/phases/phase-5-integration-tests.md` — protocolo específico
- `skills/implement-us/phases/phase-6-bdd-validation.md` — protocolo específico
- `skills/implement-us/phases/phase-7-quality-gates.md` — protocolo específico

#### Protocolo general a definir en `skill.md`

```
Si una fase falla:
1. Identificar causa concreta (no asumir, leer el output completo del error)
2. Determinar si la corrección corresponde a esta fase o a una fase anterior
3. Aplicar corrección en la fase correspondiente
4. Re-ejecutar la fase completa (no solo el paso que falló)
5. No avanzar a la siguiente fase hasta que el checklist de salida esté completo
6. Si después de 2 intentos la fase sigue fallando, informar al usuario
   y no continuar de forma autónoma
```

#### Protocolos específicos por fase

- **Fase 4/5 — Tests fallan:** volver a Fase 3 e identificar qué implementación está incompleta
- **Fase 6 — BDD falla:** puede ser issue en implementación (→ Fase 3) o en los escenarios (→ Fase 1)
- **Fase 7 — Quality gate falla:** corregir en la implementación, re-ejecutar Fase 7 completa.
  Si el umbral no se alcanza después de correcciones razonables, documentar como excepción
  justificada en el reporte (no ignorar silenciosamente)

#### Criterios de Aceptación

- [ ] `skill.md` incluye sección "Manejo de Fallas" con el protocolo general
- [ ] Fases 4, 5, 6 y 7 incluyen sección explícita de qué hacer si la fase falla
- [ ] El protocolo especifica el límite de intentos autónomos antes de escalar al usuario
- [ ] Queda claro que una fase con estado RECHAZADO no puede avanzar

#### Dependencias

- **Depende de:** TICKET-076 (los checklists definen cuándo una fase "falla")
- **Bloquea a:** —

---

### TICKET-079: Remover estimaciones de tiempo de la ejecución del skill

**Grupo:** Principios
**Estado:** Pendiente
**Prioridad:** Media
**Complejidad:** S
**Principio base:** PRIN-001

#### Objetivo

Las estimaciones de duración en los archivos de fase ("Duración estimada: 10-15 minutos")
fueron definidas con base en esfuerzo humano. Presentarlas durante la ejecución por agente
genera expectativas incorrectas. El sistema de tracking tiene como propósito acumular datos
reales de performance del agente, no medir varianza respecto a una línea base humana.

#### Archivos a modificar

Todos los archivos de fase (phase-0 a phase-9) y `skill.md`.

#### Cambios a aplicar

1. **Remover** la línea `**Duración estimada:** X minutos` del encabezado de cada fase.
   Puede mantenerse en un comentario interno como referencia de diseño si se considera útil,
   pero no debe mostrarse durante la ejecución.

2. **Remover** cualquier mención de tiempo estimado dentro del contenido de las fases
   que sea presentada como objetivo a cumplir.

3. **Mantener** las estimaciones en el plan de implementación generado por Fase 2
   (`docs/plans/{US_ID}-plan.md`) como referencia de complejidad relativa entre tareas,
   pero sin presentarlas como tiempos esperados de ejecución.

#### Criterios de Aceptación

- [ ] Ningún archivo de fase muestra "Duración estimada" en el encabezado
- [ ] No hay instrucciones que comparen tiempo real con estimado
- [ ] El sistema de tracking sigue registrando tiempos reales (no se modifica su funcionamiento)
- [ ] El propósito del tracking (acumular baselines de agente) queda documentado en `skill.md`

#### Dependencias

- **Depende de:** —
- **Bloquea a:** —

---

## Estado del Plan

| Ticket | Estado | PR |
|--------|--------|----|
| TICKET-069 | ✅ Completado | #25 |
| TICKET-070 | ✅ Completado | #25 |
| TICKET-071 | ✅ Completado | #26 |
| TICKET-072 | ✅ Completado | #26 |
| TICKET-073 | ✅ Completado | #26 |
| TICKET-074 | ✅ Completado | #27 |
| TICKET-075 | ✅ Completado | #27 |
| TICKET-076 | ✅ Completado | #27 |
| TICKET-077 | ✅ Completado | #27 |
| TICKET-078 | ✅ Completado | #28 |
| TICKET-079 | ✅ Completado | #25 |

**Gestión:** GitHub Issues #14–#24 · Milestone "v1.1 — Mejoras implement-us" (11/11 cerrados)

---

**Plan completado.** Ver CHANGELOG.md sección `[Sin publicar]` para el registro formal de cambios.
