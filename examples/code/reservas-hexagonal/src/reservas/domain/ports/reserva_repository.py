"""Port ReservaRepository del BC Reservas."""

from abc import ABC, abstractmethod
from typing import Optional

from reservas.domain.aggregates.reserva import Reserva
from reservas.domain.value_objects.fecha_reserva import FechaReserva
from reservas.domain.value_objects.rango_horario import RangoHorario


class ReservaRepository(ABC):
    """Contrato de persistencia para el aggregate Reserva.

    Solo métodos abstractos — la implementación concreta vive en
    infrastructure/repositories/.
    """

    @abstractmethod
    def guardar(self, reserva: Reserva) -> None:
        """Persiste una reserva (alta o actualización)."""

    @abstractmethod
    def obtener_por_id(self, reserva_id: str) -> Optional[Reserva]:
        """Obtiene una reserva por su id, o None si no existe."""

    @abstractmethod
    def existe_solapamiento(
        self, recurso_id: str, fecha: FechaReserva, horario: RangoHorario
    ) -> bool:
        """Indica si ya existe una reserva confirmada que se solape."""
