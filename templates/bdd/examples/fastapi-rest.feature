# Template: Escenario BDD (Gherkin)
# Este template se usa para generar archivos .feature basados en historias de usuario
#
# Ejemplo generado para perfil: fastapi-rest
# Historia: US-001 - Implementar Endpoint de Temperatura

Feature: Endpoint de Temperatura (US-001)
  Como cliente de la API
  Quiero consultar la temperatura actual
  Para integrar el termostato con otros sistemas

  Background:
    Given el servidor API está corriendo
    And las variables de entorno están configuradas

  Scenario: Obtener temperatura actual
    Given el termostato está conectado
    And la temperatura es de 22 grados
    When se hace GET a "/api/temperatura"
    Then el código de respuesta es 200
    And el JSON contiene "temperatura": 22

  Scenario: Manejar termostato desconectado
    Given el termostato NO está conectado
    When se hace GET a "/api/temperatura"
    Then el código de respuesta es 503
    And el error contiene "Termostato desconectado"

  # Agregar más escenarios según criterios de aceptación

# Notas de implementación:
# - Un escenario por cada criterio de aceptación principal
# - Given: Estado inicial/precondiciones
# - When: Acción del usuario o evento del sistema
# - Then: Resultado observable esperado
# - And/But: Para múltiples condiciones
