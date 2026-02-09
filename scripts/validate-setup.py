#!/usr/bin/env python3
"""
Claude Dev Kit - Validador de Instalación

Valida que una instalación del Claude Dev Kit fue exitosa, verificando
directorios requeridos, archivos críticos, configuración, e imports Python.

Uso:
    # Validar directorio actual
    python validate-setup.py

    # Validar directorio específico
    python validate-setup.py --target /path/to/proyecto

    # Modo verbose
    python validate-setup.py --verbose

Autor: Victor Valotto
Versión: 1.0.0
"""

import sys
import json
import os
import argparse
from pathlib import Path
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass, field


# =============================================================================
# CONFIGURACIÓN DE COLORES PARA TERMINAL
# =============================================================================

class Colors:
    """Códigos ANSI para colores en terminal"""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    CYAN = '\033[0;36m'
    BOLD = '\033[1m'
    NC = '\033[0m'  # No Color

    @staticmethod
    def disable():
        """Deshabilitar colores"""
        Colors.RED = ''
        Colors.GREEN = ''
        Colors.YELLOW = ''
        Colors.BLUE = ''
        Colors.CYAN = ''
        Colors.BOLD = ''
        Colors.NC = ''


# =============================================================================
# DATACLASSES PARA RESULTADOS DE VALIDACIÓN
# =============================================================================

@dataclass
class ValidationResult:
    """Resultado de una validación individual"""
    name: str
    passed: bool
    message: str = ""
    is_warning: bool = False


@dataclass
class ValidationReport:
    """Reporte completo de validación"""
    target_dir: Path
    results: List[ValidationResult] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        """Retorna True si todas las validaciones críticas pasaron"""
        return all(r.passed or r.is_warning for r in self.results)

    @property
    def error_count(self) -> int:
        """Número de errores críticos"""
        return sum(1 for r in self.results if not r.passed and not r.is_warning)

    @property
    def warning_count(self) -> int:
        """Número de warnings"""
        return sum(1 for r in self.results if r.is_warning and not r.passed)


# =============================================================================
# CLASE PRINCIPAL DEL VALIDADOR
# =============================================================================

