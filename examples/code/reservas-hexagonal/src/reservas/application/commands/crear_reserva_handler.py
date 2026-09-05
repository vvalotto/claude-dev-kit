"""CommandHandler CrearReservaHandler del BC Reservas."""

from dataclasses import dataclass
from datetime import date, time

from reservas.domain.aggregates.reserva import Reserva
from reservas.domain.errors import ReservaSolapadaError
from reservas.domain.ports.reserva_repository import ReservaRepository
from reservas.domain.value_objects.fecha_reserva import FechaReserva
from reservas.domain.value_objects.rango_horario import RangoHorario


@dataclass(frozen=True)
class CrearReservaComando:
    """Comando de entrada para crear una reserva."""

    recurso_id: str
    fecha: date
    hora_inicio: time
    hora_fin: time
    cliente_nombre: str


class CrearReservaHandler:
    """Orquesta la creación de una reserva.

    Sin lógica de negocio propia — delega las invariantes al aggregate
    y consulta el repositorio solo para verificar solapamientos.
    """

    def __init__(self, repository: ReservaRepository) -> None:
        self._repository = repository

    def handle(self, comando: CrearReservaComando) -> str:
        """Crea una reserva y la persiste. Devuelve el id generado."""
        fecha = FechaReserva(comando.fecha)
        horario = RangoHorario(comando.hora_inicio, comando.hora_fin)

        if self._repository.existe_solapamiento(comando.recurso_id, fecha, horario):
            raise ReservaSolapadaError(
                f"Ya existe una reserva para {comando.recurso_id} "
                f"el {fecha} en el horario {horario}"
            )

        reserva = Reserva.crear(
            recurso_id=comando.recurso_id,
            fecha=fecha,
            horario=horario,
            cliente_nombre=comando.cliente_nombre,
        )
        self._repository.guardar(reserva)
        reserva.eventos_pendientes()  # en un BC real se publicarían acá

        return reserva.id
