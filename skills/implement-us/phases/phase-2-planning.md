# Fase 2: Generación del Plan de Implementación

**Objetivo:** Crear un plan detallado de implementación basado en la arquitectura configurada del proyecto.

**Duración estimada:** 15-20 minutos

---

## Tracking

**Al inicio de la fase:**
```python
tracker.start_phase(2, "Generación del Plan de Implementación")
```

---

## Acción

Crear plan detallado basado en el patrón arquitectónico configurado (`{ARCHITECTURE_PATTERN}`).

**Template:** `.claude/templates/implementation-plan.md`

---

## Pasos de Generación del Plan

### 1. Identificar componentes a crear según arquitectura

Leer del archivo de configuración `.claude/skills/implement-us/config.json` la estructura de componentes:

```json
{
  "architecture_pattern": "{ARCHITECTURE_PATTERN}",
  "component_structure": {
    "layers": ["layer1", "layer2", "layer3"],
    "base_path": "{COMPONENT_PATH}"
  }
}
```

> **Componentes según patrón:**
>
> **MVC (PyQt, Desktop UI):**
> - Modelo (dataclass inmutable, lógica de negocio)
> - Vista (interfaz gráfica, QWidget)
> - Controlador (mediador entre modelo y vista)
> - Dependencias: Factory, Coordinator (si aplica)
>
> **Layered - FastAPI (Backend API async):**
> - Schema (Pydantic models para validación)
> - Service (lógica de negocio)
> - Repository (acceso a datos)
> - Router (endpoints HTTP)
> - Dependencias: Dependency Injection (FastAPI Depends)
>
> **Layered - Flask (Backend API sync):**
> - API (Flask blueprints, endpoints REST)
> - Domain (modelos de negocio, dataclasses)
> - Repository (ABC interfaces + implementaciones)
> - Mapper (conversión datos opcional)
> - Dependencias: Singleton pattern (Configurador)
>
> **Generic (Python genérico):**
> - Module (módulo principal)
> - Utils (utilidades si son necesarias)
> - Dependencias: Según necesidad del proyecto

### 2. Identificar dependencias y puntos de integración

- Componentes externos que la US necesita consumir
- Servicios o módulos existentes que deben integrarse
- Patrones del proyecto que deben aplicarse

### 3. Generar checklist de tareas

Organizar en secciones:
1. **Componentes principales** (según patrón arquitectónico)
2. **Integración** (conexión con componentes existentes)
3. **Tests** (unitarios, integración, BDD)
4. **Validación** (quality gates)

### 4. Estimar tiempo por tarea

Usar estimaciones estándar según tipo de componente y complejidad de la US.

---

## Ejemplos de Output por Stack

### Ejemplo 1: PyQt/MVC - Panel UI

```markdown
# Plan de Implementación: US-001 - Mostrar información de estado

**Patrón:** MVC
**Producto:** ux_monitor
**Estimación Total:** 2h 15min

## Componentes a Implementar

### 1. Panel Estado (MVC)
- [ ] app/presentacion/paneles/estado/modelo.py (10 min)
  - EstadoModelo: dataclass inmutable con datos del estado
  - Hereda de ModeloBase
- [ ] app/presentacion/paneles/estado/vista.py (20 min)
  - EstadoVista: QWidget con layout y labels
  - Hereda de QWidget
- [ ] app/presentacion/paneles/estado/controlador.py (15 min)
  - EstadoControlador: mediador entre modelo y vista
  - Maneja eventos y actualización de vista

### 2. Integración con Comunicación
- [ ] Conectar ServicioDatos → EstadoControlador (10 min)
  - Suscripción a actualizaciones de datos
  - Callback para actualizar modelo

### 3. Factory y Coordinator
- [ ] Registrar en Factory (5 min)
  - Agregar EstadoControlador a factory_paneles.py
- [ ] Integrar con Coordinator (5 min)
  - Agregar panel a main_coordinator.py

### 4. Tests
- [ ] tests/test_estado_modelo.py (15 min)
- [ ] tests/test_estado_vista.py (20 min)
- [ ] tests/test_estado_controlador.py (20 min)
- [ ] tests/test_estado_integracion.py (15 min)

### 5. Validación
- [ ] Ejecutar escenarios BDD (5 min)
- [ ] Quality gates (Pylint, CC, MI) (5 min)

**Estado:** 0/12 tareas completadas
```

### Ejemplo 2: FastAPI - Endpoint REST

