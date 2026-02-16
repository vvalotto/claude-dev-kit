"""
Tests unitarios del CalculatorController.
"""

import pytest
from app.modelos.calculator_model import CalculatorModel
from app.controladores.calculator_controller import CalculatorController


class TestCalculatorController:
    """Suite de tests para CalculatorController."""

    @pytest.fixture
    def controller(self):
        """Fixture que retorna un controlador con modelo."""
        model = CalculatorModel()
        return CalculatorController(model)

    def test_handle_number_input_single_digit(self, controller):
        """Test de input de un solo dígito."""
        result = controller.handle_number_input('5')
        assert result == '5'

    def test_handle_number_input_multiple_digits(self, controller):
        """Test de input de múltiples dígitos."""
        controller.handle_number_input('1')
        controller.handle_number_input('2')
        result = controller.handle_number_input('3')
        assert result == '123'

    def test_handle_clear(self, controller):
        """Test de clear resetea el controlador."""
        controller.handle_number_input('9')
        result = controller.handle_clear()
        assert result == '0'

    def test_handle_operation_stores_value(self, controller):
        """Test que operación guarda valor actual."""
        controller.handle_number_input('5')
        controller.handle_operation('+')

        assert controller.model.pending_value == 5.0
        assert controller.model.pending_operation == '+'
        assert controller.waiting_for_operand is True

    def test_handle_equals_simple_addition(self, controller):
        """Test de equals con suma simple."""
        controller.handle_number_input('5')
        controller.handle_operation('+')
        controller.handle_number_input('3')
        result = controller.handle_equals()

        assert result == '8.0'

    def test_handle_equals_division_by_zero(self, controller):
        """Test de equals con división por cero."""
        controller.handle_number_input('8')
        controller.handle_operation('/')
        controller.handle_number_input('0')

        with pytest.raises(ZeroDivisionError):
            controller.handle_equals()
