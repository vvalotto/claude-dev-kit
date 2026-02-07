# CLAUDE.md

Este archivo proporciona orientación a Claude Code (claude.ai/code) al trabajar con código en este repositorio.

---

## Visión General del Proyecto

**Claude Dev Kit** es un framework de desarrollo agnóstico de dominio diseñado para asistir la construcción de software con Claude Code. Proporciona skills reutilizables, templates y herramientas de tracking que automatizan el ciclo de implementación de historias de usuario.

**Estado Actual:** Fase de configuración inicial. El proyecto contiene documentos de planificación y archivos migrados del proyecto fuente (ISSE_Simuladores) en el directorio `_work/`. Aún no se ha creado la estructura de código de producción.

**Objetivo Principal:** Crear un framework instalable y reutilizable para proyectos Python que pueda personalizarse para diferentes stacks tecnológicos (PyQt, FastAPI, Django, etc.).

---

## Estructura del Repositorio

```
claude-dev-kitc/
├── PROJECT_PLAN_claude-dev-kit.md  # Plan completo del proyecto y roadmap
├── _work/                          # Directorio de trabajo con archivos migrados
│   ├── QUICK_SUMMARY.md           # Resumen rápido del contenido migrado
│   ├── MIGRATION_NOTES.md         # Notas detalladas de migración
│   └── from-simapp/               # Archivos fuente de simapp_termostato
│       ├── skills/                # Definición del skill implement-us
│       ├── templates/             # Templates BDD, planning, testing
│       ├── tracking/              # Sistema de tracking de tiempo (listo para usar)
│       └── docs/                  # Documentación de referencia
```

**Archivos Clave para Leer Primero:**
- `PROJECT_PLAN_claude-dev-kit.md` - Arquitectura completa y plan de implementación
- `_work/QUICK_SUMMARY.md` - Resumen rápido de lo que hay que hacer
- `_work/MIGRATION_NOTES.md` - Notas detalladas sobre cómo generalizar componentes

---

## Arquitectura Planificada (Estado Objetivo)

La estructura final será:

```
claude-dev-kit/
├── install/              # Sistema de instalación
│   ├── installer.py      # Instalador multiplataforma
│   ├── config.yaml       # Configuración de instalación
│   └── validate-setup.py # Validador post-instalación
├── skills/               # Definiciones de skills
│   └── implement-us/     # Skill principal para implementar historias de usuario
│       ├── skill.md      # Definición completa del skill
│       ├── config.json   # Configuración base
│       ├── phases/       # Documentación de cada fase (0-9)
│       └── customizations/ # Perfiles específicos por stack
│           ├── pyqt-mvc.json
│           ├── fastapi-rest.json
│           ├── django-mvt.json
│           └── generic-python.json
├── templates/            # Templates reutilizables
│   ├── bdd/             # Escenarios Gherkin, steps pytest-bdd
│   ├── planning/        # Planes de implementación, ADRs
│   ├── testing/         # Templates de tests unitarios e integración
│   └── reporting/       # Reportes de implementación
├── tracking/             # Sistema de tracking de tiempo
│   ├── time_tracker.py  # Funcionalidad core de tracking
│   ├── commands.py      # Comandos /track-*
│   └── models.py        # Modelos de datos (Task, Phase, Pause)
├── docs/                 # Documentación del framework
├── examples/             # Proyectos de ejemplo completos
└── scripts/              # Scripts de utilidad
```

---

## Flujo de Trabajo de Desarrollo

### Fase Actual: Sprint 1 - Configuración Inicial

Seguir el plan de implementación en `PROJECT_PLAN_claude-dev-kit.md` Sección 5.

**Próximos Pasos Inmediatos:**

1. **Crear Estructura de Directorios Base**
   ```bash
   mkdir -p install skills/implement-us/{phases,customizations} templates/{bdd,planning,testing,reporting} tracking docs examples scripts tests
   ```

2. **Migrar Componentes Listos para Usar**
   - Copiar sistema de tracking de `_work/from-simapp/tracking/` → `tracking/`
   - Estos archivos son 100% genéricos y no necesitan modificaciones

