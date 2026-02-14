# Reporte de Implementación: {US_ID} - {US_TITLE}

<!-- Template para generar reporte final de implementación de historias de usuario -->
<!-- Variables: US, componentes, tests, métricas, tiempos, etc. -->
<!-- Snippets: architecture_code_blocks, manual_testing_specifics -->

## Información General

| Campo | Valor |
|-------|-------|
| **Historia de Usuario** | {US_ID} |
| **Título** | {US_TITLE} |
| **Producto** | {PRODUCT} |
| **Prioridad** | {PRIORITY} |
| **Puntos estimados** | {STORY_POINTS} |
| **Fecha inicio** | {START_DATE} |
| **Fecha fin** | {END_DATE} |
| **Tiempo real** | {ACTUAL_TIME} |
| **Estado** | ✅ COMPLETADO / ⚠️ PARCIAL / ❌ BLOQUEADO |

---

## Resumen Ejecutivo

{EXECUTIVE_SUMMARY}

---

## Componentes Implementados

### Código Fuente

- ✅ `{FILE_1}` - {DESCRIPTION_1}
- ✅ `{FILE_2}` - {DESCRIPTION_2}
- ✅ `{FILE_3}` - {DESCRIPTION_3}

**Total archivos creados:** {TOTAL_FILES}
**Líneas de código:** {LOC}

---

### Tests

#### Tests Unitarios
- ✅ `{TEST_FILE_1}` - {TEST_COUNT_1} tests
- ✅ `{TEST_FILE_2}` - {TEST_COUNT_2} tests
- ✅ `{TEST_FILE_3}` - {TEST_COUNT_3} tests

**Total tests unitarios:** {TOTAL_UNIT_TESTS}
**Estado:** {UNIT_TESTS_PASSED}/{TOTAL_UNIT_TESTS} pasando

#### Tests de Integración
- ✅ `{INTEGRATION_TEST_FILE}` - {INTEGRATION_TEST_COUNT} tests

**Estado:** {INTEGRATION_TESTS_PASSED}/{INTEGRATION_TEST_COUNT} pasando

#### Escenarios BDD
- ✅ `{BDD_FILE}` - {BDD_SCENARIO_COUNT} escenarios

**Estado:** {BDD_PASSED}/{BDD_SCENARIO_COUNT} pasando

---

## Métricas de Calidad

| Métrica | Valor | Objetivo | Estado |
|---------|-------|----------|--------|
| **Pylint** | {PYLINT_SCORE}/10 | ≥ 8.0 | {PYLINT_STATUS} |
| **Complejidad Ciclomática** | {CC_AVG} | ≤ 10 | {CC_STATUS} |
| **Índice Mantenibilidad** | {MI_AVG} | > 20 | {MI_STATUS} |
| **Coverage** | {COVERAGE}% | ≥ 95% | {COVERAGE_STATUS} |

### Detalle de Pylint

```
{PYLINT_OUTPUT}
```

### Detalle de Coverage

```
{COVERAGE_REPORT}
```

---

## Criterios de Aceptación

{ACCEPTANCE_CRITERIA_CHECKLIST}

**Ejemplo:**
- [x] Criterio 1: Descripción
- [x] Criterio 2: Descripción
- [x] Criterio 3: Descripción

**Estado:** {CRITERIA_MET}/{TOTAL_CRITERIA} cumplidos

---

## Arquitectura Implementada

### Patrón Aplicado

{ARCHITECTURE_DESCRIPTION}

### Diagrama de Componentes

```
{COMPONENT_DIAGRAM}
```

### Flujo de Datos

```
{DATA_FLOW_DIAGRAM}
```

---

## Integración con Sistema Existente

{SNIPPET:architecture_code_blocks}

---

## Desafíos y Soluciones

### Desafío 1: {CHALLENGE_1_TITLE}

**Descripción:** {CHALLENGE_1_DESCRIPTION}

**Solución:** {CHALLENGE_1_SOLUTION}

**Aprendizaje:** {CHALLENGE_1_LEARNING}

---

### Desafío 2: {CHALLENGE_2_TITLE}

**Descripción:** {CHALLENGE_2_DESCRIPTION}

