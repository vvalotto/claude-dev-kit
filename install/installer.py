#!/usr/bin/env python3
"""
Claude Dev Kit - Instalador Multiplataforma

Instala el Claude Dev Kit en un proyecto Python, copiando skills, templates y
sistema de tracking al directorio .claude/ del proyecto.

Uso:
    # Interactivo
    python installer.py

    # No-interactivo con perfil
    python installer.py --profile pyqt-mvc --yes

    # Dry-run
    python installer.py --profile fastapi-rest --dry-run

Autor: Victor Valotto
Versión: 1.0.0
"""

import argparse
import sys
import shutil
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime


# =============================================================================
# CONFIGURACIÓN DE COLORES PARA TERMINAL
# =============================================================================

class Colors:
    """Códigos ANSI para colores en terminal"""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    MAGENTA = '\033[0;35m'
    CYAN = '\033[0;36m'
    BOLD = '\033[1m'
    NC = '\033[0m'  # No Color

    @staticmethod
    def disable():
        """Deshabilitar colores (para --no-color)"""
        Colors.RED = ''
        Colors.GREEN = ''
        Colors.YELLOW = ''
        Colors.BLUE = ''
        Colors.MAGENTA = ''
        Colors.CYAN = ''
        Colors.BOLD = ''
        Colors.NC = ''


# =============================================================================
# CLASE PRINCIPAL DEL INSTALADOR
# =============================================================================

