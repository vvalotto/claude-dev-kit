"""
Tests unitarios del CalculatorModel.
"""

import pytest
from app.modelos.calculator_model import CalculatorModel


class TestCalculatorModel:
    """Suite de tests para CalculatorModel."""

    @pytest.fixture
    def model(self):
        """Fixture que retorna una instancia del modelo."""
        return CalculatorModel()

    def test_add(self, model):
        """Test de suma."""
        result = model.add(5, 3)
        assert result == 8

    def test_subtract(self, model):
        """Test de resta."""
        result = model.subtract(10, 3)
        assert result == 7

    def test_multiply(self, model):
        """Test de multiplicación."""
        result = model.multiply(4, 6)
        assert result == 24

    def test_divide(self, model):
        """Test de división."""
        result = model.divide(15, 3)
        assert result == 5

    def test_divide_by_zero(self, model):
        """Test de división por cero debe levantar excepción."""
        with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
            model.divide(8, 0)

    def test_reset(self, model):
        """Test de reset limpia todos los valores."""
        model.current_value = 42
        model.pending_value = 10
        model.pending_operation = '+'

        model.reset()

        assert model.current_value == 0.0
        assert model.pending_value == 0.0
        assert model.pending_operation is None

    def test_execute_pending_operation_add(self, model):
        """Test de ejecución de suma pendiente."""
        model.pending_value = 5
        model.pending_operation = '+'

        result = model.execute_pending_operation(3)

        assert result == 8
        assert model.current_value == 8

    def test_execute_pending_operation_divide_by_zero(self, model):
        """Test de división por cero en operación pendiente."""
        model.pending_value = 10
        model.pending_operation = '/'

        with pytest.raises(ZeroDivisionError):
            model.execute_pending_operation(0)
