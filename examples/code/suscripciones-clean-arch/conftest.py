"""Fixtures compartidas por tests de integración y BDD (nivel HTTP)."""

import pytest
from fastapi.testclient import TestClient

import main


@pytest.fixture
def client():
    """TestClient contra la app real, limpiando estado entre tests."""
    main.repositorio.limpiar()
    main.notificador.enviadas.clear()
    return TestClient(main.app)
