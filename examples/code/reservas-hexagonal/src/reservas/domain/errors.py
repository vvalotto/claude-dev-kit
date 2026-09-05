"""Errores de dominio del BC Reservas."""


class ReservaSolapadaError(Exception):
    """Se lanza cuando una nueva reserva se solapa con una existente."""


class ReservaNoEncontradaError(Exception):
    """Se lanza cuando se busca una reserva que no existe."""
