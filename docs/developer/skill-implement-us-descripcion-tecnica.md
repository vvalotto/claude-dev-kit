# Descripción Técnica del Skill implement-us

Documento de referencia interna para desarrolladores del framework.
Describe la estructura completa del skill, fase a fase: entradas, salidas, templates, convenciones, artefactos y discrepancias detectadas (estado post v1.2).

**Skill:** `/implement-us`
**Versión analizada:** 2.1.0 (post correcciones v1.2)
**Archivos de referencia:** `skill.md`, `artifacts.md`, `conventions.md`, `config.json`, `customizations/*.json`, `phases/phase-*.md`

---

## Precondiciones Generales para Ejecutar el Skill

Antes de invocar `/implement-us`, el entorno del proyecto destino debe satisfacer:

| Precondición | Verificación | Quién la valida |
|---|---|---|
| Python 3.10+ disponible | `python --version` | Usuario / Fase 0 |
| Repositorio git inicializado | `git status` | Usuario |
| Framework instalado en `.claude/` | `ls .claude/skills/implement-us/config.json` | Fase 0 |
| Perfil de customización activo | Clave en `config.json` | Fase 0 |
| pylint instalado | `python -m pylint --version` | Fase 0 |
| radon instalado | `python -m radon --version` | Fase 0 |
| pytest instalado | `python -m pytest --version` | Fase 0 |
| pytest-bdd instalado (si aplica BDD) | `python -c "import pytest_bdd; ..."` | Fase 0 |
| Historia de usuario accesible | Documento local / Issue / Ticket | Confirmado en Fase 0 |

El skill no define una precondición explícita sobre la existencia de CLAUDE.md, aunque la Fase 0 asume que puede leer quality gates de `config.json`.

---

## Fases del Skill

### Fase 0 — Validación de Contexto

**Descripción conceptual**

La Fase 0 es el punto de entrada del skill. Su responsabilidad es triple: verificar que el entorno técnico es apto para ejecutar el skill (herramientas disponibles), establecer las fuentes de información que guiarán la implementación (HU y arquitectura), y generar el archivo de contexto `context.md` que todas las fases siguientes leerán como fuente de verdad sobre la ejecución.

La fase pregunta explícitamente al usuario antes de buscar la HU o la arquitectura —a diferencia de un enfoque que asume rutas por defecto— lo cual la hace resiliente a proyectos con estructuras diversas. También clasifica el tipo de HU para decidir si BDD aplica, y registra los umbrales de calidad del perfil activo en el contexto.

El archivo de contexto (`context.md`) es el único artefacto que esta fase produce, y es la única manera confiable de que las fases 1-9 compartan información sin depender de la memoria de la conversación.

**Entradas**

| Entrada | Tipo | Requerida | Fuente |
|---|---|---|---|
| `{US_ID}` | Parámetro CLI | ✅ Sí | Usuario |
| `--producto {PRODUCT}` | Parámetro CLI | ❌ No | Usuario (default en config.json) |
| Perfil activo | `config.json` + `customizations/*.json` | ✅ Sí | Instalación del framework |
| Ubicación de la HU | Respuesta del usuario (Paso 3) | ✅ Sí | Usuario en runtime |
| Ubicación de arquitectura | Respuesta del usuario (Paso 3) | ❌ Opcional | Usuario en runtime |

**Templates requeridos**

Ninguno. El template del `context.md` está embebido directamente en el archivo de fase (Paso 8), no proviene de un archivo externo.

**Convenciones aplicables**

- Paso 1 es imperativo (`🔴`): tracking antes que todo.
- El orden de los pasos es estricto (instrucción al inicio del archivo).
- La verificación de existencia del artefacto (Paso 9) es imperativa antes de cerrar.

**Artefactos**

| Artefacto | Operación | Ruta |
|---|---|---|
| `{US_ID}-context.md` | **Genera** | `docs/plans/{US_ID}-context.md` |
| `config.json` | **Lee** | `.claude/skills/implement-us/config.json` |
| `customizations/{perfil}.json` | **Lee** | `.claude/skills/implement-us/customizations/` |
| `.pylintrc`, `pytest.ini` | **Crea si no existen** | raíz del proyecto |

**Salidas**

| Salida | Tipo | Descripción |
|---|---|---|
| `docs/plans/{US_ID}-context.md` | Artefacto físico | Fuentes de HU/arquitectura, perfil activo, umbrales, decisión BDD, fases a ejecutar |
| Confirmación de herramientas | En conversación | Lista de herramientas verificadas |
| Clasificación de HU + decisión BDD | En conversación | Tipo de HU y si aplica BDD (confirmado por usuario) |

**Dependencias**

| Dirección | Fase | Qué provee |
|---|---|---|
| → siguiente | Fase 1 | `context.md` con decisión BDD y umbrales |
| → siguiente | Fase 2 | `context.md` con patrón arquitectónico |
| → siguiente | Todas (1-9) | `context.md` como fuente de verdad del contexto |

**Discrepancias detectadas (post v1.2)**

