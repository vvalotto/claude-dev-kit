"""api_router — capa más externa. Conoce todo, es conocida por nada.

Expone los endpoints HTTP y delega en el Controller. Traduce las
excepciones de dominio/aplicación a códigos de estado HTTP.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from suscripciones.entities.excepciones import (
    EmailInvalidoError,
    PlanInvalidoError,
    SuscripcionYaCanceladaError,
)
from suscripciones.interface_adapters.controllers.suscripcion_controller import (
    SuscripcionController,
)
from suscripciones.use_cases.excepciones import (
    SuscripcionNoEncontradaError,
    SuscripcionYaExisteError,
)


class CrearSuscripcionRequest(BaseModel):
    """Body esperado para dar de alta una suscripción."""

    email: str
    plan: str


def crear_router(controller: SuscripcionController) -> APIRouter:
    """Construye el router de Suscripciones inyectando su Controller."""
    router = APIRouter(prefix="/suscripciones", tags=["suscripciones"])

    @router.post("", status_code=201)
    def crear_suscripcion(body: CrearSuscripcionRequest):
        try:
            return controller.crear(body.model_dump())
        except (EmailInvalidoError, PlanInvalidoError) as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        except SuscripcionYaExisteError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc

    @router.post("/{suscripcion_id}/cancelar")
    def cancelar_suscripcion(suscripcion_id: int):
        try:
            return controller.cancelar(suscripcion_id)
        except SuscripcionNoEncontradaError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except SuscripcionYaCanceladaError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc

    return router
