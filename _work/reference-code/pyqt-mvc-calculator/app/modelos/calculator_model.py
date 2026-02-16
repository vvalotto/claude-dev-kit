"""
Modelo de la calculadora - Lógica matemática pura.

Este módulo contiene la lógica de negocio para operaciones matemáticas básicas.
Sigue el patrón MVC, donde el Modelo es independiente de la Vista y el Controlador.
"""

from typing import Optional


class CalculatorModel:
    """
    Modelo para operaciones matemáticas básicas.

    Attributes:
        current_value (float): Valor actual en el display
        pending_value (float): Valor almacenado para operación pendiente
        pending_operation (Optional[str]): Operación pendiente (+, -, *, /)
    """

    def __init__(self):
        """Inicializa el modelo con valores por defecto."""
        self.current_value: float = 0.0
        self.pending_value: float = 0.0
        self.pending_operation: Optional[str] = None

    def add(self, a: float, b: float) -> float:
        """
        Suma dos números.

        Args:
            a: Primer operando
            b: Segundo operando

        Returns:
            Suma de a + b
        """
        return a + b

    def subtract(self, a: float, b: float) -> float:
        """
        Resta dos números.

        Args:
            a: Minuendo
            b: Sustraendo

        Returns:
            Diferencia de a - b
        """
        return a - b

    def multiply(self, a: float, b: float) -> float:
        """
        Multiplica dos números.

        Args:
            a: Primer factor
            b: Segundo factor

        Returns:
            Producto de a * b
        """
        return a * b

    def divide(self, a: float, b: float) -> float:
        """
        Divide dos números.

        Args:
            a: Dividendo
            b: Divisor

        Returns:
            Cociente de a / b

        Raises:
            ZeroDivisionError: Si b es 0
        """
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return a / b

    def reset(self) -> None:
        """Reinicia todos los valores a su estado inicial."""
        self.current_value = 0.0
        self.pending_value = 0.0
        self.pending_operation = None

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
            result = operation_func(self.pending_value, new_value)
            self.current_value = result
            return result

        return new_value
