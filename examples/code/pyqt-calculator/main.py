"""
Entry point de la aplicación de calculadora PyQt6 MVC.

Este módulo inicializa la aplicación y conecta los componentes MVC.
"""

import sys
from PyQt6.QtWidgets import QApplication
from app.presentacion.paneles.calculator.modelo import CalculatorModelo
from app.presentacion.paneles.calculator.vista import CalculatorVista
from app.presentacion.paneles.calculator.controlador import CalculatorControlador


def main():
    """Función principal de la aplicación."""
    # Crear aplicación Qt
    app = QApplication(sys.argv)

    # Crear componentes MVC
    modelo = CalculatorModelo()
    vista = CalculatorVista()
    controlador = CalculatorControlador(modelo, vista)

    # Mostrar ventana
    vista.show()

    # Ejecutar aplicación
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
