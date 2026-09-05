"""Gateway: implementa el Port de notificaciones hacia un servicio externo.

En este ejemplo el "servicio externo" se simula guardando las notificaciones
en memoria (en un proyecto real, aquí iría un cliente de email/SMS/push).
"""

from suscripciones.entities.suscripcion import Suscripcion
from suscripciones.use_cases.ports.notificacion_gateway_port import NotificacionGatewayPort


class NotificacionGateway(NotificacionGatewayPort):
    """Adaptador de notificaciones — registra los eventos enviados."""

    def __init__(self) -> None:
        self.enviadas: list[str] = []

    def notificar_alta(self, suscripcion: Suscripcion) -> None:
        self.enviadas.append(
            f"ALTA: {suscripcion.email} suscripto al plan '{suscripcion.plan}'"
        )

    def notificar_baja(self, suscripcion: Suscripcion) -> None:
        self.enviadas.append(f"BAJA: {suscripcion.email} canceló su suscripción")
