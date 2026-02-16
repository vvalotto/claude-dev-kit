# ADR-001: Arquitectura con Flask Blueprints

## Estado

Aceptado

## Fecha

2026-02-16

## Contexto

Para implementar la API REST de contactos necesitamos elegir una arquitectura que sea:
- Simple y fácil de entender para propósitos demostrativos
- Escalable para proyectos más grandes
- Testeable con coverage alto
- Mantenible y con separación de responsabilidades clara

Las opciones consideradas fueron:

### Opción 1: Aplicación Flask monolítica (app.py)
Todo el código en un solo archivo con rutas definidas directamente en la app.

**Pros:**
- Muy simple para proyectos tiny
- Menos archivos
- Setup mínimo

**Contras:**
- No escala bien
- Difícil de testear
- Mezcla de responsabilidades
- No es un buen ejemplo para proyectos reales

### Opción 2: Flask-RESTX
Framework más opinado con Swagger automático, namespaces, y validación integrada.

**Pros:**
- Swagger UI automático
- Validación de schemas integrada
- Documentación OpenAPI
- Estructura más rígida

**Contras:**
- Más dependencias
- Curva de aprendizaje mayor
- Opinado (menos flexible)
- Overkill para este ejemplo

### Opción 3: Flask Blueprints + Layered Architecture
Usar Flask Blueprints con separación en capas (Models, Services, Routes).

**Pros:**
- Balance entre simplicidad y estructura
- Separación de responsabilidades clara
- Altamente testeable
- Flask nativo (sin dependencias extra)
- Escalable
- Buen ejemplo de arquitectura limpia

**Contras:**
- Más archivos que opción 1
- Requiere entender Blueprints

## Decisión

**Elegimos Flask Blueprints con arquitectura en capas** (Opción 3).

### Arquitectura Implementada

```
app/
├── models/           # Capa de datos (dataclasses)
│   └── contact.py    # Contact, ContactCreate, ContactUpdate
├── database.py       # Capa de persistencia (in-memory)
├── services/         # Capa de lógica de negocio
│   └── contact_service.py
├── routes/           # Capa de presentación (HTTP)
│   └── contacts.py   # Blueprint con endpoints
└── __init__.py       # Application factory
```

### Responsabilidades por Capa

#### 1. Models Layer (`app/models/`)
- Definir estructuras de datos (dataclasses)
- Validaciones a nivel de modelo
- Type hints
- Conversión a dict para serialización

**Ejemplo:**
```python
@dataclass
class Contact:
    id: int
    nombre: str
    email: str
    telefono: str

    def to_dict(self) -> dict:
        return {...}
```

#### 2. Database Layer (`app/database.py`)
- Abstracción del almacenamiento
- In-memory dict en este caso
- Podría reemplazarse con SQLAlchemy sin cambiar otras capas

**Ejemplo:**
```python
_contacts_db: Dict[int, Contact] = {}

def get_db() -> Dict[int, Contact]:
    return _contacts_db
```

#### 3. Service Layer (`app/services/`)
- Lógica de negocio
- Operaciones CRUD
- Validaciones complejas
- No depende de Flask (puro Python)

**Ejemplo:**
```python
class ContactService:
    @staticmethod
    def create_contact(contact_data: ContactCreate) -> Contact:
        # Business logic here
```

#### 4. Routes Layer (`app/routes/`)
- Flask Blueprint
- HTTP endpoints
- Request/Response handling
- Serialización JSON
- Status codes
- Error handling

**Ejemplo:**
```python
contacts_bp = Blueprint('contacts', __name__)

@contacts_bp.route('/contacts', methods=['POST'])
def create_contact():
    # HTTP handling here
```

#### 5. Application Factory (`app/__init__.py`)
- create_app() pattern
- Configuración
- Registro de blueprints
- Error handlers globales

**Ejemplo:**
```python
def create_app():
    app = Flask(__name__)
    app.register_blueprint(contacts_bp)
    return app
```

### Flujo de una Request

```
HTTP Request (POST /contacts)
    ↓
routes/contacts.py (Blueprint endpoint)
    ↓
Validación de request.get_json()
    ↓
models/contact.py (ContactCreate con validación)
    ↓
services/contact_service.py (lógica de negocio)
    ↓
database.py (almacenamiento)
    ↓
services/contact_service.py (retorna Contact)
    ↓
routes/contacts.py (serializa a JSON)
    ↓
HTTP Response (201 Created + JSON)
```

## Consecuencias

### Positivas

1. **Testabilidad**
   - Service layer se puede testear sin Flask (tests unitarios puros)
   - Routes se testean con test_client (tests de integración)
   - Separación clara facilita mocking
   - Coverage alcanzó 94%

2. **Mantenibilidad**
   - Cada capa tiene una responsabilidad única
   - Cambios en persistencia no afectan rutas
   - Cambios en validación no afectan HTTP handling
   - Pylint score: 9.65/10

3. **Escalabilidad**
   - Fácil agregar nuevos endpoints (nuevo Blueprint)
   - Fácil agregar nuevos recursos (nueva clase Service)
   - Fácil reemplazar in-memory DB por SQLAlchemy

4. **Educativo**
   - Buen ejemplo de arquitectura limpia
   - Demuestra separación de responsabilidades
   - Patrones reutilizables

### Negativas

1. **Complejidad inicial**
   - Más archivos que una app monolítica
   - Requiere entender el flujo entre capas
   - Overhead para proyectos muy pequeños

2. **Boilerplate**
   - Más código para setup inicial
   - Múltiples imports

### Mitigaciones

- Documentación clara del flujo
- README con explicación de arquitectura
- Tests que demuestran cómo usar cada capa
- Comentarios y docstrings descriptivos

## Alternativas Descartadas

### Flask-RESTX

Descartado por:
- Añade dependencias extras
- Más complejo para un ejemplo demostrativo
- La generación automática de Swagger no era un requisito
- Queríamos demostrar Flask puro

Si en el futuro se necesita:
- Documentación OpenAPI automática
- Validación de schemas más robusta
- Múltiples versiones de API

Entonces Flask-RESTX sería una mejor opción.

### FastAPI

No aplicable porque el stack elegido es Flask, pero FastAPI sería superior para:
- Type checking automático
- Validación con Pydantic
- OpenAPI automático
- Performance (async)

## Validación

La decisión se validó mediante:

1. **Implementación completa**: API funcional con CRUD completo
2. **Tests**: 38 tests (14 unitarios + 14 integración + 10 BDD)
3. **Quality gates**: Todos pasaron (pylint, coverage, complexity)
4. **Métricas**:
   - Coverage: 94%
   - Pylint: 9.65/10
   - Complexity: A (promedio 2.5)
   - Maintainability: A en todos los módulos

## Notas

- La base de datos in-memory es solo para demostración
- En producción, reemplazar `app/database.py` con SQLAlchemy models
- El patrón de capas se mantiene igual independientemente del backend de datos

## Referencias

- [Flask Blueprints Documentation](https://flask.palletsprojects.com/en/3.0.x/blueprints/)
- [Flask Application Factories](https://flask.palletsprojects.com/en/3.0.x/patterns/appfactories/)
- [Clean Architecture in Python](https://www.cosmicpython.com/)
- Claude Dev Kit Framework Documentation

---

**Autor**: Claude Code (con validación humana)
**Última actualización**: 2026-02-16