class SetupValidator:
    """
    Validador de instalación del Claude Dev Kit.

    Verifica que todos los componentes requeridos estén presentes y funcionales.
    """

    def __init__(self, target_dir: Path, verbose: bool = False):
        """
        Inicializar validador.

        Args:
            target_dir: Directorio del proyecto a validar
            verbose: Si True, mostrar información detallada
        """
        self.target_dir = target_dir
        self.verbose = verbose
        self.claude_dir = target_dir / '.claude'
        self.report = ValidationReport(target_dir=target_dir)

    def log_verbose(self, message: str):
        """Imprimir mensaje solo en modo verbose"""
        if self.verbose:
            print(f"  {Colors.CYAN}→{Colors.NC} {message}")

    def validate_directories(self) -> ValidationResult:
        """
        Verificar que directorios requeridos existen.

        Returns:
            ValidationResult con resultado de la validación
        """
        self.log_verbose("Verificando estructura de directorios...")

        required_dirs = [
            '.claude',
            '.claude/skills',
            '.claude/skills/implement-us',
            '.claude/templates',
            '.claude/templates/bdd',
            '.claude/templates/planning',
            '.claude/templates/testing',
            '.claude/templates/reporting',
            '.claude/tracking'
        ]

        missing_dirs = []
        for dir_path in required_dirs:
            full_path = self.target_dir / dir_path
            if not full_path.exists():
                missing_dirs.append(dir_path)
                self.log_verbose(f"  ❌ Falta: {dir_path}")
            else:
                self.log_verbose(f"  ✓ {dir_path}")

        if missing_dirs:
            return ValidationResult(
                name="Estructura de Directorios",
                passed=False,
                message=f"Faltan {len(missing_dirs)} directorios: {', '.join(missing_dirs[:3])}"
            )

        return ValidationResult(
            name="Estructura de Directorios",
            passed=True,
            message=f"{len(required_dirs)} directorios verificados"
        )

    def validate_files(self) -> ValidationResult:
        """
        Verificar que archivos críticos existen.

        Returns:
            ValidationResult con resultado de la validación
        """
        self.log_verbose("Verificando archivos críticos...")

        required_files = [
            '.claude/config.json',
            '.claude/skills/implement-us/SKILL.md',
            '.claude/tracking/time_tracker.py',
            '.claude/tracking/commands.py',
            '.claude/tracking/__init__.py'
        ]

        missing_files = []
        for file_path in required_files:
            full_path = self.target_dir / file_path
            if not full_path.exists():
                missing_files.append(file_path)
                self.log_verbose(f"  ❌ Falta: {file_path}")
            elif not full_path.is_file():
                missing_files.append(f"{file_path} (no es archivo)")
                self.log_verbose(f"  ❌ No es archivo: {file_path}")
            else:
                self.log_verbose(f"  ✓ {file_path}")

        if missing_files:
            return ValidationResult(
                name="Archivos Críticos",
                passed=False,
                message=f"Faltan {len(missing_files)} archivos: {', '.join(missing_files[:2])}"
            )

        return ValidationResult(
            name="Archivos Críticos",
            passed=True,
            message=f"{len(required_files)} archivos verificados"
        )

    def validate_config_json(self) -> ValidationResult:
        """
        Validar que config.json es válido y tiene campos requeridos.

        Returns:
            ValidationResult con resultado de la validación
        """
        self.log_verbose("Verificando config.json...")

        config_file = self.claude_dir / 'config.json'

        if not config_file.exists():
            return ValidationResult(
                name="Configuración JSON",
                passed=False,
                message="config.json no existe"
            )

        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)

            self.log_verbose(f"  ✓ JSON válido")

            # Verificar campos requeridos
            required_keys = ['profile', 'version']
            missing_keys = [key for key in required_keys if key not in config]

            if missing_keys:
                return ValidationResult(
                    name="Configuración JSON",
                    passed=False,
                    message=f"Faltan keys requeridos: {', '.join(missing_keys)}"
                )

            self.log_verbose(f"  ✓ Perfil: {config['profile']}")
            self.log_verbose(f"  ✓ Versión: {config['version']}")

            return ValidationResult(
                name="Configuración JSON",
                passed=True,
                message=f"Perfil: {config['profile']}"
            )

        except json.JSONDecodeError as e:
            return ValidationResult(
                name="Configuración JSON",
                passed=False,
                message=f"JSON inválido: {e}"
            )
        except Exception as e:
            return ValidationResult(
                name="Configuración JSON",
                passed=False,
                message=f"Error: {e}"
            )

    def validate_python_imports(self) -> ValidationResult:
        """
        Validar que módulos Python pueden importarse.

        Returns:
            ValidationResult con resultado de la validación
        """
        self.log_verbose("Verificando imports Python...")

        # Agregar .claude al path para imports
        claude_dir_str = str(self.claude_dir.absolute())
        if claude_dir_str not in sys.path:
            sys.path.insert(0, claude_dir_str)

        try:
            # Intentar importar tracking module
            import tracking
            self.log_verbose(f"  ✓ import tracking")

            import tracking.time_tracker
            self.log_verbose(f"  ✓ import tracking.time_tracker")

            import tracking.commands
            self.log_verbose(f"  ✓ import tracking.commands")

            # Verificar que clases principales existen
            from tracking.time_tracker import TimeTracker, Task, Phase
            self.log_verbose(f"  ✓ Clases principales accesibles")

            return ValidationResult(
                name="Imports Python",
                passed=True,
                message="Módulos tracking importan correctamente"
            )

        except ImportError as e:
            return ValidationResult(
                name="Imports Python",
                passed=False,
                message=f"Error de import: {e}"
            )
        except Exception as e:
            return ValidationResult(
                name="Imports Python",
                passed=False,
                message=f"Error: {e}"
            )
        finally:
            # Remover .claude del path
            if claude_dir_str in sys.path:
                sys.path.remove(claude_dir_str)

    def validate_permissions(self) -> ValidationResult:
        """
        Validar permisos de ejecución en hooks (opcional).

        Returns:
            ValidationResult con resultado de la validación
        """
        self.log_verbose("Verificando permisos de hooks...")

        hooks_dir = self.claude_dir / 'hooks'

        if not hooks_dir.exists():
            return ValidationResult(
                name="Permisos de Hooks",
                passed=True,
                is_warning=True,
                message="Hooks no instalados (opcional)"
            )

        hooks = list(hooks_dir.glob('*.sh'))

        if not hooks:
            return ValidationResult(
                name="Permisos de Hooks",
                passed=True,
                is_warning=True,
                message="No se encontraron hooks .sh"
            )

        non_executable = []
        for hook in hooks:
            if not os.access(hook, os.X_OK):
                non_executable.append(hook.name)
                self.log_verbose(f"  ⚠️  No ejecutable: {hook.name}")
            else:
                self.log_verbose(f"  ✓ {hook.name}")

        if non_executable:
            return ValidationResult(
                name="Permisos de Hooks",
                passed=True,
                is_warning=True,
                message=f"{len(non_executable)} hooks sin permisos de ejecución"
            )

        return ValidationResult(
            name="Permisos de Hooks",
            passed=True,
            message=f"{len(hooks)} hooks con permisos correctos"
        )

    def generate_report(self) -> str:
        """
        Generar reporte de validación formateado.

        Returns:
            String con reporte formateado
        """
        lines = []
        separator = "━" * 50

        # Header
        lines.append(f"\n{separator}")
        lines.append(f"{Colors.BOLD}Claude Dev Kit - Validación de Instalación{Colors.NC}")
        lines.append(f"{separator}\n")
        lines.append(f"Target: {Colors.CYAN}{self.target_dir}{Colors.NC}\n")

        # Resultados de validaciones
        for result in self.report.results:
            if result.passed:
                if result.is_warning:
                    icon = f"{Colors.YELLOW}⚠️{Colors.NC} "
                    status = f"{Colors.YELLOW}WARNING{Colors.NC}"
                else:
                    icon = f"{Colors.GREEN}✅{Colors.NC}"
                    status = f"{Colors.GREEN}OK{Colors.NC}"
            else:
                icon = f"{Colors.RED}❌{Colors.NC}"
                status = f"{Colors.RED}FAIL{Colors.NC}"

            # Formatear nombre con padding
            name_padded = result.name.ljust(25, '.')

            lines.append(f"{icon} {name_padded} {status}")

            if result.message and (not result.passed or self.verbose):
                lines.append(f"   {Colors.CYAN}→{Colors.NC} {result.message}")

        # Separador
        lines.append(f"\n{separator}")

        # Resultado final
        if self.report.passed:
            result_icon = f"{Colors.GREEN}✅{Colors.NC}"
            result_text = f"{Colors.GREEN}{Colors.BOLD}INSTALACIÓN VÁLIDA{Colors.NC}"
        else:
            result_icon = f"{Colors.RED}❌{Colors.NC}"
            result_text = f"{Colors.RED}{Colors.BOLD}INSTALACIÓN INCOMPLETA{Colors.NC}"

        lines.append(f"Resultado: {result_icon} {result_text}")

        # Estadísticas
        if self.report.error_count > 0 or self.report.warning_count > 0:
            stats = []
            if self.report.error_count > 0:
                stats.append(f"{Colors.RED}{self.report.error_count} errores{Colors.NC}")
            if self.report.warning_count > 0:
                stats.append(f"{Colors.YELLOW}{self.report.warning_count} warnings{Colors.NC}")
            lines.append(f"   {' | '.join(stats)}")

        lines.append(f"{separator}\n")

        return '\n'.join(lines)

    def run(self) -> int:
        """
        Ejecutar todas las validaciones.

        Returns:
            Exit code (0 = éxito, 1 = error)
        """
        # Verificar que .claude/ existe
        if not self.claude_dir.exists():
            print(f"{Colors.RED}Error: Directorio .claude/ no encontrado en {self.target_dir}{Colors.NC}")
            print(f"Este proyecto no parece tener Claude Dev Kit instalado.")
            return 1

        # Ejecutar validaciones
        self.report.results.append(self.validate_directories())
        self.report.results.append(self.validate_files())
        self.report.results.append(self.validate_config_json())
        self.report.results.append(self.validate_python_imports())
        self.report.results.append(self.validate_permissions())

        # Generar y mostrar reporte
        report_text = self.generate_report()
        print(report_text)

        # Retornar exit code
        return 0 if self.report.passed else 1


