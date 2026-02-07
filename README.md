# Claude Dev Kit

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

Framework agnóstico de dominio para desarrollo asistido con [Claude Code](https://claude.ai/code). Automatiza el ciclo completo de implementación de historias de usuario en proyectos Python.

---

## 🎯 ¿Qué es Claude Dev Kit?

**Claude Dev Kit** es un framework instalable que proporciona skills, templates y herramientas de tracking para asistir el desarrollo de software con Claude Code. Está diseñado para ser **agnóstico de dominio**, permitiendo su uso en diferentes stacks tecnológicos mediante un sistema de perfiles.

En lugar de escribir código desde cero, el framework guía paso a paso la implementación de historias de usuario a través de 9 fases estructuradas, desde la validación inicial hasta el reporte final, incluyendo:

- Generación automática de escenarios BDD
- Planes de implementación detallados
- Tests unitarios y de integración
- Validación de quality gates (pylint, complejidad, cobertura)
- Tracking automático de tiempo por fase y tarea

---

## ✨ Características Principales

### 🤖 Skill `implement-us` - Implementación Guiada de User Stories

Proceso estructurado de 9 fases para implementar historias de usuario:

1. **Validación de Contexto** - Verifica arquitectura y estándares
2. **Generación BDD** - Crea escenarios Gherkin automáticamente
3. **Plan de Implementación** - Genera checklist detallado con estimaciones
4. **Implementación** - Desarrollo guiado del código
5. **Tests Unitarios** - Generación de tests con fixtures
6. **Tests de Integración** - Tests end-to-end
7. **Validación BDD** - Ejecuta escenarios contra implementación
8. **Quality Gates** - Valida métricas de calidad (pylint, CC, MI, coverage)
9. **Reporte Final** - Documenta tiempo, varianzas y resultados

### ⏱️ Sistema de Tracking de Tiempo Automático

- Tracking automático por fase y tarea
- Pausas manuales con razón (`/track-pause`, `/track-resume`)
- Reportes en tiempo real (`/track-status`)
- Historial y métricas (`/track-report`, `/track-history`)
- Análisis de varianza (estimado vs. real)

### 📄 Templates Reutilizables

- **BDD**: Escenarios Gherkin, steps pytest-bdd
- **Planning**: Planes de implementación, ADRs
- **Testing**: Tests unitarios e integración con fixtures
- **Reporting**: Reportes de implementación y retrospectivas

### 🎨 Sistema de Perfiles por Stack Tecnológico

Personalización para diferentes tecnologías:

- **pyqt-mvc**: PyQt6 + arquitectura MVC + patrones Factory/Coordinator
- **fastapi-rest**: FastAPI + APIs REST + arquitectura en capas
- **django-mvt**: Django + patrón MVT + convenciones Django
- **generic-python**: Proyectos Python genéricos sin framework específico

---

## 🚀 Instalación

### Prerrequisitos

- Python 3.10 o superior
- [Claude Code](https://claude.ai/code) instalado y configurado
- Git

### Instalación Global (Recomendada)

```bash
# 1. Clonar el kit en ubicación global
git clone https://github.com/vvalotto/claude-dev-kit.git ~/.claude-dev-kit

# 2. Navegar al proyecto donde lo quieres usar
cd ~/mi-proyecto-python

# 3. Ejecutar instalador (interactivo)
python ~/.claude-dev-kit/install/installer.py

# 4. Seleccionar perfil según tu stack
# Opciones: pyqt-mvc | fastapi-rest | django-mvt | generic-python

# 5. Validar instalación
python ~/.claude-dev-kit/scripts/validate-setup.py
```

### Instalación No Interactiva

```bash
# Especificar perfil directamente
python ~/.claude-dev-kit/install/installer.py --profile pyqt-mvc --yes

# Dry-run (simular sin ejecutar)
python ~/.claude-dev-kit/install/installer.py --profile fastapi-rest --dry-run
```

### Estructura Post-Instalación

Después de la instalación, tu proyecto tendrá:

```
mi-proyecto/
├── .claude/                    # Instalado por el kit
│   ├── skills/                # Skill implement-us
│   ├── templates/             # Templates personalizados
│   ├── tracking/              # Sistema de tracking
│   └── config.json            # Configuración del kit
├── CLAUDE.md                  # Generado si no existe
└── [tu código existente]
```

---

## 💡 Uso Rápido

### Implementar una Historia de Usuario

```bash
# Abrir Claude Code en tu proyecto
cd ~/mi-proyecto-python

# Ejecutar el skill
/implement-us US-001

# Con especificación de producto
/implement-us US-001 --producto mi_aplicacion

# Saltar generación BDD (opcional)
/implement-us US-001 --skip-bdd
```

### Comandos de Tracking

```bash
# Pausar tracking (ej: reunión, almuerzo)
/track-pause "Reunión de equipo"

# Reanudar tracking
/track-resume

# Ver estado actual
/track-status

# Generar reporte de una US
/track-report US-001

# Ver historial de las últimas 5 USs
/track-history --last 5
```

### Ejemplo de Flujo Completo

```bash
# 1. Implementar US
/implement-us US-001

# Claude Code guiará paso a paso:
# ✓ Fase 0: Validación de contexto
# ✓ Fase 1: Generación de escenarios BDD
#   → Genera: tests/features/US-001-nombre.feature
# ✓ Fase 2: Plan de implementación
#   → Genera: docs/plans/US-001-plan.md
# ✓ Fase 3-5: Implementación y tests
#   → Crea código + tests
# ✓ Fase 6-7: Validación BDD y quality gates
#   → Ejecuta pytest, pylint, coverage
# ✓ Fase 8-9: Documentación y reporte
#   → Genera: docs/reports/US-001-report.md

# 2. Ver reporte final
cat docs/reports/US-001-report.md

# 3. Ver métricas de tiempo
/track-report US-001
```

---

## 🎨 Perfiles Disponibles

### PyQt + MVC (`pyqt-mvc`)

Para aplicaciones de escritorio con PyQt6:
- Arquitectura: MVC (Modelo-Vista-Controlador)
- Patrones: Factory, Coordinator
- Testing: pytest-qt, fixtures especializados
- Componentes: Paneles, Displays, Controles

### FastAPI + REST (`fastapi-rest`)

Para APIs REST con FastAPI:
- Arquitectura: Capas (routes, services, repositories)
- Patrones: Dependency Injection, Repository
- Testing: TestClient, fixtures de DB
- Componentes: Endpoints, Services, Models

### Django + MVT (`django-mvt`)

Para aplicaciones web con Django:
- Arquitectura: MVT (Model-View-Template)
- Patrones: Django conventions
- Testing: Django TestCase, fixtures
- Componentes: Models, Views, Templates

### Generic Python (`generic-python`)

Para proyectos Python sin framework específico:
- Arquitectura: Flexible
- Patrones: Configurables
- Testing: pytest estándar
- Componentes: Módulos, clases, funciones

---

## 📚 Documentación

La documentación completa está en el directorio `docs/`:

- **[Guía de Inicio Rápido](docs/getting-started.md)** - Primeros pasos
- **[Instalación Detallada](docs/installation.md)** - Opciones de instalación
- **[Personalización](docs/customization.md)** - Cómo personalizar perfiles y templates
- **[Configuración](docs/configuration.md)** - Referencia completa de configuración
- **[Skill implement-us](docs/skills/implement-us.md)** - Documentación del skill principal
- **[Sistema de Tracking](docs/tracking/tracking-guide.md)** - Guía del tracking de tiempo
- **[Ejemplos por Stack](docs/examples/)** - Tutoriales para cada tecnología

### Archivos Importantes

- **[CLAUDE.md](CLAUDE.md)** - Guía para Claude Code al trabajar en este repositorio
- **[PROJECT_PLAN_claude-dev-kit.md](PROJECT_PLAN_claude-dev-kit.md)** - Plan completo del proyecto
- **[CHANGELOG.md](CHANGELOG.md)** - Historial de versiones (próximamente)

---

## 🏗️ Arquitectura del Framework

```
claude-dev-kit/
├── install/              # Sistema de instalación multiplataforma
│   ├── installer.py      # Instalador Python
│   ├── config.yaml       # Configuración de perfiles
│   └── validate-setup.py # Validador post-instalación
├── skills/               # Definiciones de skills
│   └── implement-us/     # Skill principal
│       ├── skill.md      # Definición completa (leída por Claude)
│       ├── config.json   # Configuración base
│       ├── phases/       # Documentación de fases (0-9)
│       └── customizations/ # Perfiles por stack
├── templates/            # Templates reutilizables
│   ├── bdd/             # Gherkin, pytest-bdd steps
│   ├── planning/        # Planes, ADRs
│   ├── testing/         # Tests, fixtures
│   └── reporting/       # Reportes, retrospectivas
├── tracking/             # Sistema de tracking
│   ├── time_tracker.py  # Core del tracking
│   ├── commands.py      # Comandos /track-*
│   └── models.py        # Modelos de datos
├── docs/                 # Documentación
├── examples/             # Proyectos de ejemplo completos
└── scripts/              # Scripts de utilidad
```

---

## 🧪 Ejemplos

El directorio `examples/` contiene proyectos de ejemplo completos para cada stack:

- **[examples/pyqt-mvc/](examples/pyqt-mvc/)** - Aplicación PyQt con MVC
- **[examples/fastapi-rest/](examples/fastapi-rest/)** - API REST con FastAPI
- **[examples/django-mvt/](examples/django-mvt/)** - Aplicación web Django
- **[examples/generic-python/](examples/generic-python/)** - Proyecto Python genérico

Cada ejemplo incluye:
- Código de aplicación funcional
- Historias de usuario de ejemplo
- Tests completos (unitarios, integración, BDD)
- Configuración del kit instalada

---

## 🛠️ Desarrollo

### Contribuir al Framework

```bash
# 1. Fork y clonar
git clone https://github.com/tu-usuario/claude-dev-kit.git
cd claude-dev-kit

# 2. Crear rama para tu feature
git checkout -b feature/mi-feature

# 3. Hacer cambios y tests
pytest tests/

# 4. Commit siguiendo convención
git commit -m "feat(scope): descripción"

# 5. Push y crear Pull Request
git push origin feature/mi-feature
```

### Convención de Commits

```
<type>(<scope>): <subject>

Types:
- feat: Nueva funcionalidad
- fix: Corrección de bug
- docs: Solo documentación
- refactor: Refactorización
- test: Agregar tests
- chore: Mantenimiento

Ejemplos:
feat(installer): agregar soporte para perfil Django
docs(tracking): documentar comando /track-history
fix(templates): corregir variables en test-unit.py
```

---

## 📊 Estado del Proyecto

**Versión Actual:** Pre-release (v0.1.0-dev)

**Sprint Actual:** Sprint 1 - Setup + Instalación

**Progreso:**
- ✅ Fase 1: Setup Inicial (50% completado)
- ⬜ Fase 2: Sistema de Instalación
- ⬜ Fase 3: Generalización de Skills
- ⬜ Fase 4: Templates
- ⬜ Fase 5: Sistema de Tracking

Ver [gestion/](gestion/) para detalles del progreso y tickets.

---

## 🗺️ Roadmap

### Versión 1.0 (En Desarrollo)

- [x] Estructura base del proyecto
- [x] Sistema de gestión por fases
- [ ] Instalador multiplataforma funcional
- [ ] Skill implement-us generalizado
- [ ] Templates completos para BDD, planning, testing, reporting
- [ ] Sistema de tracking de tiempo
- [ ] Documentación completa
- [ ] Al menos 2 ejemplos funcionales (PyQt, FastAPI)

### Versión 1.1 (Futuro)

- [ ] Skill adicional: `/code-review`
- [ ] Dashboard web de métricas
- [ ] Soporte para TypeScript/JavaScript
- [ ] Más perfiles (Flask, React, Vue)

### Versión 1.2 (Futuro)

- [ ] Integración con Jira (actualizar estado de issues)
- [ ] Integración con GitHub Issues
- [ ] Notificaciones (Slack, email)

### Versión 2.0 (Futuro)

- [ ] Marketplace de skills comunitarios
- [ ] API pública para crear skills
- [ ] Soporte para múltiples lenguajes (Go, Rust, Java)

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor:

1. Lee la [guía de contribución](CONTRIBUTING.md) (próximamente)
2. Revisa los [issues abiertos](https://github.com/vvalotto/claude-dev-kit/issues)
3. Sigue la convención de commits
4. Agrega tests para nuevas funcionalidades
5. Actualiza la documentación según corresponda

---

## 📝 Licencia

Este proyecto está licenciado bajo la licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

```
MIT License

Copyright (c) 2026 Victor Valotto

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 👥 Autor

**Victor Valotto**
- GitHub: [@vvalotto](https://github.com/vvalotto)
- Email: vvalotto@gmail.com

---

## 🙏 Agradecimientos

- Proyecto inspirado en el trabajo con [Claude Code](https://claude.ai/code) de Anthropic
- Metodología BDD basada en [pytest-bdd](https://pytest-bdd.readthedocs.io/)
- Patrones arquitectónicos del proyecto ISSE_Simuladores

---

## 📞 Soporte

- **Issues**: [GitHub Issues](https://github.com/vvalotto/claude-dev-kit/issues)
- **Discusiones**: [GitHub Discussions](https://github.com/vvalotto/claude-dev-kit/discussions)
- **Documentación**: [docs/](docs/)

---

**¿Listo para automatizar tu desarrollo con Claude Code?** 🚀

```bash
git clone https://github.com/vvalotto/claude-dev-kit.git ~/.claude-dev-kit
cd ~/tu-proyecto
python ~/.claude-dev-kit/install/installer.py
```
