# TICKET-016: Crear install/install.ps1 (script para Windows PowerShell)

**Fase:** 2 - Sistema de Instalación
**Sprint:** 1
**Estado:** PENDING
**Prioridad:** Baja
**Estimación:** 1 hora
**Asignado a:** Claude Code

## Descripción

Crear el script PowerShell `install/install.ps1` que sirve como wrapper para ejecutar el instalador Python en sistemas Windows. Similar a install.sh pero para Windows PowerShell.

Este script verifica Python, configura execution policy si es necesario, y ejecuta el instalador.

## Criterios de Aceptación

- [ ] Archivo `install/install.ps1` creado
- [ ] Verifica que Python 3 esté disponible en PATH
- [ ] Detecta ruta correcta a installer.py
- [ ] Pasa todos los argumentos CLI a installer.py
- [ ] Maneja error si Python no está disponible
- [ ] Mensajes de error claros con colores
- [ ] Funciona en Windows 10/11
- [ ] Documentación de uso

## Dependencias

- **Depende de:** TICKET-013 (installer.py debe existir)
- **Bloquea a:** TICKET-018 (testing en Windows)

## Notas Técnicas

### Contenido del Script

```powershell
# Claude Dev Kit - Instalador (Windows PowerShell)
# Wrapper para ejecutar installer.py

[CmdletBinding()]
param(
    [Parameter(ValueFromRemainingArguments=$true)]
    $RemainingArgs
)

# Configurar colores
$ErrorColor = "Red"
$SuccessColor = "Green"
$WarningColor = "Yellow"

# Detectar directorio del script
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$InstallerPy = Join-Path $ScriptDir "installer.py"

# Función para verificar Python
function Test-Python {
    try {
        $pythonVersion = & python --version 2>&1
        if ($pythonVersion -match "Python (\d+)\.(\d+)") {
            $major = [int]$matches[1]
            $minor = [int]$matches[2]
            if ($major -eq 3 -and $minor -ge 8) {
                return $true
            }
        }
    } catch {
        return $false
    }
    return $false
}

# Verificar Python está disponible
Write-Host "Verificando Python..." -ForegroundColor $SuccessColor

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Python no está instalado o no está en PATH" -ForegroundColor $ErrorColor
    Write-Host "Por favor instala Python 3.8 o superior desde:" -ForegroundColor $WarningColor
    Write-Host "  https://www.python.org/downloads/"
    exit 1
}

# Verificar versión de Python
if (-not (Test-Python)) {
    Write-Host "Error: Se requiere Python 3.8 o superior" -ForegroundColor $ErrorColor
    Write-Host "Version actual: $(python --version)" -ForegroundColor $WarningColor
    exit 1
}

# Verificar que installer.py existe
if (-not (Test-Path $InstallerPy)) {
    Write-Host "Error: No se encontró installer.py en $InstallerPy" -ForegroundColor $ErrorColor
    exit 1
}

# Ejecutar instalador
Write-Host "Ejecutando Claude Dev Kit Installer..." -ForegroundColor $SuccessColor
& python $InstallerPy @RemainingArgs

exit $LASTEXITCODE
```

### Execution Policy

En Windows, puede ser necesario permitir ejecución de scripts:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Uso

```powershell
# Instalación interactiva
.\install\install.ps1

# Con perfil específico
.\install\install.ps1 --profile pyqt-mvc

# Dry-run
.\install\install.ps1 --profile fastapi-rest --dry-run
```

## Checklist de Implementación

- [ ] Crear archivo install/install.ps1
- [ ] Implementar parámetros con [CmdletBinding()]
- [ ] Implementar Test-Python function
- [ ] Implementar verificación de Python disponible
- [ ] Implementar verificación de versión >=3.8
- [ ] Implementar detección de ruta a installer.py
- [ ] Implementar paso de argumentos con @RemainingArgs
- [ ] Agregar mensajes con colores (Write-Host -ForegroundColor)
- [ ] Manejar exit codes correctamente
- [ ] Documentar execution policy en comentarios
- [ ] Agregar comentarios explicativos

## Resultado

**Fecha de Completado:** _Pendiente_

**Nota:** Este ticket puede ser completado sin testing en Windows si no hay acceso a un sistema Windows. El script puede ser verificado sintácticamente.

### Archivo Creado

_A completar al finalizar_

### Testing

_A completar al finalizar (o marcar como "no testeado en Windows")_

**Estado:** ⏳ Pendiente
