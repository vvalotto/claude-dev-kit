"""DomainEvent ReservaCreada del BC Reservas."""

from dataclasses import dataclass, field
from datetime import date, datetime, time, timezone


@dataclass(frozen=True)
class ReservaCreada:
    """Describe que una reserva fue creada en el dominio.

    Inmutable — todos los campos son de solo lectura tras la construcción.
    """

    reserva_id: str
    recurso_id: str
    fecha: date
    hora_inicio: time
    hora_fin: time
    ocurrido_en: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
