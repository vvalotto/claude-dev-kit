# TICKET-029: Crear Perfil flask-webapp.json

**Estado:** ✅ Completado
**Fecha Creación:** 2026-02-13
**Fecha Implementación:** 2026-02-14
**Estimación:** 1.5 horas
**Tiempo Real:** ~2 horas
**Prioridad:** Media
**Sprint:** Post-Sprint 2 (Extensión)

---

## Contexto

Después del análisis del proyecto `webapp_termostato` ubicado en `/Users/victor/PycharmProjects/webapp_termostato`, se identificó que:

1. **Flask Fullstack Webapp es un stack DIFERENTE de Flask REST API**
2. **No mapea bien** a los perfiles existentes:
   - ❌ `flask-rest.json` (TICKET-028) - Es API pura, sin frontend
   - ❌ `pyqt-mvc.json` - No es desktop app
   - ❌ `fastapi-rest.json` - Usa Flask, no FastAPI
   - ⚠️ `generic-python.json` - Funciona pero es demasiado genérico
3. **Tiene suficientes diferencias** con `flask-rest.json` para justificar un perfil propio
4. **Tenemos un proyecto real** de referencia para basarnos

---

## Objetivo

Crear el perfil `flask-webapp.json` para proyectos fullstack con Flask + Jinja2 templates + frontend integrado, basándose en el análisis del proyecto `webapp_termostato` y las mejores prácticas de Flask web apps.

---

## Análisis del Proyecto de Referencia

### Stack Identificado (webapp_termostato)

**Framework:** Flask 3.1.0 + Jinja2 + Vanilla JavaScript

**Arquitectura:** BFF (Backend for Frontend) + Server-Side Rendering
```
webapp/
├── __init__.py           # Application factory
├── routes.py             # HTTP routes + view functions
├── static/               # Frontend assets
│   ├── css/
│   ├── js/
│   │   ├── main.js      # Módulo principal
│   │   ├── api.js       # API client
│   │   ├── ui.js        # UI components
│   │   └── utils.js     # Utilities
│   └── images/
├── templates/            # Jinja2 templates
│   ├── base.html        # Layout base
│   ├── index.html       # Home page
│   ├── components/      # Componentes reutilizables
│   └── errors/          # Error pages
└── config.py            # Configuration object
```

**Patrones Identificados:**
- ✅ BFF (Backend for Frontend) - Webapp actúa como proxy a API backend
- ✅ Server-Side Rendering con Jinja2
- ✅ Vanilla JavaScript modular (sin frameworks frontend)
- ✅ Application Factory pattern
- ✅ Blueprint pattern
- ✅ Configuration object pattern
- ✅ API client pattern (requests a backend separado)

**Testing:**
- Framework: pytest
- Fixtures: Flask test client
- Tests solo de backend (templates rendering, routes)
- **NO hay tests de JavaScript** (frontend no testeado en el proyecto original)

**Características Clave:**
- **Puerto:** 5000 (webapp) → 5050 (app_termostato API)
- **Comunicación:** HTTP requests desde Flask webapp a API backend
- **Frontend:** Vanilla JavaScript ES6 modules
- **Templates:** Jinja2 con herencia (base.html → pages)
- **Forms:** Flask-WTF para formularios
- **Bootstrap:** Flask-Bootstrap para estilos

---

## Diferencias Flask REST vs Flask Webapp

| Aspecto | Flask REST (TICKET-028) | Flask Webapp (Este Ticket) |
|---------|-------------------------|----------------------------|
| **Propósito** | API backend pura | Aplicación fullstack |
| **Frontend** | No (consumido por otros) | Sí (templates + JS) |
| **Rendering** | JSON responses | Server-Side Rendering (Jinja2) |
| **Arquitectura** | Layered (API-Domain-Data) | BFF (Backend → API externa) |
| **Estructura** | `app/servicios/`, `app/general/`, `app/datos/` | `webapp/routes.py`, `webapp/templates/`, `webapp/static/` |
| **Patrón Principal** | Repository + Mapper | BFF + SSR |
| **Testing** | API endpoints (JSON) | Templates rendering + routes |
| **Dependencies** | Flask, flask-cors, flasgger | Flask, Jinja2, Flask-Bootstrap, Flask-WTF |
| **Complejidad** | Media | Media-Alta |
| **Use Case** | Backend para móvil/SPA | Webapp tradicional con servidor |

