# Plan de Proyecto: Claude Dev Kit

**Versión:** 1.0
**Fecha:** 2026-02-07
**Autor:** Victor Valotto
**Estado:** En Ejecución

> ⚠️ **Nota sobre Progreso:** Este documento describe la arquitectura y plan original del proyecto.
> Para el **progreso actualizado** y estado de tickets, ver `gestion/README.md`
>
> **Estado actual:** Sprint 3 - Fase 6 (Documentación)
> - ✅ Fases 1-5 completadas (100%)
> - 🔄 Fase 6 en planificación
> - ⬜ Fases 7-9 pendientes

---

## 1. Resumen Ejecutivo

### 1.1 Propósito del Proyecto

**Claude Dev Kit** es un framework de desarrollo agnóstico de dominio para asistir la construcción de software con Claude Code. Proporciona skills, templates y herramientas de tracking reutilizables que automatizan el ciclo de implementación de historias de usuario.

### 1.2 Objetivos

- **Objetivo 1:** Crear un framework instalable y reutilizable para cualquier proyecto Python
- **Objetivo 2:** Generalizar skills y templates del proyecto ISSE_Simuladores
- **Objetivo 3:** Proporcionar sistema de tracking de tiempo independiente del dominio
- **Objetivo 4:** Soportar personalización por tipo de proyecto (PyQt, FastAPI, Django, etc.)
- **Objetivo 5:** Distribuir vía GitHub como repositorio público/privado

### 1.3 Alcance

**En Scope:**
- Skill `implement-us` generalizado
- Sistema de tracking de tiempo (time_tracker + commands)
- Templates BDD, testing, planning, reporting
- Mecanismo de instalación automatizado
- Documentación completa
- Ejemplos por stack tecnológico

**Out of Scope (Versión 1.0):**
- Integración con Jira/GitHub Issues
- Dashboard web de métricas
- Skills adicionales (code-review, refactor-legacy)
- Soporte para lenguajes no-Python

### 1.4 Stakeholders

- **Victor Valotto:** Product Owner, Developer
- **Claude Code:** Runtime de ejecución de skills
- **Usuarios finales:** Desarrolladores usando Claude Code en proyectos Python

---

## 2. Arquitectura del Proyecto

### 2.1 Estructura de Directorios

