# Fase 9: Reporte Final

**Objetivo:** Generar un reporte completo de la implementación con métricas, componentes creados y estado final.


---

## 🔴 Acción Requerida — Verificar insumos del reporte

El reporte final consolida datos de fases anteriores. Antes de comenzar, verificá que existen:

```bash
ls docs/plans/{US_ID}-plan.md              # Para listar tareas completadas
ls quality/reports/{US_ID}-quality.json    # Para incluir métricas reales
```

Si alguno no existe, **no avances** — completá la fase correspondiente primero.

---

## 🔴 Acción Requerida — Iniciar tracking de fase

Ejecutá como primera acción, antes de cualquier otra:

```bash
python .claude/tracking/tracker_cli.py start-phase 9 "Reporte Final"
```

---

## 🔴 Acción Requerida — Leer umbrales antes de completar el template

Antes de generar el reporte, leé los umbrales reales desde el reporte de quality gates:

```bash
cat quality/reports/{US_ID}-quality.json | jq '.umbrales'
```

Mapeá los valores obtenidos a los placeholders del template:

| Campo en `quality.json → umbrales` | Placeholder en el template |
|------------------------------------|---------------------------|
| `pylint_min` | `{PYLINT_MIN}` |
| `cc_max` | `{CC_MAX}` |
| `mi_min` | `{MI_MIN}` |
| `coverage_min` | `{COVERAGE_MIN}` |

No uses valores hardcodeados ni los reconstruyas de memoria. El `quality.json` es la fuente de verdad.

---

## Acción

Generar un reporte estructurado que documente todo el proceso de implementación, desde los escenarios BDD hasta las métricas de calidad final.

**Template:** `.claude/templates/implementation-report.md`

---

## Contenido del Reporte

### Estructura del Reporte

```markdown
# Reporte de Implementación: {US_ID}

## Resumen Ejecutivo
- **Historia de Usuario:** {US_ID} - {US_TITLE}
- **Puntos estimados:** {STORY_POINTS}
- **Tiempo estimado:** {ESTIMATED_TIME}
- **Tiempo real:** {ACTUAL_TIME}
- **Varianza:** {VARIANCE} ({VARIANCE_PERCENTAGE}%)
- **Estado:** ✅ COMPLETADO
- **Fecha completado:** {COMPLETION_DATE}

## Componentes Implementados
[Lista de componentes con checkmarks]

## Métricas de Calidad
[Pylint, CC, MI, Coverage con valores y status]

## Tests Implementados
[Cantidad y tipos de tests]

## Archivos Creados/Modificados
[Lista completa de archivos]

## Criterios de Aceptación
[Checklist de criterios cumplidos]

## Próximos Pasos
[Tareas pendientes o sugerencias]
```

---

## Template por Stack

### PyQt/MVC - Reporte de Implementación

