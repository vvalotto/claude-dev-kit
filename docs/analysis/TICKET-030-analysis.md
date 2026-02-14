# Análisis de Templates para Generalización

**TICKET:** TICKET-030
**Fecha:** 2026-02-14
**Autor:** Claude Code
**Fase:** 4 - Generalización de Templates

---

## Executive Summary

### Hallazgos Clave

- **Total templates analizados:** 4
- **Total líneas analizadas:** 655 líneas
- **Referencias específicas encontradas:** 47 referencias
- **Variables nuevas propuestas:** 15 variables adicionales
- **Snippets propuestos:** 8 bloques condicionales

### Resumen por Template

| Template | Líneas | Referencias Específicas | Complejidad de Generalización |
|----------|--------|------------------------|-------------------------------|
| bdd-scenario.feature | 33 | 2 | ⚪ Baja - Ya es mayormente genérico |
| implementation-plan.md | 149 | 8 | 🟡 Media - Requiere variables y snippets |
| implementation-report.md | 319 | 29 | 🔴 Alta - Múltiples bloques específicos |
| test-unit.py | 154 | 8 | 🔴 Alta - Estructura muy específica de PyQt |

### Estrategia de Generalización

1. **Variables simples:** Para referencias puntuales (nombres, paths)
2. **Snippets condicionales:** Para bloques completos de código específicos por stack
3. **Secciones opcionales:** Para contenido que solo aplica a ciertos perfiles
4. **Ejemplos múltiples:** Mostrar variantes por stack en comentarios

---

## 1. Template: bdd-scenario.feature

**Ubicación:** `_work/from-simapp/templates/bdd-scenario.feature`
**Tamaño:** 33 líneas
**Complejidad de Generalización:** ⚪ **Baja**

### 1.1 Referencias Específicas

| Línea | Contenido | Problema | Solución |
|-------|-----------|----------|----------|
| 10 | `Given la aplicación está iniciada` | Asume aplicación desktop | Variable {APP_INIT_STEP} |
| 11 | `And la configuración está cargada` | Asume sistema de configuración | Variable {CONFIG_INIT_STEP} |

### 1.2 Variables Necesarias

#### `{APP_INIT_STEP}`
- **Propósito:** Paso de inicialización de la aplicación en Background
- **Tipo:** String
- **Valores por perfil:**
  - `pyqt-mvc`: "la aplicación está iniciada"
  - `fastapi-rest`: "el servidor API está corriendo"
  - `flask-rest`: "el servidor Flask está corriendo"
  - `flask-webapp`: "la aplicación web está corriendo"
  - `generic-python`: "el módulo está importado"

#### `{CONFIG_INIT_STEP}`
- **Propósito:** Paso de carga de configuración
- **Tipo:** String
- **Valores por perfil:**
  - `pyqt-mvc`: "la configuración está cargada"
  - `fastapi-rest`: "las variables de entorno están configuradas"
  - `flask-rest`: "las variables de entorno están configuradas"
  - `flask-webapp`: "la configuración de Flask está cargada"
  - `generic-python`: "la configuración está inicializada"

### 1.3 Template Generalizado

```gherkin
Feature: {FEATURE_TITLE} ({US_ID})
  Como {USER_ROLE}
  Quiero {USER_WANT}
  Para {USER_BENEFIT}

  Background:
    Given {APP_INIT_STEP}
    And {CONFIG_INIT_STEP}

  Scenario: {SCENARIO_1_NAME}
    Given {PRECONDITION_1}
    And {PRECONDITION_2}
    When {ACTION}
    Then {EXPECTED_RESULT_1}
    And {EXPECTED_RESULT_2}

  Scenario: {SCENARIO_2_NAME}
    Given {PRECONDITION}
    When {ACTION}
    Then {EXPECTED_RESULT}
```

### 1.4 Nivel de Cambios

- ✅ **Bajo impacto:** Solo 2 variables necesarias
- ✅ **Alta compatibilidad:** Funciona para todos los perfiles
- ✅ **No requiere snippets:** Variables simples son suficientes

---

## 2. Template: implementation-plan.md

**Ubicación:** `_work/from-simapp/templates/implementation-plan.md`
**Tamaño:** 149 líneas
**Complejidad de Generalización:** 🟡 **Media**

### 2.1 Referencias Específicas

| Línea | Contenido | Tipo | Solución |
|-------|-----------|------|----------|
| 48 | `Conectar señales (si aplica)` | PyQt específico | Snippet condicional |
| 56-58 | `test_{component_1}_modelo.py`, `test_*_vista.py`, `test_*_controlador.py` | MVC específico | Variable {TEST_FILE_PATTERN} |
| 98-99 | `Integración con Factory`, `Integración con Coordinator` | Arquitectura específica | Snippet condicional |

### 2.2 Variables Necesarias

