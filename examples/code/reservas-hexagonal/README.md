# Reservas API (Hexagonal DDD BC-First)

API de reservas de un recurso (ej. una mesa), construida con FastAPI,
demostrando el framework Claude Dev Kit con el perfil **hexagonal-ddd-bc**.

## Features

- ✅ **Crear y consultar reservas**: `POST /reservas/`, `GET /reservas/{id}`
- ✅ **Invariante de negocio real**: rechaza reservas solapadas para el mismo recurso
- ✅ **Arquitectura Hexagonal DDD BC-First**: `domain → application → infrastructure → api`
- ✅ **Tests completos**: unitarios + integración + BDD (pytest-bdd)
- ✅ **100% Type Hints**: type safety completo con anotaciones de Python

## Arquitectura

```
src/reservas/
├── domain/                  # Sin dependencias externas
│   ├── aggregates/           # Reserva (AggregateRoot)
│   ├── value_objects/        # FechaReserva, RangoHorario
│   ├── events/                # ReservaCreada (DomainEvent)
│   ├── ports/                 # ReservaRepository (interfaz)
│   └── errors.py              # Excepciones de dominio
├── application/              # Orquesta el domain, sin infraestructura directa
│   ├── commands/               # CrearReservaHandler
│   └── queries/                 # ObtenerReservaHandler
├── infrastructure/           # Implementa los Ports
│   └── repositories/           # ReservaRepositoryMemoria
└── api/                      # Solo importa application/
    └── router.py                # Endpoints FastAPI
```

### Regla de dependencia (Bounded Context `reservas`)

`domain/` no importa nada fuera de su propio `domain/`. `application/` importa
`domain/` pero nunca `infrastructure/`. `api/` importa `application/`, nunca
`domain/` directamente.

## Prerequisites

- Python 3.10+
- pip

## Installation

```bash
cd examples/code/reservas-hexagonal

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

## Running the API

```bash
# PYTHONPATH=src es necesario porque el código fuente vive en src/reservas/
# (pytest lo resuelve solo vía pytest.ini; uvicorn no)
PYTHONPATH=src uvicorn main:app --reload
```

- **API:** http://localhost:8000
- **Swagger UI:** http://localhost:8000/docs

## Running Tests

```bash
# Todo (unitarios + integración + BDD)
pytest

# Solo unitarios
pytest tests/unit/ -v

# Solo integración
pytest tests/integration/ -v

# Solo BDD
pytest features/steps/ -v

# Con reporte de cobertura HTML
pytest --cov-report=html
open htmlcov/index.html
```

## Quality Gates (perfil hexagonal-ddd-bc)

```bash
# Pylint sobre domain/ + application/ (scope del perfil)
PYTHONPATH=src pylint src/reservas/domain src/reservas/application

# Complejidad ciclomática
radon cc src/reservas -a
```

| Métrica | Umbral | Resultado |
|---|---|---|
| Pylint (`domain/` + `application/`) | ≥ 8.0 | 9.60/10 |
| Coverage (`domain/` + `application/`) | ≥ 90% | 100% |
| CC máx. por función | ≤ 10 | A (máx. 3) |

## Documentación

- Historia de usuario: [`historias-usuario/US-070.md`](historias-usuario/US-070.md)
- Plan de implementación: [`docs/planning/US-070-plan.md`](docs/planning/US-070-plan.md)
- Reporte final: [`docs/reporting/US-070-report.md`](docs/reporting/US-070-report.md)
- Tutorial completo paso a paso: [`docs/examples/hexagonal-ddd-bc-project.md`](../../../docs/examples/hexagonal-ddd-bc-project.md)

## Ejemplo de uso

```bash
# Crear una reserva
curl -X POST http://localhost:8000/reservas/ \
  -H "Content-Type: application/json" \
  -d '{
    "recurso_id": "mesa-1",
    "fecha": "2026-12-24",
    "hora_inicio": "20:00:00",
    "hora_fin": "22:00:00",
    "cliente_nombre": "Ana"
  }'
# → 201 {"id": "..."}

# Consultarla
curl http://localhost:8000/reservas/{id}
# → 200 {"id": "...", "recurso_id": "mesa-1", "estado": "CONFIRMADA", ...}

# Intentar una reserva solapada
curl -X POST http://localhost:8000/reservas/ \
  -H "Content-Type: application/json" \
  -d '{
    "recurso_id": "mesa-1",
    "fecha": "2026-12-24",
    "hora_inicio": "20:30:00",
    "hora_fin": "21:30:00",
    "cliente_nombre": "Bruno"
  }'
# → 409 {"detail": "Ya existe una reserva para mesa-1 el 2026-12-24 en el horario 20:00:00-22:00:00"}
```
