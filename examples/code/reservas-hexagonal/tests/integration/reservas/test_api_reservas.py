"""Tests de integración end-to-end de la API de Reservas (router + handlers + repo)."""

from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient

from main import app
from reservas.api.router import get_repository
from reservas.infrastructure.repositories.reserva_repository_memoria import (
    ReservaRepositoryMemoria,
)


@pytest.fixture
def client():
    """Cliente de test con un repositorio en memoria aislado por test."""
    repository = ReservaRepositoryMemoria()
    app.dependency_overrides[get_repository] = lambda: repository
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def _payload(**overrides) -> dict:
    defaults = {
        "recurso_id": "mesa-1",
        "fecha": str(date.today() + timedelta(days=1)),
        "hora_inicio": "10:00:00",
        "hora_fin": "11:00:00",
        "cliente_nombre": "Ana",
    }
    defaults.update(overrides)
    return defaults


class TestFlujoCompleto:
    """Valida el flujo HTTP completo: crear y luego consultar una reserva."""

    def test_crear_y_obtener_reserva(self, client):
        """Verifica que una reserva creada por POST se puede leer con GET."""
        respuesta_creacion = client.post("/reservas/", json=_payload())
        assert respuesta_creacion.status_code == 201
        reserva_id = respuesta_creacion.json()["id"]

        respuesta_lectura = client.get(f"/reservas/{reserva_id}")

        assert respuesta_lectura.status_code == 200
        data = respuesta_lectura.json()
        assert data["cliente_nombre"] == "Ana"
        assert data["estado"] == "CONFIRMADA"

    def test_crear_reserva_solapada_devuelve_409(self, client):
        """Verifica que una segunda reserva solapada responde 409."""
        client.post("/reservas/", json=_payload())

        respuesta = client.post("/reservas/", json=_payload(cliente_nombre="Otro"))

        assert respuesta.status_code == 409

    def test_obtener_reserva_inexistente_devuelve_404(self, client):
        """Verifica que consultar una reserva inexistente responde 404."""
        respuesta = client.get("/reservas/no-existe")

        assert respuesta.status_code == 404

    def test_crear_reserva_con_fecha_pasada_devuelve_422(self, client):
        """Verifica que una fecha inválida responde 422 (violación de invariante)."""
        respuesta = client.post(
            "/reservas/",
            json=_payload(fecha=str(date.today() - timedelta(days=1))),
        )

        assert respuesta.status_code == 422
