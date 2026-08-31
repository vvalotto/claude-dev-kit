# Claude Dev Kit

> Framework agnóstico de dominio para implementación automatizada de historias de usuario con Claude Code

[![Version](https://img.shields.io/badge/version-1.5.0-blue.svg)](https://github.com/vvalotto/claude-dev-kit/releases/tag/v1.5.0)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-stable-brightgreen.svg)](https://github.com/vvalotto/claude-dev-kit)
[![Tests](https://img.shields.io/badge/tests-142%20passed-brightgreen.svg)](tests/)
[![Coverage](https://img.shields.io/badge/coverage-99%25-brightgreen.svg)](tests/)

---

## 🎯 ¿Qué es Claude Dev Kit?

Claude Dev Kit es un framework instalable que **automatiza el ciclo completo de implementación** de historias de usuario a través de 10 fases estructuradas, con tracking automático de tiempo y validación de calidad.

**¿Por qué usarlo?**
- ✅ **Automatiza** el flujo de trabajo: Desde BDD hasta reporte final
- ✅ **Personalizable** por stack: PyQt, FastAPI, Flask REST, Flask WebApp, Python genérico
- ✅ **Trackea tiempo** automáticamente por fase y tarea
- ✅ **Genera** BDD, planes, tests, documentación y reportes
- ✅ **Valida calidad** con quality gates (Pylint, coverage, complejidad)

---

## 🚀 Quick Start

### Instalación (5 minutos)

```bash
# 1. Clonar el framework
git clone https://github.com/vvalotto/claude-dev-kit.git ~/.claude-dev-kit

# 2. Navegar a tu proyecto
cd ~/mi-proyecto-python

# 3. Ejecutar instalador
python ~/.claude-dev-kit/install/installer.py

# 4. Seleccionar perfil (pyqt-mvc, fastapi-rest, flask-rest, flask-webapp, generic-python)
# El instalador te guiará interactivamente
```

### Primera Historia de Usuario (5 minutos)

```bash
# Crear historia de usuario
cat > docs/user-stories/US-001.md << 'EOF'
# US-001: Calculadora Simple

## Descripción
Como usuario, quiero una calculadora que sume dos números.

## Criterios de Aceptación
- Acepta dos números como parámetros
- Retorna la suma correcta
- Maneja casos edge (negativos, ceros)
EOF

# Ejecutar skill
/implement-us US-001

# El skill automatiza las 10 fases:
# 0. Validación ✅
# 1. Escenarios BDD ✅
# 2. Plan de implementación ✅
# 3. Código base ✅
# 4. Tests unitarios ✅
# 5. Tests de integración ✅
# 6. Validación BDD ✅
# 7. Quality gates ✅
# 8. Documentación ✅
# 9. Reporte final ✅
```

**Ver:** [Guía de Inicio Rápido](docs/user/getting-started.md) para tutorial completo.

---

## 📚 Features Principales

### 🛠️ Skill implement-us: 10 Fases Automatizadas

| Fase | Qué Hace | Output |
|------|----------|--------|
| **0. Validación** | Verifica herramientas, clasifica HU, decide BDD | `docs/plans/{US_ID}-context.md` |
| **1. BDD** | Genera escenarios Gherkin | `tests/features/{US_ID}-{nombre}.feature` |
| **2. Planning** | Crea plan detallado con tareas *(STOP — requiere aprobación)* | `docs/plans/{US_ID}-plan.md` |
| **3. Implementación** | Genera código guiado por el plan en disco | `src/*.py` |
| **4. Tests Unitarios** | Crea tests por componente | `tests/test_*.py` |
| **5. Tests Integración** | Tests end-to-end | `tests/integration/` |
| **6. Validación BDD** | Ejecuta escenarios | pytest-bdd output |
| **7. Quality Gates** | Valida métricas | `quality/reports/{US_ID}-quality.json` |
| **8. Documentación** | Docstrings y comentarios | Código documentado |
| **9. Reporte Final** | Resumen y métricas *(STOP — reporte debe existir)* | `docs/reports/{US_ID}-report.md` |

**Ver:** [Documentación completa del skill](docs/skills/implement-us/index.md)

---

### 🎨 Sistema de Perfiles

Personaliza el framework para tu stack tecnológico:

| Perfil | Stack | Arquitectura | Tests | Coverage |
|--------|-------|--------------|-------|----------|
| **pyqt-mvc** | PyQt6 Desktop | MVC | pytest-qt | 90% |
| **fastapi-rest** | FastAPI API | Layered | pytest-asyncio | 95% |
| **flask-rest** | Flask API | Layered | pytest-flask | 95% |
| **flask-webapp** | Flask Web | BFF + SSR | pytest-flask | 90% |
| **generic-python** | Python | Flexible | pytest | 95% |
| **hexagonal-ddd-bc** | Python DDD | Hexagonal + BC-first | pytest | 90% |
| **clean-architecture-bc** | FastAPI + SQLAlchemy async | Clean Architecture + BC-first | pytest-asyncio | 90% |

**Ver:** [Guía de Personalización](docs/user/customization.md)

**¿Ninguno encaja con tu proyecto?** Corré `/adapt-project` una sola vez — diagnostica la arquitectura real y genera un perfil custom calibrado, sin editar JSON a mano.

---

### ⏱️ Sistema de Tracking

Tracking automático de tiempo por fase y tarea:

```bash
# Ver estado actual
/track-status

# Pausar trabajo
/track-pause "Lunch break"

# Reanudar
/track-resume

# Ver reporte de US
/track-report US-001

# Output:
# ⏱️ US-001: 1h 45min (est: 2h, -15min)
# Fase 0: 2min | Fase 1: 5min | Fase 2: 8min ...
# Varianza: -7.5% (mejor que estimado)
```

**Ver:** [Tracking - Guía de Usuario](docs/user/tracking/user-guide.md)

---

### 📝 Sistema de Templates

Templates parametrizados con variables y snippets:

- **BDD:** Escenarios Gherkin por stack
- **Planning:** Planes de implementación
- **Testing:** Tests unitarios e integración
- **Reporting:** Reportes finales

**Variables:** `{US_ID}`, `{COMPONENT_TYPE}`, `{ARCHITECTURE_PATTERN}`, etc.
**Snippets:** Bloques de código multi-línea por perfil

**Ver:** [Sistema de Templates](docs/developer/architecture/template-system.md)

---

## 📖 Documentación

### Para Usuarios

| Documento | Descripción |
|-----------|-------------|
| [📘 Índice Principal](docs/user/index.md) | Hub de toda la documentación |
| [🚀 Getting Started](docs/user/getting-started.md) | Primera experiencia en <15 min |
| [📦 Instalación](docs/user/installation.md) | Setup completo y troubleshooting |
| [🎨 Personalización](docs/user/customization.md) | Adaptar a tu stack |
| [⚙️ Configuración](docs/user/configuration.md) | Referencia de opciones |
| [🛠️ Skill implement-us](docs/skills/implement-us/index.md) | Las 10 fases explicadas |
| [⏱️ Sistema de Tracking](docs/user/tracking/user-guide.md) | Comandos y reportes |

### Para Desarrolladores

| Documento | Descripción |
|-----------|-------------|
| [🏗️ Creando Skills](docs/developer/contributing/creating-skills.md) | Guía para crear skills custom |
| [📝 Templates](docs/developer/architecture/template-system.md) | Variables y snippets |
| [⏱️ Tracking - Arquitectura](docs/developer/architecture/tracking.md) | Diseño técnico |

### Tutoriales por Stack

| Tutorial | Descripción | Tests |
|----------|-------------|-------|
| [PyQt-MVC](docs/examples/pyqt-project.md) | Calculadora desktop | 14 tests, 86% cov |
| [FastAPI-REST](docs/examples/fastapi-project.md) | TODO API asíncrona | 29 tests, 98% cov |
| [Flask-REST](docs/examples/flask-rest-api-project.md) | Contacts API | 38 tests, 94% cov |
| [Flask-WebApp](docs/examples/flask-webapp-project.md) | Blog fullstack | 43 tests, 99% cov |
| [Python Genérico](docs/examples/generic-python.md) | CSV Tool CLI | 90 tests, 98% cov |

> 📖 **[Wiki](https://github.com/vvalotto/claude-dev-kit/wiki)** — Documentación completa en GitHub Wiki

---

## 🗺️ Roadmap

### v1.5.0 ✅ (Completado — 2026-08-31)

- ✅ Nuevo perfil `clean-architecture-bc`: Clean Architecture BC-first, target FastAPI + SQLAlchemy async
- ✅ Nuevo skill `/adapt-project`: calibra `implement-us` a proyectos sin perfil bundleado (#41)
- ✅ Docs de fase ya no hardcodean el perfil `hexagonal-ddd-bc`; leen umbrales y rutas del perfil activo real
- ✅ Fase 7 acota `codeguard` a archivos modificados por la US, no todo el árbol del componente
- ✅ Template `test-unit.py` renombrado a `.tpl` — ya no rompe hooks de pre-commit del proyecto consumidor

### v1.4.1 ✅ (Completado — 2026-05-18)

- ✅ Instalador: eliminada dependencia de `pyyaml`; configuración migrada a JSON (stdlib pura)
- ✅ Instalador: manejo de `EOFError` en stdin no interactivo (CI, pipes)
- ✅ Tracking: nuevo `tracker_cli.py` — CLI bash-callable con 7 subcomandos (init, start/end-phase, start/end-task, status, end)
- ✅ Tracking: `TimeTracker.load(us_id)` — carga tracker por ID; glob corregido para soportar cualquier prefijo
- ✅ Pipeline: fases 0–9 migradas de `track.py` a `tracker_cli.py`
- ✅ Pipeline: gates ejecutables en Fase 7 (`quality/reports/`) y Fase 9 (`docs/reports/`)
- ✅ Suite de tests: 142 tests, 99% cobertura

### v1.4.0 ✅ (Completado — 2026-04-09)

- ✅ Nuevo perfil `hexagonal-ddd-bc` para proyectos con arquitectura hexagonal + DDD + BC-first
- ✅ Integración con `codeguard` como orquestador de quality gates para este perfil

### v1.3.0 ✅ (Completado — 2026-02-27)

- ✅ Skill `implement-us` — correcciones sistemáticas post-análisis (42 hallazgos + 24 discrepancias)

### v1.1.0 ✅ (Completado — 2026-02-24)

- ✅ Skill `implement-us` — mejoras de robustez y reproducibilidad
  - Fase 0: verificación fail-fast + clasificación de HU + `context.md`
  - Gates de entrada y checklists de salida en todas las fases
  - STOP bloqueante en Fase 2 y Fase 9

### v1.0.0 ✅ (Completado — 2026-02-17)

- ✅ Sistema de instalación multiplataforma (Linux, macOS, Windows)
- ✅ Skill `implement-us` con 10 fases y 5 perfiles
- ✅ Sistema de templates parametrizados (35 snippets)
- ✅ Sistema de tracking de tiempo automático (5 skills)
- ✅ 5 ejemplos funcionales completos con tests
- ✅ Suite de tests del framework

### Futuro (v1.6)

- Instalador (`--profile`) soporta los perfiles BC-first `hexagonal-ddd-bc` y `clean-architecture-bc` (#56)
- Soporte para proyectos TypeScript/Node.js
- Integración con GitHub Actions para quality gates automáticos
- Dashboard web para tracking de tiempo

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas!

```bash
# 1. Fork del proyecto
git clone https://github.com/TU-USUARIO/claude-dev-kit.git

# 2. Crear branch
git checkout -b feature/mi-feature

# 3. Commit cambios
git commit -m "feat: agregar feature X"

# 4. Push y crear PR
git push origin feature/mi-feature
```

**Ver:** [Guía de Contribución](CONTRIBUTING.md) (pendiente)

---

## 📋 Prerequisitos

- Python 3.9 o superior
- Git 2.0+
- Claude Code CLI
- Proyecto Python (opcional para pruebas)

---

## 🐛 Reportar Issues

¿Encontraste un bug o tienes una sugerencia?

- **Bug:** [Crear Issue](https://github.com/vvalotto/claude-dev-kit/issues/new?template=bug_report.md)
- **Feature Request:** [Crear Issue](https://github.com/vvalotto/claude-dev-kit/issues/new?template=feature_request.md)

---

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

---

## 👨‍💻 Autor

**Víctor Valotto**
- GitHub: [@vvalotto](https://github.com/vvalotto)
- Email: victor@valotto.com

---

## 🙏 Agradecimientos

- **Anthropic** - Por Claude Code y la API de Claude
- **Comunidad Python** - Por las herramientas y frameworks
- **Contributors** - Por mejorar este proyecto

---

## 🔗 Enlaces

- [Documentación](docs/user/index.md)
- [Wiki](https://github.com/vvalotto/claude-dev-kit/wiki)
- [CHANGELOG](CHANGELOG.md)
- [GitHub Issues](https://github.com/vvalotto/claude-dev-kit/issues)
- [GitHub Releases](https://github.com/vvalotto/claude-dev-kit/releases)

---

**¿Listo para empezar?** → [Guía de Inicio Rápido](docs/user/getting-started.md)
