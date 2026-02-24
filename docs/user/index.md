# Documentación Claude Dev Kit

**Última Actualización:** 2026-02-24
**Versión:** 1.0.0 (v1.1 en desarrollo)
**Estado:** Estable

---

Bienvenido a la documentación completa del **Claude Dev Kit**, un framework agnóstico de dominio diseñado para asistir la construcción de software con Claude Code.

Este framework proporciona skills reutilizables, templates y herramientas de tracking que automatizan el ciclo de implementación de historias de usuario.

---

## 🎯 ¿Qué es Claude Dev Kit?

Claude Dev Kit es un framework instalable y reutilizable para proyectos Python que:

✅ **Automatiza** la implementación de historias de usuario en 10 fases estructuradas
✅ **Personaliza** el flujo de trabajo para diferentes stacks (PyQt, FastAPI, Flask, Django, etc.)
✅ **Trackea** automáticamente el tiempo de desarrollo por fase y tarea
✅ **Genera** documentación BDD, planes de implementación y reportes
✅ **Valida** calidad con quality gates (Pylint, cobertura, complejidad)

---

## 🚀 Inicio Rápido

¿Primera vez? Comienza aquí:

1. **[Guía de Inicio Rápido](UserGettingStarted)** - Tu primera experiencia en <15 minutos
   Aprende a instalar el framework e implementar tu primera historia de usuario.

2. **[Instalación Detallada](UserInstallation)** - Setup completo paso a paso
   Instalación interactiva y no interactiva, selección de perfil, validación.

3. **[Skill implement-us](UserSkillsImplementUs)** - El skill principal
   Guía completa del skill que automatiza la implementación de historias de usuario.

---

## 📚 Documentación por Categoría

### Para Usuarios del Framework

Si eres desarrollador usando el framework en tu proyecto:

| Documento | Descripción | Estado |
|-----------|-------------|--------|
| **[Getting Started](UserGettingStarted)** | Guía de inicio rápido (<15 min) | ✅ Completo |
| **[Instalación](UserInstallation)** | Instalación detallada con validación | ✅ Completo |
| **[Personalización](UserCustomization)** | Adapta el framework a tu stack | ✅ Completo |
| **[Configuración](UserConfiguration)** | Referencia completa de opciones | ✅ Completo |

### Skills y Herramientas

Documentación de los skills disponibles:

| Documento | Descripción | Estado |
|-----------|-------------|--------|
| **[Skill implement-us](UserSkillsImplementUs)** | Implementación automatizada de US | ✅ Completo |
| **[Tracking - Guía de Usuario](UserTrackingUserGuide)** | Sistema de tracking de tiempo | ✅ Completo |
| **[Tracking - Ejemplos](UserTrackingExamples)** | Ejemplos de uso del tracking | ✅ Completo |

### Para Desarrolladores del Framework

Si quieres contribuir o crear extensiones:

| Documento | Descripción | Estado |
|-----------|-------------|--------|
| **[Creando Skills](DeveloperContributingCreatingSkills)** | Guía para crear skills custom | ✅ Completo |
| **[Sistema de Templates](DeveloperArchitectureTemplateSystem)** | Variables, snippets y personalización | ✅ Completo |
| **[Tracking - Arquitectura](DeveloperArchitectureTracking)** | Diseño técnico del sistema | ✅ Completo |

### Tutoriales por Stack Tecnológico

Proyectos ejemplo completos end-to-end:

| Tutorial | Stack | Estado |
|----------|-------|--------|
| **[Proyecto PyQt-MVC](ExamplesPyqtProject)** | PyQt6 + MVC | ✅ Completado |
| **[Proyecto FastAPI-REST](ExamplesFastapiProject)** | FastAPI + REST API | ✅ Completado |
| **[Proyecto Flask-REST](ExamplesFlaskRestApiProject)** | Flask + REST API | ✅ Completado |
| **[Proyecto Flask-WebApp](ExamplesFlaskWebappProject)** | Flask + Templates | ✅ Completado |
| **[Proyecto Python Genérico](ExamplesGenericPython)** | Python sin framework | ✅ Completado |

---

## 🗺️ Rutas de Aprendizaje Sugeridas

