# TICKET-028: Crear Perfil flask-rest.json

**Estado:** 📋 Pendiente
**Fecha Creación:** 2026-02-13
**Estimación:** 1 hora
**Prioridad:** Media
**Sprint:** Post-Sprint 2 (Extensión)

---

## Contexto

Después del análisis del proyecto `app_termostato` ubicado en `/Users/victor/PycharmProjects/app_termostato`, se identificó que:

1. **Flask REST API es un stack MUY común** en la comunidad Python
2. **No mapea bien** a los perfiles existentes:
   - ❌ `pyqt-mvc.json` - No tiene GUI
   - ❌ `fastapi-rest.json` - Usa Flask, no FastAPI (diferencias significativas)
   - ⚠️ `generic-python.json` - Funciona pero es demasiado genérico
3. **Tiene suficientes diferencias** con FastAPI para justificar un perfil propio
4. **Tenemos un proyecto real** de referencia para basarnos

---

## Objetivo

Crear el perfil `flask-rest.json` para proyectos de APIs REST con Flask y arquitectura en capas, basándose en el análisis del proyecto `app_termostato` y las mejores prácticas de Flask.

---

## Análisis del Proyecto de Referencia

### Stack Identificado (app_termostato)

**Framework:** Flask 3.1.0 + Flask-CORS + Flasgger

**Arquitectura:** 3 capas (Layered)
```
app/
├── servicios/          # API Layer (Routes/Controllers)
│   ├── api.py         # Flask endpoints
│   └── errors.py      # Error handling
├── general/           # Domain Layer (Business Logic)
│   └── termostato.py  # Core model
└── datos/            # Data Access Layer
    ├── repositorio.py    # Interface (ABC)
    ├── memoria.py        # In-memory implementation
    ├── persistidor.py    # Persistence interface
    └── mapper.py         # Data mapping
```

**Patrones Identificados:**
- ✅ Singleton pattern (configurador global)
- ✅ Abstract Base Classes (ABC) para interfaces
- ✅ Repository pattern
- ✅ Mapper pattern
- ✅ Dependency Injection básico
- ✅ Configuration object pattern

**Testing:**
- Framework: pytest
- Fixtures: Flask test client
- Coverage: 100%
- Tests: 62 (35 unitarios + 27 integración)

**Quality Gates:**
- Pylint: 8.41/10
- Complejidad Ciclomática: 1.75
- Índice Mantenibilidad: 92.21/100
- Coverage: 100%

---

## Diferencias Flask vs FastAPI

| Aspecto | Flask | FastAPI |
|---------|-------|---------|
| **Routing** | `@app.route('/users')` | `@router.get('/users')` |
| **Async** | No (sync only) | Sí (async/await) |
| **Validation** | Manual o Flask-RESTX | Pydantic (nativo) |
| **OpenAPI** | Flasgger/Flask-RESTX | Nativo |
| **DI** | Blueprints/Extensions | Depends() |
| **Testing** | Flask test client (sync) | httpx AsyncClient |
| **Request Body** | `request.get_json()` | Pydantic models |
| **Response** | `jsonify()` | Return directo |
| **Config** | Flask config object | Settings (Pydantic) |

---

## Especificación del Perfil

### 1. Profile Metadata

```json
{
  "profile_metadata": {
    "name": "flask-rest",
    "display_name": "Flask REST API + Layered Architecture",
    "description": "APIs REST con Flask, arquitectura en capas (API-Domain-Data) y sync/threading",
    "extends": "config.json",
    "version": "1.0.0",
    "author": "Claude Dev Kit",
    "created": "2026-02-13",
    "target_stack": "Flask 2.0+ / 3.0+ + Python 3.8+",
    "architecture": "Layered (Servicios → General → Datos)"
  }
}
```

### 2. Variables Override

| Variable | Valor Base | Valor Flask | Justificación |
|----------|------------|-------------|---------------|
| `architecture_pattern` | `generic` | `layered` | Flask REST típicamente usa capas |
| `component_type` | `Component` | `Endpoint` | Componentes son endpoints REST |
| `component_path` | `src/{name}/` | `app/{layer}/{name}/` | Estructura por capas |
| `test_framework` | `pytest` | `pytest + Flask test client` | Testing sync con Flask |
| `base_class` | `object` | `ABC` para repositorios | Interfaces comunes |
| `domain_context` | `application` | `servicios` | Capa de API |
| `project_root` | `.` | `app/` | Convención Flask |

### 3. Component Structure

**Estructura por Feature en Capas:**

