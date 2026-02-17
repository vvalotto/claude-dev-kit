# Sistema de Instalación - Documentación Técnica

Documentación técnica del sistema de instalación del Claude Dev Kit.

> **Para usuarios:** Ver [docs/installation.md](../docs/installation.md)

---

## 📋 Tabla de Contenidos

- [Instalación Rápida](#-instalación-rápida)
- [Instalación Detallada](#-instalación-detallada)
- [Perfiles Disponibles](#-perfiles-disponibles)
- [Opciones de Línea de Comandos](#-opciones-de-línea-de-comandos)
- [Ejemplos por Sistema Operativo](#-ejemplos-por-sistema-operativo)
- [Troubleshooting](#-troubleshooting)
- [Próximos Pasos](#-próximos-pasos)

---

## 🚀 Instalación Rápida

### macOS / Linux

```bash
# Clonar Claude Dev Kit en ubicación global
git clone https://github.com/vvalotto/claude-dev-kit.git ~/.claude-dev-kit

# Navegar a tu proyecto
cd ~/mi-proyecto

# Ejecutar instalador (modo interactivo)
~/.claude-dev-kit/install/install.sh
```

### Windows

```powershell
# Clonar Claude Dev Kit
git clone https://github.com/vvalotto/claude-dev-kit.git C:\claude-dev-kit

# Navegar a tu proyecto
cd C:\mi-proyecto

# Ejecutar instalador (modo interactivo)
python C:\claude-dev-kit\install\installer.py
```

---

## 📚 Instalación Detallada

### Paso 1: Clonar el Repositorio

Clona el Claude Dev Kit en una ubicación global (recomendado) o local:

**Opción A: Instalación Global (Recomendada)**

```bash
# macOS/Linux
git clone https://github.com/vvalotto/claude-dev-kit.git ~/.claude-dev-kit

# Windows
git clone https://github.com/vvalotto/claude-dev-kit.git C:\claude-dev-kit
```

**Opción B: Instalación Local (Por Proyecto)**

```bash
# Dentro del proyecto
git clone https://github.com/vvalotto/claude-dev-kit.git .claude-dev-kit
```

### Paso 2: Navegar a tu Proyecto

```bash
cd /ruta/a/tu/proyecto
```

Tu proyecto debe ser un directorio Python (con o sin git inicializado).

### Paso 3: Ejecutar el Instalador

**Opción A: Modo Interactivo (Recomendado)**

El instalador te preguntará qué perfil quieres instalar:

```bash
# macOS/Linux
~/.claude-dev-kit/install/install.sh

# Windows
python C:\claude-dev-kit\install\installer.py
```

**Opción B: Modo No-Interactivo**

Especifica el perfil directamente:

```bash
# macOS/Linux
~/.claude-dev-kit/install/install.sh --profile pyqt-mvc --yes

# Windows
python C:\claude-dev-kit\install\installer.py --profile pyqt-mvc --yes
```

### Paso 4: Verificar Instalación

El instalador ejecuta validación automáticamente. Para validar manualmente:

```bash
python ~/.claude-dev-kit/scripts/validate-setup.py
```

---

## 🎯 Perfiles Disponibles

El Claude Dev Kit soporta múltiples perfiles que personalizan el framework para diferentes stacks tecnológicos.

### 1. PyQt + MVC (`pyqt-mvc`)

**Descripción:** PyQt6 applications with MVC architecture

**Cuándo usar:**
- Aplicaciones de escritorio con PyQt6
- Arquitectura MVC (Model-View-Controller)
- Patrones Factory, Coordinator, Observer

**Ejemplo de proyecto:**
```
mi-app-pyqt/
├── app/
│   ├── presentacion/    # Views y Controllers
│   ├── modelo/          # Models
│   └── coordinador/     # Coordinators
├── tests/
└── .claude/             # Instalado por el kit
```

**Testing Framework:** `pytest-qt`

---

### 2. FastAPI + REST (`fastapi-rest`)

**Descripción:** FastAPI REST APIs with layered architecture

**Cuándo usar:**
- APIs REST con FastAPI
- Arquitectura en capas (Router, Service, Repository)
- Patrones Dependency Injection, Repository Pattern

**Ejemplo de proyecto:**
```
mi-api-fastapi/
├── app/
│   ├── routers/         # API endpoints
│   ├── services/        # Business logic
│   ├── repositories/    # Data access
│   └── schemas/         # Pydantic models
├── tests/
└── .claude/             # Instalado por el kit
```

**Testing Framework:** `pytest`

---

### 3. Flask REST API (`flask-rest`)

**Descripción:** Flask REST APIs with layered architecture

**Cuándo usar:**
- APIs REST con Flask
- Arquitectura en capas (Blueprint, Service, Repository)
- Proyectos que necesitan sync/threading (sin async)

**Ejemplo de proyecto:**
```
mi-api-flask/
├── app/
│   ├── blueprints/      # API endpoints (Flask Blueprints)
│   ├── services/        # Business logic
│   ├── repositories/    # Data access
│   └── models/          # Domain models
├── tests/
└── .claude/             # Instalado por el kit
```

**Testing Framework:** `pytest`

---

### 4. Flask WebApp (`flask-webapp`)

**Descripción:** Flask fullstack webapps with Jinja2 templates and SSR

**Cuándo usar:**
- Aplicaciones web fullstack con Flask
- Server-Side Rendering con Jinja2
- Patrón BFF (Backend for Frontend)

**Ejemplo de proyecto:**
```
mi-webapp-flask/
├── app/
│   ├── blueprints/      # Routes (Flask Blueprints)
│   ├── templates/       # Jinja2 templates
│   ├── static/          # CSS, JS, images
│   └── models/          # Domain models
├── tests/
└── .claude/             # Instalado por el kit
```

**Testing Framework:** `pytest`

---

### 5. Generic Python (`generic-python`)

**Descripción:** Generic Python projects without specific framework

**Cuándo usar:**
- Proyectos Python genéricos
- Scripts, bibliotecas, herramientas CLI
- Sin framework específico
- Cuando quieres máxima flexibilidad

**Ejemplo de proyecto:**
```
mi-proyecto-python/
├── src/
│   └── modulos/
├── tests/
└── .claude/             # Instalado por el kit
```

**Testing Framework:** `pytest`

---

## ⚙️ Opciones de Línea de Comandos

### Sintaxis Completa

```bash
python installer.py [OPTIONS]

# O con script wrapper (Unix/macOS)
./install.sh [OPTIONS]
```

### Opciones Disponibles

| Opción | Descripción | Ejemplo |
|--------|-------------|---------|
| `--profile PROFILE` | Perfil a instalar | `--profile pyqt-mvc` |
| `--yes`, `-y` | Aceptar todas las confirmaciones | `-y` |
| `--dry-run` | Simular instalación sin cambios | `--dry-run` |
| `--force` | Sobrescribir archivos existentes | `--force` |
| `--config PATH` | Usar config.yaml personalizado | `--config custom.yaml` |
| `--target DIR` | Directorio destino del proyecto | `--target /path/to/proyecto` |
| `--no-color` | Deshabilitar colores (para CI/CD) | `--no-color` |
| `--skip-validation` | Omitir validación post-instalación | `--skip-validation` |
| `--help`, `-h` | Mostrar ayuda completa | `--help` |

### Ejemplos de Uso

**Instalación interactiva:**
```bash
./install.sh
```

**Instalación rápida con perfil:**
```bash
./install.sh --profile fastapi-rest --yes
```

**Dry-run (ver qué haría sin ejecutar):**
```bash
./install.sh --profile flask-rest --dry-run
```

**Reinstalación (sobrescribir existente):**
```bash
./install.sh --profile pyqt-mvc --force --yes
```

**Instalación en directorio específico:**
```bash
python installer.py --profile generic-python --target /path/to/otro-proyecto
```

**Para CI/CD (sin colores, sin confirmaciones):**
```bash
python installer.py --profile generic-python --yes --no-color
```

---

## 💻 Ejemplos por Sistema Operativo

### macOS

```bash
# 1. Instalar Homebrew (si no está instalado)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Instalar Python 3.8+
brew install python3

# 3. Clonar Claude Dev Kit
git clone https://github.com/vvalotto/claude-dev-kit.git ~/.claude-dev-kit

# 4. Navegar a tu proyecto
cd ~/Projects/mi-proyecto

# 5. Instalar (modo interactivo)
~/.claude-dev-kit/install/install.sh

# 6. Verificar instalación
python3 ~/.claude-dev-kit/scripts/validate-setup.py
```

---

### Linux (Ubuntu/Debian)

```bash
# 1. Actualizar sistema
sudo apt update

# 2. Instalar Python 3.8+
sudo apt install python3 python3-pip git

# 3. Clonar Claude Dev Kit
git clone https://github.com/vvalotto/claude-dev-kit.git ~/.claude-dev-kit

# 4. Navegar a tu proyecto
cd ~/projects/mi-proyecto

# 5. Instalar (con perfil específico)
~/.claude-dev-kit/install/install.sh --profile fastapi-rest --yes

# 6. Verificar instalación
python3 ~/.claude-dev-kit/scripts/validate-setup.py
```

---

### Linux (Fedora/RHEL)

```bash
# 1. Instalar Python 3.8+
sudo dnf install python3 git

# 2. Clonar Claude Dev Kit
git clone https://github.com/vvalotto/claude-dev-kit.git ~/.claude-dev-kit

# 3. Navegar a tu proyecto
cd ~/projects/mi-proyecto

# 4. Instalar
~/.claude-dev-kit/install/install.sh --profile generic-python --yes
```

---

### Windows

```powershell
# 1. Instalar Python 3.8+ desde https://www.python.org/downloads/
# Asegúrate de marcar "Add Python to PATH"

# 2. Instalar Git desde https://git-scm.com/download/win

# 3. Abrir PowerShell y clonar Claude Dev Kit
git clone https://github.com/vvalotto/claude-dev-kit.git C:\claude-dev-kit

# 4. Navegar a tu proyecto
cd C:\Projects\mi-proyecto

# 5. Instalar (modo interactivo)
python C:\claude-dev-kit\install\installer.py

# 6. Verificar instalación
python C:\claude-dev-kit\scripts\validate-setup.py
```

---

## 🔧 Troubleshooting

### Error: Python no encontrado

**Síntoma:**
```
Error: Python 3 no está instalado o no está en PATH
```

**Solución:**

**macOS:**
```bash
brew install python3
```

**Ubuntu/Debian:**
```bash
sudo apt install python3
```

**Windows:**
- Descargar e instalar desde https://www.python.org/downloads/
- ✅ Marcar "Add Python to PATH" durante instalación

---

### Error: Versión de Python incompatible

**Síntoma:**
```
Error: Python 3.7 no es compatible
Se requiere Python 3.8 o superior
```

**Solución:**

Actualiza Python a versión 3.8+:

**macOS:**
```bash
brew upgrade python3
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt upgrade python3
```

**Windows:**
- Descargar última versión desde https://www.python.org/downloads/

---

### Error: .claude/ ya existe

**Síntoma:**
```
⚠️  El directorio .claude/ ya existe.
```

**Soluciones:**

**Opción 1: Usar --force para sobrescribir**
```bash
./install.sh --profile pyqt-mvc --force --yes
```

**Opción 2: Eliminar manualmente**
```bash
rm -rf .claude/
./install.sh
```

**Opción 3: Cancelar y revisar**
Si ya tienes una instalación, verifica qué perfil tienes:
```bash
cat .claude/config.json
```

---

### Error: Permisos insuficientes

**Síntoma:**
```
Permission denied: .claude/
```

**Solución:**

**Unix/Linux:**
```bash
# Verificar permisos del directorio
ls -la

# Cambiar propietario si es necesario
sudo chown -R $USER:$USER .
```

**Windows:**
- Ejecutar PowerShell como Administrador
- O cambiar permisos del directorio del proyecto

---

### Error: installer.py no encontrado

**Síntoma:**
```
Error: No se encontró installer.py
```

**Solución:**

Verifica que clonaste el repositorio correctamente:

```bash
# Verificar que existe
ls ~/.claude-dev-kit/install/installer.py

# Si no existe, clonar nuevamente
git clone https://github.com/vvalotto/claude-dev-kit.git ~/.claude-dev-kit
```

---

### Validación falla después de instalación

**Síntoma:**
```
❌ INSTALACIÓN INCOMPLETA
```

**Solución:**

1. Ejecutar validación en modo verbose:
```bash
python ~/.claude-dev-kit/scripts/validate-setup.py --verbose
```

2. Revisar qué archivos/directorios faltan

3. Reinstalar con --force:
```bash
./install.sh --profile [tu-perfil] --force --yes
```

---

## 🎓 Próximos Pasos

### 1. Verificar Instalación

```bash
python ~/.claude-dev-kit/scripts/validate-setup.py
```

Deberías ver:
```
✅ INSTALACIÓN VÁLIDA
```

### 2. Revisar Archivos Generados

**`.claude/` - Directorio del framework:**
```
.claude/
├── config.json          # Configuración del perfil
├── skills/              # Skills disponibles
├── templates/           # Templates BDD, testing, etc.
└── tracking/            # Sistema de tracking de tiempo
```

**`CLAUDE.md` - Guía del proyecto (si se generó):**
Contiene instrucciones específicas de tu proyecto para Claude Code.

### 3. Configurar tu Proyecto (Opcional)

Edita `.claude/config.json` si necesitas personalizar:
```json
{
  "profile": "pyqt-mvc",
  "version": "1.0",
  "variables": {
    "base_class": "MiClaseBase"
  }
}
```

### 4. Usar Skills Disponibles

**Implementar Historia de Usuario:**
```bash
/implement-us US-001
```

**Comandos de Tracking:**
```bash
/track-status          # Ver estado actual
/track-pause motivo    # Pausar tracking
/track-resume          # Reanudar tracking
/track-report US-001   # Reporte de una US
/track-history         # Historial completo
```

### 5. Documentación Adicional

- **Proyecto Principal:** [README.md](../README.md)
- **Guía del Proyecto:** `CLAUDE.md` (en tu proyecto)
- **Sistema de Tracking:** [Documentación de tracking](../docs/user/tracking/user-guide.md)
- **Skills:** [Skill implement-us](../skills/implement-us/README.md)

---

## 📖 Recursos Adicionales

- **Repositorio:** https://github.com/vvalotto/claude-dev-kit
- **Issues:** https://github.com/vvalotto/claude-dev-kit/issues
- **Documentación completa:** [docs/](../docs/)

---

## 📄 Licencia

MIT License - Ver [LICENSE](../LICENSE) para más detalles.

---

**Versión:** 1.0.0
**Última Actualización:** 2026-02-17
