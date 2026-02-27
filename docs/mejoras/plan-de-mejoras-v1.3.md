# Plan de Mejoras — Claude Dev Kit v1.3

**Fecha:** 2026-02-27
**Basado en:** `docs/developer/skill-implement-us-descripcion-tecnica.md` (análisis post v1.2)
**Estado:** Pendiente
**Tickets:** TICKET-080 a TICKET-089 (10 tickets · 24 discrepancias)

---

## Contexto

Durante la generación del documento técnico `skill-implement-us-descripcion-tecnica.md` (sesión 2026-02-27),
se detectaron **24 discrepancias** entre los archivos del skill y las convenciones establecidas.
Este plan organiza su resolución en tickets agrupados por archivo afectado y prioridad.

**Fuente de discrepancias:** Análisis del documento técnico, sección "Resumen de Discrepancias Detectadas (Post v1.2)"

| Severidad | Total |
|-----------|-------|
| Alta      | 3 (D6-1, D7-2, D9-1) |
| Media     | 13 |
| Baja      | 8 |
| **Total** | **24** |

---

## Resumen de Tickets

| Ticket | Título | Archivos afectados | Complejidad | Discrepancias | Depende de |
|--------|--------|-------------------|-------------|---------------|------------|
| TICKET-080 | Corregir discrepancias en config.json y perfiles | `config.json` | M | D6-1, D4-2, D5-2, D8-1, D0-1 | — |
| TICKET-081 | Documentar subcomando end-tracking | `skill.md`, `phase-9-final-report.md` | S | D9-1 | — |
| TICKET-082 | Corregir umbrales hardcodeados en Fase 7 | `phase-7-quality-gates.md` | M | D7-2, D7-1, D7-3 | — |
| TICKET-083 | Clarificar Fase 0: defaults y flag --skip-bdd | `phase-0-validation.md` | S | D0-2, D0-3 | — |
| TICKET-084 | Clarificar Fase 1: uso de template y nombres | `phase-1-bdd.md` | S | D1-1, D1-3, D1-2 | — |
| TICKET-085 | Clarificar Fase 2: rutas y prioridad de templates | `phase-2-planning.md` | S | D2-2, D2-3, D2-1 | — |
| TICKET-086 | Clarificar Fase 3: --skip-bdd y component_structure | `phase-3-implementation.md` | S | D3-1, D3-2 | TICKET-080 |
| TICKET-087 | Clarificar Fase 4: rutas de test según perfil | `phase-4-unit-tests.md` | S | D4-1 | TICKET-080 |
| TICKET-088 | Ajustes en Fases 5 y 6 | `phase-5-integration-tests.md`, `phase-6-bdd-validation.md` | S | D5-1, D6-2 | — |
| TICKET-089 | Ajustes menores en Fases 8 y 9 | `phase-8-documentation.md`, `phase-9-final-report.md` | S | D8-2, D9-2 | — |

**Complejidad:** S = 1-2 archivos · M = 3-5 archivos

---

## Diagrama de Dependencias

```
TICKET-080 (config.json) ──┬──► TICKET-086 (Fase 3)
                            └──► TICKET-087 (Fase 4)

TICKET-081 (end-tracking)  ──── independiente
TICKET-082 (Fase 7)        ──── independiente
TICKET-083 (Fase 0)        ──── independiente
TICKET-084 (Fase 1)        ──── independiente
TICKET-085 (Fase 2)        ──── independiente
TICKET-088 (Fases 5-6)     ──── independiente
TICKET-089 (Fases 8-9)     ──── independiente
```

**Ejecución paralela posible:** TICKET-081, TICKET-082, TICKET-083, TICKET-084, TICKET-085, TICKET-088, TICKET-089
**Ejecución secuencial:** TICKET-080 → TICKET-086 y TICKET-087

---

## Fases del Plan

### Fase 1 — Alta Prioridad (3 discrepancias)

Resolver las 3 discrepancias de severidad alta antes de avanzar.

#### TICKET-080 — Corregir discrepancias en config.json y perfiles

**Archivo principal:** `skills/implement-us/config.json`

**Discrepancias a resolver:**

