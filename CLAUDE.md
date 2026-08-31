# CLAUDE.md

Este archivo proporciona orientación a Claude Code al trabajar en este repositorio.

---

## Visión General del Proyecto

**Claude Dev Kit** es un framework de desarrollo agnóstico de dominio que automatiza la implementación de historias de usuario con Claude Code. Proporciona skills reutilizables, templates y un sistema de tracking de tiempo.

**Estado Actual:** v1.6.0 — Estable y completo. El framework está publicado y en uso.

---

## Estructura del Repositorio

```
claude-dev-kitc/
├── skills/implement-us/       # Skill principal (orquestador + 10 fases + 7 perfiles)
│   ├── skill.md               # Orquestador — leer primero al trabajar con el skill
│   ├── artifacts.md           # Mapa centralizado de artefactos y rutas canónicas
│   ├── conventions.md         # Convención estructural de archivos de fase
│   ├── config.json            # Configuración base genérica
│   ├── phases/                # phase-0-validation.md … phase-9-final-report.md
│   └── customizations/        # pyqt-mvc.json, fastapi-rest.json, flask-rest.json,
│                              #   flask-webapp.json, generic-python.json, hexagonal-ddd-bc.json,
│                              #   clean-architecture-bc.json
├── skills/adapt-project/      # Skill de calibración inicial (una vez por proyecto)
│   └── skill.md                #   Diagnóstico + preguntas guiadas + genera perfil custom
├── templates/                 # Templates parametrizados con {VARIABLE} y {SNIPPET:id}
│   ├── bdd/scenario.feature
│   ├── planning/implementation-plan.md
│   ├── testing/test-unit.py.tpl
│   └── reporting/implementation-report.md
├── tracking/                  # Sistema de tracking de tiempo (Python, dataclasses)
│   ├── time_tracker.py        # Core: TimeTracker, Task, Phase, Pause
│   ├── tracker_cli.py         # CLI bash-callable (init, start/end-phase, start/end-task, status, end)
│   ├── commands.py            # Comandos /track-*
│   └── reports.py             # Generación de reportes
├── install/                   # Instalador multiplataforma
├── docs/                      # Documentación completa
│   ├── skills/implement-us/   # Documentación unificada del skill (índice + phase-0…9)
│   ├── user/                  # Guías de usuario (getting-started, installation, etc.)
│   ├── developer/             # Docs técnicas (architecture, contributing)
│   ├── examples/              # Tutoriales por stack
│   └── mejoras/               # Registro de hallazgos y planes de mejora
├── examples/                  # Proyectos de ejemplo completos con tests
├── tests/                     # Suite de tests del framework (142 tests, 99% cobertura)
└── gestion/                   # Tickets y progreso del proyecto
```

---

## El Skill implement-us

El skill guía la implementación de una historia de usuario a través de **10 fases** (0–9):

| Fase | Nombre | Output principal |
|------|--------|-----------------|
| 0 | Validación de Contexto | `docs/plans/{US_ID}-context.md` |
| 1 | Generación BDD | `tests/features/{US_ID}-{nombre}.feature` |
| 2 | Plan de Implementación | `docs/plans/{US_ID}-plan.md` |
| 3 | Implementación | Archivos de código según perfil activo |
| 4 | Tests Unitarios | `tests/unit/test_*.py` |
| 5 | Tests de Integración | `tests/integration/test_*.py` |
| 6 | Validación BDD | `tests/step_defs/test_*_steps.py` |
| 7 | Quality Gates | `quality/reports/{US_ID}-quality.json` |
| 8 | Documentación | Actualiza plan, CHANGELOG, docs de arquitectura |
| 9 | Reporte Final | `docs/reports/{US_ID}-report.md` |

**Archivos clave del skill:**
- `skills/implement-us/skill.md` — orquestador, punto de entrada
- `skills/implement-us/artifacts.md` — **fuente de verdad de rutas canónicas**
- `skills/implement-us/conventions.md` — convención estructural de archivos de fase
- `docs/skills/implement-us/` — documentación completa del skill para referencia

### Perfiles Disponibles

| Perfil | Stack | Arquitectura | Coverage mín. |
|--------|-------|--------------|--------------|
| `pyqt-mvc` | PyQt6 Desktop | MVC | 90% |
| `fastapi-rest` | FastAPI | Layered | 95% |
| `flask-rest` | Flask API | Layered | 95% |
| `flask-webapp` | Flask Web | BFF + SSR | 90% |
| `generic-python` | Python genérico | Flexible | 95% |
| `hexagonal-ddd-bc` | Python DDD | Hexagonal + BC-first | 90% |
| `clean-architecture-bc` | FastAPI + SQLAlchemy async | Clean Architecture + BC-first | 90% |

Si ninguno encaja con el proyecto real, correr `/adapt-project` (`skills/adapt-project/skill.md`) una vez para generar un perfil custom calibrado.

---

## Sistema de Templates

Templates en `templates/` con placeholders `{VARIABLE_NAME}` y `{SNIPPET:id}`:
- Las variables se definen en `skills/implement-us/customizations/{perfil}.json`
- Los snippets son bloques de código específicos por stack (condicionales por perfil)
- Documentación técnica: `docs/developer/architecture/template-system.md`

---

## Sistema de Tracking

Tracking automático de tiempo por fase mediante directivas bash imperativas en cada archivo de fase. Las instrucciones están en secciones `🔴 Acción Requerida`.

**CLI bash-callable:** `python .claude/tracking/tracker_cli.py <subcomando>` — usada internamente por las fases del skill. Subcomandos: `init`, `start-phase`, `end-phase`, `start-task`, `end-task`, `status`, `end`.

**Comandos de usuario:** `/track-pause`, `/track-resume`, `/track-status`, `/track-report`, `/track-history`

**Persistencia:** `.claude/tracking/{US_ID}-tracking.json`

---

## Convenciones de Código

### Commits
```
<type>(<scope>): <subject>
# Types: feat, fix, docs, refactor, test, chore
```

### Branching
```
main                    # Releases de producción
  └── develop           # Desarrollo activo
       ├── feature/xxx
       ├── fix/xxx
       └── docs/xxx
```

### Quality Gates (del skill)
- **Pylint:** ≥ 8.0 (FastAPI: ≥ 8.5)
- **Complejidad Ciclomática:** ≤ 10 por función (PyQt: ≤ 12)
- **Índice de Mantenibilidad:** > 20 (FastAPI: > 25)
- **Cobertura:** según perfil (ver tabla de perfiles)

---

## Documentación de Referencia

| Qué necesito saber | Dónde leer |
|--------------------|------------|
| Cómo funciona el skill fase a fase | `docs/skills/implement-us/phase-X.md` |
| Rutas canónicas de artefactos | `skills/implement-us/artifacts.md` |
| Variables y snippets de templates | `docs/developer/architecture/template-system.md` |
| Arquitectura del tracking | `docs/developer/architecture/tracking.md` |
| Crear un skill custom | `docs/developer/contributing/creating-skills.md` |
| Guía de usuario final | `docs/user/index.md` |
| Hallazgos y mejoras pendientes | `docs/mejoras/hallazgos.md` |
| Tickets y progreso | `gestion/` |

---

**Última Actualización:** 2026-08-31 — v1.6.0
