# Template: Escenario BDD (Gherkin)
# Este template se usa para generar archivos .feature basados en historias de usuario
#
# Variables disponibles:
# - {FEATURE_TITLE}: Título de la feature
# - {US_ID}: ID de historia de usuario (ej. US-001)
# - {USER_ROLE}: Rol del usuario (ej. "un usuario", "un administrador")
# - {USER_WANT}: Acción que quiere realizar
# - {USER_BENEFIT}: Beneficio esperado
# - {BACKGROUND_SETUP}: Steps de setup inicial (específico del perfil)
# - {SCENARIO_N_NAME}: Nombre del escenario N
# - {PRECONDITION_N}: Precondición N
# - {ACTION}: Acción principal del escenario
# - {EXPECTED_RESULT_N}: Resultado esperado N

Feature: {FEATURE_TITLE} ({US_ID})
  Como {USER_ROLE}
  Quiero {USER_WANT}
  Para {USER_BENEFIT}

  Background:
{BACKGROUND_SETUP}

  Scenario: {SCENARIO_1_NAME}
    Given {PRECONDITION_1}
    And {PRECONDITION_2}
    When {ACTION}
    Then {EXPECTED_RESULT_1}
    And {EXPECTED_RESULT_2}

  Scenario: {SCENARIO_2_NAME}
    Given {PRECONDITION}
    When {ACTION}
    Then {EXPECTED_RESULT}

  # Agregar más escenarios según criterios de aceptación

# Notas de implementación:
# - Un escenario por cada criterio de aceptación principal
# - Given: Estado inicial/precondiciones
# - When: Acción del usuario o evento del sistema
# - Then: Resultado observable esperado
# - And/But: Para múltiples condiciones
