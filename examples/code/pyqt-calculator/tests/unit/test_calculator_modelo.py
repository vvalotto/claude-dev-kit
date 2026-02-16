"""
Tests unitarios del CalculatorModelo.
"""

import pytest
from dataclasses import replace
from app.presentacion.paneles.calculator.modelo import CalculatorModelo


class TestCalculatorModelo:
    """Suite de tests para CalculatorModelo."""

    @pytest.fixture
    def modelo(self):
        """Fixture que retorna una instancia del modelo."""
        return CalculatorModelo()

    def test_add(self, modelo):
        """Test de suma."""
        result = modelo.add(5, 3)
        assert result == 8

    def test_subtract(self, modelo):
        """Test de resta."""
        result = modelo.subtract(10, 3)
        assert result == 7

    def test_multiply(self, modelo):
        """Test de multiplicación."""
        result = modelo.multiply(4, 6)
        assert result == 24

    def test_divide(self, modelo):
        """Test de división."""
        result = modelo.divide(15, 3)
        assert result == 5

    def test_divide_by_zero(self, modelo):
        """Test de división por cero debe levantar excepción."""
        with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
            modelo.divide(8, 0)

    def test_modelo_is_immutable(self, modelo):
        """Test que el modelo es inmutable (frozen dataclass)."""
        with pytest.raises(AttributeError):
            modelo.current_value = 42  # type: ignore

    def test_execute_pending_operation_add(self, modelo):
        """Test de ejecución de suma pendiente."""
        # Crear nuevo modelo con operación pendiente (inmutable)
        modelo_con_operacion = replace(
            modelo,
            pending_value=5,
            pending_operation='+'
        )

        result = modelo_con_operacion.execute_pending_operation(3)
        assert result == 8

    def test_execute_pending_operation_divide_by_zero(self, modelo):
        """Test de división por cero en operación pendiente."""
        modelo_con_operacion = replace(
            modelo,
            pending_value=10,
            pending_operation='/'
        )

        with pytest.raises(ZeroDivisionError):
            modelo_con_operacion.execute_pending_operation(0)
