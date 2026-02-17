"""
Modelo de la calculadora - Lógica matemática pura.

Este módulo contiene el estado y operaciones matemáticas siguiendo el patrón MVC.
El modelo es inmutable (dataclass frozen) y no conoce la Vista.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class CalculatorModelo:
    """
    Modelo inmutable para la calculadora.

    Attributes:
        current_value (float): Valor actual mostrado
        pending_value (float): Valor almacenado para operación pendiente
        pending_operation (Optional[str]): Operación pendiente (+, -, *, /)
    """

    current_value: float = 0.0
    pending_value: float = 0.0
    pending_operation: Optional[str] = None

    def add(self, a: float, b: float) -> float:
        """Suma dos números."""
        return a + b

    def subtract(self, a: float, b: float) -> float:
        """Resta dos números."""
        return a - b

    def multiply(self, a: float, b: float) -> float:
        """Multiplica dos números."""
        return a * b

    def divide(self, a: float, b: float) -> float:
        """
        Divide dos números.

        Raises:
            ZeroDivisionError: Si b es 0
        """
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return a / b

    def execute_pending_operation(self, new_value: float) -> float:
        """
        Ejecuta la operación pendiente con el nuevo valor.

        Args:
            new_value: Valor actual para operar

        Returns:
            Resultado de la operación

        Raises:
            ZeroDivisionError: Si hay división por cero
        """
        if self.pending_operation is None:
            return new_value

        operations = {
            '+': self.add,
            '-': self.subtract,
            '*': self.multiply,
            '/': self.divide
        }

        operation_func = operations.get(self.pending_operation)
        if operation_func:
            return operation_func(self.pending_value, new_value)

        return new_value
