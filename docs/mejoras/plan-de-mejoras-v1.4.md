# Plan de Mejoras — Claude Dev Kit v1.4

**Fecha:** 2026-05-18
**Basado en:** Issues #38–#45 (GitHub) + uso real del skill en proyecto AtaraxiaDive (DDD hexagonal)
**Estado:** Pendiente
**Tickets:** TICKET-090 a TICKET-099 (10 tickets)

---

## Contexto

Este plan consolida los problemas detectados durante el uso real del framework en el
proyecto **AtaraxiaDive** (FastAPI + DDD BC-first + Event Sourcing), que representa el
primer proyecto de producción que usó el Dev Kit en modo hexagonal con IDs de US con
prefijos distintos a `US-*`.

Las issues identificadas cubren tres áreas independientes:

| Área | Issues | Descripción |
|------|--------|-------------|
| **Installer** | #38, #39, #40 | Dependencia de `pyyaml`, crash con stdin no-TTY, falta doc para `uv` |
| **Tracking** | #42, #45 | CLI no funciona desde Bash, glob hardcodeado `US-*` |
| **Pipeline del skill** | #43, #44 | LLM omite Fases 8-9, falta gate de verificación de artefactos |

El issue #41 (skill `/adapt-project`) es una feature de mayor alcance y se planifica
como candidata a v1.5.

---

## Resumen de Tickets

| Ticket | Título | Área | Complejidad | Issues | Depende de |
|--------|--------|------|-------------|--------|------------|
| TICKET-090 | Migrar config.yaml a config.json (eliminar pyyaml) | Installer | M | #38 | — |
| TICKET-091 | Manejar stdin no-TTY en installer | Installer | S | #39 | — |
| TICKET-092 | Documentar instalación con uv / venv sin pip | Installer | S | #40 | TICKET-090 |
| TICKET-093 | Agregar classmethod load() a TimeTracker | Tracking | M | #42 | — |
| TICKET-094 | Crear tracker_cli.py — CLI wrapper Bash para TimeTracker | Tracking | M | #42 | TICKET-093 |
| TICKET-095 | Corregir glob US-* en _find_active_us_id() | Tracking | S | #45 | TICKET-094 |
| TICKET-096 | Agregar validación de trackers activos múltiples | Tracking | S | #45 | TICKET-095 |
| TICKET-097 | Gate de cierre ejecutable en Fase 7 | Pipeline | S | #43, #44 | — |
| TICKET-098 | Gate de cierre ejecutable en Fase 9 | Pipeline | S | #43, #44 | TICKET-097 |
| TICKET-099 | Actualizar phase files: tracking en Bash con tracker_cli.py | Pipeline | M | #42 | TICKET-094 |

**Complejidad:** S = pequeño (1-2 archivos, cambio localizado) · M = medio (3-5 archivos o diseño no trivial)

---

## Diagrama de Dependencias

```
TICKET-090 (yaml→json) ──────────────► TICKET-092 (docs uv)
TICKET-091 (stdin TTY)  ──── independiente

TICKET-093 (load())  ──► TICKET-094 (tracker_cli) ──► TICKET-095 (glob fix)
                                                    └──► TICKET-096 (multi-tracker)
                                                    └──► TICKET-099 (phase files Bash)

TICKET-097 (gate Fase 7) ──► TICKET-098 (gate Fase 9)
```

**Ejecución paralela posible:** Bloque installer (090–092) en paralelo con bloque tracking (093–099),
y bloque pipeline (097–098) en paralelo con ambos.

**Ejecución secuencial obligatoria:**
- 090 antes de 092
- 093 → 094 → 095, 096, 099
- 097 → 098

---

## Fase 1 — Installer: zero-dependency y robustez

### TICKET-090 — Migrar config.yaml a config.json (eliminar pyyaml)

**Issue:** #38
**Archivos:** `install/installer.py`, `install/config.yaml` → `install/config.json`

**Problema:** El instalador requiere `pyyaml` para leer su configuración. En entornos
con `uv` u otros gestores donde el venv no expone `pip`, la instalación falla antes de
comenzar.

**Cambios:**