```
claude-dev-kit/
│
├── README.md                      # Documentación principal del proyecto
├── LICENSE                        # Licencia MIT
├── .gitignore                     # Exclusiones de Git
├── CHANGELOG.md                   # Historial de versiones
├── PROJECT_PLAN.md                # Este documento (incluir en repo)
│
├── install/                       # Sistema de instalación
│   ├── install.sh                 # Instalador Unix/macOS
│   ├── install.ps1                # Instalador Windows PowerShell
│   ├── installer.py               # Instalador Python multiplataforma
│   ├── config.yaml                # Configuración del instalador
│   └── README.md                  # Documentación de instalación
│
├── skills/                        # Definición de skills
│   ├── implement-us/
│   │   ├── skill.md               # Definición completa del skill
│   │   ├── config.json            # Configuración base
│   │   ├── phases/                # Documentación de fases
│   │   │   ├── phase-00-validation.md
│   │   │   ├── phase-01-bdd.md
│   │   │   ├── phase-02-planning.md
│   │   │   ├── phase-03-implementation.md
│   │   │   ├── phase-04-unit-tests.md
│   │   │   ├── phase-05-integration-tests.md
│   │   │   ├── phase-06-bdd-validation.md
│   │   │   ├── phase-07-quality-gates.md
│   │   │   ├── phase-08-documentation.md
│   │   │   └── phase-09-final-report.md
│   │   ├── customizations/        # Perfiles por stack tecnológico
│   │   │   ├── pyqt-mvc.json      # Configuración para PyQt + MVC
│   │   │   ├── fastapi-rest.json  # Configuración para FastAPI
│   │   │   ├── django-mvt.json    # Configuración para Django
│   │   │   └── generic-python.json# Configuración genérica
│   │   └── README.md
│   │
│   └── README.md                  # Catálogo de skills (futuro)
│
├── templates/                     # Templates reutilizables
│   ├── bdd/
│   │   ├── scenario.feature       # Template escenarios Gherkin
│   │   ├── steps.py               # Template steps pytest-bdd
│   │   └── README.md
│   ├── planning/
│   │   ├── implementation-plan.md # Plan de implementación de US
│   │   ├── sprint-plan.md         # Plan de sprint
│   │   ├── architecture-decision.md # ADR template
│   │   └── README.md
│   ├── testing/
│   │   ├── test-unit.py           # Template test unitario
│   │   ├── test-integration.py    # Template test integración
│   │   ├── conftest.py            # Template fixtures pytest
│   │   └── README.md
│   ├── reporting/
│   │   ├── implementation-report.md # Reporte de US completada
│   │   ├── sprint-retrospective.md  # Retrospectiva de sprint
│   │   ├── quality-report.md        # Reporte de métricas
│   │   └── README.md
│   └── README.md                  # Catálogo de templates
│
├── tracking/                      # Sistema de tracking de tiempo
│   ├── __init__.py
│   ├── time_tracker.py            # Core del tracking
│   ├── commands.py                # Comandos /track-*
│   ├── models.py                  # Dataclasses (Task, Phase, Pause)
│   ├── utils.py                   # Utilidades de formateo
│   └── README.md                  # Documentación del tracking
│
├── docs/                          # Documentación del framework
│   ├── index.md                   # Índice de documentación
│   ├── getting-started.md         # Guía de inicio rápido
│   ├── installation.md            # Guía de instalación detallada
│   ├── customization.md           # Cómo personalizar el kit
│   ├── configuration.md           # Referencia de configuración
│   ├── skills/
│   │   ├── implement-us.md        # Documentación completa
│   │   └── creating-skills.md     # Cómo crear nuevos skills
│   ├── templates/
│   │   └── template-guide.md      # Guía de templates
│   ├── tracking/
│   │   └── tracking-guide.md      # Guía del sistema de tracking
│   └── examples/
│       ├── pyqt-project.md        # Ejemplo PyQt
│       ├── fastapi-project.md     # Ejemplo FastAPI
│       ├── django-project.md      # Ejemplo Django
│       └── generic-python.md      # Ejemplo genérico
│
├── examples/                      # Proyectos de ejemplo completos
│   ├── pyqt-mvc/
│   │   ├── .claude/               # Configuración del kit
│   │   ├── app/                   # Código de ejemplo
│   │   ├── tests/                 # Tests de ejemplo
│   │   ├── README.md
│   │   └── requirements.txt
│   ├── fastapi-rest/
│   │   ├── .claude/
│   │   ├── app/
│   │   ├── tests/
│   │   ├── README.md
│   │   └── requirements.txt
│   ├── django-mvt/
│   │   ├── .claude/
│   │   ├── myproject/
│   │   ├── tests/
│   │   ├── README.md
│   │   └── requirements.txt
│   └── generic-python/
│       ├── .claude/
│       ├── src/
│       ├── tests/
│       ├── README.md
│       └── requirements.txt
│
├── scripts/                       # Scripts de utilidad
│   ├── validate-setup.py          # Valida instalación del kit
│   ├── migrate-version.py         # Migración entre versiones
│   ├── generate-docs.py           # Genera documentación
│   └── README.md
│
└── tests/                         # Tests del framework mismo
    ├── test_installer.py
    ├── test_tracking.py
    └── conftest.py
```

### 2.2 Componentes Principales

#### 2.2.1 Sistema de Instalación (`install/`)

**Responsabilidad:** Desplegar el kit en proyectos de usuario

**Archivos:**
- `installer.py`: Instalador Python multiplataforma (preferido)
- `install.sh`: Script Bash para Unix/macOS (alternativo)
- `install.ps1`: Script PowerShell para Windows (alternativo)
- `config.yaml`: Configuración de rutas y perfiles

**Funcionalidad:**
1. Detectar si el proyecto ya tiene `.claude/`
2. Seleccionar perfil de instalación (interactivo o vía flag)
3. Copiar skills, templates, tracking al proyecto
4. Generar configuración personalizada
5. Crear `CLAUDE.md` base si no existe
6. Validar instalación

#### 2.2.2 Skills (`skills/`)

