# TICKET-012: Crear install/config.yaml con configuración base

**Fase:** 2 - Sistema de Instalación
**Sprint:** 1
**Estado:** DONE
**Prioridad:** Alta
**Estimación:** 2 horas
**Asignado a:** Claude Code

## Descripción

Crear el archivo `install/config.yaml` que contendrá toda la configuración del sistema de instalación, incluyendo definiciones de perfiles para diferentes stacks tecnológicos, paths de instalación, y reglas de validación.

Este archivo es crucial porque define cómo el instalador se comporta para cada tipo de proyecto (PyQt, FastAPI, Django, genérico).

## Criterios de Aceptación

- [ ] Archivo `install/config.yaml` creado con estructura válida
- [ ] 4 perfiles definidos: pyqt-mvc, fastapi-rest, django-mvt, generic-python
- [ ] Cada perfil incluye: name, description, architecture_pattern, test_framework
- [ ] Sección `validation` con required_dirs y required_files
- [ ] Sección `installation` con paths y configuración de copia
- [ ] Sintaxis YAML correcta y validada
- [ ] Documentación inline (comentarios) clara

## Dependencias

- **Depende de:** Ninguna (puede hacerse en paralelo)
- **Bloquea a:** TICKET-013 (instalador lee este config)

## Notas Técnicas

### Estructura del Archivo

```yaml
# Claude Dev Kit - Configuración de Instalación
version: "1.0"

# Perfiles por stack tecnológico
profiles:
  pyqt-mvc:
    name: "PyQt + MVC"
    description: "PyQt6 applications with MVC architecture"
    architecture_pattern: "mvc"
    test_framework: "pytest-qt"
    component_types:
      - "Panel"
      - "Model"
      - "Controller"
      - "Display"
    patterns:
      - "Factory"
      - "Coordinator"
      - "Observer"

  fastapi-rest:
    name: "FastAPI + REST"
    description: "FastAPI REST APIs with layered architecture"
    architecture_pattern: "layered"
    test_framework: "pytest"
    component_types:
      - "Router"
      - "Service"
      - "Repository"
      - "Schema"
    patterns:
      - "Dependency Injection"
      - "Repository Pattern"

  django-mvt:
    name: "Django + MVT"
    description: "Django applications with Model-View-Template pattern"
    architecture_pattern: "mvt"
    test_framework: "pytest-django"
    component_types:
      - "Model"
      - "View"
      - "Template"
      - "Form"
    patterns:
      - "MTV Pattern"
      - "Class-Based Views"

  generic-python:
    name: "Generic Python"
    description: "Generic Python projects without specific framework"
    architecture_pattern: "modular"
    test_framework: "pytest"
    component_types:
      - "Module"
      - "Class"
      - "Function"
    patterns:
      - "SOLID Principles"

# Configuración de instalación
installation:
  target_dir: ".claude"
  create_claude_md: true
  overwrite_policy: "ask"  # ask, skip, overwrite

  copy_rules:
    - source: "skills"
      target: "{target_dir}/skills"
      recursive: true
    - source: "templates"
      target: "{target_dir}/templates"
      recursive: true
    - source: "tracking"
      target: "{target_dir}/tracking"
      recursive: true

# Reglas de validación post-instalación
validation:
  required_dirs:
    - ".claude"
    - ".claude/skills"
    - ".claude/skills/implement-us"
    - ".claude/templates"
    - ".claude/templates/bdd"
    - ".claude/templates/planning"
    - ".claude/templates/testing"
    - ".claude/templates/reporting"
    - ".claude/tracking"

  required_files:
    - ".claude/config.json"
    - ".claude/skills/implement-us/SKILL.md"
    - ".claude/tracking/time_tracker.py"
    - ".claude/tracking/commands.py"

  optional_files:
    - "CLAUDE.md"
    - ".claude/hooks/save-session.sh"
```

### Validación YAML

```bash
# Validar sintaxis
python3 -c "import yaml; yaml.safe_load(open('install/config.yaml'))"
```

## Checklist de Implementación

- [ ] Crear estructura base del YAML
- [ ] Definir perfil pyqt-mvc completo
- [ ] Definir perfil fastapi-rest completo
- [ ] Definir perfil django-mvt completo
- [ ] Definir perfil generic-python completo
- [ ] Agregar sección installation con copy_rules
- [ ] Agregar sección validation con required_dirs/files
- [ ] Agregar comentarios explicativos
- [ ] Validar sintaxis YAML
- [ ] Documentar uso del archivo

## Resultado

**Fecha de Completado:** 2026-02-09

### Archivo Creado

```
install/config.yaml (272 líneas, 8.7KB)
```

**Contenido:**
- 4 perfiles completos (pyqt-mvc, fastapi-rest, django-mvt, generic-python)
- Sección installation con copy_rules y generated_files
- Sección validation con required_dirs/files y checks
- Sección messages con textos de instalación
- Comentarios explicativos inline

### Validación

- ✅ Sintaxis YAML válida
- ✅ 4 perfiles detectados correctamente
- ✅ Versión 1.0 configurada
- ✅ Commit: f8a05e6

**Estado:** ✅ Completado
