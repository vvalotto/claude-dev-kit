# BRIEF — Issue #46: Perfil `hexagonal-ddd-bc` para `/implement-us`

> **Fecha:** 2026-04-09
> **Autor:** Preparado en sesión AtaraxiaDive para retomar en sesión claude-dev-kitc
> **Issue:** #46 en vvalotto/claude-dev-kit (OPEN)
> **Versión objetivo:** v1.4.0

---

## 1. Contexto del problema

El skill `/implement-us` tiene perfiles de customización en
`skills/implement-us/customizations/`. El perfil existente `fastapi-rest.json`
(v1.0.0) asume **arquitectura en capas** (Router → Service → Repository).

AtaraxiaDive usa **arquitectura hexagonal + DDD BC-first** (domain →
application → infrastructure → api) y actualmente tiene su propio
`fastapi-rest.json` v2.0.0 en `.claude/skills/implement-us/customizations/`
que sobreescribe el del dev kit. Ese archivo hace dos cosas que deberían
estar separadas:

1. Describe la arquitectura hexagonal DDD (genérico, reutilizable)
2. Describe los detalles de AtaraxiaDive (6 BCs específicos, paths, vocabulario IEDD)

El issue #46 pide un perfil genérico para cualquier proyecto con arquitectura
hexagonal DDD BC-first — no atado a AtaraxiaDive.

---

## 2. Qué hay que hacer

### Proyecto 1 — claude-dev-kitc (este proyecto, hacer primero)

**Crear** `skills/implement-us/customizations/hexagonal-ddd-bc.json`

Es el perfil genérico. Contiene todo lo que es reutilizable en cualquier
proyecto hexagonal DDD:
- `architecture_pattern: hexagonal`
- `component_type`: AggregateRoot, ValueObject, DomainEvent, Port,
  CommandHandler, QueryHandler, Repository, ApiRouter
- `component_structure`: estructura de archivos por tipo DDD
- `quality_gates`: con codeguard (no radon directo)
- `design_patterns`: la regla de oro hexagonal

**Anotar** `phases/phase-3-implementation.md`:
- Agregar nota condicional: cuando el perfil activo es `hexagonal-ddd-bc`,
  la secuencia de implementación dentro de una tarea sigue el orden DDD:
  VOs → Events → Aggregate → Ports → CommandHandlers → QueryHandlers →
  Repositories → ApiRouter (cada uno depende del anterior)

**Anotar** `phases/phase-7-quality-gates.md`:
- Agregar nota condicional: cuando el perfil activo es `hexagonal-ddd-bc`,
  usar `codeguard` en lugar de `radon` directamente (codeguard orquesta
  pylint + radon + designreviewer)

**Versionar** como v1.4.0 en CHANGELOG.md y PR.

### Proyecto 2 — AtaraxiaDive (después)

Reemplazar el `fastapi-rest.json` v2.0.0 por un perfil delgado que solo
tenga overrides específicos de AtaraxiaDive. Ver §6 de este brief.

---

## 3. Contenido de `hexagonal-ddd-bc.json`

El archivo de AtaraxiaDive (`.claude/skills/implement-us/customizations/fastapi-rest.json`)
es la fuente autoritativa. Lo que sigue es exactamente lo que debe ir al
perfil genérico del dev kit (sin los overrides de AtaraxiaDive).

