# Fase 5: Tests de Integración

Crea tests que validan que múltiples componentes funcionan correctamente juntos, probando flujos end-to-end del sistema en condiciones realistas.

**Aprobación requerida:** No (el skill avanza automáticamente cuando todos los tests pasan).

---

## Para el usuario

### Qué hace esta fase

1. Verifica que los tests unitarios de Fase 4 pasan (precondición ejecutable)
2. Identifica los flujos de integración críticos basándose en los escenarios BDD de Fase 1
3. Genera tests en `tests/integration/` que validan la interacción entre componentes
4. Ejecuta `pytest tests/integration/ -v` y verifica que todos los tests pasan

### Qué esperar

A diferencia de los tests unitarios, los de integración usan dependencias reales o test-doubles (no mocks puros), y verifican flujos completos: desde la entrada del usuario hasta la persistencia de datos.

**Diferencia clave con Fase 4:**

| Aspecto | Tests unitarios | Tests de integración |
|---|---|---|
| Scope | Un componente aislado | Múltiples componentes |
| Dependencias | Totalmente mockeadas | Reales o parcialmente mockeadas |
| Velocidad | Rápidos (ms) | Más lentos (segundos) |
| Objetivo | Validar lógica interna | Validar interacción |

### Estrategia de mocking

**Mockear siempre:** APIs y servicios externos fuera del sistema (servicios de terceros, backends remotos), operaciones no determinísticas (emails, tiempo, random).

**Usar real o test double:** Base de datos → usar test DB (SQLite en memoria), filesystem → usar `tmp_path` de pytest, componentes propios del sistema → integrarlos realmente.

### Artefactos que produce

Archivos en `tests/integration/test_{feature}_integration.py` por flujo crítico.

### Flujos típicos por stack

**PyQt/MVC:** Señal modelo → actualización de vista, acción usuario → actualización modelo vía controlador, comunicación entre paneles.

**FastAPI/Layered:** Endpoint → Service → Repository → Database, manejo de excepciones end-to-end, autenticación/autorización.

**Flask REST/Layered:** Flujo CRUD completo, validación propagada a través de capas, error handling.

**Flask Webapp:** Template rendering con datos de API mockeada, form submission, error handlers.

**Generic Python:** Pipelines de procesamiento, integración entre módulos, integración con filesystem.

---

## Referencia técnica

### Entradas

| Entrada | Tipo | Requerida | Fuente |
|---|---|---|---|
| Archivos de código de producción | Artefactos | ✅ Sí | Fase 3 |
| Suite de tests unitarios pasando | Resultado ejecutable | ✅ Sí | Fase 4 |
| `docs/plans/{US_ID}-context.md` | Artefacto | ✅ Sí | Fase 0 |
| Framework de testing del perfil | `config.json` → `test_framework_config` | ✅ Sí | Perfil activo |

### Salidas

| Salida | Tipo | Descripción |
|---|---|---|
| `tests/integration/test_{feature}_integration.py` | Artefactos físicos | Tests de flujo completo |
| Resultado de `pytest tests/integration/ -v` | En conversación | Todos los tests deben pasar |

### Templates

| Template | Ruta en `config.json` |
|---|---|
| Test de integración genérico | `templates/testing/test-integration.py.tpl` |

Los perfiles definen `snippets.test_integration_class` con ejemplos concretos por stack.

### Artefactos

| Artefacto | Operación | Ruta |
|---|---|---|
| `test_{feature}_integration.py` | **Genera** | `tests/integration/` |
| `tests/conftest.py` | **Actualiza** (fixtures de integración) | `tests/conftest.py` |
| Código de producción | **Lee** | `{COMPONENT_PATH}/` |

### Estructura de tests recomendada

```python
"""Tests de integración para {FEATURE_NAME}."""
import pytest

class TestIntegration{Feature}:
    """Tests del flujo completo."""

    def test_flujo_exitoso_completo(self, fixtures):
        """Test del happy path end-to-end.
        Arrange: Setup del sistema completo
        Act: Ejecutar acción que atraviesa múltiples componentes
        Assert: Validar resultado final y estados intermedios
        """
        pass

    def test_flujo_con_error_en_componente_intermedio(self, fixtures):
        """Test de manejo de errores entre componentes."""
        pass
```

### Convenciones

- La precondición es ejecutar `pytest tests/unit/ -v --tb=short` y verificar que **pasan** (no solo que el directorio existe).
- Tests en `tests/integration/`.
- Ejecución: `pytest tests/integration/ -v`.
- El protocolo de recuperación usa "ciclos completos" (ejecución → diagnóstico → corrección), no "intentos".
- Las excepciones de mocking (mockear un componente interno) deben documentarse con comentario en el test.

### Protocolo de recuperación

**Síntoma:** Uno o más tests de integración fallan.

1. Leer el output completo del error
2. Determinar el origen del fallo:
   - **Problema de integración entre componentes** → revisar interfaces y contratos en Fase 3
   - **Componente individual roto** → volver a Fase 3, corregir, volver a Fases 4 y 5
   - **Test mal configurado** (fixture, mock incorrecto) → corregir el test en esta fase
3. Re-ejecutar: `pytest tests/integration/ -v`
4. No avanzar hasta que **todos** los tests pasen
5. Después de 2 ciclos sin resolución → informar al usuario

### Dependencias

| Dirección | Fase | Qué provee |
|---|---|---|
| ← anterior | Fase 4 | Tests unitarios pasando (precondición real) |
| → siguiente | Fase 6 | Tests de integración pasando |
| → siguiente | Fase 7 | Tests para medir coverage |

### Checklist de salida

- [ ] `pytest tests/unit/ -v --tb=short` pasa (precondición verificada)
- [ ] Todos los tests de integración pasan: `pytest tests/integration/ -v`
- [ ] Tracking de Fase 5 cerrado

### Estado en v1.3

| ID | Descripción | Resolución |
|---|---|---|
| D5-1 | La precondición no era clara: verificaba solo que el directorio `tests/unit/` existía, no que los tests pasaban | Se cambió a: ejecutar `pytest tests/unit/ -v --tb=short` y verificar que **pasan**. Si fallan, resolver en Fase 4 antes de continuar |
| D5-2 | `config.json` no tenía clave `integration_test_path` | Registrado como deuda técnica de baja prioridad; la ruta canónica es `tests/integration/` |

---

**Fase anterior:** [Fase 4: Tests Unitarios](phase-4.md)
**Siguiente fase:** [Fase 6: Validación BDD](phase-6.md) (si BDD aplica) / [Fase 7: Quality Gates](phase-7.md) (si BDD no aplica)
