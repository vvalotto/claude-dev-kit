# Skill: implement-us - Documentación Técnica

Documentación técnica de la arquitectura y estructura interna del skill.

> **Para usuarios:** Ver [docs/skills/implement-us.md](../../docs/skills/implement-us.md)

---

## 📋 Descripción

El skill `implement-us` guía paso a paso la implementación de una Historia de Usuario en proyectos Python, adaptándose automáticamente al stack tecnológico mediante perfiles de configuración.

**Características:**
- ✅ Framework-agnostic (PyQt, FastAPI, Flask REST, Flask Webapp, Python genérico)
- ✅ 10 fases de implementación (Fase 0: Validación hasta Fase 9: Reporte Final)
- ✅ Generación automática de BDD, tests, documentación
- ✅ Quality gates integrados (Pylint, CC, MI, Coverage)
- ✅ Time tracking automático
- ✅ Sistema de perfiles personalizables

---

## 🚀 Uso

```bash
/implement-us US-001
/implement-us US-001 --producto mi_producto
/implement-us US-001 --skip-bdd
```

---

## 📁 Estructura

```
skills/implement-us/
├── skill.md                   # Orquestador principal
├── config.json                # Configuración base genérica
├── phases/                    # Agentes especializados por fase
│   ├── phase-0-validation.md
│   ├── phase-1-bdd.md
│   ├── phase-2-planning.md
│   ├── phase-3-implementation.md
│   ├── phase-4-unit-tests.md
│   ├── phase-5-integration-tests.md
│   ├── phase-6-bdd-validation.md
│   ├── phase-7-quality-gates.md
│   ├── phase-8-documentation.md
│   └── phase-9-final-report.md
├── customizations/            # Perfiles específicos por stack
│   ├── pyqt-mvc.json
│   ├── fastapi-rest.json
│   ├── flask-rest.json
│   ├── flask-webapp.json
│   └── generic-python.json
└── README.md                  # Este archivo
```

---

## 🎯 Perfiles Disponibles

### 1. PyQt MVC (`pyqt-mvc.json`)

**Para:** Aplicaciones desktop con PyQt6 + arquitectura MVC

**Características:**
- Arquitectura MVC estricta (modelo.py, vista.py, controlador.py)
- Factory pattern para creación de componentes
- Coordinator pattern para comunicación entre paneles
- Testing con pytest-qt (fixtures: qapp, qtbot)
- Quality gates ajustados para UI (coverage 90%)

**Cuándo usar:**
- ✅ Aplicaciones desktop con PyQt6
- ✅ Necesitas separación MVC
- ✅ Componentes UI (paneles, diálogos, widgets)

**Ejemplo de estructura generada:**
```
app/presentacion/paneles/display/
├── modelo.py       # Dataclass inmutable
├── vista.py        # QWidget con UI
├── controlador.py  # Lógica de negocio
└── __init__.py
```

---

### 2. FastAPI REST (`fastapi-rest.json`)

**Para:** APIs REST con FastAPI + arquitectura en capas

**Características:**
- Arquitectura en capas (router → service → repository)
- Async/await por defecto
- Dependency injection con FastAPI Depends()
- Testing async con httpx
- Quality gates elevados (Pylint 8.5, MI 25, coverage 95%)
- OpenAPI automática

**Cuándo usar:**
- ✅ APIs REST con FastAPI
- ✅ Necesitas async/await
- ✅ Arquitectura en capas

**Ejemplo de estructura generada:**
```
app/api/users/
├── router.py       # Endpoints HTTP
├── service.py      # Lógica de negocio
├── repository.py   # Acceso a datos
├── schemas.py      # Pydantic DTOs
├── models.py       # SQLAlchemy ORM
└── __init__.py
```

---

### 3. Flask REST (`flask-rest.json`)

**Para:** APIs REST con Flask + arquitectura en capas (sync)

