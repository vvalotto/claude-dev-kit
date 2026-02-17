# Plan de Implementación - US-001: Calculadora Simple

**Fecha:** 2026-02-16
**Perfil:** pyqt-mvc
**Arquitectura:** MVC (Model-View-Controller)

---

## 📊 Resumen Ejecutivo

**Componente:** Calculator
**Patrón:** MVC con separación estricta
**Estructura:** app/presentacion/paneles/calculator/
**Estimación:** 2.5 horas

---

## 🏗️ Arquitectura MVC

### Modelo (modelo.py)
**Clase:** CalculatorModelo
**Base:** ModeloBase (dataclass frozen=True)
**Responsabilidades:**
- Estado del panel (current_value, pending_value, pending_operation)
- Operaciones matemáticas (add, subtract, multiply, divide)
- Validación (división por cero)

### Vista (vista.py)
**Clase:** CalculatorVista
**Base:** QWidget
**Responsabilidades:**
- UI con QGridLayout (botones + display)
- Emisión de señales de usuario (button_clicked)
- Actualización visual desde modelo

### Controlador (controlador.py)
**Clase:** CalculatorControlador
**Base:** object
**Responsabilidades:**
- Lógica de negocio
- Coordinación Modelo-Vista
- Manejo de eventos

---

## 📝 Tareas de Implementación

### 1. Modelo (30 min)
- [x] `app/presentacion/paneles/calculator/modelo.py`
  - Clase CalculatorModelo como dataclass frozen
  - Atributos: current_value, pending_value, pending_operation
  - Métodos: add(), subtract(), multiply(), divide()
  - Validación de división por cero

### 2. Vista (45 min)
- [x] `app/presentacion/paneles/calculator/vista.py`
  - Clase CalculatorVista(QWidget)
  - QLineEdit para display (read-only)
  - QPushButton × 17 (0-9, +, -, *, /, =, ., C)
  - QGridLayout (5×4)
  - Señales: button_clicked(str)

### 3. Controlador (30 min)
- [x] `app/presentacion/paneles/calculator/controlador.py`
  - Clase CalculatorControlador
  - Conexión Vista → Modelo
  - handle_number_input()
  - handle_operation()
  - handle_equals()
  - handle_clear()

### 4. Entry Point (15 min)
- [x] `main.py`
  - QApplication
  - Instanciar MVC
  - Mostrar ventana

---

## 🧪 Estrategia de Testing

### Tests Unitarios (14 tests)
- **test_calculator_modelo.py** (8 tests)
  - test_add, test_subtract, test_multiply, test_divide
  - test_divide_by_zero
  - test_reset
  - test_execute_pending_operation

- **test_calculator_controlador.py** (6 tests)
  - test_handle_number_input
  - test_handle_operation
  - test_handle_equals
  - test_handle_clear

### Tests de Integración (4 tests)
- **test_calculator_integration.py**
  - test_full_addition_flow
  - test_division_by_zero_flow
  - test_clear_functionality
  - test_chained_operations

### BDD (6 escenarios)
- **test_calculator_steps.py**
  - Steps para los 6 escenarios de US-001.feature

---

## 📊 Quality Gates

| Gate | Umbral | Estrategia |
|------|--------|------------|
| Pylint | >= 8.0/10 | Docstrings completas, type hints |
| Coverage | >= 90% | Tests completos de M-V-C |
| Complejidad | < 12 | Métodos simples y claros |
| Mantenibilidad | >= 20 | Código limpio y documentado |

---

## 🎯 Criterios de Aceptación

- [x] Display muestra números
- [x] Botones 0-9 funcionan
- [x] Operaciones +, -, *, / funcionan
- [x] Botón = calcula resultado
- [x] Botón C limpia
- [x] División por cero maneja error

---

## 📅 Timeline

| Fase | Duración | Acumulado |
|------|----------|-----------|
| Modelo | 30 min | 30 min |
| Vista | 45 min | 1h 15min |
| Controlador | 30 min | 1h 45min |
| Entry Point | 15 min | 2h |
| Tests Unitarios | 20 min | 2h 20min |
| Tests Integración | 15 min | 2h 35min |
| BDD Steps | 15 min | 2h 50min |

**Total Estimado:** 2h 50min

---

**Generado por:** Claude Dev Kit v1.0
**Perfil:** pyqt-mvc
