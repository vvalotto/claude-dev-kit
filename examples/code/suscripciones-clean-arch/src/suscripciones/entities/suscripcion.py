"""Entity Suscripcion — regla de negocio empresarial del BC Suscripciones."""

from dataclasses import dataclass, field
from datetime import date
from typing import Optional

from suscripciones.entities.excepciones import (
    EmailInvalidoError,
    PlanInvalidoError,
    SuscripcionYaCanceladaError,
)

PLANES_VALIDOS = frozenset({"basico", "premium"})


@dataclass
class Suscripcion:
    """Suscripción de un usuario a un plan del servicio.

    Encapsula las invariantes de negocio: un email válido, un plan
    soportado, y las reglas de transición de alta/baja.
    """

    email: str
    plan: str
    fecha_alta: date
    id: Optional[int] = None
    activa: bool = field(default=True)
    fecha_baja: Optional[date] = None

    def __post_init__(self) -> None:
        if "@" not in self.email or not self.email.strip():
            raise EmailInvalidoError(f"Email inválido: '{self.email}'")
        if self.plan not in PLANES_VALIDOS:
            raise PlanInvalidoError(
                f"Plan '{self.plan}' no soportado. Válidos: {sorted(PLANES_VALIDOS)}"
            )

    def cancelar(self, fecha: date) -> None:
        """Da de baja la suscripción.

        Args:
            fecha: Fecha en la que se produce la baja.

        Raises:
            SuscripcionYaCanceladaError: Si la suscripción ya estaba inactiva.
        """
        if not self.activa:
            raise SuscripcionYaCanceladaError(
                f"La suscripción {self.id} ya estaba cancelada"
            )
        self.activa = False
        self.fecha_baja = fecha
