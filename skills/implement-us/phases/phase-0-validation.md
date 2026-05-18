# Fase 0: Validación de Contexto

**Objetivo:** Verificar que el entorno del proyecto tiene todo lo necesario para implementar la Historia de Usuario, clasificar la HU y generar el archivo de contexto que guiará todas las fases siguientes.

> **📌 Instrucción de ejecución:** Seguir este archivo de arriba a abajo, en el orden en que aparecen los pasos. No saltar ni reordenar.

---

## Paso 1 🔴 — Iniciar tracking

Ejecutá este comando antes de cualquier otra acción en esta fase:

```bash
python .claude/tracking/tracker_cli.py init {US_ID} "{US_TITLE}" {STORY_POINTS} {PRODUCT}
python .claude/tracking/tracker_cli.py start-phase 0 "Validación de Contexto"
```

---

## Paso 2 🔴 — Verificar herramientas requeridas

Verificá que las herramientas del skill están disponibles:

```bash
python -m pylint --version     # Requerido: Fase 7
python -m radon --version      # Requerido: Fase 7
python -m pytest --version     # Requerido: Fases 4, 5, 6, 7
python -c "import pytest_bdd; print(pytest_bdd.__version__)" # Requerido: Fase 6
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

## Paso 3 🔴 — Establecer fuentes

Antes de buscar ningún archivo, preguntá al usuario:

1. **Fuente de la historia de usuario:** ¿Dónde está la HU a implementar?
   - a) Documento local (indicar ruta o patrón, ej. `docs/user-stories/US-001.md`)
   - b) GitHub Issue (indicar número, ej. `#42`)
   - c) Jira (indicar ticket ID, ej. `PROJ-123`)
   - d) Otro sistema (indicar cómo acceder)

2. **Fuente de arquitectura:** ¿Dónde está la definición de arquitectura del proyecto?
   - a) Archivo local (indicar ruta, ej. `docs/architecture.md`)
   - b) Wiki / Confluence / Notion (indicar URL o instrucción de acceso)
   - c) No está documentada (el agente inferirá del código existente)

Registrá las respuestas en `docs/plans/{US_ID}-context.md` como `fuente_hu` y `fuente_arquitectura`.

---

## Paso 4 — Verificar que existe la historia de usuario

Buscá la HU en la fuente indicada en el Paso 3. Si la fuente es un documento local, buscá según el patrón indicado por el usuario o bien en las ubicaciones comunes:

> **📖 Rutas comunes según stack:**
> - **PyQt/MVC:** `{PRODUCT}/docs/HISTORIAS-USUARIO-*.md`
> - **FastAPI:** `docs/user-stories/US-*.md` o `{PRODUCT}/docs/US-*.md`
> - **Flask/Generic:** `docs/US-*.md` o `requirements/US-*.md`

Extraé de la HU:
- Título de la historia
- Criterios de aceptación
- Puntos de estimación
- Prioridad

**Si no se encuentra:** preguntá al usuario por la ubicación antes de continuar.

---

## Paso 5 — Validar arquitectura de referencia

1. Leé el perfil activo del archivo `.claude/skills/implement-us/config.json`, clave `variables.architecture_pattern`. Registrá el valor en `context.md` como `Patrón activo`.

2. Buscá documentación de arquitectura del proyecto en:
   - `docs/architecture*.md`
   - `ARCHITECTURE.md`
   - `README.md` (sección de arquitectura)
   - La ubicación indicada por el usuario en el Paso 3

3. Si no existe ningún archivo de arquitectura:

   > **⚠️ Sin documentación de arquitectura.** El agente inferirá el patrón del código existente. Continuando.

---

## Paso 6 — Verificar estándares de calidad

Verificá que existen:

1. **CLAUDE.md** con quality gates definidos (pylint mínimo, cobertura mínima)
2. **Estructura de tests:** directorio `tests/`, `conftest.py` (si usa pytest)
3. **Herramientas de calidad:** `.pylintrc`, `pytest.ini` o `pyproject.toml`

Si alguno falta, crealo automáticamente con los defaults del perfil activo y notificá al usuario.

**Contenido mínimo de `.pylintrc`** (leé `quality_gates.pylint.min_score` del perfil activo):

```ini
[MASTER]
fail-under={pylint_min}

[FORMAT]
max-line-length=120

[MESSAGES CONTROL]
disable=C0114,C0115,C0116
```

