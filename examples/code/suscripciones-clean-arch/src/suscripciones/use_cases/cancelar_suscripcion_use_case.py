"""UseCase: baja de una suscripción existente."""

from suscripciones.use_cases.dtos import CancelarSuscripcionInput, SuscripcionOutput
from suscripciones.use_cases.excepciones import SuscripcionNoEncontradaError
from suscripciones.use_cases.ports.notificacion_gateway_port import NotificacionGatewayPort
from suscripciones.use_cases.ports.suscripcion_repository_port import SuscripcionRepositoryPort


class CancelarSuscripcionUseCase:
    """Orquesta la baja de una suscripción a través de sus Ports."""

    def __init__(
        self,
        repositorio: SuscripcionRepositoryPort,
        notificador: NotificacionGatewayPort,
    ) -> None:
        self._repositorio = repositorio
        self._notificador = notificador

    def ejecutar(self, datos: CancelarSuscripcionInput) -> SuscripcionOutput:
        """Da de baja una suscripción existente.

        Args:
            datos: Id de la suscripción y fecha de baja.

        Returns:
            DTO con la suscripción ya cancelada.

        Raises:
            SuscripcionNoEncontradaError: Si no existe una suscripción con ese id.
            SuscripcionYaCanceladaError: Si la suscripción ya estaba inactiva.
        """
        suscripcion = self._repositorio.obtener_por_id(datos.suscripcion_id)
        if suscripcion is None:
            raise SuscripcionNoEncontradaError(
                f"No existe suscripción con id {datos.suscripcion_id}"
            )

        suscripcion.cancelar(datos.fecha_baja)

        suscripcion = self._repositorio.guardar(suscripcion)
        self._notificador.notificar_baja(suscripcion)

        return SuscripcionOutput(
            id=suscripcion.id,
            email=suscripcion.email,
            plan=suscripcion.plan,
            activa=suscripcion.activa,
            fecha_alta=suscripcion.fecha_alta,
            fecha_baja=suscripcion.fecha_baja,
        )