Elige tu camino según tu objetivo:

### 👨‍💻 Nuevo Usuario - Primera Instalación

**Objetivo:** Instalar el framework y ejecutar tu primera historia de usuario

1. [Guía de Inicio Rápido](UserGettingStarted) - 15 minutos
2. [Instalación Detallada](UserInstallation) - 10 minutos
3. [Skill implement-us](UserSkillsImplementUs) - 20 minutos
4. [Tracking - Guía de Usuario](UserTrackingUserGuide) - 10 minutos

**Tiempo total:** ~1 hora
**Resultado:** Framework instalado + Primera US implementada

---

### 🔧 Usuario Avanzado - Personalización

**Objetivo:** Adaptar el framework a tu stack específico

1. [Personalización](UserCustomization) - Sistema de perfiles
2. [Configuración](UserConfiguration) - Opciones avanzadas
3. [Sistema de Templates](DeveloperArchitectureTemplateSystem) - Variables y snippets
4. [Tutorial específico](examples) - Según tu stack

**Tiempo total:** ~2 horas
**Resultado:** Framework personalizado para tu proyecto

---

### 🏗️ Contributor - Extensibilidad

**Objetivo:** Crear skills custom o contribuir al framework

1. [Creando Skills](DeveloperContributingCreatingSkills) - Anatomía de un skill
2. [Sistema de Templates](DeveloperArchitectureTemplateSystem) - Sistema de variables
3. [Tracking - Arquitectura](DeveloperArchitectureTracking) - Integración con tracking
4. [Documentación Interna](DeveloperArchitectureTemplateSystem) - Decisiones arquitectónicas

**Tiempo total:** ~3 horas
**Resultado:** Skill custom funcional o contribución al framework

---

### 🎓 Por Stack Tecnológico

Rutas específicas según tu tecnología:

#### PyQt Desktop Apps
1. [Instalación](UserInstallation) - Seleccionar perfil `pyqt-mvc`
2. [Tutorial PyQt-MVC](ExamplesPyqtProject) - Proyecto completo
3. [Personalización](UserCustomization) - Ajustes específicos PyQt

#### FastAPI REST APIs
1. [Instalación](UserInstallation) - Seleccionar perfil `fastapi-rest`
2. [Tutorial FastAPI](ExamplesFastapiProject) - API completa
3. [Configuración](UserConfiguration) - Quality gates para APIs

#### Flask Applications
1. [Instalación](UserInstallation) - Seleccionar `flask-rest` o `flask-webapp`
2. [Tutorial Flask REST](ExamplesFlaskRestApiProject) o [Flask WebApp](ExamplesFlaskWebappProject)
3. [Personalización](UserCustomization) - Blueprints y templates Flask

#### Django Projects
1. [Instalación](UserInstallation) - Seleccionar perfil `generic-python`
2. [Personalización](UserCustomization) - Crear perfil Django custom
3. [Creando Skills](DeveloperContributingCreatingSkills) - Crear skill adaptado a Django

---

## 📖 Conceptos Clave

### El Skill implement-us

El skill principal del framework que guía paso a paso la implementación de historias de usuario a través de **10 fases**:

0. **Validación de Contexto** - Verifica prerequisitos
1. **Generación BDD** - Escenarios Gherkin
2. **Plan de Implementación** - Desglose en tareas
3. **Implementación** - Código guiado por tareas
4. **Tests Unitarios** - Cobertura por componente
5. **Tests de Integración** - End-to-end testing
6. **Validación BDD** - Ejecutar escenarios
7. **Quality Gates** - Pylint, cobertura, complejidad
8. **Documentación** - Docstrings y comentarios
9. **Reporte Final** - Métricas y resumen

**Ver:** [Documentación completa del skill](UserSkillsImplementUs)

### Sistema de Perfiles

El framework soporta múltiples stacks tecnológicos a través de **perfiles de personalización**:

- **pyqt-mvc** - Aplicaciones desktop con PyQt6 + arquitectura MVC
- **fastapi-rest** - APIs REST async con FastAPI
- **flask-rest** - APIs REST con Flask
- **flask-webapp** - Aplicaciones web fullstack con Flask
- **generic-python** - Proyectos Python sin framework específico