1. Convertir `install/config.yaml` a `install/config.json` (contenido equivalente)
2. En `installer.py`, reemplazar:
   ```python
   import yaml
   config = yaml.safe_load(f)
   ```
   por:
   ```python
   import json
   config = json.load(f)
   ```
3. Eliminar cualquier referencia a `pyyaml` en la documentación del instalador

**Criterio de cierre:** `installer.py` corre con Python stdlib puro. Sin `import yaml`.
`config.yaml` eliminado, `config.json` presente con contenido equivalente.

---

### TICKET-091 — Manejar stdin no-TTY en installer

**Issue:** #39
**Archivos:** `install/installer.py`

**Problema:** Cuando `.claude/` ya existe, el instalador llama a `input()` para pedir
confirmación. Si stdin no es un TTY (Claude Code, scripts, CI), se lanza `EOFError` y
la instalación falla con un mensaje opaco.

**Cambios:**

Capturar `EOFError` en todas las llamadas a `input()` y aplicar default conservador:

```python
try:
    respuesta = input("¿Sobrescribir instalación existente? [s/N]: ").strip().lower()
except EOFError:
    respuesta = "n"
    print("(stdin no interactivo — usando default: N. Usar --force para sobrescribir.)")
```

Aplicar el mismo patrón a cualquier otra llamada a `input()` en el instalador.

**Criterio de cierre:** El instalador no lanza `EOFError` en ningún contexto. Cuando
stdin no es TTY y no se usó `--force`, imprime el motivo y termina con código de
salida `0` (no es un error).

---

### TICKET-092 — Documentar instalación con uv / venv sin pip

**Issue:** #40
**Archivos:** `install/README.md`, `README.md` (sección Quick Start)
**Depende de:** TICKET-090

**Problema:** La documentación asume que `python` expone `pip`. En proyectos con `uv`
o virtualenvs sin pip expuesto, el comando estándar falla sin instrucción de
troubleshooting.

**Cambios en `install/README.md`:**

Agregar sección "Entornos sin pip (uv, venv)":

```markdown
## Entornos sin pip (uv, venv)

Si tu proyecto usa `uv` u otro gestor donde el virtualenv no expone `pip`,
usá el Python del sistema directamente:

```bash
# macOS / Linux — Python del sistema
python3 ~/.claude-dev-kit/install/installer.py --profile fastapi-rest --yes

# macOS con Python.framework
/Library/Frameworks/Python.framework/Versions/3.12/bin/python3 \
  ~/.claude-dev-kit/install/installer.py --profile fastapi-rest --yes
```

Para re-instalar sobre una instalación existente, usá `--force`:

```bash
python3 ~/.claude-dev-kit/install/installer.py --profile fastapi-rest --yes --force
```
```

**Criterio de cierre:** Sección de troubleshooting presente en `install/README.md`
con ejemplos para uv y `--force` documentado en Quick Start.

---

## Fase 2 — Tracking: CLI usable desde Bash y robustez de lookup

### TICKET-093 — Agregar classmethod load() a TimeTracker

**Issue:** #42
**Archivos:** `tracking/time_tracker.py`

**Problema:** `TimeTracker` fue diseñado para vivir en sesión Python continua. En
Claude Code cada fase corre en llamadas Bash separadas — el objeto in-memory muere
entre llamadas. `commands.py` tiene `_load_tracker_from_file()` pero no restaura
`phases`, `pauses`, ni `started_at`.

**Cambios:**

Agregar `classmethod load(cls, us_id: str) -> "TimeTracker"` que reconstruya estado
completo desde el JSON de persistencia:

```python
@classmethod
def load(cls, us_id: str) -> "TimeTracker":
    storage_path = Path(f".claude/tracking/{us_id}-tracking.json")
    if not storage_path.exists():
        raise FileNotFoundError(f"No existe tracking para {us_id}: {storage_path}")
    data = json.loads(storage_path.read_text())
    tracker = cls(
        us_id=data["us_id"],
        us_title=data["us_title"],
        story_points=data["story_points"],
        product=data["product"],
    )
    tracker.started_at = _parse_dt(data["timeline"]["started_at"])
    tracker.completed_at = _parse_dt(data["timeline"]["completed_at"])
    # reconstruir phases, tasks, pauses, current_phase, current_task, current_pause
    ...
    return tracker
```