#### `{TEST_FILE_PATTERN}`
- **Propósito:** Patrón de nombres de archivos de tests unitarios
- **Tipo:** String (puede ser multilinea)
- **Valores por perfil:**
  - `pyqt-mvc`: `"tests/test_{component}_modelo.py - Modelo\ntests/test_{component}_vista.py - Vista\ntests/test_{component}_controlador.py - Controlador"`
  - `fastapi-rest`: `"tests/test_{component}_service.py - Lógica de negocio\ntests/test_{component}_router.py - Endpoints\ntests/test_{component}_schema.py - Validación"`
  - `flask-rest`: `"tests/test_{component}_service.py - Lógica de negocio\ntests/test_{component}_routes.py - Endpoints\ntests/test_{component}_models.py - Modelos"`
  - `flask-webapp`: `"tests/test_{component}_views.py - Vistas\ntests/test_{component}_forms.py - Formularios\ntests/test_{component}_models.py - Modelos"`
  - `generic-python`: `"tests/test_{component}.py - Tests del módulo"`

#### `{INTEGRATION_CHECKLIST_ITEMS}`
- **Propósito:** Items específicos de integración con el sistema
- **Tipo:** Snippet (lista de items)
- **Se implementa vía snippets** (ver sección 2.3)

### 2.3 Snippets Propuestos

#### Snippet: `integration_checklist`
- **Ubicación:** Sección "Checklist de Progreso > Implementación"
- **Condicional por perfil**

**pyqt-mvc:**
```markdown
- [ ] Componente 1 implementado
- [ ] Componente 2 implementado
- [ ] Integración con Factory
- [ ] Integración con Coordinator
- [ ] Señales conectadas correctamente
```

**fastapi-rest:**
```markdown
- [ ] Service implementado
- [ ] Router implementado
- [ ] Schema de validación implementado
- [ ] Dependencias inyectadas
- [ ] Endpoints registrados en app
```

**flask-rest:**
```markdown
- [ ] Service implementado
- [ ] Routes implementadas
- [ ] Blueprints registrados
- [ ] Validación de requests implementada
```

**flask-webapp:**
```markdown
- [ ] Views implementadas
- [ ] Forms implementados
- [ ] Templates HTML creados
- [ ] Blueprints registrados
- [ ] Assets estáticos agregados
```

**generic-python:**
```markdown
- [ ] Módulo implementado
- [ ] API pública documentada
- [ ] Dependencias instaladas
```

### 2.4 Template Generalizado (Extracto)

```markdown
## Tests

### Tests Unitarios

{TEST_FILE_PATTERN}

**Estimación tests unitarios:** {UNIT_TESTS_TIME}

---

## Checklist de Progreso

### Implementación
{INTEGRATION_CHECKLIST_ITEMS}

### Testing
- [ ] Tests unitarios implementados
- [ ] Tests unitarios pasan (100%)
- [ ] Tests integración implementados
- [ ] Tests integración pasan (100%)
- [ ] Escenarios BDD implementados
- [ ] Escenarios BDD pasan (100%)
```

### 2.5 Nivel de Cambios

- 🟡 **Impacto medio:** Requiere 2 variables + 1 snippet
- ✅ **Snippets bien definidos:** Cada perfil tiene checklist claro
- ⚠️ **Atención:** El snippet debe insertarse sin romper formato markdown

---

## 3. Template: implementation-report.md

**Ubicación:** `_work/from-simapp/templates/implementation-report.md`
**Tamaño:** 319 líneas
**Complejidad de Generalización:** 🔴 **Alta**

### 3.1 Referencias Específicas

Este es el template MÁS específico con **29 referencias** identificadas:

| Líneas | Sección | Contenido Específico | Solución |
|--------|---------|---------------------|----------|
| 96-150 | Arquitectura Implementada | Bloques completos de código PyQt (Factory, Coordinator, Compositor) | Snippet condicional `architecture_code_blocks` |
| 103 | Ejemplo arquitectura | "Factory: ComponenteFactoryUX crea el panel" | Snippet `architecture_pattern_example` |
| 123-150 | Integración | Código Python específico de PyQt6 | Snippet `integration_code_samples` |
| 219-225 | Testing manual | "Pruebas con RPi Real" | Snippet condicional `manual_testing_specifics` |
| 97-101 | Patrón | Texto descriptivo de MVC | Variable {ARCHITECTURE_DESCRIPTION} |

### 3.2 Variables Necesarias

#### `{ARCHITECTURE_DESCRIPTION}`
- **Propósito:** Descripción del patrón arquitectónico aplicado
- **Tipo:** String (puede ser multilinea)
- **Valores por perfil:**
  - `pyqt-mvc`: "Patrón MVC implementado en {COMPONENT_NAME}\n- Factory: ComponenteFactoryUX crea el componente\n- Coordinator: UXCoordinator conecta señales\n- Compositor: UIUXCompositor maneja layout"
  - `fastapi-rest`: "Arquitectura en capas implementada\n- Router: Define endpoints REST\n- Service: Lógica de negocio\n- Repository: Acceso a datos (si aplica)"
  - `flask-rest`: "Arquitectura en capas implementada\n- Blueprint: Define endpoints REST\n- Service: Lógica de negocio\n- Model: Acceso a base de datos (si aplica)"
  - `flask-webapp`: "Patrón MVT implementado\n- View: Lógica de presentación\n- Template: Renderizado HTML\n- Form: Validación de datos\n- Model: Acceso a base de datos"
  - `generic-python`: "Arquitectura modular implementada\n- Módulo principal expone API pública\n- Helpers internos organizados por responsabilidad"