**Responsabilidad:** Definición de skills de Claude Code

**Skill Principal: `implement-us`**
- Implementación asistida de Historias de Usuario
- 9 fases documentadas
- Perfiles de customización por stack

**Estructura del skill:**
```
skills/implement-us/
├── skill.md              # Definición completa (leída por Claude)
├── config.json           # Configuración base
├── phases/               # Documentación de cada fase
│   └── phase-XX-name.md
└── customizations/       # Perfiles por stack
    └── {stack}.json
```

#### 2.2.3 Templates (`templates/`)

**Responsabilidad:** Plantillas reutilizables para generación de código/docs

**Categorías:**
- **BDD:** Escenarios Gherkin, steps pytest-bdd
- **Planning:** Planes de implementación, ADRs
- **Testing:** Tests unitarios, integración, fixtures
- **Reporting:** Reportes de implementación, retrospectivas

**Formato:** Markdown con variables `{VAR_NAME}`

#### 2.2.4 Tracking (`tracking/`)

**Responsabilidad:** Sistema de tracking de tiempo para USs

**Componentes:**
- `time_tracker.py`: Clase `TimeTracker` (core)
- `commands.py`: Funciones para comandos `/track-*`
- `models.py`: Dataclasses `Task`, `Phase`, `Pause`
- `utils.py`: Formateo de duración, reportes

**Comandos soportados:**
- `/track-pause [razón]`
- `/track-resume`
- `/track-status`
- `/track-report [us_id]`
- `/track-history [--last N] [--producto X]`

#### 2.2.5 Documentación (`docs/`)

**Responsabilidad:** Documentación del framework

**Estructura:**
- **Inicio rápido:** `getting-started.md`
- **Instalación:** `installation.md`
- **Personalización:** `customization.md`, `configuration.md`
- **Skills:** Documentación de cada skill
- **Templates:** Guía de uso de templates
- **Tracking:** Guía del sistema de tracking
- **Ejemplos:** Tutoriales por stack

#### 2.2.6 Ejemplos (`examples/`)

**Responsabilidad:** Proyectos de ejemplo funcionales

**Cada ejemplo incluye:**
- Configuración `.claude/` completa
- Código de aplicación ejemplo
- Tests de ejemplo
- Historias de Usuario de ejemplo
- README con instrucciones

---

## 3. Administración de Configuración

### 3.1 Estructura Inicial del Proyecto

El proyecto se inicializará con la siguiente estructura base:

```
claude-dev-kit/
├── README.md
├── LICENSE
├── .gitignore
├── CHANGELOG.md
├── PROJECT_PLAN.md
├── install/
├── skills/
├── templates/
├── tracking/
├── docs/
├── examples/
├── scripts/
└── tests/
```

### 3.2 Ítems de Configuración (CI - Configuration Items)

| ID | Nombre | Tipo | Ubicación | Descripción | Versionado |
|----|--------|------|-----------|-------------|------------|
| CI-001 | Instalador Python | Script | `install/installer.py` | Instalador multiplataforma | Sí |
| CI-002 | Config Instalador | YAML | `install/config.yaml` | Configuración de instalación | Sí |
| CI-003 | Skill implement-us | Markdown | `skills/implement-us/skill.md` | Definición del skill | Sí |
| CI-004 | Config implement-us | JSON | `skills/implement-us/config.json` | Configuración base | Sí |
| CI-005 | Perfiles Stack | JSON | `skills/implement-us/customizations/*.json` | Perfiles por stack | Sí |
| CI-006 | Templates BDD | Markdown | `templates/bdd/*.feature` | Templates Gherkin | Sí |
| CI-007 | Templates Planning | Markdown | `templates/planning/*.md` | Templates planificación | Sí |
| CI-008 | Templates Testing | Python | `templates/testing/*.py` | Templates tests | Sí |
| CI-009 | Templates Reporting | Markdown | `templates/reporting/*.md` | Templates reportes | Sí |
| CI-010 | TimeTracker | Python | `tracking/time_tracker.py` | Sistema de tracking | Sí |
| CI-011 | Track Commands | Python | `tracking/commands.py` | Comandos /track-* | Sí |
| CI-012 | Documentación | Markdown | `docs/*.md` | Documentación del kit | Sí |
| CI-013 | Ejemplo PyQt | Proyecto | `examples/pyqt-mvc/` | Ejemplo completo PyQt | Sí |
| CI-014 | Ejemplo FastAPI | Proyecto | `examples/fastapi-rest/` | Ejemplo completo FastAPI | Sí |
| CI-015 | Scripts Validación | Python | `scripts/*.py` | Scripts de utilidad | Sí |

