"""Port de persistencia para Suscripcion.

Implementado en frameworks/repositories/ (repository_impl).
"""

from abc import ABC, abstractmethod
from typing import Optional

from suscripciones.entities.suscripcion import Suscripcion


class SuscripcionRepositoryPort(ABC):
    """Contrato de persistencia que necesita el UseCase."""

    @abstractmethod
    def guardar(self, suscripcion: Suscripcion) -> Suscripcion:
        """Persiste una suscripción (nueva o ya existente) y la retorna."""

    @abstractmethod
    def obtener_por_id(self, suscripcion_id: int) -> Optional[Suscripcion]:
        """Busca una suscripción por id. None si no existe."""

    @abstractmethod
    def obtener_por_email(self, email: str) -> Optional[Suscripcion]:
        """Busca la última suscripción registrada de un email. None si no existe."""