| ID | Descripción | Severidad |
|---|---|---|
| D0-1 | `config.json` → `variables.*.examples` incluye clave `"django"` en todas las variables (arquitectura, componente, path, etc.), aunque Django no es un perfil soportado. No causa fallo operativo pero es inconsistente con la eliminación de Django del skill. | Baja |
| D0-2 | Fase 0, Paso 6: "Si alguno falta, crealo automáticamente con los defaults del perfil activo" — no especifica cuáles son esos defaults ni qué valores escribe en `.pylintrc` o `pytest.ini`. El agente debe inventar valores. | Media |
| D0-3 | El `context.md` template no incluye un campo para registrar si `--skip-bdd` fue activado, aunque ese flag afecta las fases a ejecutar. | Baja |

---

### Fase 1 — Generación de Escenarios BDD

**Descripción conceptual**

La Fase 1 transforma los criterios de aceptación de la HU en escenarios ejecutables en formato Gherkin. Es la única fase que requiere que el usuario haya aprobado explícitamente la HU como candidata a BDD (decisión tomada en Fase 0). Si el usuario eligió `--skip-bdd` o la HU fue clasificada como no-BDD, esta fase se omite.

El rol central del agente es interpretar los criterios de aceptación y generar escenarios Given-When-Then que capturen el comportamiento observable del sistema desde la perspectiva del usuario. Cada criterio genera al menos un escenario; los edge cases y caminos de error se agregan a criterio del agente.

El archivo `.feature` generado es el artefacto de mayor longevidad del skill: persiste como especificación ejecutable hasta la Fase 6, donde se implementan sus steps y se valida que el sistema cumple con el comportamiento descrito.

**Entradas**

| Entrada | Tipo | Requerida | Fuente |
|---|---|---|---|
| `docs/plans/{US_ID}-context.md` | Artefacto | ✅ Sí | Fase 0 |
| Criterios de aceptación de la HU | Leídos de la fuente HU | ✅ Sí | Fase 0, Paso 4 |
| Perfil activo (idioma, tag_prefix) | `config.json` → `bdd_config` | ✅ Sí | Instalación |
| Template de escenarios | Ver templates | ❌ Opcional | `templates/bdd/` |

**Templates requeridos**

| Template | Ruta en config.json | Ruta en perfil (si difiere) |
|---|---|---|
| Feature template genérico | `templates/bdd/scenario.feature` | PyQt: `templates/bdd/pyqt-scenario.feature`<br>FastAPI: `templates/bdd/api-scenario.feature` |

> **Nota:** La fase menciona el template (`**.claude/templates/bdd-scenario.feature`**) pero no da instrucciones precisas sobre cómo usarlo. Ver discrepancias.

**Convenciones aplicables**

- La ruta canónica del feature file (definida en `artifacts.md`) es `tests/features/{US_ID}-{nombre}.feature`.
- El agente debe guardar en esa ruta y presentar el contenido al usuario antes de avanzar.
- El punto de aprobación es imperativo: el agente no puede avanzar a Fase 2 sin respuesta explícita `[aprobado]`.

**Artefactos**

| Artefacto | Operación | Ruta |
|---|---|---|
| `{US_ID}-{nombre}.feature` | **Genera** | `tests/features/{US_ID}-{nombre}.feature` |
| `{US_ID}-context.md` | **Lee** | `docs/plans/{US_ID}-context.md` |

**Salidas**

| Salida | Tipo | Descripción |
|---|---|---|
| `tests/features/{US_ID}-{nombre}.feature` | Artefacto físico | Escenarios Gherkin en español, con tag `@US-{ID}` |
| Aprobación del usuario | En conversación | Respuesta `[aprobado]` antes de avanzar |

**Dependencias**

| Dirección | Fase | Qué provee |
|---|---|---|
| ← anterior | Fase 0 | `context.md` con criterios de la HU y decisión BDD |
| → siguiente | Fase 2 | (ninguna dependencia directa) |
| → siguiente | Fase 6 | Feature file para implementar steps y validar |

**Discrepancias detectadas (post v1.2)**

| ID | Descripción | Severidad |
|---|---|---|
| D1-1 | La fase menciona `Template: .claude/templates/bdd-scenario.feature` pero no indica cómo usarlo: ¿leerlo como referencia, copiarlo, completar variables? `config.json` y los perfiles referencian templates distintos pero tampoco hay instrucción de uso. | Media |
| D1-2 | `config.json` → `bdd_config.language: "es"` es correcto, pero los perfiles `pyqt-mvc.json` y `fastapi-rest.json` también definen `language: "es"` redundantemente. No hay mecanismo documentado de merge base+perfil para `bdd_config`. | Baja |
| D1-3 | El bloque de presentación al usuario menciona `tests/features/{US_ID}-{nombre}.feature` (correcto), pero no dice explícitamente qué nombre de archivo usar para `{nombre}` (slug del título de la HU, nombre técnico, etc.). | Media |

---

### Fase 2 — Generación del Plan de Implementación

**Descripción conceptual**

La Fase 2 traduce la HU aprobada en un plan de implementación estructurado: una lista de checkboxes de archivos a crear/modificar, organizados por capa arquitectónica según el patrón del perfil activo. El plan es la hoja de ruta que la Fase 3 ejecutará tarea a tarea.

