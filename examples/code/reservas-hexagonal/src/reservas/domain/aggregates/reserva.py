"""AggregateRoot Reserva del BC Reservas."""

import uuid
from enum import Enum

from reservas.domain.events.reserva_creada import ReservaCreada
from reservas.domain.value_objects.fecha_reserva import FechaReserva
from reservas.domain.value_objects.rango_horario import RangoHorario


class EstadoReserva(str, Enum):
    """Estados posibles de una reserva."""

    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"


class Reserva:
    """Aggregate Root que encapsula las invariantes de una reserva.

    Sin dependencias de infraestructura: solo conoce sus propios
    ValueObjects y emite DomainEvents ante cambios de estado relevantes.
    """

    def __init__(
        self,
        reserva_id: str,
        recurso_id: str,
        fecha: FechaReserva,
        horario: RangoHorario,
        cliente_nombre: str,
        estado: EstadoReserva = EstadoReserva.CONFIRMADA,
    ) -> None:
        if not recurso_id:
            raise ValueError("recurso_id es obligatorio")
        if not cliente_nombre:
            raise ValueError("cliente_nombre es obligatorio")

        self.id = reserva_id
        self.recurso_id = recurso_id
        self.fecha = fecha
        self.horario = horario
        self.cliente_nombre = cliente_nombre
        self.estado = estado
        self._eventos: list = []

    @classmethod
    def crear(
        cls,
        recurso_id: str,
        fecha: FechaReserva,
        horario: RangoHorario,
        cliente_nombre: str,
    ) -> "Reserva":
        """Factory que crea una nueva reserva y registra su DomainEvent."""
        reserva = cls(
            reserva_id=str(uuid.uuid4()),
            recurso_id=recurso_id,
            fecha=fecha,
            horario=horario,
            cliente_nombre=cliente_nombre,
        )
        reserva._eventos.append(
            ReservaCreada(
                reserva_id=reserva.id,
                recurso_id=reserva.recurso_id,
                fecha=fecha.valor,
                hora_inicio=horario.hora_inicio,
                hora_fin=horario.hora_fin,
            )
        )
        return reserva

    def cancelar(self) -> None:
        """Cancela la reserva si está confirmada."""
        if self.estado == EstadoReserva.CANCELADA:
            raise ValueError("La reserva ya está cancelada")
        self.estado = EstadoReserva.CANCELADA

    def se_solapa_con(self, fecha: FechaReserva, horario: RangoHorario) -> bool:
        """Indica si esta reserva se solapa con la fecha/horario dados."""
        return self.fecha == fecha and self.horario.se_solapa_con(horario)

    def eventos_pendientes(self) -> list:
        """Devuelve y limpia los DomainEvents pendientes de publicar."""
        eventos, self._eventos = self._eventos, []
        return eventos