| ID | Descripción | Acción |
|----|-------------|--------|
| D6-1 | `steps_path: "tests/features/steps/"` debe ser `"tests/step_defs/"` | Cambiar valor en `config.json` |
| D4-2 | `test_path: "tests/"` vs `pytest tests/unit/` en Fase 4 | Agregar `unit_test_path: "tests/unit/"` e `integration_test_path: "tests/integration/"` en `test_framework_config` |
| D5-2 | No existe `integration_test_path` en config | Incluido en D4-2 |
| D8-1 | `phases.8.approval_required: false` vs `skill.md` que dice "Aprobación: Requerida" | Cambiar a `true` en `config.json` (la Fase 8 sí requiere aprobación del usuario) |
| D0-1 | `variables.*.examples` incluye clave `"django"` en todas las variables | Eliminar todas las entradas `"django"` de los arrays `examples` |

**Criterio de cierre:** `config.json` actualizado + verificar que `customizations/*.json` no tengan conflictos con los cambios.

---

#### TICKET-081 — Documentar subcomando end-tracking

**Archivos:** `skills/implement-us/skill.md`, `skills/implement-us/phases/phase-9-final-report.md`

**Discrepancias a resolver:**

| ID | Descripción | Acción |
|----|-------------|--------|
| D9-1 | `end-tracking` aparece solo en Fase 9, no documentado en ningún otro archivo | Agregar en `skill.md` → sección de comandos de tracking: `track.py end-tracking` con descripción. Agregar nota en `phase-9-final-report.md` que explique qué hace el subcomando. |

**Acción concreta en `skill.md`:**
- Agregar `end-tracking` en la sección de comandos CLI (junto a `start-phase`, `end-phase`, `start-task`, etc.)
- Definición: "Cierra el tracking completo de la US, calcula tiempo total real, guarda el histórico y genera el reporte de tiempo final."

**Acción concreta en `phase-9-final-report.md`:**
- En el paso donde se invoca `track.py end-tracking`, agregar una nota que explique que este subcomando cierra el tracking completo (distinto de `end-phase` que cierra solo la fase actual).

**Criterio de cierre:** `end-tracking` documentado en `skill.md` + nota explicativa en `phase-9`.

---

#### TICKET-082 — Corregir umbrales hardcodeados en Fase 7

**Archivo:** `skills/implement-us/phases/phase-7-quality-gates.md`

**Discrepancias a resolver:**

| ID | Descripción | Acción |
|----|-------------|--------|
| D7-2 | Script Python `generar_reporte_quality` / `todas_metricas_pasan` hardcodea umbrales `8.0`, `10.0`, `20.0`, `95.0` | Reescribir el script para que lea umbrales desde `context.md` (campo `quality_gates`) en lugar de literales. Agregar comentario explicativo. |
| D7-1 | El cuerpo del archivo hardcodea "Target: ≥ 8.0/10", "Si no pasa (< 95%)" | Reemplazar todos los valores fijos por referencias al perfil activo: "Target: valor de `quality_gates.pylint.min_score` del perfil activo" |
| D7-3 | El template del `quality.json` tiene campo `"umbrales"` con valores fijos | El template debe usar placeholders `{PYLINT_MIN}`, `{CC_MAX}`, `{MI_MIN}`, `{COVERAGE_MIN}` con instrucción de que el agente los complete desde `context.md` |

**Criterio de cierre:** Ningún valor numérico de umbral hardcodeado en el archivo. Todos los umbrales referenciados dinámicamente desde el perfil activo / context.md.

---

### Fase 2 — Media Prioridad, Instrucciones Ambiguas (13 discrepancias)

Clarificar instrucciones en cada fase del skill para reducir comportamiento no determinista del agente.

#### TICKET-083 — Clarificar Fase 0: defaults y flag --skip-bdd

**Archivo:** `skills/implement-us/phases/phase-0-validation.md`

**Discrepancias a resolver:**

| ID | Descripción | Acción |
|----|-------------|--------|
| D0-2 | "Si alguno falta, crealo automáticamente con los defaults del perfil activo" no especifica qué escribir | Agregar sección con el contenido mínimo de `.pylintrc` (umbral del perfil activo) y `pytest.ini` (ruta de tests del perfil activo). El agente debe leer `quality_gates.pylint.min_score` desde `config.json` para escribir `.pylintrc`. |
| D0-3 | El template de `context.md` no incluye campo para `--skip-bdd` | Agregar campo `skip_bdd: true/false` en el template embebido del `context.md` dentro de este archivo. |

