"""ApiRouter del BC Reservas.

Solo importa application/ — nunca domain/ directamente. Traduce el
request HTTP a Command/Query y el resultado de vuelta a response HTTP.
"""

from datetime import date, time
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from reservas.application.commands.crear_reserva_handler import (
    CrearReservaComando,
    CrearReservaHandler,
)
from reservas.application.queries.obtener_reserva_handler import (
    ObtenerReservaHandler,
    ObtenerReservaQuery,
)
from reservas.domain.errors import ReservaSolapadaError
from reservas.infrastructure.repositories.reserva_repository_memoria import (
    ReservaRepositoryMemoria,
)

router = APIRouter(prefix="/reservas", tags=["reservas"])

_repository = ReservaRepositoryMemoria()


class CrearReservaRequest(BaseModel):
    """Body de la petición para crear una reserva."""

    recurso_id: str
    fecha: date
    hora_inicio: time
    hora_fin: time
    cliente_nombre: str


class ReservaResponse(BaseModel):
    """Respuesta con los datos de una reserva."""

    id: str
    recurso_id: str
    fecha: date
    hora_inicio: time
    hora_fin: time
    cliente_nombre: str
    estado: str


def get_repository() -> ReservaRepositoryMemoria:
    """Provee la instancia del repositorio (override-able en tests vía dependency_overrides)."""
    return _repository


RepositoryDep = Annotated[ReservaRepositoryMemoria, Depends(get_repository)]


@router.post("/", response_model=dict, status_code=201)
def crear_reserva(request: CrearReservaRequest, repository: RepositoryDep) -> dict:
    """Crea una nueva reserva."""
    handler = CrearReservaHandler(repository)
    comando = CrearReservaComando(
        recurso_id=request.recurso_id,
        fecha=request.fecha,
        hora_inicio=request.hora_inicio,
        hora_fin=request.hora_fin,
        cliente_nombre=request.cliente_nombre,
    )
    try:
        reserva_id = handler.handle(comando)
    except ReservaSolapadaError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error

    return {"id": reserva_id}


@router.get("/{reserva_id}", response_model=ReservaResponse)
def obtener_reserva(reserva_id: str, repository: RepositoryDep) -> ReservaResponse:
    """Obtiene una reserva por id."""
    handler = ObtenerReservaHandler(repository)
    dto = handler.handle(ObtenerReservaQuery(reserva_id=reserva_id))

    if dto is None:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")

    return ReservaResponse(
        id=dto.id,
        recurso_id=dto.recurso_id,
        fecha=dto.fecha,
        hora_inicio=dto.hora_inicio,
        hora_fin=dto.hora_fin,
        cliente_nombre=dto.cliente_nombre,
        estado=dto.estado.value,
    )
