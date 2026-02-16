"""
Vista de la calculadora - Interfaz gráfica PyQt6.

Este módulo define la interfaz de usuario siguiendo el patrón MVC.
La vista solo se encarga de UI y emisión de señales.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout,
    QLineEdit, QPushButton
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class CalculatorVista(QWidget):
    """
    Vista de la calculadora con botones y display.

    Signals:
        button_clicked(str): Emitido cuando se presiona un botón
    """

    # Señal para comunicar clicks de botones al controlador
    button_clicked = pyqtSignal(str)

    def __init__(self, parent=None):
        """Inicializa la vista."""
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        """Construye la interfaz de usuario."""
        self.setWindowTitle("Calculadora Simple")
        self.setFixedSize(300, 400)

        # Layout principal
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

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

        # Definir botones (label, row, col, rowspan, colspan)
        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
            ('0', 3, 0), ('.', 3, 1), ('=', 3, 2), ('+', 3, 3),
            ('C', 4, 0, 1, 4)  # Clear ocupa toda la fila
        ]

        # Crear botones
        for button_def in buttons:
            label = button_def[0]
            row = button_def[1]
            col = button_def[2]
            rowspan = button_def[3] if len(button_def) > 3 else 1
            colspan = button_def[4] if len(button_def) > 4 else 1

            button = QPushButton(label)
            button.setFont(QFont('Arial', 16))
            button.setFixedHeight(60)

            # Conectar señal
            button.clicked.connect(lambda checked, l=label: self.button_clicked.emit(l))

            buttons_layout.addWidget(button, row, col, rowspan, colspan)

    def update_display(self, value: str):
        """
        Actualiza el valor mostrado en el display.

        Args:
            value: Valor a mostrar
        """
        self.display.setText(value)

    def get_display_value(self) -> str:
        """
        Obtiene el valor actual del display.

        Returns:
            Valor del display
        """
        return self.display.text()
