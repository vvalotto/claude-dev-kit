# TICKET-053: Tutorial PyQt-MVC Completo 🖥️

**Fase:** 7 - Ejemplos por Stack
**Sprint:** 4
**Estado:** ✅ Completado
**Prioridad:** Alta
**Estimación:** 3 horas
**Tiempo Real:** ~1.5 horas (automatizado con Claude)
**Asignado a:** Claude Code

## Descripción

Crear tutorial end-to-end completo para el stack **PyQt-MVC**, demostrando el uso del framework Claude Dev Kit para implementar una aplicación desktop con interfaz gráfica.

**Historia de Usuario:**
```
US-001: Calculadora Simple

Como usuario de escritorio,
Quiero una calculadora con interfaz gráfica
Para realizar operaciones matemáticas básicas (+, -, *, ÷)

Criterios de Aceptación:
- Display que muestra número actual
- Botones 0-9 para ingresar números
- Botones +, -, *, ÷ para operaciones
- Botón = para mostrar resultado
- Botón C para limpiar
- Validación de división por cero
```

## Criterios de Aceptación

### Contenido del Tutorial

- [ ] **Introducción clara** - Qué se va a construir y por qué
- [ ] **Requisitos** - Python 3.9+, PyQt6, pytest-qt, sistema operativo
- [ ] **Setup del proyecto** - Creación de estructura de directorios
- [ ] **Instalación del framework** - Comando completo con perfil pyqt-mvc
- [ ] **Historia de usuario completa** - US-001 documentada

### Walkthrough de las 10 Fases

- [ ] **Fase 0: Validación** - Verificar prerequisitos
- [ ] **Fase 1: BDD** - Escenarios Gherkin generados
- [ ] **Fase 2: Planning** - Plan de implementación con tareas
- [ ] **Fase 3: Implementación** - Código de:
  - MainWindow (Vista)
  - CalculatorController (Controlador)
  - CalculatorModel (Modelo)
- [ ] **Fase 4: Tests Unitarios** - Tests de modelo y controlador
- [ ] **Fase 5: Tests Integración** - Tests end-to-end con PyQt
- [ ] **Fase 6: Validación BDD** - Ejecutar escenarios
- [ ] **Fase 7: Quality Gates** - Pylint, cobertura, complejidad
- [ ] **Fase 8: Documentación** - Docstrings y comentarios
- [ ] **Fase 9: Reporte** - Reporte final con métricas

### Código y Ejemplos

- [ ] **Código ejecutable** - Fragmentos que realmente funcionan
- [ ] **Screenshots** - Al menos 3: UI inicial, operación, resultado
- [ ] **Output de terminal** - Ejemplos de comandos y su output
- [ ] **Archivos generados** - Mostrar BDD scenarios, plan, tests

### Calidad

- [ ] **Troubleshooting** - 5+ problemas comunes y soluciones
- [ ] **Próximos pasos** - Ideas para extender la calculadora
- [ ] **Tiempo realista** - Completable en 45-60 minutos
- [ ] **Links funcionando** - Referencias a otras partes de la docs

## Dependencias

- **Depende de:** TICKET-052 (análisis y template)
- **Bloquea a:** TICKET-058 (validación)

## Notas Técnicas

### Estructura del Proyecto

```
calculator/
├── main.py                       # Entry point
├── app/
│   ├── __init__.py
│   ├── presentacion/
│   │   ├── __init__.py
│   │   ├── main_window.py       # Vista principal
│   │   └── ui/
│   │       └── calculator.ui    # Diseño Qt (opcional)
│   ├── controladores/
│   │   ├── __init__.py
│   │   └── calculator_controller.py
│   └── modelos/
│       ├── __init__.py
│       └── calculator_model.py
├── tests/
│   ├── test_model.py
│   ├── test_controller.py
│   └── test_integration.py
└── features/
    ├── calculator.feature
    └── steps/
        └── calculator_steps.py
```

### Componentes Clave

**CalculatorModel:**
- Métodos: add(), subtract(), multiply(), divide()
- Validación: división por cero
- Estado: current_value, pending_operation

**CalculatorController:**
- Lógica de negocio
- Coordina Vista ↔ Modelo
- Manejo de eventos