La fase es agnóstica al stack en su estructura: lee el patrón del `config.json` y adapta el desglose de componentes según si es MVC, Layered (FastAPI), Layered (Flask), BFF (Webapp) o Generic. Los ejemplos embebidos en el archivo de fase sirven como referencia concreta para cada stack.

Un punto clave es que el plan **no incluye tests** (son responsabilidad de Fases 4-6) ni quality gates (Fase 7). Esto fue una corrección explícita de v1.1 (OBS-4), pero los ejemplos aún contienen referencias a esas secciones — ver discrepancias.

**Entradas**

| Entrada | Tipo | Requerida | Fuente |
|---|---|---|---|
| `docs/plans/{US_ID}-context.md` | Artefacto | ✅ Sí | Fase 0 |
| Patrón arquitectónico | `config.json` → `variables.architecture_pattern` | ✅ Sí | Perfil activo |
| Criterios de aceptación (para identificar componentes) | Leídos de la fuente HU | ✅ Sí | Fase 0 |
| Dependencias externas del proyecto | Análisis del código existente | ❌ Opcional | Fase 0 / exploración |

**Templates requeridos**

| Template | Ruta en config.json |
|---|---|
| Plan de implementación | `templates/planning/implementation-plan.md` |

> El template canónico está embebido en el archivo de fase (sección `📖 Template de Output`). El archivo `templates/planning/implementation-plan.md` existe como referencia externa pero la fase no lo invoca explícitamente.

**Convenciones aplicables**

- El plan no debe incluir secciones de tests, validación ni quality gates.
- Las tareas siguen orden bottom-up: capas inferiores primero (modelo/schema antes que controlador/router).
- El archivo debe existir en disco antes de presentarlo al usuario (verificación imperativa, Paso 6).

**Artefactos**

| Artefacto | Operación | Ruta |
|---|---|---|
| `{US_ID}-plan.md` | **Genera** | `docs/plans/{US_ID}-plan.md` |
| `{US_ID}-context.md` | **Lee** | `docs/plans/{US_ID}-context.md` |
| `config.json` | **Lee** (patrón arquitectónico) | `.claude/skills/implement-us/config.json` |

**Salidas**

| Salida | Tipo | Descripción |
|---|---|---|
| `docs/plans/{US_ID}-plan.md` | Artefacto físico | Checklist de componentes a implementar por capa |
| Aprobación del usuario | En conversación | El usuario puede solicitar ajustes antes de aprobar |

**Dependencias**

| Dirección | Fase | Qué provee |
|---|---|---|
| ← anterior | Fase 0 | `context.md` con patrón y umbrales |
| ← anterior | Fase 1 | (ninguna: plan es independiente de los escenarios BDD) |
| → siguiente | Fase 3 | Plan de tareas a ejecutar |
| → siguiente | Fase 9 | Lista de tareas completadas para el reporte |

**Discrepancias detectadas (post v1.2)**

| ID | Descripción | Severidad |
|---|---|---|
| D2-1 | Los ejemplos de output (PyQt, FastAPI, Flask REST, Flask Webapp, Generic) incluyen implícitamente secciones de integración que a veces mencionan "Registrar en Factory/Coordinator" (específico de PyQt). El template genérico no cubre estos casos para otros stacks. | Baja |
| D2-2 | El `📖 Template de Output` no especifica la ruta del archivo a guardar (`docs/plans/{US_ID}-plan.md`). Esa ruta solo aparece en el Paso 6 (verificación). Un agente podría guardar en otra ruta. | Media |
| D2-3 | `config.json` tiene `"output_template": "templates/planning/implementation-plan.md"` para la Fase 2, pero la fase no menciona leer ese template. Si el template difiere del embebido en el archivo de fase, hay ambigüedad sobre cuál es canónico. | Media |

---

### Fase 3 — Implementación Guiada por Tareas

**Descripción conceptual**

La Fase 3 es la de mayor duración del skill y la única que produce código de producción. El agente ejecuta las tareas del plan de Fase 2 de forma secuencial, una por una, usando el tool `Write` (o `Edit` para archivos existentes) para crear los archivos.

Para cada tarea el agente abre un ciclo: presenta el código propuesto al usuario con opciones `[sí] / [no] / [editar]`. Si el usuario aprueba, avanza; si edita, incorpora las instrucciones verbales (o el código pegado) hasta obtener aprobación; si rechaza, omite la tarea con justificación.

Al finalizar todas las tareas, el agente ejecuta una revisión de código obsoleto: busca en el proyecto archivos que ya no son necesarios como consecuencia de los nuevos componentes implementados (OBS-2).

**Entradas**

| Entrada | Tipo | Requerida | Fuente |
|---|---|---|---|
| `docs/plans/{US_ID}-plan.md` | Artefacto | ✅ Sí | Fase 2 |
| `docs/plans/{US_ID}-context.md` | Artefacto | ✅ Sí | Fase 0 |
| Perfil activo (rutas, clases base, patrones) | `config.json` + perfil | ✅ Sí | Instalación |
| `customizations/{perfil}.json` → `component_structure` | Perfil | ✅ Sí | Instalación |

**Templates requeridos**

