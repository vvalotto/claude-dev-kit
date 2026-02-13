# TICKET-024: Crear Perfil fastapi-rest.json

**Estado:** ✅ Completado
**Fecha Inicio:** 2026-02-13
**Fecha Fin:** 2026-02-13
**Estimación:** 1.5 horas
**Tiempo Real:** ~40 minutos

---

## Objetivo

Crear el perfil de customización `fastapi-rest.json` para APIs REST con FastAPI y arquitectura en capas (router-service-repository), extendiendo el `config.json` base con configuración específica para este stack tecnológico.

---

## Contexto

Segundo perfil de customización creado, enfocado en APIs REST modernas con:
- FastAPI (framework async)
- Arquitectura en capas (presentación → negocio → datos)
- Async/await para mejor performance
- Testing con httpx (async client)
- Dependency injection nativa de FastAPI

---

## Implementación

### Archivo Creado

**Ubicación:** `skills/implement-us/customizations/fastapi-rest.json`
**Tamaño:** ~460 líneas
**Formato:** JSON con comentarios descriptivos

### Características Principales

#### 1. Variables Override

| Variable | Valor Base | Valor FastAPI | Descripción |
|----------|------------|---------------|-------------|
| `architecture_pattern` | `generic` | `layered` | Arquitectura en 3 capas |
| `component_type` | `Component` | `Endpoint`, `Service`, `Repository` | Componentes API |
| `component_path` | `src/{name}/` | `app/api/{name}/` | Feature-based organization |
| `test_framework` | `pytest` | `pytest + httpx` | Testing async de APIs |
| `base_class` | `object` | `BaseModel` (Pydantic), `BaseService`, `BaseRepository` | Clases base por capa |
| `domain_context` | `application` | `api` | Contexto de APIs REST |
| `project_root` | `.` | `app/` | Raíz FastAPI |

#### 2. Arquitectura en Capas

**Estructura por feature:**
```
app/api/{feature}/
├── router.py       (FastAPI endpoints)
├── service.py      (lógica de negocio)
├── repository.py   (acceso a datos)
├── schemas.py      (Pydantic models)
├── models.py       (SQLAlchemy ORM)
└── __init__.py
```

**Responsabilidades por capa:**
- **Router:** Endpoints HTTP, validación Pydantic, dependency injection
- **Service:** Lógica de negocio, orquestación de repositories, transacciones
- **Repository:** CRUD, queries específicas, gestión de sesiones DB

#### 3. Testing Async con httpx

**Fixtures específicos:**
- `client`: TestClient síncrono de FastAPI
- `async_client`: httpx.AsyncClient para testing async
- `db_session`: Sesión de DB para tests (SQLite in-memory)
- `override_get_db`: Override de dependency injection

**Markers:**
- `api`: Tests de endpoints HTTP
- `async`: Tests asíncronos (pytest-asyncio)
- `db`: Tests que requieren base de datos
- `unit`, `integration`, `bdd`, `slow`

#### 4. Quality Gates

| Métrica | Base | FastAPI | Justificación |
|---------|------|---------|---------------|
| Pylint | ≥8.0 | ≥8.5 | APIs bien estructuradas, mejor score |
| CC | ≤10 | ≤10 | Servicios pequeños y cohesivos |
| MI | ≥20 | ≥25 | APIs bien diseñadas tienen MI alto |
| Coverage | ≥95% | ≥95% | APIs fáciles de testear (inyección de dependencias) |

**Pylint - Checks Deshabilitados:**
- `too-few-public-methods` (DTOs pueden tener solo datos)
- `too-many-arguments` (endpoints con muchos query params)
- `redefined-outer-name` (fixtures de pytest)

#### 5. Design Patterns

**5 patrones principales:**

1. **Layered Architecture:** Router → Service → Repository → DB
2. **Dependency Injection:** FastAPI `Depends()` para testabilidad
3. **Async/Await:** Código asíncrono para I/O-bound operations
4. **DTO Pattern:** Pydantic schemas (Create, Update, Response, InDB)
5. **Repository Pattern:** Abstracción de acceso a datos con CRUD genérico

#### 6. API Conventions

**HTTP Methods:**
- GET: Obtener recursos (idempotente)
- POST: Crear recursos
- PUT/PATCH: Actualizar recursos
- DELETE: Eliminar recursos (idempotente)

**Status Codes:**
- 200: OK, 201: Created, 204: No Content
- 400: Bad Request, 401: Unauthorized, 403: Forbidden, 404: Not Found
- 422: Unprocessable Entity (validación Pydantic)
- 500: Internal Server Error

**Endpoint Naming:**
- Collection: `/api/v1/{resources}`
- Item: `/api/v1/{resources}/{id}`
- Action: `/api/v1/{resources}/{id}/{action}`
- Nested: `/api/v1/{parent}/{parent_id}/{resources}`

**Pagination:**
- Query params: `skip` (offset) y `limit` (page size)
- Default limit: 100, Max limit: 1000
- Response: `{items: [...], total: N, skip: M, limit: L}`

