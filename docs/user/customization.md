# Guía de Personalización

**Última Actualización:** 2026-02-15
**Audiencia:** Usuario Avanzado
**Nivel:** Intermedio

---

## Introducción

Esta guía explica cómo personalizar Claude Dev Kit para adaptarlo exactamente a tu stack tecnológico y workflow.

**Personalización disponible:**
- Sistema de perfiles
- Variables y snippets
- Configuración de skills
- Templates custom
- Quality gates

---

## Sistema de Perfiles

Los perfiles definen comportamiento y estructura según tu stack.

### Perfiles Predefinidos

```bash
# Usar perfil predefinido
python ~/.claude-dev-kit/install/installer.py --profile pyqt-mvc
```

| Perfil | Stack | Arquitectura | Tests |
|--------|-------|--------------|-------|
| pyqt-mvc | PyQt6 Desktop | MVC | pytest-qt |
| fastapi-rest | FastAPI API | Layered | pytest-asyncio |
| flask-rest | Flask API | Blueprints | pytest-flask |
| flask-webapp | Flask Web | MVT | pytest-flask |
| generic-python | Python | Flexible | pytest |

### Crear Perfil Custom

```bash
# Copiar perfil base
cp .claude/skills/implement-us/customizations/generic-python.json \
   .claude/skills/implement-us/customizations/mi-perfil.json

# Editar perfil
nano .claude/skills/implement-us/customizations/mi-perfil.json
```

**Ejemplo - Perfil Django:**
```json
{
  "profile_name": "django-mvt",
  "architecture_pattern": "mvt",
  "component_types": ["Model", "View", "Template", "Form"],
  "test_framework": "pytest-django",
  "directory_structure": {
    "models": "app/models/",
    "views": "app/views/",
    "templates": "app/templates/",
    "tests": "app/tests/"
  },
  "quality_gates": {
    "pylint_threshold": 9.0,
    "coverage_threshold": 95,
    "max_complexity": 8
  }
}
```

---

## Personalización de Skills

Modifica comportamiento del skill implement-us.

### Archivo de Configuración

```bash
# Editar config principal
nano .claude/skills/implement-us/config.json
```

### Opciones Principales

```json
{
  "profile": "generic-python",
  "architecture_pattern": "layered",
  "test_framework": "pytest",

  "phases": {
    "enable_bdd": true,
    "enable_integration_tests": true,
    "enable_quality_gates": true,
    "enable_documentation": true
  },

  "quality_gates": {
    "pylint_threshold": 8.0,
    "coverage_threshold": 90,
    "max_complexity": 10,
    "min_maintainability": 20
  },

  "tracking": {
    "auto_start": true,
    "track_pauses": true
  }
}
```

### Deshabilitar Fases

```json
{
  "phases": {
    "enable_bdd": false,              // Saltar BDD
    "enable_integration_tests": false // Saltar integración
  }
}
```

---

## Sistema de Variables

Variables disponibles en templates.

### Variables Core

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `{US_ID}` | ID de historia | US-001 |
| `{US_TITLE}` | Título de US | Calculadora Simple |
| `{ARCHITECTURE_PATTERN}` | Patrón arquitectónico | mvc, mvt, layered |
| `{COMPONENT_TYPE}` | Tipo de componente | Model, View, Controller |
| `{COMPONENT_PATH}` | Ruta de archivo | src/models/calculator.py |
| `{TEST_FRAMEWORK}` | Framework de tests | pytest, pytest-qt |

### Usar Variables en Templates

```markdown
# Plan de Implementación: {US_TITLE}

## Arquitectura: {ARCHITECTURE_PATTERN}

### Componentes

1. {COMPONENT_TYPE}: {COMPONENT_PATH}
```

**Resultado:**
```markdown
# Plan de Implementación: Calculadora Simple

## Arquitectura: MVC

### Componentes

1. Model: src/models/calculator.py
```

---

## Personalización de Templates

Modifica templates para tu proyecto.

### Templates Disponibles

