"""DTOs que cruzan los límites de capa — nunca entities ni modelos de framework."""

from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass(frozen=True)
class CrearSuscripcionInput:
    """Input del caso de uso de alta de suscripción."""

    email: str
    plan: str


@dataclass(frozen=True)
class SuscripcionOutput:
    """Output común: representación plana de una Suscripcion."""

    id: int
    email: str
    plan: str
    activa: bool
    fecha_alta: date
    fecha_baja: Optional[date]


@dataclass(frozen=True)
class CancelarSuscripcionInput:
    """Input del caso de uso de baja de suscripción."""

    suscripcion_id: int
    fecha_baja: date
