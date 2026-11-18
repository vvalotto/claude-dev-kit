# Hallazgos — Análisis Skill por Skill

Inventario de ajustes y ambigüedades del skill `implement-us`.

**Última auditoría completa:** 2026-11-18 (v1.7.0) — Fases 0-9 + `skill.md`, `artifacts.md`, `conventions.md`, `README.md`.
**Auditoría anterior:** 2026-02-27 (v1.2). Detalle original en el historial de git de este archivo.

**Metodología:** Cada hallazgo se re-verifica contra el archivo actual (lectura directa y `grep`), en orden: fases 0→9 y luego archivos genéricos. Después se buscan problemas nuevos introducidos por releases posteriores (perfiles BC-first, `tracker_cli.py`, CodeGuard).

---

## Severidades

| Nivel | Criterio |
|-------|---------|
| Alta | Puede causar fallo o comportamiento incorrecto del agente |
| Media | Genera inconsistencia o resultado subóptimo |
| Baja | Mejora de claridad o mantenibilidad |

---

## Resumen

| Estado | Cantidad |
|--------|---------|
| Hallazgos originales (2026-02-27) | 64 |
| ✅ Resueltos | 68 |
| ⚠️ Vigentes | 0 |
| 🆕 Nuevos (2026-11-18) | 9 (4 resueltos) |
| **Abiertos en total** | **5** |

> El resumen de la auditoría anterior indicaba 48 hallazgos; el recuento real de IDs listados era 64.

---

## ⚠️ Hallazgos vigentes (de la auditoría anterior)

Ninguno. F3-AMB2, F3-AMB4 y F7-AMB1 se corrigieron tras la auditoría (ver sección de resueltos).

---

## 🆕 Hallazgos nuevos (2026-11-18)

| ID | Dónde | Descripción | Severidad |
|----|-------|-------------|-----------|
| N-5 | Fases 8 y 9 | No hay instrucción para obtener el tiempo real: `{ACTUAL_TIME}` y la tabla "Métricas de Tiempo" no indican qué comando usar (`status` solo da el total transcurrido). El script opcional de Fase 9 llama a `tracker.get_report(us_id)`, que no existe en `TimeTracker`, y `tracker` no está definido. | Media |
| N-6 | Fase 7 | El ejemplo de CI/CD hardcodea `--fail-under=8.0` y `--cov-fail-under=95`, mientras el resto de la fase exige leer los umbrales del perfil activo. | Baja |
| N-7 | Fase 0 | Paso 6 indica leer `unit_test_path` e `integration_test_path` del perfil para `pytest.ini`, pero el contenido de ejemplo fija `testpaths = tests` y no usa esas claves. El template de `context.md` (Paso 8) además repite rutas literales aunque remite a `artifacts.md`. | Baja |
| N-8 | `templates/planning/implementation-plan.md` | El template del plan todavía incluye secciones "Tests" y "Validación" con estimaciones (`{UNIT_TESTS_TIME}`, `{INTEGRATION_TESTS_TIME}`), checklist de testing y "Coverage ≥ 95%" hardcodeado. Contradice la Fase 2 (F2-A2/OBS-4: el plan no incluye tests ni quality gates) y los umbrales por perfil. Fase 2 indica usar este template si existe en `.claude/templates/planning/`. | Media |
| N-9 | Fases 7 y 9, perfiles BC-first | `hexagonal-ddd-bc` y `clean-architecture-bc` no definen `quality_gates.maintainability_index`, pero el snippet de Fase 7 lee `qg["maintainability_index"]["min_score"]` y Fase 9 mapea `mi_min` desde `quality.json`. Con esos perfiles el snippet falla (`KeyError`) y el reporte queda sin umbral de MI. | Media |

---

## ✅ Hallazgos resueltos

Verificados en 2026-11-18 contra el código actual.

### Fase 0 — `phase-0-validation.md`

