"""
Tests del módulo install/installer.py

Cubre: ClaudeDevKitInstaller
  - load_config
  - validate_profile
  - check_target_dir
  - copy_framework_files
  - generate_config_json
  - generate_claude_md
  - run_validation
  - install (integración dry-run)
"""
import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Hacer importable install/
sys.path.insert(0, str(Path(__file__).parent.parent / "install"))
from installer import ClaudeDevKitInstaller  # noqa: E402

REPO_ROOT = Path(__file__).parent.parent
INSTALL_DIR = REPO_ROOT / "install"
CONFIG_PATH = INSTALL_DIR / "config.json"


# =============================================================================
# Tests: load_config
# =============================================================================

class TestLoadConfig:

    def test_load_config_valid(self, installer):
        """Config real carga correctamente con las claves esperadas."""
        assert "profiles" in installer.config
        assert "installation" in installer.config
        assert "messages" in installer.config

    def test_load_config_missing_file(self, kit_root, tmp_path):
        """Lanza FileNotFoundError si config.json no existe."""
        missing = tmp_path / "nonexistent.json"
        with pytest.raises(FileNotFoundError):
            ClaudeDevKitInstaller(missing, kit_root)

    def test_load_config_invalid_json(self, kit_root, tmp_path):
        """Lanza json.JSONDecodeError si el archivo tiene JSON inválido."""
        bad_json = tmp_path / "bad.json"
        bad_json.write_text("{profiles: [invalid json content")
        with pytest.raises(json.JSONDecodeError):
            ClaudeDevKitInstaller(bad_json, kit_root)


# =============================================================================
# Tests: validate_profile
# =============================================================================

class TestValidateProfile:

    def test_validate_profile_known(self, installer):
        """Un perfil conocido retorna True."""
        assert installer.validate_profile("pyqt-mvc") is True

    def test_validate_profile_unknown(self, installer):
        """Un perfil desconocido retorna False."""
        assert installer.validate_profile("nonexistent-profile") is False

    def test_validate_profile_all_seven(self, installer):
        """Los 7 perfiles del config.json retornan True."""
        profiles = [
            "pyqt-mvc", "fastapi-rest", "flask-rest", "flask-webapp", "generic-python",
            "hexagonal-ddd-bc", "clean-architecture-bc",
        ]
        for profile in profiles:
            assert installer.validate_profile(profile) is True, (
                f"Perfil '{profile}' debería ser válido"
            )


# =============================================================================
# Tests: check_target_dir
# =============================================================================

class TestCheckTargetDir:

    def test_target_dir_not_exists(self, installer, tmp_path):
        """Si el directorio no existe, retorna True directamente."""
        target = tmp_path / ".claude"
        assert not target.exists()
        result = installer.check_target_dir(target, force=False)
        assert result is True

    def test_target_dir_exists_with_force(self, installer, tmp_path):
        """Si existe y force=True, retorna True sin preguntar."""
        target = tmp_path / ".claude"
        target.mkdir()
        result = installer.check_target_dir(target, force=True)
        assert result is True

    def test_target_dir_exists_user_confirms(self, installer, tmp_path):
        """Si existe, force=False y usuario confirma, retorna True."""
        target = tmp_path / ".claude"
        target.mkdir()
        with patch("builtins.input", return_value="s"):
            result = installer.check_target_dir(target, force=False)
        assert result is True

    def test_target_dir_exists_user_denies(self, installer, tmp_path):
        """Si existe, force=False y usuario niega, retorna False."""
        target = tmp_path / ".claude"
        target.mkdir()
        with patch("builtins.input", return_value="n"):
            result = installer.check_target_dir(target, force=False)
        assert result is False

    def test_target_dir_exists_eof_returns_false(self, installer, tmp_path):
        """Si stdin no es TTY (EOFError), retorna False sin crashear."""
        target = tmp_path / ".claude"
        target.mkdir()
        with patch("builtins.input", side_effect=EOFError):
            result = installer.check_target_dir(target, force=False)
        assert result is False


# =============================================================================
# Tests: copy_framework_files
# =============================================================================

