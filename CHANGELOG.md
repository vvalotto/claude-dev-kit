# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

#### Fase 4: Generalización de Templates (Sprint 2) - 2026-02-14

- **Sistema de templates generalizado** - 4 templates framework-agnostic:
  - `templates/bdd/scenario.feature` - Escenarios Gherkin
  - `templates/planning/implementation-plan.md` - Planes de implementación
  - `templates/reporting/implementation-report.md` - Reportes finales
  - `templates/testing/test-unit.py` - Tests unitarios

- **Sistema de variables expandido** - 20+ variables parametrizadas:
  - Variables simples: `{US_ID}`, `{US_TITLE}`, `{ARCHITECTURE_PATTERN}`, etc.
  - Variables de template: `{BACKGROUND_SETUP}`, `{TEST_FILE_PATTERN}`, `{ARCHITECTURE_DESCRIPTION}`, `{TEST_CLASS_ORGANIZATION_COMMENT}`

- **Sistema de snippets** - 7 tipos × 5 perfiles = 35 snippets:
  - `integration_checklist` - Checklist de integración por stack
  - `architecture_code_blocks` - Código de integración específico (~20-30 líneas/perfil)
  - `manual_testing_specifics` - Testing manual relevante
  - `test_imports` - Imports de frameworks de testing
  - `test_signals_class` - Clase TestSignals (solo PyQt)
  - `test_integration_class` - Clase TestIntegracion por stack
  - `test_fixtures` - Fixtures pytest específicas

- **Perfiles actualizados** - 5 perfiles con snippets:
  - `pyqt-mvc.json` - PyQt6 MVC + Factory/Coordinator
  - `fastapi-rest.json` - FastAPI async REST APIs
  - `flask-rest.json` - Flask REST APIs
  - `flask-webapp.json` - Flask fullstack webapps
  - `generic-python.json` - Python genérico

- **Documentación completa:**
  - `templates/README.md` (~487 líneas) - Guía de usuario
  - `docs/templates/template-system.md` (~600 líneas) - Documentación técnica
  - `docs/analysis/TICKET-030-analysis.md` (~1,200 líneas) - Análisis exhaustivo

**Tickets:** TICKET-030 a TICKET-037 (8 tickets)
**Commits:** 8 commits en branch `feature/template-generalization`
**Líneas agregadas:** ~3,500 líneas (templates + documentación + snippets)

#### Fase Inicial: Configuración del Proyecto

- Configuración inicial del proyecto Claude Dev Kit
- Estructura de directorios base para el framework
  - `install/` - Sistema de instalación multiplataforma
  - `skills/implement-us/` - Skill principal con subdirectorios phases/ y customizations/
  - `templates/` - Templates reutilizables (bdd/, planning/, testing/, reporting/)
  - `tracking/` - Sistema de tracking de tiempo
  - `docs/` - Documentación del framework
  - `examples/` - Proyectos de ejemplo
  - `scripts/` - Scripts de utilidad
  - `tests/` - Tests del framework
- Documentación inicial completa
  - CLAUDE.md - Guía para Claude Code (en español, 438 líneas)
  - README.md - Documentación principal (440 líneas, 18 secciones)
  - PROJECT_PLAN_claude-dev-kit.md - Plan completo del proyecto
- Sistema de gestión del proyecto
  - Estructura por fases (9 fases) y sprints (4 sprints)
  - Sistema de tickets con estados (TODO, IN_PROGRESS, DONE, BLOCKED)
  - Fase 1 documentada con 10 tickets
- Material de migración incluido en `_work/`
  - Skills de implement-us desde simapp_termostato
  - Templates (BDD, planning, testing, reporting)
  - Sistema de tracking completo (time_tracker.py, commands.py)
  - Documentación de referencia
- Configuración de .gitignore optimizada
  - Exclusiones estándar de Python
  - Exclusiones de IDEs (.idea/)
  - Exclusiones de archivos de sistema (macOS, Windows)
  - Exclusiones de archivos temporales
  - Decisión documentada de incluir _work/ en git
- LICENSE MIT incluido (Copyright 2026 Victor Valotto)

### Changed
- N/A

### Deprecated
- N/A

### Removed
- N/A

### Fixed
- N/A

### Security
- N/A

---

## Roadmap Futuro

### [1.0.0] - Versión Inicial (En Desarrollo)

#### Fase 1: Setup Inicial ✅ (Completada)
- Estructura base del proyecto
- Documentación inicial
- Sistema de gestión

#### Fase 2: Sistema de Instalación (Sprint 1)
- Instalador Python multiplataforma
- Configuración YAML con perfiles
- Validador post-instalación

#### Fase 3: Generalización de Skills (Sprint 2)
- Skill implement-us generalizado
- Configuración base + perfiles

#### Fase 4: Templates (Sprint 2)
- Templates BDD generalizados
- Templates de planning
- Templates de testing
- Templates de reporting

#### Fase 5: Sistema de Tracking (Sprint 2)
- Migración de time_tracker.py
- Comandos /track-*
- Modelos de datos

#### Fase 6: Documentación (Sprint 3)
- Documentación completa en docs/
- Guías por stack tecnológico

#### Fase 7: Ejemplos (Sprint 3)
- Proyectos de ejemplo completos
- Al menos 2 stacks (PyQt, FastAPI)

#### Fase 8: Testing y Validación (Sprint 4)
- Tests del framework
- Validación multiplataforma

#### Fase 9: Release v1.0 (Sprint 4)
- Release inicial
- Publicación en GitHub

### [1.1.0] - Funcionalidades Adicionales (Futuro)
- Skill adicional: `/code-review`
- Dashboard web de métricas
- Soporte para TypeScript/JavaScript
- Más perfiles (Flask, React, Vue)

### [1.2.0] - Integraciones (Futuro)
- Integración con Jira
- Integración con GitHub Issues
- Notificaciones (Slack, email)

### [2.0.0] - Ecosistema (Futuro)
- Marketplace de skills comunitarios
- API pública para crear skills
- Soporte para múltiples lenguajes (Go, Rust, Java)

---

**Nota:** Este proyecto está actualmente en fase de desarrollo inicial (Pre-release v0.1.0-dev).
Los cambios se documentarán aquí a medida que se completen las fases del proyecto.
