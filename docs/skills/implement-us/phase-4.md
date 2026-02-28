# Fase 4: Tests Unitarios

Crea tests unitarios para cada componente implementado en Fase 3. Los tests verifican el comportamiento de cada unidad de forma aislada, usando mocks para las dependencias externas.

**Aprobación requerida:** No (el skill avanza automáticamente cuando todos los tests pasan).

---

## Para el usuario

### Qué hace esta fase

1. Lee el plan desde `docs/plans/{US_ID}-plan.md` para identificar los componentes a testear
2. Genera archivos de test en `tests/unit/` para cada componente
3. Ejecuta `pytest tests/unit/ -v` y verifica que todos los tests pasen
4. Verifica que la cobertura alcanza el umbral del perfil activo

### Qué esperar

El skill genera una suite de tests completa por componente. Si algún test falla, aplica el protocolo de recuperación antes de avanzar.

La cobertura objetivo varía según el perfil activo:
- PyQt MVC: 90% (UI es más difícil de testear)
- Flask Webapp: 90% (solo Python backend, no JavaScript)
- FastAPI REST, Flask REST, Generic: 95%

### Artefactos que produce

Archivos en `tests/unit/test_{component_name}.py` por cada componente del plan.

### Estrategia de tests por stack

**PyQt/MVC:** Tests de modelo (validación, inmutabilidad), vista (construcción de widgets, señales), controlador (mediación, eventos).

**FastAPI/Layered:** Tests de schemas (Pydantic validation), services (lógica con mocks de repositorio), repositories (CRUD con test DB).

**Flask REST/Layered:** Tests de domain models (to_dict, validar), repositories in-memory (CRUD, integridad de IDs), endpoints (request/response, status codes).

**Flask Webapp:** Tests de routes (template rendering con mocks de APIClient), API client (get/post con requests_mock), error handlers.

**Generic Python:** Tests de clases y funciones públicas, casos edge, excepciones.

---

## Referencia técnica

### Entradas

| Entrada | Tipo | Requerida | Fuente |
|---|---|---|---|
| Archivos de código de producción | Artefactos | ✅ Sí | Fase 3 |
| `docs/plans/{US_ID}-plan.md` | Artefacto | ✅ Sí | Fase 2 |
| Framework de testing del perfil | `config.json` → `test_framework_config` | ✅ Sí | Perfil activo |
| Umbral de cobertura | `config.json` → `quality_gates.coverage.min_percent` | ✅ Sí | Perfil activo |

### Salidas

| Salida | Tipo | Descripción |
|---|---|---|
| `tests/unit/test_{component}.py` | Artefactos físicos | Tests por componente según perfil |
| Resultado de `pytest tests/unit/ -v` | En conversación | Todos los tests deben pasar |
| Cobertura verificada | En conversación | ≥ umbral del perfil activo |

### Templates

| Template | Ruta en `config.json` |
|---|---|
| Test unitario genérico | `templates/testing/test-unit.py` |

Los perfiles definen `template_variables.TEST_FILE_PATTERN` con el patrón de nombres de archivos de test por stack.

### Artefactos

| Artefacto | Operación | Ruta |
|---|---|---|
| `test_{component}_*.py` | **Genera** | `tests/unit/` |
| `tests/conftest.py` | **Crea/actualiza** (fixtures compartidos) | `tests/conftest.py` |
| Código de producción | **Lee** | `{COMPONENT_PATH}/` |

### Estructura de tests recomendada

```python
"""Tests unitarios para {COMPONENT_NAME}."""
import pytest

class Test{Component}Creation:
    """Tests de creación e inicialización."""

    def test_crear_con_valores_default(self):
        pass

    def test_crear_con_valores_custom(self):
        pass

class Test{Component}Validation:
    """Tests de validación de datos."""

    def test_campo_requerido_falla_si_vacio(self):
        pass

class Test{Component}Behavior:
    """Tests de comportamiento y métodos."""

    def test_metodo_principal(self):
        pass
```

### Frameworks de testing por perfil

| Perfil | Dependencias | Fixtures clave |
|---|---|---|
| PyQt/MVC | `pytest`, `pytest-qt`, `pytest-cov` | `qapp`, `qtbot` |
| FastAPI/Layered | `pytest`, `pytest-asyncio`, `httpx`, `pytest-cov` | `client`, `test_db`, `async_client` |
| Flask REST/Webapp | `pytest`, `pytest-flask`, `pytest-cov` | `app` (scope=module), `client`, `context` |
| Generic Python | `pytest`, `pytest-cov` | `tmp_path`, `monkeypatch`, `capsys` |

### Convenciones

- Tests en `tests/unit/` (no en la raíz de `tests/`).
- Ejecución: `pytest tests/unit/ -v`.
- La ruta de tests unitarios se lee de `config.json` → `test_framework_config.unit_test_path` (por defecto `tests/unit/`).
- El umbral de cobertura se lee del perfil activo, no se hardcodea.

### Protocolo de recuperación

**Síntoma:** Uno o más tests fallan (`FAILED` en pytest).

1. Leer el output completo sin asumir la causa
2. Determinar si el error está en el test o en la implementación:
   - **Error en implementación** → volver a Fase 3, corregir, regresar a Fase 4
   - **Error en el test** (fixture incorrecto, mal escrito) → corregir el test en esta fase
3. Re-ejecutar: `pytest tests/unit/ -v`
4. No avanzar hasta que **todos** los tests pasen
5. Después de 2 intentos sin resolución → informar al usuario

### Dependencias

| Dirección | Fase | Qué provee |
|---|---|---|
| ← anterior | Fase 3 | Código de producción |
| → siguiente | Fase 5 | Suite de tests unitarios pasando (precondición) |
| → siguiente | Fase 7 | Tests para medir coverage |

### Checklist de salida

- [ ] Todos los tests unitarios pasan: `pytest tests/unit/ -v`
- [ ] Cobertura ≥ umbral del perfil activo
- [ ] Tracking de Fase 4 cerrado

### Estado en v1.3

| ID | Descripción | Resolución |
|---|---|---|
| D4-1 | Las rutas de archivos de test eran inconsistentes entre perfiles (algunos usaban raíz `tests/`, otros subdirectorios) | Se estableció `tests/unit/` como ruta canónica y se instruyó leer `unit_test_path` del config |
| D4-2 | `config.json` base tenía `test_path: "tests/"` sin subdirectorio unit, pero la fase ejecutaba `pytest tests/unit/` | Se alineó config y fase a `unit_test_path: "tests/unit/"` |

---

**Fase anterior:** [Fase 3: Implementación](phase-3.md)
**Siguiente fase:** [Fase 5: Tests de Integración](phase-5.md)