```markdown
# Plan de Implementación: US-002 - Endpoint de consulta de usuarios

**Patrón:** Layered Architecture
**Producto:** api_users
**Estimación Total:** 1h 45min

## Componentes a Implementar

### 1. User Endpoint (Layered)
- [ ] app/domain/schemas/user_schema.py (10 min)
  - UserResponse: Pydantic model para respuesta
  - UserFilter: Pydantic model para filtros
- [ ] app/services/user_service.py (20 min)
  - UserService: lógica de negocio
  - Método get_users(filter: UserFilter)
- [ ] app/repositories/user_repository.py (15 min)
  - UserRepository: acceso a datos
  - Query con filtros dinámicos
- [ ] app/api/v1/routers/users.py (15 min)
  - GET /users endpoint
  - Dependency injection de UserService

### 2. Integración
- [ ] Configurar dependency injection (10 min)
  - Registrar UserService en dependencies.py
  - Configurar repository con session de BD

### 3. Tests
- [ ] tests/unit/test_user_service.py (15 min)
- [ ] tests/integration/test_user_repository.py (15 min)
- [ ] tests/api/test_users_endpoint.py (20 min)

### 4. Validación
- [ ] Ejecutar escenarios BDD (5 min)
- [ ] Quality gates (Pylint, coverage) (5 min)

**Estado:** 0/10 tareas completadas
```

### Ejemplo 3: Flask REST - API Endpoint

```markdown
# Plan de Implementación: US-003 - API de consulta de productos

**Patrón:** Layered Architecture (Flask)
**Producto:** api_catalog
**Estimación Total:** 1h 50min

## Componentes a Implementar

### 1. Product API (Layered - 3 capas)

#### Capa de Servicios (API Layer)
- [ ] app/servicios/products/api.py (20 min)
  - Flask Blueprint con endpoints REST
  - GET /api/products (listar productos)
  - GET /api/products/<id> (obtener producto)
  - POST /api/products (crear producto)
  - Validación de request.get_json()
  - Serialización con jsonify()

#### Capa General (Domain Layer)
- [ ] app/general/products/product.py (15 min)
  - Dataclass Product (modelo de dominio)
  - Lógica de negocio (validaciones)
  - Método to_dict() para serialización

#### Capa de Datos (Data Access Layer)
- [ ] app/datos/products/repositorio.py (10 min)
  - ProductRepository (ABC interface)
  - Métodos abstractos (get_all, get_by_id, create)
- [ ] app/datos/products/memoria.py (15 min)
  - ProductRepositoryMemory (implementación in-memory)
  - Storage en lista Python

### 2. Configuración y Error Handling
- [ ] app/servicios/products/errors.py (10 min)
  - Custom exceptions (ProductNotFound, ValidationError)
  - Error handlers (@app.errorhandler)

### 3. Integración
- [ ] Registrar blueprint en app/__init__.py (5 min)
  - app.register_blueprint(products_bp)
- [ ] Configurar Configurador singleton (5 min)
  - Inyectar repository en endpoints

### 4. Tests
- [ ] tests/unit/test_product_model.py (10 min)
- [ ] tests/unit/test_product_repository.py (15 min)
- [ ] tests/integration/test_products_api.py (25 min)
  - Tests con Flask test client
  - Fixtures: app, client

### 5. Validación
- [ ] Ejecutar escenarios BDD (5 min)
- [ ] Quality gates (Pylint ≥8.0, Coverage ≥95%) (5 min)

**Estado:** 0/11 tareas completadas
```

### Ejemplo 4: Flask Webapp - Página de Productos

```markdown
# Plan de Implementación: US-004 - Página de listado de productos

**Patrón:** BFF + SSR
**Producto:** webapp_catalog
**Estimación Total:** 2h 15min

## Componentes a Implementar

### 1. Backend (Routes + API Client)

#### Routes (View Functions)
- [ ] webapp/routes.py - Agregar routes de productos (20 min)
  - GET /products (listar productos)
  - GET /products/<id> (detalle de producto)
  - Llamar APIClient.get_products()
  - render_template() con datos

#### API Client (BFF Pattern)
- [ ] webapp/api_client.py - Métodos de productos (15 min)
  - get_products() → requests.get('http://api:5050/api/products')
  - get_product(id) → requests.get(f'http://api:5050/api/products/{id}')
  - Manejo de errores HTTP (404, 500)

### 2. Frontend (Templates + JavaScript + CSS)

#### Templates (Jinja2 SSR)
- [ ] webapp/templates/products/list.html (25 min)
  - Extends base.html
  - Loop {% for product in products %}
  - Inclusión de card component
  - Manejo de caso vacío
- [ ] webapp/templates/products/detail.html (20 min)
  - Detalle de producto individual
  - Formulario de actualización (opcional)
  - Botones de acción

#### Components (Partials)
- [ ] webapp/templates/components/product_card.html (10 min)
  - Card reutilizable para mostrar producto
  - Imagen, nombre, precio, stock

#### JavaScript (Vanilla JS)
- [ ] webapp/static/js/products.js (20 min)
  - Event handlers para botones
  - Fetch API para updates dinámicos
  - DOM manipulation (update sin reload)

#### CSS
- [ ] webapp/static/css/products.css (10 min)
  - Estilos específicos de productos
  - Responsive grid layout

### 3. Forms (Opcional)
- [ ] webapp/forms.py - ProductFilterForm (10 min)
  - Flask-WTF form para filtros
  - Fields: categoria, precio_min, precio_max
  - CSRF protection automático

### 4. Integración
- [ ] Registrar routes en app/__init__.py (5 min)
  - No usar blueprints (routes en archivo único)
- [ ] Configurar API_BASE_URL en config.py (5 min)
  - Development: http://localhost:5050
  - Production: variable de entorno

### 5. Tests
- [ ] tests/unit/test_api_client_products.py (15 min)
  - Test métodos get_products, get_product
  - Mock requests con responses library
- [ ] tests/integration/test_products_routes.py (25 min)
  - Test routes con Flask test client
  - Mock APIClient.get_products()
  - Assert template rendering
  - Assert status codes (200, 404)

### 6. Validación
- [ ] Ejecutar escenarios BDD (5 min)
- [ ] Quality gates (Pylint ≥8.0, Coverage ≥90%) (5 min)
  - Coverage solo backend (routes + api_client)
  - JavaScript NO incluido en coverage

**Estado:** 0/14 tareas completadas
```

