# TICKET-023: Crear Perfil pyqt-mvc.json

**Estado:** ✅ Completado
**Fecha Inicio:** 2026-02-13
**Fecha Fin:** 2026-02-13
**Estimación:** 1.5 horas
**Tiempo Real:** ~35 minutos

---

## Objetivo

Crear el perfil de customización `pyqt-mvc.json` para proyectos PyQt6 con arquitectura MVC + Factory/Coordinator, extendiendo el `config.json` base con configuración específica para este stack tecnológico.

---

## Contexto

Este es el **primer perfil de customización** creado, basado en:
- Proyecto original ISSE_Simuladores (PyQt6 + MVC)
- Análisis TICKET-019 (47 referencias específicas identificadas)
- Skill generalizado TICKET-021 (variables parametrizadas)
- Config base TICKET-022 (foundation genérica)

El perfil permite que el skill `implement-us` funcione optimizado para proyectos PyQt6 siguiendo el patrón MVC con Factory y Coordinator.

---

## Implementación

### Archivo Creado

**Ubicación:** `skills/implement-us/customizations/pyqt-mvc.json`
**Tamaño:** ~350 líneas
**Formato:** JSON con comentarios descriptivos (prefijo `_comment_`)

### Estructura del Perfil

#### 1. Profile Metadata (líneas 3-15)

```json
{
  "profile_metadata": {
    "name": "pyqt-mvc",
    "display_name": "PyQt6 MVC + Factory/Coordinator",
    "description": "Configuración para aplicaciones desktop PyQt6 con patrón MVC...",
    "extends": "config.json",
    "version": "1.0.0",
    "target_stack": "PyQt6 + Python 3.10+",
    "architecture": "MVC (Model-View-Controller) + Factory + Coordinator patterns"
  }
}
```

**Características:**
- Identificación clara del perfil
- Referencia explícita a config.json base
- Stack tecnológico objetivo documentado
- Patrones arquitectónicos especificados

---

#### 2. Variables Override (líneas 19-93)

Override de las 8 variables del config base con valores específicos PyQt/MVC:

| Variable | Valor Base | Valor PyQt/MVC | Impacto |
|----------|------------|----------------|---------|
| `architecture_pattern` | `generic` | `mvc` | Fuerza arquitectura MVC estricta |
| `component_type` | `Component` | `Panel` | Componentes son Paneles UI |
| `component_path` | `src/{name}/` | `app/presentacion/paneles/{name}/` | Path específico PyQt |
| `test_framework` | `pytest` | `pytest + pytest-qt` | Testing de UI con qtbot |
| `base_class` | `object` | `ModeloBase` para modelos, `QWidget` para vistas | Clases base PyQt |
| `domain_context` | `application` | `presentacion` | Capa de presentación |
| `project_root` | `.` | `app/` | Raíz en directorio app/ |

**Detalles Adicionales:**

- **architecture_pattern:**
  - Define componentes MVC: `model`, `view`, `controller`, `factory`, `coordinator`
  - Disponible solo MVC (no otros patrones)

- **component_type:**
  - Tipos: `Panel`, `Dialog`, `Widget`, `Window`
  - Ejemplos: PanelDisplay, DialogConfiguración

- **test_framework:**
  - Plugins: pytest-qt, pytest-cov, pytest-bdd
  - Version constraints especificadas

- **base_class:**
  - Diferenciado por tipo de componente:
    - Modelo: `ModeloBase` (dataclass inmutable)
    - Vista: `QWidget`
    - Controlador: `object`
    - Coordinator: `QObject` (para signals/slots)

---

#### 3. Component Structure (líneas 97-156)

**Estructura MVC Panel Completa:**

```json
"mvc_panel": {
  "base_path": "app/presentacion/paneles/{component_name}/",
  "files": {
    "model": {
      "filename": "modelo.py",
      "class_name": "{ComponentName}Modelo",
      "base_class": "ModeloBase",
      "pattern": "dataclass inmutable",
      "responsibilities": [
        "Estado del panel (datos)",
        "Validación de datos",
        "Inmutabilidad (sin setters)"
      ]
    },
    "view": { /* ... */ },
    "controller": { /* ... */ },
    "init": { /* ... */ }
  }
}
```

**3 archivos por panel:**
1. **modelo.py:** Dataclass inmutable con estado
2. **vista.py:** QWidget con UI y signals
3. **controlador.py:** Lógica de negocio y coordinación

**Archivos de tests:**
- `test_{component_name}_modelo.py`
- `test_{component_name}_vista.py`
- `test_{component_name}_controlador.py`
- `test_{component_name}_integration.py`

**Factory Pattern:**
- Enabled: true
- Método: `crear_{component_name}(parent, config) -> tuple[Modelo, Vista, Controlador]`
- Ubicación: `app/presentacion/factory.py`

**Coordinator:**
- Base class: `QObject`
- Pattern: Signals/Slots para pub-sub entre paneles
- Ubicación: `app/presentacion/coordinadores/`