class TestCopyFrameworkFiles:

    def test_copy_dry_run_no_files_created(self, installer, tmp_path):
        """dry_run=True no crea ningún archivo."""
        target = tmp_path / ".claude"
        installer.copy_framework_files(target, dry_run=True)
        assert not target.exists()

    def test_copy_creates_skills_dir(self, installer, tmp_path, monkeypatch):
        """Copia el directorio skills/ al destino (con mock de shutil para rapidez)."""
        # Crear un mini skills/ en tmp_path para que la fuente exista
        fake_source = tmp_path / "kit"
        (fake_source / "skills").mkdir(parents=True)
        monkeypatch.setattr(installer, "kit_root", fake_source)
        fake_rules = [{"source": "skills", "target": "{target_dir}/skills", "description": "Skills"}]
        monkeypatch.setitem(installer.config["installation"], "copy_rules", fake_rules)
        target = tmp_path / ".claude"
        installer.copy_framework_files(target, dry_run=False)
        assert (target / "skills").exists()

    def test_copy_creates_tracking_dir(self, installer, tmp_path, monkeypatch):
        """Copia el directorio tracking/ al destino."""
        fake_source = tmp_path / "kit"
        (fake_source / "tracking").mkdir(parents=True)
        monkeypatch.setattr(installer, "kit_root", fake_source)
        fake_rules = [{"source": "tracking", "target": "{target_dir}/tracking", "description": "Tracking"}]
        monkeypatch.setitem(installer.config["installation"], "copy_rules", fake_rules)
        target = tmp_path / ".claude"
        installer.copy_framework_files(target, dry_run=False)
        assert (target / "tracking").exists()

    def test_copy_missing_source_no_error(self, installer, tmp_path, monkeypatch):
        """Si una fuente no existe, continúa sin lanzar excepción."""
        fake_rules = [{"source": "nonexistent_dir", "target": "{target_dir}/x", "description": "test"}]
        monkeypatch.setitem(installer.config["installation"], "copy_rules", fake_rules)
        target = tmp_path / ".claude"
        installer.copy_framework_files(target, dry_run=False)  # No debe lanzar


# =============================================================================
# Tests: generate_config_json
# =============================================================================

class TestGenerateConfigJson:

    def test_creates_config_file(self, installer, tmp_path):
        """Genera config.json en el directorio destino."""
        target = tmp_path / ".claude"
        target.mkdir()
        installer.generate_config_json(target, "generic-python")
        assert (target / "config.json").exists()

    def test_dry_run_no_file_created(self, installer, tmp_path):
        """dry_run=True no crea config.json."""
        target = tmp_path / ".claude"
        target.mkdir()
        installer.generate_config_json(target, "generic-python", dry_run=True)
        assert not (target / "config.json").exists()

    def test_generates_valid_json(self, installer, tmp_path):
        """El archivo generado es JSON válido."""
        target = tmp_path / ".claude"
        target.mkdir()
        installer.generate_config_json(target, "fastapi-rest")
        content = (target / "config.json").read_text()
        data = json.loads(content)  # No debe lanzar
        assert isinstance(data, dict)

    @pytest.mark.parametrize("profile", ["hexagonal-ddd-bc", "clean-architecture-bc"])
    def test_generates_valid_json_bc_first_profiles(self, installer, tmp_path, profile):
        """Los perfiles BC-first generan config.json válido con la clave profile correcta."""
        target = tmp_path / ".claude"
        target.mkdir()
        installer.generate_config_json(target, profile)
        data = json.loads((target / "config.json").read_text())
        assert data["profile"] == profile


# =============================================================================
# Tests: generate_claude_md
# =============================================================================

class TestGenerateClaudeMd:

    def test_creates_when_missing(self, installer, tmp_path):
        """Genera CLAUDE.md si no existe."""
        installer.generate_claude_md(tmp_path, "pyqt-mvc")
        assert (tmp_path / "CLAUDE.md").exists()

    def test_skips_existing_file(self, installer, tmp_path):
        """No sobreescribe un CLAUDE.md existente."""
        existing = tmp_path / "CLAUDE.md"
        original = "# Mi proyecto original"
        existing.write_text(original)
        installer.generate_claude_md(tmp_path, "pyqt-mvc")
        assert existing.read_text() == original

    def test_dry_run_no_file_created(self, installer, tmp_path):
        """dry_run=True no crea CLAUDE.md."""
        installer.generate_claude_md(tmp_path, "pyqt-mvc", dry_run=True)
        assert not (tmp_path / "CLAUDE.md").exists()

    @pytest.mark.parametrize("profile", ["hexagonal-ddd-bc", "clean-architecture-bc"])
    def test_creates_for_bc_first_profiles(self, installer, tmp_path, profile):
        """Genera CLAUDE.md para los perfiles BC-first sin lanzar excepciones."""
        installer.generate_claude_md(tmp_path, profile)
        content = (tmp_path / "CLAUDE.md").read_text()
        assert "Port" in content  # component_type compartido por ambos perfiles