### 3.3 Control de Versiones

**Sistema:** Git + GitHub

**Estrategia de Branching:**
```
main                    # Producción (releases estables)
  └── develop           # Desarrollo activo
       ├── feature/xxx  # Features nuevas
       ├── fix/xxx      # Bugfixes
       └── docs/xxx     # Documentación
```

**Convención de Commits:**
```
<type>(<scope>): <subject>

Types:
- feat: Nueva funcionalidad
- fix: Corrección de bug
- docs: Documentación
- refactor: Refactorización
- test: Tests
- chore: Mantenimiento

Ejemplos:
feat(installer): agregar soporte para Django
docs(tracking): documentar comando /track-history
fix(templates): corregir variables en test-unit.py
```

**Versionado Semántico:** `MAJOR.MINOR.PATCH`
- **MAJOR:** Cambios incompatibles (breaking changes)
- **MINOR:** Nuevas funcionalidades compatibles
- **PATCH:** Correcciones de bugs

**Versión Inicial:** `1.0.0` (al completar proyecto)

### 3.4 Gestión de Dependencias

**Dependencias del Framework:**
- Python 3.10+
- PyYAML (para config.yaml)
- (Mínimas, solo para instalación)

**Dependencias de Ejemplos:**
- PyQt6 (ejemplo pyqt-mvc)
- FastAPI, uvicorn (ejemplo fastapi-rest)
- Django (ejemplo django-mvt)
- pytest, pytest-cov, pytest-bdd (todos)

**Archivo:** `requirements.txt` (solo para desarrollo del framework)
**Archivos por ejemplo:** `examples/{stack}/requirements.txt`

### 3.5 Baseline del Proyecto

**Baseline Inicial (v1.0.0):**

| Componente | Versión | Estado | Fecha Target |
|------------|---------|--------|--------------|
| Instalador Python | 1.0 | Pendiente | Sprint 1 |
| Skill implement-us | 1.0 | Pendiente | Sprint 2 |
| Templates (todos) | 1.0 | Pendiente | Sprint 2 |
| Tracking System | 1.0 | Pendiente | Sprint 1 |
| Documentación | 1.0 | Pendiente | Sprint 3 |
| Ejemplo PyQt | 1.0 | Pendiente | Sprint 3 |
| Ejemplo FastAPI | 1.0 | Pendiente | Sprint 3 |

**Criterios de Aceptación v1.0:**
- ✅ Instalador funcional en Linux/macOS/Windows
- ✅ Skill implement-us 100% funcional con al menos 2 perfiles
- ✅ Templates completos para BDD, planning, testing, reporting
- ✅ Sistema de tracking funcionando
- ✅ Documentación completa (getting-started, installation, customization)
- ✅ Al menos 2 ejemplos funcionales (PyQt, FastAPI)
- ✅ Tests de instalación
- ✅ README.md profesional

---

## 4. Mecanismo de Despliegue

### 4.1 Estrategia de Distribución

**Método Principal:** GitHub Repository (público o privado)

**URL del Repositorio (sugerido):**
```
https://github.com/vvalotto/claude-dev-kit
```

**Método Secundario (futuro):** PyPI package
```bash
pip install claude-dev-kit
```

### 4.2 Proceso de Instalación para Usuarios

#### 4.2.1 Instalación Global (Recomendada)

**Paso 1: Clonar el kit**
```bash
git clone https://github.com/vvalotto/claude-dev-kit.git ~/.claude-dev-kit
```

**Paso 2: Navegar al proyecto de usuario**
```bash
cd ~/mi-proyecto-python
```

**Paso 3: Ejecutar instalador**

**Opción A: Instalador Python (Multiplataforma)**
```bash
python ~/.claude-dev-kit/install/installer.py
```

