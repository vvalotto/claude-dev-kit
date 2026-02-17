# Flask Contacts API

API REST para gestión de contactos construida con Flask, siguiendo las mejores prácticas del Claude Dev Kit framework.

## Características

- **CRUD Completo**: Crear, leer, actualizar y eliminar contactos
- **Validación**: Email validation y campos requeridos
- **Arquitectura Limpia**: Separación en capas (Models, Services, Routes)
- **Alta Cobertura**: 94% test coverage
- **Calidad de Código**: Pylint score 9.65/10
- **BDD Testing**: 10 escenarios Gherkin con pytest-bdd

## Requisitos

- Python 3.10+
- pip

## Instalación

### 1. Clonar el repositorio

```bash
cd examples/code/flask-contacts-api/
```

### 2. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## Uso

### Iniciar el servidor

```bash
python main.py
```

La API estará disponible en `http://localhost:5000`

### Health Check

```bash
curl http://localhost:5000/health
```

### Endpoints Disponibles

#### 1. Listar todos los contactos

```bash
GET /contacts
```

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "nombre": "Juan Pérez",
    "email": "juan.perez@email.com",
    "telefono": "555-1234"
  }
]
```

#### 2. Obtener contacto por ID

```bash
GET /contacts/{id}
```

**Response** (200 OK):
```json
{
  "id": 1,
  "nombre": "Juan Pérez",
  "email": "juan.perez@email.com",
  "telefono": "555-1234"
}
```

**Response** (404 Not Found):
```json
{
  "error": "Contact not found"
}
```

#### 3. Crear contacto

```bash
POST /contacts
Content-Type: application/json

{
  "nombre": "María García",
  "email": "maria.garcia@email.com",
  "telefono": "555-5678"
}
```

**Response** (201 Created):
```json
{
  "id": 2,
  "nombre": "María García",
  "email": "maria.garcia@email.com",
  "telefono": "555-5678"
}
```

**Response** (400 Bad Request):
```json
{
  "error": "Invalid email format: invalid-email"
}
```

#### 4. Actualizar contacto

```bash
PUT /contacts/{id}
Content-Type: application/json