# =============================================================================
# Tests: run_validation
# =============================================================================

class TestRunValidation:

    def test_dry_run_returns_true(self, installer, tmp_path):
        """En dry_run retorna True sin ejecutar nada."""
        result = installer.run_validation(tmp_path, dry_run=True)
        assert result is True

    def test_missing_script_returns_true(self, installer, tmp_path):
        """Si validate-setup.py no existe, retorna True con warning."""
        # tmp_path no contiene scripts/validate-setup.py
        result = installer.run_validation(tmp_path, dry_run=False)
        assert result is True


# =============================================================================
# Tests: install (integración)
# =============================================================================

class TestInstall:

    def test_install_dry_run_returns_true(self, installer, tmp_path):
        """Instalación dry-run con perfil válido retorna True."""
        result = installer.install(
            profile="generic-python",
            project_dir=tmp_path,
            force=True,
            dry_run=True,
            skip_validation=True,
        )
        assert result is True

    def test_install_dry_run_no_files_created(self, installer, tmp_path):
        """Instalación dry-run no crea ningún archivo en el destino."""
        installer.install(
            profile="generic-python",
            project_dir=tmp_path,
            force=True,
            dry_run=True,
            skip_validation=True,
        )
        claude_dir = tmp_path / ".claude"
        assert not claude_dir.exists()

    def test_install_invalid_profile_returns_false(self, installer, tmp_path):
        """Perfil inválido hace que install() retorne False."""
        result = installer.install(
            profile="invalid-profile",
            project_dir=tmp_path,
            force=True,
            dry_run=True,
            skip_validation=True,
        )
        assert result is False

    def test_install_cancelled_by_user_returns_false(self, installer, tmp_path):
        """check_target_dir devuelve False → install cancela y retorna False."""
        target = tmp_path / ".claude"
        target.mkdir()
        with patch("builtins.input", return_value="n"):
            result = installer.install(
                profile="generic-python",
                project_dir=tmp_path,
                force=False,
                dry_run=False,
                skip_validation=True,
            )
        assert result is False

    def test_install_real_creates_target_dir(self, installer, tmp_path):
        """Instalación real (no dry-run) crea el directorio .claude/."""
        with patch.object(installer, "copy_framework_files"):
            result = installer.install(
                profile="generic-python",
                project_dir=tmp_path,
                force=True,
                dry_run=False,
                skip_validation=True,
            )
        assert result is True
        assert (tmp_path / ".claude").exists()

    def test_install_real_runs_validation(self, installer, tmp_path):
        """Instalación real con skip_validation=False ejecuta run_validation."""
        with patch.object(installer, "copy_framework_files"), \
             patch.object(installer, "run_validation", return_value=True) as mock_val:
            installer.install(
                profile="generic-python",
                project_dir=tmp_path,
                force=True,
                dry_run=False,
                skip_validation=False,
            )
        mock_val.assert_called_once()

    def test_install_exception_returns_false(self, installer, tmp_path):
        """Si copy_framework_files lanza excepción, install retorna False."""
        with patch.object(installer, "copy_framework_files", side_effect=RuntimeError("boom")):
            result = installer.install(
                profile="generic-python",
                project_dir=tmp_path,
                force=True,
                dry_run=False,
                skip_validation=True,
            )
        assert result is False

    def test_install_validation_fails_returns_false(self, installer, tmp_path):
        """Si run_validation retorna False, install retorna False."""
        with patch.object(installer, "copy_framework_files"), \
             patch.object(installer, "run_validation", return_value=False):
            result = installer.install(
                profile="generic-python",
                project_dir=tmp_path,
                force=True,
                dry_run=False,
                skip_validation=False,
            )
        assert result is False


# =============================================================================
# Tests: Colors
# =============================================================================

class TestColors:

    def test_colors_disable_clears_codes(self):
        """Colors.disable() vacía todos los códigos ANSI."""
        from installer import Colors
        Colors.disable()
        assert Colors.RED == ""
        assert Colors.GREEN == ""
        assert Colors.BOLD == ""
        assert Colors.NC == ""


# =============================================================================
# Tests: select_profile_interactive
# =============================================================================

