# Templates - Documentación Técnica

Documentación técnica del sistema de templates del framework.

> **Para usuarios:** Ver [docs/templates/template-system.md](../docs/templates/template-system.md)

Este directorio contiene los templates reutilizables que el skill `/implement-us` utiliza internamente.

---

## Índice

- [Introducción](#introducción)
- [Categorías de Templates](#categorías-de-templates)
- [Sistema de Variables](#sistema-de-variables)
- [Sistema de Snippets](#sistema-de-snippets)
- [Uso de Templates](#uso-de-templates)
- [Ejemplos por Perfil](#ejemplos-por-perfil)
- [Personalización](#personalización)

---

## Introducción

### Propósito

Los templates son **archivos modelo parametrizados** que permiten generar automáticamente documentación y código adaptado al stack tecnológico del proyecto (PyQt, FastAPI, Flask, Python genérico, etc.).

### Características Principales

- **Framework-agnostic:** Un mismo template funciona para múltiples stacks
- **Basado en variables:** Placeholders `{VARIABLE}` que se reemplazan dinámicamente
- **Snippets condicionales:** Bloques de código específicos por perfil
- **Ejemplos incluidos:** Resultados pre-generados para cada perfil en `examples/`

### Cómo se Usan

El skill `/implement-us` genera archivos automáticamente durante las 10 fases de implementación:

| Fase | Template Usado | Output Generado |
|------|----------------|-----------------|
| Fase 1 | `bdd/scenario.feature` | `tests/features/{US_ID}-{name}.feature` |
| Fase 2 | `planning/implementation-plan.md` | `docs/plans/{US_ID}-plan.md` |
| Fase 4 | `testing/test-unit.py` | `tests/test_{component}.py` |
| Fase 9 | `reporting/implementation-report.md` | `docs/reports/{US_ID}-report.md` |

---

## Categorías de Templates

### 1. BDD Templates

**Directorio:** `templates/bdd/`

#### `scenario.feature`

Template para generar escenarios BDD en formato Gherkin usando pytest-bdd.

**Descripción:** Archivo `.feature` con la estructura de la historia de usuario traducida a escenarios ejecutables Given-When-Then.

**Variables principales:**
- `{FEATURE_TITLE}`, `{US_ID}`, `{USER_ROLE}`, `{USER_WANT}`, `{USER_BENEFIT}`
- `{APP_INIT_STEP}`, `{CONFIG_INIT_STEP}` - Pasos de inicialización por perfil
- `{SCENARIO_*_NAME}`, `{PRECONDITION_*}`, `{ACTION}`, `{EXPECTED_RESULT_*}`

**Output:** `tests/features/{US_ID}-{name}.feature`

**Ejemplos:** Ver `bdd/examples/{profile}.feature` para versiones generadas por perfil.

---

### 2. Planning Templates

**Directorio:** `templates/planning/`

#### `implementation-plan.md`

Template para generar el plan de implementación detallado de una historia de usuario.

**Descripción:** Documento markdown con tareas, componentes, tests, dependencias y checklist de progreso.

**Variables principales:**
- `{US_ID}`, `{US_TITLE}`, `{PRIORITY}`, `{STORY_POINTS}`, `{PRODUCT}`
- `{COMPONENT_*_NAME}`, `{COMPONENT_*_TYPE}`, `{COMPONENT_*_PATH}`, `{COMPONENT_*_TIME}`
- `{TEST_FILE_PATTERN}` - Nombres de tests unitarios por perfil
- `{UNIT_TESTS_TIME}`, `{INTEGRATION_TESTS_TIME}`

**Snippets:**
- `{SNIPPET:integration_checklist}` - Checklist de integración específica por stack

**Output:** `docs/plans/{US_ID}-plan.md`

**Ejemplos:** Ver `planning/examples/{profile}.md`

---

### 3. Testing Templates

**Directorio:** `templates/testing/`

#### `test-unit.py`

Template para generar estructura de tests unitarios usando pytest.

**Descripción:** Archivo Python con clases de tests organizadas (TestCreacion, TestMetodos, TestValidacion, TestIntegracion) y fixtures específicas del framework.

**Variables principales:**
- `{COMPONENT_NAME}`, `{CLASS_NAME}`, `{MODULE_PATH}`
- `{TEST_CLASS_ORGANIZATION_COMMENT}` - Descripción de organización de tests por perfil

**Snippets:**
- `{SNIPPET:test_imports}` - Imports específicos del framework de testing
- `{SNIPPET:test_signals_class}` - Clase TestSignals (solo PyQt)
- `{SNIPPET:test_integration_class}` - Clase TestIntegracion por stack
- `{SNIPPET:test_fixtures}` - Fixtures pytest específicas

**Output:** `tests/test_{component}.py`

**Ejemplos:** Ver `testing/examples/{profile}.py`

#### `test-integration.py` (Opcional - BONUS)

Template para tests de integración end-to-end.

---

### 4. Reporting Templates

**Directorio:** `templates/reporting/`

#### `implementation-report.md`

Template para generar el reporte final de implementación de una historia de usuario.

**Descripción:** Documento markdown exhaustivo con código implementado, tests, métricas de calidad (Pylint, CC, MI, Coverage), arquitectura, lecciones aprendidas y tiempo invertido.

**Variables principales:**
- Todas las variables de US y componentes
- `{ARCHITECTURE_DESCRIPTION}` - Descripción del patrón aplicado por perfil
- Variables de métricas: `{PYLINT_SCORE}`, `{CC_AVG}`, `{MI_AVG}`, `{COVERAGE}`
- Variables de tiempo: `{*_EST}`, `{*_ACTUAL}`, `{*_DIFF}`, `{ESTIMATION_ACCURACY}`

**Snippets:**
- `{SNIPPET:architecture_code_blocks}` - Código de integración específico por stack
- `{SNIPPET:manual_testing_specifics}` - Testing manual relevante por perfil

**Output:** `docs/reports/{US_ID}-report.md`

**Ejemplos:** Ver `reporting/examples/{profile}.md`

---

## Sistema de Variables

### Variables Disponibles

| Categoría | Variable | Descripción | Ejemplo |
|-----------|----------|-------------|---------|
| **User Story** | `{US_ID}` | ID de historia de usuario | `US-001` |
| | `{US_TITLE}` | Título de la historia | `Implementar panel display` |
| | `{USER_ROLE}` | Rol del usuario | `usuario` |
| | `{USER_WANT}` | Lo que quiere el usuario | `ver el display de temperatura` |
| | `{USER_BENEFIT}` | Beneficio esperado | `monitorear el termostato` |
| | `{PRIORITY}` | Prioridad | `Alta`, `Media`, `Baja` |
| | `{STORY_POINTS}` | Puntos estimados | `5` |
| | `{PRODUCT}` | Nombre del producto | `app_termostato` |
| **Componente** | `{COMPONENT_NAME}` | Nombre del componente | `display`, `user_service` |
| | `{COMPONENT_TYPE}` | Tipo de componente | `Panel`, `Service`, `View` |
| | `{COMPONENT_PATH}` | Ruta del archivo | `app/presentacion/paneles/display/` |
| | `{CLASS_NAME}` | Nombre de clase principal | `DisplayController` |
| | `{MODULE_PATH}` | Path para imports | `app.presentacion.paneles.display` |
| **Arquitectura** | `{ARCHITECTURE_PATTERN}` | Patrón arquitectónico | `mvc`, `layered`, `mvt` |
| | `{ARCHITECTURE_DESCRIPTION}` | Descripción del patrón aplicado | (multilinea, por perfil) |
| **Testing** | `{TEST_FRAMEWORK}` | Framework de testing | `pytest-qt`, `pytest`, `pytest-asyncio` |
| | `{TEST_FILE_PATTERN}` | Patrón de nombres de tests | (multilinea, por perfil) |
| | `{TEST_CLASS_ORGANIZATION_COMMENT}` | Organización de clases de tests | (multilinea, por perfil) |
| **BDD** | `{FEATURE_TITLE}` | Título del feature | `Display de Temperatura` |
| | `{APP_INIT_STEP}` | Paso de inicialización de app | (por perfil) |
| | `{CONFIG_INIT_STEP}` | Paso de carga de config | (por perfil) |
| | `{SCENARIO_*_NAME}` | Nombre de escenario | `Mostrar temperatura actual` |
| | `{PRECONDITION_*}` | Precondición Given | `el termostato está conectado` |
| | `{ACTION}` | Acción When | `el usuario abre la aplicación` |
| | `{EXPECTED_RESULT_*}` | Resultado Then | `se muestra la temperatura` |
| **Fechas** | `{START_DATE}` | Fecha de inicio | `2026-02-14` |
| | `{END_DATE}` | Fecha de fin | `2026-02-15` |
| | `{LAST_UPDATE}` | Última actualización | `2026-02-14 10:30` |
| | `{REPORT_DATE}` | Fecha del reporte | `2026-02-15` |
| **Tiempos** | `{COMPONENT_*_TIME}` | Estimación por componente | `30 min` |
| | `{UNIT_TESTS_TIME}` | Estimación tests unitarios | `1h` |
| | `{INTEGRATION_TESTS_TIME}` | Estimación tests integración | `30 min` |
| | `{TIME_SPENT}` | Tiempo real invertido | `2h 15min` |
| | `{*_EST}`, `{*_ACTUAL}`, `{*_DIFF}` | Estimado vs real por fase | `1h`, `1.2h`, `+0.2h` |
| **Métricas** | `{PYLINT_SCORE}` | Puntaje Pylint | `8.5` |
| | `{CC_AVG}` | Complejidad Ciclomática promedio | `6.2` |
| | `{MI_AVG}` | Índice de Mantenibilidad promedio | `65.3` |
| | `{COVERAGE}` | Cobertura de tests | `96` |
| **Estado** | `{CURRENT_STATE}` | Estado actual | `EN PROGRESO`, `COMPLETADO` |
| | `{COMPLETED_TASKS}` | Tareas completadas | `15` |
| | `{TOTAL_TASKS}` | Total de tareas | `20` |
| | `{PROGRESS_PERCENTAGE}` | Porcentaje de progreso | `75` |

### Variables Específicas por Perfil

Algunas variables tienen valores diferentes según el perfil activo:

| Variable | pyqt-mvc | fastapi-rest | flask-rest | flask-webapp | generic-python |
|----------|----------|--------------|------------|--------------|----------------|
| `{APP_INIT_STEP}` | la aplicación está iniciada | el servidor API está corriendo | el servidor Flask está corriendo | la aplicación web está corriendo | el módulo está importado |
| `{CONFIG_INIT_STEP}` | la configuración está cargada | las variables de entorno están configuradas | las variables de entorno están configuradas | la configuración de Flask está cargada | la configuración está inicializada |
| `{COMPONENT_TYPE}` | Panel, Modelo, Vista, Controlador | Service, Router, Schema | Service, Route, Model | View, Form, Model, Template | Module, Class, Function |
| `{TEST_FRAMEWORK}` | pytest-qt | pytest, pytest-asyncio | pytest | pytest | pytest |

---

## Sistema de Snippets

### ¿Qué son los Snippets?

Los **snippets** son bloques de código o texto que se insertan condicionalmente según el perfil activo. Permiten incluir secciones completas específicas de un stack sin contaminar el template base.

### Sintaxis

En los templates, los snippets se marcan con:

```
{SNIPPET:snippet_id}
```

Ejemplo en template:
```markdown
## Integración con Sistema

{SNIPPET:architecture_code_blocks}
```

### Snippets Disponibles

| Snippet ID | Template | Descripción | Perfiles |
|------------|----------|-------------|----------|
| `integration_checklist` | implementation-plan.md | Checklist de integración con el sistema | Todos |
| `architecture_code_blocks` | implementation-report.md | Bloques de código de integración (Factory, Router, etc.) | Todos |
| `manual_testing_specifics` | implementation-report.md | Secciones de testing manual específicas | Todos |
| `test_imports` | test-unit.py | Imports del framework de testing | Todos |
| `test_signals_class` | test-unit.py | Clase TestSignals para PyQt | Solo pyqt-mvc |
| `test_integration_class` | test-unit.py | Clase TestIntegracion específica | Todos |
| `test_fixtures` | test-unit.py | Fixtures pytest del framework | Todos |

### Cómo Funcionan

1. El skill `/implement-us` lee el template
2. Detecta placeholders `{SNIPPET:snippet_id}`
3. Carga el perfil activo desde `skills/implement-us/config.json`
4. Busca el snippet en `skills/implement-us/customizations/{profile}.json`
5. Reemplaza el placeholder con el contenido del snippet
6. Preserva la indentación del contexto

### Snippets Vacíos

Algunos snippets pueden estar vacíos para ciertos perfiles. Por ejemplo, `test_signals_class` solo contiene código para `pyqt-mvc`, en otros perfiles es una cadena vacía `""`.

---

## Uso de Templates

### Proceso de Generación

Cuando el skill `/implement-us` ejecuta una fase que genera un archivo:

1. **Leer template:** Carga el template correspondiente desde `templates/{category}/{name}.ext`
2. **Cargar configuración:** Lee `skills/implement-us/config.json` para obtener perfil activo y variables
3. **Cargar snippets:** Lee `skills/implement-us/customizations/{profile}.json` para snippets
4. **Reemplazar variables:** Busca y reemplaza todos los `{VARIABLE}` con sus valores
5. **Insertar snippets:** Busca y reemplaza todos los `{SNIPPET:id}` con su contenido
6. **Generar archivo:** Escribe el resultado en la ruta de destino

### Ejemplo de Generación

**Template:** `templates/bdd/scenario.feature`
```gherkin
Feature: {FEATURE_TITLE} ({US_ID})
  Como {USER_ROLE}
  Quiero {USER_WANT}
  Para {USER_BENEFIT}

  Background:
    Given {APP_INIT_STEP}
    And {CONFIG_INIT_STEP}
```

**Perfil activo:** `pyqt-mvc`

**Variables:**
- `{FEATURE_TITLE}` = "Display de Temperatura"
- `{US_ID}` = "US-001"
- `{USER_ROLE}` = "usuario"
- `{USER_WANT}` = "ver la temperatura actual"
- `{USER_BENEFIT}` = "monitorear el termostato"
- `{APP_INIT_STEP}` = "la aplicación está iniciada" (desde perfil pyqt-mvc)
- `{CONFIG_INIT_STEP}` = "la configuración está cargada" (desde perfil pyqt-mvc)

**Output:** `tests/features/US-001-display.feature`
```gherkin
Feature: Display de Temperatura (US-001)
  Como usuario
  Quiero ver la temperatura actual
  Para monitorear el termostato

  Background:
    Given la aplicación está iniciada
    And la configuración está cargada
```

---

## Ejemplos por Perfil

Cada subdirectorio `examples/` contiene versiones **pre-generadas** de los templates para los 5 perfiles soportados:

### Estructura de Examples

```
templates/
├── bdd/examples/
│   ├── pyqt-mvc.feature
│   ├── fastapi-rest.feature
│   ├── flask-rest.feature
│   ├── flask-webapp.feature
│   └── generic-python.feature
├── planning/examples/
│   ├── pyqt-mvc.md
│   ├── fastapi-rest.md
│   ├── flask-rest.md
│   ├── flask-webapp.md
│   └── generic-python.md
├── testing/examples/
│   ├── pyqt-mvc.py
│   ├── fastapi-rest.py
│   ├── flask-rest.py
│   ├── flask-webapp.py
│   └── generic-python.py
└── reporting/examples/
    ├── pyqt-mvc.md
    ├── fastapi-rest.md
    ├── flask-rest.md
    ├── flask-webapp.md
    └── generic-python.md
```

### Propósito de los Ejemplos

- **Referencia rápida:** Ver cómo se ve el output final para cada stack
- **Validación:** Verificar que los snippets y variables funcionan correctamente
- **Documentación:** Mostrar a usuarios cómo adaptar templates a su proyecto
- **Testing:** Validar sintaxis y completitud de templates generados

---

## Personalización

### Modificar Templates Existentes

Los templates son archivos de texto que puedes editar directamente:

1. Navegar a `templates/{category}/{template_name}`
2. Editar el archivo (agregar variables, cambiar estructura, etc.)
3. Actualizar ejemplos en `examples/` si es necesario
4. Regenerar archivos con `/implement-us` para validar

### Agregar Nuevas Variables

Para agregar una variable nueva:

1. **Definir en perfil:** Agregar a `skills/implement-us/customizations/{profile}.json`
   ```json
   {
     "variables": {
       "MY_NEW_VARIABLE": "valor para este perfil"
     }
   }
   ```

2. **Usar en template:** Agregar placeholder `{MY_NEW_VARIABLE}` donde corresponda

3. **Documentar:** Actualizar tabla de variables en este README

### Agregar Nuevos Snippets

Para agregar un snippet nuevo:

1. **Definir en perfiles:** Agregar a todos los perfiles en `customizations/`
   ```json
   {
     "snippets": {
       "my_snippet": "contenido del snippet para este perfil"
     }
   }
   ```

2. **Usar en template:** Agregar `{SNIPPET:my_snippet}` donde corresponda

3. **Documentar:** Actualizar tabla de snippets en este README

### Crear Templates Nuevos

Para agregar un template completamente nuevo:

1. **Crear archivo:** En la categoría apropiada (o crear nueva categoría)
   ```bash
   # Ejemplo: nuevo template para ADR
   touch templates/planning/architecture-decision-record.md
   ```

2. **Definir estructura:** Escribir template con variables `{VARIABLE}` y snippets `{SNIPPET:id}`

3. **Crear snippets:** Definir snippets necesarios en todos los perfiles

4. **Generar ejemplos:** Crear versión para cada perfil en `examples/`

5. **Documentar:** Agregar sección en este README

6. **Integrar en skill:** Modificar `/implement-us` para usar el template en la fase apropiada

### Adaptar a Stack No Soportado

Si tu proyecto usa un stack no incluido (ej. Django, NestJS, etc.):

1. **Crear perfil nuevo:** Duplicar perfil similar en `skills/implement-us/customizations/`
   ```bash
   cp skills/implement-us/customizations/generic-python.json \
      skills/implement-us/customizations/my-stack.json
   ```

2. **Personalizar variables:** Editar valores de variables en el nuevo perfil

3. **Personalizar snippets:** Adaptar snippets al stack (imports, código de integración, etc.)

4. **Validar:** Generar ejemplos y verificar que funcionan

5. **Configurar:** Actualizar `skills/implement-us/config.json` para usar el nuevo perfil

---

## Validación de Templates

### Checklist de Calidad

Al crear o modificar templates, validar:

- [ ] **Variables bien formadas:** Sintaxis `{VARIABLE_NAME}` en mayúsculas
- [ ] **Snippets bien formados:** Sintaxis `{SNIPPET:snippet_id}` en minúsculas
- [ ] **Todas las variables documentadas:** En tabla de este README
- [ ] **Todos los snippets documentados:** En tabla de este README
- [ ] **Ejemplos generados:** Para los 5 perfiles en `examples/`
- [ ] **Sintaxis válida:** Markdown, Python, Gherkin según corresponda
- [ ] **Código ejecutable:** Templates de Python deben generar código que pase pylint/pytest
- [ ] **Indentación preservada:** Snippets de código mantienen indentación correcta
- [ ] **Sin hardcoding:** No hay referencias específicas a un stack fuera de snippets

---

## Recursos Adicionales

### Documentación Relacionada

- **Análisis de Templates:** `docs/analysis/TICKET-030-analysis.md` - Análisis exhaustivo de referencias específicas
- **Skill implement-us:** `skills/implement-us/skill.md` - Orquestador que usa estos templates
- **Perfiles:** `skills/implement-us/customizations/{profile}.json` - Definiciones de snippets y variables

### Ejemplos de Uso Real

- **Proyecto de ejemplo PyQt:** `examples/code/pyqt-calculator/` — Calculadora MVC ([tutorial](../docs/examples/pyqt-project.md))
- **Proyecto de ejemplo FastAPI:** `examples/code/fastapi-todo-api/` — TODO API ([tutorial](../docs/examples/fastapi-project.md))
- **Proyecto de ejemplo Flask REST:** `examples/code/flask-contacts-api/` — Contacts API ([tutorial](../docs/examples/flask-rest-api-project.md))
- **Proyecto de ejemplo Flask WebApp:** `examples/code/flask-blog-app/` — Blog App ([tutorial](../docs/examples/flask-webapp-project.md))
- **Proyecto de ejemplo CLI:** `examples/code/csv-tool/` — CSV Tool ([tutorial](../docs/examples/generic-python.md))

---

## Contribuir

Para contribuir con nuevos templates o mejoras:

1. Fork del repositorio
2. Crear branch: `git checkout -b feature/nuevo-template`
3. Agregar template + ejemplos + documentación
4. Commit: `git commit -m "feat(templates): agregar template para X"`
5. Push y crear Pull Request

---

**Versión:** 1.0
**Última actualización:** 2026-02-17
**Mantenido por:** Claude Dev Kit Team
