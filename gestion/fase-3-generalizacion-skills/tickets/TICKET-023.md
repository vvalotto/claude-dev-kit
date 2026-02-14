# TICKET-023: Crear perfil pyqt-mvc.json

**Fase:** 3 - Generalización de Skills
**Sprint:** 2
**Estado:** TODO
**Prioridad:** Alta
**Estimación:** 1 hora
**Asignado a:** Claude Code

## Descripción

Crear el perfil de customización `pyqt-mvc.json` que adapta el skill `implement-us` para proyectos PyQt6 con arquitectura MVC + Factory/Coordinator patterns.

Este perfil es el más específico ya que está basado en la implementación original de simapp_termostato.

## Criterios de Aceptación

- [ ] Archivo `skills/implement-us/customizations/pyqt-mvc.json` creado
- [ ] Schema JSON válido
- [ ] Override de valores específicos de PyQt/MVC
- [ ] Estructura MVC (modelo, vista, controlador) definida
- [ ] Test framework configurado (pytest + pytest-qt)
- [ ] Fixtures específicas definidas (qapp, qtbot)
- [ ] Base classes configuradas (ModeloBase, QWidget)
- [ ] Paths específicos de PyQt/MVC
- [ ] Compatible con fusión sobre config.json base

## Dependencias

- **Depende de:** TICKET-022 (config.json base creado)
- **Bloquea a:** TICKET-027 (testing)

## Notas Técnicas

### Estructura del Perfil

```json
{
  "profile_name": "pyqt-mvc",
  "profile_version": "1.0",
  "description": "Proyectos PyQt6 con arquitectura MVC + Factory/Coordinator patterns",
  "extends": "config.json",

  "architecture_patterns": {
    "default": "mvc",
    "available": ["mvc"]
  },

  "component_structure": {
    "mvc": {
      "files": [
        "modelo.py",
        "vista.py",
        "controlador.py"
      ],
      "base_path": "app/presentacion/paneles/{component_name}/",
      "description": "Estructura MVC para paneles PyQt"
    }
  },

  "test_framework": {
    "runner": "pytest",
    "plugins": [
      "pytest-qt",
      "pytest-cov",
      "pytest-bdd",
      "pytest-mock"
    ],
    "fixtures_required": [
      "qapp",
      "qtbot"
    ],
    "coverage_tool": "pytest-cov",
    "config_file": "pytest.ini"
  },

  "base_classes": {
    "model": "ModeloBase",
    "view": "QWidget",
    "controller": "object",
    "description": "Clases base para componentes MVC"
  },

  "dependencies": {
    "required": [
      "PyQt6>=6.4.0",
      "pytest>=7.0.0",
      "pytest-qt>=4.2.0",
      "pytest-cov>=4.0.0",
      "pytest-bdd>=6.0.0"
    ],
    "description": "Dependencias específicas del perfil"
  },

  "patterns": {
    "factory": {
      "enabled": true,
      "description": "Usar Factory pattern para creación de componentes"
    },
    "coordinator": {
      "enabled": true,
      "description": "Usar Coordinator pattern para gestión de flujos"
    }
  },

  "quality_gates": {
    "pylint_min": 8.0,
    "cc_max": 10,
    "mi_min": 20,
    "coverage_min": 95.0,
    "specific_rules": [
      "Qt-specific naming conventions",
      "Signal/Slot connections must be documented"
    ]
  },

  "templates": {
    "bdd": ".claude/templates/bdd/scenario.feature",
    "planning": ".claude/templates/planning/implementation-plan-mvc.md",
    "testing_unit": ".claude/templates/testing/test-unit-pyqt.py",
    "testing_integration": ".claude/templates/testing/test-integration-pyqt.py",
    "reporting": ".claude/templates/reporting/implementation-report.md"
  },

  "variables": {
    "architecture_pattern": "mvc",
    "component_type": "Panel",
    "component_path": "app/presentacion/paneles/{component_name}/",
    "test_framework": "pytest-qt",
    "base_class": "ModeloBase"
  },

  "example_component": {
    "name": "DisplayTemperatura",
    "files": [
      "app/presentacion/paneles/display_temperatura/modelo.py",
      "app/presentacion/paneles/display_temperatura/vista.py",
      "app/presentacion/paneles/display_temperatura/controlador.py"
    ],
    "description": "Ejemplo de componente típico en este perfil"
  }
}
```

### Validación

El perfil debe:
1. Extender `config.json` base (no redefinir todo)
2. Solo sobrescribir valores específicos de PyQt/MVC
3. Ser fusionable correctamente por el instalador

### Referencias

- Archivo original: `_work/from-simapp/skills/implement-us-config.json`
- Documentación PyQt: Patrones MVC específicos
- simapp_termostato: Estructura de referencia

## Checklist de Implementación

- [ ] Leer `_work/from-simapp/skills/implement-us-config.json` como base
- [ ] Extraer valores específicos de PyQt/MVC
- [ ] Crear estructura JSON del perfil
- [ ] Definir architecture_patterns (solo mvc)
- [ ] Definir component_structure MVC
- [ ] Definir test_framework con pytest-qt
- [ ] Definir base_classes específicas
- [ ] Definir dependencies de PyQt
- [ ] Definir patterns (Factory, Coordinator)
- [ ] Definir quality_gates específicas
- [ ] Definir templates específicas (si existen)
- [ ] Definir variables con valores MVC
- [ ] Agregar example_component
- [ ] Validar sintaxis JSON
- [ ] Verificar fusión con config.json base
- [ ] Guardar como `skills/implement-us/customizations/pyqt-mvc.json`

## Resultado

**Fecha de Completado:** _Pendiente_

### Archivo Generado

- Ubicación: `skills/implement-us/customizations/pyqt-mvc.json`
- Tamaño: _X_ líneas
- Validación JSON: ✅ / ❌

### Testing de Fusión

```bash
# Probar fusión config base + perfil
python -c "
import json
base = json.load(open('skills/implement-us/config.json'))
profile = json.load(open('skills/implement-us/customizations/pyqt-mvc.json'))
# Fusión... (implementar lógica)
"
```

### Commit

_Pendiente_

**Estado:** 📋 Pendiente
