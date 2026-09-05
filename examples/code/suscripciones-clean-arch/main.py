"""Composition root: arma el grafo de dependencias y expone la app FastAPI.

Es el único lugar del proyecto que conoce todas las capas a la vez —
entities, use_cases, interface_adapters y frameworks — para poder
conectarlas (Dependency Injection manual).
"""

from fastapi import FastAPI

from suscripciones.frameworks.api.router import crear_router
from suscripciones.frameworks.repositories.memoria_suscripcion_repository import (
    MemoriaSuscripcionRepository,
)
from suscripciones.interface_adapters.controllers.suscripcion_controller import (
    SuscripcionController,
)
from suscripciones.interface_adapters.gateways.notificacion_gateway import NotificacionGateway
from suscripciones.use_cases.cancelar_suscripcion_use_case import CancelarSuscripcionUseCase
from suscripciones.use_cases.crear_suscripcion_use_case import CrearSuscripcionUseCase

repositorio = MemoriaSuscripcionRepository()
notificador = NotificacionGateway()

crear_use_case = CrearSuscripcionUseCase(repositorio, notificador)
cancelar_use_case = CancelarSuscripcionUseCase(repositorio, notificador)

controller = SuscripcionController(crear_use_case, cancelar_use_case)

app = FastAPI(title="Suscripciones API", version="1.0.0")
app.include_router(crear_router(controller))


@app.get("/")
def root():
    """Endpoint de salud usado por los tests de integración."""
    return {"status": "ok", "service": "suscripciones"}