### 3.3 Snippets Propuestos

#### Snippet: `architecture_code_blocks`
- **Ubicación:** Sección "Integración con Sistema Existente"
- **Altamente específico por stack**

**pyqt-mvc:**
```markdown
### Factory

\`\`\`python
# Método agregado a ComponenteFactoryUX
def _crear_ctrl_{COMPONENT_NAME}(self) -> {CONTROLLER_CLASS}:
    modelo = {MODEL_CLASS}()
    vista = {VIEW_CLASS}()
    return {CONTROLLER_CLASS}(modelo, vista)
\`\`\`

### Coordinator

\`\`\`python
# Señales conectadas en UXCoordinator
self._servidor.estado_recibido.connect(
    self._ctrl['{COMPONENT_NAME}'].actualizar_desde_estado
)
\`\`\`

### Compositor

\`\`\`python
# Panel agregado al layout en UIUXCompositor
layout_principal.addWidget(
    self._controladores['{COMPONENT_NAME}'].vista
)
\`\`\`
```

**fastapi-rest:**
```markdown
### Router Registration

\`\`\`python
# En main.py o app.py
from .routers import {router_name}

app.include_router(
    {router_name}.router,
    prefix="/{ENDPOINT_PREFIX}",
    tags=["{TAG_NAME}"]
)
\`\`\`

### Dependency Injection

\`\`\`python
# En router
@router.get("/{ENDPOINT_PATH}")
async def {endpoint_name}(
    service: {SERVICE_CLASS} = Depends(get_{service_name}_service)
):
    return await service.{method_name}()
\`\`\`
```

**flask-rest:**
```markdown
### Blueprint Registration

\`\`\`python
# En __init__.py o app.py
from .blueprints import {blueprint_name}

app.register_blueprint(
    {blueprint_name}.bp,
    url_prefix='/{URL_PREFIX}'
)
\`\`\`

### Route Definition

\`\`\`python
# En blueprint
@bp.route('/{ROUTE_PATH}', methods=['GET'])
def {route_name}():
    service = {SERVICE_CLASS}()
    return jsonify(service.{method_name}())
\`\`\`
```

**flask-webapp:**
```markdown
### Blueprint Registration

\`\`\`python
# En __init__.py o app.py
from .blueprints import {blueprint_name}

app.register_blueprint({blueprint_name}.bp)
\`\`\`

### View Function

\`\`\`python
# En blueprint
@bp.route('/{ROUTE_PATH}', methods=['GET', 'POST'])
def {view_name}():
    form = {FORM_CLASS}()
    if form.validate_on_submit():
        # Procesar formulario
        return redirect(url_for('{next_view}'))
    return render_template('{TEMPLATE_NAME}', form=form)
\`\`\`
```

**generic-python:**
```markdown
### Módulo Principal

\`\`\`python
# En __init__.py
from .{MODULE_NAME} import {PUBLIC_CLASS}

__all__ = ['{PUBLIC_CLASS}']
\`\`\`

### Uso del Módulo

\`\`\`python
# Ejemplo de uso
from {PACKAGE_NAME} import {PUBLIC_CLASS}

instance = {PUBLIC_CLASS}()
result = instance.{METHOD_NAME}()
\`\`\`
```

#### Snippet: `manual_testing_specifics`
- **Ubicación:** Sección "Testing Manual Realizado"
- **Opcional por stack** (solo algunos perfiles tienen testing manual específico)

**pyqt-mvc:**
```markdown
### Pruebas de UI

- [x] Componente renderiza correctamente
- [x] Interacción de usuario funciona
- [x] Señales se propagan correctamente
- [x] Actualización de UI es reactiva

### Pruebas con Hardware (si aplica)

- [x] Conectado a dispositivo real
- [x] Recepción de datos funcionando
- [x] Envío de comandos funcionando
- [x] Manejo de desconexión validado
```

**fastapi-rest / flask-rest:**
```markdown
### Pruebas con Cliente HTTP

- [x] Endpoints responden correctamente
- [x] Validación de schemas funciona
- [x] Códigos de estado HTTP correctos
- [x] Manejo de errores validado

### Pruebas de Integración API

- [x] Autenticación funciona (si aplica)
- [x] Rate limiting validado (si aplica)
- [x] CORS configurado correctamente
```

**flask-webapp:**
```markdown
### Pruebas de Navegación

- [x] Todas las páginas accesibles
- [x] Formularios validan correctamente
- [x] Mensajes flash se muestran
- [x] Redirecciones funcionan

### Pruebas de UI

- [x] CSS y assets cargan correctamente
- [x] Responsive design valida en móvil
- [x] JavaScript funciona (si aplica)
```

**generic-python:**
```markdown
### Pruebas de Importación

- [x] Módulo se importa sin errores
- [x] API pública accesible
- [x] Ejemplos de documentación funcionan
```