class ClaudeDevKitInstaller:
    """
    Instalador del Claude Dev Kit.

    Este instalador copia el framework al proyecto del usuario, fusiona
    configuraciones según el perfil seleccionado, y ejecuta validaciones.
    """

    def __init__(self, config_path: Path, kit_root: Path):
        """
        Inicializar instalador.

        Args:
            config_path: Ruta al archivo config.yaml
            kit_root: Directorio raíz del Claude Dev Kit
        """
        self.kit_root = kit_root
        self.config_path = config_path
        self.config = self.load_config(config_path)
        self.logger = self.setup_logging()

    def setup_logging(self) -> logging.Logger:
        """Configurar sistema de logging"""
        logger = logging.getLogger('installer')
        logger.setLevel(logging.INFO)

        # Handler para consola
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(levelname)s: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger

    def load_config(self, path: Path) -> Dict[str, Any]:
        """
        Cargar configuración desde config.yaml.

        Args:
            path: Ruta al archivo config.yaml

        Returns:
            Diccionario con configuración

        Raises:
            FileNotFoundError: Si config.yaml no existe
            yaml.YAMLError: Si YAML es inválido
        """
        if not path.exists():
            raise FileNotFoundError(
                f"{Colors.RED}Error: config.yaml no encontrado en {path}{Colors.NC}"
            )

        try:
            with open(path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            return config
        except yaml.YAMLError as e:
            raise yaml.YAMLError(
                f"{Colors.RED}Error: config.yaml inválido: {e}{Colors.NC}"
            )

    def select_profile_interactive(self) -> str:
        """
        Selector interactivo de perfil.

        Muestra menú con perfiles disponibles y retorna el seleccionado.

        Returns:
            Nombre del perfil seleccionado
        """
        profiles = self.config['profiles']

        # Mostrar mensaje de bienvenida
        print(self.config['messages']['welcome'])

        # Mostrar perfiles disponibles
        print(f"{Colors.BOLD}Perfiles disponibles:{Colors.NC}\n")

        profile_list = list(profiles.keys())
        for i, profile_key in enumerate(profile_list, 1):
            profile = profiles[profile_key]
            print(f"{Colors.CYAN}{i}. {profile['name']}{Colors.NC} ({profile_key})")
            print(f"   {profile['description']}\n")

        # Solicitar selección
        while True:
            try:
                choice = input(f"{Colors.BOLD}Selecciona un perfil [1-{len(profile_list)}]: {Colors.NC}")
                choice_num = int(choice)

                if 1 <= choice_num <= len(profile_list):
                    selected = profile_list[choice_num - 1]
                    print(f"\n{Colors.GREEN}✓ Perfil seleccionado: {profiles[selected]['name']}{Colors.NC}\n")
                    return selected
                else:
                    print(f"{Colors.RED}Por favor, selecciona un número entre 1 y {len(profile_list)}{Colors.NC}")
            except ValueError:
                print(f"{Colors.RED}Por favor, ingresa un número válido{Colors.NC}")
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}Instalación cancelada por el usuario{Colors.NC}")
                sys.exit(0)

    def validate_profile(self, profile: str) -> bool:
        """
        Validar que el perfil existe.

        Args:
            profile: Nombre del perfil a validar

        Returns:
            True si el perfil es válido
        """
        if profile not in self.config['profiles']:
            available = ', '.join(self.config['profiles'].keys())
            self.logger.error(
                f"{Colors.RED}Perfil inválido: {profile}{Colors.NC}\n"
                f"Perfiles disponibles: {available}"
            )
            return False
        return True

    def check_target_dir(self, target_dir: Path, force: bool = False) -> bool:
        """
        Verificar si el directorio destino ya existe.

        Args:
            target_dir: Directorio destino (.claude/)
            force: Si True, sobrescribir sin preguntar

        Returns:
            True si se puede continuar
        """
        if not target_dir.exists():
            return True

        if force:
            self.logger.warning(
                f"{Colors.YELLOW}Sobrescribiendo {target_dir} (--force){Colors.NC}"
            )
            return True

        # Mostrar mensaje de advertencia
        print(self.config['messages']['already_exists'])

        response = input(f"{Colors.BOLD}¿Sobrescribir? [s/N]: {Colors.NC}").lower()
        return response in ['s', 'y', 'yes', 'si', 'sí']

    def copy_framework_files(self, target_dir: Path, dry_run: bool = False) -> None:
        """
        Copiar archivos del framework al proyecto destino.

        Args:
            target_dir: Directorio destino (usualmente .claude/)
            dry_run: Si True, solo mostrar qué se haría sin ejecutar
        """
        copy_rules = self.config['installation']['copy_rules']

        self.logger.info(f"{Colors.BOLD}Copiando archivos del framework...{Colors.NC}")

        for rule in copy_rules:
            source = self.kit_root / rule['source']
            target = Path(str(rule['target']).format(target_dir=target_dir))

            if not source.exists():
                self.logger.warning(
                    f"{Colors.YELLOW}⚠️  Fuente no existe: {source}{Colors.NC}"
                )
                continue

            action = "[DRY-RUN] " if dry_run else ""
            self.logger.info(
                f"{action}{Colors.CYAN}Copiando {rule['description']}...{Colors.NC}"
            )
            self.logger.info(f"  {source} → {target}")

            if not dry_run:
                if target.exists():
                    shutil.rmtree(target)

                if source.is_dir():
                    shutil.copytree(source, target)
                else:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, target)

    def merge_configs(self, profile: str) -> Dict[str, Any]:
        """
        Fusionar configuración base con perfil seleccionado.

        Args:
            profile: Nombre del perfil seleccionado

        Returns:
            Configuración fusionada
        """
        profile_config = self.config['profiles'][profile]

        merged = {
            'version': self.config['version'],
            'profile': profile,
            'profile_name': profile_config['name'],
            'installed_at': datetime.now().isoformat(),
            'architecture_pattern': profile_config['architecture_pattern'],
            'test_framework': profile_config['test_framework'],
            'component_types': profile_config['component_types'],
            'patterns': profile_config['patterns'],
            'variables': profile_config.get('variables', {})
        }

        return merged

    def generate_config_json(self, target_dir: Path, profile: str, dry_run: bool = False) -> None:
        """
        Generar archivo .claude/config.json con configuración fusionada.

        Args:
            target_dir: Directorio destino (.claude/)
            profile: Perfil seleccionado
            dry_run: Si True, solo mostrar sin ejecutar
        """
        config_file = target_dir / 'config.json'
        merged_config = self.merge_configs(profile)

        action = "[DRY-RUN] " if dry_run else ""
        self.logger.info(f"{action}{Colors.CYAN}Generando config.json...{Colors.NC}")

        if not dry_run:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(merged_config, f, indent=2, ensure_ascii=False)

    def generate_claude_md(self, project_dir: Path, profile: str, dry_run: bool = False) -> None:
        """
        Generar CLAUDE.md si no existe.

        Args:
            project_dir: Directorio del proyecto
            profile: Perfil seleccionado
            dry_run: Si True, solo mostrar sin ejecutar
        """
        claude_md = project_dir / 'CLAUDE.md'

        if claude_md.exists():
            self.logger.info(f"{Colors.CYAN}CLAUDE.md ya existe, omitiendo...{Colors.NC}")
            return

        profile_config = self.config['profiles'][profile]

        content = f"""# CLAUDE.md

Este archivo proporciona orientación a Claude Code al trabajar con este proyecto.

---

## Perfil del Proyecto

**Stack:** {profile_config['name']}
**Patrón Arquitectónico:** {profile_config['architecture_pattern']}
**Framework de Testing:** {profile_config['test_framework']}

## Tipos de Componentes

{chr(10).join(f'- {ct}' for ct in profile_config['component_types'])}

## Patrones de Diseño Comunes

{chr(10).join(f'- {p}' for p in profile_config['patterns'])}

---

## Claude Dev Kit Instalado

Este proyecto tiene instalado el Claude Dev Kit en `.claude/`.

### Skills Disponibles

- `/implement-us`: Implementar historias de usuario con metodología BDD

### Comandos de Tracking

- `/track-pause [razón]`: Pausar tracking de tiempo
- `/track-resume`: Reanudar tracking
- `/track-status`: Ver estado actual
- `/track-report [us_id]`: Generar reporte de US
- `/track-history`: Ver historial de tracking

---

**Instalado:** {datetime.now().strftime('%Y-%m-%d')}
**Perfil:** {profile}
"""

        action = "[DRY-RUN] " if dry_run else ""
        self.logger.info(f"{action}{Colors.CYAN}Generando CLAUDE.md...{Colors.NC}")

        if not dry_run:
            with open(claude_md, 'w', encoding='utf-8') as f:
                f.write(content)

    def run_validation(self, project_dir: Path, dry_run: bool = False) -> bool:
        """
        Ejecutar validación post-instalación.

        Args:
            project_dir: Directorio del proyecto
            dry_run: Si True, omitir validación

        Returns:
            True si la validación pasó
        """
        if dry_run:
            self.logger.info(f"{Colors.CYAN}[DRY-RUN] Validación omitida{Colors.NC}")
            return True

        validate_script = self.kit_root.parent / 'scripts' / 'validate-setup.py'

        if not validate_script.exists():
            self.logger.warning(
                f"{Colors.YELLOW}validate-setup.py no encontrado, omitiendo validación{Colors.NC}"
            )
            return True

        self.logger.info(
            f"\n{self.config['messages']['validation_running']}"
        )

        # Por ahora, retornamos True ya que validate-setup.py se implementará después
        # TODO: Ejecutar validate-setup.py cuando esté disponible
        self.logger.info(f"{Colors.GREEN}✓ Validación pendiente (TICKET-014){Colors.NC}")
        return True

    def install(
        self,
        profile: str,
        project_dir: Path,
        force: bool = False,
        dry_run: bool = False,
        skip_validation: bool = False
    ) -> bool:
        """
        Ejecutar instalación completa.

        Args:
            profile: Perfil a instalar
            project_dir: Directorio del proyecto destino
            force: Sobrescribir archivos existentes
            dry_run: Modo dry-run (mostrar sin ejecutar)
            skip_validation: Omitir validación post-instalación

        Returns:
            True si la instalación fue exitosa
        """
        try:
            # Validar perfil
            if not self.validate_profile(profile):
                return False

            # Determinar directorio destino
            target_dir = project_dir / self.config['installation']['target_dir']

            # Verificar si ya existe
            if not self.check_target_dir(target_dir, force):
                self.logger.info(f"{Colors.YELLOW}Instalación cancelada{Colors.NC}")
                return False

            # Crear directorio destino
            if not dry_run:
                target_dir.mkdir(parents=True, exist_ok=True)

            # Copiar archivos del framework
            self.copy_framework_files(target_dir, dry_run)

            # Generar config.json
            self.generate_config_json(target_dir, profile, dry_run)

            # Generar CLAUDE.md si no existe
            if self.config['installation']['create_claude_md']:
                self.generate_claude_md(project_dir, profile, dry_run)

            # Ejecutar validación
            if not skip_validation and not dry_run:
                if not self.run_validation(project_dir, dry_run):
                    self.logger.error(f"{Colors.RED}Validación falló{Colors.NC}")
                    return False

            # Mensaje de éxito
            if not dry_run:
                print(self.config['messages']['success'])
            else:
                print(f"\n{Colors.GREEN}[DRY-RUN] Instalación simulada exitosamente{Colors.NC}\n")

            return True

        except Exception as e:
            self.logger.error(f"{Colors.RED}Error durante instalación: {e}{Colors.NC}")
            return False