```json
{
  "_comment_profile": "Perfil genérico para arquitectura hexagonal + DDD + BC-first",

  "profile_metadata": {
    "name": "hexagonal-ddd-bc",
    "display_name": "Hexagonal DDD BC-First",
    "description": "Arquitectura hexagonal con DDD organizada por Bounded Context. domain → application → infrastructure → api.",
    "extends": "config.json",
    "version": "1.0.0",
    "author": "Claude Dev Kit",
    "created": "2026-04-09",
    "target_stack": "Python 3.10+ + cualquier framework HTTP",
    "architecture": "Hexagonal DDD BC-First (domain → application → infrastructure → api)"
  },

  "variables": {
    "architecture_pattern": {
      "default": "hexagonal",
      "description": "Hexagonal DDD BC-first: domain → application → infrastructure → api",
      "available": ["hexagonal"],
      "layers": {
        "domain": "Aggregates, ValueObjects, DomainEvents, Ports (interfaces)",
        "application": "CommandHandlers, QueryHandlers",
        "infrastructure": "Repository implementations, EventStore, ACLs",
        "api": "Framework router del BC"
      },
      "golden_rule": "<bc>/domain/ no importa nada fuera de su domain/. Solo shared/domain/ es excepción."
    },
    "component_type": {
      "default": "AggregateRoot",
      "description": "Tipo de componente DDD a implementar",
      "available": [
        "AggregateRoot",
        "ValueObject",
        "DomainEvent",
        "Port",
        "CommandHandler",
        "QueryHandler",
        "Repository",
        "ApiRouter"
      ]
    },
    "component_path": {
      "default": "src/{bc}/domain/aggregates/",
      "description": "Ruta base según tipo de componente y BC",
      "by_component": {
        "AggregateRoot": "src/{bc}/domain/aggregates/",
        "ValueObject":   "src/{bc}/domain/value_objects/",
        "DomainEvent":   "src/{bc}/domain/events/",
        "Port":          "src/{bc}/domain/ports/",
        "CommandHandler":"src/{bc}/application/commands/",
        "QueryHandler":  "src/{bc}/application/queries/",
        "Repository":    "src/{bc}/infrastructure/repositories/",
        "ApiRouter":     "src/{bc}/api/"
      }
    },
    "test_framework": {
      "default": "pytest + httpx",
      "plugins": ["pytest-asyncio", "httpx", "pytest-cov", "pytest-bdd"]
    },
    "project_root": {
      "default": "src/",
      "description": "Raíz del código fuente — organizado por BC"
    }
  },

  "component_structure": {
    "bc_feature": {
      "description": "BC completo con arquitectura hexagonal DDD",
      "base_path": "src/{bc}/",
      "implementation_order": [
        "ValueObjects",
        "DomainEvents",
        "AggregateRoot",
        "Ports",
        "CommandHandlers",
        "QueryHandlers",
        "Repositories",
        "ApiRouter"
      ],
      "_comment_order": "El orden es obligatorio: cada elemento depende del anterior.",
      "files": {
        "aggregate": {
          "path": "src/{bc}/domain/aggregates/{nombre}.py",
          "responsibilities": [
            "Encapsula invariantes del BC",
            "Emite DomainEvents ante cambios de estado",
            "Sin dependencias de infraestructura"
          ]
        },
        "value_object": {
          "path": "src/{bc}/domain/value_objects/{nombre}.py",
          "responsibilities": [
            "Inmutable — frozen dataclass o __setattr__ bloqueado",
            "Validación propia en __init__",
            "Igualdad por valor, no por identidad"
          ]
        },
        "domain_event": {
          "path": "src/{bc}/domain/events/{nombre}.py",
          "responsibilities": [
            "Describe algo que ocurrió en el dominio",
            "Inmutable — todos los campos readonly",
            "Nombrado en pasado: EntidadCreada, EstadoCambiado"
          ]
        },
        "port": {
          "path": "src/{bc}/domain/ports/{nombre}.py",
          "responsibilities": [
            "Define el contrato de repositorio o servicio externo",
            "Solo métodos abstractos — sin implementación",
            "Implementado en infrastructure/"
          ]
        },
        "command_handler": {
          "path": "src/{bc}/application/commands/{nombre}_handler.py",
          "responsibilities": [
            "Carga aggregate desde repositorio",
            "Llama método del aggregate",
            "Persiste aggregate",
            "Sin lógica de negocio — delega al aggregate"
          ]
        },
        "query_handler": {
          "path": "src/{bc}/application/queries/{nombre}_handler.py",
          "responsibilities": [
            "Lee datos del repositorio o read model",
            "Retorna DTOs o view models",
            "Sin side effects"
          ]
        },
        "repository_impl": {
          "path": "src/{bc}/infrastructure/repositories/{nombre}_repository.py",
          "responsibilities": [
            "Implementa el puerto definido en domain/ports/",
            "Traduce entre domain objects y mecanismo de persistencia",
            "Sin lógica de negocio"
          ]
        },
        "api_router": {
          "path": "src/{bc}/api/router.py",
          "responsibilities": [
            "Solo importa application/ — nunca domain/ directamente",
            "Traduce HTTP request → Command/Query",
            "Traduce resultado → HTTP response"
          ]
        }
      },
      "test_files": {
        "test_aggregate":      "tests/unit/{bc}/test_{nombre}.py",
        "test_value_object":   "tests/unit/{bc}/test_{nombre}.py",
        "test_command_handler":"tests/unit/{bc}/test_{nombre}_handler.py",
        "test_integration":    "tests/integration/{bc}/test_{nombre}.py"
      }
    }
  },

  "quality_gates": {
    "codeguard": {
      "enabled": true,
      "tool": "codeguard",
      "command": "codeguard src/{bc}/ --format json",
      "notes": "CodeGuard orquesta pylint + radon + designreviewer. Usar codeguard, nunca radon directamente."
    },
    "pylint": {
      "enabled": true,
      "min_score": 8.0,
      "scope": "src/{bc}/domain/ + src/{bc}/application/",
      "notes": "Invocado por CodeGuard"
    },
    "cyclomatic_complexity": {
      "enabled": true,
      "max_per_function": 10,
      "tool": "radon (vía CodeGuard)"
    },
    "coverage": {
      "enabled": true,
      "min_percent": 90.0,
      "tool": "pytest-cov",
      "scope": "src/{bc}/domain/ + src/{bc}/application/",
      "notes": "Infrastructure y api no cuentan para el umbral mínimo"
    }
  },

  "design_patterns": {
    "hexagonal_architecture": {
      "description": "Hexagonal DDD BC-First",
      "import_rules": [
        "domain/: sin imports fuera de su propio domain/ (solo shared/domain/ permitido)",
        "application/: importa domain/, nunca infrastructure/",
        "infrastructure/: implementa puertos de domain/",
        "api/: importa application/, nunca domain/ directamente"
      ],
      "bc_communication": "Solo a través de puertos (domain/ports/). Nunca imports directos entre BCs.",
      "acl_location": "infrastructure/ del BC consumidor"
    },
    "aggregate_pattern": {
      "event_sourcing_note": "Si el BC usa Event Sourcing, los eventos son la fuente de verdad. El aggregate los emite y se reconstruye desde ellos.",
      "crud_note": "Si el BC es CRUD, el aggregate tiene estado directo. Los eventos son opcionales (auditoria)."
    }
  },

  "bdd_config": {
    "runner": "pytest-bdd",
    "language_note": "NO usar # language: es — pytest-bdd 8.x requiere English keywords (Given/When/Then)",
    "tag_prefix": "@US-"
  }
}
```

