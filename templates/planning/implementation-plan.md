# Plan de Implementación: {US_ID} - {US_TITLE}

<!-- Template para generar plan de implementación de historias de usuario -->
<!-- Variables disponibles:
  - US: {US_ID}, {US_TITLE}, {PRIORITY}, {STORY_POINTS}, {PRODUCT}
  - Usuario: {USER_ROLE}, {USER_WANT}, {USER_BENEFIT}
  - Componentes: {COMPONENT_N_NAME}, {COMPONENT_N_TYPE}, {COMPONENT_N_PATH}, {COMPONENT_N_PATTERN}, {COMPONENT_N_TIME}
  - Tests: {UNIT_TESTS_TIME}, {INTEGRATION_TESTS_TIME}
  - Dependencias: {BLOCKING_US}, {RELATED_US}, {EXTERNAL_DEPS}
  - Progreso: {CURRENT_STATE}, {COMPLETED_TASKS}, {TOTAL_TASKS}, {PROGRESS_PERCENTAGE}, {TIME_SPENT}, {TIME_REMAINING}
  - Notas: {IMPLEMENTATION_NOTES}, {LESSONS_LEARNED}
  - Revisión: {LAST_UPDATE}, {UPDATED_BY}
  - Snippets: {SNIPPET:integration_checklist}
-->

## Información de la Historia

**US:** {US_ID}
**Título:** {US_TITLE}
**Prioridad:** {PRIORITY}
**Puntos:** {STORY_POINTS}
**Producto:** {PRODUCT}
**Fecha inicio:** {START_DATE}
**Estado:** EN PROGRESO

---

## Resumen

**Como** {USER_ROLE}
**Quiero** {USER_WANT}
**Para** {USER_BENEFIT}

---

## Componentes a Implementar

### 1. {COMPONENT_1_NAME} ({COMPONENT_1_TYPE})

**Ubicación:** `{COMPONENT_1_PATH}`
**Patrón:** {COMPONENT_1_PATTERN}
**Estimación:** {COMPONENT_1_TIME}

**Tareas:**
- [ ] Crear archivo base con estructura
- [ ] Implementar lógica principal
- [ ] Agregar validaciones
- [ ] Documentar con docstrings

---

### 2. {COMPONENT_2_NAME} ({COMPONENT_2_TYPE})

**Ubicación:** `{COMPONENT_2_PATH}`
**Patrón:** {COMPONENT_2_PATTERN}
**Estimación:** {COMPONENT_2_TIME}

**Tareas:**
- [ ] Crear archivo base
- [ ] Implementar métodos principales
- [ ] Conectar componentes según arquitectura

---

## Tests

### Tests Unitarios

{TEST_FILE_PATTERN}

**Estimación tests unitarios:** {UNIT_TESTS_TIME}

---

### Tests de Integración

- [ ] `tests/test_{component_1}_integracion.py` - Flujo completo

**Estimación tests integración:** {INTEGRATION_TESTS_TIME}

---

## Validación

### Escenarios BDD
- [ ] `tests/features/{US_ID}-{name}.feature` - Todos los escenarios pasan

### Quality Gates
- [ ] Pylint ≥ 8.0
- [ ] CC promedio ≤ 10
- [ ] MI promedio > 20
- [ ] Coverage ≥ 95%

---

## Dependencias

**Historias bloqueantes:** {BLOCKING_US}
**Historias relacionadas:** {RELATED_US}
**Componentes externos:** {EXTERNAL_DEPS}

---

## Checklist de Progreso

### Implementación
- [ ] Componente 1 implementado
- [ ] Componente 2 implementado
{SNIPPET:integration_checklist}

### Testing
- [ ] Tests unitarios implementados
- [ ] Tests unitarios pasan (100%)
- [ ] Tests integración implementados
- [ ] Tests integración pasan (100%)
- [ ] Escenarios BDD implementados
- [ ] Escenarios BDD pasan (100%)

### Calidad
- [ ] Pylint ejecutado y aprobado
- [ ] Métricas CC/MI calculadas y aprobadas
- [ ] Coverage ≥ 95%
- [ ] Code review realizado

### Documentación
- [ ] Docstrings agregados
- [ ] Arquitectura actualizada (si aplica)
- [ ] CHANGELOG actualizado
- [ ] Reporte final generado

---

## Progreso

**Estado:** {CURRENT_STATE}
**Tareas completadas:** {COMPLETED_TASKS}/{TOTAL_TASKS}
**Progreso:** {PROGRESS_PERCENTAGE}%
**Tiempo invertido:** {TIME_SPENT}
**Tiempo estimado restante:** {TIME_REMAINING}

---

## Notas de Implementación

{IMPLEMENTATION_NOTES}

---

## Lecciones Aprendidas

{LESSONS_LEARNED}

---

## Revisión

**Última actualización:** {LAST_UPDATE}
**Actualizado por:** {UPDATED_BY}
