# TODO - Claude Dev Kit

## 🔥 Ahora (Esta Sesión)

### Sistema de Memorización de Contexto
- [ ] Implementar sistema de memorización entre sesiones
  - [ ] Crear `.claude/hooks/save-session.sh` (hook SessionEnd)
  - [ ] Configurar `.claude/settings.json`
  - [ ] Crear archivos base de memoria en `~/.claude/projects/.../memory/`
  - [ ] Probar flujo completo (exit → init → resumen)
  - [ ] Documentación: ✅ `docs/session-memory-system.md`

> **Referencia:** Ver `docs/session-memory-system.md` para guía completa de implementación

---

## 📋 Siguiente Sesión

### Fase 2: Sistema de Instalación
- [ ] Migrar sistema de tracking desde `_work/from-simapp/tracking/` → `tracking/`
  - [ ] `time_tracker.py` (100% genérico, listo para copiar)
  - [ ] `commands.py` (comandos /track-*)
  - [ ] `__init__.py`
- [ ] Crear `install/installer.py` - versión básica
  - [ ] Modo interactivo: selección de perfil
  - [ ] Modo no-interactivo: `--profile` flag
  - [ ] Copiar archivos a `.claude/` del proyecto destino
- [ ] Crear `install/config.yaml` - definir perfiles base
  - [ ] pyqt-mvc
  - [ ] fastapi-rest
  - [ ] django-mvt
  - [ ] generic-python
- [ ] Crear `scripts/validate-setup.py` - validador post-instalación

> **Estimación:** 3-4 horas
> **Referencia:** `PROJECT_PLAN_claude-dev-kit.md` Sección 5.2 (Fase 2)

---

## 🎯 Más Adelante (Sprint 2)

### Fase 3: Generalización de Skills
- [ ] Adaptar `_work/from-simapp/skills/implement-us.md`
  - [ ] Remover referencias específicas a MVC/PyQt
  - [ ] Reemplazar con variables: `{ARCHITECTURE_PATTERN}`, `{COMPONENT_TYPE}`
  - [ ] Crear `skills/implement-us/config.json` base
  - [ ] Crear perfiles en `skills/implement-us/customizations/`

### Fase 4: Templates
- [ ] Generalizar templates de `_work/from-simapp/templates/`
  - [ ] `implementation-plan.md`
  - [ ] `implementation-report.md`
  - [ ] `test-unit.py`
  - [ ] `bdd-scenario.feature` (ya es genérico ✅)

### Fase 5: Sistema de Tracking
- [ ] Integrar tracking migrado con skills
- [ ] Crear documentación de comandos `/track-*`

---

## 📚 Backlog (Sprints 3-4)

### Documentación (Sprint 3)
- [ ] `docs/getting-started.md`
- [ ] `docs/installation.md`
- [ ] `docs/customization.md`
- [ ] `docs/configuration.md`

### Ejemplos (Sprint 3)
- [ ] `examples/pyqt-mvc/` - Proyecto completo de ejemplo
- [ ] `examples/fastapi-rest/` - API REST de ejemplo
- [ ] `examples/django-mvt/` - Proyecto Django de ejemplo

### Testing y Release (Sprint 4)
- [ ] Suite de tests completa
- [ ] Validación de quality gates
- [ ] Release v1.0

---

## 📌 Notas Rápidas

- **Branch actual:** `main`
- **Sprint actual:** Sprint 1 - Setup + Instalación
- **Fase actual:** Transición Fase 1 → Fase 2
- **Fase 1:** ✅ Completada al 100%

### Archivos Clave
- Plan completo: `PROJECT_PLAN_claude-dev-kit.md`
- Guía del proyecto: `CLAUDE.md`
- Fase 2 Sprint: `gestion/fase-2-sistema-instalacion/sprint-1.md`
- Material fuente: `_work/from-simapp/`
- Sistema de sesiones: `docs/session-memory-system.md`

### Decisiones Recientes
- Sistema de memorización: Enfoque híbrido (hook simple + resumen inteligente)
- Priorizar migración de tracking antes que instalador (ganancias rápidas)

---

**Última Actualización:** 2026-02-08
