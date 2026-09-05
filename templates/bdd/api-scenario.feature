# Template: Escenario BDD (Gherkin) — específico para perfil fastapi-rest
# Este template se usa como referencia estructural para generar archivos
# .feature de endpoints REST.
#
# Variables disponibles: ver templates/bdd/scenario.feature (genérico).
# Diferencia respecto al genérico: steps orientados a request/response HTTP.
#
# Step patterns de referencia (ver customizations/fastapi-rest.json → bdd_config):
# - given_api: "Dado que la API está disponible"
# - when_request: "Cuando se envía una petición {method} a {endpoint}"
# - then_response: "Entonces la respuesta tiene código de estado {status}"
# - then_json: "Y el JSON de respuesta contiene {field} con valor {value}"

Feature: {FEATURE_TITLE} ({US_ID})
  Como {USER_ROLE}
  Quiero {USER_WANT}
  Para {USER_BENEFIT}

  Background:
    Dado que la API está disponible

  Scenario: {SCENARIO_1_NAME}
    Cuando se envía una petición {METODO} a "{ENDPOINT}" con:
      | campo         | valor           |
      | {CAMPO_1}     | {VALOR_1}       |
    Entonces la respuesta tiene código de estado {STATUS_ESPERADO}
    Y el JSON de respuesta contiene "{CAMPO_1}" con valor "{VALOR_1}"

  Scenario: {SCENARIO_2_NAME}
    Dado que {PRECONDICION}
    Cuando se envía una petición {METODO} a "{ENDPOINT}"
    Entonces la respuesta tiene código de estado {STATUS_ESPERADO}

  # Agregar más escenarios según criterios de aceptación (incluyendo errores 4xx/5xx)

# Notas de implementación:
# - Un escenario por cada criterio de aceptación principal
# - Given: estado previo de la base de datos/recursos
# - When: petición HTTP (método + endpoint + body opcional)
# - Then: código de estado y contenido del JSON de respuesta
# - Cubrir al menos un escenario de error (404, 400, 422 según el endpoint)
