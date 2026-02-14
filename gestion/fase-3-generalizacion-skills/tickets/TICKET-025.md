# TICKET-025: Crear perfil django-mvt.json

**Fase:** 3 - Generalización de Skills
**Sprint:** 2
**Estado:** TODO
**Prioridad:** Media
**Estimación:** 1.5 horas
**Asignado a:** Claude Code

## Descripción

Crear el perfil de customización `django-mvt.json` que adapta el skill `implement-us` para aplicaciones web Django siguiendo el patrón MVT (Model-View-Template) y las convenciones de Django.

## Criterios de Aceptación

- [ ] Archivo `skills/implement-us/customizations/django-mvt.json` creado
- [ ] Schema JSON válido
- [ ] Patrón MVT definido (model, view, template, forms, urls)
- [ ] Test framework configurado (pytest-django)
- [ ] Fixtures Django definidas (db, client, admin_client)
- [ ] Convenciones Django seguidas (apps, migrations, admin)
- [ ] Paths específicos de Django
- [ ] Compatible con fusión sobre config.json base

## Dependencias

- **Depende de:** TICKET-022 (config.json base creado)
- **Bloquea a:** TICKET-027 (testing)

## Notas Técnicas

### Estructura del Perfil

```json
{
  "profile_name": "django-mvt",
  "profile_version": "1.0",
  "description": "Aplicaciones web Django con patrón MVT",
  "extends": "config.json",

  "architecture_patterns": {
    "default": "mvt",
    "available": ["mvt"]
  },

  "component_structure": {
    "mvt": {
      "files": [
        "models.py",
        "views.py",
        "forms.py",
        "urls.py",
        "admin.py",
        "templates/{app_name}/{template_name}.html"
      ],
      "base_path": "{app_name}/",
      "description": "Estructura MVT para apps Django"
    }
  },

  "test_framework": {
    "runner": "pytest",
    "plugins": [
      "pytest-django",
      "pytest-cov",
      "pytest-mock"
    ],
    "fixtures_required": [
      "db",
      "client",
      "admin_client",
      "django_user_model"
    ],
    "coverage_tool": "pytest-cov",
    "config_file": "pytest.ini",
    "django_settings": "project.settings.test"
  },

  "base_classes": {
    "model": "models.Model",
    "view": "View",
    "form": "forms.Form",
    "admin": "admin.ModelAdmin",
    "description": "Clases base para componentes Django"
  },

  "dependencies": {
    "required": [
      "django>=4.2.0",
      "pytest>=7.0.0",
      "pytest-django>=4.5.0",
      "pytest-cov>=4.0.0"
    ],
    "description": "Dependencias específicas del perfil"
  },

  "django_conventions": {
    "apps": {
      "required_files": [
        "__init__.py",
        "apps.py",
        "models.py",
        "views.py",
        "urls.py",
        "admin.py",
        "tests.py"
      ],
      "optional_files": [
        "forms.py",
        "serializers.py",
        "signals.py",
        "managers.py"
      ]
    },
    "migrations": {
      "auto_generate": true,
      "naming": "auto"
    },
    "admin": {
      "register_all_models": true
    },
    "description": "Convenciones específicas de Django"
  },

  "patterns": {
    "class_based_views": {
      "enabled": true,
      "preferred": true,
      "description": "Preferir CBVs sobre FBVs"
    },
    "generic_views": {
      "enabled": true,
      "description": "Usar generic views de Django cuando sea apropiado"
    },
    "signals": {
      "enabled": true,
      "description": "Usar signals para desacoplamiento"
    }
  },

  "quality_gates": {
    "pylint_min": 8.0,
    "cc_max": 10,
    "mi_min": 20,
    "coverage_min": 90.0,
    "specific_rules": [
      "All models must have __str__ method",
      "All models must have Meta class with ordering",
      "All views must have docstrings"
    ]
  },

  "templates": {
    "bdd": ".claude/templates/bdd/scenario-web.feature",
    "planning": ".claude/templates/planning/implementation-plan-django.md",
    "testing_unit": ".claude/templates/testing/test-unit-django.py",
    "testing_integration": ".claude/templates/testing/test-integration-django.py",
    "reporting": ".claude/templates/reporting/implementation-report.md"
  },

  "variables": {
    "architecture_pattern": "mvt",
    "component_type": "App",
    "component_path": "{app_name}/",
    "test_framework": "pytest-django",
    "base_class": "models.Model"
  },

  "url_conventions": {
    "pattern": "path",
    "namespace": "recommended",
    "naming": "kebab-case",
    "description": "Convenciones de URLs Django"
  },

  "example_component": {
    "name": "blog",
    "app_name": "blog",
    "files": [
      "blog/models.py",
      "blog/views.py",
      "blog/forms.py",
      "blog/urls.py",
      "blog/admin.py",
      "blog/templates/blog/post_list.html",
      "blog/templates/blog/post_detail.html"
    ],
    "models": [
      "Post",
      "Category",
      "Comment"
    ],
    "views": [
      "PostListView",
      "PostDetailView",
      "PostCreateView",
      "PostUpdateView"
    ],
    "description": "Ejemplo de app Django típica (blog)"
  }
}
```

### Convenciones Django

- **Apps:** Cada componente es una app Django
- **Modelos:** Heredan de models.Model
- **Vistas:** Preferir Class-Based Views
- **Templates:** En `templates/{app_name}/`
- **URLs:** path() en lugar de url()
- **Admin:** Registrar todos los modelos
- **Migraciones:** Auto-generadas con makemigrations

## Checklist de Implementación

- [ ] Investigar convenciones Django actuales (Django 4.2+)
- [ ] Crear estructura JSON del perfil
- [ ] Definir architecture_patterns (mvt)
- [ ] Definir component_structure MVT
- [ ] Definir test_framework con pytest-django
- [ ] Definir base_classes para Django
- [ ] Definir dependencies de Django
- [ ] Definir django_conventions (apps, migrations, admin)
- [ ] Definir patterns (CBV, generic views, signals)
- [ ] Definir quality_gates específicas
- [ ] Definir templates específicas
- [ ] Definir variables con valores Django
- [ ] Definir url_conventions
- [ ] Agregar example_component (blog app)
- [ ] Validar sintaxis JSON
- [ ] Verificar fusión con config.json base
- [ ] Guardar como `skills/implement-us/customizations/django-mvt.json`

## Resultado

**Fecha de Completado:** _Pendiente_

### Archivo Generado

- Ubicación: `skills/implement-us/customizations/django-mvt.json`
- Tamaño: _X_ líneas
- Validación JSON: ✅ / ❌

### Commit

_Pendiente_

**Estado:** 📋 Pendiente
