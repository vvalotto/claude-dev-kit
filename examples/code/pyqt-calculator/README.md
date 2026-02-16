# Calculadora PyQt6 MVC - Ejemplo Real del Claude Dev Kit

✅ **Este proyecto fue generado usando el Claude Dev Kit framework**

## 🎯 Descripción

Calculadora simple implementada siguiendo el patrón MVC con PyQt6, generada completamente usando el perfil `pyqt-mvc` del Claude Dev Kit.

**Historia de Usuario:** US-001 - Calculadora Simple

## 📊 Métricas de Generación

- **Tiempo total:** ~81 minutos
- **Código generado:** 4 archivos (~500 líneas)
- **Tests generados:** 2 archivos (~150 líneas)
- **Documentación:** 3 archivos

## 🏗️ Arquitectura

Siguiendo el perfil `pyqt-mvc`:

```
app/presentacion/paneles/calculator/
├── modelo.py          # CalculatorModelo (dataclass frozen)
├── vista.py           # CalculatorVista (QWidget)
└── controlador.py     # CalculatorControlador
```

**Patrón MVC:**
- **Modelo:** Inmutable (dataclass frozen=True), solo datos y lógica matemática
- **Vista:** QWidget con señales PyQt, solo UI
- **Controlador:** Coordina M-V, lógica de negocio

## 🚀 Instalación y Ejecución

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar calculadora
python main.py
```

## 🧪 Tests

```bash
# Todos los tests
pytest tests/ -v

# Con cobertura
pytest tests/ --cov=app --cov-report=term-missing

# Solo unitarios
pytest tests/unit/ -v
```

## 📋 Archivos Generados por el Framework

### Fase 1 - BDD
- ✅ `tests/bdd/US-001.feature` (6 escenarios Gherkin)

### Fase 2 - Planning
- ✅ `docs/planning/US-001-plan.md`

### Fase 3 - Implementación
- ✅ `app/presentacion/paneles/calculator/modelo.py`
- ✅ `app/presentacion/paneles/calculator/vista.py`
- ✅ `app/presentacion/paneles/calculator/controlador.py`
- ✅ `main.py`

### Fase 4 - Tests Unitarios
- ✅ `tests/unit/test_calculator_modelo.py`
- ✅ `tests/unit/test_calculator_controlador.py`

### Configuración
- ✅ `requirements.txt`
- ✅ Estructura MVC según perfil pyqt-mvc

## 🎓 Aprendizajes del Framework

1. **Estructura consistente:** Todos los proyectos PyQt siguen la misma organización
2. **Modelos inmutables:** dataclass frozen=True fuerza buenas prácticas
3. **Separación MVC estricta:** Responsabilidades claras
4. **Tests desde el inicio:** No como afterthought
5. **Documentación automática:** Plan y reportes generados

## 🔗 Claude Dev Kit

Este proyecto demuestra el uso real del framework:
- Perfil usado: `pyqt-mvc`
- Templates aplicados: BDD, planning
- Quality gates: Pylint >= 8.0, Coverage >= 90%

**Repositorio:** https://github.com/vvalotto/claude-dev-kit

---

**Generado con:** Claude Dev Kit v1.0
**Fecha:** 2026-02-16
**Tiempo total:** ~81 minutos