Ninguno externo. El agente genera el código directamente según el perfil activo. Los perfiles (`customizations/*.json`) incluyen en `code_templates` ejemplos de código por stack (PyQt: `modelo.py`, `vista.py`, `controlador.py`; FastAPI: `router.py`, `service.py`, `repository.py`, etc.).

**Convenciones aplicables**

- Tracking de tarea (`start-task` / `end-task`) por cada ítem del plan.
- Tracking de fase inicia **antes** de leer el plan.
- El ciclo `sí/no/editar` es imperativo; no se avanza sin aprobación.
- El agente usa el tool `Write` directamente, sin pseudocódigo intermedio.

**Artefactos**

| Artefacto | Operación | Ruta |
|---|---|---|
| `{US_ID}-plan.md` | **Lee y actualiza** (marca ✅ cada tarea) | `docs/plans/{US_ID}-plan.md` |
| Archivos de código | **Genera** (según plan) | `{COMPONENT_PATH}/*` |
| `{US_ID}-context.md` | **Lee** | `docs/plans/{US_ID}-context.md` |

**Salidas**

| Salida | Tipo | Descripción |
|---|---|---|
| Archivos de código de producción | Artefactos físicos | Según estructura del perfil activo |
| Plan actualizado con checkboxes | `docs/plans/{US_ID}-plan.md` | Cada tarea marcada ✅ al completarse |
| Revisión de código obsoleto | En conversación | Lista de archivos candidatos a eliminar |

**Dependencias**

| Dirección | Fase | Qué provee |
|---|---|---|
| ← anterior | Fase 2 | Plan de implementación aprobado |
| → siguiente | Fase 4 | Código de producción para testear |
| → siguiente | Fase 5 | Código de producción para tests de integración |
| → siguiente | Fase 7 | Código a analizar con pylint/radon |

**Discrepancias detectadas (post v1.2)**

| ID | Descripción | Severidad |
|---|---|---|
| D3-1 | `config.json` no registra que el flag `--skip-bdd` omite Fase 1 y Fase 6. El archivo de fase 3 no verifica ni menciona ese flag. Si se ejecuta con `--skip-bdd`, el agente puede intentar leer un feature file que no existe en Fase 6. | Media |
| D3-2 | Los perfiles `customizations/*.json` → `component_structure` definen rutas detalladas de archivos a crear, pero la fase 3 no incluye instrucción explícita de leerlos. El agente puede no consultar el perfil y usar valores por defecto erróneos. | Media |

---

### Fase 4 — Tests Unitarios

**Descripción conceptual**

La Fase 4 crea los tests unitarios para cada componente implementado en la Fase 3. La estrategia es probar cada unidad (clase, función, método) de forma aislada, usando mocks para dependencias externas.

El scope de la fase se limita a `tests/unit/`. El agente genera tests siguiendo los patrones del framework de testing del perfil activo (pytest + pytest-qt para PyQt, pytest + httpx para FastAPI, pytest para Flask y Generic). Al finalizar, ejecuta `pytest tests/unit/ -v` para confirmar que todos los tests pasan.

La cobertura objetivo se lee del perfil activo (`quality_gates.coverage.min_percent` en `config.json`) y varía entre stacks: 90% para PyQt MVC y Flask Webapp, 95% para FastAPI REST, Flask REST y Generic Python.

**Entradas**

| Entrada | Tipo | Requerida | Fuente |
|---|---|---|---|
| Archivos de código de producción | Artefactos | ✅ Sí | Fase 3 |
| `docs/plans/{US_ID}-context.md` | Artefacto | ✅ Sí | Fase 0 |
| Framework de testing del perfil | `config.json` → `test_framework_config` | ✅ Sí | Perfil activo |
| Umbral de cobertura | `config.json` → `quality_gates.coverage.min_percent` | ✅ Sí | Perfil activo |

**Templates requeridos**

| Template | Ruta en config.json |
|---|---|
| Test unitario genérico | `templates/testing/test-unit.py` |

> Los perfiles definen `template_variables.TEST_FILE_PATTERN` con el patrón de nombres de archivos de test específicos por stack.

**Convenciones aplicables**

- Tests en `tests/unit/` (no en `tests/` raíz).
- Ejecución: `pytest tests/unit/ -v`.
- Los frameworks de testing son listas de dependencias, no bloques bash ejecutables.

**Artefactos**

| Artefacto | Operación | Ruta |
|---|---|---|
| `test_{component}_*.py` | **Genera** | `tests/unit/` (o `tests/` según perfil) |
| `tests/conftest.py` | **Crea/actualiza** | `tests/conftest.py` |
| Código de producción | **Lee** | `{COMPONENT_PATH}/` |

**Salidas**

| Salida | Tipo | Descripción |
|---|---|---|
| Archivos de test unitario | Artefactos físicos | Tests por componente según perfil |
| Resultado de `pytest tests/unit/ -v` | En conversación | Todos los tests deben pasar |

**Dependencias**

| Dirección | Fase | Qué provee |
|---|---|---|
| ← anterior | Fase 3 | Código de producción |
| → siguiente | Fase 5 | Suite de tests unitarios pasando |
| → siguiente | Fase 7 | Tests para medir coverage |

