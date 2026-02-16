# Calculadora PyQt - Ejemplo del Claude Dev Kit

Este es un ejemplo completo de aplicación PyQt6 construida siguiendo el patrón MVC (Model-View-Controller) como demostración del **Claude Dev Kit** con el perfil `pyqt-mvc`.

## 🎯 Descripción

Calculadora simple de escritorio que implementa:
- ✅ Operaciones básicas (+, -, *, /)
- ✅ Interfaz gráfica con PyQt6
- ✅ Arquitectura MVC limpia
- ✅ Tests completos (unitarios + integración)
- ✅ Validación de calidad (Pylint, Coverage)

## 📋 Requisitos

- Python 3.10 o superior
- PyQt6 >= 6.4.0
- pytest >= 7.4.0
- pytest-qt >= 4.2.0

## 🚀 Instalación

```bash
# Clonar el repositorio
cd examples/code/pyqt-mvc-calculator

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

## ▶️ Ejecución

```bash
# Ejecutar la calculadora
python main.py
```

## 🧪 Tests

```bash
# Ejecutar todos los tests
pytest tests/ -v

# Tests con cobertura
pytest tests/ --cov=app --cov-report=term-missing

# Solo tests unitarios
pytest tests/unit/ -v

# Solo tests de integración
pytest tests/integration/ -v
```

## 🏗️ Arquitectura

### Patrón MVC

```
┌─────────────────────────────────────────┐
│              MainWindow                 │
│          (Vista / UI)                   │
│  - Display (QLineEdit)                  │
│  - Botones (QPushButton)                │
└──────────────┬──────────────────────────┘
               │
               │ eventos (clicked)
               ▼
┌─────────────────────────────────────────┐
│       CalculatorController              │
│         (Controlador)                   │
│  - handle_number_input()                │
│  - handle_operation()                   │
│  - handle_equals()                      │
└──────────────┬──────────────────────────┘
               │
               │ operaciones
               ▼
┌─────────────────────────────────────────┐
│        CalculatorModel                  │
│           (Modelo)                      │
│  - add(), subtract()                    │
│  - multiply(), divide()                 │
│  - execute_pending_operation()          │
└─────────────────────────────────────────┘
```

### Estructura de Archivos

```
pyqt-mvc-calculator/
├── app/
│   ├── __init__.py
│   ├── modelos/
│   │   ├── __init__.py
│   │   └── calculator_model.py      # Lógica matemática
│   ├── controladores/
│   │   ├── __init__.py
│   │   └── calculator_controller.py # Coordinación MVC
│   └── presentacion/
│       ├── __init__.py
│       └── main_window.py           # Interfaz gráfica
├── tests/
│   ├── unit/
│   │   ├── test_calculator_model.py
│   │   └── test_calculator_controller.py
│   └── integration/
│       └── test_calculator_integration.py
├── historias-usuario/
│   └── US-001.md                    # Historia de usuario
├── main.py                          # Entry point
├── requirements.txt                 # Dependencias
└── README.md                        # Este archivo
```

## 📊 Métricas de Calidad

- **Cobertura:** >= 90%
- **Pylint:** >= 8.5/10
- **Complejidad Ciclomática:** < 10
- **Líneas de código:** ~420 líneas

## 🎓 Tutorial

Para una guía completa paso a paso sobre cómo se construyó este ejemplo usando el Claude Dev Kit, ver:

📖 **[Tutorial: PyQt6 MVC - Calculadora Simple](../../../docs/examples/pyqt-project.md)**

## 🔗 Relacionado

- [Claude Dev Kit](https://github.com/vvalotto/claude-dev-kit)
- [Documentación PyQt6](https://doc.qt.io/qtforpython-6/)
- [pytest-qt](https://pytest-qt.readthedocs.io/)

## 📝 Licencia

Este ejemplo es parte del Claude Dev Kit y se distribuye bajo la misma licencia del proyecto principal.