```markdown
# Reporte de Implementación: {US_ID}

## Resumen Ejecutivo

- **Historia de Usuario:** {US_ID} - {US_TITLE}
- **Puntos estimados:** {STORY_POINTS}
- **Tiempo estimado:** {ESTIMATED_TIME}
- **Tiempo real:** {ACTUAL_TIME}
- **Varianza:** {VARIANCE} ({VARIANCE_PERCENTAGE}%)
- **Estado:** ✅ COMPLETADO
- **Fecha completado:** {COMPLETION_DATE}

---

## Componentes Implementados

### Arquitectura MVC

- ✅ **{COMPONENT_NAME}Modelo** (`{COMPONENT_PATH}/modelo.py`)
  - Dataclass inmutable con validación
  - {FIELD_COUNT} campos de datos
  - Métodos de negocio implementados

- ✅ **{COMPONENT_NAME}Vista** (`{COMPONENT_PATH}/vista.py`)
  - {WIDGET_COUNT} widgets
  - Layout: {LAYOUT_TYPE}
  - Señales conectadas: {SIGNAL_COUNT}

- ✅ **{COMPONENT_NAME}Controlador** (`{COMPONENT_PATH}/controlador.py`)
  - Mediador entre Modelo y Vista
  - Manejo de {EVENT_COUNT} eventos
  - Integración con {EXTERNAL_SERVICES}

- ✅ **Factory** (`{COMPONENT_PATH}/__init__.py`)
  - Función `crear_{component_name}()`
  - Inyección de dependencias

---

## Métricas de Calidad

| Métrica | Valor | Umbral | Estado |
|---------|-------|--------|--------|
| Pylint | {PYLINT_SCORE}/10 | ≥ {PYLINT_MIN} | {STATUS} |
| Complejidad Ciclomática (máx/función) | {CC_SCORE} | ≤ {CC_MAX} | {STATUS} |
| Índice de Mantenibilidad | {MI_SCORE} | > {MI_MIN} | {STATUS} |
| Cobertura de Tests | {COVERAGE}% | ≥ {COVERAGE_MIN}% | {STATUS} |

> Leé los umbrales del campo `umbrales` en `quality/reports/{US_ID}-quality.json`

**Estado General:** ✅ APROBADO

---

## Tests Implementados

### Tests Unitarios ({UNIT_TEST_COUNT} tests)

- ✅ `test_{component}_modelo.py` ({MODEL_TEST_COUNT} tests)
  - Creación con valores default/custom
  - Inmutabilidad (frozen dataclass)
  - Validación de datos
  - Métodos de negocio

- ✅ `test_{component}_vista.py` ({VIEW_TEST_COUNT} tests)
  - Construcción de widgets
  - Actualización de UI
  - Señales emitidas

- ✅ `test_{component}_controlador.py` ({CONTROLLER_TEST_COUNT} tests)
  - Mediación modelo-vista
  - Manejo de eventos
  - Lógica de presentación

### Tests de Integración ({INTEGRATION_TEST_COUNT} tests)

- ✅ `test_{component}_integration.py`
  - Flujo completo MVC
  - Integración con servicios externos
  - Comunicación entre paneles

### Escenarios BDD ({BDD_SCENARIO_COUNT} escenarios)

- ✅ `{US_ID}-{feature}.feature`
  - {SCENARIO_1_NAME}
  - {SCENARIO_2_NAME}
  - {SCENARIO_3_NAME}

**Todos los tests pasando:** ✅ {TOTAL_TEST_COUNT} passed, 0 failed

---

## Archivos Creados

### Código de Producción
- `{COMPONENT_PATH}/modelo.py` ({MODEL_LOC} líneas)
- `{COMPONENT_PATH}/vista.py` ({VIEW_LOC} líneas)
- `{COMPONENT_PATH}/controlador.py` ({CONTROLLER_LOC} líneas)
- `{COMPONENT_PATH}/__init__.py` ({FACTORY_LOC} líneas)

### Tests
- `tests/test_{component}_modelo.py` ({MODEL_TEST_LOC} líneas)
- `tests/test_{component}_vista.py` ({VIEW_TEST_LOC} líneas)
- `tests/test_{component}_controlador.py` ({CONTROLLER_TEST_LOC} líneas)
- `tests/test_{component}_integration.py` ({INTEGRATION_TEST_LOC} líneas)
- `tests/features/{US_ID}-{feature}.feature` ({FEATURE_LOC} líneas)
- `tests/step_defs/test_{feature}_steps.py` ({STEPS_LOC} líneas)

### Documentación
- `docs/plans/{US_ID}-plan.md`
- `docs/reports/{US_ID}-report.md` (este archivo)
- `quality/reports/{US_ID}-quality.json`

**Total líneas de código:** {TOTAL_LOC} (producción: {PROD_LOC}, tests: {TEST_LOC})

---

## Criterios de Aceptación

- [x] {CRITERION_1}
- [x] {CRITERION_2}
- [x] {CRITERION_3}
- [x] {CRITERION_4}
- [x] {CRITERION_5}

**Todos los criterios cumplidos:** ✅

---

## Próximos Pasos

- [ ] {INTEGRATION_TASK} (integración del componente con el sistema existente)
- [ ] Implementar {NEXT_US_ID} ({NEXT_US_TITLE})
- [ ] {OPTIONAL_IMPROVEMENT} (opcional)

---

## Lecciones Aprendidas

- ✅ {LESSON_1}
- ⚠️ {LESSON_2}
- 💡 {LESSON_3}

---

**Reporte generado automáticamente por Claude Code**
**Fecha:** {REPORT_DATE}
```

---

### FastAPI - Reporte de Implementación