**Discrepancias detectadas (post v1.2)**

| ID | Descripción | Severidad |
|---|---|---|
| D4-1 | Las rutas de archivos de test en los perfiles son inconsistentes entre sí: `pyqt-mvc.json` usa `tests/test_{component}_modelo.py` (raíz de tests), `fastapi-rest.json` usa `tests/api/test_{feature_name}_router.py` (subdirectorio). La fase 4 no especifica qué ruta usar; el agente debe inferirlo del perfil. | Media |
| D4-2 | El `config.json` base tiene `"test_path": "tests/"` (sin subdirectorio unit/), pero la fase ejecuta `pytest tests/unit/ -v`. Discrepancia entre config y fase. | Media |

---

### Fase 5 — Tests de Integración

**Descripción conceptual**

La Fase 5 crea tests que validan la interacción entre componentes en flujos completos. A diferencia de los tests unitarios, los de integración verifican que la composición de componentes funciona correctamente bajo condiciones realistas.

La estrategia de mocking es deliberada: se mockean solo servicios externos al sistema (APIs externas, bases de datos en producción, dispositivos físicos); los componentes internos se prueban con sus implementaciones reales o con test-doubles documentados. Las excepciones a esta regla deben anotarse explícitamente.

El scope de la fase es `tests/integration/`. Al finalizar, se ejecuta `pytest tests/integration/ -v`. La precondición real es que los tests unitarios de Fase 4 pasen.

**Entradas**

| Entrada | Tipo | Requerida | Fuente |
|---|---|---|---|
| Archivos de código de producción | Artefactos | ✅ Sí | Fase 3 |
| Suite de tests unitarios pasando | Resultado | ✅ Sí | Fase 4 |
| `docs/plans/{US_ID}-context.md` | Artefacto | ✅ Sí | Fase 0 |
| Framework de testing del perfil | `config.json` → `test_framework_config` | ✅ Sí | Perfil activo |

**Templates requeridos**

| Template | Ruta en config.json |
|---|---|
| Test de integración genérico | `templates/testing/test-integration.py` |

> Los perfiles definen `snippets.test_integration_class` con ejemplos concretos de clases de test de integración.

**Convenciones aplicables**

- Tests en `tests/integration/`.
- Estrategia de mocking: externo → mock, interno → real (con excepciones documentadas).
- El protocolo de recuperación usa el concepto de "ciclo" (ejecución → detección de no conformidad → corrección), no "intento".
- Ejecución: `pytest tests/integration/ -v`.

**Artefactos**

| Artefacto | Operación | Ruta |
|---|---|---|
| `test_{component}_integration.py` | **Genera** | `tests/integration/` |
| `tests/conftest.py` | **Actualiza** (fixtures de integración) | `tests/conftest.py` |
| Código de producción | **Lee** | `{COMPONENT_PATH}/` |

**Salidas**

| Salida | Tipo | Descripción |
|---|---|---|
| Archivos de test de integración | Artefactos físicos | Tests de flujo completo por perfil |
| Resultado de `pytest tests/integration/ -v` | En conversación | Todos los tests deben pasar |

**Dependencias**

| Dirección | Fase | Qué provee |
|---|---|---|
| ← anterior | Fase 4 | Tests unitarios pasando (precondición real) |
| → siguiente | Fase 6 | Tests de integración pasando |
| → siguiente | Fase 7 | Tests para medir coverage |

**Discrepancias detectadas (post v1.2)**

| ID | Descripción | Severidad |
|---|---|---|
| D5-1 | La precondición ejecuta `pytest tests/unit/ -v --tb=short` (correcto), pero no verifica que existan archivos en `tests/integration/` al iniciar —no hay ruta de integración pre-existente que validar. Menor, pero la precondición implica que ya había tests de integración. | Baja |
| D5-2 | `config.json` → `test_framework_config` no tiene clave `integration_test_path` (solo `test_path: "tests/"`). La fase asume `tests/integration/` sin configuración explícita. | Baja |

---

### Fase 6 — Validación BDD

**Descripción conceptual**

La Fase 6 cierra el ciclo BDD iniciado en Fase 1: implementa los step definitions que ejecutan los escenarios Gherkin y valida que el sistema cumple con el comportamiento especificado. Si `--skip-bdd` fue activado, esta fase se omite.

Los step definitions se ubican en `tests/step_defs/` e importan los escenarios desde `tests/features/`. pytest-bdd descubre los escenarios a través de los archivos de steps (no ejecutando los `.feature` directamente). La ejecución se hace con `pytest tests/step_defs/ -v`.

El criterio de éxito es 100% de escenarios en verde. Si un escenario falla, el agente diagnostica el origen: bug en implementación (→ Fase 3), step mal implementado (corregir aquí), o escenario mal redactado (editar `.feature` con aprobación del usuario; volver a Fase 1 solo si implica cambio de lógica de HU).

**Entradas**

| Entrada | Tipo | Requerida | Fuente |
|---|---|---|---|
| `tests/features/{US_ID}-*.feature` | Artefacto | ✅ Sí | Fase 1 |
| Archivos de código de producción | Artefactos | ✅ Sí | Fase 3 |
| Tests unitarios e integración pasando | Resultado | ✅ Sí | Fases 4-5 |

