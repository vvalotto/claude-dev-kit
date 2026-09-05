"""Excepciones de orquestación de los UseCases (no de reglas de la entidad)."""


class UseCaseError(Exception):
    """Raíz de las excepciones de aplicación del BC Suscripciones."""


class SuscripcionYaExisteError(UseCaseError):
    """El email ya tiene una suscripción activa."""


class SuscripcionNoEncontradaError(UseCaseError):
    """No existe una suscripción con el id solicitado."""
