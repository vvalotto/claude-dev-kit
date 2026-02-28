# Registro de Cambios

Todos los cambios notables de Claude Dev Kit se documentan en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
y este proyecto adhiere a [Versionado Semántico](https://semver.org/spec/v2.0.0.html).

## [Sin publicar]

---

## [1.3.0] - 2026-02-27

### Corregido

#### Skill `implement-us` — Correcciones sistemáticas post-análisis (42 hallazgos v1.2 + 24 discrepancias v1.3)

**Archivos de configuración (`config.json`)**
- Corregida clave `steps_path`: `"tests/features/steps/"` → `"tests/step_defs/"` (alineada con convención real)
- Corregida clave `test_path`: `"tests/"` → incluye subdirectorios `unit/` e `integration/` según fase
- Eliminadas referencias residuales a Django de `variables.*.examples` en todos los campos

**`skill.md`**
- Documentado subcomando `end-tracking` del CLI de tracking (antes ausente, causaba fallo en Fase 9)
- Eliminadas referencias a Django de ejemplos de perfil

**Fases 0–9** (correcciones aplicadas sobre todas las fases):
- **Fase 0:** Clarificados valores por defecto para `.pylintrc` y `pytest.ini`; agregado campo `skip_bdd` al template de `context.md`; eliminadas rutas BDD hardcodeadas (reemplazadas por referencias a `artifacts.md`)
- **Fase 1:** Clarificada forma de usar el template BDD y convención de nombres del feature file (`{US_ID}-{nombre}.feature`); unificada ruta canónica `tests/features/` en todos los puntos del archivo
- **Fase 2:** Clarificada ruta de output del plan (`docs/plans/{US_ID}-plan.md`) en el template; establecida prioridad explícita entre template externo y template embebido
- **Fase 3:** Agregada verificación de flag `--skip-bdd` antes de referencias a feature files; agregada instrucción de leer `component_structure` del perfil activo
- **Fase 4:** Ruta de tests unitarios leída desde `config.json` en lugar de hardcodeada como `tests/unit/`
- **Fase 5:** Ajustada precondición: verifica que no existan tests de integración previos antes de crear
- **Fase 6:** Clarificado uso de `bdd_config.steps_template` del perfil activo
- **Fase 7:** Corregidos umbrales hardcodeados en script Python de quality gates; umbrales ahora leídos desde `quality_gates` del perfil activo
- **Fase 8:** Eliminada referencia a `python manage.py generate_swagger` (Django) de la sección de automatización
- **Fase 9:** Agregado mapeo explícito de `quality.json → umbrales` para rellenar templates de reporte

**`artifacts.md`, `conventions.md`**
- Rutas BDD corregidas: `docs/bdd/` → `tests/features/` en toda la documentación de artefactos
- Eliminadas referencias a Django de ejemplos de rutas

---

## [1.1.0] - 2026-02-24

### Agregado

#### Skill `implement-us` — Nuevos archivos de referencia
- `skills/implement-us/artifacts.md` — Mapa centralizado de artefactos: rutas canónicas, fase generadora y fases consumidoras de cada output del skill
- `skills/implement-us/conventions.md` — Convención estructural para archivos de fase: secciones imperativas (`🔴 Acción Requerida`), secciones de referencia (`📖 Referencia`), checklists de salida y bloques STOP

### Modificado

#### Skill `implement-us` — Mejoras de robustez y reproducibilidad (v1.1)

**Fase 0 — Validación de Contexto**
- Verificación fail-fast de herramientas requeridas al inicio: pylint, radon, pytest, pytest-bdd; el proceso se detiene si alguna falta
- Clasificación automática del tipo de HU (nueva funcionalidad, refactorización, corrección de bug, etc.) con decisión automática sobre si aplica BDD
- Generación de `docs/plans/{US_ID}-context.md` con decisiones de ejecución, rutas de artefactos y umbrales de calidad del perfil activo

**Tracking — Todas las fases**
- Instrucciones de tracking (inicio/cierre de fase) reescritas como directivas bash imperativas en secciones `🔴 Acción Requerida`; se eliminaron los bloques de código Python que el agente interpretaba como documentación y no ejecutaba
- Estimaciones de duración humana (`Duración estimada: X minutos`) removidas de los encabezados de todas las fases (PRIN-001: las estimaciones humanas no producen varianza útil en ejecución por agente)

**Gates de entrada y checklists de salida — Todas las fases**
- Cada fase incluye ahora un gate de entrada que verifica la existencia de los artefactos requeridos de la fase anterior antes de comenzar
- Cada fase incluye un checklist de salida con condiciones verificables antes de avanzar a la siguiente fase

**Fase 2 — Plan de Implementación**
- Bloque STOP bloqueante antes de avanzar a Fase 3: el plan debe existir en disco y el usuario debe dar aprobación explícita

**Fase 3 — Implementación**
- Gate de entrada que verifica `context.md` y `plan.md` en disco antes de comenzar
- Instrucción imperativa de lectura del plan desde disco (no reconstruido desde contexto de sesión)
- Verificación de que cada tarea cubre al menos un criterio de aceptación de la HU

**Fase 9 — Reporte Final**
- Verificación de insumos al inicio (plan.md y quality.json deben existir en disco)
- Bloque STOP antes de cerrar tracking: el reporte debe existir en disco antes de finalizar

**Resiliencia — Protocolo de recuperación ante fallas**
- `skill.md`: sección "Manejo de Fallas" con protocolo general de 6 pasos; límite de 2 intentos autónomos antes de escalar al usuario
- Fases 4, 5, 6 y 7: protocolos específicos de qué hacer cuando la fase falla, con árbol de decisión del origen del fallo (implementación, escenario, step definition, quality gate específico)

---

## [1.0.0] - 2026-02-17

### Agregado

#### Sistema de Instalación
- Instalador multiplataforma (`install/installer.py`) compatible con Linux, macOS y Windows
- Configuración de instalación en YAML (`install/config.yaml`) con selección de perfil
- Validador post-instalación (`install/validate-setup.py`) con diagnósticos detallados
- Modo interactivo (selección guiada de perfil) y modo no interactivo (`--profile`, `--yes`, `--dry-run`, `--force`)
- Script wrapper para Unix/macOS (`install/install.sh`)

#### Skill `implement-us`
- Skill principal `implement-us` que guía paso a paso la implementación de historias de usuario en proyectos Python
- Arquitectura modular con un orquestador (`skill.md`) y 10 agentes de fase especializados (Fase 0–9):
  - Fase 0: Validación de Contexto
  - Fase 1: Generación de Escenarios BDD
  - Fase 2: Planificación de Implementación
  - Fase 3: Implementación
  - Fase 4: Tests Unitarios
  - Fase 5: Tests de Integración
  - Fase 6: Validación BDD
  - Fase 7: Quality Gates (Pylint, Complejidad Ciclomática, Índice de Mantenibilidad, Cobertura)
  - Fase 8: Documentación
  - Fase 9: Reporte Final
- 5 perfiles por stack tecnológico, cada uno con convenciones arquitectónicas y quality gates específicos:
  - `pyqt-mvc` — Aplicaciones de escritorio PyQt6 con arquitectura MVC
  - `fastapi-rest` — APIs REST con FastAPI, arquitectura en capas y async/await
  - `flask-rest` — APIs REST con Flask, arquitectura en capas (sync)
  - `flask-webapp` — Webapps fullstack con Flask, Jinja2 SSR y patrón BFF
  - `generic-python` — Proyectos Python genéricos (librerías, herramientas CLI, scripts, data science)
- Sistema de variables parametrizables (`{ARCHITECTURE_PATTERN}`, `{COMPONENT_TYPE}`, `{COMPONENT_PATH}`, etc.) que permite que una única definición de skill se adapte a cualquier stack
- Archivo de configuración base (`skills/implement-us/config.json`) con sistema de overrides por perfil

#### Sistema de Templates
- Template de escenarios BDD (`templates/bdd/bdd-scenario.feature`) en formato Gherkin
- Template de plan de implementación (`templates/planning/implementation-plan.md`) con desglose de tareas y estimaciones de tiempo
- Template de reporte final (`templates/reporting/implementation-report.md`) con métricas de calidad
- Template de tests unitarios (`templates/testing/test-unit.py`) con fixtures y tests parametrizados
- Biblioteca de snippets: 35 fragmentos de código organizados por tipo (modelo, vista, controlador, servicio, repositorio, test, config) × 5 perfiles

#### Sistema de Tracking de Tiempo
- Módulo core de tracking (`tracking/time_tracker.py`) con medición automática de tiempo por fase y tarea
- Módulo de reportes (`tracking/reports.py`) para análisis histórico
- 5 skills de tracking para Claude Code:
  - `/track-pause [motivo]` — Pausar tracking con motivo opcional
  - `/track-resume` — Reanudar tracking después de una pausa
  - `/track-status` — Ver estado actual del tracking
  - `/track-report [us_id]` — Generar reporte detallado de una historia de usuario
  - `/track-history [--last N]` — Ver historial de tracking
- Persistencia JSON en `.claude/tracking/{us_id}-tracking.json`
- Tracking de varianza: tiempo estimado vs. real por fase y tarea

#### Documentación
- Documentación de usuario (8 documentos, ~2.800 líneas):
  - Guía de inicio rápido — desde la clonación hasta el primer `/implement-us` en menos de 15 minutos
  - Guía de instalación detallada para todas las plataformas
  - Guía de personalización — perfiles, variables, creación de perfiles custom
  - Referencia de configuración — todas las opciones disponibles con ejemplos
  - Referencia del skill `implement-us` con todas las fases documentadas
  - Guía de usuario del sistema de tracking
  - Ejemplos de uso del tracking
  - Índice de documentación con navegación
- Documentación técnica para desarrolladores (5 documentos, ~1.900 líneas):
  - Guía para crear skills personalizados
  - Arquitectura del sistema de templates
  - Arquitectura del sistema de tracking
  - Documentación del sistema de memoria de sesiones
  - Plantilla de documento para contributors
- Workflow de GitHub Actions para sincronización automática a la Wiki (`.github/workflows/sync-wiki.yml`) — se activa en cada push a `main` y aplana la estructura de directorios a nombres PascalCase

#### Ejemplos de Código por Stack
Cinco proyectos completos y funcionales generados usando el propio framework, cada uno con escenarios BDD completos, tests unitarios, tests de integración y validación de quality gates:

- **PyQt6 MVC — Calculadora** (`examples/code/pyqt-calculator/`): Calculadora de escritorio con arquitectura MVC. 14 tests, 86% de cobertura. Tutorial completo en `docs/examples/pyqt-project.md`.
- **FastAPI REST — TODO API** (`examples/code/fastapi-todo-api/`): API REST asíncrona con arquitectura en capas e inyección de dependencias. 29 tests, 98% de cobertura. Tutorial completo en `docs/examples/fastapi-project.md`.
- **Flask REST — Contacts API** (`examples/code/flask-contacts-api/`): API REST sincrónica con patrones Repository + Mapper. 38 tests, 94% de cobertura. Tutorial completo en `docs/examples/flask-rest-api-project.md`.
- **Flask WebApp — Blog** (`examples/code/flask-blog-app/`): Aplicación web fullstack con patrón BFF y Server-Side Rendering. 43 tests, 99% de cobertura. Tutorial completo en `docs/examples/flask-webapp-project.md`.
- **Python Genérico CLI — CSV Tool** (`examples/code/csv-tool/`): Herramienta CLI de procesamiento de datos con pandas. 90 tests, 98% de cobertura. Tutorial completo en `docs/examples/generic-python.md`.

#### Suite de Tests del Framework
- Suite de tests completa del propio framework: 107 tests, 99% de cobertura global
- `tests/test_installer.py` (37 tests) — lógica del instalador, fusión de perfiles, validación, opciones CLI
- `tests/test_tracking.py` (38 tests) — tracking de tiempo, pausas, cálculo de varianza, persistencia JSON
- `tests/test_config_merge.py` (31 tests) — fusión de config base + perfil, resolución de variables
- Configuración compartida de pytest (`pytest.ini`) y fixtures (`tests/conftest.py`)

### Modificado

- Estado de la documentación actualizado de "en desarrollo" a "estable v1.0"
- Conjunto de perfiles del framework actualizado: eliminado `django-mvt`, agregados `flask-rest` y `flask-webapp` como perfiles listos para producción
- Workflow de sincronización con la Wiki actualizado con nombres PascalCase sin guiones ni extensión `.md` para plena compatibilidad con GitHub Wiki

### Corregido

- Links internos de documentación actualizados al nuevo formato PascalCase de la Wiki
- Referencias al perfil eliminado `django-mvt` corregidas en toda la documentación y READMEs
- Referencias a agentes de fase en `skill.md` actualizadas de marcadores provisionales a links correctos
- Conteo de fases inconsistente ("9 fases") corregido a "10 fases (Fase 0 a Fase 9)" en toda la documentación
- Links internos rotos en `install/README.md` que apuntaban a rutas inexistentes corregidos
- Directorio `docs/examples/` agregado al workflow de sync de la Wiki (estaba ausente en el workflow inicial)

### Eliminado

- Perfil `django-mvt` eliminado de `install/config.yaml` y `skills/implement-us/customizations/` — este perfil estaba planificado pero no fue implementado; usar `generic-python` como punto de partida para proyectos Django

---

[Sin publicar]: https://github.com/vvalotto/claude-dev-kit/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/vvalotto/claude-dev-kit/releases/tag/v1.0.0
