# TICKET-037: Documentación de Templates y Sistema de Variables

**Fase:** 4 - Generalización de Templates
**Sprint:** 2
**Estado:** TODO
**Prioridad:** Media
**Estimación:** 1 hora
**Asignado a:** Claude Code

---

## Descripción

Crear documentación completa del sistema de templates generalizado, incluyendo referencia de variables, guía de uso, guía de personalización, y actualizar README principal del proyecto.

---

## Criterios de Aceptación

- [ ] `templates/README.md` completo con:
  - [ ] Introducción al sistema de templates
  - [ ] Referencia completa de variables
  - [ ] Guía de uso para cada template
  - [ ] Ejemplos por perfil
  - [ ] Guía de personalización
- [ ] Documentación técnica en `docs/templates/`
- [ ] README principal del proyecto actualizado
- [ ] CHANGELOG.md actualizado con Fase 4

---

## Dependencias

**Depende de:**
- ✅ TICKET-032 a TICKET-035: Templates generalizados
- ✅ TICKET-036: Ejemplos validados

**Bloquea a:**
- Fase 5: Sistema de Tracking

---

## Estructura de Documentación

### 1. templates/README.md

#### Sección 1: Introducción
```markdown
# Templates del Claude Dev Kit

Este directorio contiene templates generalizados usados por el skill /implement-us
para generar documentación automática durante la implementación de historias de
usuario.

## Filosofía

Los templates son framework-agnostic y se adaptan automáticamente al perfil
tecnológico del proyecto mediante un sistema de variables y snippets.
```

#### Sección 2: Categorías de Templates

Descripción detallada de cada template:
- Propósito
- Cuándo se usa (fase del skill)
- Variables principales
- Ejemplo de output

#### Sección 3: Referencia de Variables

Tabla completa de todas las variables disponibles:

| Variable | Tipo | Descripción | Ejemplo | Usado en |
|----------|------|-------------|---------|----------|
| `{US_ID}` | String | ID de historia | US-001 | Todos |
| `{US_TITLE}` | String | Título de historia | Implementar... | Todos |
| `{ARCHITECTURE_PATTERN}` | String | Patrón arquitectónico | mvc, layered | Plan, Report |
| `{BACKGROUND_SETUP}` | Snippet | Setup de escenario BDD | Given app iniciada... | BDD |
| `{TEST_IMPORTS}` | Snippet | Imports de tests | from PyQt6... | Testing |
| ... | ... | ... | ... | ... |

**Total:** ~20-25 variables documentadas

#### Sección 4: Sistema de Snippets

Explicar cómo funcionan los snippets:
- Qué son snippets
- Cómo se definen en perfiles
- Cómo se aplican en templates
- Ejemplos

#### Sección 5: Guía de Uso

Cómo el skill /implement-us usa templates:

```markdown
## Flujo de Generación

1. El skill determina la fase actual (BDD, Planning, Testing, etc.)
2. Carga el template correspondiente
3. Lee variables del perfil activo
4. Reemplaza placeholders `{VARIABLE}` con valores
5. Aplica snippets específicos del perfil
6. Genera archivo final
```

#### Sección 6: Ejemplos por Perfil

Links a ejemplos en subdirectorios `examples/`:
- Ver `bdd/examples/pyqt-mvc.feature` para ejemplo PyQt
- Ver `planning/examples/fastapi-rest.md` para ejemplo FastAPI
- etc.

#### Sección 7: Personalización

Guía para crear templates custom o modificar existentes:
- Crear nuevo template
- Agregar variables custom
- Agregar snippets custom a perfiles
- Testing de templates custom

---

### 2. docs/templates/template-system.md

Documentación técnica detallada:
- Arquitectura del sistema de templates
- Algoritmo de reemplazo de variables
- Sistema de snippets (implementación)
- Extensibilidad
- Best practices

---

### 3. Actualizar README.md Principal

Agregar sección sobre templates:

```markdown
## Sistema de Templates

El framework incluye 4 templates generalizados:

- **BDD Scenarios** - Escenarios Gherkin
- **Implementation Plans** - Planes de implementación
- **Implementation Reports** - Reportes finales
- **Unit Tests** - Tests unitarios

Los templates se adaptan automáticamente al perfil tecnológico del proyecto.

Ver [templates/README.md](templates/README.md) para más detalles.
```

---

### 4. Actualizar CHANGELOG.md

```markdown
## [Unreleased]

### Added

#### Fase 4: Generalización de Templates (Sprint 2)

- Sistema de templates generalizado con 4 templates framework-agnostic
- Templates BDD, Planning, Testing y Reporting
- Sistema de variables expandido (20+ variables)
- Sistema de snippets por perfil
- 20 ejemplos validados (4 templates × 5 perfiles)
- Documentación completa del sistema de templates

**Tickets:** TICKET-030 a TICKET-037

**Commits:** 8 commits

**Líneas:** ~2,000 líneas de templates y documentación
```

---

## Checklist de Implementación

### templates/README.md

- [ ] Sección 1: Introducción
- [ ] Sección 2: Categorías de Templates
- [ ] Sección 3: Referencia de Variables (tabla completa)
- [ ] Sección 4: Sistema de Snippets
- [ ] Sección 5: Guía de Uso
- [ ] Sección 6: Ejemplos por Perfil (links)
- [ ] Sección 7: Personalización

### Documentación Técnica

- [ ] `docs/templates/template-system.md` creado
- [ ] Arquitectura documentada
- [ ] Algoritmos explicados
- [ ] Ejemplos de código

### Actualizaciones

- [ ] README principal actualizado
- [ ] CHANGELOG.md actualizado
- [ ] session-current.md actualizado

### Commit

- [ ] Commit: `docs(templates): completar documentación de sistema de templates (TICKET-037)`

---

## Ejemplos de Documentación

### Ejemplo: Documentar Variable {BACKGROUND_SETUP}

```markdown
### {BACKGROUND_SETUP}

**Tipo:** Snippet
**Descripción:** Steps de setup inicial en escenarios BDD (sección Background)
**Usado en:** `templates/bdd/scenario.feature`

**Valores por Perfil:**

| Perfil | Valor |
|--------|-------|
| pyqt-mvc | `Given la aplicación está iniciada\nAnd la configuración está cargada` |
| fastapi-rest | `Given el servidor API está corriendo\nAnd la base de datos está migrada` |
| flask-rest | `Given el servidor Flask está corriendo\nAnd la base de datos está inicializada` |
| flask-webapp | `Given la aplicación web está corriendo\nAnd el usuario está en la página principal` |
| generic-python | `Given el sistema está inicializado\nAnd las dependencias están cargadas` |

**Ejemplo de Uso:**

```gherkin
Feature: Login de Usuario (US-001)
  Como un usuario
  Quiero iniciar sesión
  Para acceder al sistema

  Background:
{BACKGROUND_SETUP}
```

**Output (pyqt-mvc):**

```gherkin
  Background:
    Given la aplicación está iniciada
    And la configuración está cargada
```
```

---

## Resultado

_A completar al finalizar el ticket._

**Archivos creados/modificados:**
- `templates/README.md` (~1,500 líneas)
- `docs/templates/template-system.md` (~800 líneas)
- `README.md` (actualizado)
- `CHANGELOG.md` (actualizado)