---

#### 4. Test Framework Config (líneas 160-216)

**Fixtures Requeridos:**

```json
"required_fixtures": {
  "qapp": {
    "description": "Aplicación QApplication para tests",
    "scope": "session"
  },
  "qtbot": {
    "description": "Helper para interacción con widgets (clicks, inputs, etc.)",
    "scope": "function"
  }
}
```

**Markers Específicos:**
- `unit`: Tests unitarios M/V/C
- `integration`: Tests entre componentes MVC
- `ui`: Tests de interfaz gráfica (requieren qtbot)
- `bdd`: Tests BDD
- `slow`: Tests lentos (>1s, UI)
- `no_display`: Tests sin display gráfico

**Coverage Config:**
- Source: `app/presentacion`
- Omit: tests, factory, __init__.py
- Exclude lines: pragma no cover, TYPE_CHECKING, NotImplementedError

**Pytest Options:**
```
-v --tb=short --strict-markers
--cov=app/presentacion
--cov-report=term-missing
--cov-report=html
```

---

#### 5. Quality Gates (líneas 220-257)

**Ajustes específicos para PyQt:**

| Métrica | Base | PyQt/MVC | Justificación |
|---------|------|----------|---------------|
| Pylint | ≥8.0 | ≥8.0 | Sin cambio, pero disable algunos checks |
| CC | ≤10 | ≤12 | UI event handlers pueden tener lógica condicional |
| MI | ≥20 | ≥20 | Sin cambio |
| Coverage | ≥95% | ≥90% | UI tiene código difícil de testear 100% |

**Pylint - Checks Deshabilitados:**
- `too-many-instance-attributes` (UI naturalmente tiene muchos widgets)
- `too-many-public-methods` (QWidget tiene muchos métodos)
- `too-few-public-methods` (Models pueden ser simples dataclasses)

**CC - Exclusiones:**
- `**/vista.py` excluida (UI tiene complejidad inherente)

**Notas:**
- Los quality gates reconocen que UI tiene complejidad legítima
- Coverage de 90% es realista para PyQt (vs 95% genérico)

---

#### 6. BDD Config (líneas 261-274)

**Step Patterns Específicos PyQt:**

```json
"step_patterns": {
  "given_ui": "Dado que la aplicación PyQt está iniciada",
  "when_click": "Cuando el usuario hace click en {widget}",
  "then_display": "Entonces se muestra {value} en {widget}"
}
```

Templates específicos:
- `templates/bdd/pyqt-scenario.feature`
- `templates/bdd/pyqt-steps.py`

---

#### 7. Dependencies (líneas 278-293)

**Required:**
- PyQt6 ≥6.4.0
- pytest ≥7.0.0
- pytest-qt ≥4.2.0
- pytest-cov ≥4.0.0
- pytest-bdd ≥6.0.0

**Development:**
- pylint ≥2.15.0
- radon ≥5.1.0
- black ≥22.0.0
- mypy ≥1.0.0

**Optional:**
- pyqt6-tools
- qt-material

---

#### 8. Design Patterns (líneas 297-328)

**Patrones Documentados:**

1. **MVC:**
   - Modelo: dataclass inmutable, solo datos y validación
   - Vista: QWidget, solo UI y signals
   - Controlador: lógica de negocio, coordina M-V

2. **Factory:**
   - Creación centralizada de paneles MVC
   - Método: `crear_{panel_name}(parent, config) -> tuple`

3. **Coordinator:**
   - Comunicación pub-sub entre paneles
   - PyQt signals para eventos cross-panel

4. **Immutability:**
   - Modelos inmutables con `@dataclass(frozen=True)`

---

#### 9. Project Conventions (líneas 344-370)

**Naming Conventions:**
- Model suffix: `Modelo`
- View suffix: `Vista`
- Controller suffix: `Controlador`
- Test prefix: `test_`
- Panel prefix: `Panel`

**Import Style:**
```python
from PyQt6.QtWidgets import QWidget, QPushButton
from app.presentacion.paneles.{name} import {Name}Modelo
```

**Signals Convention:**
```python
dato_actualizado_signal = pyqtSignal(int)
```

---

## Decisiones de Diseño

### 1. Quality Gates Más Flexibles para UI

**Decisión:** Reducir coverage de 95% → 90% y aumentar CC de 10 → 12.

**Justificación:**
- UI tiene código inherentemente difícil de testear al 100%
- Event handlers pueden tener lógica condicional legítima
- Deshabilitar ciertos checks de Pylint para widgets (muchos atributos es normal)

**Alternativa rechazada:** Mantener umbrales estrictos del base config.

**Impacto:** Quality gates más realistas sin sacrificar calidad general.

---

### 2. Factory Pattern Obligatorio

**Decisión:** Incluir factory pattern en component_structure con `enabled: true`.

**Justificación:**
- Centraliza creación de tríada MVC (Modelo, Vista, Controlador)
- Facilita inyección de dependencias
- Patrón usado exitosamente en proyecto original

