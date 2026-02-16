"""
Controlador de la calculadora - Lógica de coordinación.

Este módulo actúa como intermediario entre la Vista (MainWindow) y el Modelo
(CalculatorModel). Maneja eventos de la UI y actualiza el modelo.
"""

from app.modelos.calculator_model import CalculatorModel


class CalculatorController:
    """
    Controlador que coordina la Vista y el Modelo.

    Attributes:
        model (CalculatorModel): Instancia del modelo
        current_input (str): Dígitos acumulados del input actual
        waiting_for_operand (bool): Flag para nuevo operando
    """

    def __init__(self, model: CalculatorModel):
        """
        Inicializa el controlador.

        Args:
            model: Instancia del modelo de calculadora
        """
        self.model = model
        self.current_input: str = "0"
        self.waiting_for_operand: bool = False

    def handle_number_input(self, digit: str) -> str:
        """
        Maneja input de dígitos numéricos.

        Args:
            digit: Dígito presionado (0-9 o '.')

        Returns:
            String actualizado para mostrar en display
        """
        if self.waiting_for_operand:
            self.current_input = digit
            self.waiting_for_operand = False
        else:
            if self.current_input == "0" and digit != ".":
                self.current_input = digit
            else:
                self.current_input += digit

        return self.current_input

    def handle_operation(self, operation: str) -> str:
        """
        Maneja input de operaciones (+, -, *, /).

        Args:
            operation: Símbolo de operación

        Returns:
            String actualizado para mostrar en display

        Raises:
            ZeroDivisionError: Si hay división por cero en operación pendiente
        """
        current_value = float(self.current_input)

        # Si hay una operación pendiente, ejecutarla primero
        if self.model.pending_operation is not None:
            try:
                result = self.model.execute_pending_operation(current_value)
                self.current_input = str(result)
            except ZeroDivisionError:
                raise

        # Guardar el valor actual y la nueva operación
        self.model.pending_value = float(self.current_input)
        self.model.pending_operation = operation
        self.waiting_for_operand = True

        return self.current_input

    def handle_equals(self) -> str:
        """
        Maneja presión del botón equals (=).

        Returns:
            Resultado de la operación como string

        Raises:
            ZeroDivisionError: Si hay división por cero
        """
        if self.model.pending_operation is None:
            return self.current_input

        current_value = float(self.current_input)

        try:
            result = self.model.execute_pending_operation(current_value)
            self.current_input = str(result)
            self.model.pending_operation = None
            self.waiting_for_operand = True
            return self.current_input
        except ZeroDivisionError:
            raise

    def handle_clear(self) -> str:
        """
        Maneja presión del botón clear (C).

        Returns:
            "0" para resetear el display
        """
        self.model.reset()
        self.current_input = "0"
        self.waiting_for_operand = False
        return self.current_input

    def get_current_display(self) -> str:
        """
        Obtiene el valor actual a mostrar.

        Returns:
            String para el display
        """
        return self.current_input
