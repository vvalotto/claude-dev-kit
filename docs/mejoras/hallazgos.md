# Hallazgos — Análisis Skill por Skill

Documento acumulativo de ajustes y ambigüedades detectados durante el análisis sistemático del skill `implement-us`.

**Metodología:** Se analiza cada archivo de fase en orden (0→9), luego los archivos genéricos (`skill.md`, `artifacts.md`, `conventions.md`).
**Cruce:** Cada hallazgo se referencia contra las observaciones existentes en `mejoras-agentes-kit.md` (OBS-1 a OBS-6) o se marca como nueva observación.

---

## Severidades

| Nivel | Criterio |
|-------|---------|
| Alta | Puede causar fallo o comportamiento incorrecto del agente |
| Media | Genera inconsistencia o resultado subóptimo |
| Baja | Mejora de claridad o mantenibilidad |

---

## Fase 0 — `phase-0-validation.md`

### Ajustes

| ID | Descripción | Severidad | OBS relacionada |
|----|-------------|-----------|-----------------|
| F0-A1 | OBS-6 aplicada solo como fallback: el archivo busca la HU primero y pregunta al usuario *si no la encuentra*. La propuesta de OBS-6 es preguntar proactivamente al inicio, antes de buscar. El bloque de preguntas obligatorias ("Establecimiento de fuentes") no está implementado. | Alta | OBS-6 pendiente |
| F0-A2 | Comando de verificación de `pytest-bdd` incorrecto: `python -m pytest_bdd --version` falla porque el paquete no tiene módulo `__main__`. Debería ser `python -c "import pytest_bdd; print(pytest_bdd.__version__)"` | Media | Nueva |
| F0-A3 | CLI de tracking inconsistente con OBS-3: el archivo usa `python .claude/tracking/time_tracker.py start --us {US_ID} --phase 0`, pero OBS-3 propone `python .claude/tracking/track.py start-phase 0 "Validación de Contexto"`. Son interfaces distintas; no queda claro cuál es la definitiva ni si el CLI existe realmente. | Media | OBS-3 |
| F0-A4 | Rutas de artefactos en el template de `context.md` hardcodeadas (ej. `docs/plans/{US_ID}-context.md`, `docs/bdd/{US_ID}.feature`). Deberían provenir de `artifacts.md`, que existe exactamente para centralizar esas rutas. Si cambia la convención en `artifacts.md`, este template queda desincronizado. | Baja | Nueva |

### Ambigüedades

| ID | Descripción | Severidad |
|----|-------------|-----------|
| F0-AMB1 | Sección 3: *"Si faltan configuraciones, ofrecé crearlas o advertí al usuario antes de continuar."* No especifica qué crea, con qué valores por defecto, ni si requiere aprobación del usuario antes de escribir los archivos. | Alta |
| F0-AMB2 | La fase mezcla bloques `🔴 Acción Requerida` con secciones numeradas (1, 2, 3) sin indicar explícitamente el orden de ejecución. Un agente podría procesar todos los 🔴 primero y luego los numerados. | Media |
| F0-AMB3 | Sección 2: *"Leé del archivo de configuración `config.json` los patrones a validar."* No especifica qué clave del JSON leer, ni qué significa "validar" un patrón arquitectónico (¿buscar archivos? ¿buscar clases en el código?). | Alta |
| F0-AMB4 | Clasificación de HU: *"Esperá confirmación antes de continuar."* No define qué cuenta como confirmación — ¿respuesta explícita "sí"? ¿cualquier mensaje? ¿silencio implica aprobación? | Baja |

---

## Fase 1 — `phase-1-bdd.md`

### Ajustes

| ID | Descripción | Severidad | OBS relacionada |
|----|-------------|-----------|-----------------|
| F1-A1 | OBS-5 Django presente: línea de ruta `**Django:** {app}/tests/features/US-XXX-{nombre}.feature` y Ejemplo 3 completo (formulario de registro Django). | Media | OBS-5 pendiente |
| F1-A2 | Inconsistencia de ruta del feature file: las instrucciones de generación usan `{PRODUCT}/tests/features/US-XXX-{nombre}.feature` (o variantes por stack), pero el checklist de salida verifica `docs/bdd/{US_ID}.feature`. Son ubicaciones distintas. | Alta | Nueva |
| F1-A3 | Link de "Siguiente fase" desactualizado: dice `_(pendiente)_` cuando la fase ya existe. | Baja | Nueva |
| F1-A4 | "Punto de Aprobación" sin instrucción concreta: describe que el usuario debe revisar, pero no hay un bloque `🔴 Acción Requerida` ni indicación de qué hace el agente para esperar. | Media | Nueva |

