# Skill: implement-us

**Nombre del comando:** `/implement-us`

**Descripción:** Implementador asistido de Historias de Usuario siguiendo el patrón arquitectónico configurado para el proyecto.

---

## Variables Disponibles

Este skill utiliza las siguientes variables definidas en `config.json` y personalizables mediante perfiles en `customizations/`:

| Variable | Descripción | Valor Default | Ejemplos por Perfil |
|----------|-------------|---------------|---------------------|
| `{ARCHITECTURE_PATTERN}` | Patrón arquitectónico del proyecto | `generic` | **PyQt:** `mvc`<br>**FastAPI:** `layered`<br>**Django:** `mvt`<br>**Generic:** `generic` |
| `{COMPONENT_TYPE}` | Tipo de componente a implementar | `Component` | **PyQt:** `Panel`, `Dialog`<br>**FastAPI:** `Endpoint`, `Service`<br>**Django:** `View`, `Model`<br>**Generic:** `Module` |
| `{COMPONENT_PATH}` | Ruta base para componentes | `src/{name}/` | **PyQt:** `app/presentacion/{name}/`<br>**FastAPI:** `app/{layer}/{name}/`<br>**Django:** `{app}/{name}/`<br>**Generic:** `src/{name}/` |
| `{TEST_FRAMEWORK}` | Framework de testing | `pytest` | **PyQt:** `pytest + pytest-qt`<br>**FastAPI:** `pytest + httpx`<br>**Django:** `pytest-django`<br>**Generic:** `pytest` |
| `{BASE_CLASS}` | Clase base para componentes | `object` | **PyQt:** `QWidget`, `ModeloBase`<br>**FastAPI:** `BaseModel`, `BaseService`<br>**Django:** `Model`, `View`<br>**Generic:** `object` |
| `{DOMAIN_CONTEXT}` | Contexto de dominio del proyecto | `application` | **PyQt:** `presentacion`, `dominio`<br>**FastAPI:** `api`, `domain`<br>**Django:** `apps`, `models`<br>**Generic:** `domain` |
| `{PROJECT_ROOT}` | Raíz del proyecto | `.` | **PyQt:** `app/`<br>**FastAPI:** `src/`<br>**Django:** `project/`<br>**Generic:** `.` |
| `{PRODUCT}` | Nombre del producto/módulo | `main` | Cualquier nombre de producto/módulo |

### Cómo se Resuelven las Variables

Las variables se resuelven en el siguiente orden de prioridad:

1. **Perfil de customización** (`.claude/skills/implement-us/customizations/{perfil}.json`)
2. **Configuración base** (`.claude/skills/implement-us/config.json`)
3. **Valores por defecto** (tabla anterior)

**Ejemplo de configuración:**

```json
{
  "architecture_pattern": "mvc",
  "component_type": "Panel",
  "component_path": "app/presentacion/paneles/{name}/",
  "test_framework": "pytest-qt",
  "base_class": "ModeloBase",
  "domain_context": "presentacion",
  "project_root": "app/"
}
```

---

## Propósito

Este skill guía paso a paso la implementación de una Historia de Usuario (US) en cualquier proyecto Python, asegurando:

- Adherencia a la arquitectura configurada para el proyecto
- Generación de escenarios BDD
- Implementación completa según el patrón arquitectónico
- Tests unitarios y de integración
- Validación de quality gates
- Documentación y reporte final

El skill es **framework-agnostic** y se adapta automáticamente según el perfil instalado:
- **PyQt/MVC:** Implementación de componentes UI con arquitectura MVC
- **FastAPI:** Implementación de endpoints REST con arquitectura en capas
- **Django:** Implementación MVT siguiendo convenciones Django
- **Generic Python:** Implementación de módulos Python genéricos

---

## Uso

```bash
/implement-us US-001
/implement-us US-001 --producto {PRODUCT}
/implement-us US-001 --skip-bdd  # Salta generación BDD
```

**Parámetros:**
- `US-XXX`: Identificador de la Historia de Usuario (requerido)
- `--producto`: Nombre del producto/módulo (opcional, default: valor de `{PRODUCT}`)
- `--skip-bdd`: Saltar generación de escenarios BDD (opcional)

---

## Validación de Concepto de Variables

### Ejemplo: Instrucciones Generalizadas vs Específicas

#### ❌ ANTES (Específico - PyQt/MVC):

```markdown
### Fase 3: Implementación

#### 1. Panel Display (MVC)
- [ ] app/presentacion/paneles/display/modelo.py (10 min)
- [ ] app/presentacion/paneles/display/vista.py (20 min)
- [ ] app/presentacion/paneles/display/controlador.py (15 min)

El modelo debe heredar de `ModeloBase` y usar el patrón Factory.
```

#### ✅ DESPUÉS (Genérico - Framework Agnostic):

```markdown
### Fase 3: Implementación

#### 1. {COMPONENT_NAME} ({ARCHITECTURE_PATTERN})

**Estructura según patrón:**

> **MVC (PyQt):**
> - [ ] {COMPONENT_PATH}/modelo.py (10 min)
> - [ ] {COMPONENT_PATH}/vista.py (20 min)
> - [ ] {COMPONENT_PATH}/controlador.py (15 min)
> - El modelo debe heredar de `{BASE_CLASS}`

> **MVT (Django):**
> - [ ] {COMPONENT_PATH}/models.py (15 min)
> - [ ] {COMPONENT_PATH}/views.py (20 min)
> - [ ] {COMPONENT_PATH}/templates/{name}.html (10 min)
> - El modelo debe heredar de `models.Model`

> **Layered (FastAPI):**
> - [ ] {COMPONENT_PATH}/schemas.py (10 min)
> - [ ] {COMPONENT_PATH}/service.py (20 min)
> - [ ] {COMPONENT_PATH}/router.py (15 min)
> - El schema debe heredar de `{BASE_CLASS}`

> **Generic:**
> - [ ] {COMPONENT_PATH}/implementation.py (30 min)
> - Seguir convenciones del proyecto
```

### Beneficios de la Generalización

✅ **Un solo skill funciona para múltiples stacks**
✅ **Configuración centralizada** en archivos JSON
✅ **Personalización fácil** mediante perfiles
✅ **Mantenimiento simplificado** (un cambio afecta todos los perfiles)
✅ **Extensible** (agregar nuevos perfiles sin modificar el skill)

---

## Proceso del Skill

> **NOTA:** Las secciones siguientes (Fase 0 a Fase 9) serán agregadas en las próximas subtareas del plan de implementación incremental.
>
> Ver: `gestion/fase-3-generalizacion-skills/tickets/TICKET-021-implementation-plan.md`

---

**Versión:** 2.0.0 (Framework-Agnostic)
**Última actualización:** 2026-02-10
**Basado en:** `_work/from-simapp/skills/implement-us.md` (versión PyQt/MVC)
