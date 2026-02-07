# Notas de Migración - Claude Dev Kit

**Fecha:** 2026-02-07
**Origen:** simapp_termostato/.claude/
**Destino:** claude-dev-kit/

---

## Archivos Copiados

### Skills (2 archivos)
- ✅ `skills/implement-us.md` - Definición completa del skill (707 líneas)
- ✅ `skills/implement-us-config.json` - Configuración base (106 líneas)

**Acción requerida:**
- [ ] Generalizar `implement-us.md`: remover referencias específicas a MVC/PyQt/Factory/Coordinator
- [ ] Crear perfiles de customización en `customizations/`:
  - [ ] `pyqt-mvc.json` (basado en config actual)
  - [ ] `fastapi-rest.json`
  - [ ] `django-mvt.json`
  - [ ] `generic-python.json`

---

### Templates (4 archivos)
- ✅ `templates/bdd-scenario.feature` - Template Gherkin (33 líneas)
- ✅ `templates/implementation-plan.md` - Template plan (152 líneas)
- ✅ `templates/implementation-report.md` - Template reporte (227 líneas)
- ✅ `templates/test-unit.py` - Template tests unitarios (180 líneas)

**Estado:**
- `bdd-scenario.feature`: ✅ Ya es genérico, solo necesita ajustes menores
- `implementation-plan.md`: ⚠️ Contiene referencias a MVC (líneas 27-40), generalizar
- `implementation-report.md`: ⚠️ Contiene referencias a paneles MVC, generalizar
- `test-unit.py`: ⚠️ Fixtures específicas de PyQt (líneas 10-30), generalizar

**Acción requerida:**
- [ ] Generalizar variables en templates:
  - `{ARCHITECTURE_PATTERN}` en lugar de "MVC"
  - `{COMPONENT_TYPE}` en lugar de "Panel"
  - `{TEST_FRAMEWORK}` en lugar de "pytest-qt"
- [ ] Crear templates adicionales:
  - [ ] `sprint-plan.md`
  - [ ] `architecture-decision.md` (ADR)
  - [ ] `test-integration.py`
  - [ ] `conftest.py`

---

### Tracking System (3 archivos)
- ✅ `tracking/time_tracker.py` - Core del tracking (521 líneas)
- ✅ `tracking/commands.py` - Comandos /track-* (444 líneas)
- ✅ `tracking/__init__.py` - Init del módulo

**Estado:**
- ✅ `time_tracker.py`: 100% genérico, no requiere cambios
- ✅ `commands.py`: 100% genérico, no requiere cambios
- ✅ `__init__.py`: Vacío, agregar exports

**Acción requerida:**
- [ ] Mejorar documentación en docstrings
- [ ] Agregar tests unitarios para tracking system
- [ ] Crear `models.py` separando dataclasses (Task, Phase, Pause)
- [ ] Crear `utils.py` con funciones de formateo

---

### Documentación (1 archivo)
- ✅ `docs/claude-readme-reference.md` - README original de .claude/ (342 líneas)

**Acción requerida:**
- [ ] Usar como referencia para crear `docs/getting-started.md`
- [ ] Extraer secciones reutilizables

---

## Plan de Trabajo

### Fase 1: Estructura Base (Sprint 1 - Día 1)
- [ ] Crear estructura de directorios completa según PROJECT_PLAN.md
- [ ] Copiar archivos del tracking system (ya genéricos)
- [ ] Crear README.md inicial
- [ ] Crear .gitignore
- [ ] Crear LICENSE (MIT)
- [ ] Primer commit

### Fase 2: Generalización de Skills (Sprint 2 - Días 2-3)
- [ ] Generalizar `implement-us.md`
- [ ] Crear `config.json` base (genérico)
- [ ] Crear perfiles de customización (4 perfiles)
- [ ] Dividir skill en fases (9 archivos .md en `phases/`)

### Fase 3: Generalización de Templates (Sprint 2 - Días 4-5)
- [ ] Generalizar templates existentes (4 archivos)
- [ ] Crear templates adicionales (4 nuevos)
- [ ] Organizar en subdirectorios (bdd/, planning/, testing/, reporting/)

