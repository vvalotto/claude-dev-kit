# Skill: adapt-project

**Nombre del comando:** `/adapt-project`

**Descripción:** Calibra el skill `implement-us` a la arquitectura real de un proyecto cuando ninguno de los perfiles bundleados en `customizations/` encaja tal cual. Se ejecuta **una sola vez**, después de instalar el Dev Kit y antes de la primera US.

**Cuándo usarlo:** Si al revisar la tabla de perfiles de `implement-us` (`skill.md` → sección "Perfiles Disponibles") ninguno describe la arquitectura real del proyecto — o si ya corriste una US y las rutas/patrones generados no coincidieron con el código real — corré este skill antes de seguir.

---

## 🔴 Acción Requerida — Verificar que no exista ya una adaptación

Antes de generar nada, verificá si el proyecto ya fue adaptado:

```bash
cat .claude/config.json 2>/dev/null | jq -r '.profile'
ls .claude/skills/implement-us/customizations/*-custom.json 2>/dev/null
ls docs/plans/PROJECT-CONTEXT.md 2>/dev/null
```

Si ya existe un perfil `*-custom.json` y/o `docs/plans/PROJECT-CONTEXT.md`:

> ⚠️ **Este proyecto ya tiene una adaptación previa.**
> Perfil actual: `{profile}`
>
> Respondé:
> - **[actualizar]** para re-ejecutar el diagnóstico y sobrescribir la adaptación existente
> - **[cancelar]** para no hacer cambios

No avances sin una respuesta explícita si ya existe una adaptación previa.

---

## Paso 1 🔴 — Diagnóstico del proyecto

Explorá el proyecto **sin preguntarle nada al usuario todavía**. Usá `Glob`/`ls`/`Grep`/`Read` para relevar:

1. **Estructura de directorios real:**
   - ¿La raíz del código es `src/`, `app/`, u otra?
   - ¿Hay carpetas por Bounded Context (`src/{nombre}/...` repetido para varios nombres)?
   - ¿Aparecen nombres de capa reconocibles: `domain/`, `application/`, `infrastructure/`, `api/` (hexagonal DDD) — o `entities/`, `use_cases/`, `interface_adapters/`, `frameworks/` (Clean Architecture) — o una estructura en capas simple (`services/`, `repositories/`, `schemas/`)?

2. **Herramientas de calidad presentes:**
   - `pyproject.toml` / `requirements*.txt`: ¿aparece `codeguard`? ¿`ruff`? ¿`pylint`?
   - `.pylintrc`, `ruff.toml`, `pytest.ini` — umbrales ya configurados.

3. **Documentación existente:**
   - Si existe `CLAUDE.md`, `ARCHITECTURE.md` o `docs/architecture*.md`, leelo — puede ya declarar el patrón arquitectónico y ahorrar preguntas del Paso 2.

4. **Ubicación de las Historias de Usuario:**
   - Buscá en `docs/user-stories/`, `docs/plans/`, `requirements/`, o donde indique la documentación existente.

**Presentá al usuario un resumen de lo detectado** antes de pasar al Paso 2:

```
📋 Diagnóstico del proyecto

Estructura: {resumen} (ej. "src/{bc}/ con 6 BCs, capas domain/application/infrastructure/api")
Patrón arquitectónico inferido: {patrón} (ej. "Hexagonal DDD BC-first")
Herramientas de calidad detectadas: {lista}
Ubicación de US: {path o "no detectada"}

Perfil bundleado más cercano: {perfil} (ver tabla de perfiles en implement-us/skill.md)
```

---

## Paso 2 🔴 — Preguntas guiadas

Preguntá **solo lo que el Paso 1 no pudo inferir con confianza**. No repitas preguntas sobre algo ya detectado — confirmalo brevemente en su lugar ("Detecté X, ¿es correcto?").

Preguntas candidatas (usar solo las necesarias):

1. **Patrón arquitectónico principal**, si el Paso 1 fue ambiguo o no hay bundleado que se le parezca.
2. **Organización de módulos:** ¿por feature/Bounded Context o por capa técnica?
3. **Herramienta de quality gates:** ¿pylint directo, `codeguard` (orquesta pylint+radon+designreviewer), o `ruff`?
4. **Path canónico de las US**, si el Paso 1 no lo encontró.

No avances al Paso 3 sin haber resuelto estos cuatro puntos, ya sea por inferencia confirmada o por respuesta del usuario.

---

## Paso 3 🔴 — Generación de artefactos

### 3.1 Perfil custom

Nombre del perfil: `{project_slug}-custom` (slug del nombre del proyecto/repo, kebab-case).

1. **Elegí el perfil bundleado más cercano** como punto de partida, según lo relevado en el Paso 1 — ver la tabla de perfiles en `.claude/skills/implement-us/skill.md`. Ejemplos de mapeo:
   - Capas `domain/application/infrastructure/api` + BCs → `hexagonal-ddd-bc.json`
   - Capas `entities/use_cases/interface_adapters/frameworks` + BCs → `clean-architecture-bc.json`
   - Arquitectura en capas simple sin BCs → `fastapi-rest.json` / `flask-rest.json` según el framework HTTP
   - Sin patrón claro → `generic-python.json`

