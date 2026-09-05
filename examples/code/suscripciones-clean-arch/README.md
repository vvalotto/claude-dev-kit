# Suscripciones — Clean Architecture BC-First

API de alta/baja de suscripciones construida con FastAPI, demostrando el framework Claude Dev Kit con el perfil **clean-architecture-bc**.

## Features

- ✅ **Alta y baja de suscripciones**: crear una suscripción y cancelarla
- ✅ **Clean Architecture BC-First**: capas `entities → use_cases → interface_adapters → frameworks`, Dependency Rule estricta
- ✅ **Ports & Adapters**: persistencia y notificaciones como Ports, implementados en capas externas
- ✅ **Tests exhaustivos**: unitarios + integración + escenarios BDD (pytest-bdd)
- ✅ **Type hints completos**

## Arquitectura

```
src/suscripciones/
├── entities/               # Reglas de negocio empresariales — sin dependencias externas
│   ├── suscripcion.py      # Entity Suscripcion
│   └── excepciones.py
├── use_cases/               # Reglas de negocio de la aplicación — solo importa entities/
│   ├── ports/                # Contratos (interfaces) que necesitan los UseCases
│   │   ├── suscripcion_repository_port.py
│   │   └── notificacion_gateway_port.py
│   ├── dtos.py                # Input/Output DTOs — cruzan límites de capa
│   ├── excepciones.py
│   ├── crear_suscripcion_use_case.py
│   └── cancelar_suscripcion_use_case.py
├── interface_adapters/      # Adapta datos entre use_cases y frameworks — solo importa use_cases/
│   ├── controllers/
│   │   └── suscripcion_controller.py
│   └── gateways/
│       └── notificacion_gateway.py   # Implementa NotificacionGatewayPort
└── frameworks/               # Capa más externa — conecta todo
    ├── repositories/
    │   └── memoria_suscripcion_repository.py   # Implementa SuscripcionRepositoryPort
    └── api/
        └── router.py          # FastAPI — traduce excepciones a códigos HTTP
```

### Dependency Rule

Las dependencias del código fuente solo apuntan hacia adentro:

`frameworks/` → `interface_adapters/` → `use_cases/` → `entities/`

`entities/` no importa nada fuera de su propio paquete. `use_cases/` solo importa `entities/`. `interface_adapters/` solo importa `use_cases/`. La comunicación entre capas externas e internas siempre cruza a través de un **Port** definido en `use_cases/ports/`.

### Simplificación deliberada del tutorial

El perfil `clean-architecture-bc` sugiere FastAPI + SQLAlchemy async + PostgreSQL. Este ejemplo usa un **repositorio en memoria** (`MemoriaSuscripcionRepository`) para poder ejecutarse sin infraestructura externa — implementa exactamente la misma interfaz (`SuscripcionRepositoryPort`) que tendría una implementación real con SQLAlchemy, por lo que reemplazarla no afecta a ninguna otra capa.

## Prerequisitos

- Python 3.10+
- pip

## Instalación

```bash
cd examples/code/suscripciones-clean-arch

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

## Ejecutar la API

```bash
uvicorn main:app --reload
```

- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs

## Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/suscripciones` | Da de alta una suscripción (`email`, `plan`) |
| POST | `/suscripciones/{id}/cancelar` | Da de baja una suscripción existente |

### Crear una suscripción

```bash
curl -X POST http://localhost:8000/suscripciones \
  -H "Content-Type: application/json" \
  -d '{"email": "ana@example.com", "plan": "basico"}'
```

Respuesta (`201`):
```json
{
  "id": 1,
  "email": "ana@example.com",
  "plan": "basico",
  "activa": true,
  "fecha_alta": "2026-09-05",
  "fecha_baja": null
}
```

### Cancelar una suscripción

```bash
curl -X POST http://localhost:8000/suscripciones/1/cancelar
```

**Códigos de error:** `409` (email ya suscripto / ya cancelada), `422` (plan inválido), `404` (id inexistente).

## Correr los Tests

```bash
# Todos los tests (unitarios + integración + BDD)
pytest

# Con reporte de cobertura (entities/ + use_cases/, según quality_gates del perfil)
pytest --cov-report=term-missing

# Solo unitarios
pytest tests/unit/

# Solo integración
pytest tests/integration/

# Solo BDD
pytest features/steps/
```

**Resultado real:** 25 tests pasando (14 unitarios + 7 integración + 4 BDD), **100% de cobertura** en `entities/` + `use_cases/` (umbral mínimo del perfil: 90%).

## Calidad de Código

```bash
pylint src/suscripciones/entities src/suscripciones/use_cases
```

**Resultado real:** 9.67/10 (umbral mínimo del perfil: 8.0). El scope de Pylint/coverage del perfil `clean-architecture-bc` es únicamente `entities/` + `use_cases/` — `interface_adapters/` y `frameworks/` no cuentan para los umbrales.

## Estructura del Proyecto

```
suscripciones-clean-arch/
├── main.py                          # Composition root — arma el grafo de dependencias
├── src/suscripciones/
│   ├── entities/
│   ├── use_cases/
│   ├── interface_adapters/
│   └── frameworks/
├── tests/
│   ├── unit/suscripciones/          # Tests de entities/ y use_cases/ (con fakes de los Ports)
│   └── integration/suscripciones/   # Tests end-to-end vía TestClient
├── features/
│   ├── suscripciones.feature
│   └── steps/
├── conftest.py                       # Fixture `client` compartida (integración + BDD)
├── requirements.txt
├── pytest.ini
└── README.md
```

## Próximos Pasos

1. **Persistencia real**: reemplazar `MemoriaSuscripcionRepository` por una implementación con SQLAlchemy async + PostgreSQL — sin tocar ninguna otra capa.
2. **Gateway real**: reemplazar `NotificacionGateway` por un cliente de email/SMS real.
3. **Más Use Cases**: `CambiarPlanUseCase`, `ListarSuscripcionesUseCase`.
4. **Autenticación**: agregar un Controller/Port de autenticación como nueva capa de `interface_adapters/`.

## Generado con Claude Dev Kit

Este proyecto fue generado siguiendo el flujo de [Claude Dev Kit](https://github.com/vvalotto/claude-dev-kit) con el perfil **clean-architecture-bc**. Ver el tutorial completo en [`docs/examples/clean-architecture-bc-project.md`](../../../docs/examples/clean-architecture-bc-project.md).

## Licencia

MIT License
