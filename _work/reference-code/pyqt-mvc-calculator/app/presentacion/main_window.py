"""
Vista principal de la calculadora - Interfaz gráfica.

Este módulo define la ventana principal con todos los botones y el display.
Sigue el patrón MVC, donde la Vista solo se encarga de la UI.
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QGridLayout,
    QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from app.controladores.calculator_controller import CalculatorController


class MainWindow(QMainWindow):
    """
    Ventana principal de la calculadora.

    Attributes:
        controller (CalculatorController): Controlador de la aplicación
        display (QLineEdit): Display para mostrar números y resultados
    """

    def __init__(self, controller: CalculatorController):
        """
        Inicializa la ventana principal.

        Args:
            controller: Instancia del controlador
        """
        super().__init__()
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        """Inicializa la interfaz de usuario."""
        self.setWindowTitle("Calculadora Simple")
        self.setFixedSize(300, 400)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Display
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setFont(QFont('Arial', 20))
        self.display.setFixedHeight(50)
        self.display.setText("0")
        main_layout.addWidget(self.display)

        # Grid de botones
        buttons_layout = QGridLayout()
        main_layout.addLayout(buttons_layout)

        # Definir botones
        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
            ('0', 3, 0), ('.', 3, 1), ('=', 3, 2), ('+', 3, 3),
            ('C', 4, 0, 1, 4)  # Clear ocupa toda la fila
        ]

        # Crear y posicionar botones
        for button_def in buttons:
            label = button_def[0]
            row = button_def[1]
            col = button_def[2]
            rowspan = button_def[3] if len(button_def) > 3 else 1
            colspan = button_def[4] if len(button_def) > 4 else 1

            button = QPushButton(label)
            button.setFont(QFont('Arial', 16))
            button.setFixedHeight(60)

            # Conectar señal según tipo de botón
            if label.isdigit() or label == '.':
                button.clicked.connect(lambda checked, l=label: self.on_number_clicked(l))
            elif label in ['+', '-', '*', '/']:
                button.clicked.connect(lambda checked, l=label: self.on_operation_clicked(l))
            elif label == '=':
                button.clicked.connect(self.on_equals_clicked)
            elif label == 'C':
                button.clicked.connect(self.on_clear_clicked)

            buttons_layout.addWidget(button, row, col, rowspan, colspan)

    def on_number_clicked(self, digit: str):
        """
        Maneja click en botón numérico.

        Args:
            digit: Dígito presionado
        """
        result = self.controller.handle_number_input(digit)
        self.update_display(result)

    def on_operation_clicked(self, operation: str):
        """
        Maneja click en botón de operación.

        Args:
            operation: Operación presionada (+, -, *, /)
        """
        try:
            result = self.controller.handle_operation(operation)
            self.update_display(result)
        except ZeroDivisionError:
            self.show_error("Cannot divide by zero")
            self.on_clear_clicked()

    def on_equals_clicked(self):
        """Maneja click en botón equals (=)."""
        try:
            result = self.controller.handle_equals()
            self.update_display(result)
        except ZeroDivisionError:
            self.show_error("Cannot divide by zero")
            self.on_clear_clicked()

    def on_clear_clicked(self):
        """Maneja click en botón clear (C)."""
        result = self.controller.handle_clear()
        self.update_display(result)

    def update_display(self, value: str):
        """
        Actualiza el display con un nuevo valor.

        Args:
            value: Valor a mostrar
        """
        self.display.setText(value)

    def show_error(self, message: str):
        """
        Muestra un diálogo de error.

        Args:
            message: Mensaje de error
        """
        QMessageBox.critical(self, "Error", message)