---

## 4. Anotación en `phase-3-implementation.md`

Agregar una sección condicional **después del bloque "Leer las rutas exactas
de componentes"** (línea ~48 del archivo actual):

```markdown
#### Si el perfil activo es `hexagonal-ddd-bc` — Orden de implementación obligatorio

En arquitectura hexagonal DDD, los componentes tienen dependencias directas
entre sí. Implementar siempre en este orden dentro de cada BC:

1. **ValueObjects** — sin dependencias
2. **DomainEvents** — usan ValueObjects
3. **AggregateRoot** — usa VOs y emite Events
4. **Ports** — interfaces ABC que el Aggregate necesita
5. **CommandHandlers** — usan Aggregate + Ports
6. **QueryHandlers** — usan Ports o read models
7. **Repositories** — implementan Ports
8. **ApiRouter** — importa solo application/

No implementar un componente si su dependencia no está lista y testeada.
```

---

## 5. Anotación en `phase-7-quality-gates.md`

Agregar una nota condicional **al inicio de la sección "Métricas de Calidad"**:

```markdown
> **Si el perfil activo es `hexagonal-ddd-bc`:** No usar `radon` directamente.
> Usar `codeguard` que orquesta pylint + radon + designreviewer en una sola pasada.
>
> ```bash
> codeguard src/{bc}/ --format json > quality/reports/codeguard/{US_ID}-codeguard.json
> ```
>
> `designreviewer` se ejecuta **al cierre del Incremento** (no por US), vía pre-push hook
> o manualmente. Si reporta CRITICAL, bloquea el merge.
```