### Ambigüedades

| ID | Descripción | Severidad |
|----|-------------|-----------|
| F1-AMB1 | `**Template:** .claude/templates/bdd-scenario.feature` se menciona pero no se explica cómo usarlo: ¿el agente lo lee como referencia? ¿lo copia? ¿qué variables tiene? | Media |
| F1-AMB2 | *"Cada criterio se convierte en al menos un escenario"* — no da guía sobre cuántos escenarios generar (¿solo happy path? ¿también errores? ¿cuántos casos edge?). | Media |
| F1-AMB3 | *"Extraídos en Fase 0"* — asume que los criterios están disponibles pero no especifica en qué campo/sección de `context.md` buscarlos. | Alta |
| F1-AMB4 | Nombre del archivo feature inconsistente en el mismo archivo: la sección de generación usa `US-XXX-{nombre}.feature` pero el checklist dice `{US_ID}.feature`. | Alta |

---

## Fase 2 — `phase-2-planning.md`

### Ajustes

| ID | Descripción | Severidad | OBS relacionada |
|----|-------------|-----------|-----------------|
| F2-A1 | OBS-5 Django presente: en "Ubicación del Archivo Generado" aparece `**Django:** docs/requirements/US-XXX-plan.md`. | Media | OBS-5 pendiente |
| F2-A2 | OBS-4 incompleta: los 5 ejemplos de output (PyQt, FastAPI, Flask REST, Flask Webapp, Generic) siguen incluyendo secciones "Tests" y "Validación" con estimaciones de tiempo. El Template de Output también las incluye. OBS-4 decía "Corrección aplicada" pero la corrección parece no haber alcanzado los ejemplos ni el template. | Alta | OBS-4 reabierta |
| F2-A3 | Link de "Siguiente fase" desactualizado: dice `_(pendiente)_` cuando la fase ya existe. | Baja | Nueva |

### Ambigüedades

| ID | Descripción | Severidad |
|----|-------------|-----------|
| F2-AMB1 | El Template de Output (estructura canónica del plan) incluye `### 3. Tests` y `### 4. Validación`, lo cual contradice la intención de OBS-4. Si el agente sigue el template, generará las secciones que se querían eliminar. | Alta |
| F2-AMB2 | Las estimaciones de tiempo en los ejemplos y en "Consideraciones Importantes" no aclaran si son para incluir en el archivo del plan (visible al usuario) o solo referencia interna del agente para estimar. | Media |
| F2-AMB3 | El snippet JSON de referencia para leer la configuración usa `{ARCHITECTURE_PATTERN}` como valor — es un placeholder ficticio, no una clave real del `config.json`. No especifica qué clave del JSON real leer. | Media |

---

## Fase 3 — `phase-3-implementation.md`

### Ajustes

| ID | Descripción | Severidad | OBS relacionada |
|----|-------------|-----------|-----------------|
| F3-A1 | OBS-5 Django presente: la sección "Ejemplos de Referencias por Stack" tiene subsección completa "Django/MVT" con referencias a Models, Views, Templates. | Media | OBS-5 pendiente |
| F3-A2 | OBS-2 no implementada: no existe paso de "Revisión de código obsoleto" al final de la fase. | Alta | OBS-2 pendiente |
| F3-A3 | Pseudocódigo Python en paso 6: `if user_approves: write_file(path=..., content=...)` mezcla pseudocódigo Python con instrucciones al agente. El agente debería usar el tool `Write` directamente, sin pseudocódigo intermedio. | Baja | Nueva |
| F3-A4 | CLI de tracking de tarea con subcomando diferente al de fase: la fase usa `start --phase N`, pero el tracking de tarea usa `start-task --task-id ... --task-name "..."`. No queda claro si ambos subcomandos existen en el mismo CLI. | Media | OBS-3 |

