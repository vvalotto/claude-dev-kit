"""Excepciones de reglas de negocio de la entidad Suscripcion."""


class SuscripcionError(Exception):
    """Raíz de las excepciones de negocio del BC Suscripciones."""


class PlanInvalidoError(SuscripcionError):
    """Se intentó crear una suscripción con un plan no soportado."""


class EmailInvalidoError(SuscripcionError):
    """El email provisto no tiene un formato válido."""


class SuscripcionYaCanceladaError(SuscripcionError):
    """Se intentó cancelar una suscripción que ya estaba cancelada."""