Manejar compatibilidad con formato simplificado (tasks como strings) y formato
completo (tasks como dicts).

**Criterio de cierre:** `TimeTracker.load("US-1.0.0")` reconstruye estado completo
desde JSON. Tests unitarios verifican reconstrucción de phases, pauses y tasks.

---

### TICKET-094 — Crear tracker_cli.py — CLI wrapper Bash para TimeTracker

**Issue:** #42
**Archivos:** `tracking/tracker_cli.py` (nuevo)
**Depende de:** TICKET-093

**Problema:** Los phase files usan pseudocódigo Python que Claude Code no puede
ejecutar como Bash. No existe un wrapper CLI que permita usar `TimeTracker` desde
la terminal entre fases.

**Cambios:**

Crear `tracking/tracker_cli.py` con los siguientes subcomandos:

| Subcomando | Acción |
|------------|--------|
| `init <us_id> <title> <points> <product>` | Inicializa tracker, crea JSON |
| `start-phase <n> <nombre>` | Abre fase N en el tracker activo |
| `end-phase <n>` | Cierra fase N |
| `start-task <id> <nombre> <area> <min>` | Abre tarea dentro de la fase activa |
| `end-task <id> <ruta>` | Cierra tarea con archivo principal |
| `end [us_id]` | Cierra el tracker completo |
| `status` | Muestra estado actual (fase activa, tiempo transcurrido) |

Cada subcomando carga el tracker con `TimeTracker.load()`, aplica la operación y
persiste. El CLI toma el `us_id` de `_find_active_us_id()` cuando no se pasa explícito.

Uso desde phase files:

```bash
uv run python .claude/tracking/tracker_cli.py start-phase 0 "Validación de Contexto"
```

**Criterio de cierre:** Los 7 subcomandos funcionan desde Bash. `tracker_cli.py`
incluye `--help`. Tests de integración verifican el ciclo completo init→phase→end.

---

### TICKET-095 — Corregir glob US-* en _find_active_us_id()

**Issue:** #45
**Archivos:** `tracking/tracker_cli.py`
**Depende de:** TICKET-094

**Problema:** `_find_active_us_id()` usa `glob(".claude/tracking/US-*-tracking.json")`.
IDs con prefijo distinto (`INC-*`, `TEC-*`) crean el archivo correctamente pero no son
encontrados por las operaciones posteriores — fallo silencioso.

**Cambio (1 línea):**

```python
# Antes
files = glob(".claude/tracking/US-*-tracking.json")

# Después
files = glob(".claude/tracking/*-tracking.json")
```

**Criterio de cierre:** `tracker_cli.py start-phase 0 "nombre"` encuentra correctamente
un tracker con ID `INC-2.0`, `TEC-1.0` u cualquier otro prefijo.

---

### TICKET-096 — Agregar validación de trackers activos múltiples

**Issue:** #45 (efecto secundario)
**Archivos:** `tracking/tracker_cli.py`
**Depende de:** TICKET-095

**Problema:** Si hay más de un tracker con `completed_at == null`, `_find_active_us_id()`
devuelve el primero en orden de glob — comportamiento silencioso y no determinista.

**Cambios:**

```python
def _find_active_us_id() -> str:
    files = glob(".claude/tracking/*-tracking.json")
    activos = []
    for f in files:
        data = json.loads(Path(f).read_text())
        if data["timeline"]["completed_at"] is None:
            activos.append(data["us_id"])
    if len(activos) == 0:
        raise RuntimeError("No hay trackers activos. Ejecutar primero: tracker_cli.py init")
    if len(activos) > 1:
        raise RuntimeError(
            f"Múltiples trackers activos: {activos}. "
            "Cerrar los huérfanos antes de continuar: tracker_cli.py end <us_id>"
        )
    return activos[0]
```

**Criterio de cierre:** Error explícito y accionable cuando hay 0 o 2+ trackers activos.
Sin comportamiento silencioso.

---

## Fase 3 — Pipeline: gates ejecutables para Fases 7 y 9

