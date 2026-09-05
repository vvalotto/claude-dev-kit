# Reporte de Validación — Reservas API (hexagonal-ddd-bc)

**Fecha:** 2026-09-05

## Comandos ejecutados

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python -m pytest
PYTHONPATH=src python -m pylint src/reservas/domain src/reservas/application
python -m radon cc src/reservas -a
```

## Resultados

### Tests

```
39 passed, 0 warnings
```

- Unitarios: `tests/unit/reservas/` (25 tests — ValueObjects, AggregateRoot, ambos Handlers)
- Integración: `tests/integration/reservas/` (7 tests — Repository real + API end-to-end)
- BDD: `features/steps/reserva_steps.py` (5 escenarios — camino feliz, solapamiento, fecha pasada, 404)

### Coverage

Scope del perfil (`domain/` + `application/`): **100%** (umbral: 90%)

### Pylint

Scope del perfil (`domain/` + `application/`): **9.60/10** (umbral: 8.0)

Hallazgos no bloqueantes (por debajo del umbral, no requieren corrección):
- `too-many-arguments` en el constructor de `Reserva` (6 parámetros — razonable
  para un aggregate con esta cantidad de atributos de dominio)
- `too-few-public-methods` en ambos Handlers (esperado: el patrón
  Command/QueryHandler expone intencionalmente un solo método `handle()`)
- `duplicate-code` entre `CrearReservaComando` y `ReservaDTO` (ambos son
  dataclasses con campos similares — duplicación aceptable entre un comando
  de entrada y un DTO de salida, son conceptos distintos)

### Complejidad Ciclomática

Todas las funciones/métodos calificados **A** (máximo observado: 3).
Umbral del perfil: ≤ 10 por función.

## Estado Final

**✅ APROBADO** — el BC `reservas` cumple todos los quality gates del perfil
`hexagonal-ddd-bc`.
