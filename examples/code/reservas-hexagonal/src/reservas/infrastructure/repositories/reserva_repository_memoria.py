"""Implementación en memoria del Port ReservaRepository."""

from typing import Dict, Optional

from reservas.domain.aggregates.reserva import EstadoReserva, Reserva
from reservas.domain.ports.reserva_repository import ReservaRepository
from reservas.domain.value_objects.fecha_reserva import FechaReserva
from reservas.domain.value_objects.rango_horario import RangoHorario


class ReservaRepositoryMemoria(ReservaRepository):
    """Implementa el puerto de dominio con almacenamiento en memoria.

    Pensado para el tutorial y para tests de integración — traduce entre
    el aggregate de dominio y el diccionario que actúa de "persistencia".
    Sin lógica de negocio: solo guarda/consulta.
    """

    def __init__(self) -> None:
        self._reservas: Dict[str, Reserva] = {}

    def guardar(self, reserva: Reserva) -> None:
        self._reservas[reserva.id] = reserva

    def obtener_por_id(self, reserva_id: str) -> Optional[Reserva]:
        return self._reservas.get(reserva_id)

    def existe_solapamiento(
        self, recurso_id: str, fecha: FechaReserva, horario: RangoHorario
    ) -> bool:
        return any(
            reserva.recurso_id == recurso_id
            and reserva.estado == EstadoReserva.CONFIRMADA
            and reserva.se_solapa_con(fecha, horario)
            for reserva in self._reservas.values()
        )

    def limpiar(self) -> None:
        """Utilidad para tests: vacía el almacenamiento en memoria."""
        self._reservas.clear()