**Alternativa rechazada:** Permitir creación ad-hoc de componentes.

**Impacto:** Código más mantenible y testeable.

---

### 3. Coordinator como QObject

**Decisión:** Base class `QObject` para coordinadores.

**Justificación:**
- Permite uso de signals/slots de PyQt
- Comunicación asíncrona entre paneles
- Desacoplamiento de componentes

**Alternativa rechazada:** Coordinador como simple clase Python con callbacks.

**Impacto:** Mejor integración con Qt event loop.

---

### 4. Estructura de 3 Archivos por Panel

**Decisión:** Separar modelo.py, vista.py, controlador.py en archivos distintos.

**Justificación:**
- Separación clara de responsabilidades
- Facilita testing unitario
- Evita archivos gigantes

**Alternativa rechazada:** Todos los componentes en un solo archivo.

**Impacto:** Mejor organización, más archivos por panel.

---

## Validación

### Tests Realizados

1. **Validación sintáctica JSON:**
   ```bash
   python3 -m json.tool customizations/pyqt-mvc.json > /dev/null
   # ✅ JSON válido
   ```

2. **Verificación de estructura:**
   - ✅ Profile metadata completa
   - ✅ 8 variables override
   - ✅ Component structure MVC completa
   - ✅ Test framework con pytest-qt
   - ✅ Quality gates ajustados
   - ✅ Design patterns documentados

3. **Comparación con proyecto original:**
   - ✅ Arquitectura MVC coincide
   - ✅ Paths coinciden (app/presentacion/paneles/)
   - ✅ Testing strategy coincide (pytest-qt, qtbot)
   - ✅ Patterns coinciden (Factory, Coordinator)

---

## Comparación Base vs PyQt/MVC

| Aspecto | Config Base (Generic) | PyQt/MVC Profile |
|---------|----------------------|------------------|
| **Architecture** | `generic` | `mvc` (estricto) |
| **Component Type** | `Component` | `Panel`, `Dialog`, `Widget` |
| **Component Path** | `src/{name}/` | `app/presentacion/paneles/{name}/` |
| **Test Framework** | `pytest` | `pytest + pytest-qt` |
| **Fixtures** | Ninguno | `qapp`, `qtbot` |
| **Base Classes** | `object` | `ModeloBase`, `QWidget`, `QObject` |
| **Files per Component** | 2 (main.py, test.py) | 4 (modelo.py, vista.py, controlador.py, __init__.py) |
| **Coverage Min** | 95% | 90% |
| **CC Max** | 10 | 12 |
| **Patterns** | Genéricos | MVC, Factory, Coordinator, Immutability |

---

## Próximos Pasos

Este perfil permite:
1. Instalar el skill en proyectos PyQt6 con configuración optimizada
2. Generar código siguiendo arquitectura MVC estricta
3. Tests con pytest-qt automáticamente configurado
4. Quality gates ajustados para UI

### Siguiente Ticket: TICKET-024

Crear perfil `fastapi-rest.json` para APIs REST con arquitectura en capas.

---

## Notas de Implementación

### Cómo Usar Este Perfil

1. **Durante instalación:**
   ```bash
   python installer.py --profile pyqt-mvc
   ```

2. **Merge con config base:**
   ```python
   config_final = merge(config_base, pyqt_mvc_profile)
   ```

3. **Variables resueltas:**
   - `{ARCHITECTURE_PATTERN}` → "mvc"
   - `{COMPONENT_TYPE}` → "Panel"
   - `{COMPONENT_PATH}` → "app/presentacion/paneles/{name}/"
   - etc.

### Extensibilidad

Este perfil puede ser extendido para:
- **Variantes de PyQt:** PyQt5, PySide6
- **Otras arquitecturas UI:** MVVM, MVP
- **Frameworks específicos:** qt-material, pyqtgraph

Crear perfil derivado:
```json
{
  "profile_metadata": {
    "extends": "pyqt-mvc.json"
  },
  "variables": {
    "component_path": {
      "default": "src/gui/panels/{name}/"
    }
  }
}
```

---

## Métricas

- **Tiempo estimado:** 1.5 horas
- **Tiempo real:** ~35 minutos ⚡ (61% más rápido)
- **Líneas de código:** ~350 líneas
- **Secciones implementadas:** 10
- **Variables override:** 8
- **Patterns documentados:** 4 (MVC, Factory, Coordinator, Immutability)
- **Dependencies definidas:** 15 paquetes

---

## Referencias

- **Config Base:** `skills/implement-us/config.json`
- **Sprint 2 Plan:** `gestion/fase-3-generalizacion-skills/sprint-2.md` (líneas 146-178)
- **Análisis TICKET-019:** `docs/analysis/TICKET-019-analysis.md`
- **Proyecto Original:** ISSE_Simuladores (arquitectura de referencia)

---

**Ticket completado exitosamente.** ✅

El perfil `pyqt-mvc.json` está listo para ser usado en proyectos PyQt6 con arquitectura MVC.
