# Fase 0: Validación de Contexto

**Objetivo:** Verificar que el entorno del proyecto tiene todo lo necesario para implementar la Historia de Usuario, clasificar la HU y generar el archivo de contexto que guiará todas las fases siguientes.

---

## 🔴 Acción Requerida — Iniciar tracking

Ejecutá este comando antes de cualquier otra acción en esta fase:

```bash
python .claude/tracking/time_tracker.py start --us {US_ID} --phase 0
```

---

## 🔴 Acción Requerida — Verificar herramientas requeridas

Antes de comenzar la implementación, verificá que las herramientas del skill están disponibles:

```bash
python -m pylint --version     # Requerido: Fase 7
python -m radon --version      # Requerido: Fase 7
python -m pytest --version     # Requerido: Fases 4, 5, 6, 7
python -m pytest_bdd --version # Requerido: Fase 6
```

Si algún comando falla, **no avances**. Informá al usuario:

> **🚫 STOP — Herramienta `{nombre}` no disponible.**
> Instalala con `pip install {paquete}` antes de continuar.
> No se puede garantizar la ejecución completa del skill sin esta herramienta.

| Herramienta | Paquete | Fases que la requieren |
|-------------|---------|------------------------|
| pylint | `pylint` | Fase 7 |
| radon | `radon` | Fase 7 |
| pytest | `pytest` | Fases 4, 5, 6, 7 |
| pytest-bdd | `pytest-bdd` | Fase 6 |

---

## 1. Verificar que existe la historia de usuario

Buscá el archivo de la HU en la estructura de documentación del proyecto:

> **📖 Referencia — Rutas comunes según stack:**
> - **PyQt/MVC:** `{PRODUCT}/docs/HISTORIAS-USUARIO-*.md`
> - **FastAPI:** `docs/user-stories/US-*.md` o `{PRODUCT}/docs/US-*.md`
> - **Flask/Generic:** `docs/US-*.md` o `requirements/US-*.md`

Extraé de la US:
- Título de la historia
- Criterios de aceptación
- Puntos de estimación
- Prioridad

**Si no se encuentra:** preguntá al usuario por la ubicación antes de continuar.

---

## 2. Validar arquitectura de referencia

Verificá que existe documentación de la arquitectura del proyecto:
- `docs/architecture/ADR-*.md`
- `docs/architecture.md`
- `ARCHITECTURE.md`
- `README.md` (sección de arquitectura)

Leé del archivo de configuración `.claude/skills/implement-us/config.json` los patrones a validar.

> **📖 Referencia — Patrones según perfil:**
> - **PyQt/MVC:** MVC, Factory, Coordinator
> - **FastAPI:** Layered Architecture, Dependency Injection, Repository
> - **Flask REST/Webapp:** Blueprints, Service Layer, Repository
> - **Generic:** Patrones definidos en config o saltar validación

Si falta documentación de arquitectura, advertí al usuario pero continuá.

---

## 3. Verificar estándares de calidad

Verificá que existen:

1. **CLAUDE.md** con quality gates definidos (pylint mínimo, cobertura mínima)
2. **Estructura de tests:** directorio `tests/`, `conftest.py` (si usa pytest)
3. **Herramientas de calidad:** `.pylintrc`, `pytest.ini` o `pyproject.toml`

Si faltan configuraciones, ofrecé crearlas o advertí al usuario antes de continuar.

---

## 🔴 Acción Requerida — Clasificar tipo de HU

Analizá la descripción y criterios de aceptación de la HU y determiná su tipo según la siguiente tabla:

| Tipo de HU | ¿BDD aplica? |
|------------|--------------|
| Nueva funcionalidad | ✅ Sí |
| Mejora de comportamiento existente | ✅ Sí |
| Refactorización (sin cambio de comportamiento) | ❌ No |
| Eliminación de code smells | ❌ No |
| Corrección de bug | ⚠️ Depende — informar al usuario |

Informá la clasificación al usuario y esperá confirmación antes de continuar. El usuario puede hacer override de la decisión de BDD.

---

## 🔴 Acción Requerida — Generar archivo de contexto

Creá el archivo `docs/plans/{US_ID}-context.md` con el siguiente contenido (completando todos los campos con los datos reales):

```markdown
# Contexto de Ejecución — {US_ID}

## Historia de Usuario
- **ID:** {US_ID}
- **Título:** {US_TITLE}
- **Tipo:** {HU_TYPE}
- **Puntos:** {US_POINTS}
- **Prioridad:** {US_PRIORITY}

## Decisiones de Ejecución
- **BDD:** {Sí / No — justificación}
- **Fases a ejecutar:** 0, [1 si BDD], 2, 3, 4, 5, [6 si BDD], 7, 8, 9

## Perfil Activo
- **Perfil:** {PROFILE}
- **Umbrales de calidad:**
  - pylint ≥ {pylint_min}
  - CC ≤ {cc_max}
  - MI ≥ {mi_min}
  - cobertura ≥ {coverage_min}%

## Rutas de Artefactos
- Contexto: docs/plans/{US_ID}-context.md
- BDD feature: docs/bdd/{US_ID}.feature
- Plan: docs/plans/{US_ID}-plan.md
- Reporte: docs/reports/{US_ID}-report.md
- Quality report: quality/reports/{US_ID}-quality.json
```

Los umbrales se leen del perfil activo en `.claude/skills/implement-us/config.json`.

## 🔴 Acción Requerida — Verificar existencia del archivo de contexto

Después de generarlo, confirmá que el archivo existe en disco:

```bash
ls docs/plans/{US_ID}-context.md
```

Si no existe, generalo nuevamente antes de avanzar a Fase 1.

---

## ✅ Checklist de Salida

Antes de avanzar a Fase 1, confirmá que:
- [ ] Todas las herramientas requeridas están disponibles (pylint, radon, pytest, pytest-bdd)
- [ ] La HU fue encontrada y sus datos extraídos
- [ ] La arquitectura del proyecto fue validada
- [ ] El tipo de HU fue clasificado y confirmado por el usuario
- [ ] La decisión de BDD fue comunicada al usuario
- [ ] `docs/plans/{US_ID}-context.md` existe en disco: `ls docs/plans/{US_ID}-context.md`
- [ ] Los umbrales de calidad provienen del perfil activo (no hardcodeados)

## 🔴 Acción Requerida — Cerrar tracking

```bash
python .claude/tracking/time_tracker.py end --us {US_ID} --phase 0
```

---

**Siguiente fase:** [Fase 1: Generación de Escenarios BDD](./phase-1-bdd.md)
