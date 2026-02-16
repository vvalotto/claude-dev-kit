"""
Tests unitarios del CalculatorControlador.
"""

import pytest
from unittest.mock import Mock, patch
from app.presentacion.paneles.calculator.modelo import CalculatorModelo
from app.presentacion.paneles.calculator.vista import CalculatorVista
from app.presentacion.paneles.calculator.controlador import CalculatorControlador


class TestCalculatorControlador:
    """Suite de tests para CalculatorControlador."""

    @pytest.fixture
    def qapp(self, qapp):
        """QApplication para tests."""
        return qapp

    @pytest.fixture
    def setup(self, qapp):
        """Setup con modelo, vista y controlador."""
        modelo = CalculatorModelo()
        vista = CalculatorVista()
        controlador = CalculatorControlador(modelo, vista)
        return modelo, vista, controlador

    def test_handle_number_input_single_digit(self, setup):
        """Test de input de un solo dígito."""
        _, vista, controlador = setup

        controlador._handle_number_input('5')

        assert vista.get_display_value() == '5'

    def test_handle_number_input_multiple_digits(self, setup):
        """Test de input de múltiples dígitos."""
        _, vista, controlador = setup

        controlador._handle_number_input('1')
        controlador._handle_number_input('2')
        controlador._handle_number_input('3')

        assert vista.get_display_value() == '123'

    def test_handle_clear(self, setup):
        """Test de clear resetea el controlador."""
        _, vista, controlador = setup

        controlador._handle_number_input('9')
        controlador._handle_clear()

        assert vista.get_display_value() == '0'

    def test_handle_operation_stores_value(self, setup):
        """Test que operación guarda valor actual."""
        _, _, controlador = setup

        controlador._handle_number_input('5')
        controlador._handle_operation('+')

        assert controlador.modelo.pending_value == 5.0
        assert controlador.modelo.pending_operation == '+'
        assert controlador.waiting_for_operand is True

    def test_handle_equals_simple_addition(self, setup):
        """Test de equals con suma simple."""
        _, vista, controlador = setup

        controlador._handle_number_input('5')
        controlador._handle_operation('+')
        controlador._handle_number_input('3')
        controlador._handle_equals()

        assert vista.get_display_value() == '8.0'

    @patch('app.presentacion.paneles.calculator.controlador.QMessageBox')
    def test_handle_equals_division_by_zero(self, mock_qmessage, setup):
        """Test de equals con división por cero."""
        _, vista, controlador = setup

        controlador._handle_number_input('8')
        controlador._handle_operation('/')
        controlador._handle_number_input('0')
        controlador._handle_equals()

        # Verifica que se mostró error y se limpió
        mock_qmessage.critical.assert_called_once()
        assert vista.get_display_value() == '0'
