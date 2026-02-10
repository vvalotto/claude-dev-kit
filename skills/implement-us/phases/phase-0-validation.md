# Fase 0: Validación de Contexto

**Objetivo:** Verificar que el entorno del proyecto tiene todo lo necesario para implementar la Historia de Usuario.

**Duración estimada:** 5-10 minutos

---

## Tracking

**Al inicio de la fase:**
```python
from .tracking.time_tracker import TimeTracker

# Inicializar tracker
tracker = TimeTracker(us_id, us_title, us_points, producto)
tracker.start_tracking()
tracker.start_phase(0, "Validación de Contexto")
```

---

## 1. Verificar que existe la historia de usuario

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

## 2. Validar arquitectura de referencia

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

## 3. Verificar estándares de calidad

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

## Output de la Fase

**Template de resumen:**

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

## Tracking

**Al finalizar la fase:**
```python
tracker.end_phase(0, auto_approved=True)
```

---

**Siguiente fase:** [Fase 1: Generación de Escenarios BDD](./phase-1-bdd.md)