**Templates requeridos**

Ninguno externo. Los step definitions se generan directamente según el perfil activo. Los perfiles definen `bdd_config.steps_template` (ej. `templates/bdd/pyqt-steps.py` para PyQt), pero no hay instrucción explícita de usarlos.

**Convenciones aplicables**

- Feature files en `tests/features/`, steps en `tests/step_defs/`.
- Ejecución: `pytest tests/step_defs/ -v` (no `pytest tests/features/`).
- La edición de `.feature` requiere aprobación explícita del usuario.
- El protocolo de recuperación usa "ciclos completos", no "intentos".

**Artefactos**

| Artefacto | Operación | Ruta |
|---|---|---|
| `tests/features/{US_ID}-*.feature` | **Lee** | `tests/features/` |
| `test_{feature}_steps.py` | **Genera** | `tests/step_defs/` |
| `tests/conftest.py` | **Actualiza** (fixtures BDD) | `tests/conftest.py` |

**Salidas**

| Salida | Tipo | Descripción |
|---|---|---|
| Archivos de step definitions | Artefactos físicos | Steps implementados para cada escenario |
| Resultado de `pytest tests/step_defs/ -v` | En conversación | 100% de escenarios pasando |

**Dependencias**

| Dirección | Fase | Qué provee |
|---|---|---|
| ← anterior | Fase 1 | Feature file con escenarios aprobados |
| ← anterior | Fases 4-5 | Tests pasando (implica implementación correcta) |
| → siguiente | Fase 7 | Evidencia de comportamiento validado |

**Discrepancias detectadas (post v1.2)**

| ID | Descripción | Severidad |
|---|---|---|
| D6-1 | `config.json` → `test_framework_config.steps_path` es `"tests/features/steps/"`, pero la convención establecida (y la fase 6 corregida) usa `"tests/step_defs/"`. Discrepancia directa entre config base y fase. | Alta |
| D6-2 | Los perfiles (`pyqt-mvc.json`, `fastapi-rest.json`) definen `bdd_config.steps_template` pero la fase no incluye instrucción de leerlo. | Baja |

---

### Fase 7 — Quality Gates

**Descripción conceptual**

La Fase 7 valida que el código de producción cumple con los estándares de calidad del proyecto usando métricas objetivas: Pylint (análisis estático), Complejidad Ciclomática (radon cc), Índice de Mantenibilidad (radon mi) y Cobertura de Tests (pytest-cov).

Los umbrales no son fijos: se leen del perfil activo en `config.json` (o del perfil de customización si está instalado). Los valores por defecto del config base son Pylint ≥ 8.0, CC ≤ 10, MI > 20, Coverage ≥ 95%, pero PyQt MVC los ajusta (CC ≤ 12, Coverage ≥ 90%) y FastAPI los eleva (Pylint ≥ 8.5, MI > 25).

El criterio de CC es por función (`max_per_function`), no promedio. El reporte consolidado `quality.json` registra métricas, umbrales y estado final (`APROBADO` / `RECHAZADO`).

**Entradas**

| Entrada | Tipo | Requerida | Fuente |
|---|---|---|---|
| Archivos de código de producción | Artefactos | ✅ Sí | Fase 3 |
| `pytest tests/unit/ tests/integration/ tests/step_defs/ -v` pasando | Resultado | ✅ Sí | Fases 4-5-6 |
| Umbrales del perfil activo | `config.json` → `quality_gates` | ✅ Sí | Perfil activo |
| `{COMPONENT_PATH}` del perfil | `config.json` → `variables.component_path` | ✅ Sí | Perfil activo |

**Templates requeridos**

Ninguno externo. El formato del `quality.json` está embebido en el archivo de fase.

**Convenciones aplicables**

- Tracking inicia antes de la precondición.
- Umbrales provienen siempre del perfil activo, nunca hardcodeados.
- CC se valida por función individual, no por promedio.

**Artefactos**

| Artefacto | Operación | Ruta |
|---|---|---|
| `{US_ID}-pylint.json` | **Genera** | `quality/reports/{US_ID}-pylint.json` |
| `{US_ID}-cc.json` | **Genera** | `quality/reports/{US_ID}-cc.json` |
| `{US_ID}-mi.json` | **Genera** | `quality/reports/{US_ID}-mi.json` |
| `{US_ID}-coverage.json` | **Genera** | `quality/reports/{US_ID}-coverage.json` |
| `{US_ID}-coverage-html/` | **Genera** | `quality/reports/{US_ID}-coverage-html/` |
| `{US_ID}-quality.json` | **Genera** | `quality/reports/{US_ID}-quality.json` |

**Salidas**

| Salida | Tipo | Descripción |
|---|---|---|
| `quality/reports/{US_ID}-quality.json` con estado `APROBADO` | Artefacto físico | Métricas consolidadas + umbrales + estado |
| Reportes individuales (pylint, cc, mi, coverage) | Artefactos físicos | Detalle por herramienta |

**Dependencias**