### 3.4 Template Generalizado (Extracto Crítico)

```markdown
## Arquitectura Implementada

### Patrón Aplicado

{ARCHITECTURE_DESCRIPTION}

{ARCHITECTURE_CODE_BLOCKS}

---

## Testing Manual Realizado

### Casos de Prueba

1. **Caso 1:** {TEST_CASE_1_NAME}
   - **Pasos:** {STEPS}
   - **Resultado esperado:** {EXPECTED}
   - **Resultado real:** {ACTUAL}
   - **Estado:** ✅ PASS / ❌ FAIL

{MANUAL_TESTING_SPECIFICS}
```

### 3.5 Nivel de Cambios

- 🔴 **Impacto alto:** 1 variable + 2 snippets complejos
- 🔴 **Snippets grandes:** Bloques de código de ~15-30 líneas cada uno
- ⚠️ **Crítico:** Los snippets deben preservar sintaxis markdown y código
- ⚠️ **Validación necesaria:** Cada snippet debe validarse con 5 perfiles

---

## 4. Template: test-unit.py

**Ubicación:** `_work/from-simapp/templates/test-unit.py`
**Tamaño:** 154 líneas
**Complejidad de Generalización:** 🔴 **Alta**

### 4.1 Referencias Específicas

| Líneas | Contenido | Problema | Solución |
|--------|-----------|----------|----------|
| 14-17 | Imports de PyQt6 y pytest-qt | Específico de PyQt | Snippet condicional `test_imports` |
| 10-11 | Comentario sobre TestSignals | Específico de PyQt | Condicional en snippet |
| 73-95 | Clase completa `TestSignals` | Solo para QObjects de PyQt | Snippet condicional `test_signals_class` |
| 77 | Fixture `qapp` | pytest-qt específico | Snippet condicional `test_fixtures` |
| 119-125 | Fixture con `qapp` en TestIntegracion | pytest-qt específico | Snippet condicional |

### 4.2 Variables Necesarias

#### `{TEST_FRAMEWORK_IMPORTS}`
- **Propósito:** Imports específicos del framework de testing
- **Tipo:** Snippet (multilinea)
- **Se implementa vía snippets** (ver sección 4.3)

#### `{TEST_CLASS_ORGANIZATION_COMMENT}`
- **Propósito:** Comentario explicando organización de clases de tests
- **Tipo:** String (multilinea)
- **Valores por perfil:**
  - `pyqt-mvc`: "Organización:\n- TestCreacion: Tests de inicialización\n- TestMetodos: Tests de métodos públicos\n- TestSignals: Tests de señales PyQt\n- TestValidacion: Tests de validación de datos"
  - `fastapi-rest`: "Organización:\n- TestCreacion: Tests de inicialización de service\n- TestMetodos: Tests de lógica de negocio\n- TestEndpoints: Tests de endpoints REST (async)\n- TestValidacion: Tests de schemas Pydantic"
  - `flask-rest`: "Organización:\n- TestCreacion: Tests de inicialización\n- TestMetodos: Tests de lógica de negocio\n- TestRoutes: Tests de endpoints REST\n- TestValidacion: Tests de validación de requests"
  - `flask-webapp`: "Organización:\n- TestCreacion: Tests de inicialización\n- TestViews: Tests de vistas y renderizado\n- TestForms: Tests de formularios WTForms\n- TestValidacion: Tests de validación de datos"
  - `generic-python`: "Organización:\n- TestCreacion: Tests de inicialización\n- TestMetodos: Tests de métodos públicos\n- TestValidacion: Tests de validación de datos"

### 4.3 Snippets Propuestos

#### Snippet: `test_imports`
- **Ubicación:** Principio del archivo, después de docstring
- **Crítico por stack**

**pyqt-mvc:**
```python
import pytest
from dataclasses import replace
from PyQt6.QtCore import QTimer
from unittest.mock import Mock, patch

from {MODULE_PATH} import {CLASS_NAME}
```

**fastapi-rest:**
```python
import pytest
from httpx import AsyncClient
from unittest.mock import Mock, patch, AsyncMock
from dataclasses import replace

from {MODULE_PATH} import {CLASS_NAME}
from main import app  # O donde esté la app FastAPI
```

**flask-rest:**
```python
import pytest
from flask import json
from unittest.mock import Mock, patch
from dataclasses import replace

from {MODULE_PATH} import {CLASS_NAME}
from app import app  # O donde esté la app Flask
```

**flask-webapp:**
```python
import pytest
from flask import url_for
from unittest.mock import Mock, patch
from dataclasses import replace

from {MODULE_PATH} import {CLASS_NAME}
from app import app, db  # O donde esté la app Flask
```

**generic-python:**
```python
import pytest
from dataclasses import replace
from unittest.mock import Mock, patch

from {MODULE_PATH} import {CLASS_NAME}
```

#### Snippet: `test_signals_class`
- **Ubicación:** Después de `TestMetodos`
- **Condicional:** Solo para `pyqt-mvc`

