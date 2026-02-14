# TICKET-035: Generalizar Template test-unit.py

**Fase:** 4 - Generalización de Templates
**Sprint:** 2
**Estado:** ✅ COMPLETADO
**Prioridad:** Alta
**Estimación:** 1 hora
**Asignado a:** Claude Code

---

## Descripción

Generalizar el template `test-unit.py` removiendo imports específicos de PyQt6 y la clase `TestSignals` completa (solo aplica a PyQt). Implementar sistema de snippets para imports y fixtures específicas del framework.

**Complejidad:** Alta - ~20% genérico, mucho contenido PyQt-specific.

---

## Criterios de Aceptación

- [ ] Template generalizado en `templates/testing/test-unit.py`
- [ ] Imports específicos removidos y convertidos a variable `{TEST_IMPORTS}`
- [ ] Clase `TestSignals` movida a snippet condicional
- [ ] Fixtures generalizadas con variable `{TEST_FIXTURES}`
- [ ] Decoradores async implementados con `{ASYNC_TEST_DECORATOR}`
- [ ] Template validado con 3+ perfiles

---

## Dependencias

**Depende de:**
- ✅ TICKET-030, TICKET-031

**Bloquea a:**
- TICKET-036

---

## Referencias Específicas a Remover

1. **Línea 16:** `from PyQt6.QtCore import QTimer`
2. **Líneas 73-94:** Clase `TestSignals` completa
3. **Líneas 77-78:** Fixtures `qapp`, `qtbot`

---

## Variables Nuevas

| Variable | Propósito | Valores por Perfil |
|----------|-----------|-------------------|
| `{TEST_IMPORTS}` | Imports del framework | PyQt6, FastAPI TestClient, Flask test_client |
| `{TEST_FIXTURES}` | Fixtures específicas | qapp/qtbot, async fixtures, flask app |
| `{ASYNC_TEST_DECORATOR}` | Decorador async | @pytest.mark.asyncio, "" |
| `{TEST_SIGNALS_CLASS}` | Clase TestSignals (condicional) | Solo PyQt |

---

## Estructura Generalizada

```python
"""
Tests unitarios para {COMPONENT_NAME}.
"""

import pytest
{TEST_IMPORTS}

from {MODULE_PATH} import {CLASS_NAME}


class TestCreacion:
    """Tests de creación e inicialización."""

    def test_crear_con_valores_default(self):
        """Verifica que se crea con valores por defecto correctos."""
        instancia = {CLASS_NAME}()
        assert instancia is not None


class TestMetodos:
    """Tests de métodos públicos."""

    @pytest.fixture
    def instancia({TEST_FIXTURES}):
        """Fixture que provee una instancia para tests."""
        return {CLASS_NAME}()

    {ASYNC_TEST_DECORATOR}
    def test_metodo_1(self, instancia):
        """Test de método."""
        resultado = instancia.metodo_1()
        assert resultado == valor_esperado


{TEST_SIGNALS_CLASS}
```

---

## Snippets por Perfil

### pyqt-mvc

```python
# TEST_IMPORTS
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QWidget

# TEST_FIXTURES
, qapp, qtbot

# TEST_SIGNALS_CLASS
class TestSignals:
    """Tests de señales PyQt."""
    # ... contenido completo
```

### fastapi-rest

```python
# TEST_IMPORTS
from fastapi.testclient import TestClient
from httpx import AsyncClient

# TEST_FIXTURES
# (vacío)

# ASYNC_TEST_DECORATOR
@pytest.mark.asyncio

# TEST_SIGNALS_CLASS
# (vacío)
```

### flask-rest / flask-webapp

```python
# TEST_IMPORTS
from flask import Flask
from flask.testing import FlaskClient

# TEST_FIXTURES
# (vacío o , flask_app)

# TEST_SIGNALS_CLASS
# (vacío)
```

---

## Checklist de Implementación

- [ ] Template copiado y generalizado
- [ ] Imports convertidos a `{TEST_IMPORTS}`
- [ ] Fixtures parametrizadas con `{TEST_FIXTURES}`
- [ ] Clase TestSignals movida a snippet condicional
- [ ] Decorador async implementado
- [ ] Snippets agregados a 5 perfiles
- [ ] Validación con tests reales
- [ ] Commit: `feat(templates): generalizar test-unit.py (TICKET-035)`

---

## Resultado

✅ **COMPLETADO** - 2026-02-14

**Template generalizado:**
- `templates/testing/test-unit.py` creado (~90 líneas)
- Imports específicos de PyQt6 removidos
- Clase TestSignals convertida a snippet condicional
- Fixtures generalizadas por framework

**Variables agregadas (5 perfiles):**
- `TEST_CLASS_ORGANIZATION_COMMENT`: Descripción de organización de tests

**Snippets agregados (5 perfiles × 4 snippets = 20 snippets):**

1. `test_imports`: Imports específicos del framework
   - pyqt-mvc: PyQt6.QtCore, dataclasses, Mock
   - fastapi-rest: httpx.AsyncClient, AsyncMock
   - flask-rest: flask.json, Mock
   - flask-webapp: flask.url_for, Mock
   - generic-python: Mock, dataclasses

2. `test_signals_class`: Clase TestSignals (solo PyQt)
   - pyqt-mvc: Clase completa (~20 líneas)
   - otros perfiles: "" (vacío)

3. `test_integration_class`: Clase TestIntegracion
   - pyqt-mvc: Tests con qapp
   - fastapi-rest: Tests async con AsyncClient
   - flask-rest: Tests con Flask test_client
   - flask-webapp: Tests con Flask + DB setup
   - generic-python: Tests de flujo simple

4. `test_fixtures`: Fixtures pytest
   - pyqt-mvc: mock_dependencia + qapp
   - fastapi-rest: AsyncMock + async test_client
   - flask-rest/flask-webapp: Mock + app_context
   - generic-python: Mock + datos_de_prueba

**Nivel de generalización:** 100% framework-agnostic, código Python ejecutable por stack
