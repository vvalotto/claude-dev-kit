"""Step definitions para el feature Reserva de un recurso (US-070)."""

import os
from datetime import date, timedelta

import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from fastapi.testclient import TestClient

from main import app
from reservas.api.router import get_repository
from reservas.infrastructure.repositories.reserva_repository_memoria import (
    ReservaRepositoryMemoria,
)

FEATURE_FILE = os.path.join(os.path.dirname(__file__), "..", "reservas.feature")
scenarios(FEATURE_FILE)

_FECHAS_RELATIVAS = {
    "hoy": lambda: date.today(),
    "manana": lambda: date.today() + timedelta(days=1),
    "ayer": lambda: date.today() - timedelta(days=1),
}


def _resolver_fecha(valor: str) -> str:
    """Traduce alias relativos ('manana', 'ayer') a fechas ISO concretas."""
    resolver = _FECHAS_RELATIVAS.get(valor)
    return str(resolver()) if resolver else valor


@pytest.fixture
def context():
    """Estado compartido entre steps: última respuesta HTTP."""
    return {"response": None}


@pytest.fixture
def client():
    """Cliente de test con repositorio en memoria aislado por escenario."""
    repository = ReservaRepositoryMemoria()
    app.dependency_overrides[get_repository] = lambda: repository
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@given("que la API está disponible")
def api_disponible(client):
    """Verifica que la API responde antes de ejecutar el escenario."""
    respuesta = client.get("/")
    assert respuesta.status_code == 200


@given(
    parsers.parse(
        'que existe una reserva para "{recurso_id}" en "{fecha}" '
        'de "{hora_inicio}" a "{hora_fin}"'
    )
)
def existe_reserva(client, recurso_id, fecha, hora_inicio, hora_fin):
    """Crea una reserva previa para usarse como precondición del escenario."""
    respuesta = client.post(
        "/reservas/",
        json={
            "recurso_id": recurso_id,
            "fecha": _resolver_fecha(fecha),
            "hora_inicio": hora_inicio,
            "hora_fin": hora_fin,
            "cliente_nombre": "Cliente Previo",
        },
    )
    assert respuesta.status_code == 201


@when(parsers.re(r'se envía una petición POST a "(?P<endpoint>[^"]+)" con:'))
def post_con_body(client, context, endpoint, datatable):
    """Envía un POST con body construido desde la tabla campo/valor."""
    body = {}
    for fila in datatable[1:]:  # saltar encabezado "campo | valor"
        campo, valor = fila[0], fila[1]
        body[campo] = _resolver_fecha(valor) if campo == "fecha" else valor

    context["response"] = client.post(endpoint, json=body)


@when(parsers.re(r'se envía una petición GET a "(?P<endpoint>[^"]+)"$'))
def get_simple(client, context, endpoint):
    """Envía un GET sin body."""
    context["response"] = client.get(endpoint)


@then(parsers.parse("la respuesta tiene código de estado {status:d}"))
def verificar_status(context, status):
    """Verifica el código de estado HTTP de la última respuesta."""
    assert context["response"].status_code == status


@then(parsers.parse('la reserva creada puede consultarse y está "{estado}"'))
def verificar_reserva_creada(client, context, estado):
    """Verifica que la reserva recién creada existe con el estado esperado."""
    reserva_id = context["response"].json()["id"]

    respuesta = client.get(f"/reservas/{reserva_id}")

    assert respuesta.status_code == 200
    assert respuesta.json()["estado"] == estado