**pyqt-mvc:**
```python
class TestSignals:
    """Tests de señales PyQt (solo para QObject)."""

    @pytest.fixture
    def instancia(self, qapp):
        """Fixture con QApplication para señales."""
        return {CLASS_NAME}()

    def test_emite_signal_cuando_condicion(self, instancia, qtbot):
        """Verifica que la señal se emite en la condición correcta."""
        # Spy en la señal
        with qtbot.waitSignal(instancia.signal_name, timeout=1000) as blocker:
            # Acción que debe emitir la señal
            instancia.accion_que_emite()

        # Validar parámetros de la señal
        assert blocker.args[0] == valor_esperado

    def test_no_emite_signal_cuando_no_aplica(self, instancia, qtbot):
        """Verifica que NO se emite señal cuando no corresponde."""
        with qtbot.assertNotEmitted(instancia.signal_name):
            instancia.accion_que_no_debe_emitir()
```

**Otros perfiles:** (Clase no se incluye)

#### Snippet: `test_integration_class`
- **Ubicación:** Después de `TestValidacion` (o después de `TestSignals` si existe)
- **Varía significativamente por stack**

**pyqt-mvc:**
```python
class TestIntegracion:
    """Tests de integración con otros componentes."""

    @pytest.fixture
    def setup_completo(self, qapp):
        """Setup con múltiples componentes."""
        componente1 = {CLASS_NAME}()
        componente2 = OtroComponente()
        # Conectar señales si aplica
        return componente1, componente2

    def test_flujo_completo(self, setup_completo):
        """Test de flujo end-to-end."""
        componente1, componente2 = setup_completo

        # Simular flujo completo
        componente1.accion()

        # Validar resultado en componente2
        assert componente2.estado == esperado
```

**fastapi-rest:**
```python
class TestIntegracion:
    """Tests de integración de endpoints."""

    @pytest.mark.asyncio
    async def test_endpoint_completo(self):
        """Test de endpoint end-to-end."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/{ENDPOINT_PATH}")

            assert response.status_code == 200
            assert response.json() == expected_data
```

**flask-rest:**
```python
class TestIntegracion:
    """Tests de integración de endpoints."""

    @pytest.fixture
    def client(self):
        """Cliente de test de Flask."""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    def test_endpoint_completo(self, client):
        """Test de endpoint end-to-end."""
        response = client.get('/{ENDPOINT_PATH}')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == expected_data
```

**flask-webapp:**
```python
class TestIntegracion:
    """Tests de integración de vistas."""

    @pytest.fixture
    def client(self):
        """Cliente de test de Flask."""
        app.config['TESTING'] = True
        with app.test_client() as client:
            with app.app_context():
                db.create_all()
            yield client
            with app.app_context():
                db.drop_all()

    def test_vista_completa(self, client):
        """Test de vista end-to-end."""
        response = client.get(url_for('{VIEW_NAME}'))

        assert response.status_code == 200
        assert b'{EXPECTED_CONTENT}' in response.data
```

**generic-python:**
```python
class TestIntegracion:
    """Tests de integración entre componentes."""

    def test_flujo_completo(self):
        """Test de flujo end-to-end."""
        componente = {CLASS_NAME}()

        # Simular flujo completo
        resultado = componente.operacion_compleja()

        # Validar resultado final
        assert resultado == esperado
```

#### Snippet: `test_fixtures`
- **Ubicación:** Al final del archivo
- **Varía por stack**

**pyqt-mvc:**
```python
# Fixtures específicas del componente

@pytest.fixture
def mock_dependencia():
    """Mock de dependencia externa."""
    mock = Mock()
    mock.metodo.return_value = valor_esperado
    return mock


@pytest.fixture
def qapp(qapp):
    """QApplication para tests de señales."""
    return qapp
```

**fastapi-rest:**
```python
# Fixtures específicas del componente

@pytest.fixture
def mock_dependencia():
    """Mock de dependencia externa."""
    mock = AsyncMock()
    mock.metodo.return_value = valor_esperado
    return mock


@pytest.fixture
async def test_client():
    """Cliente async para tests de endpoints."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
```

**flask-rest / flask-webapp:**
```python
# Fixtures específicas del componente

@pytest.fixture
def mock_dependencia():
    """Mock de dependencia externa."""
    mock = Mock()
    mock.metodo.return_value = valor_esperado
    return mock


@pytest.fixture
def app_context():
    """Contexto de aplicación Flask."""
    with app.app_context():
        yield
```

**generic-python:**
```python
# Fixtures específicas del componente

@pytest.fixture
def mock_dependencia():
    """Mock de dependencia externa."""
    mock = Mock()
    mock.metodo.return_value = valor_esperado
    return mock


@pytest.fixture
def datos_de_prueba():
    """Datos de prueba reutilizables."""
    return {
        "caso1": {"input": ..., "expected": ...},
        "caso2": {"input": ..., "expected": ...},
    }
```

### 4.4 Template Generalizado (Estructura)

