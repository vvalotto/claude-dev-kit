# Resumen Ejecutivo — Reservas API (hexagonal-ddd-bc)

**Objetivo:** Demostrar el perfil `hexagonal-ddd-bc` del Claude Dev Kit con un
Bounded Context real y completo, ejecutable de punta a punta.

## Qué se construyó

Un BC `reservas` con las 8 piezas obligatorias del perfil (AggregateRoot,
2 ValueObjects, DomainEvent, Port, CommandHandler, QueryHandler, Repository,
ApiRouter), expuesto vía FastAPI, con una invariante de negocio real: no se
pueden crear dos reservas del mismo recurso que se solapen en fecha/horario.

## Resultado

| Aspecto | Resultado |
|---|---|
| Tests | 39 (25 unitarios + 7 integración + 5 BDD + 2 fixtures BDD internas), todos en verde |
| Pylint (`domain/` + `application/`) | 9.60/10 (umbral: 8.0) |
| Coverage (`domain/` + `application/`) | 100% (umbral: 90%) |
| Complejidad ciclomática | A en todas las funciones (umbral: 10) |

## Para quién es este ejemplo

Cualquiera que quiera adoptar el perfil `hexagonal-ddd-bc` y necesite ver,
antes de empezar su propio BC, cómo se ve un Bounded Context completo
respetando el orden de implementación y la regla de dependencia del perfil.

Ver el tutorial narrativo completo en
[`docs/examples/hexagonal-ddd-bc-project.md`](../../../docs/examples/hexagonal-ddd-bc-project.md).