**Contenido mínimo de `pytest.ini`** (leé `test_framework_config.unit_test_path` e `integration_test_path` del perfil activo):

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

> ✅ Creado `.pylintrc` con score mínimo {pylint_min}
> ✅ Creado `pytest.ini` con testpaths = tests

Los archivos pueden modificarse manualmente antes de continuar si se requiere personalización.

---

## Paso 7 🔴 — Clasificar tipo de HU

Analizá la descripción y criterios de aceptación de la HU y determiná su tipo según la siguiente tabla:

| Tipo de HU | ¿BDD aplica? |
|------------|--------------|
| Nueva funcionalidad | ✅ Sí |
| Mejora de comportamiento existente | ✅ Sí |
| Refactorización (sin cambio de comportamiento) | ❌ No |
| Eliminación de code smells | ❌ No |
| Corrección de bug | ⚠️ Depende — informar al usuario |

Presentá la clasificación al usuario con las opciones:

> **Clasificación propuesta:** {tipo de HU}
> **Decisión BDD:** {Sí / No}
>
> Respondé:
> - **[sí]** para confirmar
> - **[no-bdd]** para forzar sin BDD
> - **[otro]** para reclasificar
>
> Cualquier otro mensaje se interpreta como confirmación de la propuesta.

---

## Paso 8 🔴 — Generar archivo de contexto

Creá el archivo `docs/plans/{US_ID}-context.md` con el siguiente contenido (completando todos los campos con los datos reales).

> **📖 Referencia:** Las rutas de artefactos provienen de `.claude/skills/implement-us/artifacts.md`. Si cambian las convenciones de rutas, ese archivo es la fuente de verdad.

```markdown
# Contexto de Ejecución — {US_ID}

## Fuentes
- **Fuente HU:** {fuente_hu}
- **Fuente Arquitectura:** {fuente_arquitectura}

## Historia de Usuario
- **ID:** {US_ID}
- **Título:** {US_TITLE}
- **Tipo:** {HU_TYPE}
- **Puntos:** {US_POINTS}
- **Prioridad:** {US_PRIORITY}

## Decisiones de Ejecución
- **BDD:** {Sí / No — justificación}
- **skip_bdd:** {true / false}
- **Fases a ejecutar:** 0, [1 si BDD], 2, 3, 4, 5, [6 si BDD], 7, 8, 9

## Perfil Activo
- **Perfil:** {PROFILE}
- **Patrón arquitectónico:** {architecture_pattern}
- **Umbrales de calidad:**
  - pylint ≥ {pylint_min}
  - CC ≤ {cc_max}
  - MI ≥ {mi_min}
  - cobertura ≥ {coverage_min}%

## Rutas de Artefactos
- Contexto: docs/plans/{US_ID}-context.md
- BDD feature: tests/features/{US_ID}-{nombre}.feature
- Plan: docs/plans/{US_ID}-plan.md
- Reporte: docs/reports/{US_ID}-report.md
- Quality report: quality/reports/{US_ID}-quality.json
```

Los umbrales se leen del perfil activo en `.claude/skills/implement-us/config.json`.

---

## Paso 9 🔴 — Verificar existencia del archivo de contexto

Después de generarlo, confirmá que el archivo existe en disco:

```bash
ls docs/plans/{US_ID}-context.md
```

Si no existe, generalo nuevamente antes de avanzar a Fase 1.

---

## ✅ Checklist de Salida

Antes de avanzar a Fase 1, confirmá que:
- [ ] Todas las herramientas requeridas están disponibles (pylint, radon, pytest, pytest-bdd)
- [ ] Las fuentes de HU y arquitectura fueron consultadas al usuario (Paso 3)
- [ ] La HU fue encontrada y sus datos extraídos
- [ ] El patrón arquitectónico fue leído del config y registrado en context.md
- [ ] El tipo de HU fue clasificado y confirmado por el usuario
- [ ] La decisión de BDD fue comunicada al usuario
- [ ] `docs/plans/{US_ID}-context.md` existe en disco: `ls docs/plans/{US_ID}-context.md`
- [ ] Los umbrales de calidad provienen del perfil activo (no hardcodeados)

---

## Paso 10 🔴 — Cerrar tracking

```bash
python .claude/tracking/tracker_cli.py end-phase 0
```

---

**Siguiente fase:** [Fase 1: Generación de Escenarios BDD](./phase-1-bdd.md)