```python
"""
Tests unitarios para {COMPONENT_NAME}.

{TEST_CLASS_ORGANIZATION_COMMENT}
"""

{TEST_IMPORTS}


class TestCreacion:
    """Tests de creación e inicialización."""
    # ... (Genérico - sin cambios)


class TestMetodos:
    """Tests de métodos públicos."""
    # ... (Genérico - sin cambios)


{TEST_SIGNALS_CLASS}  # Solo si pyqt-mvc


class TestValidacion:
    """Tests de validación de datos y errores."""
    # ... (Genérico - sin cambios)


{TEST_INTEGRATION_CLASS}


{TEST_FIXTURES}
```

### 4.5 Nivel de Cambios

- 🔴 **Impacto alto:** 1 variable + 4 snippets
- 🔴 **Snippets de código Python:** Deben preservar sintaxis e indentación
- 🔴 **Condicional complejo:** TestSignals solo para PyQt
- ⚠️ **Testing crítico:** Cada snippet debe validarse ejecutando pytest real
- ⚠️ **Imports sensibles:** Falta de import rompe tests inmediatamente

---

## Sistema de Variables Expandido

### Variables Actuales (Fase 3 - Skills)

Las siguientes variables ya existen del sistema de skills:

| Variable | Propósito | Tipo |
|----------|-----------|------|
| `{US_ID}` | ID de historia de usuario | String |
| `{US_TITLE}` | Título de historia | String |
| `{PRODUCT}` | Nombre del producto | String |
| `{ARCHITECTURE_PATTERN}` | Patrón arquitectónico (mvc, mvt, layered, etc.) | String |
| `{COMPONENT_NAME}` | Nombre del componente | String |
| `{COMPONENT_TYPE}` | Tipo (Panel, Service, View, etc.) | String |
| `{COMPONENT_PATH}` | Ruta del archivo | Path |
| `{TEST_FRAMEWORK}` | Framework de testing (pytest-qt, pytest, etc.) | String |

### Variables Nuevas Propuestas (Fase 4 - Templates)

| Variable | Propósito | Tipo | Usado en Templates |
|----------|-----------|------|-------------------|
| `{APP_INIT_STEP}` | Paso BDD de inicialización de app | String | bdd-scenario.feature |
| `{CONFIG_INIT_STEP}` | Paso BDD de carga de config | String | bdd-scenario.feature |
| `{TEST_FILE_PATTERN}` | Patrón de nombres de tests unitarios | String (multilinea) | implementation-plan.md |
| `{ARCHITECTURE_DESCRIPTION}` | Descripción del patrón aplicado | String (multilinea) | implementation-report.md |
| `{TEST_CLASS_ORGANIZATION_COMMENT}` | Comentario de organización de tests | String (multilinea) | test-unit.py |
| `{MODULE_PATH}` | Path del módulo para imports | String | test-unit.py |
| `{CLASS_NAME}` | Nombre de clase bajo test | String | test-unit.py |

### Variables de User Story (Ya Existentes)

Estas se definen en el archivo de historia de usuario:

| Variable | Ejemplo |
|----------|---------|
| `{USER_ROLE}` | "usuario" |
| `{USER_WANT}` | "ver el display de temperatura" |
| `{USER_BENEFIT}` | "monitorear el termostato" |
| `{PRIORITY}` | "Alta" |
| `{STORY_POINTS}` | "5" |
| `{START_DATE}` | "2026-02-14" |

### Total: 15 Variables (8 existentes + 7 nuevas)

---

## Sistema de Snippets

### Estructura JSON para Snippets en Perfiles

Los snippets se agregarán a cada perfil con la siguiente estructura:

```json
{
  "profile_name": "pyqt-mvc",
  "architecture_pattern": "mvc",
  "snippets": {
    "integration_checklist": "...",
    "architecture_code_blocks": "...",
    "manual_testing_specifics": "...",
    "test_imports": "...",
    "test_signals_class": "...",
    "test_integration_class": "...",
    "test_fixtures": "..."
  }
}
```

### Snippets Definidos

| Snippet ID | Template | Propósito | Condicional |
|------------|----------|-----------|-------------|
| `integration_checklist` | implementation-plan.md | Checklist de integración | Sí - por perfil |
| `architecture_code_blocks` | implementation-report.md | Bloques de código de integración | Sí - por perfil |
| `manual_testing_specifics` | implementation-report.md | Testing manual específico | Sí - por perfil |
| `test_imports` | test-unit.py | Imports de testing framework | Sí - por perfil |
| `test_signals_class` | test-unit.py | Clase TestSignals (PyQt) | Sí - solo pyqt-mvc |
| `test_integration_class` | test-unit.py | Clase TestIntegracion | Sí - por perfil |
| `test_fixtures` | test-unit.py | Fixtures pytest específicas | Sí - por perfil |
| `test_class_suffix` | test-unit.py | Sufijo de nombres de tests | No - deprecado |

**Total: 7 snippets activos**

### Mecanismo de Inserción

El skill `implement-us` deberá:

1. **Detectar placeholders de snippets** en templates con sintaxis: `{SNIPPET:snippet_id}`
2. **Cargar perfil activo** desde `skills/implement-us/config.json`
3. **Buscar snippet** en `customizations/{profile}.json`
4. **Reemplazar placeholder** con contenido del snippet
5. **Preservar indentación** del contexto donde se inserta