### Ejemplo 5: Generic Python - Módulo de Procesamiento

```markdown
# Plan de Implementación: US-004 - Procesador de datos

**Patrón:** Generic
**Producto:** data_processor
**Estimación Total:** 1h 30min

## Componentes a Implementar

### 1. Data Processor Module
- [ ] src/processor/validator.py (15 min)
  - Clase DataValidator
  - Métodos de validación de datos de entrada
- [ ] src/processor/transformer.py (20 min)
  - Clase DataTransformer
  - Lógica de transformación de datos
- [ ] src/processor/processor.py (15 min)
  - Clase DataProcessor (orquestador)
  - Integra validator y transformer

### 2. Utilidades
- [ ] src/processor/exceptions.py (10 min)
  - Excepciones custom para errores de procesamiento

### 3. Tests
- [ ] tests/test_validator.py (15 min)
- [ ] tests/test_transformer.py (15 min)
- [ ] tests/test_processor.py (20 min)

### 4. Validación
- [ ] Ejecutar escenarios BDD (5 min)
- [ ] Quality gates (Pylint, coverage) (5 min)

**Estado:** 0/8 tareas completadas
```

---

## Template de Output

El plan generado debe seguir esta estructura:

```markdown
# Plan de Implementación: {US_ID} - {US_TITLE}

**Patrón:** {ARCHITECTURE_PATTERN}
**Producto:** {PRODUCT}
**Estimación Total:** Xh XXmin

## Componentes a Implementar

### 1. {COMPONENT_NAME} ({ARCHITECTURE_PATTERN})
- [ ] {COMPONENT_PATH}/file1.py (XX min)
  - Descripción breve del componente
  - Responsabilidades principales
- [ ] {COMPONENT_PATH}/file2.py (XX min)
  ...

### 2. Integración
- [ ] Descripción de integración (XX min)
  - Puntos de conexión con componentes existentes

### 3. Tests
- [ ] tests/test_*.py por cada componente (XX min)

### 4. Validación
- [ ] Ejecutar escenarios BDD (5 min)
- [ ] Quality gates (5 min)

**Estado:** 0/N tareas completadas
```

---

## Ubicación del Archivo Generado

> **Según stack:**
> - **PyQt/MVC:** `{PRODUCT}/docs/plans/US-XXX-plan.md`
> - **FastAPI:** `docs/plans/US-XXX-plan.md`
> - **Django:** `docs/requirements/US-XXX-plan.md`
> - **Generic:** `docs/plans/US-XXX-plan.md`

---

## Consideraciones Importantes

### Estimaciones de Tiempo

**Componentes simples:**
- Modelo/Schema: 10-15 min
- Vista/Template básica: 15-20 min
- Controlador/Service: 15-20 min

**Componentes complejos:**
- Vista interactiva: 25-30 min
- Service con múltiple lógica: 25-35 min
- Repository con queries complejas: 20-30 min

**Tests:**
- Test unitario simple: 10-15 min
- Test con mocks: 15-20 min
- Test de integración: 15-25 min

**Validación:**
- BDD: 5 min
- Quality gates: 5 min

### Organización de Tareas

1. **Secuencia bottom-up:** Empezar por capas inferiores (modelo, schema) hacia superiores (controlador, router)
2. **Dependencias primero:** Componentes sin dependencias antes que los que dependen de otros
3. **Tests después de implementación:** Tests inmediatamente después del componente correspondiente

---

## Punto de Aprobación

**Usuario revisa y aprueba el plan**

Este es un punto crítico donde el usuario debe validar:
- La estructura de componentes es correcta
- Las estimaciones son razonables
- No falta ningún componente o integración importante
- El orden de tareas tiene sentido

**El plan puede ajustarse en esta fase** antes de comenzar la implementación.

---

## Tracking

**Al finalizar la fase:**
```python
tracker.end_phase(2, auto_approved=False)  # Requiere aprobación del usuario
```

---

**Fase anterior:** [Fase 1: Generación de Escenarios BDD](./phase-1-bdd.md)
**Siguiente fase:** Fase 3: Implementación Guiada por Tareas _(pendiente)_
