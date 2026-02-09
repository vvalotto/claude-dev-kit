# TICKET-015: Crear install/install.sh (script para Unix/macOS)

**Fase:** 2 - Sistema de Instalación
**Sprint:** 1
**Estado:** PENDING
**Prioridad:** Media
**Estimación:** 1 hora
**Asignado a:** Claude Code

## Descripción

Crear el script shell `install/install.sh` que sirve como wrapper para ejecutar el instalador Python en sistemas Unix/macOS. Este script verifica que Python esté disponible y pasa todos los argumentos al `installer.py`.

Proporciona una interfaz más amigable para usuarios Unix/macOS que preferirían ejecutar `./install.sh` en lugar de `python install/installer.py`.

## Criterios de Aceptación

- [ ] Archivo `install/install.sh` creado
- [ ] Shebang correcto (`#!/usr/bin/env bash`)
- [ ] Verifica que Python 3 esté disponible
- [ ] Detecta ruta correcta a installer.py (relativa al script)
- [ ] Pasa todos los argumentos CLI a installer.py
- [ ] Maneja error si Python no está disponible
- [ ] Tiene permisos de ejecución (`chmod +x`)
- [ ] Funciona en macOS y Linux
- [ ] Mensajes de error claros

## Dependencias

- **Depende de:** TICKET-013 (installer.py debe existir)
- **Bloquea a:** TICKET-018 (testing)

## Notas Técnicas

### Contenido del Script

```bash
#!/usr/bin/env bash

# Claude Dev Kit - Instalador (Unix/macOS)
# Wrapper para ejecutar installer.py

set -e  # Exit on error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Detectar directorio del script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALLER_PY="${SCRIPT_DIR}/installer.py"

# Verificar que Python 3 está disponible
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 no está instalado o no está en PATH${NC}"
    echo "Por favor instala Python 3.8 o superior:"
    echo "  - macOS: brew install python3"
    echo "  - Ubuntu/Debian: sudo apt install python3"
    exit 1
fi

# Verificar versión de Python (>=3.8)
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.8"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    echo -e "${RED}Error: Python ${PYTHON_VERSION} no es compatible${NC}"
    echo "Se requiere Python 3.8 o superior"
    exit 1
fi

# Verificar que installer.py existe
if [ ! -f "${INSTALLER_PY}" ]; then
    echo -e "${RED}Error: No se encontró installer.py en ${INSTALLER_PY}${NC}"
    exit 1
fi

# Ejecutar instalador pasando todos los argumentos
echo -e "${GREEN}Ejecutando Claude Dev Kit Installer...${NC}"
python3 "${INSTALLER_PY}" "$@"
```

### Hacer Ejecutable

```bash
chmod +x install/install.sh
```

### Uso

```bash
# Instalación interactiva
./install/install.sh

# Con perfil específico
./install/install.sh --profile pyqt-mvc

# Dry-run
./install/install.sh --profile fastapi-rest --dry-run
```

## Checklist de Implementación

- [ ] Crear archivo install/install.sh
- [ ] Agregar shebang `#!/usr/bin/env bash`
- [ ] Implementar verificación de Python 3
- [ ] Implementar verificación de versión Python >=3.8
- [ ] Implementar detección de ruta a installer.py
- [ ] Implementar paso de argumentos con "$@"
- [ ] Agregar mensajes de error con colores
- [ ] Agregar `set -e` para exit on error
- [ ] Hacer ejecutable con chmod +x
- [ ] Testear en macOS
- [ ] Agregar comentarios explicativos

## Resultado

**Fecha de Completado:** _Pendiente_

### Archivo Creado

_A completar al finalizar_

### Testing

_A completar al finalizar_

**Estado:** ⏳ Pendiente