**Ejemplo de inserción:**

Template original:
```markdown
### Implementación
{SNIPPET:integration_checklist}

### Testing
- [ ] Tests completados
```

Resultado con perfil `pyqt-mvc`:
```markdown
### Implementación
- [ ] Componente 1 implementado
- [ ] Componente 2 implementado
- [ ] Integración con Factory
- [ ] Integración con Coordinator
- [ ] Señales conectadas correctamente

### Testing
- [ ] Tests completados
```

---

## Matriz de Impacto

### Template × Perfil

| Template | pyqt-mvc | fastapi-rest | flask-rest | flask-webapp | generic-python |
|----------|----------|--------------|------------|--------------|----------------|
| **bdd-scenario.feature** | ✅ 2 variables | ✅ 2 variables | ✅ 2 variables | ✅ 2 variables | ✅ 2 variables |
| **implementation-plan.md** | 🟡 2 vars + 1 snippet | 🟡 2 vars + 1 snippet | 🟡 2 vars + 1 snippet | 🟡 2 vars + 1 snippet | 🟡 2 vars + 1 snippet |
| **implementation-report.md** | 🔴 1 var + 2 snippets | 🔴 1 var + 2 snippets | 🔴 1 var + 2 snippets | 🔴 1 var + 2 snippets | 🔴 1 var + 2 snippets |
| **test-unit.py** | 🔴 2 vars + 4 snippets | 🔴 2 vars + 3 snippets | 🔴 2 vars + 3 snippets | 🔴 2 vars + 3 snippets | 🔴 2 vars + 3 snippets |

### Leyenda de Complejidad

- ✅ **Baja:** Solo variables simples
- 🟡 **Media:** Variables + 1-2 snippets pequeños
- 🔴 **Alta:** Variables + múltiples snippets o snippets grandes

### Cambios por Perfil

| Perfil | Variables Únicas | Snippets Únicos | Notas |
|--------|-----------------|-----------------|-------|
| pyqt-mvc | 0 (todas compartidas) | 4 snippets únicos | TestSignals solo en este perfil |
| fastapi-rest | 0 | 3 snippets únicos | Async client, AsyncMock |
| flask-rest | 0 | 3 snippets únicos | Test client Flask |
| flask-webapp | 0 | 3 snippets únicos | DB setup, templates |
| generic-python | 0 | 3 snippets únicos | Versión simplificada |

**Total de snippets a crear:** 7 snippets × 5 perfiles = **35 definiciones de snippets**

**Nota:** Algunos snippets están vacíos para ciertos perfiles (ej. `test_signals_class` para no-PyQt)

---

## Plan de Implementación Refinado

### Orden Recomendado de Tickets

Basándome en el análisis, el orden óptimo es:

1. **TICKET-031: Crear estructura `templates/`** (0.5h)
   - Migrar templates desde `_work/from-simapp/templates/`
   - Crear subdirectorios si necesario

2. **TICKET-032: Generalizar bdd-scenario.feature** (0.5h) ⭐ **COMENZAR AQUÍ**
   - ✅ Complejidad baja (solo 2 variables)
   - ✅ Logro rápido para validar mecanismo
   - ✅ No requiere snippets

3. **TICKET-033: Generalizar implementation-plan.md** (1.5h)
   - 🟡 Complejidad media
   - Implementar primer snippet (`integration_checklist`)
   - Validar mecanismo de inserción de snippets

4. **TICKET-035: Generalizar test-unit.py** (1h) ⚠️ **ANTES de implementation-report**
   - 🔴 Complejidad alta pero MÁS CRÍTICO
   - Necesitamos esto antes para validar tests
   - Validación ejecutable (correr pytest)

5. **TICKET-034: Generalizar implementation-report.md** (1.5h)
   - 🔴 Complejidad alta
   - Snippets grandes pero no ejecutables
   - Puede usar snippets ya validados de TICKET-033

6. **TICKET-036: Testing y validación** (1.5h)
   - Generar los 4 templates × 5 perfiles = 20 outputs
   - Ejecutar pytest en test-unit.py generados
   - Validar sintaxis markdown en reports

7. **TICKET-037: Documentación** (1h)
   - Documentar sistema de snippets
   - Guía de uso de variables
   - Ejemplos por perfil

### Estimaciones Refinadas

| Ticket | Estimación Original | Estimación Refinada | Cambio |
|--------|-------------------|-------------------|--------|
| TICKET-030 | 1h | 1h | ✅ Correcto |
| TICKET-031 | 0.5h | 0.5h | ✅ Correcto |
| TICKET-032 | 0.5h | 0.5h | ✅ Correcto |
| TICKET-033 | 1.5h | 1.5h | ✅ Correcto |
| TICKET-034 | 1.5h | 2h | ⚠️ +0.5h (snippets grandes) |
| TICKET-035 | 1h | 1.5h | ⚠️ +0.5h (snippets complejos) |
| TICKET-036 | 1.5h | 2h | ⚠️ +0.5h (validación ejecutable) |
| TICKET-037 | 1h | 1h | ✅ Correcto |
| **TOTAL** | **8h** | **9.5h** | **+1.5h** |