3. **Generalizar Skills**
   - Adaptar `_work/from-simapp/skills/implement-us.md`
   - Remover referencias específicas a MVC/PyQt
   - Reemplazar con variables: `{ARCHITECTURE_PATTERN}`, `{COMPONENT_TYPE}`
   - Crear `config.json` base con valores por defecto genéricos
   - Crear perfiles específicos por stack en `customizations/`

4. **Generalizar Templates**
   - Adaptar templates de `_work/from-simapp/templates/`
   - Reemplazar referencias específicas con variables genéricas
   - `bdd-scenario.feature` ya es mayormente genérico
   - Generalizar `implementation-plan.md`, `implementation-report.md`, `test-unit.py`

5. **Crear Sistema de Instalación**
   - Desarrollar `install/installer.py` con selección interactiva de perfil
   - Crear `install/config.yaml` con perfiles y reglas de validación
   - Desarrollar `scripts/validate-setup.py` para validación post-instalación

### Al Crear Nuevos Archivos

- **Skills**: Deben estar en formato Markdown, seguir la estructura en `_work/from-simapp/skills/implement-us.md`
- **Templates**: Usar sintaxis `{VARIABLE_NAME}` para placeholders
- **Código Python**: Seguir patrones del sistema de tracking (dataclasses, type hints, docstrings)
- **Configuración**: Usar JSON para configs de skills, YAML para config del instalador

---

## Conceptos Clave

### 1. Mecanismo de Instalación

El instalador copia el framework en el proyecto del usuario bajo `.claude/`:

```
proyecto-usuario/
├── .claude/              # Creado por el instalador
│   ├── skills/
│   ├── templates/
│   ├── tracking/
│   └── config.json
└── CLAUDE.md            # Generado si no existe
```

**Modos de Instalación:**
- Interactivo: Pregunta al usuario para seleccionar perfil (PyQt, FastAPI, Django, Genérico)
- No interactivo: `python installer.py --profile pyqt-mvc --yes`
- Validación: Valida automáticamente la instalación después de completarla

### 2. Sistema de Perfiles

Los perfiles personalizan el framework para stacks tecnológicos específicos:

- **pyqt-mvc**: PyQt6 + arquitectura MVC + patrones Factory/Coordinator
- **fastapi-rest**: FastAPI + APIs REST + arquitectura en capas
- **django-mvt**: Django + patrón MVT + convenciones Django
- **generic-python**: Proyectos Python genéricos sin framework específico

Cada perfil proporciona:
- Configuración personalizada (`customizations/{profile}.json`)
- Configuración del framework de testing específico del stack
- Definiciones de patrones arquitectónicos
- Templates de estructura de componentes

### 3. El Skill implement-us

El skill principal que guía paso a paso la implementación de historias de usuario:

**9 Fases:**
0. Validación de Contexto
1. Generación de Escenarios BDD
2. Generación de Plan de Implementación
3. Implementación
4. Tests Unitarios
5. Tests de Integración
6. Validación BDD
7. Quality Gates (pylint, complejidad, cobertura)
8. Documentación
9. Reporte Final

Cada fase incluye:
- Tracking de tiempo (inicio/fin automático)
- Checkpoints opcionales de aprobación del usuario
- Generación de output basada en templates
- Desglose de tareas con estimaciones

### 4. Sistema de Tracking de Tiempo

Ubicado en `_work/from-simapp/tracking/` (listo para migrar):

**Características:**
- Tracking automático de tiempo por fase y tarea
- Pausa/reanudación manual con tracking de razón (`/track-pause`, `/track-resume`)
- Reportes de estado en tiempo real (`/track-status`)
- Reportes históricos por US o producto (`/track-report`, `/track-history`)
- Tracking de varianza (tiempo estimado vs. real)

**Modelos de Datos:**
- `Task`: Tarea individual dentro de una fase
- `Phase`: Una de las 9 fases de implementación
- `Pause`: Períodos de pausa manual con razón

