# Guía de Instalación Detallada

**Última Actualización:** 2026-02-15
**Audiencia:** Usuario Final
**Nivel:** Básico - Intermedio
**Tiempo estimado:** 10-20 minutos

---

## Tabla de Contenidos

- [Introducción](#introducción)
- [Prerequisitos](#prerequisitos)
- [Instalación Interactiva](#instalación-interactiva)
- [Instalación No Interactiva](#instalación-no-interactiva)
- [Sistema de Perfiles](#sistema-de-perfiles)
- [Validación Post-Instalación](#validación-post-instalación)
- [Troubleshooting](#troubleshooting)
- [Actualización](#actualización)
- [Desinstalación](#desinstalación)

---

## Introducción

Esta guía cubre la instalación completa de Claude Dev Kit en tu proyecto, incluyendo todos los modos de instalación, perfiles disponibles y resolución de problemas.

**Modos de instalación:**
- **Interactivo:** Asistente paso a paso (recomendado para usuarios nuevos)
- **No interactivo:** Instalación automatizada con flags (ideal para CI/CD)

---

## Prerequisitos

### Software Requerido

| Software | Versión Mínima | Verificación |
|----------|----------------|--------------|
| **Python** | 3.9+ | `python --version` |
| **Git** | 2.0+ | `git --version` |
| **Claude Code CLI** | Latest | `claude --version` |

### Verificar Prerequisitos

```bash
# Verificar Python
python --version
# Debe mostrar: Python 3.9.x o superior

# Verificar Git
git --version
# Debe mostrar: git version 2.x.x

# Verificar Claude Code
claude --version
# Debe mostrar versión de Claude Code
```

> **Importante:** Si Python muestra versión <3.9, actualízalo antes de continuar.

### Proyecto Python (Opcional)

- **Proyecto existente:** El framework se instalará en `.claude/`
- **Proyecto nuevo:** Puedes crear uno para probar

```bash
# Crear proyecto nuevo para pruebas
mkdir ~/test-claude-dev-kit
cd ~/test-claude-dev-kit
git init
python -m venv venv
source venv/bin/activate
mkdir -p src tests docs
touch src/__init__.py
```

---

## Instalación Interactiva

Modo recomendado para usuarios nuevos. El instalador te guiará paso a paso.

### Paso 1: Clonar Repositorio

```bash
git clone https://github.com/vvalotto/claude-dev-kit.git ~/.claude-dev-kit
```

### Paso 2: Navegar a tu Proyecto

```bash
cd ~/mi-proyecto-python
```

### Paso 3: Ejecutar Instalador

```bash
python ~/.claude-dev-kit/install/installer.py
```

### Paso 4: Seleccionar Perfil

El instalador mostrará:

```
=== Claude Dev Kit - Instalador Interactivo ===

Proyecto detectado: /Users/usuario/mi-proyecto-python

Selecciona tu stack tecnológico:

1. pyqt-mvc       - Aplicaciones desktop PyQt6 + MVC
2. fastapi-rest   - APIs REST asíncronas con FastAPI
3. flask-rest     - APIs REST con Flask
4. flask-webapp   - Aplicaciones web fullstack con Flask
5. generic-python - Proyectos Python genéricos

Ingresa el número (1-5): _
```

### Paso 5: Confirmar Instalación

```
Configuración seleccionada:
  Perfil: pyqt-mvc
  Arquitectura: MVC
  Test Framework: pytest-qt
  Tracking: Habilitado

¿Confirmar instalación? (s/n): s
```

### Paso 6: Validación Automática

El instalador validará automáticamente:

```
✅ Copiando skills...
✅ Copiando templates...
✅ Generando configuración...
✅ Validando instalación...

✅ Instalación completada exitosamente

Archivos creados:
  .claude/skills/implement-us/
  .claude/skills/track-*/
  .claude/templates/
  .claude/config.json

Siguiente paso: /implement-us US-001
```

---

## Instalación No Interactiva

Ideal para automatización, CI/CD o instalaciones masivas.

### Instalación con Flags

```bash
python ~/.claude-dev-kit/install/installer.py \
  --profile pyqt-mvc \
  --yes
```

**Flags disponibles:**

| Flag | Descripción | Ejemplo |
|------|-------------|---------|
| `--profile NOMBRE` | Seleccionar perfil | `--profile fastapi-rest` |
| `--yes` / `-y` | No solicitar confirmación | `--yes` |
| `--path RUTA` | Ruta del proyecto | `--path /Users/x/proyecto` |
| `--quiet` / `-q` | Modo silencioso | `--quiet` |
| `--verbose` / `-v` | Modo verbose | `--verbose` |

### Ejemplos de Uso

**FastAPI en CI/CD:**
```bash
cd /app
python ~/.claude-dev-kit/install/installer.py \
  --profile fastapi-rest \
  --yes \
  --quiet
```

**Flask con path específico:**
```bash
python ~/.claude-dev-kit/install/installer.py \
  --profile flask-rest \
  --path /Users/dev/api-project \
  --yes
```

**Generic Python verbose:**
```bash
python ~/.claude-dev-kit/install/installer.py \
  --profile generic-python \
  --verbose \
  --yes
```

### Instalación desde Archivo de Configuración

```bash
# Crear config de instalación
cat > install-config.json << 'EOF'
{
  "profile": "fastapi-rest",
  "path": "/app/proyecto",
  "options": {
    "enable_bdd": true,
    "enable_tracking": true
  }
}
EOF

# Instalar con config
python ~/.claude-dev-kit/install/installer.py --config install-config.json
```

---

## Sistema de Perfiles

El framework soporta 5 perfiles predefinidos que personalizan la experiencia según tu stack.

### 1. pyqt-mvc - Aplicaciones Desktop PyQt6

**Ideal para:** Aplicaciones de escritorio con interfaz gráfica

**Características:**
- Arquitectura MVC (Model-View-Controller)
- Patrones: Factory, Coordinator, Observer
- Test Framework: pytest-qt
- Quality Gates: 95% coverage, Pylint 8.5+

**Ejemplo de proyecto:**
```
src/
├── modelos/      # Modelos de datos
├── vistas/       # Widgets PyQt
├── controladores/# Lógica de negocio
└── coordinadores/# Coordinación de componentes
```

---

### 2. fastapi-rest - APIs REST Asíncronas

**Ideal para:** APIs backend modernas con async/await

**Características:**
- Arquitectura: Layered (Router → Service → Repository)
- Patrones: Dependency Injection, Repository
- Test Framework: pytest-asyncio
- Quality Gates: 95% coverage, Pylint 9.0+

**Ejemplo de proyecto:**
```
src/
├── routers/     # Endpoints API
├── services/    # Lógica de negocio
├── repositories/# Acceso a datos
└── models/      # Pydantic models
```

---

### 3. flask-rest - APIs REST Flask

**Ideal para:** APIs REST tradicionales con Flask

**Características:**
- Arquitectura: Blueprints + Services
- Patrones: Blueprint, Factory
- Test Framework: pytest + pytest-flask
- Quality Gates: 90% coverage, Pylint 8.0+

**Ejemplo de proyecto:**
```
src/
├── blueprints/  # Módulos de API
├── services/    # Lógica de negocio
└── models/      # SQLAlchemy models
```

---

### 4. flask-webapp - Aplicaciones Web Flask

**Ideal para:** Aplicaciones web fullstack con templates

**Características:**
- Arquitectura: MVT (Model-View-Template)
- Patrones: Blueprint, Template Inheritance
- Test Framework: pytest + pytest-flask
- Quality Gates: 85% coverage, Pylint 8.0+

**Ejemplo de proyecto:**
```
src/
├── views/       # Views (controladores)
├── models/      # Models de datos
├── templates/   # Jinja2 templates
└── static/      # CSS, JS, imágenes
```

---

### 5. generic-python - Python Genérico

**Ideal para:** Cualquier proyecto Python, CLIs, librerías

**Características:**
- Arquitectura: Layered (flexible)
- Patrones: Configurable
- Test Framework: pytest
- Quality Gates: 90% coverage, Pylint 8.0+

**Ejemplo de proyecto:**
```
src/
├── core/        # Funcionalidad core
├── utils/       # Utilidades
└── interfaces/  # CLIs, APIs, etc.
```

---

## Validación Post-Instalación

Después de instalar, valida que todo esté correcto.

### Validación Manual

```bash
# Verificar estructura
ls -la .claude/

# Deberías ver:
.claude/
├── config.json
├── skills/
│   ├── implement-us/
│   ├── track-pause/
│   ├── track-resume/
│   ├── track-status/
│   └── track-report/
├── templates/
│   ├── bdd/
│   ├── planning/
│   ├── testing/
│   └── reporting/
└── tracking/
```

### Script de Validación (Futuro)

```bash
# Ejecutar validador automático
python ~/.claude-dev-kit/scripts/validate-setup.py
```

**Output esperado:**
```
✅ Python 3.9+ detected
✅ Git installed
✅ Claude Code installed
✅ Config file valid
✅ Skills installed (5/5)
✅ Templates installed (4/4)

✅ Instalación válida - Todo listo para usar
```

### Test de Smoke

Crea una US de prueba:

```bash
# Crear US de prueba
echo "# US-TEST: Test Installation" > US-TEST.md

# Ejecutar skill
/implement-us US-TEST --dry-run

# Debería mostrar las 10 fases sin errores
```

---

## Troubleshooting

### Error: "Python version not supported"

**Síntoma:**
```
Error: Python 3.9+ required. Found: 3.8.10
```

**Solución:**
```bash
# Opción 1: Actualizar Python del sistema
sudo apt update && sudo apt install python3.11

# Opción 2: Usar pyenv
pyenv install 3.11
pyenv local 3.11

# Opción 3: Especificar python3.11 explícitamente
python3.11 ~/.claude-dev-kit/install/installer.py
```

---

### Error: "Project directory not found"

**Síntoma:**
```
Error: No valid Python project found
```

**Solución:**
```bash
# Verificar que estás en directorio correcto
pwd

# El directorio debe contener archivos Python o estructura de proyecto
ls -la

# Si es proyecto nuevo, crear estructura básica
mkdir -p src tests
touch src/__init__.py

# Re-intentar instalación
python ~/.claude-dev-kit/install/installer.py
```

---

### Error: "Permission denied"

**Síntoma:**
```
PermissionError: [Errno 13] Permission denied: '.claude/'
```

**Solución:**
```bash
# Verificar permisos del directorio
ls -la

# Cambiar propietario si es necesario
sudo chown -R $USER:$USER .

# O instalar en directorio con permisos
cd ~/mi-proyecto
python ~/.claude-dev-kit/install/installer.py
```

---

### Error: "Git not installed"

**Solución:**
```bash
# Ubuntu/Debian
sudo apt install git

# macOS
brew install git

# Windows
# Descargar de: https://git-scm.com/
```

---

### Error: "Skills not found after install"

**Síntoma:**
```
Command not found: /implement-us
```

**Solución:**
```bash
# 1. Verificar instalación
ls -la .claude/skills/

# 2. Si falta, reinstalar
python ~/.claude-dev-kit/install/installer.py --yes

# 3. Reiniciar Claude Code
# Cerrar y abrir de nuevo

# 4. Verificar con /help
/help
# Debería listar /implement-us
```

---

### Instalación corrupta

**Solución:**
```bash
# Limpiar instalación anterior
rm -rf .claude/

# Reinstalar limpio
python ~/.claude-dev-kit/install/installer.py --yes
```

---

## Actualización

Actualiza el framework a una nueva versión.

### Actualizar Framework

```bash
# Paso 1: Actualizar repositorio local
cd ~/.claude-dev-kit
git pull origin main

# Paso 2: Navegar a proyecto
cd ~/mi-proyecto

# Paso 3: Re-ejecutar instalador con --upgrade
python ~/.claude-dev-kit/install/installer.py --upgrade
```

**El modo upgrade:**
- ✅ Preserva configuración custom en .claude/config.json
- ✅ Actualiza skills a nueva versión
- ✅ Actualiza templates
- ⚠️ Backup automático de config anterior

### Actualizar Solo Configuración

```bash
# Actualizar solo config (mantener skills)
python ~/.claude-dev-kit/install/installer.py \
  --profile fastapi-rest \
  --config-only
```

### Ver Versión Instalada

```bash
cat .claude/config.json | grep version
```

---

## Desinstalación

Eliminar el framework del proyecto.

### Desinstalación Completa

```bash
# Eliminar directorio .claude/
rm -rf .claude/

# Opcional: Eliminar repo global
rm -rf ~/.claude-dev-kit
```

### Desinstalación Parcial (Mantener Config)

```bash
# Hacer backup de config
cp .claude/config.json ~/config-backup.json

# Eliminar framework
rm -rf .claude/

# Más tarde, reinstalar con config guardado
mkdir -p .claude
cp ~/config-backup.json .claude/config.json
python ~/.claude-dev-kit/install/installer.py --upgrade
```

---

## Recursos Adicionales

- [Getting Started](Getting-Started) - Guía de inicio rápido
- [Personalización](Customization) - Modificar perfiles y configuración
- [Configuración](Configuration) - Referencia completa de opciones
- [Skill implement-us](user-skills-Implement-Us) - Uso del skill principal

---

**Anterior:** [Getting Started](Getting-Started)
**Siguiente:** [Personalización](Customization)
**Índice:** [Volver al índice](Index)