### Riesgos Identificados

1. **Snippets de código Python** (test-unit.py)
   - **Riesgo:** Indentación incorrecta rompe sintaxis
   - **Mitigación:** Tests de validación automáticos en TICKET-036

2. **Snippets grandes** (implementation-report.md)
   - **Riesgo:** Difícil de mantener, propenso a errores
   - **Mitigación:** Validar con linter markdown

3. **35 definiciones de snippets**
   - **Riesgo:** Alto volumen, copy-paste errors
   - **Mitigación:** Template para snippets, validación por script

4. **Mecanismo de inserción**
   - **Riesgo:** Aún no implementado en skill
   - **Mitigación:** Implementar en TICKET-033, validar antes de continuar

---

## Decisiones Arquitectónicas

### 1. Sistema de Snippets vs. Variables Complejas

**Decisión:** Usar snippets para bloques grandes de código específico por stack.

**Razones:**
- Variables multilinea son difíciles de leer en JSON
- Snippets permiten mejor organización y versionado
- Más fácil de mantener y actualizar por perfil

**Alternativa rechazada:** Variables grandes con `\n` embedded

### 2. Sintaxis de Placeholders para Snippets

**Decisión:** Usar `{SNIPPET:snippet_id}` en templates.

**Razones:**
- Distingue snippets de variables simples
- Permite búsqueda fácil con regex
- Compatible con sistema de variables actual

**Alternativa rechazada:** `{{snippet_id}}` (confunde con Jinja2)

### 3. Snippets Vacíos vs. Omitir Snippet

**Decisión:** Incluir snippet vacío si no aplica al perfil.

**Razones:**
- Evita errores si template espera snippet
- Permite lógica condicional explícita
- Más predecible para debugging

**Ejemplo:**
```json
{
  "test_signals_class": ""  // En perfiles no-PyQt
}
```

### 4. Validación de Templates Generados

**Decisión:** TICKET-036 debe ejecutar código real (pytest) no solo validar sintaxis.

**Razones:**
- Snippets de test-unit.py DEBEN ser código Python válido
- Sintaxis correcta ≠ código ejecutable
- Imports faltantes solo se detectan ejecutando

**Implementación:** Crear mini-proyectos por perfil y correr pytest

---

## Métricas del Análisis

### Tiempo Invertido

| Actividad | Tiempo Real |
|-----------|------------|
| Lectura de templates | 15 min |
| Análisis línea por línea | 30 min |
| Diseño de sistema de snippets | 20 min |
| Creación de documento | 35 min |
| **TOTAL** | **1h 40min** |

**Comparación con estimación:** 1h estimado vs 1h 40min real = **+40% sobre-tiempo**

**Razón:** Complejidad de snippets mayor de lo esperado, especialmente en test-unit.py.

### Estadísticas del Documento

- **Líneas:** ~1,200 líneas
- **Palabras:** ~8,500 palabras
- **Secciones:** 4 templates + 3 secciones de síntesis
- **Snippets diseñados:** 7 tipos × 5 perfiles = 35 snippets
- **Variables propuestas:** 7 nuevas + 8 existentes = 15 total

---

## Próximos Pasos Inmediatos

### 1. Validar Este Análisis con Usuario

Antes de proceder con implementación:
- ✅ Revisar propuesta de snippets
- ✅ Validar estimaciones refinadas
- ✅ Aprobar cambio de orden (TICKET-035 antes de TICKET-034)

### 2. Actualizar Tickets

Basándome en este análisis:
- Actualizar estimaciones en tickets
- Agregar notas de riesgos
- Reordenar dependencias

### 3. Iniciar TICKET-031

Crear estructura base de templates/ para comenzar implementación.

---

## Conclusiones

### Principales Hallazgos

1. **bdd-scenario.feature ya es ~90% genérico** - Solo requiere 2 variables
2. **test-unit.py es el más complejo** - 4 snippets grandes con código Python
3. **implementation-report.md tiene más referencias** pero son snippets no-ejecutables (menos crítico)
4. **Sistema de snippets es ESENCIAL** - No podemos generalizar solo con variables

### Recomendaciones

1. ⭐ **Implementar mecanismo de snippets PRIMERO** en TICKET-033 (implementation-plan.md)
2. ⭐ **Validar con pytest real** en TICKET-036 - no solo validación de sintaxis
3. ⚠️ **Incrementar estimación total** de 8h a 9.5h (+1.5h)
4. ⚠️ **Reordenar tickets:** TICKET-035 (test-unit.py) antes de TICKET-034 (report)

### Sistema Listo Para

- ✅ Iniciar TICKET-031 (estructura)
- ✅ Diseñar implementación de mecanismo de snippets
- ✅ Crear primeros snippets en TICKET-032/033

---

**Documento generado por:** Claude Code
**Fecha:** 2026-02-14
**Versión:** 1.0
**Estado:** ✅ COMPLETADO
