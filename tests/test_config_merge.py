"""
Tests de fusión de configuración (merge_configs, generate_config_json, generate_claude_md)

Verifica que cada perfil genera la configuración correcta al instalar.
Perfiles: pyqt-mvc, fastapi-rest, flask-rest, flask-webapp, generic-python
"""
import json
import pytest
from datetime import datetime
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'install'))
from installer import ClaudeDevKitInstaller  # noqa: E402


# ─────────────────────────────────────────────────────────────────────────────
# Tests: merge_configs — Campos comunes (aplican a todos los perfiles)
# ─────────────────────────────────────────────────────────────────────────────

class TestMergeConfigsCommon:
    REQUIRED_KEYS = {
        "version", "profile", "profile_name", "installed_at",
        "architecture_pattern", "test_framework", "component_types",
        "patterns", "variables"
    }

    def test_merge_has_required_keys(self, installer):
        result = installer.merge_configs("pyqt-mvc")
        assert self.REQUIRED_KEYS.issubset(result.keys())

    def test_merge_profile_name_matches(self, installer):
        result = installer.merge_configs("pyqt-mvc")
        assert result["profile"] == "pyqt-mvc"

    def test_merge_installed_at_is_iso(self, installer):
        result = installer.merge_configs("fastapi-rest")
        # Debe ser parseable como ISO 8601
        installed_at = result["installed_at"]
        parsed = datetime.fromisoformat(installed_at.replace("Z", "+00:00"))
        assert isinstance(parsed, datetime)

    def test_merge_all_profiles_have_required_keys(self, installer):
        profiles = ["pyqt-mvc", "fastapi-rest", "flask-rest", "flask-webapp", "generic-python"]
        for profile in profiles:
            result = installer.merge_configs(profile)
            missing = self.REQUIRED_KEYS - result.keys()
            assert not missing, f"Perfil '{profile}' faltan claves: {missing}"


# ─────────────────────────────────────────────────────────────────────────────
# Tests: merge_configs — Perfil pyqt-mvc
# ─────────────────────────────────────────────────────────────────────────────

class TestMergeConfigsPyQt:
    def test_merge_pyqt_architecture(self, installer):
        result = installer.merge_configs("pyqt-mvc")
        assert result["architecture_pattern"] == "mvc"

    def test_merge_pyqt_test_framework(self, installer):
        result = installer.merge_configs("pyqt-mvc")
        assert result["test_framework"] == "pytest-qt"

    def test_merge_pyqt_component_types(self, installer):
        result = installer.merge_configs("pyqt-mvc")
        types = result["component_types"]
        assert "Panel" in types
        assert "Model" in types
        assert "Controller" in types

    def test_merge_pyqt_variables(self, installer):
        result = installer.merge_configs("pyqt-mvc")
        assert result["variables"]["base_class"] == "ModeloBase"


# ─────────────────────────────────────────────────────────────────────────────
# Tests: merge_configs — Perfil fastapi-rest
# ─────────────────────────────────────────────────────────────────────────────

class TestMergeConfigsFastAPI:
    def test_merge_fastapi_architecture(self, installer):
        result = installer.merge_configs("fastapi-rest")
        assert result["architecture_pattern"] == "layered"

    def test_merge_fastapi_test_framework(self, installer):
        result = installer.merge_configs("fastapi-rest")
        assert result["test_framework"] == "pytest"

    def test_merge_fastapi_component_types(self, installer):
        result = installer.merge_configs("fastapi-rest")
        types = result["component_types"]
        assert "Router" in types
        assert "Service" in types
        assert "Repository" in types

    def test_merge_fastapi_variables(self, installer):
        result = installer.merge_configs("fastapi-rest")
        assert result["variables"]["base_class"] == "BaseModel"


# ─────────────────────────────────────────────────────────────────────────────
# Tests: merge_configs — Perfil flask-rest
# ─────────────────────────────────────────────────────────────────────────────

class TestMergeConfigsFlaskRest:
    def test_merge_flask_rest_architecture(self, installer):
        result = installer.merge_configs("flask-rest")
        assert result["architecture_pattern"] == "layered"

    def test_merge_flask_rest_test_framework(self, installer):
        result = installer.merge_configs("flask-rest")
        assert result["test_framework"] == "pytest"

    def test_merge_flask_rest_component_types(self, installer):
        result = installer.merge_configs("flask-rest")
        types = result["component_types"]
        assert "Blueprint" in types
        assert "Service" in types
        assert "Repository" in types

    def test_merge_flask_rest_variables(self, installer):
        result = installer.merge_configs("flask-rest")
        assert "base_class" in result["variables"]