```json
"component_structure": {
  "api_feature": {
    "description": "Feature completo con arquitectura en capas",
    "base_path": "app/",
    "layers": {
      "servicios": {
        "path": "app/servicios/{feature}/",
        "files": {
          "api": {
            "filename": "api.py",
            "description": "Flask endpoints y routing",
            "pattern": "Blueprint pattern",
            "responsibilities": [
              "Definir rutas HTTP (@app.route)",
              "Validación de request (request.get_json())",
              "Serialización con jsonify()",
              "Manejo de errores HTTP"
            ]
          },
          "errors": {
            "filename": "errors.py",
            "description": "Error handlers específicos del feature",
            "pattern": "Custom exceptions + @app.errorhandler"
          }
        }
      },
      "general": {
        "path": "app/general/{feature}/",
        "files": {
          "modelo": {
            "filename": "{feature}.py",
            "description": "Modelo de dominio (business logic)",
            "pattern": "Dataclass o class con lógica",
            "responsibilities": [
              "Lógica de negocio del feature",
              "Validaciones de dominio",
              "Reglas de negocio",
              "Sin dependencias de Flask"
            ]
          }
        }
      },
      "datos": {
        "path": "app/datos/{feature}/",
        "files": {
          "repositorio": {
            "filename": "repositorio.py",
            "description": "Interface abstracta (ABC)",
            "pattern": "ABC + abstract methods"
          },
          "implementacion": {
            "filename": "{storage}.py",
            "description": "Implementación concreta (memoria, json, db)",
            "examples": "memoria.py, persistidor_json.py, db.py"
          },
          "mapper": {
            "filename": "mapper.py",
            "description": "Conversión entre modelos y DTOs",
            "optional": true
          }
        }
      }
    }
  }
}
```

### 4. Test Framework Config

```json
"test_framework_config": {
  "runner": "pytest",
  "plugins": ["pytest-cov", "pytest-flask"],
  "fixtures_path": "tests/conftest.py",
  "required_fixtures": {
    "app": {
      "description": "Flask app instance para tests",
      "scope": "module",
      "example": "return create_app(config='testing')"
    },
    "client": {
      "description": "Flask test client para requests HTTP",
      "scope": "function",
      "example": "return app.test_client()"
    }
  },
  "markers": {
    "unit": "Tests unitarios de dominio/repositories",
    "integration": "Tests de integración de endpoints",
    "api": "Tests de API HTTP (requieren client)",
    "slow": "Tests lentos (>1s)"
  }
}
```

### 5. Flask-Specific Patterns

```json
"flask_patterns": {
  "blueprints": {
    "description": "Organización modular con Flask Blueprints",
    "pattern": "bp = Blueprint('feature', __name__, url_prefix='/api/feature')",
    "registration": "app.register_blueprint(bp)"
  },
  "application_factory": {
    "description": "Factory pattern para crear app",
    "pattern": "def create_app(config=None): ...",
    "file": "app/__init__.py"
  },
  "configuration": {
    "description": "Flask config object",
    "pattern": "app.config.from_object('config.DevelopmentConfig')",
    "hierarchy": "BaseConfig → DevelopmentConfig/ProductionConfig/TestingConfig"
  },
  "error_handling": {
    "description": "Centralized error handlers",
    "pattern": "@app.errorhandler(404)\ndef not_found(error): ...",
    "file": "app/servicios/errors.py"
  }
}
```

### 6. Dependencies

```json
"dependencies": {
  "required": [
    "Flask>=2.0.0",
    "flask-cors>=4.0.0",
    "python-dotenv>=1.0.0",
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0"
  ],
  "recommended": [
    "flasgger>=0.9.7 (OpenAPI/Swagger docs)",
    "flask-restx (REST API framework)",
    "marshmallow (serialization)",
    "gunicorn (production server)"
  ],
  "development": [
    "pylint>=2.15.0",
    "radon>=5.1.0",
    "black>=22.0.0",
    "mypy>=1.0.0"
  ]
}
```

### 7. Quality Gates

Ajustes para Flask REST:

```json
"quality_gates": {
  "pylint": {
    "enabled": true,
    "min_score": 8.0,
    "disable_checks": [
      "too-few-public-methods",
      "invalid-name"
    ]
  },
  "cyclomatic_complexity": {
    "enabled": true,
    "max_per_function": 10
  },
  "maintainability_index": {
    "enabled": true,
    "min_score": 25
  },
  "coverage": {
    "enabled": true,
    "min_percent": 95.0
  }
}
```

---

## Ejemplos de Código

### Ejemplo: API Endpoint (Flask)

```python
# app/servicios/users/api.py
from flask import Blueprint, request, jsonify
from app.general.users import UserService
from app.servicios.errors import NotFoundError

bp = Blueprint('users', __name__, url_prefix='/api/users')

@bp.route('/', methods=['GET'])
def get_users():
    """Obtener todos los usuarios."""
    service = UserService()
    users = service.get_all()
    return jsonify([user.to_dict() for user in users]), 200

@bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Obtener usuario por ID."""
    service = UserService()
    user = service.get_by_id(user_id)
    if not user:
        raise NotFoundError(f"User {user_id} not found")
    return jsonify(user.to_dict()), 200

@bp.route('/', methods=['POST'])
def create_user():
    """Crear nuevo usuario."""
    data = request.get_json()
    service = UserService()
    user = service.create(data)
    return jsonify(user.to_dict()), 201
```

### Ejemplo: Repository Pattern (Flask)