---

## Especificación del Perfil

### 1. Profile Metadata

```json
{
  "profile_metadata": {
    "name": "flask-webapp",
    "display_name": "Flask Fullstack Webapp + Jinja2 + Vanilla JS",
    "description": "Aplicaciones web fullstack con Flask, Server-Side Rendering (Jinja2) y frontend integrado",
    "extends": "config.json",
    "version": "1.0.0",
    "author": "Claude Dev Kit",
    "created": "2026-02-13",
    "target_stack": "Flask 2.0+ / 3.0+ + Jinja2 + Vanilla JavaScript",
    "architecture": "BFF (Backend for Frontend) + SSR"
  }
}
```

### 2. Variables Override

| Variable | Valor Base | Valor Flask Webapp | Justificación |
|----------|------------|-------------------|---------------|
| `architecture_pattern` | `generic` | `bff` | Flask webapp como proxy a backend API |
| `component_type` | `Component` | `Page` | Componentes son páginas web |
| `component_path` | `src/{name}/` | `webapp/templates/{name}/` | Templates organizadas por feature |
| `test_framework` | `pytest` | `pytest + Flask test client` | Testing de templates y routes |
| `base_class` | `object` | `Flask` para app factory | Application factory pattern |
| `domain_context` | `application` | `webapp` | Contexto de webapp (no API) |
| `project_root` | `.` | `webapp/` | Convención Flask fullstack |

### 3. Component Structure

**Estructura por Feature/Page:**

```json
"component_structure": {
  "page_feature": {
    "description": "Feature completo con template, ruta y assets",
    "base_path": "webapp/",
    "layers": {
      "routes": {
        "path": "webapp/routes.py",
        "description": "HTTP routes y view functions",
        "pattern": "Blueprint pattern",
        "responsibilities": [
          "Definir rutas HTTP (@app.route)",
          "Renderizar templates (render_template())",
          "Llamar API backend si necesario",
          "Manejo de forms (Flask-WTF)",
          "Manejo de errores HTTP"
        ]
      },
      "templates": {
        "path": "webapp/templates/{feature}/",
        "files": {
          "page": {
            "filename": "{feature}.html",
            "description": "Template Jinja2 para la página",
            "pattern": "Template inheritance (extends base.html)",
            "responsibilities": [
              "HTML markup de la página",
              "Bloques Jinja2 ({% block content %})",
              "Inclusión de componentes",
              "Data binding con {{ variable }}"
            ]
          },
          "components": {
            "path": "webapp/templates/components/",
            "description": "Componentes reutilizables (partials)",
            "examples": "navbar.html, footer.html, card.html"
          }
        }
      },
      "static": {
        "path": "webapp/static/",
        "files": {
          "javascript": {
            "path": "webapp/static/js/{feature}.js",
            "description": "Vanilla JavaScript module",
            "pattern": "ES6 modules",
            "responsibilities": [
              "Lógica de frontend del feature",
              "Event handlers",
              "DOM manipulation",
              "API calls (fetch/axios)"
            ]
          },
          "css": {
            "path": "webapp/static/css/{feature}.css",
            "description": "Estilos específicos del feature",
            "pattern": "CSS modular o Bootstrap overrides"
          }
        }
      },
      "backend_client": {
        "description": "API client para comunicación con backend",
        "files": {
          "api_client": {
            "filename": "webapp/api_client.py",
            "description": "Cliente HTTP para API backend",
            "pattern": "Singleton o dependency injection",
            "responsibilities": [
              "Requests HTTP a API externa",
              "Manejo de errores de red",
              "Transformación de responses",
              "Base URL configuration"
            ]
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
    "unit": "Tests unitarios de helpers/utils",
    "integration": "Tests de integración de routes + templates",
    "template": "Tests de rendering de templates",
    "slow": "Tests lentos (>1s, incluyen llamadas a API)"
  },
  "frontend_testing": {
    "note": "Frontend JavaScript NO se testea con pytest",
    "recommendation": "Usar Jest o Vitest si necesitas tests de JS"
  }
}
```

### 5. Flask Webapp-Specific Patterns

