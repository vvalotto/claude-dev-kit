# Template: Step Definitions BDD (pytest-bdd) — genérico
# Este template se usa como referencia estructural para implementar los steps
# de un archivo .feature en la Fase 6 (Validación BDD).
#
# No es código ejecutable — es una guía de estructura. Adaptar imports,
# fixtures y aserciones al stack real del componente bajo test.
#
# Variables disponibles:
# - {FEATURE_FILE_PATH}: Ruta relativa al archivo .feature correspondiente
# - {SCENARIO_N_NAME}: Nombre del escenario N (debe coincidir literal con el .feature)

"""Step definitions para {FEATURE_TITLE} ({US_ID})."""

import os
import pytest
from pytest_bdd import scenario, given, when, then, parsers


FEATURE_FILE = os.path.join(os.path.dirname(__file__), "{FEATURE_FILE_PATH}")


# Un decorador @scenario por cada Scenario del .feature — el nombre debe
# coincidir literal con el texto tras "Scenario:"
@scenario(FEATURE_FILE, "{SCENARIO_1_NAME}")
def test_{scenario_1_slug}():
    """Test para el escenario {SCENARIO_1_NAME}."""


@pytest.fixture
def context():
    """Estado compartido entre steps de un mismo escenario."""
    return {}


# Given steps — precondiciones
@given("{PRECONDITION}", target_fixture="context")
def given_precondition(context):
    """Configura el estado inicial descrito en la precondición."""
    return context


# When steps — acción/evento bajo test
@when(parsers.parse("{ACTION}"))
def when_action(context):
    """Ejecuta la acción principal del escenario."""


# Then steps — resultado observable
@then(parsers.parse("{EXPECTED_RESULT}"))
def then_expected_result(context):
    """Verifica el resultado esperado."""
    assert context is not None

# Notas de implementación:
# - Un @scenario por Scenario del .feature, con el texto exacto como nombre
# - given/when/then deben matchear el texto Gherkin (usar parsers.parse
#   o parsers.re para capturar variables entre llaves)
# - Reutilizar la fixture `context` para pasar estado entre steps