**Solución:** {CHALLENGE_2_SOLUTION}

---

## Cambios no Previstos

{UNPLANNED_CHANGES}

**Ejemplo:**
- Se agregó validación adicional por casos extremos
- Se modificó componente para mejor UX (aprobado por usuario)

---

## Refactorings Realizados

{REFACTORINGS}

**Ejemplo:**
- Se extrajo lógica común a método helper
- Se simplificó condicional complejo usando dict lookup

---

## Documentación Actualizada

- [x] Docstrings agregados a todas las clases y métodos
- [x] Arquitectura actualizada (si aplica)
- [x] CHANGELOG.md actualizado
- [x] Plan de implementación completado
- [ ] README con screenshots (pendiente)

---

## Testing Manual Realizado

### Casos de Prueba

1. **Caso 1:** {TEST_CASE_1_NAME}
   - **Pasos:** {STEPS}
   - **Resultado esperado:** {EXPECTED}
   - **Resultado real:** {ACTUAL}
   - **Estado:** ✅ PASS / ❌ FAIL

2. **Caso 2:** {TEST_CASE_2_NAME}
   - **Pasos:** {STEPS}
   - **Resultado esperado:** {EXPECTED}
   - **Resultado real:** {ACTUAL}
   - **Estado:** ✅ PASS

{SNIPPET:manual_testing_specifics}

---

## Deuda Técnica

{TECHNICAL_DEBT}

**Ejemplo:**
- TODO: Agregar animación de transición
- TODO: Implementar retry logic en caso de error
- NOTE: Considerar refactor futuro

---

## Próximos Pasos

### Historias Relacionadas

- [ ] {NEXT_US_1} - {NEXT_US_1_TITLE}
- [ ] {NEXT_US_2} - {NEXT_US_2_TITLE}

### Mejoras Futuras

- {FUTURE_IMPROVEMENT_1}
- {FUTURE_IMPROVEMENT_2}

---

## Tiempo Invertido

| Fase | Tiempo Estimado | Tiempo Real | Diferencia |
|------|----------------|-------------|------------|
| **Generación BDD** | {BDD_EST} | {BDD_ACTUAL} | {BDD_DIFF} |
| **Plan** | {PLAN_EST} | {PLAN_ACTUAL} | {PLAN_DIFF} |
| **Implementación** | {IMPL_EST} | {IMPL_ACTUAL} | {IMPL_DIFF} |
| **Tests unitarios** | {UNIT_EST} | {UNIT_ACTUAL} | {UNIT_DIFF} |
| **Tests integración** | {INT_EST} | {INT_ACTUAL} | {INT_DIFF} |
| **Validación BDD** | {VAL_EST} | {VAL_ACTUAL} | {VAL_DIFF} |
| **Quality gates** | {QG_EST} | {QG_ACTUAL} | {QG_DIFF} |
| **TOTAL** | {TOTAL_EST} | {TOTAL_ACTUAL} | {TOTAL_DIFF} |

**Accuracy:** {ESTIMATION_ACCURACY}%

---

## Lecciones Aprendidas

### Lo que Funcionó Bien

1. {WHAT_WORKED_1}
2. {WHAT_WORKED_2}

### Lo que Puede Mejorar

1. {WHAT_CAN_IMPROVE_1}
2. {WHAT_CAN_IMPROVE_2}

### Recomendaciones para Próximas Historias

1. {RECOMMENDATION_1}
2. {RECOMMENDATION_2}

---

## Aprobación

**Implementado por:** {DEVELOPER_NAME}
**Revisado por:** {REVIEWER_NAME}
**Aprobado por:** {APPROVER_NAME}
**Fecha de aprobación:** {APPROVAL_DATE}

---

## Anexos

### Anexo A: Salida Completa de Tests

```
{FULL_TEST_OUTPUT}
```

### Anexo B: Reporte de Coverage HTML

Ubicación: `htmlcov/index.html`

### Anexo C: Reporte de Quality Metrics

Ubicación: `quality/reports/{US_ID}-quality.json`

---

**Versión del reporte:** 1.0
**Generado por:** Claude Code - Skill /implement-us
**Fecha:** {REPORT_DATE}
