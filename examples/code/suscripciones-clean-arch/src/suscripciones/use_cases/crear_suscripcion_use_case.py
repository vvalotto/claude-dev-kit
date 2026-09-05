"""UseCase: alta de una nueva suscripción."""

from datetime import date

from suscripciones.entities.suscripcion import Suscripcion
from suscripciones.use_cases.dtos import CrearSuscripcionInput, SuscripcionOutput
from suscripciones.use_cases.excepciones import SuscripcionYaExisteError
from suscripciones.use_cases.ports.notificacion_gateway_port import NotificacionGatewayPort
from suscripciones.use_cases.ports.suscripcion_repository_port import SuscripcionRepositoryPort


class CrearSuscripcionUseCase:
    """Orquesta el alta de una suscripción a través de sus Ports."""

    def __init__(
        self,
        repositorio: SuscripcionRepositoryPort,
        notificador: NotificacionGatewayPort,
    ) -> None:
        self._repositorio = repositorio
        self._notificador = notificador

    def ejecutar(self, datos: CrearSuscripcionInput) -> SuscripcionOutput:
        """Da de alta una suscripción nueva.

        Args:
            datos: Email y plan solicitados.

        Returns:
            DTO con la suscripción creada.

        Raises:
            SuscripcionYaExisteError: Si el email ya tiene una suscripción activa.
        """
        existente = self._repositorio.obtener_por_email(datos.email)
        if existente is not None and existente.activa:
            raise SuscripcionYaExisteError(
                f"El email '{datos.email}' ya tiene una suscripción activa"
            )

        suscripcion = Suscripcion(
            email=datos.email,
            plan=datos.plan,
            fecha_alta=date.today(),
        )
        suscripcion = self._repositorio.guardar(suscripcion)
        self._notificador.notificar_alta(suscripcion)

        return SuscripcionOutput(
            id=suscripcion.id,
            email=suscripcion.email,
            plan=suscripcion.plan,
            activa=suscripcion.activa,
            fecha_alta=suscripcion.fecha_alta,
            fecha_baja=suscripcion.fecha_baja,
        )