### 5. Sistema de Templates

Los templates usan placeholders `{VARIABLE_NAME}` que se reemplazan durante la generación:

**Variables Comunes:**
- `{US_ID}`: Identificador de historia de usuario (ej. US-001)
- `{US_TITLE}`: Título de la historia de usuario
- `{ARCHITECTURE_PATTERN}`: mvc, mvt, layered, etc.
- `{COMPONENT_TYPE}`: Panel, View, Controller, Service, etc.
- `{COMPONENT_PATH}`: Ruta del archivo para el componente
- `{TEST_FRAMEWORK}`: pytest, unittest, etc.

---

## Estándares de Calidad

### Quality Gates de Código (del plan)

Al implementar el framework mismo:
- **Pylint**: Puntaje mínimo 8.0/10
- **Complejidad Ciclomática**: Máximo 10 por función
- **Índice de Mantenibilidad**: Mínimo 20
- **Cobertura de Tests**: Mínimo 95% para el sistema de tracking

### Convención de Commits

```
<type>(<scope>): <subject>

Types:
- feat: Nueva funcionalidad
- fix: Corrección de bug
- docs: Solo documentación
- refactor: Refactorización de código
- test: Agregar tests
- chore: Mantenimiento

Ejemplos:
feat(installer): agregar soporte para perfil Django
docs(tracking): documentar comando /track-history
fix(templates): corregir variables en test-unit.py
```

### Estrategia de Branching

```
main                    # Releases de producción
  └── develop           # Desarrollo activo
       ├── feature/xxx  # Nuevas funcionalidades
       ├── fix/xxx      # Correcciones de bugs
       └── docs/xxx     # Documentación
```

Rama actual: `inicializacion-proyecto` (rama de configuración inicial)

---

## Comandos Esenciales

### Instalación (cuando esté implementado)

```bash
# Clonar kit en ubicación global
git clone https://github.com/vvalotto/claude-dev-kit.git ~/.claude-dev-kit

# Navegar al proyecto destino
cd ~/mi-proyecto-python

# Ejecutar instalador (interactivo)
python ~/.claude-dev-kit/install/installer.py

# O no interactivo con perfil
python ~/.claude-dev-kit/install/installer.py --profile pyqt-mvc --yes

# Validar instalación
python ~/.claude-dev-kit/scripts/validate-setup.py
```

### Desarrollo

```bash
# Instalar dependencias del framework (cuando exista requirements.txt)
pip install -r requirements.txt

# Ejecutar tests del framework (cuando tests/ esté implementado)
pytest tests/

# Validar script de instalación
python scripts/validate-setup.py
```

### Usando el Skill (después de instalación en un proyecto)

```bash
# Implementar una historia de usuario
/implement-us US-001

# Con especificación de producto
/implement-us US-001 --producto mi_producto

# Saltar generación BDD
/implement-us US-001 --skip-bdd
```

### Comandos de Time Tracking (después de implementación)

```bash
/track-pause [razón]          # Pausar tracking actual
/track-resume                 # Reanudar tracking
/track-status                 # Mostrar estado actual
/track-report [us_id]         # Generar reporte para US
/track-history [--last N]     # Mostrar historial
```

---

## Guías de Migración

Al generalizar componentes de `_work/from-simapp/`:

### Generalización de Skills

**Remover:**
- Referencias específicas a "MVC", "Factory", "Coordinator"
- Menciones específicas de PyQt6
- Rutas hardcodeadas a simapp_termostato
- Referencias a "Panel", "Display", componentes específicos

**Reemplazar con:**
- Variables: `{ARCHITECTURE_PATTERN}`, `{COMPONENT_TYPE}`, `{COMPONENT_PATH}`
- Instrucciones para leer configuración del perfil
- Ejemplos genéricos o múltiples ejemplos por stack

**Ejemplo:**

Antes:
```markdown
### 1. Panel Display (MVC)
- [ ] app/presentacion/paneles/display/modelo.py (10 min)
```

