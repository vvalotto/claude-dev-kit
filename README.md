# Claude Dev Kit

> Framework agnóstico de dominio para implementación automatizada de historias de usuario con Claude Code

[![Version](https://img.shields.io/badge/version-1.0.0--alpha-blue.svg)](https://github.com/vvalotto/claude-dev-kit)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-alpha-yellow.svg)](https://github.com/vvalotto/claude-dev-kit)

---

## 🎯 ¿Qué es Claude Dev Kit?

Claude Dev Kit es un framework instalable que **automatiza el ciclo completo de implementación** de historias de usuario a través de 10 fases estructuradas, con tracking automático de tiempo y validación de calidad.

**¿Por qué usarlo?**
- ✅ **Automatiza** el flujo de trabajo: Desde BDD hasta reporte final
- ✅ **Personalizable** por stack: PyQt, FastAPI, Flask, Django, Python genérico
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

**Ver:** [Guía de Inicio Rápido](docs/getting-started.md) para tutorial completo.

---

## 📚 Features Principales

### 🛠️ Skill implement-us: 10 Fases Automatizadas

| Fase | Qué Hace | Output |
|------|----------|--------|
| **0. Validación** | Verifica prerequisitos | - |
| **1. BDD** | Genera escenarios Gherkin | `tests/features/US-001.feature` |
| **2. Planning** | Crea plan detallado con tareas | `docs/planning/US-001-plan.md` |
| **3. Implementación** | Genera código base | `src/*.py` |
| **4. Tests Unitarios** | Crea tests por componente | `tests/test_*.py` |
| **5. Tests Integración** | Tests end-to-end | `tests/integration/` |
| **6. Validación BDD** | Ejecuta escenarios | pytest-bdd output |
| **7. Quality Gates** | Valida métricas | Pylint, coverage, CC |
| **8. Documentación** | Docstrings y comentarios | Código documentado |
| **9. Reporte Final** | Resumen y métricas | `docs/reports/US-001-report.md` |

**Ver:** [Documentación completa del skill](docs/skills/implement-us.md)

---

### 🎨 Sistema de Perfiles

Personaliza el framework para tu stack tecnológico:

| Perfil | Stack | Arquitectura | Tests | Coverage |
|--------|-------|--------------|-------|----------|
| **pyqt-mvc** | PyQt6 Desktop | MVC | pytest-qt | 95% |
| **fastapi-rest** | FastAPI API | Layered | pytest-asyncio | 95% |
| **flask-rest** | Flask API | Blueprints | pytest-flask | 90% |
| **flask-webapp** | Flask Web | MVT | pytest-flask | 85% |
| **generic-python** | Python | Flexible | pytest | 90% |

**Ver:** [Guía de Personalización](docs/customization.md)

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

**Ver:** [Tracking - Guía de Usuario](docs/tracking/user-guide.md)

---

### 📝 Sistema de Templates

Templates parametrizados con variables y snippets:

- **BDD:** Escenarios Gherkin por stack
- **Planning:** Planes de implementación
- **Testing:** Tests unitarios e integración
- **Reporting:** Reportes finales

**Variables:** `{US_ID}`, `{COMPONENT_TYPE}`, `{ARCHITECTURE_PATTERN}`, etc.
**Snippets:** Bloques de código multi-línea por perfil

**Ver:** [Sistema de Templates](docs/templates/template-system.md)

---

## 📖 Documentación

### Para Usuarios

| Documento | Descripción |
|-----------|-------------|
| [📘 Índice Principal](docs/index.md) | Hub de toda la documentación |
| [🚀 Getting Started](docs/getting-started.md) | Primera experiencia en <15 min |
| [📦 Instalación](docs/installation.md) | Setup completo y troubleshooting |
| [🎨 Personalización](docs/customization.md) | Adaptar a tu stack |
| [⚙️ Configuración](docs/configuration.md) | Referencia de opciones |
| [🛠️ Skill implement-us](docs/skills/implement-us.md) | Las 10 fases explicadas |
| [⏱️ Sistema de Tracking](docs/tracking/user-guide.md) | Comandos y reportes |

### Para Desarrolladores

| Documento | Descripción |
|-----------|-------------|
| [🏗️ Creando Skills](docs/skills/creating-skills.md) | Guía para crear skills custom |
| [📝 Templates](docs/templates/template-system.md) | Variables y snippets |
| [⏱️ Tracking - Arquitectura](docs/tracking/architecture.md) | Diseño técnico |

### Tutoriales por Stack (Fase 7)

- [PyQt-MVC](docs/examples/pyqt-project.md) - Aplicación desktop
- [FastAPI-REST](docs/examples/fastapi-project.md) - API asíncrona
- [Flask-REST](docs/examples/flask-rest-project.md) - API REST
- [Flask-WebApp](docs/examples/flask-webapp-project.md) - Web app
- [Python Genérico](docs/examples/generic-python.md) - CLI/librería

---

## 🗺️ Roadmap

### Completado ✅

- ✅ **Fase 1-2:** Setup y sistema de instalación (100%)
- ✅ **Fase 3:** Generalización de skills - 5 perfiles (100%)
- ✅ **Fase 4:** Generalización de templates (100%)
- ✅ **Fase 5:** Sistema de tracking completo (100%)
- ✅ **Fase 6:** Documentación general (100%)

### En Progreso 🔄

- 🔄 **Fase 7:** Ejemplos por stack tecnológico

### Pendiente ⏳

- ⏳ **Fase 8:** Testing del framework
- ⏳ **Fase 9:** Release 1.0

**Ver progreso detallado:** [Gestión de Tareas](gestion/)

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

- [Documentación](docs/index.md)
- [Plan del Proyecto](PROJECT_PLAN_claude-dev-kit.md)
- [Changelog](CHANGELOG.md) (pendiente)
- [GitHub Issues](https://github.com/vvalotto/claude-dev-kit/issues)

---

**¿Listo para empezar?** → [Guía de Inicio Rápido](docs/getting-started.md)