{
  "nombre": "María García López",
  "email": "maria.nuevo@email.com",
  "telefono": "555-9999"
}
```

**Response** (200 OK):
```json
{
  "id": 2,
  "nombre": "María García López",
  "email": "maria.nuevo@email.com",
  "telefono": "555-9999"
}
```

**Nota**: Los campos son opcionales. Solo se actualizan los campos proporcionados.

#### 5. Eliminar contacto

```bash
DELETE /contacts/{id}
```

**Response**: 204 No Content (exitoso)
**Response**: 404 Not Found (contacto no existe)

## Testing

### Ejecutar todos los tests

```bash
pytest tests/ -v
```

### Tests unitarios (service layer)

```bash
pytest tests/test_contact_service.py -v
```

**14 tests** cubriendo:
- Creación de contactos (datos válidos, email inválido, campos faltantes)
- Listado de contactos (vacío, con datos)
- Obtener por ID (existente, inexistente)
- Actualización (completa, parcial, inexistente)
- Eliminación (existente, inexistente)
- Validación de email
- IDs únicos secuenciales

### Tests de integración (endpoints)

```bash
pytest tests/test_endpoints.py -v
```

**14 tests** cubriendo:
- Todos los endpoints HTTP
- Status codes correctos
- Formato de respuestas JSON
- Manejo de errores
- Flujo CRUD completo

### Tests BDD (escenarios Gherkin)

```bash
pytest tests/test_bdd_contacts.py -v
```

**10 escenarios** en español:
- Crear contacto con datos válidos
- Intentar crear con email inválido
- Listar todos los contactos
- Obtener contacto por ID (existente/inexistente)
- Actualizar contacto (existente/inexistente)
- Eliminar contacto (existente/inexistente)
- Validar campos requeridos

### Coverage

```bash
pytest --cov=app --cov-report=term-missing --cov-report=html tests/
```

**Coverage actual**: 94%

El reporte HTML estará disponible en `htmlcov/index.html`

## Quality Gates

### Pylint

```bash
pylint app/
```

**Score**: 9.65/10 (objetivo: >= 8.5) ✓

### Complejidad Ciclomática

```bash
radon cc app/ -a
```

**Resultado**: Promedio A (2.5) - Todas las funciones con complejidad < 10 ✓

### Maintainability Index

```bash
radon mi app/
```

**Resultado**: Todos los módulos con ranking A (MI >= 25) ✓

## Arquitectura

### Estructura del Proyecto

```
flask-contacts-api/
├── app/
│   ├── __init__.py              # Application factory
│   ├── models/
│   │   ├── __init__.py
│   │   └── contact.py           # Contact, ContactCreate, ContactUpdate
│   ├── database.py              # In-memory database
│   ├── services/
│   │   ├── __init__.py
│   │   └── contact_service.py   # Business logic
│   └── routes/
│       ├── __init__.py
│       └── contacts.py          # Flask Blueprint (endpoints)
├── tests/
│   ├── conftest.py              # Pytest fixtures
│   ├── test_contact_service.py  # Unit tests
│   ├── test_endpoints.py        # Integration tests
│   └── test_bdd_contacts.py     # BDD tests
├── features/
│   ├── contacts.feature         # Gherkin scenarios
│   └── steps/
│       └── contact_steps.py     # Step definitions
├── docs/
│   ├── planning/
│   │   └── US-055-plan.md       # Implementation plan
│   ├── architecture/
│   │   └── ADR-001-flask-blueprint-architecture.md
│   └── reporting/
│       └── US-055-report.md     # Final report
├── main.py                      # Entry point
├── requirements.txt
├── pytest.ini
└── README.md
```

### Capas de la Aplicación

1. **Models Layer** (`app/models/`)
   - Dataclasses para Contact, ContactCreate, ContactUpdate
   - Validación de email

2. **Database Layer** (`app/database.py`)
   - In-memory storage (dict)
   - Auto-increment IDs

3. **Service Layer** (`app/services/`)
   - Business logic
   - CRUD operations
   - Validaciones

4. **Routes Layer** (`app/routes/`)
   - Flask Blueprint
   - HTTP endpoints
   - Request/Response handling
   - Error handling

5. **Application Factory** (`app/__init__.py`)
   - create_app() pattern
   - Blueprint registration
   - Configuration

## Validaciones

### Email

El email debe contener:
- Texto antes del @
- El símbolo @
- Texto después del @
- Un punto (.)

Ejemplos válidos:
- `juan.perez@email.com`
- `user+tag@domain.co.uk`

Ejemplos inválidos:
- `invalid-email`
- `@example.com`
- `test@`

### Campos Requeridos

Al crear un contacto, todos los campos son requeridos:
- `nombre`: string no vacío
- `email`: string con formato válido
- `telefono`: string no vacío

## Decisiones de Diseño

Ver `docs/architecture/ADR-001-flask-blueprint-architecture.md` para detalles sobre:
- Por qué Flask Blueprints vs Flask-RESTX
- Arquitectura en capas
- In-memory database vs persistencia

## Limitaciones Conocidas

- **Base de datos**: Los datos se almacenan en memoria y se pierden al reiniciar
- **Autenticación**: No implementada (fuera del alcance)
- **Paginación**: No implementada para el listado de contactos
- **Búsqueda**: No hay filtros o búsqueda de contactos

## Próximos Pasos

Para un entorno de producción, considerar:
- [ ] Persistencia (SQLite, PostgreSQL, etc.)
- [ ] Autenticación y autorización (JWT, OAuth2)
- [ ] Paginación y filtros
- [ ] Rate limiting
- [ ] CORS configuration
- [ ] Logging estructurado
- [ ] Containerización (Docker)
- [ ] CI/CD pipeline

## Contribuir

Este proyecto es un ejemplo del Claude Dev Kit framework. Para contribuir:

1. Fork el repositorio
2. Crear feature branch (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'feat: agregar funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abrir Pull Request

## Licencia

MIT

## Contacto

Para preguntas sobre el Claude Dev Kit framework, consultar la documentación principal en `/docs/`.

---

**Generado con Claude Dev Kit** - Framework para desarrollo asistido con Claude Code