# =============================================================================
# FUNCIÓN PRINCIPAL
# =============================================================================

def main():
    """Punto de entrada principal del validador"""

    parser = argparse.ArgumentParser(
        description='Claude Dev Kit - Validador de Instalación',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  # Validar directorio actual
  python validate-setup.py

  # Validar directorio específico
  python validate-setup.py --target /path/to/proyecto

  # Modo verbose con detalles
  python validate-setup.py --verbose

  # Sin colores (para CI/CD)
  python validate-setup.py --no-color

Exit codes:
  0 - Instalación válida
  1 - Instalación incompleta o errores
        """
    )

    parser.add_argument(
        '--target',
        type=Path,
        default=Path.cwd(),
        help='Directorio del proyecto a validar (default: directorio actual)'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Mostrar información detallada de validación'
    )

    parser.add_argument(
        '--no-color',
        action='store_true',
        help='Deshabilitar colores en output'
    )

    args = parser.parse_args()

    # Deshabilitar colores si se solicita
    if args.no_color:
        Colors.disable()

    try:
        # Crear y ejecutar validador
        validator = SetupValidator(
            target_dir=args.target,
            verbose=args.verbose
        )

        exit_code = validator.run()
        sys.exit(exit_code)

    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Validación cancelada por el usuario{Colors.NC}")
        sys.exit(130)
    except Exception as e:
        print(f"{Colors.RED}Error fatal: {e}{Colors.NC}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