### Ambigüedades

| ID | Descripción | Severidad |
|----|-------------|-----------|
| F3-AMB1 | Opción `edit` en `yes/no/edit`: no se explica el flujo — ¿el agente espera que el usuario pegue el código editado? ¿Propone cambios? ¿Espera instrucciones verbales del usuario? | Alta |
| F3-AMB2 | *"Ejecutar tests básicos (si aplica)"* — no define cuándo aplica y cuándo no. ¿Solo si ya existen tests? ¿Solo para ciertos tipos de componente? | Media |
| F3-AMB3 | El orden de las acciones requeridas al inicio pone "Establecer contexto" (leer el plan) antes de "Iniciar tracking". El tracking debería iniciarse antes de cualquier trabajo, no después de leer el plan. | Media |
| F3-AMB4 | Los "Tipos de tarea" para el tracker (`modelo`, `vista`, `api`, etc.) no tienen una relación explícita con las tareas generadas en el plan de Fase 2. No queda claro cómo el agente mapea una tarea del plan a un "tipo de tarea" del tracker. | Media |

---

## Fase 4 — `phase-4-unit-tests.md`

### Ajustes

| ID | Descripción | Severidad | OBS relacionada |
|----|-------------|-----------|-----------------|
| F4-A1 | OBS-5 Django presente: comandos de ejecución con `--ds=config.settings.test` y `--reuse-db`, más un `conftest.py` completo con fixtures Django. | Media | OBS-5 pendiente |
| F4-A2 | Coverage hardcodeado al 95%: el objetivo `> 95%` aparece en la fase sin leer el perfil activo. Flask Webapp y PyQt MVC tienen umbrales distintos (90%) según Fase 7 y `config.json`. Genera contradicción con el sistema de perfiles. | Media | Nueva |

### Ambigüedades

| ID | Descripción | Severidad |
|----|-------------|-----------|
| F4-AMB1 | La sección "Configuración de Testing por Stack" usa bloques de código bash pero su contenido son descripciones de texto (fixtures, dependencias en formato de lista). El formato mezcla lo ejecutable con lo descriptivo. | Baja |
| F4-AMB2 | El checklist de salida dice `pytest tests/ -v` (toda la suite), pero en Fase 4 solo deberían existir tests unitarios. Ejecutar la suite completa es correcto pero puede generar confusión sobre el scope de la fase. | Baja |

---

## Fase 5 — `phase-5-integration-tests.md`

### Ajustes

| ID | Descripción | Severidad | OBS relacionada |
|----|-------------|-----------|-----------------|
| F5-A1 | OBS-5 Django presente: estrategias de integración para Django/MVT (sección completa con herramientas, ejemplos extensos con `@pytest.mark.django_db`, vista de lista con filtros y paginación, signals). | Media | OBS-5 pendiente |
| F5-A2 | Precondición débil: `ls tests/` verifica que el directorio existe, no que hay tests creados en Fase 4. La precondición no cumple su función de gate real. | Media | Nueva |
| F5-A3 | Checklist de salida ejecuta `pytest tests/ -v` (toda la suite) en lugar de `pytest tests/integration/ -v`. Es impreciso respecto al scope de validación de la fase. | Baja | Nueva |

### Ambigüedades

| ID | Descripción | Severidad |
|----|-------------|-----------|
| F5-AMB1 | Estrategia de mocking contradictoria: la guía dice "NO mockear componentes internos del sistema", pero los ejemplos de PyQt y Django mockean servicios internos (ej. `mocker.patch('app.services.user_service.save_user')`). | Alta |
| F5-AMB2 | El protocolo de recuperación establece "después de 2 intentos" como límite, pero no define qué cuenta como un "intento" ni qué hacer exactamente si se supera el límite (además de "informar al usuario"). | Baja |

---

## Fase 6 — `phase-6-bdd-validation.md`

### Ajustes

