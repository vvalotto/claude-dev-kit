"""
Entry point de la aplicación de calculadora.

Este módulo inicializa la aplicación PyQt6 y conecta todos los componentes.
"""

import sys
from PyQt6.QtWidgets import QApplication
from app.modelos.calculator_model import CalculatorModel
from app.controladores.calculator_controller import CalculatorController
from app.presentacion.main_window import MainWindow


def main():
    """Función principal de la aplicación."""
    # Crear aplicación Qt
    app = QApplication(sys.argv)

    # Crear componentes MVC
    model = CalculatorModel()
    controller = CalculatorController(model)
    window = MainWindow(controller)

    # Mostrar ventana
    window.show()

    # Ejecutar aplicación
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
