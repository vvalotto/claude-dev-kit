# Fase 6: Validación BDD

Cierra el ciclo iniciado en Fase 1: implementa los step definitions de los escenarios Gherkin y valida que el sistema cumple con el comportamiento especificado. Esta fase se **omite** si `skip_bdd: true` en `context.md`.

**Aprobación requerida:** No (el skill avanza automáticamente cuando todos los escenarios pasan).

---

## Para el usuario

### Qué hace esta fase

1. Verifica que el feature file de Fase 1 existe en disco
2. Consulta el `steps_template` del perfil activo como referencia estructural
3. Genera los step definitions en `tests/step_defs/test_{feature}_steps.py`
4. Ejecuta `pytest tests/step_defs/ -v` y verifica que **todos** los escenarios pasan (100%)
5. Si algún escenario falla, diagnostica el origen y aplica la corrección correspondiente

### Qué esperar

El criterio de éxito es 100% de escenarios en verde. Ningún escenario puede estar en estado `FAILED` o `SKIP`.

Si un escenario falla, el skill identifica el origen:
- **Bug en la implementación** → vuelve a Fase 3 a corregir el código
- **Step definition mal implementado** → corrige el step en esta fase
- **Escenario mal redactado** → edita el `.feature` y te muestra el cambio para aprobación (si implica revisar la lógica de la HU, vuelve a Fase 1)

### Artefactos que produce

`tests/step_defs/test_{feature}_steps.py` — implementación de los steps Given/When/Then que ejecutan los escenarios del feature file.

### Estructura de archivos BDD

```
tests/
├── features/                       # Archivos .feature (generados en Fase 1)
│   └── {US_ID}-{nombre}.feature
├── step_defs/                      # Implementación de steps (generados en Fase 6)
│   └── test_{feature}_steps.py
└── conftest.py                     # Fixtures compartidos
```

> pytest-bdd descubre los escenarios a través de los archivos de step_defs (que importan `scenarios(...)`). Los features residen en `tests/features/` y los steps en `tests/step_defs/`. **No** se ejecutan los `.feature` directamente.

### Ejemplo de output esperado

```
tests/step_defs/test_calculadora_steps.py::Sumar dos números positivos PASSED
tests/step_defs/test_calculadora_steps.py::División por cero retorna error PASSED

2 scenarios passed, 0 failed, 0 skipped
```

---

## Referencia técnica

### Entradas

| Entrada | Tipo | Requerida | Fuente |
|---|---|---|---|
| `tests/features/{US_ID}-*.feature` | Artefacto | ✅ Sí | Fase 1 |
| Archivos de código de producción | Artefactos | ✅ Sí | Fase 3 |
| Tests unitarios e integración pasando | Resultado ejecutable | ✅ Sí | Fases 4-5 |
| `steps_template` del perfil | `customizations/{perfil}.json` → `bdd_config.steps_template` | ❌ Opcional | Perfil activo |

### Salidas

| Salida | Tipo | Descripción |
|---|---|---|
| `tests/step_defs/test_{feature}_steps.py` | Artefacto físico | Steps implementados por escenario |
| Resultado de `pytest tests/step_defs/ -v` | En conversación | 100% de escenarios pasando |

### Templates

Ninguno externo obligatorio. Si el perfil define `bdd_config.steps_template`, se usa como referencia estructural (patrón de imports, decoradores `@given/@when/@then`, fixtures del stack).

Si no hay template, se usa el patrón estándar de pytest-bdd.

### Artefactos

| Artefacto | Operación | Ruta |
|---|---|---|
| `{US_ID}-*.feature` | **Lee** | `tests/features/` |
| `test_{feature}_steps.py` | **Genera** | `tests/step_defs/` |
| `tests/conftest.py` | **Actualiza** (fixtures BDD) | `tests/conftest.py` |

### Convenciones

- Feature files en `tests/features/`, steps en `tests/step_defs/`.
- Ejecución: `pytest tests/step_defs/ -v` (no `pytest tests/features/`).
- La ruta `tests/step_defs/` es la canónica del skill (reemplazó `tests/features/steps/` de versiones anteriores).
- La edición de un `.feature` requiere aprobación explícita del usuario; si implica cambio de lógica de la HU, volver a Fase 1.
- El protocolo de recuperación usa "ciclos completos", no "intentos".

### Patrón de steps (pytest-bdd)

```python
# tests/step_defs/test_{feature}_steps.py
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
# Imports del sistema según stack

scenarios('../features/{US_ID}-{nombre}.feature')

@pytest.fixture
def context():
    """Contexto compartido entre steps."""
    return {}

@given("estado inicial del sistema")
def estado_inicial(context):
    """Setup del contexto inicial."""
    pass

@when(parsers.parse('acción del usuario con parámetro "{param}"'))
def accion_usuario(context, param):
    """Ejecutar acción."""
    pass

@then(parsers.parse('el resultado es {valor:d}'))
def validar_resultado(context, valor):
    """Validar resultado."""
    pass
```

### Protocolo de recuperación

**Síntoma:** Uno o más escenarios en estado FAILED o SKIP.

1. Leer el output completo del error del escenario fallido
2. Determinar el origen:
   - **La implementación no cumple el escenario** → volver a Fase 3
   - **El step está mal implementado** → corregir el step en esta fase
   - **El escenario está mal redactado** → editar `.feature`, mostrar al usuario, re-ejecutar; si afecta lógica de HU → volver a Fase 1
3. Re-ejecutar: `pytest tests/step_defs/ -v`
4. No avanzar hasta que **todos** los escenarios estén en verde
5. Después de 2 ciclos sin resolución → informar al usuario

### Dependencias

| Dirección | Fase | Qué provee |
|---|---|---|
| ← anterior | Fase 1 | Feature file con escenarios aprobados |
| ← anterior | Fases 4-5 | Tests pasando (implica implementación correcta) |
| → siguiente | Fase 7 | Evidencia de comportamiento validado |

### Checklist de salida

- [ ] Todos los escenarios BDD pasan: `pytest tests/step_defs/ -v`
- [ ] Ningún escenario en estado SKIP o FAILED
- [ ] Tracking de Fase 6 cerrado

### Estado en v1.3

| ID | Descripción | Resolución |
|---|---|---|
| D6-1 | `config.json` → `test_framework_config.steps_path` era `"tests/features/steps/"` pero la fase usa `"tests/step_defs/"` | Corregido en `config.json`: `steps_path: "tests/step_defs/"` |
| D6-2 | Los perfiles definen `bdd_config.steps_template` pero la fase no incluía instrucción de leerlo | Se agregó: si el perfil define `steps_template`, leerlo como referencia estructural antes de implementar los steps |

---

**Fase anterior:** [Fase 5: Tests de Integración](phase-5.md)
**Siguiente fase:** [Fase 7: Quality Gates](phase-7.md)