| Dirección | Fase | Qué provee |
|---|---|---|
| ← anterior | Fases 4-5-6 | Tests pasando (precondición ejecutable) |
| → siguiente | Fase 8 | `quality.json` para documentar en plan |
| → siguiente | Fase 9 | `quality.json` para incluir métricas en reporte final |

**Discrepancias detectadas (post v1.2)**

| ID | Descripción | Severidad |
|---|---|---|
| D7-1 | El texto de las secciones de métricas hardcodea los targets: "Target: ≥ 8.0/10" (Pylint), "Target: ≥ 95%" (Coverage), "Si no pasa (< 95%)" — solo el checklist y los "Comandos de Validación" finales leen del perfil. El cuerpo de la fase es inconsistente. | Media |
| D7-2 | El script Python embebido (`generar_reporte_quality` / `todas_metricas_pasan`) hardcodea umbrales (`8.0`, `10.0`, `20.0`, `95.0`). Si el agente lo usa, generará un quality.json con umbrales incorrectos para PyQt (90%) o FastAPI (8.5). | Alta |
| D7-3 | El template del `quality.json` (sección "Formato") tiene un campo `"umbrales"` con valores fijos. No hay instrucción de leerlos dinámicamente del perfil activo para ese campo. | Media |

---

### Fase 8 — Actualización de Documentación

**Descripción conceptual**

La Fase 8 sincroniza la documentación del proyecto con los cambios realizados durante la implementación. Tiene cuatro tareas principales: actualizar el plan de implementación con estado "COMPLETADO" y métricas de tiempo; buscar activamente archivos de arquitectura desactualizados (discovery explícito con grep/find); actualizar el CHANGELOG; y actualizar el README si la funcionalidad es visible al usuario.

El discovery de arquitectura (Paso 2) es una instrucción imperativa añadida en v1.2: el agente debe buscar archivos con diagramas Mermaid, PlantUML o C4 y evaluar si quedaron desactualizados por los cambios de esta US, sin esperar que el usuario lo indique.

**Entradas**

| Entrada | Tipo | Requerida | Fuente |
|---|---|---|---|
| `quality/reports/{US_ID}-quality.json` | Artefacto | ✅ Sí | Fase 7 |
| `docs/plans/{US_ID}-plan.md` | Artefacto | ✅ Sí | Fase 2 |
| Datos de tracking (tiempo real por fase) | CLI de tracking | ❌ Opcional | Sistema de tracking |
| Archivos de arquitectura del proyecto | Exploración | ❌ Opcional | Discovery en Paso 2 |

**Templates requeridos**

Ninguno externo. Los ejemplos de actualización de documentación están embebidos en el archivo de fase.

**Convenciones aplicables**

- El discovery de arquitectura es imperativo (🔴), no opcional.
- Si el CLI de tracking no está disponible, usar tiempo observado en la sesión o anotar "Tracking no disponible".
- Hay un único checklist de salida (6 ítems).

**Artefactos**

| Artefacto | Operación | Ruta |
|---|---|---|
| `{US_ID}-plan.md` | **Actualiza** (estado COMPLETADO, tiempos) | `docs/plans/{US_ID}-plan.md` |
| `{US_ID}-quality.json` | **Lee** | `quality/reports/{US_ID}-quality.json` |
| `CHANGELOG.md` | **Actualiza** | raíz del proyecto |
| `docs/architecture*.md` (si existe) | **Actualiza** (si aplica) | Según discovery |
| `README.md` (si aplica) | **Actualiza** | raíz del proyecto |

**Salidas**

| Salida | Tipo | Descripción |
|---|---|---|
| Plan actualizado con estado y tiempos | `docs/plans/{US_ID}-plan.md` | Sección de métricas de tiempo agregada |
| Entrada en CHANGELOG.md | `CHANGELOG.md` | Formato Keep a Changelog |
| Documentación de arquitectura actualizada | Varios | Solo si el discovery detectó archivos desactualizados |

**Dependencias**

| Dirección | Fase | Qué provee |
|---|---|---|
| ← anterior | Fase 7 | `quality.json` con métricas para documentar |
| → siguiente | Fase 9 | Plan actualizado para incluir en reporte |

**Discrepancias detectadas (post v1.2)**

| ID | Descripción | Severidad |
|---|---|---|
| D8-1 | `config.json` → `phases.8.approval_required: false`, pero `skill.md` dice "Aprobación: Requerida (usuario revisa docs)" para Fase 8. Contradicción entre el orquestador y la configuración. | Media |
| D8-2 | La sección "Automatización (opcional)" tiene un subsección `#### API Documentation (FastAPI, Django REST)` con comando `python manage.py generate_swagger` (Django). Referencia residual OBS-5 en contexto de automatización. | Baja |

---

### Fase 9 — Reporte Final

**Descripción conceptual**

La Fase 9 cierra el ciclo del skill generando un reporte completo de la implementación: resumen ejecutivo con métricas de tiempo y varianza, componentes creados, métricas de calidad reales (leídas desde `quality.json`), tests implementados, archivos creados y criterios de aceptación verificados.

El reporte no reconstruye métricas desde memoria: lee `quality/reports/{US_ID}-quality.json` para los valores reales. Los umbrales en el reporte también provienen de ese archivo (campo `umbrales`), no están hardcodeados.