```json
"flask_webapp_patterns": {
  "application_factory": {
    "description": "Factory pattern para crear app",
    "pattern": "def create_app(config=None): ...",
    "file": "webapp/__init__.py",
    "includes": [
      "app.config.from_object()",
      "register_blueprints()",
      "init_extensions() (Bootstrap, WTF, etc.)"
    ]
  },
  "blueprints": {
    "description": "Organización modular con Flask Blueprints",
    "pattern": "bp = Blueprint('main', __name__)",
    "registration": "app.register_blueprint(bp)"
  },
  "template_inheritance": {
    "description": "Jinja2 template inheritance",
    "pattern": "{% extends 'base.html' %} ... {% block content %}",
    "file": "webapp/templates/base.html"
  },
  "static_files": {
    "description": "Servir archivos estáticos (CSS, JS, images)",
    "pattern": "{{ url_for('static', filename='css/style.css') }}",
    "organization": "Por tipo: static/css/, static/js/, static/images/"
  },
  "forms": {
    "description": "Flask-WTF para forms con validación",
    "pattern": "class LoginForm(FlaskForm): ...",
    "file": "webapp/forms.py"
  },
  "error_handling": {
    "description": "Custom error pages",
    "pattern": "@app.errorhandler(404)\\ndef not_found(error): return render_template('errors/404.html'), 404",
    "file": "webapp/routes.py"
  },
  "bff_pattern": {
    "description": "Backend for Frontend - proxy a API backend",
    "pattern": "Webapp llama API externa con requests/httpx",
    "example": "response = requests.get(f'{API_BASE_URL}/api/termostatos')",
    "file": "webapp/api_client.py"
  }
}
```

### 6. Dependencies

```json
"dependencies": {
  "required": [
    "Flask>=2.0.0",
    "Jinja2>=3.0.0",
    "Flask-WTF>=1.0.0",
    "WTForms>=3.0.0",
    "python-dotenv>=1.0.0",
    "requests>=2.28.0",
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "pytest-flask>=1.2.0"
  ],
  "recommended": [
    "Flask-Bootstrap>=4.0.0 (Bootstrap integration)",
    "Flask-Moment>=1.0.0 (Datetime formatting)",
    "flask-cors>=4.0.0 (si webapp llama APIs externas desde JS)",
    "httpx>=0.24.0 (alternativa async a requests)",
    "gunicorn>=20.0.0 (production server)"
  ],
  "development": [
    "pylint>=2.15.0",
    "radon>=5.1.0",
    "black>=22.0.0",
    "mypy>=1.0.0"
  ],
  "frontend": [
    "Sin dependencias npm (Vanilla JS)",
    "Bootstrap via CDN o Flask-Bootstrap",
    "Opcional: Jest/Vitest para tests de JS"
  ]
}
```

### 7. Quality Gates

Ajustes para Flask Webapp:

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
    "max_per_function": 10,
    "note": "Routes pueden ser más complejas si renderizan múltiples templates"
  },
  "maintainability_index": {
    "enabled": true,
    "min_score": 20
  },
  "coverage": {
    "enabled": true,
    "min_percent": 90.0,
    "note": "Coverage solo de Python (routes, api_client). JS no incluido."
  },
  "frontend_quality": {
    "note": "No automatizado en el perfil original",
    "recommendation": "Usar ESLint manualmente si agregás mucho JS"
  }
}
```

---

## Ejemplos de Código

### Ejemplo: Application Factory (Flask Webapp)

```python
# webapp/__init__.py
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect

bootstrap = Bootstrap()
csrf = CSRFProtect()

def create_app(config_name='default'):
    """Application factory pattern."""
    app = Flask(__name__)
    app.config.from_object(f'webapp.config.{config_name.capitalize()}Config')

    # Initialize extensions
    bootstrap.init_app(app)
    csrf.init_app(app)

    # Register blueprints
    from webapp.routes import main_bp
    app.register_blueprint(main_bp)

    return app