```markdown
# Reporte de Implementación: {US_ID}

## Resumen Ejecutivo

- **Historia de Usuario:** {US_ID} - {US_TITLE}
- **Puntos estimados:** {STORY_POINTS}
- **Tiempo real:** {ACTUAL_TIME}
- **Estado:** ✅ COMPLETADO

---

## Componentes Implementados

### Arquitectura en Capas

- ✅ **Endpoints** (`app/api/v1/endpoints/{component}.py`)
  - {ENDPOINT_COUNT} endpoints REST
  - Autenticación/autorización configurada
  - OpenAPI docs generados

- ✅ **Schemas** (`app/schemas/{component}.py`)
  - {SCHEMA_COUNT} schemas Pydantic
  - Validación automática
  - Serialización/deserialización

- ✅ **Service** (`app/services/{component}_service.py`)
  - Lógica de negocio
  - {METHOD_COUNT} métodos públicos
  - Manejo de excepciones de dominio

- ✅ **Repository** (`app/repositories/{component}_repo.py`)
  - CRUD operations
  - Queries optimizadas
  - Transacciones

- ✅ **Model** (`app/models/{component}.py`)
  - ORM model (SQLAlchemy/Tortoise)
  - {FIELD_COUNT} campos
  - Relaciones configuradas

---

## API Endpoints

| Método | Ruta | Descripción | Auth |
|--------|------|-------------|------|
| GET | `/api/v1/{resource}` | Listar {resource} | ✅ |
| GET | `/api/v1/{resource}/{id}` | Obtener por ID | ✅ |
| POST | `/api/v1/{resource}` | Crear {resource} | ✅ |
| PUT | `/api/v1/{resource}/{id}` | Actualizar {resource} | ✅ |
| DELETE | `/api/v1/{resource}/{id}` | Eliminar {resource} | ✅ |

**OpenAPI Docs:** `/docs`

---

## Métricas de Calidad

| Métrica | Valor | Umbral | Estado |
|---------|-------|--------|--------|
| Pylint | {PYLINT_SCORE}/10 | ≥ {PYLINT_MIN} | {STATUS} |
| Complejidad Ciclomática (máx/función) | {CC_SCORE} | ≤ {CC_MAX} | {STATUS} |
| Índice de Mantenibilidad | {MI_SCORE} | > {MI_MIN} | {STATUS} |
| Cobertura de Tests | {COVERAGE}% | ≥ {COVERAGE_MIN}% | {STATUS} |

> Leé los umbrales del campo `umbrales` en `quality/reports/{US_ID}-quality.json`

---

## Tests Implementados

### Tests Unitarios ({UNIT_TEST_COUNT} tests)
- Schema validation ({SCHEMA_TEST_COUNT} tests)
- Service logic ({SERVICE_TEST_COUNT} tests)
- Repository operations ({REPO_TEST_COUNT} tests)

### Tests de Integración ({INTEGRATION_TEST_COUNT} tests)
- API endpoints end-to-end
- Database transactions
- Authentication flows

### Escenarios BDD ({BDD_SCENARIO_COUNT} escenarios)
- {SCENARIO_1_NAME}
- {SCENARIO_2_NAME}

**Todos los tests pasando:** ✅

---

## Migraciones de Base de Datos

- ✅ `migrations/{VERSION}_{component}.py`
  - Tabla `{TABLE_NAME}` creada
  - {FIELD_COUNT} columnas
  - Índices configurados

---

## Próximos Pasos

- [ ] Agregar endpoints de búsqueda/filtrado
- [ ] Implementar paginación en lista
- [ ] Agregar WebSocket para real-time updates
- [ ] Implementar {NEXT_US_ID}
```

---

### Generic Python - Reporte de Implementación

```markdown
# Reporte de Implementación: {US_ID}

## Componentes Implementados

- ✅ **{ComponentClass}** (`{module_path}/{component}.py`)
  - {METHOD_COUNT} métodos públicos
  - {PROPERTY_COUNT} properties
  - Documentación completa

- ✅ **Utilidades** (`{module_path}/utils.py`)
  - {UTIL_COUNT} funciones auxiliares

---

## API Pública

```python
from {module_path} import {ComponentClass}

# Uso básico
component = {ComponentClass}(config)
result = component.{main_method}(data)
```

---

## Dependencias Agregadas

- {DEPENDENCY_1} >= {VERSION}
- {DEPENDENCY_2} >= {VERSION}
```

---

## Ubicación del Reporte

**Archivo:** `{PROJECT_PATH}/docs/reports/{US_ID}-report.md`

**Alternativas:**
- `{PROJECT_PATH}/docs/implementation-reports/{US_ID}.md`
- `{PROJECT_PATH}/reports/{US_ID}-implementation.md`

---

## Generación Automática (opcional)

Crear script para generar reporte automáticamente:

```python
# scripts/generate_report.py
import json
from datetime import datetime
from pathlib import Path

def generar_reporte(us_id, component_path, metricas, archivos, tests):
    """Generar reporte de implementación."""

    # Leer quality report
    quality_file = f"quality/reports/{us_id}-quality.json"
    with open(quality_file) as f:
        quality = json.load(f)

    # Leer time tracking
    time_data = tracker.get_report(us_id)

    # Generar markdown
    report = f"""# Reporte de Implementación: {us_id}

## Resumen Ejecutivo

- **Historia:** {us_id}
- **Tiempo real:** {time_data['total_time']}
- **Estado:** ✅ COMPLETADO
- **Fecha:** {datetime.now().strftime('%Y-%m-%d')}

## Métricas de Calidad

| Métrica | Valor | Estado |
|---------|-------|--------|
| Pylint | {quality['metricas']['pylint']}/10 | ✅ |
| CC | {quality['metricas']['cc_promedio']} | ✅ |
| MI | {quality['metricas']['mi_promedio']} | ✅ |
| Coverage | {quality['metricas']['coverage']}% | ✅ |

## Archivos Creados

{generar_lista_archivos(archivos)}

## Tests

- Unitarios: {tests['unit']} tests
- Integración: {tests['integration']} tests
- BDD: {tests['bdd']} escenarios

**Total:** {tests['total']} tests ✅
"""

    # Guardar reporte
    output = f"docs/reports/{us_id}-report.md"
    Path(output).parent.mkdir(parents=True, exist_ok=True)

    with open(output, 'w') as f:
        f.write(report)

    return output
```

**Uso:**
```bash
python scripts/generate_report.py {US_ID}
```

---

## 🚫 STOP — Verificar reporte antes de cerrar

**No cierres el tracking hasta que:**
1. `docs/reports/{US_ID}-report.md` exista en disco: `ls docs/reports/{US_ID}-report.md`
2. El reporte incluya las métricas reales leídas desde `quality/reports/{US_ID}-quality.json` (no reconstruidas de memoria)
3. El contenido completo del reporte fue presentado en la conversación e indicada la ruta del archivo: *"Reporte generado: `docs/reports/{US_ID}-report.md`"*

---

## ✅ Checklist de Salida

Antes de cerrar el tracking, confirmá que:
- [ ] `docs/reports/{US_ID}-report.md` existe en disco
- [ ] El reporte incluye métricas reales de Fase 7
- [ ] Reporte presentado en la conversación con ruta del archivo (`docs/reports/{US_ID}-report.md`)
- [ ] Tracking de Fase 9 cerrado

---

## 🔴 Acción Requerida — Verificar reporte antes de cerrar

Confirmá que el reporte final existe en disco antes de cerrar el tracking:

```bash
ls docs/reports/{US_ID}-report.md
```

Si no existe, generalo usando el template de la sección anterior antes de continuar.

---

## 🔴 Acción Requerida — Cerrar tracking

```bash
# Cerrar fase 9
python .claude/tracking/tracker_cli.py end-phase 9

# Cerrar tracking completo de la US
python .claude/tracking/tracker_cli.py end
```

> **¿Qué hace `end`?** Es el único punto del skill donde se invoca este subcomando.
> A diferencia de `end-phase` (que cierra solo la fase actual), `end` cierra el
> tracking completo de la US: calcula el tiempo total real acumulado en todas las fases,
> guarda el histórico en `.claude/tracking/` y genera el reporte de tiempo final.
> Debe ejecutarse **después** de `end-phase 9`, no en lugar de él.

---

## Resumen de la Fase

Al finalizar esta fase:

✅ Reporte completo de implementación generado
✅ Resumen ejecutivo con tiempos y varianza
✅ Lista completa de componentes implementados
✅ Métricas de calidad documentadas
✅ Tests y cobertura reportados
✅ Archivos creados listados
✅ Criterios de aceptación verificados
✅ Próximos pasos identificados
✅ Tracking finalizado y datos guardados

**El skill implement-us ha completado todas sus fases.** ✅

---

## Acciones Post-Implementación

Después de generar el reporte:

1. **Compartir reporte** con el equipo (standup, chat, wiki)
2. **Actualizar board** (mover ticket a "Done")
3. **Cerrar branch** (si no se mergea automáticamente)
4. **Celebrar** 🎉 - Implementación completada exitosamente

---

**Fin del Skill implement-us**