| ID | Descripción | Severidad | OBS relacionada |
|----|-------------|-----------|-----------------|
| F6-A1 | OBS-5 Django presente: sección completa con steps para Django Client (`@pytest.mark.django_db`, `client.force_login`, etc.). | Media | OBS-5 pendiente |
| F6-A2 | Inconsistencia de rutas de features en la misma fase: la estructura de archivos muestra `tests/features/`, los ejemplos usan `../features/{US_ID}-*.feature`, pero el checklist y el protocolo de recuperación ejecutan `pytest tests/bdd/ -v`. Tres rutas distintas para el mismo artefacto. | Alta | Nueva |
| F6-A3 | El feature file generado en Fase 1 se verifica en `docs/bdd/{US_ID}.feature` (precondición), pero los steps apuntan a `../features/` relativo desde `tests/step_defs/`. No hay instrucción de dónde debe residir el `.feature` para que pytest-bdd pueda ejecutarlo. | Alta | Nueva |

### Ambigüedades

| ID | Descripción | Severidad |
|----|-------------|-----------|
| F6-AMB1 | El protocolo de recuperación dice "volvé a Fase 1 a revisar y ajustar el escenario con el usuario" si hay un escenario mal redactado — pero no aclara qué pasa con el feature file si estaba en `docs/bdd/` y necesita moverse a `tests/features/` para ejecutarse. | Media |

---

## Fase 7 — `phase-7-quality-gates.md`

### Ajustes

| ID | Descripción | Severidad | OBS relacionada |
|----|-------------|-----------|-----------------|
| F7-A1 | Precondición no ejecutable: `ls tests pasando (Fase 4, 5, 6)` no es un comando bash válido. Es texto descriptivo disfrazado de comando. | Alta | Nueva |
| F7-A2 | "Herramientas Alternativas por Lenguaje": incluye secciones para TypeScript, Java y C#/.NET en un skill exclusivamente Python. Genera ruido y puede confundir al agente sobre el scope del skill. | Baja | Nueva |
| F7-A3 | Umbrales hardcoded en el "Resumen de la Fase": dice `Coverage ≥ 95%` y `CC ≤ 10`, pero Flask Webapp tiene 90% y PyQt MVC tiene CC 12. El resumen contradice la tabla de perfiles que está más abajo en el mismo archivo. | Media | Nueva |

### Ambigüedades

| ID | Descripción | Severidad |
|----|-------------|-----------|
| F7-AMB1 | El texto mezcla "CC promedio ≤ 10" con "CC máx por función": la tabla comparativa de perfiles habla de "CC máx" pero los comandos de radon calculan el promedio. No queda claro qué valor comparar con el umbral. | Alta |
| F7-AMB2 | Los comandos de validación por perfil hardcodean rutas (`app/presentacion`, `app/api`, `app/`, `src/`) en lugar de usar `{COMPONENT_PATH}`. En un proyecto real con estructura diferente, estos comandos fallarían. | Media |

---

## Fase 8 — `phase-8-documentation.md`

### Ajustes

| ID | Descripción | Severidad | OBS relacionada |
|----|-------------|-----------|-----------------|
| F8-A1 | OBS-5 Django presente: sección de arquitectura Django/MVT con estructura de archivos (models, views, templates, forms, urls). | Media | OBS-5 pendiente |
| F8-A2 | OBS-1 parcialmente resuelta: la fase menciona "Actualizar Arquitectura (si aplica)" y el checklist incluye "Diagramas actualizados (si cambió arquitectura)", pero falta el paso de *discovery explícito* propuesto en OBS-1: buscar activamente archivos de arquitectura con diagramas Mermaid/C4/UML y evaluar si reflejan los cambios. | Alta | OBS-1 pendiente |
| F8-A3 | La tabla de "Métricas de Tiempo" del plan (paso 1) requiere datos de tracking por fase, pero si el CLI de tracking no existe (OBS-3), esos datos no estarán disponibles. La fase asume que el tracker funcionó cuando en la práctica no funciona. | Media | OBS-3 |

### Ambigüedades

| ID | Descripción | Severidad |
|----|-------------|-----------|
| F8-AMB1 | Hay dos checklists: "Checklist de Documentación" (9 ítems detallados) y "Checklist de Salida" (3 ítems genéricos). No queda claro si el agente debe completar ambos o solo el de salida. El de salida es mucho más permisivo que el de documentación. | Alta |
| F8-AMB2 | *"Actualizar Arquitectura (si aplica)"* — la lista de cuándo actualizar (4 criterios) es orientativa pero no imperativa. El agente puede ignorarla fácilmente sin que el checklist de salida lo detecte. | Media |