**Criterio de cierre:** Paso 6 con instrucciones precisas de qué escribir. Template de `context.md` incluye `skip_bdd`.

---

#### TICKET-084 — Clarificar Fase 1: uso de template y convención de nombres

**Archivo:** `skills/implement-us/phases/phase-1-bdd.md`

**Discrepancias a resolver:**

| ID | Descripción | Acción |
|----|-------------|--------|
| D1-1 | Fase menciona template `bdd-scenario.feature` sin instrucción de cómo usarlo | Agregar instrucción: "Leer el template de `.claude/templates/bdd/{perfil}-scenario.feature` como referencia estructural; completar con el contenido específico de la HU." |
| D1-3 | No especifica qué usar como `{nombre}` en el nombre del archivo | Agregar instrucción: "`{nombre}` = slug del título de la HU en minúsculas con guiones (ej. HU título 'Alta de producto' → `alta-de-producto`). Resultado: `US-001-alta-de-producto.feature`" |
| D1-2 | Perfiles `pyqt-mvc.json` y `fastapi-rest.json` definen `language: "es"` redundantemente | Eliminar `language` de `bdd_config` en los perfiles que la dupliquen. La clave canónica está en `config.json` base. |

**Criterio de cierre:** Instrucción de uso de template presente + regla de naming explícita + perfiles sin `language` redundante.

---

#### TICKET-085 — Clarificar Fase 2: rutas y prioridad de templates

**Archivo:** `skills/implement-us/phases/phase-2-planning.md`

**Discrepancias a resolver:**

| ID | Descripción | Acción |
|----|-------------|--------|
| D2-2 | El `📖 Template de Output` no especifica la ruta donde guardar el archivo | Agregar en la cabecera del template: `<!-- Guardar en: docs/plans/{US_ID}-plan.md -->` |
| D2-3 | `config.json` tiene `output_template: "templates/planning/implementation-plan.md"` pero la fase no lo invoca | Agregar instrucción al inicio de la fase: "Si existe `.claude/templates/planning/implementation-plan.md`, úsalo como base; si no, usa el template embebido en este archivo." Establecer prioridad: template externo > template embebido. |
| D2-1 | Ejemplos contienen "Registrar en Factory/Coordinator" (específico de PyQt) | Reemplazar por instrucción genérica: "Registrar en el mecanismo de composición del perfil activo (ej. Factory para PyQt, DI container para FastAPI)" |

**Criterio de cierre:** Ruta de salida explícita en template + prioridad de templates documentada + ejemplos agnósticos al stack.

---

#### TICKET-086 — Clarificar Fase 3: flag --skip-bdd y lectura de component_structure

**Archivo:** `skills/implement-us/phases/phase-3-implementation.md`

**Discrepancias a resolver:**

| ID | Descripción | Acción |
|----|-------------|--------|
| D3-1 | Fase 3 no verifica ni menciona el flag `--skip-bdd` antes de avanzar | Agregar en la precondición de Fase 3: "Leer `context.md → skip_bdd`. Si es `true`, verificar que Fase 6 también está omitida del plan de ejecución." Agregar nota de que en ese caso el agente no intentará leer el feature file en Fase 6. |
| D3-2 | No hay instrucción explícita de leer `customizations/{perfil}.json → component_structure` | Agregar como primer paso de implementación: "Leer `customizations/{perfil}.json → component_structure` para obtener las rutas exactas de cada componente antes de iniciar el ciclo de tareas." |

**Criterio de cierre:** Verificación de `--skip-bdd` en precondición + instrucción de lectura de `component_structure` al inicio.

---

#### TICKET-087 — Clarificar Fase 4: rutas de test según perfil activo

**Archivo:** `skills/implement-us/phases/phase-4-unit-tests.md`

**Discrepancias a resolver:**

| ID | Descripción | Acción |
|----|-------------|--------|
| D4-1 | Rutas de archivos de test inconsistentes entre perfiles (raíz vs subdirectorio) | Agregar instrucción: "Leer `config.json → test_framework_config.unit_test_path` (o del perfil activo si lo sobreescribe). Crear archivos en esa ruta. Ejecutar `pytest {unit_test_path} -v`." Actualizar el comando de ejecución para usar la ruta del config en vez de hardcodear `tests/unit/`. |