### TICKET-097 — Gate de cierre ejecutable en Fase 7

**Issues:** #43, #44
**Archivos:** `skills/implement-us/phases/phase-7-quality-gates.md`

**Problema:** El LLM omite sistemáticamente las Fases 8 y 9 al terminar la Fase 7.
La causa: el criterio de completitud implícito del LLM es "tests verdes + quality gates
aprobados = listo para mergear". El gate de texto actual es ignorable.

**Cambios:**

Agregar al final de `phase-7-quality-gates.md`, como **último paso obligatorio antes
de continuar**, un bloque Bash ejecutable:

```bash
## 🔒 Gate de salida — ejecutar antes de continuar

US_ID="..."  # completar con el ID de la US activa
REPORT_Q="quality/reports/${US_ID}-quality.json"

if [ ! -f "$REPORT_Q" ]; then
  echo "❌ BLOQUEADO: $REPORT_Q no existe en disco."
  echo "Persistir el reporte de quality gates antes de avanzar."
  exit 1
fi

echo "✅ Fase 7 completa. Artefacto verificado: $REPORT_Q"
echo ""
echo "⏭️  SIGUIENTE OBLIGATORIO: Fase 8 — Documentación"
echo "   NO hacer commit. NO abrir PR. Ejecutar Fase 8 ahora."
```

El output del comando es observable — el LLM lo ve como resultado de herramienta,
no como texto ignorable.

**Criterio de cierre:** El bloque Bash está presente y es el último paso de la fase.
La instrucción "SIGUIENTE OBLIGATORIO" está en output de herramienta, no en texto
descriptivo.

---

### TICKET-098 — Gate de cierre ejecutable en Fase 9

**Issues:** #43, #44
**Archivos:** `skills/implement-us/phases/phase-9-final-report.md`
**Depende de:** TICKET-097

**Problema:** El gate de cierre actual en Fase 9 es texto:
> "Mostrar en el chat ≠ persistir en disco."

El LLM puede "completar conceptualmente" la fase y continuar sin haber escrito el
archivo — degradación silenciosa documentada en múltiples sesiones.

**Cambios:**

Agregar al final de `phase-9-final-report.md` un gate Bash equivalente al de Fase 7:

```bash
## 🔒 Gate de cierre — ejecutar antes de cerrar el tracking

US_ID="..."  # completar con el ID de la US activa
REPORT="docs/reports/${US_ID}-report.md"

if [ ! -f "$REPORT" ]; then
  echo "❌ BLOQUEADO: $REPORT no existe en disco."
  echo "El skill implement-us NO está completo hasta que este archivo exista."
  echo "Generar el reporte siguiendo el template antes de continuar."
  exit 1
fi

echo "✅ Gate de cierre superado — $REPORT existe en disco."
echo "Proceder a: tracker_cli.py end ${US_ID} → commit → PR"
```

Agregar también al **inicio** de la fase, como precondición explícita verificada:

```bash
## ✅ Precondición — verificar Fase 8 completa

PLAN="docs/plans/${US_ID}-plan.md"
if [ ! -f "$PLAN" ]; then
  echo "⚠️  $PLAN no encontrado. Verificar que Fase 8 se ejecutó correctamente."
fi
```

**Criterio de cierre:** Gate ejecutable presente al final. Precondición de Fase 8
verificada al inicio. El archivo de reporte debe existir en disco antes de que el
gate pase.

---

### TICKET-099 — Actualizar phase files: tracking en Bash con tracker_cli.py

**Issue:** #42
**Archivos:** `phase-0-validation.md` … `phase-9-final-report.md` (10 archivos)
**Depende de:** TICKET-094

**Problema:** Todos los phase files definen el tracking como pseudocódigo Python
no ejecutable. Claude Code no puede correr estos bloques como herramienta Bash.
El resultado documentado: el tracking se reconstruye post-facto o se omite.

**Cambios:**

En cada `phase-N-*.md`, reemplazar los bloques de tracking Python por comandos
Bash usando `tracker_cli.py`. Patrón para cada fase:

```bash
# 🔴 Inicio de Fase N — ejecutar ANTES de cualquier acción
uv run python .claude/tracking/tracker_cli.py start-phase N "{NOMBRE_FASE}"
```

```bash
# 🔴 Cierre de Fase N — ejecutar DESPUÉS del gate de salida
uv run python .claude/tracking/tracker_cli.py end-phase N
```

Para Fase 0 (init), agregar también:

```bash
# 🔴 Inicializar tracker al comenzar la US
uv run python .claude/tracking/tracker_cli.py init {US_ID} "{US_TITLE}" {STORY_POINTS} {PRODUCT}
```

Para Fase 9 (cierre):

```bash
# 🔴 Cerrar tracker al finalizar la US (después del gate de Fase 9)
uv run python .claude/tracking/tracker_cli.py end {US_ID}
```

Los bloques de tracking deben estar en secciones `🔴 Acción Requerida` para mantener
la convención imperativa establecida en v1.1.

**Criterio de cierre:** Los 10 phase files usan exclusivamente comandos Bash para
tracking. Sin pseudocódigo Python. Verificar en una ejecución real que `start-phase`
y `end-phase` se persisten correctamente entre fases consecutivas.

---

## Versión Objetivo: v1.4

### Criterio de Completitud

El plan está completo cuando:

- [ ] TICKET-090: `install/config.json` presente, `config.yaml` eliminado, sin `import yaml`
- [ ] TICKET-091: installer no lanza `EOFError` en contextos no-interactivos
- [ ] TICKET-092: `install/README.md` documenta instalación con `uv` y flag `--force`
- [ ] TICKET-093: `TimeTracker.load()` reconstruye estado completo desde JSON
- [ ] TICKET-094: `tracker_cli.py` operativo con los 7 subcomandos
- [ ] TICKET-095: `_find_active_us_id()` encuentra IDs con cualquier prefijo
- [ ] TICKET-096: error explícito ante 0 o 2+ trackers activos
- [ ] TICKET-097: gate Bash ejecutable al final de `phase-7-quality-gates.md`
- [ ] TICKET-098: gate Bash ejecutable al final de `phase-9-final-report.md`
- [ ] TICKET-099: los 10 phase files usan `tracker_cli.py` en Bash
- [ ] Tests del framework pasan al 100% (suite existente + nuevos tests de tracking)
- [ ] CHANGELOG.md actualizado con los cambios de v1.4

### Estrategia de Commits y PRs

Tres PRs independientes — uno por área, ejecutables en paralelo:

```
PR A — feature/installer-v1.4
  fix(installer): migrar config.yaml a config.json — eliminar dependencia pyyaml (TICKET-090)
  fix(installer): manejar stdin no-TTY sin EOFError (TICKET-091)
  docs(installer): documentar instalación con uv y flag --force (TICKET-092)

PR B — feature/tracking-v1.4
  feat(tracking): agregar classmethod load() con reconstrucción completa de estado (TICKET-093)
  feat(tracking): crear tracker_cli.py — CLI wrapper Bash para TimeTracker (TICKET-094)
  fix(tracking): corregir glob US-* para soportar cualquier prefijo de US_ID (TICKET-095)
  fix(tracking): agregar validación explícita de trackers activos múltiples (TICKET-096)

PR C — feature/pipeline-v1.4
  feat(fase-7): agregar gate de cierre ejecutable antes de continuar (TICKET-097)
  feat(fase-9): agregar gate de cierre ejecutable y precondición de Fase 8 (TICKET-098)
  refactor(phases): reemplazar pseudocódigo tracking por comandos Bash tracker_cli (TICKET-099)
```

Merge a `main` → release v1.4 con tag `v1.4.0`.

---

## Backlog post v1.4

| Issue | Descripción | Candidato |
|-------|-------------|-----------|
| #41 | Skill `/adapt-project` — calibración automática del skill al proyecto | v1.5 |
| — | Perfil `hexagonal-ddd-bc` con paths y patrones propios para el tracker CLI | v1.5 |

---

**Generado:** 2026-05-18
**Versión objetivo:** v1.4
**Fuente:** Issues #38–#45 (GitHub) + uso real en proyecto AtaraxiaDive
