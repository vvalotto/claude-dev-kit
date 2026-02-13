# Sprint 2 - Fase 3: Generalización de Skills

**Fecha Inicio:** 2026-02-09
**Fecha Fin Estimada:** 2026-02-11
**Sprint:** 2 (Semana 2)
**Estado:** 🔄 En Progreso

---

## Objetivos de la Fase

Generalizar el skill `implement-us` desde su implementación específica de PyQt/MVC a un framework agnóstico que soporte múltiples stacks tecnológicos mediante un sistema de perfiles de configuración.

---

## Tareas (Tickets)

### Completados ✅

- [x] **TICKET-019**: Análisis del skill implement-us actual y planificación de generalización ✅
- [x] **TICKET-020**: Crear estructura de directorios `skills/implement-us/` ✅
- [x] **TICKET-021**: Generalizar `implement-us.md` (remover referencias MVC/PyQt) ✅
- [x] **TICKET-022**: Crear `config.json` base genérico ✅

### En Progreso 🔄

Ninguno actualmente.

- [x] **TICKET-023**: Crear perfil `pyqt-mvc.json` ✅

### Pendientes 📋
- [ ] **TICKET-024**: Crear perfil `fastapi-rest.json`
- [ ] **TICKET-025**: Crear perfil `django-mvt.json`
- [ ] **TICKET-026**: Crear perfil `generic-python.json`
- [ ] **TICKET-027**: Testing de perfiles y validación del skill generalizado

---

## Métricas

- **Total de Tickets:** 9
- **Completados:** 5 (56%)
- **En Progreso:** 0 (0%)
- **Pendientes:** 4 (44%)
- **Bloqueados:** 0

**Estimación Total:** 14 horas
**Tiempo Consumido:** ~7.1 horas
**Tiempo Restante:** ~6.9 horas

**Progreso:** ████████████░░░░ 56%

---

## Dependencias

**Depende de:**
- ✅ Fase 1: Setup Inicial (completada)
- ✅ Fase 2: Sistema de Instalación (completada)

**Bloquea a:**
- Fase 4: Templates (requiere variables definidas en los perfiles)
- Fase 6: Documentación (requiere skill finalizado)
- Fase 7: Ejemplos (requiere perfiles funcionando)

---

## Criterios de Aceptación de la Fase

- [ ] Estructura `skills/implement-us/` creada con subdirectorios `phases/` y `customizations/`
- [ ] `skill.md` generalizado sin referencias específicas a PyQt/MVC/Factory/Coordinator
- [ ] Variables `{ARCHITECTURE_PATTERN}`, `{COMPONENT_TYPE}`, `{COMPONENT_PATH}` implementadas
- [ ] `config.json` base creado con valores genéricos por defecto
- [ ] 4 perfiles de customización creados y funcionales:
  - [ ] `pyqt-mvc.json` (basado en implementación original)
  - [ ] `fastapi-rest.json` (para APIs REST)
  - [ ] `django-mvt.json` (para aplicaciones Django)
  - [ ] `generic-python.json` (para proyectos Python genéricos)
- [ ] Sistema de fusión config base + perfil funcionando correctamente
- [ ] Testing manual con al menos 2 perfiles diferentes
- [ ] Documentación de las variables disponibles y cómo personalizarlas

---

## Notas Técnicas

### Variables a Implementar

Las siguientes variables deben reemplazar referencias hardcodeadas:

| Variable | Reemplaza | Ejemplo Valor |
|----------|-----------|---------------|
| `{ARCHITECTURE_PATTERN}` | "MVC" | mvc, mvt, clean-architecture, layered |
| `{COMPONENT_TYPE}` | "Panel", "Display" | View, Service, Controller, Component |
| `{COMPONENT_PATH}` | `app/presentacion/paneles/` | Ruta base de componentes |
| `{TEST_FRAMEWORK}` | "pytest-qt" | pytest, unittest, pytest-bdd |
| `{BASE_CLASS}` | "ModeloBase" | Clase base de modelos |
| `{COMPONENT_NAME}` | Nombre del componente | login, dashboard, user_profile |

### Estructura de config.json Base

```json
{
  "version": "1.0",
  "skill_name": "implement-us",
  "description": "Implementador asistido de Historias de Usuario",

  "architecture_patterns": {
    "default": "generic",
    "available": ["mvc", "mvt", "clean-architecture", "layered", "generic"]
  },

  "component_structure": {
    "default": ["implementation", "tests"],
    "paths": {
      "default": "src/{component_name}/"
    }
  },

  "test_framework": {
    "runner": "pytest",
    "plugins": [],
    "fixtures_required": []
  },

  "quality_gates": {
    "pylint_min": 8.0,
    "cc_max": 10,
    "mi_min": 20,
    "coverage_min": 95.0
  },

  "phases": {
    "0": "Validación de Contexto",
    "1": "Generación de Escenarios BDD",
    "2": "Generación de Plan de Implementación",
    "3": "Implementación",
    "4": "Tests Unitarios",
    "5": "Tests de Integración",
    "6": "Validación BDD",
    "7": "Quality Gates",
    "8": "Documentación",
    "9": "Reporte Final"
  }
}
```

### Ejemplo de Perfil (pyqt-mvc.json)

```json
{
  "profile_name": "pyqt-mvc",
  "description": "Proyectos PyQt6 con arquitectura MVC + Factory/Coordinator",
  "extends": "config.json",

  "architecture_patterns": {
    "default": "mvc",
    "available": ["mvc"]
  },

  "component_structure": {
    "mvc": {
      "files": ["modelo.py", "vista.py", "controlador.py"],
      "base_path": "app/presentacion/paneles/{component_name}/"
    }
  },

  "test_framework": {
    "runner": "pytest",
    "plugins": ["pytest-qt", "pytest-cov", "pytest-bdd"],
    "fixtures_required": ["qapp", "qtbot"]
  },

  "base_classes": {
    "model": "ModeloBase",
    "view": "QWidget",
    "controller": "object"
  }
}
```

---

## Riesgos Identificados

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Generalización pierde funcionalidad específica | Media | Alto | Mantener perfiles específicos muy detallados |
| Variables demasiado complejas de usar | Media | Medio | Documentar claramente con ejemplos |
| Perfiles incompatibles entre sí | Baja | Medio | Validación de esquema JSON |
| Referencias hardcodeadas olvidadas | Media | Medio | Búsqueda exhaustiva con grep de términos clave |

---

## Checklist Pre-Commit

Antes de hacer commit de esta fase:
- [ ] Skill generalizado sin referencias específicas (grep verificado)
- [ ] Todos los perfiles creados y validados
- [ ] config.json base con schema válido
- [ ] Testing manual con al menos 2 perfiles
- [ ] Variables documentadas en comentarios del skill
- [ ] Fusión config base + perfil testeada
- [ ] Actualizar CHANGELOG.md
- [ ] Actualizar session-current.md

---

## Retrospectiva (Al finalizar)

### ¿Qué salió bien?

_A completar al finalizar la fase._

### ¿Qué se puede mejorar?

_A completar al finalizar la fase._

### Lecciones Aprendidas

_A completar al finalizar la fase._

---

## Siguiente Fase

**Fase 4: Generalización de Templates** - Ver `gestion/fase-4-templates/sprint-2.md`

---

**Última Actualización:** 2026-02-13 (TICKET-023 completado - perfil pyqt-mvc.json creado)
