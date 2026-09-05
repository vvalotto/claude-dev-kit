# Template: Escenario BDD (Gherkin) — específico para perfil pyqt-mvc
# Este template se usa como referencia estructural para generar archivos
# .feature de features con interfaz gráfica PyQt6.
#
# Variables disponibles: ver templates/bdd/scenario.feature (genérico).
# Diferencia respecto al genérico: steps orientados a interacción de UI
# (widgets, clicks, valores mostrados) en vez de HTTP/dominio puro.
#
# Step patterns de referencia (ver customizations/pyqt-mvc.json → bdd_config):
# - given_ui: "Dado que la aplicación PyQt está iniciada"
# - when_click: "Cuando el usuario hace click en {widget}"
# - then_display: "Entonces se muestra {value} en {widget}"

Feature: {FEATURE_TITLE} ({US_ID})
  Como {USER_ROLE}
  Quiero {USER_WANT}
  Para {USER_BENEFIT}

  Background:
    Dado que la aplicación PyQt está iniciada
    Y la configuración está cargada

  Scenario: {SCENARIO_1_NAME}
    Dado que {widget_inicial} muestra "{VALOR_INICIAL}"
    Cuando el usuario hace click en "{WIDGET_1}"
    Y el usuario hace click en "{WIDGET_2}"
    Entonces se muestra "{VALOR_ESPERADO}" en "{widget_resultado}"

  Scenario: {SCENARIO_2_NAME}
    Dado que {PRECONDICION}
    Cuando el usuario hace click en "{WIDGET}"
    Entonces se muestra "{VALOR_ESPERADO}" en "{widget_resultado}"

  # Agregar más escenarios según criterios de aceptación

# Notas de implementación:
# - Un escenario por cada criterio de aceptación principal
# - Given: estado inicial de la UI (valores en pantalla, configuración cargada)
# - When: interacción del usuario (click, tipeo, selección)
# - Then: valor observable en un widget concreto
# - Usar nombres de widget consistentes con los definidos en la vista (MVC)
