# US-070: Reserva de un Recurso — Reporte Final

**Perfil:** hexagonal-ddd-bc
**Bounded Context:** `reservas`
**Fecha:** 2026-09-05

---

## Resumen

Se implementó el BC `reservas` completo siguiendo el perfil `hexagonal-ddd-bc`:
1 AggregateRoot, 2 ValueObjects, 1 DomainEvent, 1 Port, 1 CommandHandler,
1 QueryHandler, 1 Repository y 1 ApiRouter, respetando el orden de
implementación y la regla de dependencia (`domain/` no importa nada fuera de
su propio `domain/`).

## Tareas Completadas

Ver checklist completo en [`US-070-plan.md`](../planning/US-070-plan.md) — las
8 tareas del orden de implementación obligatorio quedaron completas.

## Tests

| Suite | Cantidad | Resultado |
|---|---|---|
| Unitarios (`tests/unit/reservas/`) | 25 | ✅ Todos pasan |
| Integración (`tests/integration/reservas/`) | 7 | ✅ Todos pasan |
| BDD (`features/reservas.feature`) | 5 escenarios | ✅ Todos pasan |
| **Total** | **39** (34 tests + 5 escenarios BDD) | ✅ |

## Quality Gates

| Métrica | Umbral del perfil | Resultado real | Estado |
|---|---|---|---|
| Pylint (`domain/` + `application/`) | ≥ 8.0 | 9.60/10 | ✅ APROBADO |
| Coverage (`domain/` + `application/`) | ≥ 90% | 100% | ✅ APROBADO |
| Complejidad ciclomática máx. por función | ≤ 10 | A (máx. observado: 3) | ✅ APROBADO |

**Estado final: APROBADO**

## Decisiones Tomadas

- **Repository en memoria** en vez de una base de datos real: mantiene el
  tutorial enfocado en la arquitectura hexagonal (el Port es lo que importa,
  no el motor de persistencia) y evita dependencias externas para correrlo.
- **1 solo DomainEvent** (`ReservaCreada`), sin Event Sourcing: el aggregate
  tiene estado directo (`estado: EstadoReserva`) y el evento es informativo,
  no la fuente de verdad — siguiendo la nota `crud_note` del perfil para BCs
  que no requieren Event Sourcing completo.
- **Invariante de solapamiento resuelta en dos capas**: el ValueObject
  `RangoHorario.se_solapa_con()` resuelve la geometría del solapamiento
  (sin conocer nada de persistencia); el `CommandHandler` orquesta la
  consulta al repositorio y decide si rechazar el comando — así `domain/`
  no depende de infraestructura para su propia lógica de comparación.

## Próximos Pasos Sugeridos (fuera de alcance de esta HU)

- Cancelación de reservas expuesta vía API (el método `cancelar()` del
  aggregate ya existe pero no tiene endpoint ni CommandHandler propio).
- Persistencia real (ej. SQLAlchemy) implementando el mismo Port
  `ReservaRepository` — el resto del BC no debería cambiar.