```
.claude/templates/
├── bdd/
│   ├── scenario.feature
│   └── steps.py
├── planning/
│   ├── implementation-plan.md
│   └── task-breakdown.md
├── testing/
│   ├── test-unit.py
│   └── test-integration.py
└── reporting/
    └── implementation-report.md
```

### Modificar Template

```bash
# Editar template de plan
nano .claude/templates/planning/implementation-plan.md
```

**Ejemplo - Agregar sección custom:**
```markdown
## Arquitectura

Patrón: {ARCHITECTURE_PATTERN}

## Security Considerations

- [ ] Validación de inputs
- [ ] Sanitización de datos
- [ ] Manejo seguro de errores

## Performance

- [ ] Complejidad algorítmica aceptable
- [ ] Sin cuellos de botella obvios
```

---

## Snippets Custom

Snippets son bloques de código reutilizables.

### Definir Snippet

En tu perfil custom:

```json
{
  "snippets": {
    "django_view": "def {view_name}(request):\n    context = {}\n    return render(request, '{template}', context)",
    "django_model": "class {ModelName}(models.Model):\n    created_at = models.DateTimeField(auto_now_add=True)\n    updated_at = models.DateTimeField(auto_now=True)"
  }
}
```

### Usar Snippet en Template

```python
# En test-unit.py template
{SNIPPET:django_model}
```

**Resultado:**
```python
class Calculator(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

---

## Quality Gates Personalizados

Ajusta umbrales según tu proyecto.

### Configuración Estricta

```json
{
  "quality_gates": {
    "pylint_threshold": 9.5,
    "coverage_threshold": 98,
    "max_complexity": 6,
    "min_maintainability": 25
  }
}
```

### Configuración Permisiva

```json
{
  "quality_gates": {
    "pylint_threshold": 7.0,
    "coverage_threshold": 80,
    "max_complexity": 15,
    "min_maintainability": 15
  }
}
```

### Deshabilitar Quality Gates

```json
{
  "phases": {
    "enable_quality_gates": false
  }
}
```

---

## Ejemplos Completos

### Ejemplo 1: Django REST Framework

```json
{
  "profile_name": "django-rest",
  "architecture_pattern": "mvt",
  "test_framework": "pytest-django",
  "component_types": ["Serializer", "ViewSet", "Model"],
  "quality_gates": {
    "pylint_threshold": 9.0,
    "coverage_threshold": 95
  },
  "snippets": {
    "serializer": "class {Name}Serializer(serializers.ModelSerializer):\n    class Meta:\n        model = {Name}\n        fields = '__all__'",
    "viewset": "class {Name}ViewSet(viewsets.ModelViewSet):\n    queryset = {Name}.objects.all()\n    serializer_class = {Name}Serializer"
  }
}
```

### Ejemplo 2: CLI Application

```json
{
  "profile_name": "python-cli",
  "architecture_pattern": "layered",
  "test_framework": "pytest",
  "phases": {
    "enable_bdd": false,
    "enable_integration_tests": true
  },
  "quality_gates": {
    "pylint_threshold": 8.5,
    "coverage_threshold": 92
  }
}
```

---

## Troubleshooting

### Profile not found

**Solución:**
```bash
# Listar perfiles disponibles
ls .claude/skills/implement-us/customizations/

# Usar nombre exacto de archivo (sin .json)
python installer.py --profile flask-rest
```

### Template variables not replaced

**Verificar sintaxis:**
```bash
# Correcto
{US_ID}

# Incorrecto
{{US_ID}}
$US_ID
```

---

## Recursos Adicionales

- [Configuración](./configuration.md) - Referencia completa de opciones
- [Sistema de Templates](../developer/architecture/template-system.md) - Variables y snippets
- [Creando Skills](../developer/contributing/creating-skills.md) - Skills custom

---

**Anterior:** [Instalación](./installation.md)
**Siguiente:** [Configuración](./configuration.md)
**Índice:** [Volver al índice](./index.md)