# =============================================================================
# FUNCIÓN PRINCIPAL
# =============================================================================

def main():
    """Punto de entrada principal del instalador"""

    # Determinar directorio raíz del kit
    script_dir = Path(__file__).parent
    kit_root = script_dir.parent
    config_path = script_dir / 'config.yaml'

    # Parser de argumentos
    parser = argparse.ArgumentParser(
        description='Claude Dev Kit - Instalador Multiplataforma',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  # Instalación interactiva
  python installer.py

  # Instalación con perfil específico
  python installer.py --profile pyqt-mvc --yes

  # Dry-run (simular instalación)
  python installer.py --profile fastapi-rest --dry-run

  # Sobrescribir instalación existente
  python installer.py --profile django-mvt --force --yes

Perfiles disponibles:
  - pyqt-mvc: PyQt6 + MVC architecture
  - fastapi-rest: FastAPI + REST APIs
  - django-mvt: Django + MVT pattern
  - generic-python: Generic Python projects
        """
    )

    parser.add_argument(
        '--profile',
        type=str,
        help='Perfil a instalar (pyqt-mvc, fastapi-rest, django-mvt, generic-python)'
    )

    parser.add_argument(
        '--yes', '-y',
        action='store_true',
        help='Aceptar todas las confirmaciones automáticamente'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Mostrar qué se haría sin ejecutar cambios'
    )

    parser.add_argument(
        '--force',
        action='store_true',
        help='Sobrescribir archivos existentes sin preguntar'
    )

    parser.add_argument(
        '--config',
        type=Path,
        default=config_path,
        help=f'Ruta al config.yaml (default: {config_path})'
    )

    parser.add_argument(
        '--target',
        type=Path,
        default=Path.cwd(),
        help='Directorio del proyecto destino (default: directorio actual)'
    )

    parser.add_argument(
        '--no-color',
        action='store_true',
        help='Deshabilitar colores en output'
    )

    parser.add_argument(
        '--skip-validation',
        action='store_true',
        help='Omitir validación post-instalación'
    )

    args = parser.parse_args()

    # Deshabilitar colores si se solicita
    if args.no_color:
        Colors.disable()

    # Verificar versión de Python
    if sys.version_info < (3, 8):
        print(f"{Colors.RED}Error: Se requiere Python 3.8 o superior{Colors.NC}")
        print(f"Versión actual: {sys.version}")
        sys.exit(1)

    try:
        # Crear instalador
        installer = ClaudeDevKitInstaller(args.config, kit_root)

        # Determinar perfil
        if args.profile:
            profile = args.profile
        else:
            # Modo interactivo
            profile = installer.select_profile_interactive()

        # Ejecutar instalación
        success = installer.install(
            profile=profile,
            project_dir=args.target,
            force=args.force,
            dry_run=args.dry_run,
            skip_validation=args.skip_validation
        )

        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Instalación cancelada por el usuario{Colors.NC}")
        sys.exit(130)
    except Exception as e:
        print(f"{Colors.RED}Error fatal: {e}{Colors.NC}")
        sys.exit(1)


if __name__ == '__main__':
    main()
