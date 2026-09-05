# Template: Step Definitions BDD — específico para perfil fastapi-rest
# Referencia estructural para implementar los steps de un .feature de API REST
# en la Fase 6. No es código ejecutable — adaptar a los endpoints reales.
#
# Variables disponibles:
# - {FEATURE_FILE_PATH}: Ruta relativa al archivo .feature correspondiente
# - {SCENARIO_N_NAME}: Nombre del escenario N (debe coincidir literal con el .feature)
# - {APP_IMPORT_PATH}: Módulo donde vive la instancia FastAPI (ej. "main")

"""Step definitions para {FEATURE_TITLE} ({US_ID})."""

import os
import pytest
from pytest_bdd import scenario, given, when, then, parsers
from fastapi.testclient import TestClient
from {APP_IMPORT_PATH} import app


FEATURE_FILE = os.path.join(os.path.dirname(__file__), "{FEATURE_FILE_PATH}")


@scenario(FEATURE_FILE, "{SCENARIO_1_NAME}")
def test_{scenario_1_slug}():
    """Test para el escenario {SCENARIO_1_NAME}."""


@pytest.fixture
def context():
    """Estado compartido entre steps: última respuesta HTTP, ids creados, etc."""
    return {"response": None}


@pytest.fixture
def client():
    """Cliente HTTP de test contra la app FastAPI."""
    with TestClient(app) as test_client:
        yield test_client


@given("que la API está disponible", target_fixture="context")
def api_available(client, context):
    """Verifica que la API responde antes de ejecutar el escenario."""
    response = client.get("/")
    assert response.status_code == 200
    return context


@when(parsers.re(r'se envía una petición (?P<method>GET|POST|PUT|DELETE) a "(?P<endpoint>[^"]+)"$'))
def send_request(client, context, method, endpoint):
    """Envía una petición HTTP sin body."""
    context["response"] = client.request(method, endpoint)


@when(parsers.re(r'se envía una petición (?P<method>POST|PUT) a "(?P<endpoint>[^"]+)" con:'))
def send_request_with_body(client, context, method, endpoint, datatable):
    """Envía una petición HTTP con body construido desde la tabla campo/valor."""
    body = {row[0]: row[1] for row in datatable[1:]}
    context["response"] = client.request(method, endpoint, json=body)


@then(parsers.parse("la respuesta tiene código de estado {status:d}"))
def check_status_code(context, status):
    """Verifica el código de estado HTTP de la respuesta."""
    assert context["response"].status_code == status


@then(parsers.parse('el JSON de respuesta contiene "{field}" con valor "{value}"'))
def check_json_field(context, field, value):
    """Verifica que un campo del JSON de respuesta tenga el valor esperado."""
    data = context["response"].json()
    assert field in data
    assert str(data[field]) == value

# Notas de implementación:
# - Reemplazar {APP_IMPORT_PATH} por el módulo real donde se instancia FastAPI
# - Usar parsers.re para capturar method/endpoint variables del Gherkin
# - Cubrir también el JSON de error (ej. campo "detail") en escenarios negativos