La fase también cierra el tracking completo de la US (`end-tracking`), que guarda el histórico y genera el reporte de tiempo final. Este es el único punto donde aparece ese subcomando.

**Entradas**

| Entrada | Tipo | Requerida | Fuente |
|---|---|---|---|
| `docs/plans/{US_ID}-plan.md` | Artefacto | ✅ Sí | Fases 2-3-8 |
| `quality/reports/{US_ID}-quality.json` | Artefacto | ✅ Sí | Fase 7 |
| `docs/plans/{US_ID}-context.md` | Artefacto | ❌ Opcional | Fase 0 |
| Templates por stack | Ver templates | ❌ Opcional | `templates/reporting/` |

**Templates requeridos**

| Template | Ruta en config.json |
|---|---|
| Reporte de implementación | `templates/reporting/implementation-report.md` |

> El template por stack (PyQt, FastAPI, Generic) está embebido en el archivo de fase. Los templates externos son alternativos.

**Convenciones aplicables**

- Las métricas deben leerse desde `quality.json`, no reconstruirse.
- El reporte debe presentarse al usuario (contenido completo + ruta del archivo).
- `end-tracking` cierra el tracking completo, no solo la fase.
- El checklist de salida requiere que el archivo exista en disco.

**Artefactos**

| Artefacto | Operación | Ruta |
|---|---|---|
| `{US_ID}-report.md` | **Genera** | `docs/reports/{US_ID}-report.md` |
| `{US_ID}-quality.json` | **Lee** | `quality/reports/{US_ID}-quality.json` |
| `{US_ID}-plan.md` | **Lee** | `docs/plans/{US_ID}-plan.md` |

**Salidas**

| Salida | Tipo | Descripción |
|---|---|---|
| `docs/reports/{US_ID}-report.md` | Artefacto físico | Reporte completo de implementación |
| Reporte presentado en conversación | En conversación | Contenido + ruta del archivo |
| Tracking cerrado | Sistema | `track.py end-phase 9` + `track.py end-tracking` |

**Dependencias**

| Dirección | Fase | Qué provee |
|---|---|---|
| ← anterior | Fase 7 | `quality.json` con métricas reales |
| ← anterior | Fase 8 | Plan actualizado con tareas completadas |
| → cierre | — | El skill ha completado todas sus fases |

**Discrepancias detectadas (post v1.2)**

| ID | Descripción | Severidad |
|---|---|---|
| D9-1 | El subcomando `end-tracking` (`track.py end-tracking`) aparece solo en esta fase. No está definido en ningún otro archivo del skill ni documentado en `skill.md`. Si el CLI no lo implementa, la fase falla en el último paso. | Alta |
| D9-2 | Los templates de reporte por stack tienen `{PYLINT_MIN}`, `{CC_MAX}`, etc. como placeholders (correcto), pero el agente debe leer esos valores desde `quality.json → umbrales` antes de rellenar el template. La fase no da instrucción explícita de ese mapeo. | Media |

---

## Resumen de Discrepancias Detectadas (Post v1.2)

### Por archivo fuente

| Archivo | Discrepancias |
|---|---|
| `config.json` | D0-1, D0-3, D4-2, D5-2, D6-1 |
| `phases/phase-0-validation.md` | D0-2 |
| `phases/phase-1-bdd.md` | D1-1, D1-2, D1-3 |
| `phases/phase-2-planning.md` | D2-1, D2-2, D2-3 |
| `phases/phase-3-implementation.md` | D3-1, D3-2 |
| `phases/phase-4-unit-tests.md` | D4-1, D4-2 |
| `phases/phase-5-integration-tests.md` | D5-1, D5-2 |
| `phases/phase-6-bdd-validation.md` | D6-1, D6-2 |
| `phases/phase-7-quality-gates.md` | D7-1, D7-2, D7-3 |
| `phases/phase-8-documentation.md` | D8-1, D8-2 |
| `phases/phase-9-final-report.md` | D9-1, D9-2 |

### Por severidad

| Severidad | IDs | Total |
|---|---|---|
| Alta | D6-1, D7-2, D9-1 | 3 |
| Media | D0-2, D1-1, D1-3, D2-2, D2-3, D3-1, D3-2, D4-1, D4-2, D7-1, D7-3, D8-1, D9-2 | 13 |
| Baja | D0-1, D0-3, D1-2, D2-1, D5-1, D5-2, D6-2, D8-2 | 8 |
| **Total** | | **24** |

### Alta prioridad de corrección

| ID | Descripción breve | Archivo |
|---|---|---|
| D6-1 | `config.json` → `steps_path: "tests/features/steps/"` vs convención `tests/step_defs/` | `config.json` |
| D7-2 | Script Python de quality gates con umbrales hardcodeados | `phase-7-quality-gates.md` |
| D9-1 | Subcomando `end-tracking` no documentado en ningún archivo del skill | `phase-9-final-report.md` |

---

**Generado:** 2026-02-27
**Basado en:** Análisis post v1.2 — correcciones fases 0-9 + archivos genéricos aplicadas
