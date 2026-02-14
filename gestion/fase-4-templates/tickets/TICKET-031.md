# TICKET-031: Crear Estructura de Directorios templates/

**Fase:** 4 - Generalización de Templates
**Sprint:** 2
**Estado:** TODO
**Prioridad:** Alta
**Estimación:** 0.5 horas
**Asignado a:** Claude Code

---

## Descripción

Crear la estructura de directorios `templates/` en el directorio raíz del proyecto siguiendo la organización por categorías (bdd, planning, testing, reporting) con subdirectorios de ejemplos por perfil.

Esta estructura será la base para todos los templates generalizados y servirá como referencia para los usuarios del framework.

---

## Criterios de Aceptación

- [ ] Estructura de directorios creada según especificación
- [ ] README.md en `templates/` con documentación completa
- [ ] Subdirectorios `examples/` creados en cada categoría
- [ ] Archivos `.gitkeep` en directorios vacíos (si aplica)
- [ ] Estructura validada y lista para recibir templates

---

## Dependencias

**Depende de:**
- ✅ TICKET-030: Análisis completado

**Bloquea a:**
- TICKET-032: Generalizar bdd-scenario.feature
- TICKET-033: Generalizar implementation-plan.md
- TICKET-034: Generalizar implementation-report.md
- TICKET-035: Generalizar test-unit.py

---

## Estructura a Crear

```
templates/
├── README.md                    # Documentación principal
├── bdd/
│   ├── scenario.feature        # (creado en TICKET-032)
│   └── examples/
│       ├── .gitkeep           # Placeholder hasta TICKET-036
│       ├── pyqt-mvc.feature   # (creado en TICKET-036)
│       ├── fastapi-rest.feature
│       ├── flask-rest.feature
│       ├── flask-webapp.feature
│       └── generic-python.feature
├── planning/
│   ├── implementation-plan.md  # (creado en TICKET-033)
│   └── examples/
│       ├── .gitkeep
│       ├── pyqt-mvc.md
│       ├── fastapi-rest.md
│       ├── flask-rest.md
│       ├── flask-webapp.md
│       └── generic-python.md
├── testing/
│   ├── test-unit.py           # (creado en TICKET-035)
│   ├── test-integration.py    # (BONUS - opcional)
│   └── examples/
│       ├── .gitkeep
│       ├── pyqt-mvc.py
│       ├── fastapi-rest.py
│       ├── flask-rest.py
│       ├── flask-webapp.py
│       └── generic-python.py
└── reporting/
    ├── implementation-report.md # (creado en TICKET-034)
    └── examples/
        ├── .gitkeep
        ├── pyqt-mvc.md
        ├── fastapi-rest.md
        ├── flask-rest.md
        ├── flask-webapp.md
        └── generic-python.md
```

---

## Contenido del README.md

El README debe incluir:

### 1. Introducción
- Propósito del directorio templates
- Cómo se usan en el skill /implement-us

### 2. Categorías de Templates

#### BDD Templates
- `bdd/scenario.feature` - Descripción y variables

#### Planning Templates
- `planning/implementation-plan.md` - Descripción y variables

#### Testing Templates
- `testing/test-unit.py` - Descripción y variables
- `testing/test-integration.py` - (opcional)

#### Reporting Templates
- `reporting/implementation-report.md` - Descripción y variables

### 3. Sistema de Variables

Tabla completa de variables disponibles:

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `{US_ID}` | ID de historia | US-001 |
| `{US_TITLE}` | Título | Implementar panel display |
| `{ARCHITECTURE_PATTERN}` | Patrón arquitectónico | mvc, layered |
| ... | ... | ... |

### 4. Uso de Templates

Cómo el skill /implement-us genera archivos desde templates:
1. Lee template correspondiente
2. Carga variables del perfil activo
3. Reemplaza placeholders `{VARIABLE}`
4. Genera archivo final

### 5. Ejemplos por Perfil

Link a ejemplos en subdirectorios `examples/`

### 6. Personalización

Cómo crear templates custom o modificar existentes

---

## Checklist de Implementación

- [ ] Crear estructura de directorios con `mkdir -p`
- [ ] Crear archivos `.gitkeep` en directorios vacíos
- [ ] Escribir README.md completo
- [ ] Validar estructura con `tree templates/`
- [ ] Documentar en session-current.md

---

## Comandos

```bash
# Crear estructura
mkdir -p templates/{bdd,planning,testing,reporting}/examples

# Crear .gitkeep
touch templates/*/examples/.gitkeep

# Validar
tree templates/
```

---

## Resultado

_A completar al finalizar el ticket._

**Archivos creados:**
- `templates/README.md`
- Estructura de 4 categorías + subdirectorios
