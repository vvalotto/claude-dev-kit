# Template: Escenario BDD (Gherkin)
# Este template se usa para generar archivos .feature basados en historias de usuario

Feature: {FEATURE_TITLE} ({US_ID})
  Como {USER_ROLE}
  Quiero {USER_WANT}
  Para {USER_BENEFIT}

  Background:
    Given la aplicación está iniciada
    And la configuración está cargada

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
