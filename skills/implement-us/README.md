# Skill: implement-us

Sistema de implementación asistida de Historias de Usuario framework-agnostic.

---

## 📋 Descripción

El skill `implement-us` guía paso a paso la implementación de una Historia de Usuario en proyectos Python, adaptándose automáticamente al stack tecnológico mediante perfiles de configuración.

**Características:**
- ✅ Framework-agnostic (PyQt, FastAPI, Python genérico)
- ✅ 9 fases de implementación (desde validación hasta reporte final)
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

### 3. Generic Python (`generic-python.json`)

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
# Selecciona perfil: 1) PyQt MVC  2) FastAPI REST  3) Generic Python
```

**No interactivo:**
```bash
python installer.py --profile pyqt-mvc --yes
python installer.py --profile fastapi-rest --yes
python installer.py --profile generic-python --yes
```

---

## 📊 Comparación de Perfiles

| Característica | PyQt MVC | FastAPI REST | Generic Python |
|----------------|----------|--------------|----------------|
| **Tamaño** | ~350 líneas | ~460 líneas | ~280 líneas |
| **Overrides** | 8 variables | 8 variables | 2 variables |
| **Arquitectura** | MVC | Layered (3 capas) | Flexible |
| **Files/Feature** | 3 (M+V+C) | 5 (router+service+repo+schemas+models) | 1-2 |
| **Test Framework** | pytest-qt | pytest + httpx | pytest |
| **Fixtures** | qapp, qtbot | client, async_client, db | Ninguno |
| **Async** | No | Sí (async/await) | Opcional |
| **Coverage Min** | 90% | 95% | 95% |
| **Pylint Min** | 8.0 | 8.5 | 8.0 |
| **Complejidad** | Alta | Media | Baja |
| **Opinionado** | Alto | Medio | Bajo |

---

## 🎨 Variables Parametrizadas

Todas las variables configurables en los perfiles:

| Variable | PyQt MVC | FastAPI REST | Generic Python |
|----------|----------|--------------|----------------|
| `{ARCHITECTURE_PATTERN}` | `mvc` | `layered` | `generic` |
| `{COMPONENT_TYPE}` | `Panel` | `Endpoint` | `Module` |
| `{COMPONENT_PATH}` | `app/presentacion/paneles/{name}/` | `app/api/{name}/` | `src/{name}/` |
| `{TEST_FRAMEWORK}` | `pytest + pytest-qt` | `pytest + httpx` | `pytest` |
| `{BASE_CLASS}` | `ModeloBase`, `QWidget` | `BaseModel`, `BaseService` | `object` |
| `{DOMAIN_CONTEXT}` | `presentacion` | `api` | `core` |
| `{PROJECT_ROOT}` | `app/` | `app/` | `.` |
| `{PRODUCT}` | `main` | `main` | `main` |

---

## ✅ Validación del Sistema

**Todos los perfiles validados:**
```
✅ config.json válido
✅ pyqt-mvc.json válido
✅ fastapi-rest.json válido
✅ generic-python.json válido
```

**Estructura verificada:**
- ✅ 1 config base (config.json)
- ✅ 3 perfiles (pyqt, fastapi, generic)
- ✅ 10 phases (phase-0 a phase-9)
- ✅ 1 orquestador (skill.md)

---

## 📚 Referencias

- **Config Base:** `config.json`
- **Perfiles:** `customizations/*.json`
- **Fases:** `phases/phase-*.md`
- **Orquestador:** `skill.md`
- **Documentación:** Ver tickets TICKET-022 a TICKET-026

---

**Última Actualización:** 2026-02-13 - Sprint 2 completado
