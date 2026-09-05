"""Controller: traduce input externo a DTOs de UseCase y viceversa.

Solo importa use_cases/ — nunca entities/ ni frameworks/ directamente.
Las excepciones de negocio/aplicación se propagan tal cual; es
responsabilidad de la capa frameworks/ (api_router) traducirlas a
códigos de estado HTTP.
"""

from datetime import date
from typing import Any, Dict

from suscripciones.use_cases.cancelar_suscripcion_use_case import CancelarSuscripcionUseCase
from suscripciones.use_cases.crear_suscripcion_use_case import CrearSuscripcionUseCase
from suscripciones.use_cases.dtos import CancelarSuscripcionInput, CrearSuscripcionInput


class SuscripcionController:
    """Adapta peticiones externas a los UseCases del BC Suscripciones."""

    def __init__(
        self,
        crear_use_case: CrearSuscripcionUseCase,
        cancelar_use_case: CancelarSuscripcionUseCase,
    ) -> None:
        self._crear_use_case = crear_use_case
        self._cancelar_use_case = cancelar_use_case

    def crear(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Da de alta una suscripción a partir de un payload externo."""
        datos = CrearSuscripcionInput(email=payload["email"], plan=payload["plan"])
        resultado = self._crear_use_case.ejecutar(datos)
        return self._a_respuesta(resultado)

    def cancelar(self, suscripcion_id: int) -> Dict[str, Any]:
        """Da de baja una suscripción existente."""
        datos = CancelarSuscripcionInput(
            suscripcion_id=suscripcion_id, fecha_baja=date.today()
        )
        resultado = self._cancelar_use_case.ejecutar(datos)
        return self._a_respuesta(resultado)

    @staticmethod
    def _a_respuesta(resultado) -> Dict[str, Any]:
        return {
            "id": resultado.id,
            "email": resultado.email,
            "plan": resultado.plan,
            "activa": resultado.activa,
            "fecha_alta": resultado.fecha_alta.isoformat(),
            "fecha_baja": resultado.fecha_baja.isoformat() if resultado.fecha_baja else None,
        }
