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

### Fase 0: Validación de Contexto

**TRACKING:** Al inicio de la fase:
```python
from .tracking.time_tracker import TimeTracker

# Inicializar tracker
tracker = TimeTracker(us_id, us_title, us_points, producto)
tracker.start_tracking()
tracker.start_phase(0, "Validación de Contexto")
```

#### 1. Verificar que existe la historia de usuario

**Buscar en estructura de documentación del proyecto:**

> **Rutas comunes según stack:**
> - **PyQt/MVC:** `{PRODUCT}/docs/HISTORIAS-USUARIO-*.md`
> - **FastAPI:** `docs/user-stories/US-*.md` o `{PRODUCT}/docs/US-*.md`
> - **Django:** `docs/requirements/US-*.md` o `{app}/docs/US-*.md`
> - **Generic:** `docs/US-*.md` o `requirements/US-*.md`

**Extraer de la US:**
- Título de la historia
- Criterios de aceptación
- Puntos de estimación
- Prioridad

**Si no se encuentra:**
- Preguntar al usuario por la ubicación
- O permitir ingresar manualmente los datos de la US

---

#### 2. Validar arquitectura de referencia

**Buscar documentación arquitectónica:**

Verificar que existe documentación de la arquitectura del proyecto en uno de estos formatos:
- `docs/architecture/ADR-*.md` (Architecture Decision Records)
- `docs/architecture.md`
- `ARCHITECTURE.md`
- `README.md` (sección de arquitectura)

**Verificar patrones arquitectónicos configurados:**

Leer del archivo de configuración `.claude/skills/implement-us/config.json` los patrones a validar:

```json
{
  "architecture_pattern": "{ARCHITECTURE_PATTERN}",
  "required_patterns": ["{PATTERNS}"],
  "architecture_doc": "{ARCHITECTURE_DOC}"
}
```

> **Patrones según perfil:**
> - **PyQt/MVC:** Validar MVC, Factory, Coordinator
> - **FastAPI:** Validar Layered Architecture, Dependency Injection, Repository
> - **Django:** Validar MVT, Class-Based Views, Managers
> - **Generic:** Validar patrones definidos en config o saltar validación

**Checkpoint:**
- ✅ Arquitectura documentada encontrada
- ✅ Patrones requeridos confirmados en el proyecto
- ⚠️ Si falta documentación, advertir al usuario pero continuar

---

#### 3. Verificar estándares de calidad

**Validar que existen:**

1. **CLAUDE.md** con quality gates definidos:
   - Pylint score mínimo
   - Complejidad ciclomática máxima
   - Cobertura de tests mínima

2. **Estructura de tests:**
   - Directorio `tests/` existe
   - `conftest.py` configurado (si usa pytest)
   - Framework de testing instalado (verificar según `{TEST_FRAMEWORK}`)

3. **Herramientas de calidad configuradas:**
   - `.pylintrc` o configuración de pylint
   - `pytest.ini` o `pyproject.toml` (si usa pytest)
   - `.coveragerc` o configuración de coverage

**Si faltan herramientas:**
- Advertir al usuario
- Ofrecer crear configuración básica
- O continuar sin quality gates (no recomendado)

---

**Output Fase 0:** Resumen de contexto validado

```markdown
## ✅ Contexto Validado

**Historia de Usuario:** US-XXX - {título}
**Producto:** {PRODUCT}
**Puntos:** X
**Prioridad:** Alta/Media/Baja

**Arquitectura:**
- Patrón: {ARCHITECTURE_PATTERN}
- Documentación: {ARCHITECTURE_DOC} encontrado
- Patrones verificados: {PATTERNS}

**Quality Gates:**
- ✅ CLAUDE.md configurado
- ✅ Tests configurados ({TEST_FRAMEWORK})
- ✅ Herramientas de calidad disponibles

**Listo para proceder con Fase 1: Generación de Escenarios BDD**
```

---

**TRACKING:** Al finalizar la fase:
```python
tracker.end_phase(0, auto_approved=True)
```

---

> **NOTA:** Las siguientes secciones (Fase 1 a Fase 9) serán agregadas en las próximas subtareas del plan de implementación incremental.
>
> Ver: `gestion/fase-3-generalizacion-skills/tickets/TICKET-021-implementation-plan.md`

---

**Versión:** 2.0.0 (Framework-Agnostic)
**Última actualización:** 2026-02-10
**Basado en:** `_work/from-simapp/skills/implement-us.md` (versión PyQt/MVC)
