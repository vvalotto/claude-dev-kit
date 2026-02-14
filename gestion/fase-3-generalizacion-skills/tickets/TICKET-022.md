# TICKET-022: Crear config.json base genérico

**Fase:** 3 - Generalización de Skills
**Sprint:** 2
**Estado:** TODO
**Prioridad:** Alta
**Estimación:** 1.5 horas
**Asignado a:** Claude Code

## Descripción

Crear el archivo `config.json` base genérico que define la configuración por defecto del skill `implement-us` sin referencias a ningún stack tecnológico específico.

Este archivo será la base que se fusiona con los perfiles específicos durante la instalación.

## Criterios de Aceptación

- [ ] Archivo `skills/implement-us/config.json` creado
- [ ] Schema JSON válido (validado con linter)
- [ ] Todas las secciones necesarias incluidas
- [ ] Valores por defecto genéricos (no específicos de ningún stack)
- [ ] Comentarios inline documentando cada sección
- [ ] Compatible con los 4 perfiles planificados
- [ ] Documentación de estructura en README.md actualizada

## Dependencias

- **Depende de:** TICKET-020 (estructura directorios), TICKET-019 (análisis)
- **Bloquea a:** TICKET-023, TICKET-024, TICKET-025, TICKET-026 (perfiles)

## Notas Técnicas

### Estructura del config.json

```json
{
  "version": "1.0",
  "skill_name": "implement-us",
  "description": "Implementador asistido de Historias de Usuario",

  "architecture_patterns": {
    "default": "generic",
    "available": [
      "mvc",
      "mvt",
      "clean-architecture",
      "layered",
      "generic"
    ],
    "description": "Patrón arquitectónico del proyecto"
  },

  "component_structure": {
    "default": {
      "files": ["implementation.py", "tests.py"],
      "base_path": "src/{component_name}/"
    },
    "description": "Estructura de archivos por componente"
  },

  "test_framework": {
    "runner": "pytest",
    "plugins": [],
    "fixtures_required": [],
    "coverage_tool": "pytest-cov",
    "description": "Framework y configuración de testing"
  },

  "quality_gates": {
    "pylint_min": 8.0,
    "cc_max": 10,
    "mi_min": 20,
    "coverage_min": 95.0,
    "description": "Umbrales de calidad de código"
  },

  "phases": {
    "0": {
      "name": "Validación de Contexto",
      "description": "Validar que existe documentación y contexto necesario"
    },
    "1": {
      "name": "Generación de Escenarios BDD",
      "description": "Generar escenarios Gherkin desde historia de usuario"
    },
    "2": {
      "name": "Generación de Plan de Implementación",
      "description": "Crear plan detallado de implementación"
    },
    "3": {
      "name": "Implementación",
      "description": "Implementar código según el plan"
    },
    "4": {
      "name": "Tests Unitarios",
      "description": "Crear tests unitarios para componentes"
    },
    "5": {
      "name": "Tests de Integración",
      "description": "Crear tests de integración del flujo completo"
    },
    "6": {
      "name": "Validación BDD",
      "description": "Validar con escenarios BDD generados en Fase 1"
    },
    "7": {
      "name": "Quality Gates",
      "description": "Verificar umbrales de calidad (pylint, coverage, etc.)"
    },
    "8": {
      "name": "Documentación",
      "description": "Generar documentación de la implementación"
    },
    "9": {
      "name": "Reporte Final",
      "description": "Generar reporte completo de implementación"
    }
  },

  "templates": {
    "bdd": ".claude/templates/bdd/scenario.feature",
    "planning": ".claude/templates/planning/implementation-plan.md",
    "testing_unit": ".claude/templates/testing/test-unit.py",
    "testing_integration": ".claude/templates/testing/test-integration.py",
    "reporting": ".claude/templates/reporting/implementation-report.md",
    "description": "Rutas a templates usados por el skill"
  },

  "tracking": {
    "enabled": true,
    "auto_start": true,
    "auto_pause_on_checkpoint": false,
    "description": "Configuración de tracking de tiempo"
  },

  "checkpoints": {
    "after_bdd": true,
    "after_planning": true,
    "after_implementation": false,
    "after_tests": true,
    "before_quality_gates": true,
    "description": "Puntos de aprobación manual del usuario"
  },

  "variables": {
    "architecture_pattern": "{architecture_patterns.default}",
    "component_type": "Component",
    "component_path": "{component_structure.default.base_path}",
    "test_framework": "{test_framework.runner}",
    "base_class": "object",
    "description": "Variables disponibles para el skill"
  }
}
```

### Validación del JSON

```bash
# Validar sintaxis JSON
python -m json.tool skills/implement-us/config.json

# O con jq si está disponible
jq . skills/implement-us/config.json
```

### Referencia

Basarse en `_work/from-simapp/skills/implement-us-config.json` pero generalizando todos los valores específicos.

## Checklist de Implementación

- [ ] Leer `_work/from-simapp/skills/implement-us-config.json` como referencia
- [ ] Crear estructura base del JSON
- [ ] Definir sección `architecture_patterns` con valores genéricos
- [ ] Definir sección `component_structure` genérica
- [ ] Definir sección `test_framework` genérica
- [ ] Definir sección `quality_gates` con umbrales estándar
- [ ] Definir sección `phases` (9 fases)
- [ ] Definir sección `templates` con rutas default
- [ ] Definir sección `tracking` con configuración default
- [ ] Definir sección `checkpoints` con valores default
- [ ] Definir sección `variables` mapeando a valores default
- [ ] Validar sintaxis JSON
- [ ] Agregar comentarios descriptivos (JSON no soporta, documentar en README)
- [ ] Guardar como `skills/implement-us/config.json`
- [ ] Actualizar README.md con estructura del config

## Resultado

**Fecha de Completado:** _Pendiente_

### Archivo Generado

- Ubicación: `skills/implement-us/config.json`
- Tamaño: _X_ líneas
- Validación JSON: ✅ / ❌

### Commit

_Pendiente_

**Estado:** 📋 Pendiente
