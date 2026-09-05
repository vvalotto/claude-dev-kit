"""ValueObject RangoHorario del BC Reservas."""

from dataclasses import dataclass
from datetime import time


@dataclass(frozen=True)
class RangoHorario:
    """Rango horario de una reserva (hora de inicio y de fin).

    Inmutable, con igualdad por valor y validación de consistencia propia:
    la hora de fin debe ser posterior a la hora de inicio.
    """

    hora_inicio: time
    hora_fin: time

    def __post_init__(self) -> None:
        if self.hora_fin <= self.hora_inicio:
            raise ValueError("La hora de fin debe ser posterior a la hora de inicio")

    def se_solapa_con(self, otro: "RangoHorario") -> bool:
        """Indica si este rango horario se superpone con otro."""
        return self.hora_inicio < otro.hora_fin and otro.hora_inicio < self.hora_fin

    def __str__(self) -> str:
        return f"{self.hora_inicio.isoformat()}-{self.hora_fin.isoformat()}"