**Opción B: Script Bash (Unix/macOS)**
```bash
~/.claude-dev-kit/install/install.sh
```

**Opción C: Script PowerShell (Windows)**
```powershell
~/.claude-dev-kit/install/install.ps1
```

**Paso 4: Seleccionar perfil**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀 Claude Dev Kit - Installer v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Selecciona el perfil para tu proyecto:

1. PyQt + MVC (pyqt-mvc)
2. FastAPI + REST (fastapi-rest)
3. Django + MVT (django-mvt)
4. Generic Python (generic-python)

Opción [1-4]: _
```

**Paso 5: Validar instalación**
```bash
# El instalador ejecuta automáticamente:
python ~/.claude-dev-kit/scripts/validate-setup.py
```

#### 4.2.2 Instalación con Flags

**Instalación no interactiva:**
```bash
# Especificar perfil directamente
python ~/.claude-dev-kit/install/installer.py --profile pyqt-mvc

# Instalación silenciosa (sin prompts)
python ~/.claude-dev-kit/install/installer.py --profile fastapi-rest --yes

# Dry-run (mostrar qué se haría sin ejecutar)
python ~/.claude-dev-kit/install/installer.py --profile django-mvt --dry-run
```

**Flags soportados:**
- `--profile {nombre}`: Seleccionar perfil sin prompt
- `--yes` / `-y`: Aceptar todas las confirmaciones
- `--dry-run`: Simular instalación sin ejecutar
- `--force`: Sobrescribir archivos existentes
- `--config {path}`: Usar archivo de configuración custom

#### 4.2.3 Instalación Local (Por Proyecto)

**Opción:** Clonar el kit dentro del proyecto
```bash
# En el proyecto
git clone https://github.com/vvalotto/claude-dev-kit.git .claude-dev-kit

# Ejecutar instalador local
./.claude-dev-kit/install/installer.py --local
```

**Ventaja:** Kit versionado junto con el proyecto
**Desventaja:** Duplicación si se usa en múltiples proyectos

### 4.3 Estructura Post-Instalación

Después de ejecutar el instalador, el proyecto de usuario tendrá:

```
mi-proyecto-python/
├── .claude/                          # ← Creado por el instalador
│   ├── skills/
│   │   └── implement-us/
│   │       ├── skill.md              # Skill instalado
│   │       └── config.json           # Config personalizada según perfil
│   ├── templates/
│   │   ├── bdd/
│   │   ├── planning/
│   │   ├── testing/
│   │   └── reporting/
│   ├── tracking/
│   │   ├── time_tracker.py
│   │   ├── commands.py
│   │   └── __init__.py
│   └── config.json                   # Configuración global del kit
│
├── CLAUDE.md                         # ← Generado si no existe
├── [código del proyecto del usuario]
└── [...]
```

### 4.4 Archivos Generados por el Instalador

| Archivo | Origen | Destino | Acción |
|---------|--------|---------|--------|
| `skill.md` | `skills/implement-us/skill.md` | `.claude/skills/implement-us/skill.md` | Copiar |
| `config.json` | `skills/implement-us/customizations/{perfil}.json` | `.claude/skills/implement-us/config.json` | Copiar + Merge con base |
| Templates | `templates/**/*` | `.claude/templates/**/*` | Copiar todos |
| Tracking | `tracking/**/*.py` | `.claude/tracking/**/*.py` | Copiar todos |
| CLAUDE.md | `install/templates/CLAUDE.md.template` | `CLAUDE.md` | Generar si no existe |
| .gitignore | - | `.claude/.gitignore` | Generar (excluir logs, tracking/*.json) |

### 4.5 Configuración del Instalador

**Archivo:** `install/config.yaml`

```yaml
# Configuración del instalador Claude Dev Kit
version: "1.0"

# Directorios de origen (dentro del kit)
source:
  skills: "skills"
  templates: "templates"
  tracking: "tracking"
  docs: "docs"

# Directorios de destino (en el proyecto del usuario)
destination:
  root: ".claude"
  skills: ".claude/skills"
  templates: ".claude/templates"
  tracking: ".claude/tracking"