Después:
```markdown
### 1. {COMPONENT_NAME} ({ARCHITECTURE_PATTERN})
- [ ] {COMPONENT_PATH}/modelo.py (10 min)

> Nota: La estructura de componentes se define en el perfil seleccionado.
> Ver `.claude/skills/implement-us/config.json` para personalizar.
```

### Generalización de Templates

Reemplazar suposiciones hardcodeadas:
- `{TEST_FRAMEWORK}` en lugar de "pytest-qt"
- `{BASE_CLASS}` en lugar de "ModeloBase"
- `{COMPONENT_TYPE}` en lugar de "Panel"

### Archivos de Configuración

Convertir `implement-us-config.json` en:
1. **Config base** (`skills/implement-us/config.json`): Valores por defecto genéricos
2. **Configs de perfil** (`skills/implement-us/customizations/{profile}.json`): Overrides específicos del stack

El instalador fusiona base + perfil al instalar.

---

## Estrategia de Testing

### Tests del Framework

```
tests/
├── test_installer.py      # Test del proceso de instalación
├── test_tracking.py       # Test del sistema de tracking de tiempo
├── test_config_merge.py   # Test de fusión de configs
└── conftest.py           # Fixtures compartidos
```

### Tests de Proyectos de Ejemplo

Cada ejemplo en `examples/{stack}/` debe incluir:
- Suite de tests completa demostrando el framework
- Escenarios BDD
- Tests unitarios y de integración
- Validación de quality gates

---

## Estructura de Documentación

Toda la documentación va en `docs/`:

- `getting-started.md` - Guía de inicio rápido para usuarios
- `installation.md` - Instrucciones de instalación detalladas
- `customization.md` - Cómo personalizar perfiles y templates
- `configuration.md` - Referencia completa de configuración
- `skills/implement-us.md` - Documentación completa del skill
- `tracking/tracking-guide.md` - Guía de tracking de tiempo
- `examples/{stack}.md` - Tutorial para cada stack

---

## Notas Importantes para Claude Code

1. **Este es un proyecto de framework, no una aplicación.** El código que escribimos será usado POR otros proyectos, no se ejecuta directamente.

2. **El directorio `_work/` contiene material fuente** que necesita ser adaptado, no código de producción. Es un área de trabajo/planificación.

3. **Comenzar con la migración del sistema de tracking** ya que es genérico y no necesita cambios. Esto proporciona logros tempranos.

4. **No crear código de implementación sin consultar el plan.** Todo sigue la estructura en `PROJECT_PLAN_claude-dev-kit.md`.

5. **El sistema de perfiles es clave.** El mismo skill/template debe funcionar para PyQt, FastAPI, Django, etc. Pensar en términos de variables y overrides.

6. **Los templates usan reemplazo simple de strings** con sintaxis `{VARIABLE}`, no motores de templating complejos.

7. **El instalador es crítico.** Los usuarios necesitan una experiencia de instalación fluida y guiada con validación.

8. **Documentar sobre la marcha.** Como esto es un framework, la documentación es tan importante como el código.

---

## Recursos

- **Plan del Proyecto**: `PROJECT_PLAN_claude-dev-kit.md` - Roadmap completo y arquitectura
- **Resumen Rápido**: `_work/QUICK_SUMMARY.md` - Qué hay que hacer
- **Notas de Migración**: `_work/MIGRATION_NOTES.md` - Cómo generalizar componentes
- **Skill Fuente**: `_work/from-simapp/skills/implement-us.md` - Implementación de referencia
- **Tracking Fuente**: `_work/from-simapp/tracking/*.py` - Sistema de tracking listo para usar

---

## Sprint Actual: Sprint 1 - Setup + Instalación (Semana 1)

**Objetivos:**
- ✅ Crear estructura de directorios base
- ✅ Copiar sistema de tracking (ya genérico)
- ⬜ Desarrollar sistema de instalación (installer.py, config.yaml, validate-setup.py)
- ⬜ Crear estructura de documentación inicial

**Entregable:** Instalador funcional que pueda desplegar el kit en un proyecto

---

**Última Actualización:** 2026-02-07
