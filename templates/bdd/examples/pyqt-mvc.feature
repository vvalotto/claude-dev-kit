# Template: Escenario BDD (Gherkin)
# Este template se usa para generar archivos .feature basados en historias de usuario
#
# Ejemplo generado para perfil: pyqt-mvc
# Historia: US-001 - Implementar Display de Temperatura

Feature: Display de Temperatura (US-001)
  Como usuario
  Quiero ver la temperatura actual del termostato
  Para monitorear el estado del sistema

  Background:
    Given la aplicación está iniciada
    And la configuración está cargada

  Scenario: Mostrar temperatura actual
    Given el termostato está conectado
    And la temperatura es de 22 grados
    When el usuario abre el panel de display
    Then se muestra la temperatura "22°C"
    And el indicador de conexión está verde

  Scenario: Actualizar temperatura en tiempo real
    Given el panel de display está abierto
    When la temperatura cambia a 24 grados
    Then la UI se actualiza automáticamente
    And se muestra la temperatura "24°C"

  # Agregar más escenarios según criterios de aceptación

# Notas de implementación:
# - Un escenario por cada criterio de aceptación principal
# - Given: Estado inicial/precondiciones
# - When: Acción del usuario o evento del sistema
# - Then: Resultado observable esperado
# - And/But: Para múltiples condiciones