```

### Ejemplo: Routes + Template Rendering (Flask Webapp)

```python
# webapp/routes.py
from flask import Blueprint, render_template, request
from webapp.api_client import APIClient

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Home page."""
    return render_template('index.html', title='Home')

@main_bp.route('/termostatos')
def termostatos():
    """Lista de termostatos desde API backend."""
    api = APIClient()
    try:
        termostatos = api.get_termostatos()
        return render_template('termostatos/list.html',
                             termostatos=termostatos,
                             title='Termostatos')
    except Exception as e:
        return render_template('errors/500.html', error=str(e)), 500

@main_bp.route('/termostatos/<int:id>')
def termostato_detail(id):
    """Detalle de termostato."""
    api = APIClient()
    termostato = api.get_termostato(id)
    if not termostato:
        return render_template('errors/404.html'), 404
    return render_template('termostatos/detail.html',
                         termostato=termostato,
                         title=f'Termostato {id}')
```

### Ejemplo: API Client (BFF Pattern)

```python
# webapp/api_client.py
import requests
from typing import List, Optional, Dict

class APIClient:
    """Cliente para comunicación con API backend."""

    BASE_URL = "http://localhost:5050"

    def get_termostatos(self) -> List[Dict]:
        """Obtener lista de termostatos."""
        response = requests.get(f"{self.BASE_URL}/api/termostatos")
        response.raise_for_status()
        return response.json()

    def get_termostato(self, id: int) -> Optional[Dict]:
        """Obtener termostato por ID."""
        try:
            response = requests.get(f"{self.BASE_URL}/api/termostatos/{id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return None
            raise

    def update_temperatura(self, id: int, temperatura: float) -> Dict:
        """Actualizar temperatura objetivo."""
        response = requests.put(
            f"{self.BASE_URL}/api/termostatos/{id}/temperatura",
            json={"temperatura_objetivo": temperatura}
        )
        response.raise_for_status()
        return response.json()
```

### Ejemplo: Jinja2 Template

```html
<!-- webapp/templates/termostatos/list.html -->
{% extends "base.html" %}

{% block title %}{{ title }}{% endblock %}

{% block content %}
<div class="container">
    <h1>Termostatos</h1>

    {% if termostatos %}
    <div class="row">
        {% for termo in termostatos %}
        <div class="col-md-4">
            {% include 'components/termostato_card.html' %}
        </div>
        {% endfor %}
    </div>
    {% else %}
    <p>No hay termostatos disponibles.</p>
    {% endif %}
</div>
{% endblock %}

{% block scripts %}
<script src="{{ url_for('static', filename='js/termostatos.js') }}"></script>
{% endblock %}
```

### Ejemplo: Vanilla JavaScript Module

```javascript
// webapp/static/js/termostatos.js
import { fetchJSON } from './api.js';
import { showError, showSuccess } from './ui.js';

class TermostatosManager {
    constructor() {
        this.apiBaseUrl = '/api/termostatos';
        this.init();
    }

    init() {
        // Event listeners
        document.querySelectorAll('.btn-update-temp').forEach(btn => {
            btn.addEventListener('click', (e) => this.handleUpdateTemp(e));
        });
    }

    async handleUpdateTemp(event) {
        const id = event.target.dataset.termoId;
        const newTemp = document.getElementById(`temp-input-${id}`).value;

        try {
            await fetchJSON(`${this.apiBaseUrl}/${id}/temperatura`, {
                method: 'PUT',
                body: JSON.stringify({ temperatura_objetivo: parseFloat(newTemp) })
            });
            showSuccess('Temperatura actualizada');
        } catch (error) {
            showError(`Error: ${error.message}`);
        }
    }
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    new TermostatosManager();
});
```

### Ejemplo: Testing (Flask Webapp)

```python
# tests/conftest.py
import pytest
from webapp import create_app

@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = create_app('testing')
    return app

@pytest.fixture
def client(app):
    """Create Flask test client."""
    return app.test_client()

# tests/test_routes.py
def test_index_page(client):
    """Test home page renders."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Home' in response.data

def test_termostatos_list(client, mocker):
    """Test termostatos list page."""
    # Mock API client
    mock_api = mocker.patch('webapp.routes.APIClient')
    mock_api.return_value.get_termostatos.return_value = [
        {'id': 1, 'nombre': 'Termo1', 'temperatura_actual': 20.0}
    ]

    response = client.get('/termostatos')
    assert response.status_code == 200
    assert b'Termostatos' in response.data
    assert b'Termo1' in response.data

