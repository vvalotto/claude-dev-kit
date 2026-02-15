# Referencia de Configuración

**Última Actualización:** 2026-02-15
**Audiencia:** Usuario Avanzado / Desarrollador
**Nivel:** Avanzado

---

## Introducción

Referencia completa de todas las opciones de configuración disponibles en Claude Dev Kit.

**Archivos de configuración:**
- `.claude/config.json` - Configuración principal
- `.claude/skills/implement-us/config.json` - Config del skill
- Perfiles en `.claude/skills/implement-us/customizations/`

---

## Estructura de .claude/config.json

```json
{
  "version": "1.0.0",
  "project": {
    "name": "mi-proyecto",
    "type": "python",
    "root": "/Users/usuario/proyecto"
  },
  "profile": "generic-python",
  "tracking": {
    "enabled": true,
    "data_dir": ".claude/tracking"
  },
  "skills": {
    "implement-us": {
      "enabled": true,
      "config_path": ".claude/skills/implement-us/config.json"
    }
  }
}
```

---

## Opciones del Skill implement-us

### Archivo: .claude/skills/implement-us/config.json

```json
{
  "profile": "generic-python",
  "architecture_pattern": "layered",
  "test_framework": "pytest",

  "phases": {
    "enable_bdd": true,
    "enable_planning": true,
    "enable_implementation": true,
    "enable_unit_tests": true,
    "enable_integration_tests": true,
    "enable_bdd_validation": true,
    "enable_quality_gates": true,
    "enable_documentation": true,
    "enable_reporting": true
  },

  "quality_gates": {
    "pylint_threshold": 8.0,
    "coverage_threshold": 90,
    "max_complexity": 10,
    "min_maintainability": 20
  },

  "tracking": {
    "auto_start": true,
    "track_pauses": true,
    "save_interval": 60
  },

  "paths": {
    "source": "src/",
    "tests": "tests/",
    "docs": "docs/",
    "features": "tests/features/"
  }
}
```

---

## Referencia de Opciones

### profile

**Tipo:** String
**Default:** "generic-python"
**Valores:** pyqt-mvc, fastapi-rest, flask-rest, flask-webapp, generic-python

```json
"profile": "fastapi-rest"
```

---

### architecture_pattern

**Tipo:** String
**Default:** "layered"
**Valores:** mvc, mvt, layered, hexagonal, clean

```json
"architecture_pattern": "mvc"
```

---

### test_framework

**Tipo:** String
**Default:** "pytest"
**Valores:** pytest, pytest-qt, pytest-asyncio, pytest-flask, pytest-django, unittest

```json
"test_framework": "pytest-asyncio"
```

---

### phases.enable_bdd

**Tipo:** Boolean
**Default:** true
**Descripción:** Habilita generación de escenarios BDD (Gherkin)

```json
"phases": {
  "enable_bdd": false  // Deshabilitar BDD
}
```

---

### phases.enable_integration_tests

**Tipo:** Boolean
**Default:** true
**Descripción:** Habilita generación de tests de integración

```json
"phases": {
  "enable_integration_tests": true
}
```

---

### phases.enable_quality_gates

**Tipo:** Boolean
**Default:** true
**Descripción:** Habilita validación de calidad (Pylint, coverage, etc.)

```json
"phases": {
  "enable_quality_gates": true
}
```

---

### quality_gates.pylint_threshold

**Tipo:** Float
**Default:** 8.0
**Rango:** 0.0 - 10.0
**Descripción:** Puntaje mínimo de Pylint requerido

```json
"quality_gates": {
  "pylint_threshold": 9.0  // Más estricto
}
```

---

### quality_gates.coverage_threshold

**Tipo:** Integer
**Default:** 90
**Rango:** 0 - 100
**Descripción:** Porcentaje mínimo de cobertura de código

```json
"quality_gates": {
  "coverage_threshold": 95  // 95% mínimo
}
```

---

### quality_gates.max_complexity

**Tipo:** Integer
**Default:** 10
**Descripción:** Complejidad ciclomática máxima por función

```json
"quality_gates": {
  "max_complexity": 8  // Máximo 8
}
```

---

### quality_gates.min_maintainability

**Tipo:** Integer
**Default:** 20
**Descripción:** Índice de mantenibilidad mínimo

```json
"quality_gates": {
  "min_maintainability": 25
}
```

---

### tracking.auto_start

**Tipo:** Boolean
**Default:** true
**Descripción:** Inicia tracking automáticamente al comenzar fase

```json
"tracking": {
  "auto_start": true
}
```

---

### tracking.track_pauses

**Tipo:** Boolean
**Default:** true
**Descripción:** Registra pausas manuales con razón

```json
"tracking": {
  "track_pauses": true
}
```

---

### paths.source

**Tipo:** String
**Default:** "src/"
**Descripción:** Directorio de código fuente

```json
"paths": {
  "source": "app/"  // Usar app/ en lugar de src/
}
```

---

### paths.tests

**Tipo:** String
**Default:** "tests/"
**Descripción:** Directorio de tests

```json
"paths": {
  "tests": "test/"
}
```

---

## Perfiles Completos

### PyQt-MVC

```json
{
  "profile": "pyqt-mvc",
  "architecture_pattern": "mvc",
  "test_framework": "pytest-qt",
  "component_types": ["Model", "View", "Controller", "Coordinator"],
  "quality_gates": {
    "pylint_threshold": 8.5,
    "coverage_threshold": 95
  }
}
```

### FastAPI-REST

```json
{
  "profile": "fastapi-rest",
  "architecture_pattern": "layered",
  "test_framework": "pytest-asyncio",
  "component_types": ["Router", "Service", "Repository"],
  "quality_gates": {
    "pylint_threshold": 9.0,
    "coverage_threshold": 95
  }
}
```

---

## Variables de Entorno

```bash
# Deshabilitar tracking temporalmente
export CLAUDE_DEVKIT_TRACKING=false

# Nivel de logging
export CLAUDE_DEVKIT_LOG_LEVEL=DEBUG

# Path custom de config
export CLAUDE_DEVKIT_CONFIG=/custom/path/config.json
```

---

## Ejemplos de Configuración

### Proyecto Pequeño

```json
{
  "quality_gates": {
    "pylint_threshold": 7.5,
    "coverage_threshold": 85
  },
  "phases": {
    "enable_integration_tests": false
  }
}
```

### Proyecto Enterprise

```json
{
  "quality_gates": {
    "pylint_threshold": 9.5,
    "coverage_threshold": 98,
    "max_complexity": 6
  },
  "phases": {
    "enable_bdd": true,
    "enable_integration_tests": true,
    "enable_quality_gates": true
  }
}
```

---

## Recursos Adicionales

- [Personalización](./customization.md) - Crear perfiles custom
- [Tracking](./tracking/user-guide.md) - Sistema de tracking
- [Templates](./templates/template-system.md) - Sistema de templates

---

**Anterior:** [Personalización](./customization.md)
**Siguiente:** [Skill implement-us](./skills/implement-us.md)
**Índice:** [Volver al índice](./index.md)
