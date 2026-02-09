# TICKET-026: Crear perfil generic-python.json

**Fase:** 3 - Generalización de Skills
**Sprint:** 2
**Estado:** TODO
**Prioridad:** Media
**Estimación:** 1 hora
**Asignado a:** Claude Code

## Descripción

Crear el perfil de customización `generic-python.json` que adapta el skill `implement-us` para proyectos Python genéricos sin framework específico.

Este perfil actúa como fallback cuando ningún otro perfil es apropiado y proporciona configuración minimalista pero funcional.

## Criterios de Aceptación

- [ ] Archivo `skills/implement-us/customizations/generic-python.json` creado
- [ ] Schema JSON válido
- [ ] Configuración minimalista pero completa
- [ ] Test framework configurado (pytest básico)
- [ ] Sin dependencies específicas de framework
- [ ] Estructura simple de archivos
- [ ] Compatible con fusión sobre config.json base

## Dependencias

- **Depende de:** TICKET-022 (config.json base creado)
- **Bloquea a:** TICKET-027 (testing)

## Notas Técnicas

### Estructura del Perfil

```json
{
  "profile_name": "generic-python",
  "profile_version": "1.0",
  "description": "Proyectos Python genéricos sin framework específico",
  "extends": "config.json",

  "architecture_patterns": {
    "default": "generic",
    "available": [
      "generic",
      "layered",
      "clean-architecture"
    ]
  },

  "component_structure": {
    "generic": {
      "files": [
        "__init__.py",
        "implementation.py",
        "tests.py"
      ],
      "base_path": "src/{component_name}/",
      "description": "Estructura simple para componentes genéricos"
    },
    "layered": {
      "files": [
        "__init__.py",
        "core.py",
        "utils.py",
        "tests.py"
      ],
      "base_path": "src/{component_name}/",
      "description": "Estructura en capas básica"
    }
  },

  "test_framework": {
    "runner": "pytest",
    "plugins": [
      "pytest-cov",
      "pytest-mock"
    ],
    "fixtures_required": [],
    "coverage_tool": "pytest-cov",
    "config_file": "pytest.ini"
  },

  "base_classes": {
    "default": "object",
    "description": "Sin clases base específicas"
  },

  "dependencies": {
    "required": [
      "pytest>=7.0.0",
      "pytest-cov>=4.0.0"
    ],
    "optional": [
      "pytest-mock>=3.10.0",
      "black>=23.0.0",
      "isort>=5.12.0",
      "mypy>=1.0.0"
    ],
    "description": "Dependencias mínimas para testing y calidad"
  },

  "patterns": {
    "modules": {
      "enabled": true,
      "description": "Organización en módulos Python estándar"
    },
    "functional": {
      "enabled": true,
      "description": "Soporte para programación funcional"
    },
    "oop": {
      "enabled": true,
      "description": "Soporte para programación orientada a objetos"
    }
  },

  "quality_gates": {
    "pylint_min": 8.0,
    "cc_max": 10,
    "mi_min": 20,
    "coverage_min": 85.0,
    "specific_rules": [
      "All public functions must have docstrings",
      "Type hints recommended but not required"
    ]
  },

  "templates": {
    "bdd": ".claude/templates/bdd/scenario.feature",
    "planning": ".claude/templates/planning/implementation-plan.md",
    "testing_unit": ".claude/templates/testing/test-unit.py",
    "testing_integration": ".claude/templates/testing/test-integration.py",
    "reporting": ".claude/templates/reporting/implementation-report.md"
  },

  "variables": {
    "architecture_pattern": "generic",
    "component_type": "Module",
    "component_path": "src/{component_name}/",
    "test_framework": "pytest",
    "base_class": "object"
  },

  "code_style": {
    "formatter": "black",
    "line_length": 88,
    "import_sorter": "isort",
    "type_checker": "mypy",
    "description": "Herramientas de estilo de código recomendadas"
  },

  "project_structure": {
    "recommended": [
      "src/",
      "tests/",
      "docs/",
      "README.md",
      "requirements.txt",
      "setup.py",
      "pytest.ini",
      ".gitignore"
    ],
    "description": "Estructura de proyecto recomendada"
  },

  "example_component": {
    "name": "calculator",
    "files": [
      "src/calculator/__init__.py",
      "src/calculator/implementation.py",
      "tests/test_calculator.py"
    ],
    "functions": [
      "add(a, b)",
      "subtract(a, b)",
      "multiply(a, b)",
      "divide(a, b)"
    ],
    "description": "Ejemplo de módulo Python simple"
  }
}
```

### Características del Perfil Generic

- **Minimalista:** Solo lo esencial
- **Flexible:** Soporta múltiples paradigmas (OOP, funcional)
- **Sin Opiniones:** No impone frameworks o patrones específicos
- **Estándar:** Sigue convenciones PEP 8
- **Testing:** pytest básico sin plugins específicos de framework

### Casos de Uso

- Scripts Python
- Librerías/paquetes
- CLI tools
- Data processing scripts
- Cualquier proyecto Python que no encaje en otros perfiles

## Checklist de Implementación

- [ ] Crear estructura JSON del perfil
- [ ] Definir architecture_patterns (generic, layered, clean-architecture)
- [ ] Definir component_structure simple
- [ ] Definir test_framework con pytest básico
- [ ] Definir base_classes (object)
- [ ] Definir dependencies mínimas
- [ ] Definir patterns genéricos (modules, functional, oop)
- [ ] Definir quality_gates con umbrales razonables
- [ ] Definir templates genéricas
- [ ] Definir variables con valores genéricos
- [ ] Definir code_style recomendado
- [ ] Definir project_structure recomendada
- [ ] Agregar example_component simple
- [ ] Validar sintaxis JSON
- [ ] Verificar fusión con config.json base
- [ ] Guardar como `skills/implement-us/customizations/generic-python.json`

## Resultado

**Fecha de Completado:** _Pendiente_

### Archivo Generado

- Ubicación: `skills/implement-us/customizations/generic-python.json`
- Tamaño: _X_ líneas
- Validación JSON: ✅ / ❌

### Commit

_Pendiente_

**Estado:** 📋 Pendiente