**Criterio de cierre:** Ruta de tests unitarios leída dinámicamente desde config. Comando `pytest` sin ruta hardcodeada.

---

### Fase 3 — Baja Prioridad, Ajustes Menores (8 discrepancias)

#### TICKET-088 — Ajustes en Fases 5 y 6

**Archivos:**
- `skills/implement-us/phases/phase-5-integration-tests.md`
- `skills/implement-us/phases/phase-6-bdd-validation.md`

**Discrepancias a resolver:**

| ID | Archivo | Descripción | Acción |
|----|---------|-------------|--------|
| D5-1 | phase-5 | La precondición asume que ya existen tests de integración | Reformular la precondición: en lugar de "verificar que `tests/integration/` exista y tenga contenido", decir "verificar que `pytest tests/unit/ -v` pasa (condición real de entrada)". |
| D6-2 | phase-6 | Perfiles definen `bdd_config.steps_template` pero la fase no incluye instrucción de usarlos | Agregar instrucción: "Si el perfil activo define `bdd_config.steps_template`, usar ese template como referencia para la estructura de los step definitions." |

**Criterio de cierre:** Precondición de Fase 5 correcta + instrucción de uso de `steps_template` en Fase 6.

---

#### TICKET-089 — Ajustes menores en Fases 8 y 9

**Archivos:**
- `skills/implement-us/phases/phase-8-documentation.md`
- `skills/implement-us/phases/phase-9-final-report.md`

**Discrepancias a resolver:**

| ID | Archivo | Descripción | Acción |
|----|---------|-------------|--------|
| D8-2 | phase-8 | Referencia residual a `python manage.py generate_swagger` (Django) | Eliminar la mención de Django; reemplazar por instrucción genérica: "Para APIs REST (FastAPI, Flask), ejecutar el comando de documentación del framework correspondiente si está disponible." |
| D9-2 | phase-9 | Fase no da instrucción de mapeo template → `quality.json` | Agregar instrucción: "Antes de completar el template de reporte, leer `quality/reports/{US_ID}-quality.json → umbrales` y mapear cada campo `{PYLINT_MIN}`, `{CC_MAX}`, `{MI_MIN}`, `{COVERAGE_MIN}` con los valores reales del archivo." |

**Criterio de cierre:** Sin referencias Django en phase-8 + instrucción de mapeo en phase-9.

---

## Criterio de Completitud v1.3

El plan está completo cuando:

- [ ] Los 10 tickets están ejecutados y commiteados
- [ ] Ninguna discrepancia D0-1 a D9-2 permanece sin resolver
- [ ] `config.json` pasa una revisión de coherencia (rutas consistentes con las fases)
- [ ] `skill.md` documenta todos los subcomandos del CLI de tracking
- [ ] `phase-7-quality-gates.md` no tiene valores numéricos de umbral hardcodeados
- [ ] El documento técnico `skill-implement-us-descripcion-tecnica.md` se actualiza para reflejar el estado post v1.3

---

## Estrategia de Commits

Un commit por ticket:

```
fix(config): corregir steps_path, test_path y limpiar referencias django (TICKET-080)
fix(skill): documentar subcomando end-tracking (TICKET-081)
fix(fase-7): corregir umbrales hardcodeados en quality gates (TICKET-082)
fix(fase-0): clarificar defaults pylintrc/pytest.ini y campo skip_bdd (TICKET-083)
fix(fase-1): clarificar uso de template BDD y convención de nombres (TICKET-084)
fix(fase-2): clarificar rutas de output y prioridad de templates (TICKET-085)
fix(fase-3): agregar verificación skip-bdd y lectura component_structure (TICKET-086)
fix(fase-4): usar ruta de tests desde config en lugar de hardcodeada (TICKET-087)
fix(fases-5-6): ajustar precondición Fase 5 y uso steps_template Fase 6 (TICKET-088)
fix(fases-8-9): eliminar referencia Django y agregar mapeo quality.json (TICKET-089)
```

---

**Generado:** 2026-02-27
**Versión objetivo:** v1.3
**Discrepancias fuente:** Análisis post v1.2 — documento técnico skill-implement-us