# Perfiles disponibles
profiles:
  pyqt-mvc:
    name: "PyQt + MVC"
    description: "Proyectos PyQt6 con arquitectura MVC"
    config_override: "skills/implement-us/customizations/pyqt-mvc.json"
    example: "examples/pyqt-mvc"

  fastapi-rest:
    name: "FastAPI + REST"
    description: "APIs REST con FastAPI"
    config_override: "skills/implement-us/customizations/fastapi-rest.json"
    example: "examples/fastapi-rest"

  django-mvt:
    name: "Django + MVT"
    description: "Aplicaciones web Django"
    config_override: "skills/implement-us/customizations/django-mvt.json"
    example: "examples/django-mvt"

  generic-python:
    name: "Generic Python"
    description: "Proyectos Python genéricos"
    config_override: "skills/implement-us/customizations/generic-python.json"
    example: "examples/generic-python"

# Archivos a excluir de la copia
exclude:
  - "*.pyc"
  - "__pycache__"
  - "*.log"
  - ".DS_Store"
  - "*.swp"

# Generación de archivos
generate:
  claude_md:
    enabled: true
    template: "install/templates/CLAUDE.md.template"
    destination: "CLAUDE.md"
    skip_if_exists: true

  gitignore:
    enabled: true
    destination: ".claude/.gitignore"
    content: |
      # Claude Dev Kit - Archivos generados
      tracking/*.json
      logs/*.log
      *.pyc
      __pycache__/

# Validación post-instalación
validation:
  enabled: true
  script: "scripts/validate-setup.py"
  required_files:
    - ".claude/skills/implement-us/skill.md"
    - ".claude/skills/implement-us/config.json"
    - ".claude/templates/bdd/scenario.feature"
    - ".claude/tracking/time_tracker.py"
```

### 4.6 Algoritmo del Instalador

**Pseudocódigo:**

```python
def install_claude_dev_kit(project_path, profile, force=False, dry_run=False):
    """
    Instala Claude Dev Kit en un proyecto.

    Args:
        project_path: Ruta al proyecto de destino
        profile: Perfil seleccionado (pyqt-mvc, fastapi-rest, etc.)
        force: Sobrescribir archivos existentes
        dry_run: Simular sin ejecutar
    """

    # 1. Cargar configuración
    config = load_yaml("install/config.yaml")

    # 2. Validar proyecto destino
    if not is_valid_python_project(project_path):
        raise Error("El directorio no parece ser un proyecto Python")

    # 3. Detectar instalación existente
    claude_dir = project_path / ".claude"
    if claude_dir.exists() and not force:
        if not confirm("Ya existe .claude/. ¿Sobrescribir?"):
            return

    # 4. Validar perfil
    if profile not in config['profiles']:
        raise Error(f"Perfil '{profile}' no válido")

    profile_config = config['profiles'][profile]

    # 5. Crear estructura de directorios
    if not dry_run:
        create_directory(claude_dir / "skills/implement-us")
        create_directory(claude_dir / "templates")
        create_directory(claude_dir / "tracking")

    print(f"✅ Estructura de directorios creada")

    # 6. Copiar skills
    source_skill = kit_root / config['source']['skills'] / "implement-us"
    dest_skill = claude_dir / "skills/implement-us"

    if not dry_run:
        copy_file(source_skill / "skill.md", dest_skill / "skill.md")

    print(f"✅ Skill 'implement-us' instalado")

    # 7. Generar configuración personalizada
    base_config = load_json(source_skill / "config.json")
    profile_override = load_json(kit_root / profile_config['config_override'])

    merged_config = merge_configs(base_config, profile_override)

    if not dry_run:
        save_json(dest_skill / "config.json", merged_config)

    print(f"✅ Configuración personalizada para '{profile}'")

    # 8. Copiar templates
    source_templates = kit_root / config['source']['templates']
    dest_templates = claude_dir / "templates"

    if not dry_run:
        copy_tree(source_templates, dest_templates, exclude=config['exclude'])

    print(f"✅ Templates instalados")

    # 9. Copiar tracking
    source_tracking = kit_root / config['source']['tracking']
    dest_tracking = claude_dir / "tracking"

    if not dry_run:
        copy_tree(source_tracking, dest_tracking, exclude=config['exclude'])

    print(f"✅ Sistema de tracking instalado")

    # 10. Generar CLAUDE.md si no existe
    claude_md_path = project_path / "CLAUDE.md"

    if not claude_md_path.exists() and config['generate']['claude_md']['enabled']:
        template = load_file(kit_root / config['generate']['claude_md']['template'])
        rendered = render_template(template, profile=profile, project_path=project_path)

        if not dry_run:
            save_file(claude_md_path, rendered)

        print(f"✅ CLAUDE.md generado")
    else:
        print(f"ℹ️  CLAUDE.md ya existe (no sobrescrito)")

    # 11. Generar .gitignore
    if config['generate']['gitignore']['enabled']:
        gitignore_path = claude_dir / ".gitignore"

        if not dry_run:
            save_file(gitignore_path, config['generate']['gitignore']['content'])

        print(f"✅ .gitignore generado en .claude/")

    # 12. Validar instalación
    if config['validation']['enabled'] and not dry_run:
        print("\n🔍 Validando instalación...")

        validation_script = kit_root / config['validation']['script']
        result = run_python_script(validation_script, project_path)

        if result.success:
            print(f"✅ Validación exitosa")
        else:
            print(f"⚠️  Validación falló: {result.error}")
            return False

    # 13. Resumen
    print("\n" + "━" * 50)
    print("🎉 Instalación completada exitosamente!")
    print("━" * 50)
    print(f"Perfil:   {profile_config['name']}")
    print(f"Destino:  {project_path}")
    print(f"\n📚 Próximos pasos:")
    print(f"   1. Revisar CLAUDE.md")
    print(f"   2. Personalizar .claude/skills/implement-us/config.json si necesario")
    print(f"   3. Ejecutar: /implement-us US-XXX")
    print(f"\n📖 Documentación: {kit_root / 'docs/getting-started.md'}")

    return True
```

### 4.7 Actualización del Kit

**Escenario:** Usuario ya tiene el kit instalado y sale una nueva versión

**Proceso:**

```bash
# 1. Actualizar el kit clonado
cd ~/.claude-dev-kit
git pull origin main

# 2. Ejecutar migración
python install/installer.py --migrate --project ~/mi-proyecto
```

**Script de migración:**
- Detecta versión instalada (leyendo `.claude/version.json`)
- Compara con versión del kit
- Aplica migraciones incrementales
- Preserva personalizaciones del usuario

---

## 5. Plan de Implementación

### 5.1 Fases del Proyecto

**Fase 1: Setup Inicial**
- Crear repositorio GitHub
- Inicializar estructura de directorios
- Configurar `.gitignore`, `LICENSE`, `README.md` base
- Incluir este `PROJECT_PLAN.md` en el repo

**Fase 2: Sistema de Instalación**
- Desarrollar `installer.py`
- Desarrollar `config.yaml`
- Crear scripts `.sh` y `.ps1`
- Desarrollar `validate-setup.py`

**Fase 3: Generalización de Skills**
- Migrar `implement-us.md` desde simapp_termostato
- Generalizar referencias específicas de MVC/PyQt
- Crear perfiles de customización
- Documentar cada fase

**Fase 4: Templates**
- Migrar templates desde simapp_termostato
- Generalizar variables
- Crear templates adicionales (sprint-plan, ADR)
- Documentar templates

**Fase 5: Sistema de Tracking**
- Migrar `time_tracker.py` y `commands.py`
- Refactorizar si necesario
- Documentar tracking

**Fase 6: Documentación**
- Crear `getting-started.md`
- Crear `installation.md`
- Crear `customization.md`
- Documentar skills, templates, tracking

**Fase 7: Ejemplos**
- Crear ejemplo PyQt + MVC
- Crear ejemplo FastAPI + REST
- Crear ejemplo genérico Python
- Validar ejemplos end-to-end

**Fase 8: Testing y Validación**
- Tests de instalador
- Tests de tracking
- Validación en múltiples plataformas
- Corrección de bugs

**Fase 9: Release v1.0**
- Generar `CHANGELOG.md`
- Crear tag `v1.0.0`
- Publicar release en GitHub
- Documentación final

### 5.2 Sprints Propuestos

**Sprint 1: Setup + Instalación (1 semana)**
- Fase 1: Setup Inicial
- Fase 2: Sistema de Instalación
- Entregable: Instalador funcional

**Sprint 2: Skills + Templates (1 semana)**
- Fase 3: Generalización de Skills
- Fase 4: Templates
- Fase 5: Sistema de Tracking
- Entregable: Skills y templates generalizados

**Sprint 3: Documentación + Ejemplos (1 semana)**
- Fase 6: Documentación
- Fase 7: Ejemplos
- Entregable: Documentación completa y ejemplos funcionales

**Sprint 4: Testing + Release (1 semana)**
- Fase 8: Testing y Validación
- Fase 9: Release v1.0
- Entregable: Versión 1.0 publicada

**Duración Total:** 4 semanas

### 5.3 Tareas Prioritarias (Primer Commit)

**Para empezar a trabajar inmediatamente:**

1. ✅ Crear repositorio en GitHub: `claude-dev-kit`
2. ✅ Clonar localmente
3. ✅ Crear estructura de directorios base
4. ✅ Agregar `README.md` inicial
5. ✅ Agregar `LICENSE` (MIT)
6. ✅ Agregar `.gitignore`
7. ✅ Agregar este `PROJECT_PLAN.md`
8. ✅ Primer commit: `chore: initial project setup`
9. ✅ Push a `main`

**Próximo paso:** Empezar Sprint 1 - Sistema de Instalación

---

## 6. Riesgos y Mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Incompatibilidad multiplataforma del instalador | Media | Alto | Desarrollar en Python puro, testear en Linux/macOS/Windows |
| Generalización pierde funcionalidad específica | Media | Medio | Mantener perfiles de customización detallados |
| Documentación incompleta | Baja | Alto | Dedicar sprint completo a documentación |
| Breaking changes en Claude Code API | Baja | Alto | Versionar el kit, documentar compatibilidad |
| Usuarios no entienden personalización | Media | Medio | Ejemplos detallados, wizard de instalación |

---

## 7. Métricas de Éxito

### 7.1 Métricas Técnicas

- ✅ Instalador funciona en Linux, macOS, Windows
- ✅ 100% de templates migrados y generalizados
- ✅ Sistema de tracking 100% funcional
- ✅ Al menos 3 perfiles de customización
- ✅ Al menos 2 ejemplos completos funcionales
- ✅ Documentación completa (>80% de cobertura de features)

### 7.2 Métricas de Calidad

- ✅ Tests de instalación (coverage >80%)
- ✅ README claro y profesional
- ✅ Changelog actualizado
- ✅ Zero errores críticos en validación

### 7.3 Métricas de Adopción (Post-Release)

- [ ] 5+ estrellas en GitHub (primera semana)
- [ ] 10+ instalaciones exitosas
- [ ] Feedback positivo de usuarios
- [ ] Contribuciones externas (issues, PRs)

---

## 8. Roadmap Futuro (Post v1.0)

### Versión 1.1 - Mejoras Incrementales
- Skill adicional: `/code-review`
- Soporte para TypeScript/JavaScript
- Dashboard web de métricas

### Versión 1.2 - Integraciones
- Integración con Jira (actualizar estado de issues)
- Integración con GitHub Issues
- Notificaciones (Slack, email)

### Versión 2.0 - Ecosistema
- Marketplace de skills comunitarios
- API pública para crear skills
- Soporte para múltiples lenguajes (Go, Rust, Java)

---

## 9. Contacto y Contribuciones

**Maintainer:** Victor Valotto
**Email:** [tu-email]
**GitHub:** https://github.com/vvalotto/claude-dev-kit

**Contribuciones:**
- Reportar issues: GitHub Issues
- Proponer features: GitHub Discussions
- Contribuir código: Pull Requests (seguir guía en `CONTRIBUTING.md`)

---

## 10. Aprobación del Plan

| Stakeholder | Rol | Aprobación | Fecha |
|-------------|-----|------------|-------|
| Victor Valotto | Product Owner | ⏳ Pendiente | 2026-02-07 |

---

**Próxima Acción:** Crear repositorio GitHub y ejecutar tareas prioritarias (Sección 5.3)