### Fase 4: Sistema de Instalación (Sprint 1 - Días 6-7)
- [ ] Desarrollar `installer.py`
- [ ] Crear `config.yaml`
- [ ] Desarrollar `validate-setup.py`
- [ ] Scripts bash/powershell opcionales

### Fase 5: Documentación (Sprint 3)
- [ ] `docs/getting-started.md`
- [ ] `docs/installation.md`
- [ ] `docs/customization.md`
- [ ] `docs/configuration.md`
- [ ] `docs/skills/implement-us.md`
- [ ] `docs/tracking/tracking-guide.md`

### Fase 6: Ejemplos (Sprint 3)
- [ ] `examples/pyqt-mvc/` (basado en simapp_termostato)
- [ ] `examples/fastapi-rest/`
- [ ] `examples/generic-python/`

### Fase 7: Testing & Release (Sprint 4)
- [ ] Tests del instalador
- [ ] Tests del tracking system
- [ ] Validación multiplataforma
- [ ] Release v1.0.0

---

## Cambios Importantes al Generalizar

### implement-us.md

**Remover:**
- Referencias a "MVC", "Factory", "Coordinator"
- Referencias a "Panel", "Display", "Climatizador"
- Referencias a PyQt6 específicas
- Paths específicos de simapp_termostato

**Reemplazar con:**
- Variables: `{ARCHITECTURE_PATTERN}`, `{COMPONENT_TYPE}`
- Instrucciones que lean la configuración del perfil
- Ejemplos genéricos (o múltiples ejemplos por stack)

**Ejemplo de cambio:**

**Antes (línea 130):**
```markdown
### 1. Panel Display (MVC)
- [ ] app/presentacion/paneles/display/modelo.py (10 min)
- [ ] app/presentacion/paneles/display/vista.py (20 min)
- [ ] app/presentacion/paneles/display/controlador.py (15 min)
```

**Después:**
```markdown
### 1. {COMPONENT_NAME} ({ARCHITECTURE_PATTERN})
- [ ] {COMPONENT_PATH}/modelo.py (10 min)
- [ ] {COMPONENT_PATH}/vista.py (20 min)
- [ ] {COMPONENT_PATH}/controlador.py (15 min)

> Nota: La estructura de componentes se define en el perfil seleccionado.
> Ver `.claude/skills/implement-us/config.json` para personalizar.
```

---

### implement-us-config.json

**Convertir en base genérica:**

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
    "mvc": ["modelo", "vista", "controlador"],
    "mvt": ["model", "view", "template"],
    "clean-architecture": ["entity", "use-case", "interface", "infrastructure"]
  },

  "quality_gates": {
    "pylint_min": 8.0,
    "cc_max": 10,
    "mi_min": 20,
    "coverage_min": 95.0
  },

  ...
}
```

**Los perfiles sobrescriben con valores específicos.**

---

## Perfiles de Customización

### pyqt-mvc.json (Ejemplo)

```json
{
  "profile_name": "pyqt-mvc",
  "description": "Proyectos PyQt6 con arquitectura MVC + Factory/Coordinator",
  "based_on": "implement-us-config.json",

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

  "templates": {
    "test_unit": "templates/testing/test-unit-pyqt.py"
  }
}
```

---

## Recursos Adicionales Necesarios

### Desde CLAUDE.md de simapp_termostato

- Sección "Key Design Patterns" → Documentar en `docs/architecture-patterns.md`
- Sección "Testing Patterns" → Usar en templates de tests
- Comandos de quality gates → Documentar en `docs/quality-gates.md`

### Nuevos Archivos a Crear

- `.gitignore` para claude-dev-kit
- `LICENSE` (MIT)
- `CHANGELOG.md`
- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md` (opcional)

---

## Siguiente Acción Inmediata

1. Revisar estos archivos migrados
2. Crear estructura de directorios base según PROJECT_PLAN.md
3. Empezar por el tracking system (ya está genérico, mover directamente)
4. Luego generalizar skills y templates

---

**Última actualización:** 2026-02-07
