# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
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
