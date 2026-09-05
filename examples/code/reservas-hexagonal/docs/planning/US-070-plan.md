# US-070: Reserva de un Recurso — Plan de Implementación

**Stack:** hexagonal-ddd-bc
**Perfil:** hexagonal-ddd-bc.json
**Arquitectura:** Hexagonal DDD BC-First (`domain → application → infrastructure → api`)
**Bounded Context:** `reservas`
**Fecha:** 2026-09-05

---

## 1. Contexto

La historia de usuario US-070 solicita permitir la reserva de un recurso (ej. una
mesa) en una fecha y horario, evitando solapamientos con otras reservas
confirmadas del mismo recurso. El perfil `hexagonal-ddd-bc` indica:

- Arquitectura hexagonal con DDD, organizada por Bounded Context
- `domain/` sin dependencias externas — solo puede importar de su propio `domain/`
- Orden de implementación obligatorio: ValueObjects → DomainEvents → AggregateRoot
  → Ports → CommandHandlers → QueryHandlers → Repositories → ApiRouter
- Quality Gates: Pylint ≥ 8.0, Coverage ≥ 90% (scope: `domain/` + `application/`),
  CC ≤ 10 por función

## 2. Arquitectura Seleccionada

```
src/reservas/
├── domain/
│   ├── aggregates/reserva.py            ← AggregateRoot Reserva
│   ├── value_objects/
│   │   ├── fecha_reserva.py             ← ValueObject FechaReserva
│   │   └── rango_horario.py             ← ValueObject RangoHorario
│   ├── events/reserva_creada.py         ← DomainEvent ReservaCreada
│   ├── ports/reserva_repository.py      ← Port ReservaRepository
│   └── errors.py                        ← Excepciones de dominio
├── application/
│   ├── commands/crear_reserva_handler.py    ← CommandHandler
│   └── queries/obtener_reserva_handler.py   ← QueryHandler
├── infrastructure/
│   └── repositories/reserva_repository_memoria.py  ← Repository (en memoria)
└── api/
    └── router.py                        ← ApiRouter (FastAPI)
```

## 3. Tareas (en orden de implementación obligatorio)

- [x] **ValueObjects:** `FechaReserva` (rechaza fechas pasadas) y `RangoHorario`
      (rechaza horarios invertidos/vacíos, expone `se_solapa_con`)
- [x] **DomainEvent:** `ReservaCreada` (inmutable, registra qué/cuándo)
- [x] **AggregateRoot:** `Reserva` — factory `crear()` que valida invariantes y
      emite `ReservaCreada`; método `cancelar()`; método `se_solapa_con()`
- [x] **Port:** `ReservaRepository` (ABC) — `guardar`, `obtener_por_id`,
      `existe_solapamiento`
- [x] **CommandHandler:** `CrearReservaHandler` — verifica solapamiento vía
      repositorio, delega la creación al aggregate, persiste
- [x] **QueryHandler:** `ObtenerReservaHandler` — lee del repositorio, traduce a
      `ReservaDTO` (sin exponer el aggregate)
- [x] **Repository:** `ReservaRepositoryMemoria` — implementación en memoria del
      Port, para el tutorial y los tests
- [x] **ApiRouter:** `POST /reservas/` y `GET /reservas/{id}` — solo importa
      `application/`, traduce HTTP ↔ Command/Query

## 4. Estrategia de Testing

- **Unitarios** (`tests/unit/reservas/`): ValueObjects, AggregateRoot, ambos
  Handlers — con repositorio en memoria como test double liviano.
- **Integración** (`tests/integration/reservas/`): Repository real +
  Aggregate real; API end-to-end vía `TestClient` con `dependency_overrides`.
- **BDD** (`features/reservas.feature` + `features/steps/reserva_steps.py`):
  5 escenarios cubriendo el camino feliz, el rechazo por solapamiento, la
  independencia entre recursos/horarios, la validación de fecha pasada y el 404.

## 5. Quality Gates Esperados

| Métrica | Umbral del perfil | Resultado |
|---|---|---|
| Pylint (`domain/` + `application/`) | ≥ 8.0 | 9.60/10 |
| Coverage (`domain/` + `application/`) | ≥ 90% | 100% |
| Complejidad ciclomática máx. por función | ≤ 10 | A (máx. 3) en todo el BC |