```python
# app/datos/users/repositorio.py
from abc import ABC, abstractmethod
from typing import List, Optional

class UserRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[User]:
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def create(self, user: User) -> User:
        pass

# app/datos/users/memoria.py
class UserRepositoryMemory(UserRepository):
    def __init__(self):
        self._users: List[User] = []

    def get_all(self) -> List[User]:
        return self._users.copy()

    def get_by_id(self, user_id: int) -> Optional[User]:
        return next((u for u in self._users if u.id == user_id), None)

    def create(self, user: User) -> User:
        self._users.append(user)
        return user
```

### Ejemplo: Testing (Flask)

```python
# tests/conftest.py
import pytest
from app import create_app

@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = create_app(config='testing')
    return app

@pytest.fixture
def client(app):
    """Create Flask test client."""
    return app.test_client()

# tests/test_users_api.py
def test_get_users(client):
    """Test GET /api/users."""
    response = client.get('/api/users/')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_create_user(client):
    """Test POST /api/users."""
    data = {'name': 'John', 'email': 'john@example.com'}
    response = client.post('/api/users/', json=data)
    assert response.status_code == 201
    assert response.json['name'] == 'John'
```

---

## Comparación de Perfiles

| Característica | PyQt MVC | FastAPI REST | Flask REST | Generic |
|----------------|----------|--------------|------------|---------|
| **Framework** | PyQt6 | FastAPI | Flask | Ninguno |
| **Arquitectura** | MVC | Layered (3) | Layered (3) | Flexible |
| **Files/Feature** | 3 (M+V+C) | 5 | 3-4 | 1-2 |
| **Async** | No | Sí | No | Opcional |
| **Test Framework** | pytest-qt | pytest + httpx | pytest + Flask client | pytest |
| **Fixtures** | qapp, qtbot | async_client, db | app, client | Ninguno |
| **OpenAPI** | - | Nativo | Flasgger | - |
| **DI** | Factory | Depends() | Blueprints | - |
| **Pylint Min** | 8.0 | 8.5 | 8.0 | 8.0 |
| **Coverage Min** | 90% | 95% | 95% | 95% |
| **Use Case** | Desktop UI | APIs async | APIs sync | Todo lo demás |

---

## Criterios de Aceptación

- [ ] Archivo `flask-rest.json` creado en `skills/implement-us/customizations/`
- [ ] JSON sintácticamente válido
- [ ] 8 variables override definidas
- [ ] Component structure en capas (servicios, general, datos)
- [ ] Test framework config con fixtures de Flask
- [ ] Flask-specific patterns documentados
- [ ] Dependencies completas (Flask, flask-cors, flasgger, pytest)
- [ ] Quality gates apropiados
- [ ] Ejemplos de código incluidos
- [ ] Documentación del ticket completa
- [ ] README.md actualizado con el nuevo perfil
- [ ] Tabla comparativa actualizada

---

## Tareas de Implementación

### 1. Crear archivo JSON (~30 min)
- [ ] Profile metadata
- [ ] Variables override (8 variables)
- [ ] Component structure (3 capas)
- [ ] Test framework config
- [ ] Flask patterns
- [ ] Dependencies
- [ ] Quality gates

### 2. Documentación (~20 min)
- [ ] Completar este ticket con implementación real
- [ ] Actualizar README.md
- [ ] Agregar a tabla comparativa
- [ ] Ejemplos de código

### 3. Validación (~10 min)
- [ ] Validar sintaxis JSON
- [ ] Verificar estructura
- [ ] Testing manual
- [ ] Commit y documentación

---

## Referencias

### Proyecto de Referencia
- **Ubicación:** `/Users/victor/PycharmProjects/app_termostato`
- **Análisis completo:** Ver output del agente Explore (agent a8327ea)
- **Características clave:**
  - Flask 3.1.0
  - Arquitectura en 3 capas
  - Repository + Mapper patterns
  - Singleton pattern (Configurador)
  - ABC interfaces
  - Coverage 100%, Pylint 8.41/10

### Flask Best Practices
- Flask Blueprints: https://flask.palletsprojects.com/patterns/blueprints/
- Application Factory: https://flask.palletsprojects.com/patterns/appfactories/
- Testing Flask: https://flask.palletsprojects.com/testing/

### Perfiles Existentes
- `config.json` - Base genérica
- `pyqt-mvc.json` - PyQt6 + MVC
- `fastapi-rest.json` - FastAPI + async
- `generic-python.json` - Python genérico

---

## Estimación

- **Tiempo estimado:** 1 hora
- **Complejidad:** Media (similar a otros perfiles)
- **Basado en:** Proyecto real (app_termostato)
- **Valor:** Alto (Flask es muy común)

---

## Próximos Pasos Después de Este Ticket

Con Flask REST cubierto, tendríamos **4 perfiles sólidos** que cubren la mayoría de casos:

1. ✅ PyQt MVC - Desktop apps
2. ✅ FastAPI REST - APIs async modernas
3. 🆕 Flask REST - APIs sync tradicionales
4. ✅ Generic Python - Todo lo demás

**Cobertura estimada:** ~80-90% de proyectos Python comunes

---

**Ticket listo para implementación cuando decidas proceder.**
