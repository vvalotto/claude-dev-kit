# Fase 2: Generación del Plan de Implementación

**Objetivo:** Crear un plan detallado de implementación basado en la arquitectura configurada del proyecto.

> **📌 Instrucción de ejecución:** Seguir este archivo de arriba a abajo, en el orden en que aparecen los pasos. No saltar ni reordenar.

---

## Paso 1 🔴 — Verificar precondiciones

Confirmá que existe el archivo de contexto generado en Fase 0:

```bash
ls docs/plans/{US_ID}-context.md
```

Si no existe, **no avances** — ejecutá Fase 0 primero.

---

## Paso 2 🔴 — Iniciar tracking

Ejecutá antes de cualquier otra acción en esta fase:

```bash
python .claude/tracking/tracker_cli.py start-phase 2 "Generación del Plan de Implementación"
```

---

## Paso 3 — Identificar patrón y componentes

Leé el patrón activo del archivo `.claude/skills/implement-us/config.json`, clave `variables.architecture_pattern`. Luego identificá los componentes a crear según la siguiente referencia:

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

---

## Paso 4 — Identificar dependencias y puntos de integración

- Componentes externos que la US necesita consumir
- Servicios o módulos existentes que deben integrarse
- Patrones del proyecto que deben aplicarse

---

## Paso 5 — Generar checklist de tareas

Organizar en secciones:
1. **Componentes principales** (según patrón arquitectónico)
2. **Integración** (conexión con componentes existentes)

> **Nota:** Tests → Fases 4, 5 y 6. Quality gates → Fase 7. No incluirlos en el plan.

---

## Paso 6 🔴 — Verificar existencia del plan

Antes de presentarlo al usuario, confirmá que el archivo fue generado en disco:

```bash
ls docs/plans/{US_ID}-plan.md
```

Si no existe, generalo siguiendo el template antes de continuar.

---

## Paso 7 🔴 — STOP — Checkpoint de aprobación

**No avances a Fase 3 hasta que:**
1. `docs/plans/{US_ID}-plan.md` exista en disco ✅
2. El usuario haya respondido explícitamente con aprobación del plan

Presentá el plan al usuario y esperá su respuesta antes de continuar. El usuario puede solicitar ajustes — incorporalos y volvé a presentar.

---

## ✅ Checklist de Salida

Antes de avanzar a Fase 3, confirmá que:
- [ ] `docs/plans/{US_ID}-plan.md` existe en disco: `ls docs/plans/{US_ID}-plan.md`
- [ ] El plan fue presentado al usuario
- [ ] El usuario aprobó el plan explícitamente
- [ ] Tracking de Fase 2 cerrado

---

## Paso 8 🔴 — Cerrar tracking

```bash
python .claude/tracking/tracker_cli.py end-phase 2
```

---

## 📖 Template de Output

**Archivo de salida:** `docs/plans/{US_ID}-plan.md`

> **Prioridad de templates:** Si existe `.claude/templates/planning/implementation-plan.md`, usalo
> como base estructural. Si no existe, usá el template embebido a continuación.

El plan generado debe seguir esta estructura:

```markdown
# Plan de Implementación: {US_ID} - {US_TITLE}

**Patrón:** {ARCHITECTURE_PATTERN}
**Producto:** {PRODUCT}

## Componentes a Implementar

### 1. {COMPONENT_NAME} ({ARCHITECTURE_PATTERN})
- [ ] {COMPONENT_PATH}/file1.py
  - Descripción breve del componente
  - Responsabilidades principales
- [ ] {COMPONENT_PATH}/file2.py
  ...

### 2. Integración
- [ ] Descripción de integración
  - Puntos de conexión con componentes existentes

**Estado:** 0/N tareas completadas
```

---

## 📖 Ejemplos de Output por Stack

### Ejemplo 1: PyQt/MVC - Panel UI

```markdown
# Plan de Implementación: US-001 - Mostrar información de estado

**Patrón:** MVC
**Producto:** ux_monitor

## Componentes a Implementar

### 1. Panel Estado (MVC)
- [ ] app/presentacion/paneles/estado/modelo.py
  - EstadoModelo: dataclass inmutable con datos del estado
  - Hereda de ModeloBase
- [ ] app/presentacion/paneles/estado/vista.py
  - EstadoVista: QWidget con layout y labels
  - Hereda de QWidget
- [ ] app/presentacion/paneles/estado/controlador.py
  - EstadoControlador: mediador entre modelo y vista
  - Maneja eventos y actualización de vista

### 2. Integración con Comunicación
- [ ] Conectar ServicioDatos → EstadoControlador
  - Suscripción a actualizaciones de datos
  - Callback para actualizar modelo

### 3. Integración con mecanismo de composición
- [ ] Registrar en el mecanismo de composición del perfil activo
  - Para PyQt/MVC: agregar controlador a Factory y Coordinator
  - Para otros patrones: registrar en el mecanismo correspondiente (DI container, app factory, etc.)

**Estado:** 0/5 tareas completadas
```

### Ejemplo 2: FastAPI - Endpoint REST