| ID | Cómo se resolvió |
|----|------------------|
| F0-A1 | Paso 3 pregunta proactivamente fuente de HU y arquitectura antes de buscar (OBS-6). |
| F0-A2 | Verificación con `python -c "import pytest_bdd; print(pytest_bdd.__version__)"`. |
| F0-A3 | Usa `tracker_cli.py init` + `start-phase`, interfaz real. |
| F0-A4 | Mitigado: el template remite a `artifacts.md` como fuente de verdad (ver N-7 para el resto). |
| F0-AMB1 | Paso 6 define qué se crea (`.pylintrc`, `pytest.ini`) con contenido mínimo y notifica al usuario. |
| F0-AMB2 | Instrucción explícita de ejecutar de arriba a abajo; pasos numerados de forma única. |
| F0-AMB3 | Lee `variables.architecture_pattern.default` del perfil; ya no hay "validar patrones". |
| F0-AMB4 | Define respuestas `[sí]`/`[no-bdd]`/`[otro]`; cualquier otro mensaje cuenta como confirmación. |

### Fase 1 — `phase-1-bdd.md`

| ID | Cómo se resolvió |
|----|------------------|
| F1-A1 | Sin referencias a Django. |
| F1-A2, F1-AMB4 | Ruta única `tests/features/{US_ID}-{nombre}.feature`, con convención de `{nombre}`. |
| F1-A3 | Links de navegación correctos. |
| F1-A4 | Paso 6 🔴 con respuestas `[aprobado]`/`[revisar]`/`[rechazar]`. |
| F1-AMB1 | Paso 3 explica el template por perfil y cómo usarlo (referencia estructural, no copia literal). Los 3 templates existen en `templates/bdd/`. |
| F1-AMB2 | Paso 4: 1 escenario exitoso por criterio + uno por cada condición de error mencionada. |
| F1-AMB3 | Lee criterios del archivo indicado en `fuente_hu` de `context.md`. |

### Fase 2 — `phase-2-planning.md`

| ID | Cómo se resolvió |
|----|------------------|
| F2-A1 | Sin referencias a Django. |
| F2-A2, F2-AMB1 | Plan sin secciones de Tests/Validación; nota explícita de que van en Fases 4-7 (OBS-4). |
| F2-A3 | Links de navegación correctos. |
| F2-AMB2 | Ya no hay estimaciones de tiempo en el plan. |
| F2-AMB3 | Define la clave real: `variables.architecture_pattern.default`. |

### Fase 3 — `phase-3-implementation.md`

| ID | Cómo se resolvió |
|----|------------------|
| F3-A1 | Sin referencias a Django. |
| F3-A2 | Paso 11 🔴 "Revisión de código obsoleto" (OBS-2). |
| F3-A3 | Paso 6 usa el tool `Write`, sin pseudocódigo. |
| F3-A4 | `start-task`/`end-task` coinciden con `tracker_cli.py`. |
| F3-AMB1 | Paso 5 define el flujo de `edit` (describir cambios o pegar código, y re-aprobar). |
| F3-AMB2 | Corregido tras la auditoría: la fase no ejecuta tests; solo verifica sintaxis e imports. |
| F3-AMB4 | Corregido tras la auditoría: tabla en el paso 2 que define `TASK_ID`, `TASK_NAME`, `TASK_TYPE` y `ESTIMATED_MINUTES`. |
| F3-AMB3 | El tracking se inicia antes que cualquier otra acción. |

### Fases 4, 5 y 6

| ID | Cómo se resolvió |
|----|------------------|
| F4-A1, F5-A1, F6-A1 | Sin referencias a Django. |
| F4-A2 | Umbral de coverage leído de `quality_gates.coverage.min_percent` del perfil. |
| F4-AMB1 | La sección de configuración por stack ya no usa bloques bash para texto descriptivo. |
| F4-AMB2, F5-A3 | Checklists ejecutan `pytest tests/unit/` y `pytest tests/integration/`. |
| F5-A2 | La precondición ejecuta `pytest tests/unit/`, un gate real. |
| F5-AMB1 | Estrategia de mocking con excepción documentada para componentes internos. |
| F5-AMB2 | "Intento" definido como ciclo completo (ejecución → detección → corrección); límite de 2 ciclos. |
| F6-A2, F6-A3 | Rutas unificadas (`tests/features/` para `.feature`, `tests/step_defs/` para steps). |
| F6-AMB1 | Protocolo de recuperación indica editar el feature en `tests/features/` y re-aprobar. |

