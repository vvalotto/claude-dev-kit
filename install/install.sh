#!/usr/bin/env bash

# Claude Dev Kit - Instalador (Unix/macOS)
# Wrapper para ejecutar installer.py
#
# Este script verifica que Python 3.8+ esté disponible y ejecuta el
# instalador Python, pasando todos los argumentos recibidos.
#
# Uso:
#   ./install.sh                    # Instalación interactiva
#   ./install.sh --profile pyqt-mvc # Instalación con perfil específico
#   ./install.sh --help             # Ver ayuda completa

set -e  # Exit on error

# =============================================================================
# COLORES PARA OUTPUT
# =============================================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# =============================================================================
# CONFIGURACIÓN
# =============================================================================

# Detectar directorio del script (funciona incluso si se invoca desde otro dir)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALLER_PY="${SCRIPT_DIR}/installer.py"

# Versión mínima requerida de Python
REQUIRED_PYTHON_MAJOR=3
REQUIRED_PYTHON_MINOR=8

# =============================================================================
# FUNCIONES DE VALIDACIÓN
# =============================================================================

check_python_installed() {
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}${BOLD}Error: Python 3 no está instalado o no está en PATH${NC}"
        echo ""
        echo "Por favor instala Python 3.8 o superior:"
        echo -e "  ${CYAN}macOS:${NC}          brew install python3"
        echo -e "  ${CYAN}Ubuntu/Debian:${NC}  sudo apt install python3"
        echo -e "  ${CYAN}Fedora/RHEL:${NC}    sudo dnf install python3"
        echo ""
        exit 1
    fi
}

check_python_version() {
    # Obtener versión de Python
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')

    # Verificar versión >= 3.8
    if ! python3 -c "import sys; exit(0 if sys.version_info >= ($REQUIRED_PYTHON_MAJOR, $REQUIRED_PYTHON_MINOR) else 1)" 2>/dev/null; then
        echo -e "${RED}${BOLD}Error: Python ${PYTHON_VERSION} no es compatible${NC}"
        echo ""
        echo "Se requiere Python ${REQUIRED_PYTHON_MAJOR}.${REQUIRED_PYTHON_MINOR} o superior"
        echo "Versión actual: Python ${PYTHON_VERSION}"
        echo ""
        echo "Por favor actualiza Python:"
        echo -e "  ${CYAN}macOS:${NC}          brew upgrade python3"
        echo -e "  ${CYAN}Ubuntu/Debian:${NC}  sudo apt upgrade python3"
        echo ""
        exit 1
    fi
}

check_installer_exists() {
    if [ ! -f "${INSTALLER_PY}" ]; then
        echo -e "${RED}${BOLD}Error: No se encontró installer.py${NC}"
        echo ""
        echo "Ruta esperada: ${INSTALLER_PY}"
        echo ""
        echo "Por favor verifica que el Claude Dev Kit esté correctamente clonado."
        exit 1
    fi
}

# =============================================================================
# FUNCIÓN PRINCIPAL
# =============================================================================

main() {
    # Banner
    echo -e "${CYAN}${BOLD}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  Claude Dev Kit - Installer (Unix/macOS)"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${NC}"

    # Verificaciones
    echo -e "${BOLD}Verificando requisitos...${NC}"

    check_python_installed
    echo -e "${GREEN}✓${NC} Python 3 encontrado"

    check_python_version
    echo -e "${GREEN}✓${NC} Python ${PYTHON_VERSION} (compatible)"

    check_installer_exists
    echo -e "${GREEN}✓${NC} installer.py encontrado"

    echo ""

    # Ejecutar instalador Python pasando todos los argumentos
    echo -e "${GREEN}${BOLD}Ejecutando instalador...${NC}"
    echo ""

    python3 "${INSTALLER_PY}" "$@"

    # Capturar exit code del instalador
    EXIT_CODE=$?

    echo ""

    if [ $EXIT_CODE -eq 0 ]; then
        echo -e "${GREEN}${BOLD}✓ Instalación completada${NC}"
    else
        echo -e "${RED}${BOLD}✗ Instalación falló (exit code: $EXIT_CODE)${NC}"
    fi

    exit $EXIT_CODE
}

# =============================================================================
# EJECUTAR
# =============================================================================

main "$@"