class TestSelectProfileInteractive:

    def test_select_valid_profile(self, installer):
        """Selección válida retorna el nombre del perfil."""
        with patch("builtins.input", return_value="1"), \
             patch("builtins.print"):
            result = installer.select_profile_interactive()
        assert result in installer.config["profiles"]

    def test_select_invalid_then_valid(self, installer):
        """Entrada inválida se ignora y el loop continúa hasta opción válida."""
        responses = iter(["abc", "99", "2"])
        with patch("builtins.input", side_effect=responses), \
             patch("builtins.print"):
            result = installer.select_profile_interactive()
        assert result in installer.config["profiles"]

    def test_select_keyboard_interrupt_exits(self, installer):
        """KeyboardInterrupt durante la selección llama sys.exit(0)."""
        with patch("builtins.input", side_effect=KeyboardInterrupt), \
             patch("builtins.print"), \
             pytest.raises(SystemExit) as exc_info:
            installer.select_profile_interactive()
        assert exc_info.value.code == 0

    def test_select_eof_exits_with_error(self, installer):
        """EOFError (stdin no-TTY) llama sys.exit(1) con mensaje claro."""
        with patch("builtins.input", side_effect=EOFError), \
             patch("builtins.print"), \
             pytest.raises(SystemExit) as exc_info:
            installer.select_profile_interactive()
        assert exc_info.value.code == 1


# =============================================================================
# Tests: copy_framework_files — ramas adicionales
# =============================================================================

class TestCopyFrameworkFilesExtra:

    def test_copy_overwrites_existing_target(self, installer, tmp_path, monkeypatch):
        """Si el target ya existe, lo elimina y vuelve a copiar."""
        # Mini kit con un directorio skills/
        fake_kit = tmp_path / "kit"
        (fake_kit / "skills").mkdir(parents=True)
        monkeypatch.setattr(installer, "kit_root", fake_kit)
        fake_rules = [{"source": "skills", "target": "{target_dir}/skills", "description": "Skills"}]
        monkeypatch.setitem(installer.config["installation"], "copy_rules", fake_rules)
        target = tmp_path / ".claude"
        # Pre-crear destino con archivo basura
        skills_target = target / "skills"
        skills_target.mkdir(parents=True)
        (skills_target / "stale.txt").write_text("viejo")
        installer.copy_framework_files(target, dry_run=False)
        # El directorio se reemplazó: stale.txt ya no existe
        assert not (skills_target / "stale.txt").exists()

    def test_copy_file_rule(self, installer, tmp_path, monkeypatch):
        """Copia de una regla con fuente tipo archivo (no directorio)."""
        # Crear un archivo fuente real en tmp_path
        source_file = tmp_path / "source_file.txt"
        source_file.write_text("contenido")
        fake_rules = [{
            "source": str(source_file.relative_to(installer.kit_root))
            if source_file.is_relative_to(installer.kit_root)
            else "../" + source_file.name,
            "target": "{target_dir}/copied_file.txt",
            "description": "archivo de prueba",
        }]
        monkeypatch.setitem(installer.config["installation"], "copy_rules", fake_rules)
        # Monkeypatch kit_root para que apunte a tmp_path
        monkeypatch.setattr(installer, "kit_root", tmp_path)
        # Re-parchear la regla con fuente relativa al nuevo kit_root
        fake_rules[0]["source"] = "source_file.txt"
        target_dir = tmp_path / "out"
        installer.copy_framework_files(target_dir, dry_run=False)
        assert (target_dir / "copied_file.txt").exists()


# =============================================================================
# Tests: run_validation con script presente
# =============================================================================

class TestRunValidationWithScript:

    def test_validation_with_existing_script(self, installer, tmp_path):
        """Si validate-setup.py existe, ejecuta el bloque de validación."""
        # Crear scripts/validate-setup.py dentro de tmp_path
        scripts_dir = tmp_path / "scripts"
        scripts_dir.mkdir()
        (scripts_dir / "validate-setup.py").write_text("# validator")
        # kit_root.parent == tmp_path para que encuentre scripts/
        with patch.object(installer, "kit_root", tmp_path / "kit"):
            # Hacer que kit_root.parent sea tmp_path
            import types
            fake_kit_root = types.SimpleNamespace(
                parent=tmp_path
            )
            with patch.object(installer, "kit_root", fake_kit_root):
                result = installer.run_validation(tmp_path, dry_run=False)
        assert result is True