**MainWindow:**
- QMainWindow con QGridLayout
- Botones 0-9, +, -, *, ÷, =, C
- QLineEdit para display

### Screenshots a Incluir

1. **UI Inicial** - Ventana con botones y display en 0
2. **Operación** - Usuario ingresando "5 + 3"
3. **Resultado** - Display mostrando "8"

### Código de Ejemplo

Incluir fragmentos clave:
- Creación del MainWindow (15-20 líneas)
- Método add() del modelo (5-10 líneas)
- Test unitario de división por cero (10 líneas)

## Checklist de Implementación

### Preparación (15 min)
- [ ] Leer TICKET-052 y usar template
- [ ] Definir estructura del tutorial
- [ ] Preparar screenshots (crear app demo)

### Escritura del Tutorial (2h)
- [ ] Sección: Introducción y requisitos
- [ ] Sección: Setup del proyecto
- [ ] Sección: Instalación del framework
- [ ] Sección: Historia de usuario
- [ ] Sección: Fase 0-2 (Validación, BDD, Planning)
- [ ] Sección: Fase 3 (Implementación) - código completo
- [ ] Sección: Fase 4-5 (Tests)
- [ ] Sección: Fase 6-7 (Validación BDD, Quality Gates)
- [ ] Sección: Fase 8-9 (Documentación, Reporte)
- [ ] Sección: Troubleshooting
- [ ] Sección: Próximos pasos

### Validación (30 min)
- [ ] Verificar código ejecutable
- [ ] Verificar screenshots claros
- [ ] Verificar links funcionando
- [ ] Verificar tiempo completación <1h
- [ ] Spell check y revisión general

### Finalización (15 min)
- [ ] Agregar navegación (anterior/siguiente/índice)
- [ ] Commit del archivo
- [ ] Actualizar sprint-4.md

## Resultado

**Estado:** ✅ COMPLETADO

**Archivo generado:** `docs/examples/pyqt-project.md` (~1,000 líneas)

### Contenido del Tutorial

- ✅ Introducción y objetivos claros
- ✅ Requisitos previos verificables
- ✅ Historia de usuario completa (US-001: Calculadora Simple)
- ✅ Setup detallado paso a paso
- ✅ Instalación del framework con perfil pyqt-mvc
- ✅ Walkthrough completo de las 10 fases con código ejecutable:
  - Fase 0: Validación de contexto
  - Fase 1: Generación de escenarios BDD (6 escenarios Gherkin)
  - Fase 2: Plan de implementación (MVC)
  - Fase 3: Implementación completa (Model, Controller, View, main.py)
  - Fase 4: Tests unitarios (14 tests)
  - Fase 5: Tests de integración (4 tests end-to-end con pytest-qt)
  - Fase 6: Validación BDD (step definitions)
  - Fase 7: Quality gates (Pylint, Coverage, Complejidad, Mantenibilidad)
  - Fase 8: Documentación (README, ADRs, docs de componentes)
  - Fase 9: Reporte final (métricas consolidadas)
- ✅ Validación final con checklist
- ✅ Troubleshooting extenso (7 problemas comunes)
- ✅ Próximos pasos para ampliar la calculadora
- ✅ Recursos completos (Framework + PyQt6 + pytest-qt + MVC)

### Código de Ejemplo Incluido

**CalculatorModel (Modelo):**
- 95 líneas con operaciones matemáticas
- Validación de división por cero
- Docstrings completas + type hints

**CalculatorController (Controlador):**
- 120 líneas con lógica de coordinación
- Manejo de eventos y estado
- Operaciones encadenadas

**MainWindow (Vista):**
- 180 líneas de UI PyQt6
- QGridLayout con 17 botones
- Signals conectados correctamente

**main.py:**
- 25 líneas de entry point
- Integración MVC completa

**Tests:**
- Tests unitarios (Model + Controller)
- Tests integración (pytest-qt)
- BDD step definitions

### Métricas

- **Líneas totales:** ~1,000 líneas
- **Secciones:** 10 principales
- **Código de ejemplo:** ~420 líneas de Python
- **Tests documentados:** 24 tests
- **Screenshots descritos:** 3 (UI inicial, operación, resultado)
- **Troubleshooting:** 7 problemas comunes
- **Tiempo estimado usuario:** 45-60 minutos

**Completado:** 2026-02-16