### Fases 7, 8 y 9

| ID | Cómo se resolvió |
|----|------------------|
| F7-A1 | Precondición con comandos ejecutables. |
| F7-A2 | Sin secciones de lenguajes no Python. |
| F7-A3, F9-A2 | Umbrales leídos del perfil activo (`config.json` / `quality.json → umbrales`). |
| F7-AMB1 | Corregido tras la auditoría: `quality.json` incluye `cc_max` y el snippet lo compara contra el umbral; `cc_promedio` es informativo. |
| F7-AMB2 | Comandos con `{COMPONENT_PATH}`; la ruta `src/` de CodeGuard es propia de perfiles BC-first. |
| F8-A1, F9-A1 | Sin referencias a Django. |
| F8-A2, F8-AMB2 | Paso 2 🔴 "Discovery de documentación de arquitectura" con `grep`/`find` (OBS-1). |
| F8-A3 | Nota de fallback si el tracking no está disponible. |
| F8-AMB1 | Un único "Checklist de Salida" con ítems detallados. |
| F9-A3 | Usa `tracker_cli.py end`, documentado en `skill.md`. |
| F9-AMB1 | Checklist exige presentar el reporte completo y la ruta en la conversación. |
| F9-AMB2 | Ya no hay placeholders específicos de PyQt (`{FACTORY_CLASS}`, etc.) en "Próximos Pasos". |

### Hallazgos nuevos corregidos

| ID | Cómo se resolvió |
|----|------------------|
| N-4 | Fase 9, `skill.md` y `docs/skills/implement-us/phase-9.md` describen `end` tal como es: marca el cierre y muestra el tiempo total, sin generar reportes (se usa `/track-report`). |
| N-3 | Fase 6: los comandos de CI/CD ejecutan `tests/step_defs/` e indican los plugins `pytest-html` y `pytest-json-report`. |
| N-2 | `installer.py` (ejemplo `django-mvt` inexistente, lista de perfiles y ayuda de `--profile`), `install/config.json` (clave `profile_selection` sin uso eliminada), `skill.md` y `README.md` del skill cubren los 7 perfiles; footer actualizado a v1.7.0. |
| N-1 | Fases 1, 2 y 3 cubren perfiles BC-first y Flask Webapp leyendo `bdd_config`, `bc_feature`/`page_feature` y un comando de verificación genérico. |

### Archivos genéricos

| ID | Cómo se resolvió |
|----|------------------|
| SK-A1, SK-A2, SK-A4 | Sin referencias a Django en `skill.md`. |
| SK-A3 | Sección de tracking con interfaz real de `tracker_cli.py` (issue #61). |
| ART-A1 | `artifacts.md` usa `tests/features/{US_ID}-{nombre}.feature`. |
| CON-A1 | `conventions.md` usa `tracker_cli.py` (issue #61). |
| README.md | Sin referencias a Django ni a comandos de tracking obsoletos (ver N-2 para perfiles BC-first). |

---

## Estado de las OBS originales

| OBS | Tema | Estado | Hallazgos relacionados |
|-----|------|--------|------------------------|
| OBS-1 | Discovery de arquitectura en Fase 8 | ✅ Resuelta | F8-A2 |
| OBS-2 | Revisión de código obsoleto en Fase 3 | ✅ Resuelta | F3-A2 |
| OBS-3 | CLI de tracking unificado | ✅ Resuelta | F0-A3, F3-A4, F8-A3, F9-A3, SK-A3, CON-A1 (ver N-4, N-5) |
| OBS-4 | Plan sin secciones de tests/validación | ✅ Resuelta | F2-A2, F2-AMB1 |
| OBS-5 | Eliminar referencias a Django | ✅ Resuelta | F1-A1, F2-A1, F3-A1, F4-A1, F5-A1, F6-A1, F8-A1, F9-A1, SK-A1, SK-A2, SK-A4 |
| OBS-6 | Preguntar fuentes al inicio | ✅ Resuelta | F0-A1 |

---

*Última actualización: 2026-11-18 — Auditoría completa (v1.7.0).*
