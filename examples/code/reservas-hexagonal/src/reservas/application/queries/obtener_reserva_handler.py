"""QueryHandler ObtenerReservaHandler del BC Reservas."""

from dataclasses import dataclass
from datetime import date, time
from typing import Optional

from reservas.domain.aggregates.reserva import EstadoReserva
from reservas.domain.ports.reserva_repository import ReservaRepository


@dataclass(frozen=True)
class ObtenerReservaQuery:
    """Query de entrada para obtener una reserva por id."""

    reserva_id: str


@dataclass(frozen=True)
class ReservaDTO:
    """Vista de solo lectura de una reserva, sin exponer el aggregate."""

    id: str
    recurso_id: str
    fecha: date
    hora_inicio: time
    hora_fin: time
    cliente_nombre: str
    estado: EstadoReserva


class ObtenerReservaHandler:
    """Lee una reserva del repositorio y la traduce a DTO.

    Sin side effects — solo lectura.
    """

    def __init__(self, repository: ReservaRepository) -> None:
        self._repository = repository

    def handle(self, query: ObtenerReservaQuery) -> Optional[ReservaDTO]:
        """Devuelve el DTO de la reserva solicitada, o None si no existe."""
        reserva = self._repository.obtener_por_id(query.reserva_id)
        if reserva is None:
            return None

        return ReservaDTO(
            id=reserva.id,
            recurso_id=reserva.recurso_id,
            fecha=reserva.fecha.valor,
            hora_inicio=reserva.horario.hora_inicio,
            hora_fin=reserva.horario.hora_fin,
            cliente_nombre=reserva.cliente_nombre,
            estado=reserva.estado,
        )