2. **Copiá ese perfil** a `.claude/skills/implement-us/customizations/{project_slug}-custom.json`. **Nunca edites el perfil bundleado original** — así una futura actualización del Dev Kit no pisa la adaptación, y el perfil oficial queda disponible como referencia limpia.

3. **Adaptá el contenido copiado** a lo relevado en los Pasos 1-2:
   - `profile_metadata`: `name`, `display_name`, `description` describiendo el proyecto real.
   - `variables.component_path.by_component`: rutas reales (verificadas contra la estructura real, no las del perfil bundleado).
   - `component_structure`: ajustar `base_path`, `files.*.path`, `test_files` a la estructura real.
   - `quality_gates`: reflejar la herramienta real (`codeguard` vs `pylint` directo) y los umbrales reales si existen en `.pylintrc`/`pyproject.toml`.

### 3.2 `.claude/config.json`

Creá o actualizá `.claude/config.json` con la misma forma que genera el instalador (`install/installer.py::merge_configs()`):

```json
{
  "version": "<misma que install/config.json del Dev Kit instalado>",
  "profile": "{project_slug}-custom",
  "profile_name": "<display_name del perfil custom>",
  "adapted_at": "<timestamp ISO>",
  "architecture_pattern": "<variables.architecture_pattern.default del perfil custom>",
  "test_framework": "<variables.test_framework.default del perfil custom>",
  "component_types": ["<variables.component_type.available del perfil custom>"],
  "patterns": [],
  "variables": {}
}
```

Esta es la clave (`profile`) que Fase 0 de `implement-us` lee para determinar el perfil activo — con esto, `/implement-us` queda calibrado sin pasos manuales adicionales.

### 3.3 Doc de contexto de proyecto

Creá `docs/plans/PROJECT-CONTEXT.md`:

```markdown
# Contexto de Proyecto — {NOMBRE_PROYECTO}

Generado por `/adapt-project` el {FECHA}.

## Perfil Activo
- **Perfil:** {project_slug}-custom
- **Basado en:** {perfil bundleado usado como base}

## Arquitectura Real
{resumen del diagnóstico del Paso 1: estructura, capas, BCs}

## Decisiones Registradas en el Paso 2
{cada pregunta respondida, con la respuesta}

## Discrepancias Conocidas con Perfiles Bundleados
{cualquier cosa que el perfil bundleado más cercano NO cubre bien y haya requerido ajuste manual adicional en el perfil custom}
```

---

## Paso 4 🔴 — Validación

1. **Verificá que las rutas generadas existen** en el proyecto real:

```bash
# Por cada path en component_structure.*.files.*.path del perfil custom (con {bc}/{nombre} como placeholders):
ls -d {directorio_base_de_cada_path} 2>&1
```

2. Si algún path base no existe todavía (ej. un Bounded Context nuevo que se creará en la primera US), **no es un error** — advertilo pero continuá:

```
⚠️ {path} no existe todavía en el proyecto — se creará durante la implementación.
```

3. Si algún path esperado según el diagnóstico del Paso 1 no aparece reflejado en el perfil generado, **es una inconsistencia real** — corregí el perfil antes de continuar.

4. **Presentá el resumen final:**

```
✅ Proyecto adaptado

Perfil generado: .claude/skills/implement-us/customizations/{project_slug}-custom.json
Config actualizado: .claude/config.json (profile: {project_slug}-custom)
Contexto de proyecto: docs/plans/PROJECT-CONTEXT.md

Próximo paso: correr /implement-us para tu primera Historia de Usuario.
```

---

## ✅ Checklist de Salida

Antes de dar por terminado el skill, confirmá que:
- [ ] El Paso 1 relevó estructura real, herramientas de calidad y ubicación de US sin asumir nada del contexto de conversación
- [ ] El Paso 2 solo preguntó lo que el Paso 1 no pudo inferir
- [ ] `.claude/skills/implement-us/customizations/{project_slug}-custom.json` existe y **no** es una copia sin adaptar del perfil bundleado
- [ ] `.claude/config.json` tiene `profile: "{project_slug}-custom"`
- [ ] `docs/plans/PROJECT-CONTEXT.md` existe y documenta las decisiones tomadas
- [ ] Las rutas del perfil custom fueron validadas contra la estructura real del proyecto
- [ ] El usuario recibió el resumen final con el próximo paso sugerido

---

## 📖 Referencia — Por qué no se edita un perfil bundleado directamente

Los 7 perfiles en `customizations/` (`pyqt-mvc`, `fastapi-rest`, `flask-rest`, `flask-webapp`, `generic-python`, `hexagonal-ddd-bc`, `clean-architecture-bc`) son la referencia canónica del Dev Kit. Editarlos in-place para adaptarlos a un proyecto específico:

- Se pierde en la próxima actualización del Dev Kit (el instalador puede resincronizar `skills/`).
- Contamina el perfil oficial con paths y decisiones de un solo proyecto, rompiendo su utilidad como plantilla para otros.

Por eso `/adapt-project` siempre copia a un nombre nuevo (`{project_slug}-custom.json`) y apunta `.claude/config.json` ahí.