---

## Fase 9 — `phase-9-final-report.md`

### Ajustes

| ID | Descripción | Severidad | OBS relacionada |
|----|-------------|-----------|-----------------|
| F9-A1 | OBS-5 Django presente: template Django/MVT con modelo, vistas, templates, forms, URLs y tabla de migraciones. | Media | OBS-5 pendiente |
| F9-A2 | Umbrales de calidad hardcodeados en los templates del reporte (≥ 8.0, ≤ 10, > 20, ≥ 95%) en lugar de leer del perfil activo como hace correctamente Fase 7. Un Flask Webapp con 92% de coverage aparecería como RECHAZADO en el reporte. | Media | Nueva |
| F9-A3 | Subcomando `end-tracking` introducido aquí por primera vez: `python .claude/tracking/time_tracker.py end-tracking --us {US_ID}`. No se menciona en ninguna fase anterior, ni en la sección de inicio de Fase 0. Si el CLI no tiene este subcomando, la fase falla en el último paso. | Media | OBS-3 |

### Ambigüedades

| ID | Descripción | Severidad |
|----|-------------|-----------|
| F9-AMB1 | Checklist: *"El usuario recibió el reporte"* — no define qué significa "recibir": ¿el agente presenta el contenido completo? ¿Solo muestra la ruta del archivo? ¿Espera confirmación explícita? | Media |
| F9-AMB2 | Los "Próximos Pasos" del template de reporte PyQt/MVC usan placeholders muy específicos del stack (`{FACTORY_CLASS}`, `{COORDINATOR_CLASS}`, `{COORDINATOR_CLASS}`). Para otros stacks (Flask, FastAPI, Generic) no hay equivalente y el agente puede dejar los placeholders sin reemplazar. | Baja |

---

## Resumen Global de Hallazgos

### Por OBS referenciada

| OBS | Estado en mejoras-agentes-kit.md | Hallazgos relacionados |
|-----|----------------------------------|------------------------|
| OBS-1 | Pendiente | F8-A2 |
| OBS-2 | Pendiente | F3-A2 |
| OBS-3 | Pendiente | F0-A3, F3-A4, F8-A3, F9-A3 |
| OBS-4 | Marcada como corregida (incorrectamente) | F2-A2, F2-AMB1 |
| OBS-5 | Pendiente | F1-A1, F2-A1, F3-A1, F4-A1, F5-A1, F6-A1, F8-A1, F9-A1 |
| OBS-6 | Pendiente | F0-A1 |

### Hallazgos nuevos (no referenciados en mejoras-agentes-kit.md)

| Hallazgo | Fase | Severidad |
|----------|------|-----------|
| F0-A2 | Comando pytest-bdd incorrecto | Media |
| F0-A4 | Rutas hardcodeadas en context.md | Baja |
| F1-A2 | Inconsistencia ruta feature file | Alta |
| F1-A3, F2-A3 | Links "siguiente fase" desactualizados | Baja |
| F1-A4 | Aprobación BDD sin instrucción concreta | Media |
| F2-A2 | OBS-4 incompleta (corrección parcial) | Alta |
| F3-A3 | Pseudocódigo Python en paso 6 | Baja |
| F4-A2 | Coverage hardcodeado vs perfil | Media |
| F5-A2 | Precondición débil en Fase 5 | Media |
| F5-A3 | Scope incorrecto en checklist Fase 5 | Baja |
| F6-A2, F6-A3 | Inconsistencia rutas feature files | Alta |
| F7-A1 | Precondición no ejecutable en Fase 7 | Alta |
| F7-A2 | Secciones de lenguajes no Python | Baja |
| F7-A3, F9-A2 | Umbrales hardcodeados vs perfil | Media |
| F8-A3, F9-A3 | CLI end-tracking sin definición | Media |

### Hallazgos por severidad

| Severidad | Cantidad |
|-----------|---------|
| Alta | 12 |
| Media | 20 |
| Baja | 10 |
| **Total** | **42** |

---

*Última actualización: 2026-02-26 — Fases 0-9 analizadas. Pendiente: skill.md, artifacts.md, conventions.md.*