**Filtering & Sorting:**
- Filters: `?status=active&price_gte=10&price_lte=100`
- Sorting: `?sort_by=created_at&order=desc`

#### 7. Authentication

- **Strategy:** JWT Bearer Token
- **Dependency:** `Depends(get_current_user)`
- **Header:** `Authorization: Bearer <token>`
- **Libraries:** python-jose, passlib

#### 8. Dependencies

**Required:**
- fastapi ≥0.104.0
- uvicorn[standard] ≥0.24.0
- pydantic ≥2.4.0
- sqlalchemy ≥2.0.0 (async)
- alembic ≥1.12.0
- pytest + pytest-asyncio + httpx

**Database Drivers (async):**
- asyncpg (PostgreSQL)
- aiomysql (MySQL)
- aiosqlite (SQLite)

#### 9. Documentation

**OpenAPI automática:**
- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI JSON: `/openapi.json`

---

## Decisiones de Diseño

### 1. Feature-Based Organization

**Decisión:** Agrupar router, service, repository, schemas, models de un feature en `app/api/{feature}/`.

**Justificación:**
- Mejor cohesión: todo relacionado a un feature en un lugar
- Fácil de navegar y entender
- Facilita trabajo en equipo (menos conflictos)

**Alternativa rechazada:** Layer-based (`app/routers/`, `app/services/`, `app/repositories/`).

### 2. Async/Await por Defecto

**Decisión:** Todos los endpoints, services y repositories son async.

**Justificación:**
- FastAPI optimizado para async
- Mejor performance en I/O-bound operations (DB, APIs externas)
- SQLAlchemy 2.0+ soporta async nativamente

**Alternativa rechazada:** Sync (más simple pero menos performante).

### 3. Quality Gates Más Estrictos

**Decisión:** Pylint ≥8.5 y MI ≥25 (vs base 8.0 y 20).

**Justificación:**
- APIs bien diseñadas son simples y cohesivas
- Arquitectura en capas fuerza separación de responsabilidades
- Código naturalmente más limpio

### 4. Dependency Injection Obligatoria

**Decisión:** Usar `Depends()` para services, repositories y DB sessions.

**Justificación:**
- Testabilidad (fácil mockear dependencias)
- Desacoplamiento (cada capa independiente)
- Reutilización (misma dependency en múltiples endpoints)

---

## Comparación PyQt/MVC vs FastAPI/Layered

| Aspecto | PyQt/MVC | FastAPI/Layered |
|---------|----------|-----------------|
| **Architecture** | MVC (3 componentes) | Layered (3-5 capas) |
| **Component Type** | Panel, Dialog, Widget | Endpoint, Service, Repository |
| **Files per Feature** | 3 (modelo, vista, controlador) | 5 (router, service, repository, schemas, models) |
| **Test Framework** | pytest + pytest-qt | pytest + httpx |
| **Fixtures** | qapp, qtbot | client, async_client, db_session |
| **Base Classes** | ModeloBase, QWidget, QObject | BaseModel (Pydantic), BaseService, BaseRepository |
| **Async** | No (Qt event loop) | Sí (async/await) |
| **Coverage Min** | 90% (UI difícil) | 95% (APIs fáciles de testear) |
| **Pylint Min** | 8.0 | 8.5 |
| **MI Min** | 20 | 25 |
| **Patterns** | Factory, Coordinator, Immutability | DI, Repository, DTO, Async |

---

## Validación

1. **JSON válido:** ✅ `python3 -m json.tool`
2. **Estructura completa:** ✅ 11 secciones implementadas
3. **Variables override:** ✅ 8 variables
4. **Patterns documentados:** ✅ 5 patterns principales
5. **API conventions:** ✅ HTTP methods, status codes, naming, pagination, filtering

---

## Próximos Pasos

Este perfil permite:
- Instalar el skill en proyectos FastAPI con configuración optimizada
- Generar código siguiendo arquitectura en capas
- Tests async con httpx automáticamente configurados
- Quality gates estrictos que fuerzan buenas prácticas

### Siguiente Ticket: TICKET-025

Crear perfil `django-mvt.json` para aplicaciones web Django con patrón MVT (Model-View-Template).

---

## Métricas

- **Tiempo estimado:** 1.5 horas
- **Tiempo real:** ~40 minutos ⚡ (56% más rápido)
- **Líneas de código:** ~460 líneas
- **Secciones implementadas:** 11
- **Variables override:** 8
- **Patterns documentados:** 5 (Layered, DI, Async, DTO, Repository)
- **API conventions:** HTTP methods, status codes, naming, pagination, filtering, sorting
- **Dependencies:** 20+ paquetes

---

## Referencias

- **Config Base:** `skills/implement-us/config.json`
- **Perfil PyQt:** `skills/implement-us/customizations/pyqt-mvc.json`
- **Sprint 2 Plan:** `gestion/fase-3-generalizacion-skills/sprint-2.md`
- **FastAPI Docs:** https://fastapi.tiangolo.com

---

**Ticket completado exitosamente.** ✅

El perfil `fastapi-rest.json` está listo para ser usado en proyectos FastAPI con arquitectura en capas.
