# TICKET-013: Desarrollar install/installer.py

**Fase:** 2 - Sistema de Instalación
**Sprint:** 1
**Estado:** PENDING
**Prioridad:** Crítica
**Estimación:** 4 horas
**Asignado a:** Claude Code

## Descripción

Desarrollar el instalador Python multiplataforma (`install/installer.py`) que es el componente core del sistema de instalación. Este script copia el framework al proyecto del usuario, fusiona configuraciones según el perfil seleccionado, y ejecuta validaciones.

El instalador debe soportar tanto modo interactivo (con prompts) como no-interactivo (con flags CLI).

## Criterios de Aceptación

- [ ] Script `install/installer.py` funcional y ejecutable
- [ ] Modo interactivo: selector de perfil funcionando
- [ ] Modo no-interactivo: flags --profile, --yes, --dry-run, --force funcionando
- [ ] Copia correcta de skills/ → .claude/skills/
- [ ] Copia correcta de templates/ → .claude/templates/
- [ ] Copia correcta de tracking/ → .claude/tracking/
- [ ] Fusión de config base + perfil seleccionado
- [ ] Generación de CLAUDE.md si no existe
- [ ] Ejecución automática de validate-setup.py al finalizar
- [ ] Logging claro con niveles (INFO, WARNING, ERROR)
- [ ] Manejo robusto de errores y excepciones
- [ ] Uso de pathlib para compatibilidad cross-platform

## Dependencias

- **Depende de:** TICKET-011 (tracking migrado), TICKET-012 (config.yaml creado)
- **Bloquea a:** TICKET-018 (testing del instalador)

## Notas Técnicas

### Flags CLI

```bash
python installer.py [OPTIONS]

Options:
  --profile PROFILE    Profile: pyqt-mvc, fastapi-rest, django-mvt, generic-python
  --yes, -y            Skip confirmations
  --dry-run            Show actions without executing
  --force              Overwrite existing files
  --config PATH        Use custom config file (default: config.yaml)
  --local              Install from local clone
  --help               Show help message
```

### Estructura del Código

```python
#!/usr/bin/env python3
"""
Claude Dev Kit - Instalador Multiplataforma
"""

import argparse
import shutil
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional
import logging

class ClaudeDevKitInstaller:
    def __init__(self, config_path: Path):
        self.config = self.load_config(config_path)
        self.setup_logging()

    def load_config(self, path: Path) -> Dict:
        """Cargar configuración desde config.yaml"""
        pass

    def select_profile_interactive(self) -> str:
        """Selector interactivo de perfil"""
        pass

    def merge_configs(self, base_config: Dict, profile: str) -> Dict:
        """Fusionar config base + perfil seleccionado"""
        pass

    def copy_framework_files(self, target_dir: Path, dry_run: bool = False):
        """Copiar skills, templates, tracking al proyecto"""
        pass

    def generate_claude_md(self, target_dir: Path, profile: str):
        """Generar CLAUDE.md si no existe"""
        pass

    def run_validation(self, target_dir: Path):
        """Ejecutar validate-setup.py"""
        pass

    def install(self, profile: str, target_dir: Path, options: Dict):
        """Ejecutar instalación completa"""
        pass

def main():
    parser = argparse.ArgumentParser(...)
    # ... args parsing
    installer = ClaudeDevKitInstaller(...)
    installer.install(...)
```

### Casos a Manejar

1. **Directorio .claude/ ya existe**: Pedir confirmación o usar --force
2. **Archivos existentes**: Skip, overwrite, o ask según config
3. **Python version incompatible**: Verificar >= 3.8
4. **Config.yaml no encontrado**: Error claro
5. **Perfil inválido**: Mostrar perfiles disponibles
6. **Permisos insuficientes**: Error claro de permisos

## Checklist de Implementación

- [ ] Crear estructura base del script
- [ ] Implementar clase ClaudeDevKitInstaller
- [ ] Implementar load_config() con YAML parsing
- [ ] Implementar select_profile_interactive() con menú
- [ ] Implementar parsing de argumentos CLI
- [ ] Implementar copy_framework_files() con pathlib
- [ ] Implementar merge_configs() para fusionar configs
- [ ] Implementar generate_claude_md() si no existe
- [ ] Implementar run_validation() llamando a validate-setup.py
- [ ] Implementar install() orquestando todo el proceso
- [ ] Agregar logging comprehensivo
- [ ] Agregar manejo de errores
- [ ] Agregar --dry-run mode
- [ ] Agregar tests unitarios básicos
- [ ] Documentar código con docstrings

## Resultado

**Fecha de Completado:** _Pendiente_

### Funcionalidad Implementada

_A completar al finalizar_

### Testing Manual

_A completar al finalizar_

**Estado:** ⏳ Pendiente
