"""ValueObject FechaReserva del BC Reservas."""

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class FechaReserva:
    """Fecha en la que se realiza una reserva.

    Inmutable y con validación propia: no acepta fechas pasadas.
    """

    valor: date

    def __post_init__(self) -> None:
        if self.valor < date.today():
            raise ValueError("La fecha de reserva no puede ser en el pasado")

    def es_hoy(self) -> bool:
        """Indica si la fecha de reserva es hoy."""
        return self.valor == date.today()

    def __str__(self) -> str:
        return self.valor.isoformat()