Cada perfil personaliza:
- Patrones arquitectónicos
- Frameworks de testing
- Estructura de componentes
- Quality gates y umbrales

**Ver:** [Guía de Personalización](UserCustomization)

### Sistema de Tracking

Tracking automático de tiempo por fase y tarea durante la implementación:

- ⏱️ **Tracking automático** - Inicio/fin de fase sin intervención
- ⏸️ **Pausas manuales** - `/track-pause` con razón opcional
- ▶️ **Reanudación** - `/track-resume` desde pausa
- 📊 **Reportes** - `/track-status`, `/track-report`, `/track-history`
- 📈 **Varianza** - Tiempo estimado vs. real por tarea

**Ver:** [Tracking - Guía de Usuario](UserTrackingUserGuide)

### Sistema de Templates

Templates parametrizados con variables y snippets:

- **Variables:** `{US_ID}`, `{COMPONENT_TYPE}`, `{ARCHITECTURE_PATTERN}`, etc.
- **Snippets:** Bloques de código multi-línea por perfil
- **Templates:** BDD scenarios, implementation plans, test units, reports

**Ver:** [Sistema de Templates](DeveloperArchitectureTemplateSystem)

---

## 🔗 Recursos Adicionales

### Proyecto en GitHub

- [Repositorio Principal](https://github.com/vvalotto/claude-dev-kit)
- [Issues y Feature Requests](https://github.com/vvalotto/claude-dev-kit/issues)
- [Pull Requests](https://github.com/vvalotto/claude-dev-kit/pulls)
- [Releases](https://github.com/vvalotto/claude-dev-kit/releases)

### Documentación del Proyecto

- [README Principal](https://github.com/vvalotto/claude-dev-kit) - Visión general del proyecto
- [Plan del Proyecto](https://github.com/vvalotto/claude-dev-kit/blob/main/PROJECT_PLAN_claude-dev-kit.md) - Roadmap completo
- [Gestión de Tareas](https://github.com/vvalotto/claude-dev-kit/tree/main/gestion) - Progreso y planificación

### Soporte y Comunidad

- [Changelog](https://github.com/vvalotto/claude-dev-kit/blob/main/CHANGELOG.md) - Historial de versiones
- Contributing - Guía de contribución (pendiente)
- [License](https://github.com/vvalotto/claude-dev-kit/blob/main/LICENSE) - Licencia MIT (pendiente)

---

## ❓ FAQ - Preguntas Frecuentes

### ¿Qué necesito para usar el framework?

- Python 3.9 o superior
- Claude Code CLI instalado
- Proyecto Python existente (opcional)
- Git instalado

### ¿Funciona con mi stack tecnológico?

El framework soporta 5 perfiles predefinidos (PyQt, FastAPI, Flask REST, Flask WebApp, Python genérico) y permite crear perfiles custom para cualquier stack.

**Ver:** [Personalización - Crear Perfil Custom](UserCustomization#crear-perfil-custom)

### ¿Puedo usar solo parte del framework?

Sí, los skills son independientes. Puedes usar:
- Solo el sistema de tracking
- Solo los templates
- Solo el skill implement-us
- Cualquier combinación

### ¿Cómo actualizo el framework?

```bash
cd ~/.claude-dev-kit
git pull origin main
python install/installer.py --upgrade
```

**Ver:** [Instalación - Actualización](UserInstallation#actualización)

### ¿Dónde reporto bugs o sugiero features?

Usa GitHub Issues:
- **Bug:** [Crear Issue](https://github.com/vvalotto/claude-dev-kit/issues/New?template=bug_report)
- **Feature:** [Crear Issue](https://github.com/vvalotto/claude-dev-kit/issues/New?template=feature_request)

---


---

## 📋 Leyenda de Estados

| Emoji | Estado | Descripción |
|-------|--------|-------------|
| ✅ | Completo | Documento finalizado y validado |
| 🔄 | En Progreso | Actualmente en desarrollo |
| ⚠️ | Pendiente | Planificado pero no iniciado |

---

**¿Listo para comenzar?** → [Guía de Inicio Rápido](UserGettingStarted)
