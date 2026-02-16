# Plan de Implementación - US-055: API REST de Contactos con Flask

## Información General

- **Historia de Usuario**: US-055
- **Título**: API REST de Contactos con Flask
- **Perfil Técnico**: flask-rest
- **Estimación Total**: 240 minutos (4 horas)

## Arquitectura de la Solución

### Patrón Arquitectónico: Layered Architecture (Flask Blueprint)

```
flask-contacts-api/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── models/
│   │   ├── __init__.py
│   │   └── contact.py           # Dataclasses: Contact, ContactCreate, ContactUpdate
│   ├── database.py              # In-memory database (dict)
│   ├── services/
│   │   ├── __init__.py
│   │   └── contact_service.py   # Business logic layer
│   └── routes/
│       ├── __init__.py
│       └── contacts.py          # Flask Blueprint (endpoints)
├── main.py                      # Entry point
├── requirements.txt
├── pytest.ini
└── .gitignore
```

### Componentes Principales

#### 1. **Models Layer** (app/models/contact.py)
- `Contact`: Dataclass para representar un contacto completo (con ID)
- `ContactCreate`: Dataclass para crear contacto (sin ID)
- `ContactUpdate`: Dataclass para actualizar contacto (campos opcionales)
- Validación de email en ContactCreate

#### 2. **Database Layer** (app/database.py)
- In-memory database usando dict: `contacts_db = {}`
- Contador auto-incremental para IDs: `next_id = 1`
- Funciones de acceso: `get_db()`, `reset_db()`

#### 3. **Service Layer** (app/services/contact_service.py)
- `ContactService`: Lógica de negocio
  - `create_contact(contact_data: ContactCreate) -> Contact`
  - `get_all_contacts() -> List[Contact]`
  - `get_contact_by_id(contact_id: int) -> Optional[Contact]`
  - `update_contact(contact_id: int, contact_data: ContactUpdate) -> Optional[Contact]`
  - `delete_contact(contact_id: int) -> bool`
  - Validaciones de negocio (email, campos requeridos)

#### 4. **Routes Layer** (app/routes/contacts.py)
- Flask Blueprint: `contacts_bp`
- Endpoints:
  - `GET /contacts` - Listar contactos
  - `GET /contacts/<int:id>` - Obtener contacto
  - `POST /contacts` - Crear contacto
  - `PUT /contacts/<int:id>` - Actualizar contacto
  - `DELETE /contacts/<int:id>` - Eliminar contacto
- Manejo de errores (404, 400)
- Serialización JSON

#### 5. **Application Factory** (app/__init__.py)
- `create_app()`: Factory pattern para crear Flask app
- Registro de blueprints
- Configuración de CORS (si necesario)
- Error handlers globales

### Decisiones Técnicas

| Aspecto | Decisión | Justificación |
|---------|----------|---------------|
| Web Framework | Flask 3.0+ | Ligero, simple para APIs REST |
| Arquitectura | Blueprints + Services | Separación de responsabilidades |
| Base de Datos | In-memory dict | Simplicidad para ejemplo/demo |
| Validación | Dataclasses + custom validators | Python nativo, type hints |
| Serialización | dataclasses.asdict() + jsonify | Simple y directo |
| Testing Framework | pytest + pytest-bdd | Estándar de la industria |

## Desglose de Tareas

### **Fase 3: Implementación** (120 min)

#### 3.1. Models Layer (20 min)
- [ ] `app/models/__init__.py` (2 min)
- [ ] `app/models/contact.py` (18 min)
  - Contact dataclass
  - ContactCreate dataclass con validación de email
  - ContactUpdate dataclass (campos opcionales)
  - Función helper: `validate_email(email: str) -> bool`

#### 3.2. Database Layer (10 min)
- [ ] `app/database.py` (10 min)
  - Dict global para almacenar contactos
  - Contador de IDs
  - Funciones get_db(), reset_db()

