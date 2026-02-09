# TICKET-014: Crear scripts/validate-setup.py

**Fase:** 2 - Sistema de Instalación
**Sprint:** 1
**Estado:** DONE
**Prioridad:** Alta
**Estimación:** 2 horas
**Asignado a:** Claude Code

## Descripción

Crear el script `scripts/validate-setup.py` que valida que una instalación del Claude Dev Kit fue exitosa. Este script verifica directorios requeridos, archivos críticos, configuración válida, e imports Python.

El instalador ejecuta este script automáticamente al finalizar, pero también puede ejecutarse manualmente para diagnosticar problemas.

## Criterios de Aceptación

- [ ] Script `scripts/validate-setup.py` funcional
- [ ] Verifica existencia de directorios requeridos
- [ ] Verifica existencia de archivos críticos
- [ ] Valida sintaxis de config JSON
- [ ] Valida que imports Python funcionan (tracking module)
- [ ] Verifica permisos de ejecución en hooks (si existen)
- [ ] Genera reporte de validación legible
- [ ] Retorna exit code apropiado (0 = OK, 1 = ERROR)
- [ ] Modo verbose con --verbose flag
- [ ] Colores en terminal con opción --no-color

## Dependencias

- **Depende de:** TICKET-012 (config.yaml define qué validar)
- **Bloquea a:** TICKET-013 (instalador llama a validación)

## Notas Técnicas

### Flags CLI

```bash
python validate-setup.py [OPTIONS]

Options:
  --target DIR         Directory to validate (default: current dir)
  --verbose, -v        Show detailed validation info
  --no-color           Disable colored output
  --help               Show help message
```

### Estructura del Código

```python
#!/usr/bin/env python3
"""
Claude Dev Kit - Validador de Instalación
"""

import sys
import json
from pathlib import Path
from typing import List, Tuple
import logging

class SetupValidator:
    def __init__(self, target_dir: Path):
        self.target_dir = target_dir
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate_directories(self) -> bool:
        """Verificar directorios requeridos existen"""
        required = [
            ".claude",
            ".claude/skills",
            ".claude/templates",
            ".claude/tracking"
        ]
        # ...

    def validate_files(self) -> bool:
        """Verificar archivos críticos existen"""
        required = [
            ".claude/config.json",
            ".claude/skills/implement-us/SKILL.md",
            ".claude/tracking/time_tracker.py"
        ]
        # ...

    def validate_config_json(self) -> bool:
        """Validar config.json es JSON válido"""
        # ...

    def validate_python_imports(self) -> bool:
        """Validar imports Python funcionan"""
        # Test: from .claude.tracking import time_tracker
        # ...

    def validate_permissions(self) -> bool:
        """Validar permisos de ejecución en hooks"""
        # ...

    def generate_report(self) -> str:
        """Generar reporte de validación"""
        # ...

    def run(self) -> int:
        """Ejecutar todas las validaciones y retornar exit code"""
        # ...

def main():
    validator = SetupValidator(...)
    exit_code = validator.run()
    sys.exit(exit_code)
```

### Validaciones a Realizar

1. **Estructura de Directorios**
   - `.claude/` existe
   - `.claude/skills/` existe
   - `.claude/templates/bdd/` existe
   - `.claude/tracking/` existe

2. **Archivos Críticos**
   - `.claude/config.json` existe
   - `.claude/skills/implement-us/SKILL.md` existe
   - `.claude/tracking/time_tracker.py` existe

3. **Configuración JSON**
   - `.claude/config.json` es JSON válido
   - Tiene keys requeridos (profile, version)

4. **Imports Python**
   - `from tracking import time_tracker` funciona
   - No hay SyntaxErrors en archivos Python

5. **Permisos** (opcional)
   - Hooks tienen permisos de ejecución (si existen)

### Formato de Reporte

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Claude Dev Kit - Validación de Instalación
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Target: /Users/user/mi-proyecto

✅ Estructura de Directorios... OK
✅ Archivos Críticos........... OK
✅ Configuración JSON.......... OK
✅ Imports Python.............. OK
⚠️  Permisos de Hooks.......... WARNING (hooks no encontrados)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Resultado: ✅ INSTALACIÓN VÁLIDA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Checklist de Implementación

- [ ] Crear estructura base del script
- [ ] Implementar clase SetupValidator
- [ ] Implementar validate_directories()
- [ ] Implementar validate_files()
- [ ] Implementar validate_config_json()
- [ ] Implementar validate_python_imports()
- [ ] Implementar validate_permissions()
- [ ] Implementar generate_report() con formato bonito
- [ ] Implementar run() orquestando validaciones
- [ ] Agregar parsing de argumentos CLI
- [ ] Agregar soporte para colores en terminal
- [ ] Agregar modo verbose
- [ ] Manejar exit codes correctamente
- [ ] Documentar código con docstrings

## Resultado

**Fecha de Completado:** 2026-02-09

### Funcionalidad Implementada

✅ **Clase SetupValidator completa** (536 líneas)
- validate_directories(): 9 directorios requeridos
- validate_files(): 5 archivos críticos
- validate_config_json(): Validación JSON + keys
- validate_python_imports(): Imports tracking module
- validate_permissions(): Hooks opcionales
- generate_report(): Reporte formateado
- run(): Orquestación completa

✅ **Dataclasses**
- ValidationResult: Resultado individual
- ValidationReport: Reporte completo con estadísticas

✅ **Flags CLI**
- --target, --verbose, --no-color
- Exit codes apropiados (0/1)
- Help message completo

✅ **Características**
- Colores con clase Colors
- Reporte profesional con emojis
- Warnings vs errores
- Modo verbose detallado

### Testing Manual

- ✅ Sintaxis Python correcta
- ✅ Archivo ejecutable
- ✅ --help funciona
- ⏳ Testing end-to-end en TICKET-018

### Commit

- ✅ Commit: c25708c

**Estado:** ✅ Completado
