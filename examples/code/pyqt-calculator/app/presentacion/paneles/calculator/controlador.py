"""
Controlador de la calculadora - Lógica de coordinación MVC.

Este módulo coordina el Modelo y la Vista siguiendo el patrón MVC.
El controlador maneja la lógica de negocio y eventos.
"""

from dataclasses import replace
from PyQt6.QtWidgets import QMessageBox
from .modelo import CalculatorModelo
from .vista import CalculatorVista


class CalculatorControlador:
    """
    Controlador que coordina Modelo y Vista.

    Attributes:
        modelo (CalculatorModelo): Instancia del modelo
        vista (CalculatorVista): Instancia de la vista
        current_input (str): Dígitos acumulados del input actual
        waiting_for_operand (bool): Flag para nuevo operando
    """

    def __init__(self, modelo: CalculatorModelo, vista: CalculatorVista):
        """
        Inicializa el controlador.

        Args:
            modelo: Instancia del modelo
            vista: Instancia de la vista
        """
        self.modelo = modelo
        self.vista = vista
        self.current_input = "0"
        self.waiting_for_operand = False

        # Conectar señales de la vista
        self.vista.button_clicked.connect(self._on_button_clicked)

    def _on_button_clicked(self, button_label: str):
        """
        Maneja clicks de botones.

        Args:
            button_label: Etiqueta del botón presionado
        """
        if button_label.isdigit() or button_label == '.':
            self._handle_number_input(button_label)
        elif button_label in ['+', '-', '*', '/']:
            self._handle_operation(button_label)
        elif button_label == '=':
            self._handle_equals()
        elif button_label == 'C':
            self._handle_clear()

    def _handle_number_input(self, digit: str):
        """Maneja input de dígitos numéricos."""
        if self.waiting_for_operand:
            self.current_input = digit
            self.waiting_for_operand = False
        else:
            if self.current_input == "0" and digit != ".":
                self.current_input = digit
            else:
                self.current_input += digit

        self.vista.update_display(self.current_input)

    def _handle_operation(self, operation: str):
        """Maneja input de operaciones (+, -, *, /)."""
        try:
            current_value = float(self.current_input)

            # Si hay operación pendiente, ejecutarla primero
            if self.modelo.pending_operation is not None:
                result = self.modelo.execute_pending_operation(current_value)
                self.current_input = str(result)
                self.vista.update_display(self.current_input)

            # Actualizar modelo con nueva operación (inmutable)
            self.modelo = replace(
                self.modelo,
                pending_value=float(self.current_input),
                pending_operation=operation
            )
            self.waiting_for_operand = True

        except ZeroDivisionError:
            self._show_error("Cannot divide by zero")
            self._handle_clear()

    def _handle_equals(self):
        """Maneja presión del botón equals (=)."""
        if self.modelo.pending_operation is None:
            return

        try:
            current_value = float(self.current_input)
            result = self.modelo.execute_pending_operation(current_value)
            self.current_input = str(result)
            self.vista.update_display(self.current_input)

            # Limpiar operación pendiente (inmutable)
            self.modelo = replace(
                self.modelo,
                current_value=result,
                pending_operation=None
            )
            self.waiting_for_operand = True

        except ZeroDivisionError:
            self._show_error("Cannot divide by zero")
            self._handle_clear()

    def _handle_clear(self):
        """Maneja presión del botón clear (C)."""
        self.modelo = CalculatorModelo()  # Reset a estado inicial
        self.current_input = "0"
        self.waiting_for_operand = False
        self.vista.update_display(self.current_input)

    def _show_error(self, message: str):
        """
        Muestra un diálogo de error.

        Args:
            message: Mensaje de error
        """
        QMessageBox.critical(self.vista, "Error", message)