#### 3.3. Service Layer (30 min)
- [ ] `app/services/__init__.py` (2 min)
- [ ] `app/services/contact_service.py` (28 min)
  - Clase ContactService
  - Implementar CRUD completo
  - Validaciones de negocio
  - Manejo de errores de validación

#### 3.4. Routes Layer (30 min)
- [ ] `app/routes/__init__.py` (2 min)
- [ ] `app/routes/contacts.py` (28 min)
  - Blueprint contacts_bp
  - 5 endpoints con manejo de errores
  - Serialización de responses
  - Error handlers (404, 400)

#### 3.5. Application Factory (10 min)
- [ ] `app/__init__.py` (10 min)
  - create_app() factory
  - Registro de blueprints
  - Configuración básica

#### 3.6. Entry Point y Configuración (20 min)
- [ ] `main.py` (5 min)
- [ ] `requirements.txt` (5 min)
- [ ] `pytest.ini` (5 min)
- [ ] `.gitignore` (5 min)

### **Fase 4: Tests Unitarios** (40 min)

#### 4.1. Setup de Tests (10 min)
- [ ] `tests/__init__.py` (2 min)
- [ ] `tests/conftest.py` (8 min)
  - Fixtures: app, client, sample_contact

#### 4.2. Tests de Service Layer (30 min)
- [ ] `tests/test_contact_service.py` (30 min)
  - `test_create_contact_valid_data()` (3 min)
  - `test_create_contact_invalid_email()` (3 min)
  - `test_create_contact_missing_fields()` (3 min)
  - `test_get_all_contacts_empty()` (2 min)
  - `test_get_all_contacts_with_data()` (3 min)
  - `test_get_contact_by_id_exists()` (3 min)
  - `test_get_contact_by_id_not_exists()` (2 min)
  - `test_update_contact_exists()` (3 min)
  - `test_update_contact_not_exists()` (2 min)
  - `test_delete_contact_exists()` (3 min)
  - `test_delete_contact_not_exists()` (2 min)
  - `test_email_validation()` (1 min)

### **Fase 5: Tests de Integración** (50 min)

#### 5.1. Tests de Endpoints (50 min)
- [ ] `tests/test_endpoints.py` (50 min)
  - `test_get_contacts_empty()` (3 min)
  - `test_create_contact_valid()` (4 min)
  - `test_create_contact_invalid_email()` (3 min)
  - `test_create_contact_missing_fields()` (3 min)
  - `test_get_contacts_after_create()` (4 min)
  - `test_get_contact_by_id_exists()` (4 min)
  - `test_get_contact_by_id_not_exists()` (3 min)
  - `test_update_contact_exists()` (4 min)
  - `test_update_contact_not_exists()` (3 min)
  - `test_update_contact_partial()` (4 min)
  - `test_delete_contact_exists()` (4 min)
  - `test_delete_contact_not_exists()` (3 min)
  - `test_full_crud_workflow()` (8 min)

### **Fase 6: Validación BDD** (30 min)

#### 6.1. Step Definitions (30 min)
- [ ] `features/steps/__init__.py` (2 min)
- [ ] `features/steps/contact_steps.py` (28 min)
  - Given steps (API running, DB empty, create contacts)
  - When steps (HTTP requests GET/POST/PUT/DELETE)
  - Then steps (status code, response validation)

### **Fase 7: Quality Gates** (20 min)

#### 7.1. Linting (5 min)
- [ ] Ejecutar `pylint app/` (score >= 8.5)
- [ ] Corregir issues críticos si aparecen

#### 7.2. Coverage (5 min)
- [ ] Ejecutar `pytest --cov=app --cov-report=term-missing`
- [ ] Verificar coverage >= 95%

#### 7.3. Complexity Analysis (5 min)
- [ ] Ejecutar `radon cc app/ -a`
- [ ] Verificar complejidad < 10