```markdown
# Plan de Implementación: US-002 - Endpoint de consulta de usuarios

**Patrón:** Layered Architecture
**Producto:** api_users

## Componentes a Implementar

### 1. User Endpoint (Layered)
- [ ] app/domain/schemas/user_schema.py
  - UserResponse: Pydantic model para respuesta
  - UserFilter: Pydantic model para filtros
- [ ] app/services/user_service.py
  - UserService: lógica de negocio
  - Método get_users(filter: UserFilter)
- [ ] app/repositories/user_repository.py
  - UserRepository: acceso a datos
  - Query con filtros dinámicos
- [ ] app/api/v1/routers/users.py
  - GET /users endpoint
  - Dependency injection de UserService

### 2. Integración
- [ ] Configurar dependency injection
  - Registrar UserService en dependencies.py
  - Configurar repository con session de BD

**Estado:** 0/5 tareas completadas
```

### Ejemplo 3: Flask REST - API Endpoint

```markdown
# Plan de Implementación: US-003 - API de consulta de productos

**Patrón:** Layered Architecture (Flask)
**Producto:** api_catalog

## Componentes a Implementar

### 1. Product API (Layered - 3 capas)

#### Capa de Servicios (API Layer)
- [ ] app/servicios/products/api.py
  - Flask Blueprint con endpoints REST
  - GET /api/products, GET /api/products/<id>, POST /api/products
  - Validación de request.get_json()
  - Serialización con jsonify()

#### Capa General (Domain Layer)
- [ ] app/general/products/product.py
  - Dataclass Product (modelo de dominio)
  - Lógica de negocio (validaciones)
  - Método to_dict() para serialización

#### Capa de Datos (Data Access Layer)
- [ ] app/datos/products/repositorio.py
  - ProductRepository (ABC interface)
  - Métodos abstractos (get_all, get_by_id, create)
- [ ] app/datos/products/memoria.py
  - ProductRepositoryMemory (implementación in-memory)
  - Storage en lista Python

### 2. Configuración y Error Handling
- [ ] app/servicios/products/errors.py
  - Custom exceptions (ProductNotFound, ValidationError)
  - Error handlers (@app.errorhandler)

### 3. Integración
- [ ] Registrar blueprint en app/__init__.py
  - app.register_blueprint(products_bp)
- [ ] Configurar Configurador singleton
  - Inyectar repository en endpoints

**Estado:** 0/6 tareas completadas
```

### Ejemplo 4: Flask Webapp - Página de Productos

```markdown
# Plan de Implementación: US-004 - Página de listado de productos

**Patrón:** BFF + SSR
**Producto:** webapp_catalog

## Componentes a Implementar

### 1. Backend (Routes + API Client)

#### Routes (View Functions)
- [ ] webapp/routes.py - Agregar routes de productos
  - GET /products (listar productos)
  - GET /products/<id> (detalle de producto)
  - Llamar APIClient.get_products()
  - render_template() con datos

#### API Client (BFF Pattern)
- [ ] webapp/api_client.py - Métodos de productos
  - get_products() → requests.get('http://api:5050/api/products')
  - get_product(id) → requests.get(f'http://api:5050/api/products/{id}')
  - Manejo de errores HTTP (404, 500)

### 2. Frontend (Templates + JavaScript + CSS)

#### Templates (Jinja2 SSR)
- [ ] webapp/templates/products/list.html
  - Extends base.html
  - Loop {% for product in products %}
  - Inclusión de card component
  - Manejo de caso vacío
- [ ] webapp/templates/products/detail.html
  - Detalle de producto individual
  - Botones de acción

#### Components (Partials)
- [ ] webapp/templates/components/product_card.html
  - Card reutilizable para mostrar producto

#### JavaScript (Vanilla JS)
- [ ] webapp/static/js/products.js
  - Event handlers para botones
  - Fetch API para updates dinámicos

#### CSS
- [ ] webapp/static/css/products.css
  - Estilos específicos de productos

### 3. Integración
- [ ] Registrar routes en app/__init__.py
- [ ] Configurar API_BASE_URL en config.py

**Estado:** 0/8 tareas completadas
```

### Ejemplo 5: Generic Python - Módulo de Procesamiento

```markdown
# Plan de Implementación: US-005 - Procesador de datos

**Patrón:** Generic
**Producto:** data_processor

## Componentes a Implementar

### 1. Data Processor Module
- [ ] src/processor/validator.py
  - Clase DataValidator
  - Métodos de validación de datos de entrada
- [ ] src/processor/transformer.py
  - Clase DataTransformer
  - Lógica de transformación de datos
- [ ] src/processor/processor.py
  - Clase DataProcessor (orquestador)
  - Integra validator y transformer

### 2. Utilidades
- [ ] src/processor/exceptions.py
  - Excepciones custom para errores de procesamiento

**Estado:** 0/4 tareas completadas
```

---

## 📖 Organización de Tareas

1. **Secuencia bottom-up:** Empezar por capas inferiores (modelo, schema) hacia superiores (controlador, router)
2. **Dependencias primero:** Componentes sin dependencias antes que los que dependen de otros

---

**Fase anterior:** [Fase 1: Generación de Escenarios BDD](./phase-1-bdd.md)
**Siguiente fase:** [Fase 3: Implementación Guiada por Tareas](./phase-3-implementation.md)
