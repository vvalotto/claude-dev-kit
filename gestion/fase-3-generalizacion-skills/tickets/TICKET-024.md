# TICKET-024: Crear perfil fastapi-rest.json

**Fase:** 3 - Generalización de Skills
**Sprint:** 2
**Estado:** TODO
**Prioridad:** Media
**Estimación:** 1.5 horas
**Asignado a:** Claude Code

## Descripción

Crear el perfil de customización `fastapi-rest.json` que adapta el skill `implement-us` para proyectos de APIs REST con FastAPI y arquitectura en capas.

Este perfil demuestra la versatilidad del framework para stacks completamente diferentes a PyQt.

## Criterios de Aceptación

- [ ] Archivo `skills/implement-us/customizations/fastapi-rest.json` creado
- [ ] Schema JSON válido
- [ ] Arquitectura en capas definida (router, service, repository, model)
- [ ] Test framework configurado (pytest + httpx)
- [ ] Fixtures específicas definidas (client, test_db)
- [ ] Base classes para entidades/servicios
- [ ] Paths específicos de FastAPI
- [ ] Compatible con fusión sobre config.json base

## Dependencias

- **Depende de:** TICKET-022 (config.json base creado)
- **Bloquea a:** TICKET-027 (testing)

## Notas Técnicas

### Estructura del Perfil

```json
{
  "profile_name": "fastapi-rest",
  "profile_version": "1.0",
  "description": "APIs REST con FastAPI y arquitectura en capas",
  "extends": "config.json",

  "architecture_patterns": {
    "default": "layered",
    "available": ["layered", "clean-architecture"]
  },

  "component_structure": {
    "layered": {
      "files": [
        "router.py",
        "schemas.py",
        "service.py",
        "repository.py",
        "models.py"
      ],
      "base_path": "app/{component_name}/",
      "description": "Arquitectura en capas para APIs REST"
    }
  },

  "test_framework": {
    "runner": "pytest",
    "plugins": [
      "pytest-asyncio",
      "pytest-cov",
      "httpx"
    ],
    "fixtures_required": [
      "client",
      "test_db",
      "async_client"
    ],
    "coverage_tool": "pytest-cov",
    "config_file": "pytest.ini"
  },

  "base_classes": {
    "router": "APIRouter",
    "service": "object",
    "repository": "object",
    "model": "Base",
    "schema": "BaseModel",
    "description": "Clases base para componentes de API"
  },

  "dependencies": {
    "required": [
      "fastapi>=0.104.0",
      "uvicorn>=0.24.0",
      "pydantic>=2.0.0",
      "sqlalchemy>=2.0.0",
      "pytest>=7.0.0",
      "pytest-asyncio>=0.21.0",
      "httpx>=0.25.0",
      "pytest-cov>=4.0.0"
    ],
    "description": "Dependencias específicas del perfil"
  },

  "patterns": {
    "dependency_injection": {
      "enabled": true,
      "description": "Usar Depends() de FastAPI para inyección de dependencias"
    },
    "async_await": {
      "enabled": true,
      "description": "Usar async/await para operaciones I/O"
    }
  },

  "quality_gates": {
    "pylint_min": 8.0,
    "cc_max": 10,
    "mi_min": 20,
    "coverage_min": 90.0,
    "specific_rules": [
      "All endpoints must have response models",
      "All async functions must be tested with pytest-asyncio"
    ]
  },

  "templates": {
    "bdd": ".claude/templates/bdd/scenario-api.feature",
    "planning": ".claude/templates/planning/implementation-plan-api.md",
    "testing_unit": ".claude/templates/testing/test-unit-fastapi.py",
    "testing_integration": ".claude/templates/testing/test-integration-fastapi.py",
    "reporting": ".claude/templates/reporting/implementation-report.md"
  },

  "variables": {
    "architecture_pattern": "layered",
    "component_type": "Endpoint",
    "component_path": "app/{component_name}/",
    "test_framework": "pytest + httpx",
    "base_class": "APIRouter"
  },

  "api_conventions": {
    "versioning": "path",
    "prefix": "/api/v1",
    "response_model": "required",
    "status_codes": "explicit",
    "description": "Convenciones de API REST"
  },

  "example_component": {
    "name": "users",
    "files": [
      "app/users/router.py",
      "app/users/schemas.py",
      "app/users/service.py",
      "app/users/repository.py",
      "app/users/models.py"
    ],
    "endpoints": [
      "GET /api/v1/users",
      "POST /api/v1/users",
      "GET /api/v1/users/{id}",
      "PUT /api/v1/users/{id}",
      "DELETE /api/v1/users/{id}"
    ],
    "description": "Ejemplo de endpoint CRUD típico"
  }
}
```

### Diferencias Clave con PyQt/MVC

- **Componente:** Endpoint/Resource vs Panel
- **Archivos:** router/service/repository vs modelo/vista/controlador
- **Testing:** httpx + async vs pytest-qt + QWidget
- **Base Path:** app/{resource}/ vs app/presentacion/paneles/
- **Patterns:** Dependency Injection vs Factory/Coordinator

## Checklist de Implementación

- [ ] Investigar convenciones FastAPI
- [ ] Crear estructura JSON del perfil
- [ ] Definir architecture_patterns (layered, clean-architecture)
- [ ] Definir component_structure en capas
- [ ] Definir test_framework con pytest-asyncio + httpx
- [ ] Definir base_classes para API
- [ ] Definir dependencies de FastAPI
- [ ] Definir patterns (DI, async/await)
- [ ] Definir quality_gates específicas
- [ ] Definir templates específicas
- [ ] Definir variables con valores API
- [ ] Definir api_conventions
- [ ] Agregar example_component (CRUD)
- [ ] Validar sintaxis JSON
- [ ] Verificar fusión con config.json base
- [ ] Guardar como `skills/implement-us/customizations/fastapi-rest.json`

## Resultado

**Fecha de Completado:** _Pendiente_

### Archivo Generado

- Ubicación: `skills/implement-us/customizations/fastapi-rest.json`
- Tamaño: _X_ líneas
- Validación JSON: ✅ / ❌

### Commit

_Pendiente_

**Estado:** 📋 Pendiente