**Características:**
- Arquitectura en capas (servicios → general → datos)
- Sync/threading (no async)
- Repository + Mapper patterns con ABC interfaces
- Testing sync con Flask test client
- Quality gates basados en proyecto real (Pylint 8.0, MI 25, coverage 95%)
- OpenAPI/Swagger con Flasgger

**Cuándo usar:**
- ✅ APIs REST con Flask (sync)
- ✅ Migración desde Flask existente
- ✅ No necesitas async/await
- ✅ Arquitectura en capas tradicional

**Ejemplo de estructura generada:**
```
app/
├── servicios/{feature}/    # API Layer
│   ├── api.py             # Flask endpoints (blueprints)
│   └── errors.py          # Error handlers
├── general/{feature}/      # Domain Layer
│   └── {feature}.py       # Business logic
└── datos/{feature}/        # Data Layer
    ├── repositorio.py     # ABC interface
    ├── memoria.py         # In-memory implementation
    └── mapper.py          # Data mapping
```

---

### 4. Flask Webapp (`flask-webapp.json`)

**Para:** Aplicaciones web fullstack con Flask + Jinja2 + JavaScript

**Características:**
- BFF (Backend for Frontend) + Server-Side Rendering
- Flask + Jinja2 templates + Vanilla JavaScript (ES6 modules)
- Arquitectura: routes → templates → static → api_client
- Testing con Flask test client + mocking
- Quality gates: Coverage 90% (solo backend Python, JS no incluido)
- Templates con herencia (base.html → pages)
- Frontend integrado (CSS + JS modular)

**Cuándo usar:**
- ✅ Webapps tradicionales fullstack con servidor
- ✅ Necesitas Server-Side Rendering (SEO-friendly)
- ✅ Backend actúa como BFF (proxy a API externa)
- ✅ Frontend simple con Vanilla JavaScript (sin SPA frameworks)

**Ejemplo de estructura generada:**
```
webapp/
├── __init__.py          # Application factory
├── routes.py            # HTTP routes + view functions
├── api_client.py        # BFF - cliente para API backend
├── forms.py             # Flask-WTF forms (opcional)
├── templates/           # Jinja2 SSR
│   ├── base.html       # Layout base
│   ├── index.html      # Home page
│   ├── {feature}/      # Templates por feature
│   └── components/     # Componentes reutilizables
└── static/              # Frontend assets
    ├── js/             # Vanilla JavaScript (ES6 modules)
    │   ├── main.js
    │   ├── api.js
    │   └── {feature}.js
    ├── css/            # Estilos CSS
    └── images/         # Imágenes, iconos
```

**Diferencia con flask-rest:**
- **flask-rest:** API pura (JSON responses), sin frontend
- **flask-webapp:** Fullstack (HTML templates + JS), con frontend integrado

---

### 5. Generic Python (`generic-python.json`)

**Para:** Proyectos Python sin framework específico

**Características:**
- Minimalista (usa mayoría de defaults)
- Estructura simple de módulos Python
- pytest básico (sin plugins específicos)
- Best practices documentadas (SOLID, type hints, docstrings)
- Máxima flexibilidad

**Cuándo usar:**
- ✅ Librerías y paquetes Python
- ✅ Scripts y herramientas CLI
- ✅ Data science / ML projects
- ✅ **No sabes qué perfil usar** → Usa este

**Ejemplo de estructura generada:**
```
src/my_module/
├── my_module.py
└── __init__.py
```

---

## 🔧 Instalación

El instalador del framework copiará esta estructura en `.claude/skills/implement-us/` y fusionará el perfil seleccionado con el config base.

**Interactivo:**
```bash
python installer.py
# Selecciona perfil:
#   1) PyQt MVC
#   2) FastAPI REST
#   3) Flask REST
#   4) Flask Webapp
#   5) Generic Python
```

**No interactivo:**
```bash
python installer.py --profile pyqt-mvc --yes
python installer.py --profile fastapi-rest --yes
python installer.py --profile flask-rest --yes
python installer.py --profile flask-webapp --yes
python installer.py --profile generic-python --yes
```

---

## 📊 Comparación de Perfiles