# ─────────────────────────────────────────────────────────────────────────────
# Tests: merge_configs — Perfil flask-webapp
# ─────────────────────────────────────────────────────────────────────────────

class TestMergeConfigsFlaskWebapp:
    def test_merge_flask_webapp_architecture(self, installer):
        result = installer.merge_configs("flask-webapp")
        assert result["architecture_pattern"] == "bff"

    def test_merge_flask_webapp_test_framework(self, installer):
        result = installer.merge_configs("flask-webapp")
        assert result["test_framework"] == "pytest"

    def test_merge_flask_webapp_component_types(self, installer):
        result = installer.merge_configs("flask-webapp")
        types = result["component_types"]
        assert "Blueprint" in types
        assert "Template" in types


# ─────────────────────────────────────────────────────────────────────────────
# Tests: merge_configs — Perfil generic-python
# ─────────────────────────────────────────────────────────────────────────────

class TestMergeConfigsGeneric:
    def test_merge_generic_architecture(self, installer):
        result = installer.merge_configs("generic-python")
        assert result["architecture_pattern"] == "modular"

    def test_merge_generic_test_framework(self, installer):
        result = installer.merge_configs("generic-python")
        assert result["test_framework"] == "pytest"

    def test_merge_generic_component_types(self, installer):
        result = installer.merge_configs("generic-python")
        types = result["component_types"]
        assert "Module" in types
        assert "Class" in types
        assert "Function" in types


# ─────────────────────────────────────────────────────────────────────────────
# Tests: generate_config_json — Contenido del JSON generado
# ─────────────────────────────────────────────────────────────────────────────

class TestGenerateConfigJson:
    def test_config_json_is_valid_json(self, installer, tmp_path):
        target_dir = tmp_path / ".claude"
        target_dir.mkdir()
        installer.generate_config_json(target_dir, "pyqt-mvc")
        config_file = target_dir / "config.json"
        with open(config_file, encoding="utf-8") as f:
            data = json.load(f)
        assert isinstance(data, dict)

    def test_config_json_has_profile_key(self, installer, tmp_path):
        target_dir = tmp_path / ".claude"
        target_dir.mkdir()
        installer.generate_config_json(target_dir, "fastapi-rest")
        config_file = target_dir / "config.json"
        with open(config_file, encoding="utf-8") as f:
            data = json.load(f)
        assert data["profile"] == "fastapi-rest"

    def test_config_json_has_version(self, installer, tmp_path):
        target_dir = tmp_path / ".claude"
        target_dir.mkdir()
        installer.generate_config_json(target_dir, "generic-python")
        config_file = target_dir / "config.json"
        with open(config_file, encoding="utf-8") as f:
            data = json.load(f)
        assert "version" in data
        assert data["version"]  # No vacío


# ─────────────────────────────────────────────────────────────────────────────
# Tests: generate_claude_md — Contenido por perfil
# ─────────────────────────────────────────────────────────────────────────────

class TestGenerateClaudeMd:
    def test_claude_md_contains_profile_name(self, installer, tmp_path):
        installer.generate_claude_md(tmp_path, "pyqt-mvc", dry_run=False)
        content = (tmp_path / "CLAUDE.md").read_text(encoding="utf-8")
        assert "PyQt + MVC" in content

    def test_claude_md_contains_architecture(self, installer, tmp_path):
        installer.generate_claude_md(tmp_path, "fastapi-rest", dry_run=False)
        content = (tmp_path / "CLAUDE.md").read_text(encoding="utf-8")
        assert "layered" in content

    def test_claude_md_contains_test_framework(self, installer, tmp_path):
        installer.generate_claude_md(tmp_path, "pyqt-mvc", dry_run=False)
        content = (tmp_path / "CLAUDE.md").read_text(encoding="utf-8")
        assert "pytest-qt" in content

    def test_claude_md_contains_skill_section(self, installer, tmp_path):
        installer.generate_claude_md(tmp_path, "generic-python", dry_run=False)
        content = (tmp_path / "CLAUDE.md").read_text(encoding="utf-8")
        assert "/implement-us" in content

    def test_claude_md_does_not_overwrite(self, installer, tmp_path):
        claude_md = tmp_path / "CLAUDE.md"
        original_content = "# Mi CLAUDE.md original - no tocar"
        claude_md.write_text(original_content, encoding="utf-8")
        installer.generate_claude_md(tmp_path, "pyqt-mvc", dry_run=False)
        assert claude_md.read_text(encoding="utf-8") == original_content

    def test_claude_md_flask_webapp_profile_name(self, installer, tmp_path):
        installer.generate_claude_md(tmp_path, "flask-webapp", dry_run=False)
        content = (tmp_path / "CLAUDE.md").read_text(encoding="utf-8")
        assert "Flask WebApp" in content