def test_termostato_detail_not_found(client, mocker):
    """Test termostato detail 404."""
    mock_api = mocker.patch('webapp.routes.APIClient')
    mock_api.return_value.get_termostato.return_value = None

    response = client.get('/termostatos/999')
    assert response.status_code == 404
```

---

## Comparación de Perfiles (Con Flask Webapp)

| Característica | PyQt MVC | FastAPI REST | Flask REST | Flask Webapp | Generic |
|----------------|----------|--------------|------------|--------------|---------|
| **Framework** | PyQt6 | FastAPI | Flask | Flask | Ninguno |
| **Arquitectura** | MVC | Layered (3) | Layered (3) | BFF + SSR | Flexible |
| **Frontend** | Qt UI | No | No | **Sí (Jinja2 + JS)** | No |
| **Files/Feature** | 3 (M+V+C) | 5 | 3-4 | **4-5 (route+template+css+js)** | 1-2 |
| **Async** | No | Sí | No | No | Opcional |
| **Test Framework** | pytest-qt | pytest + httpx | pytest + Flask | pytest + Flask | pytest |
| **Fixtures** | qapp, qtbot | async_client, db | app, client | app, client | Ninguno |
| **Dependencies** | 10+ | 20+ | 8+ | **12+** | 2 |
| **Pylint Min** | 8.0 | 8.5 | 8.0 | 8.0 | 8.0 |
| **Coverage Min** | 90% | 95% | 95% | **90%** | 95% |
| **Use Case** | Desktop UI | APIs async | APIs sync | **Webapps fullstack** | Todo lo demás |

---

## Criterios de Aceptación

- [x] Archivo `flask-webapp.json` creado en `skills/implement-us/customizations/` ✅
- [x] JSON sintácticamente válido ✅
- [x] 7 variables override definidas ✅
- [x] Component structure en capas (routes, templates, static, api_client) ✅
- [x] Test framework config con fixtures de Flask ✅
- [x] Flask webapp-specific patterns documentados ✅
- [x] Dependencies completas (Flask, Jinja2, Flask-Bootstrap, Flask-WTF, requests, pytest) ✅
- [x] Quality gates apropiados (coverage 90% - solo backend) ✅
- [x] Ejemplos de código incluidos ✅
- [x] Documentación del ticket completa ✅
- [x] README.md actualizado con el nuevo perfil ✅
- [x] Tabla comparativa actualizada ✅
- [x] Phases actualizadas con ejemplos Flask Webapp ✅

---

## Tareas de Implementación

### 1. Crear archivo JSON (~40 min)
- [ ] Profile metadata
- [ ] Variables override (7 variables)
- [ ] Component structure (routes, templates, static, api_client)
- [ ] Test framework config
- [ ] Flask webapp patterns
- [ ] Dependencies (backend + frontend)
- [ ] Quality gates

### 2. Documentación (~40 min)
- [ ] Completar este ticket con implementación real
- [ ] Actualizar README.md
- [ ] Agregar a tabla comparativa
- [ ] Ejemplos de código (routes, templates, JS)
- [ ] Diferenciar de flask-rest.json

### 3. Validación (~10 min)
- [ ] Validar sintaxis JSON
- [ ] Verificar estructura
- [ ] Testing manual
- [ ] Commit y documentación

---

## Referencias

### Proyecto de Referencia
- **Ubicación:** `/Users/victor/PycharmProjects/webapp_termostato`
- **Análisis completo:** Ver output del agente Explore
- **Características clave:**
  - Flask 3.1.0
  - Jinja2 templates + Vanilla JavaScript
  - BFF pattern (proxy a app_termostato API)
  - Server-Side Rendering
  - Flask-Bootstrap + Flask-WTF
  - Estructura: webapp/ con templates/ y static/

### Flask Best Practices
- Flask Templates: https://flask.palletsprojects.com/templates/
- Jinja2 Documentation: https://jinja.palletsprojects.com/
- Flask-WTF: https://flask-wtf.readthedocs.io/
- Flask-Bootstrap: https://pythonhosted.org/Flask-Bootstrap/

### Perfiles Existentes
- `config.json` - Base genérica
- `pyqt-mvc.json` - PyQt6 + MVC
- `fastapi-rest.json` - FastAPI + async
- `flask-rest.json` (TICKET-028) - Flask REST API
- `generic-python.json` - Python genérico

---

## Estimación

- **Tiempo estimado:** 1.5 horas
- **Complejidad:** Media-Alta (más complejo que flask-rest por frontend)
- **Basado en:** Proyecto real (webapp_termostato)
- **Valor:** Alto (Flask webapps tradicionales siguen siendo muy comunes)

---

## Diferencias Clave con TICKET-028 (flask-rest)

| Aspecto | TICKET-028 (flask-rest) | TICKET-029 (flask-webapp) |
|---------|------------------------|---------------------------|
| **Propósito** | API backend pura | Webapp fullstack |
| **Frontend** | ❌ No | ✅ Sí (templates + JS) |
| **Rendering** | JSON | HTML (Jinja2) |
| **Arquitectura** | Layered (3 capas) | BFF + SSR |
| **Estructura** | servicios/general/datos | routes/templates/static |
| **Testing** | API endpoints | Templates + routes |
| **Coverage** | 95% | 90% (solo backend) |
| **Dependencies** | 8+ | 12+ (incluye frontend) |
| **Complejidad** | Media | Media-Alta |

**Ambos son necesarios** porque cubren casos de uso completamente diferentes:
- **flask-rest:** Backend API para consumir desde móvil/SPA/otros servicios
- **flask-webapp:** Aplicación web tradicional con servidor renderizando HTML

---

## Próximos Pasos Después de Este Ticket

Con Flask REST y Flask Webapp cubiertos, tendríamos **5 perfiles sólidos** que cubren la mayoría de casos:

1. ✅ PyQt MVC - Desktop apps
2. ✅ FastAPI REST - APIs async modernas
3. 🆕 Flask REST (TICKET-028) - APIs sync tradicionales
4. 🆕 Flask Webapp (TICKET-029) - Webapps fullstack tradicionales
5. ✅ Generic Python - Todo lo demás

**Cobertura estimada:** ~85-95% de proyectos Python comunes

---

## Resultado de Implementación

### Archivo Creado

**Ubicación:** `skills/implement-us/customizations/flask-webapp.json`
**Líneas:** ~1100 líneas
**Tamaño:** ~44KB

### Estructura Implementada

**Secciones completadas:**
1. ✅ Profile metadata (referencia a webapp_termostato)
2. ✅ Variables override (7 variables + async_support)
3. ✅ Component structure (4 capas: routes, templates, static, api_client)
4. ✅ Test framework config (pytest + Flask client + mock)
5. ✅ Flask webapp patterns (6 patterns: factory, templates, blueprints, static, forms, BFF)
6. ✅ Dependencies (required, recommended, development, frontend)
7. ✅ Quality gates (Pylint 8.0, CC ≤10, MI ≥20, Coverage 90%)
8. ✅ Design patterns (5 patterns: BFF, SSR, Factory, Blueprint, Template Inheritance)
9. ✅ Webapp conventions (routing, templates, static, forms, errors, API calls)
10. ✅ Documentation (readme, code docs, architecture)

### Características Destacadas

**Variables override implementadas:**
- `architecture_pattern`: bff (Backend for Frontend)
- `component_type`: Page
- `component_path`: webapp/templates/{name}/
- `test_framework`: pytest + Flask client + mock
- `base_class`: Flask, FlaskForm
- `domain_context`: webapp
- `project_root`: webapp/
- `async_support`: false (sync)

**Flask webapp patterns documentados:**
1. **Application Factory** - def create_app(config)
2. **Template Inheritance** - Jinja2 base.html → pages
3. **Blueprints** - Organización modular
4. **Static Files** - url_for('static', ...)
5. **Forms** - Flask-WTF con CSRF
6. **BFF Pattern** - Webapp → API Backend

**Component structure (4 capas):**
- **Routes:** routes.py (view functions + BFF calls)
- **Templates:** Jinja2 SSR (base + features + components + errors)
- **Static:** JavaScript ES6 modules + CSS + images
- **Backend Client:** api_client.py (BFF pattern con requests)

**Test framework:**
- Fixtures: app, client
- Markers: unit, integration, template, slow, bdd
- Frontend testing: NO (JavaScript no testeado con pytest)
- Estructura: tests/unit/, tests/integration/, tests/bdd/

**Quality gates:**
- Pylint: ≥8.0
- Cyclomatic Complexity: ≤10
- Maintainability Index: ≥20
- Coverage: ≥90% (solo backend Python, JS no incluido)

**Diferencia clave con flask-rest:**
- **flask-rest:** API pura (JSON), layered 3 capas, coverage 95%
- **flask-webapp:** Fullstack (HTML+JS), BFF+SSR, coverage 90% (solo backend)

---

### Phases Actualizadas (4 commits)

**1. README.md (commit 5304651)**
- Agregar Flask Webapp a frameworks soportados
- Nueva sección Flask Webapp con descripción BFF+SSR
- Tabla comparativa con 5 perfiles
- Tabla de variables parametrizadas actualizada
- Instalación con opción flask-webapp
- Validación de 5 perfiles

**2. Phase 2 - Planning (commit ac09fc0)**
- Ejemplo 4 agregado: Plan Flask Webapp (~90 líneas)
- Página de productos fullstack (14 tareas, 2h 15min)
- Backend: routes + api_client (BFF pattern)
- Frontend: templates (Jinja2) + JavaScript + CSS
- Forms con Flask-WTF (opcional)
- Tests de routes + api_client con mocking

**3. Phase 3 - Implementation (commit 478e054)**
- 3 ejemplos completos de código Flask Webapp (~290 líneas):
  - Routes: View functions con BFF pattern (GET, POST, error handlers)
  - Template Jinja2: SSR con herencia, loops, components, paginación
  - JavaScript: Vanilla JS ES6 module con event handlers, fetch, DOM manipulation

**4. Phase 4 - Unit Tests (commit d356075)**
- 2 ejemplos completos de tests (~220 líneas):
  - Test de Routes: Template rendering + mocking APIClient (7 test methods)
  - Test de API Client: BFF pattern con requests_mock (5 test methods)

**5. Phase 7 - Quality Gates (commit 4c8f03b)**
- Tabla comparativa actualizada con Flask Webapp
- Sección Flask Webapp con justificación de umbrales
- Coverage 90% (no 95%) - solo backend Python
- Nota sobre frontend testing (Jest/Vitest opcional)

---

### Resumen Final de Implementación

**Archivos creados/modificados:**
1. ✅ `flask-webapp.json` (1 archivo nuevo)
2. ✅ `README.md` (1 archivo modificado)
3. ✅ `phase-2-planning.md` (1 archivo modificado)
4. ✅ `phase-3-implementation.md` (1 archivo modificado)
5. ✅ `phase-4-unit-tests.md` (1 archivo modificado)
6. ✅ `phase-7-quality-gates.md` (1 archivo modificado)
7. ✅ `TICKET-029-flask-webapp.md` (1 archivo modificado - este)

**Total:**
- **Commits:** 6 commits
- **Archivos:** 7 archivos creados/modificados
- **Líneas agregadas:** ~2,000 líneas totales
  - flask-webapp.json: ~1100 líneas
  - Phases: ~900 líneas (ejemplos, documentación)

**Tiempo total:** ~2 horas (estimado 1.5h en plan original)
**Eficiencia:** 133% del estimado (más complejo que flask-rest por frontend)

---

## Estado Final del Sistema

**Perfiles disponibles:** 5/5 (100%) 🎉
1. ✅ **pyqt-mvc.json** - Desktop apps PyQt6
2. ✅ **fastapi-rest.json** - APIs async FastAPI
3. ✅ **flask-rest.json** - APIs sync Flask (TICKET-028)
4. ✅ **flask-webapp.json** - Webapps fullstack Flask ← **COMPLETADO**
5. ✅ **generic-python.json** - Python genérico

**Cobertura estimada:** ~85-95% de proyectos Python comunes ✅

**Sistema completo:**
- 1 config base (config.json)
- 5 perfiles funcionales
- 10 phases documentadas
- Ejemplos exhaustivos por stack
- Quality gates por perfil

---

**TICKET-029 COMPLETADO AL 100% ✅**
**SISTEMA DE PERFILES COMPLETO - 5 PERFILES FUNCIONALES 🎉**
