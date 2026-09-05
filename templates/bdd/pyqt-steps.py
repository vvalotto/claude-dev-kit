# Template: Step Definitions BDD — específico para perfil pyqt-mvc (pytest-qt)
# Referencia estructural para implementar los steps de un .feature de UI PyQt6
# en la Fase 6. No es código ejecutable — adaptar a los widgets reales.
#
# Requiere pytest-qt (fixture `qtbot`) para simular interacción de UI.
#
# Variables disponibles:
# - {FEATURE_FILE_PATH}: Ruta relativa al archivo .feature correspondiente
# - {SCENARIO_N_NAME}: Nombre del escenario N (debe coincidir literal con el .feature)
# - {MAIN_WINDOW_CLASS}: Clase de la ventana principal (vista MVC)

"""Step definitions para {FEATURE_TITLE} ({US_ID})."""

import os
import pytest
from pytest_bdd import scenario, given, when, then, parsers


FEATURE_FILE = os.path.join(os.path.dirname(__file__), "{FEATURE_FILE_PATH}")


@scenario(FEATURE_FILE, "{SCENARIO_1_NAME}")
def test_{scenario_1_slug}():
    """Test para el escenario {SCENARIO_1_NAME}."""


@pytest.fixture
def app_window(qtbot):
    """Instancia la ventana principal y la registra en qtbot."""
    window = {MAIN_WINDOW_CLASS}()
    qtbot.addWidget(window)
    window.show()
    return window


@given("que la aplicación PyQt está iniciada", target_fixture="app_window")
def app_started(app_window):
    """La ventana ya quedó instanciada por la fixture."""
    return app_window


@given(parsers.parse('que {widget} muestra "{valor}"'))
def widget_shows_initial_value(app_window, widget, valor):
    """Verifica el valor inicial de un widget antes de interactuar."""
    assert getattr(app_window, widget).text() == valor


@when(parsers.parse('el usuario hace click en "{widget}"'))
def user_clicks_widget(app_window, qtbot, widget):
    """Simula un click sobre el widget indicado."""
    qtbot.mouseClick(getattr(app_window, widget), 1)  # Qt.LeftButton


@then(parsers.parse('se muestra "{valor}" en "{widget}"'))
def widget_shows_value(app_window, widget, valor):
    """Verifica el valor final mostrado en el widget."""
    assert getattr(app_window, widget).text() == valor

# Notas de implementación:
# - `qtbot` (pytest-qt) simula eventos de usuario sin abrir una ventana real
# - Acceder a widgets por atributo de la vista (self.boton_igual, self.display, etc.)
# - Reemplazar {MAIN_WINDOW_CLASS} por la clase real de la ventana principal
