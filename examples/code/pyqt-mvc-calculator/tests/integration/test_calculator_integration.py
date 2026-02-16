"""
Tests de integración end-to-end de la calculadora.
"""

import pytest
from pytestqt.qtbot import QtBot
from PyQt6.QtWidgets import QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from app.modelos.calculator_model import CalculatorModel
from app.controladores.calculator_controller import CalculatorController
from app.presentacion.main_window import MainWindow


@pytest.fixture
def calculator_app(qtbot: QtBot):
    """Fixture que crea la aplicación completa."""
    model = CalculatorModel()
    controller = CalculatorController(model)
    window = MainWindow(controller)
    qtbot.addWidget(window)
    window.show()
    return window


class TestCalculatorIntegration:
    """Tests de integración completos."""

    def test_full_addition_flow(self, calculator_app, qtbot):
        """Test del flujo completo de suma: 5 + 3 = 8."""
        window = calculator_app

        # Simular clicks: 5 + 3 =
        buttons = window.findChildren(QPushButton)
        button_5 = [b for b in buttons if b.text() == '5'][0]
        button_plus = [b for b in buttons if b.text() == '+'][0]
        button_3 = [b for b in buttons if b.text() == '3'][0]
        button_equals = [b for b in buttons if b.text() == '='][0]

        qtbot.mouseClick(button_5, Qt.MouseButton.LeftButton)
        assert window.display.text() == '5'

        qtbot.mouseClick(button_plus, Qt.MouseButton.LeftButton)
        assert window.display.text() == '5'

        qtbot.mouseClick(button_3, Qt.MouseButton.LeftButton)
        assert window.display.text() == '3'

        qtbot.mouseClick(button_equals, Qt.MouseButton.LeftButton)
        assert window.display.text() == '8.0'

    def test_full_division_by_zero_flow(self, calculator_app, qtbot, monkeypatch):
        """Test del flujo de división por cero muestra error."""
        window = calculator_app

        # Mock QMessageBox.critical para evitar diálogo real
        def mock_critical(*args, **kwargs):
            pass
        monkeypatch.setattr(QMessageBox, 'critical', mock_critical)

        # Simular clicks: 8 / 0 =
        buttons = window.findChildren(QPushButton)
        button_8 = [b for b in buttons if b.text() == '8'][0]
        button_div = [b for b in buttons if b.text() == '/'][0]
        button_0 = [b for b in buttons if b.text() == '0'][0]
        button_equals = [b for b in buttons if b.text() == '='][0]

        qtbot.mouseClick(button_8, Qt.MouseButton.LeftButton)
        qtbot.mouseClick(button_div, Qt.MouseButton.LeftButton)
        qtbot.mouseClick(button_0, Qt.MouseButton.LeftButton)
        qtbot.mouseClick(button_equals, Qt.MouseButton.LeftButton)

        # Después del error, debe resetear a 0
        assert window.display.text() == '0'

    def test_clear_functionality(self, calculator_app, qtbot):
        """Test del botón clear limpia el display."""
        window = calculator_app

        buttons = window.findChildren(QPushButton)
        button_1 = [b for b in buttons if b.text() == '1'][0]
        button_2 = [b for b in buttons if b.text() == '2'][0]
        button_clear = [b for b in buttons if b.text() == 'C'][0]

        # Ingresar 12
        qtbot.mouseClick(button_1, Qt.MouseButton.LeftButton)
        qtbot.mouseClick(button_2, Qt.MouseButton.LeftButton)
        assert window.display.text() == '12'

        # Clear
        qtbot.mouseClick(button_clear, Qt.MouseButton.LeftButton)
        assert window.display.text() == '0'

    def test_chained_operations(self, calculator_app, qtbot):
        """Test de operaciones encadenadas: 5 + 3 + 2 = 10."""
        window = calculator_app

        buttons = window.findChildren(QPushButton)
        button_5 = [b for b in buttons if b.text() == '5'][0]
        button_plus = [b for b in buttons if b.text() == '+'][0]
        button_3 = [b for b in buttons if b.text() == '3'][0]
        button_2 = [b for b in buttons if b.text() == '2'][0]
        button_equals = [b for b in buttons if b.text() == '='][0]

        # 5 + 3 + 2 =
        qtbot.mouseClick(button_5, Qt.MouseButton.LeftButton)
        qtbot.mouseClick(button_plus, Qt.MouseButton.LeftButton)
        qtbot.mouseClick(button_3, Qt.MouseButton.LeftButton)
        assert window.display.text() == '3'

        qtbot.mouseClick(button_plus, Qt.MouseButton.LeftButton)
        # Debería ejecutar 5+3=8 y guardar +
        assert window.display.text() == '8.0'

        qtbot.mouseClick(button_2, Qt.MouseButton.LeftButton)
        qtbot.mouseClick(button_equals, Qt.MouseButton.LeftButton)
        assert window.display.text() == '10.0'