---

## 6. Qué queda en AtaraxiaDive (perfil delgado post-migración)

Después de crear `hexagonal-ddd-bc.json` en el dev kit, el archivo de
AtaraxiaDive se renombra a `hexagonal-ddd-bc.json` y se slim-down a solo
los overrides de proyecto:

```json
{
  "_comment": "Override de hexagonal-ddd-bc.json para AtaraxiaDive",
  "profile_metadata": {
    "name": "hexagonal-ddd-bc",
    "display_name": "AtaraxiaDive — Hexagonal DDD BC-First",
    "version": "1.0.0",
    "target_stack": "FastAPI + Python 3.14 + uv",
    "context_document": "docs/contexto/ATARAXIADIVE-CONTEXT.md"
  },
  "variables": {
    "project_root": {
      "bounded_contexts": ["competencia", "torneo", "registro", "resultados", "identidad", "notificaciones"],
      "shared": "src/shared/domain/",
      "app_entry": "src/app.py"
    }
  },
  "quality_gates": {
    "codeguard": {
      "command": "codeguard src/{bc}/ --format json > quality/reports/codeguard/{US_ID}-codeguard.json",
      "designreviewer_command": "designreviewer src/ --config pyproject.toml"
    },
    "coverage": { "min_percent": 90.0 }
  },
  "documentation_config": {
    "spec_path": "docs/specs/sp{SP}/",
    "plan_path": "docs/plans/sp{SP}/",
    "report_path": "docs/reports/",
    "adr_path": "docs/adr/"
  }
}
```

*(El `ATARAXIADIVE-CONTEXT.md` se crea por separado — es el doc de contexto
rico para Fase 0, con descripción del dominio, BCs, lenguaje ubicuo, etc.)*

---

## 7. Entrada de CHANGELOG para v1.4.0

```markdown
## [1.4.0] - 2026-04-09

### Agregado

#### Perfil `hexagonal-ddd-bc` para el skill `implement-us`

- Nuevo perfil de customización `skills/implement-us/customizations/hexagonal-ddd-bc.json`
  para proyectos con arquitectura hexagonal + DDD + BC-first (Bounded Context first)
- Cubre los 8 tipos de componentes DDD: AggregateRoot, ValueObject, DomainEvent,
  Port, CommandHandler, QueryHandler, Repository, ApiRouter
- Define `implementation_order` explícito (VOs → Events → Aggregate → Ports →
  CommandHandlers → QueryHandlers → Repositories → ApiRouter)
- Integrado con `codeguard` como orquestador de quality gates (no radon directo)
- Cierra issue #46

#### Anotaciones en fases para arquitectura hexagonal

- `phase-3-implementation.md`: nota sobre el orden de implementación obligatorio
  para BCs DDD
- `phase-7-quality-gates.md`: nota sobre uso de `codeguard` en lugar de `radon`
  directo cuando el perfil activo es `hexagonal-ddd-bc`
```

---

## 8. Secuencia de trabajo recomendada

1. Crear `skills/implement-us/customizations/hexagonal-ddd-bc.json` con el
   contenido del §3
2. Anotar `phase-3-implementation.md` (§4)
3. Anotar `phase-7-quality-gates.md` (§5)
4. Agregar entrada en `CHANGELOG.md` (§7)
5. Correr los tests del dev kit si existen
6. Commit + PR + release tag `v1.4.0`
7. (En sesión AtaraxiaDive) slim-down del perfil local según §6

---

## 9. Archivos a modificar/crear en claude-dev-kitc

| Acción | Archivo |
|--------|---------|
| CREAR | `skills/implement-us/customizations/hexagonal-ddd-bc.json` |
| EDITAR | `skills/implement-us/phases/phase-3-implementation.md` |
| EDITAR | `skills/implement-us/phases/phase-7-quality-gates.md` |
| EDITAR | `CHANGELOG.md` |

---

*Brief preparado en sesión AtaraxiaDive — 2026-04-09*