#### 7.4. Maintainability Index (5 min)
- [ ] Ejecutar `radon mi app/`
- [ ] Verificar MI >= 25

### **Fase 8: Documentación** (30 min)

#### 8.1. README Principal (15 min)
- [ ] `README.md` (15 min)
  - Descripción del proyecto
  - Instalación
  - Uso de la API
  - Ejecución de tests
  - Quality gates

#### 8.2. ADR - Arquitectura (15 min)
- [ ] `docs/architecture/ADR-001-flask-blueprint-architecture.md` (15 min)
  - Contexto
  - Decisión: Blueprints vs Flask-RESTX
  - Consecuencias
  - Alternativas consideradas

### **Fase 9: Reporte Final** (20 min)

#### 9.1. Reporte de Implementación (20 min)
- [ ] `docs/reporting/US-055-report.md` (20 min)
  - Resumen ejecutivo
  - Criterios de aceptación cumplidos
  - Métricas de calidad
  - Tests ejecutados
  - Tiempo invertido

## Plan de Testing

### Tests Unitarios (12 tests)
- **Cobertura esperada**: 100% del service layer
- **Framework**: pytest
- **Fixtures**: app, client, sample_contact

### Tests de Integración (13 tests)
- **Cobertura esperada**: 100% de endpoints
- **Método**: Flask test_client
- **Validación**: status codes, JSON responses

### Tests BDD (10 escenarios)
- **Framework**: pytest-bdd
- **Escenarios**: CRUD completo + validaciones
- **Coverage**: Criterios de aceptación

## Criterios de Éxito

### Funcionales
- [x] Todos los endpoints implementados
- [x] CRUD completo funcionando
- [x] Validación de email
- [x] Manejo de errores (404, 400)

### No Funcionales
- [x] Pylint score >= 8.5
- [x] Test coverage >= 95%
- [x] Complejidad ciclomática < 10
- [x] Maintainability Index >= 25

### Testing
- [x] Tests unitarios: 12/12 passing
- [x] Tests integración: 13/13 passing
- [x] Tests BDD: 10/10 passing

### Documentación
- [x] README completo
- [x] ADR de arquitectura
- [x] Reporte final

## Riesgos y Mitigaciones

| Riesgo | Impacto | Probabilidad | Mitigación |
|--------|---------|--------------|------------|
| Tests BDD fallan por step definitions incorrectos | Alto | Media | Seguir ejemplos de pytest-bdd oficiales |
| Coverage < 95% | Medio | Baja | Agregar tests para edge cases |
| Pylint score bajo | Bajo | Baja | Seguir PEP 8, agregar docstrings |

## Dependencias Externas

```
Flask>=3.0.0
pytest>=8.0.0
pytest-bdd>=7.0.0
pytest-cov>=4.1.0
pylint>=3.0.0
radon>=6.0.0
```

## Notas de Implementación

### Orden de Desarrollo
1. Models (bottom-up)
2. Database
3. Services
4. Routes
5. App factory
6. Tests (paralelo con implementación)

### Convenciones de Código
- Type hints en todas las funciones
- Docstrings en Google style
- PEP 8 compliance
- Máximo 100 caracteres por línea

### Git Workflow
- Commits atómicos por componente
- Mensajes descriptivos
- Branch: feature/flask-contacts-api

## Anexos

### A. Estructura de Contact
```python
@dataclass
class Contact:
    id: int
    nombre: str
    email: str
    telefono: str
```

### B. Ejemplo de Response JSON
```json
{
  "id": 1,
  "nombre": "Juan Pérez",
  "email": "juan.perez@email.com",
  "telefono": "555-1234"
}
```

### C. Ejemplo de Error Response
```json
{
  "error": "Contact not found",
  "status": 404
}
```

---

**Fecha de Creación**: 2026-02-16
**Última Actualización**: 2026-02-16
**Estado**: Implementación Completada
