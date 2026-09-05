"""Port hacia un servicio externo de notificaciones (no persistencia).

Implementado en interface_adapters/gateways/ (gateway).
"""

from abc import ABC, abstractmethod

from suscripciones.entities.suscripcion import Suscripcion


class NotificacionGatewayPort(ABC):
    """Contrato de notificación externa que necesitan los UseCases."""

    @abstractmethod
    def notificar_alta(self, suscripcion: Suscripcion) -> None:
        """Notifica al usuario que su suscripción fue dada de alta."""

    @abstractmethod
    def notificar_baja(self, suscripcion: Suscripcion) -> None:
        """Notifica al usuario que su suscripción fue dada de baja."""