| Característica | PyQt MVC | FastAPI REST | Flask REST | Flask Webapp | Generic Python |
|----------------|----------|--------------|------------|--------------|----------------|
| **Tamaño** | ~350 líneas | ~460 líneas | ~1000 líneas | ~1100 líneas | ~280 líneas |
| **Overrides** | 8 variables | 8 variables | 8 variables + async | 7 variables + async | 2 variables |
| **Arquitectura** | MVC | Layered (3) | Layered (3) | BFF + SSR | Flexible |
| **Frontend** | Qt UI | No | No | **Sí (Jinja2 + JS)** | No |
| **Files/Feature** | 3 (M+V+C) | 5 | 3-4 | **4-5 (route+template+css+js)** | 1-2 |
| **Test Framework** | pytest-qt | pytest + httpx | pytest + Flask | pytest + Flask + mock | pytest |
| **Fixtures** | qapp, qtbot | async_client, db | app, client | app, client | Ninguno |
| **Async** | No | Sí (async/await) | No (sync) | No (sync) | Opcional |
| **Coverage Min** | 90% | 95% | 95% | **90%** (solo backend) | 95% |
| **Pylint Min** | 8.0 | 8.5 | 8.0 | 8.0 | 8.0 |
| **OpenAPI** | - | Nativo | Flasgger | - | - |
| **Patterns** | 4 | 5 | 5 | 5 | 2 |
| **Complejidad** | Alta | Media | Media | Media-Alta | Baja |
| **Opinionado** | Alto | Medio | Medio | Medio-Alto | Bajo |
| **Proyecto Real** | simapp_termostato | - | app_termostato | webapp_termostato | - |

---

## 🎨 Variables Parametrizadas

Todas las variables configurables en los perfiles:

| Variable | PyQt MVC | FastAPI REST | Flask REST | Flask Webapp | Generic Python |
|----------|----------|--------------|------------|--------------|----------------|
| `{ARCHITECTURE_PATTERN}` | `mvc` | `layered` | `layered` | `bff` | `generic` |
| `{COMPONENT_TYPE}` | `Panel` | `Endpoint` | `Endpoint` | `Page` | `Module` |
| `{COMPONENT_PATH}` | `app/presentacion/paneles/{name}/` | `app/api/{name}/` | `app/{layer}/{name}/` | `webapp/templates/{name}/` | `src/{name}/` |
| `{TEST_FRAMEWORK}` | `pytest + pytest-qt` | `pytest + httpx` | `pytest + Flask client` | `pytest + Flask + mock` | `pytest` |
| `{BASE_CLASS}` | `ModeloBase`, `QWidget` | `BaseModel`, `BaseService` | `ABC` (repositories) | `Flask`, `FlaskForm` | `object` |
| `{DOMAIN_CONTEXT}` | `presentacion` | `api` | `servicios` | `webapp` | `core` |
| `{PROJECT_ROOT}` | `app/` | `app/` | `app/` | `webapp/` | `.` |
| `{PRODUCT}` | `main` | `main` | `main` | `main` | `main` |

---

## ✅ Validación del Sistema

**Todos los perfiles validados:**
```
✅ config.json válido
✅ pyqt-mvc.json válido
✅ fastapi-rest.json válido
✅ flask-rest.json válido
✅ flask-webapp.json válido
✅ generic-python.json válido
```

**Estructura verificada:**
- ✅ 1 config base (config.json)
- ✅ 5 perfiles (pyqt, fastapi, flask-rest, flask-webapp, generic)
- ✅ 10 phases (phase-0 a phase-9)
- ✅ 1 orquestador (skill.md)

---

## 📚 Referencias

- **Config Base:** `config.json`
- **Perfiles:** `customizations/*.json`
- **Fases:** `phases/phase-*.md`
- **Orquestador:** `skill.md`
- **Documentación:** Ver tickets TICKET-022 a TICKET-029

---

**Última Actualización:** 2026-02-17 - 5 perfiles completos, 10 fases implementadas, validados en Fase 7
