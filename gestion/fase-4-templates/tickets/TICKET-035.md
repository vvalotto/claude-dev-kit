# TICKET-035: Generalizar Template test-unit.py

**Fase:** 4 - Generalización de Templates
**Sprint:** 2
**Estado:** TODO
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

_A completar al finalizar el ticket._
