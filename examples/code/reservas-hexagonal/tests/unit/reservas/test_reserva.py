"""Tests unitarios para el Aggregate Reserva."""

from datetime import date, time, timedelta

import pytest

from reservas.domain.aggregates.reserva import EstadoReserva, Reserva
from reservas.domain.events.reserva_creada import ReservaCreada
from reservas.domain.value_objects.fecha_reserva import FechaReserva
from reservas.domain.value_objects.rango_horario import RangoHorario


def _fecha_futura() -> FechaReserva:
    return FechaReserva(date.today() + timedelta(days=1))


def _horario() -> RangoHorario:
    return RangoHorario(time(10, 0), time(11, 0))


class TestCreacion:
    """Tests de creación e inicialización."""

    def test_crear_reserva_queda_confirmada(self):
        """Verifica que una reserva nueva queda en estado CONFIRMADA."""
        reserva = Reserva.crear(
            recurso_id="mesa-1",
            fecha=_fecha_futura(),
            horario=_horario(),
            cliente_nombre="Ana",
        )

        assert reserva.estado == EstadoReserva.CONFIRMADA
        assert reserva.id is not None

    def test_crear_emite_evento_reserva_creada(self):
        """Verifica que crear() registra un DomainEvent ReservaCreada."""
        reserva = Reserva.crear(
            recurso_id="mesa-1",
            fecha=_fecha_futura(),
            horario=_horario(),
            cliente_nombre="Ana",
        )

        eventos = reserva.eventos_pendientes()

        assert len(eventos) == 1
        assert isinstance(eventos[0], ReservaCreada)
        assert eventos[0].reserva_id == reserva.id

    def test_eventos_pendientes_se_limpian_tras_leerlos(self):
        """Verifica que eventos_pendientes() vacía la lista interna."""
        reserva = Reserva.crear(
            recurso_id="mesa-1",
            fecha=_fecha_futura(),
            horario=_horario(),
            cliente_nombre="Ana",
        )
        reserva.eventos_pendientes()

        assert reserva.eventos_pendientes() == []


class TestValidacion:
    """Tests de validación de datos y errores."""

    def test_rechaza_recurso_id_vacio(self):
        """Verifica que rechaza un recurso_id vacío."""
        with pytest.raises(ValueError):
            Reserva.crear(
                recurso_id="",
                fecha=_fecha_futura(),
                horario=_horario(),
                cliente_nombre="Ana",
            )

    def test_rechaza_cliente_nombre_vacio(self):
        """Verifica que rechaza un cliente_nombre vacío."""
        with pytest.raises(ValueError):
            Reserva.crear(
                recurso_id="mesa-1",
                fecha=_fecha_futura(),
                horario=_horario(),
                cliente_nombre="",
            )


class TestMetodos:
    """Tests de métodos públicos."""

    def test_cancelar_reserva_confirmada(self):
        """Verifica que cancelar() cambia el estado a CANCELADA."""
        reserva = Reserva.crear(
            recurso_id="mesa-1",
            fecha=_fecha_futura(),
            horario=_horario(),
            cliente_nombre="Ana",
        )

        reserva.cancelar()

        assert reserva.estado == EstadoReserva.CANCELADA

    def test_cancelar_reserva_ya_cancelada_falla(self):
        """Verifica que no se puede cancelar dos veces la misma reserva."""
        reserva = Reserva.crear(
            recurso_id="mesa-1",
            fecha=_fecha_futura(),
            horario=_horario(),
            cliente_nombre="Ana",
        )
        reserva.cancelar()

        with pytest.raises(ValueError):
            reserva.cancelar()

    def test_se_solapa_con_misma_fecha_y_horario(self):
        """Verifica que detecta solapamiento con la misma fecha y horario."""
        fecha = _fecha_futura()
        horario = _horario()
        reserva = Reserva.crear(
            recurso_id="mesa-1", fecha=fecha, horario=horario, cliente_nombre="Ana"
        )

        assert reserva.se_solapa_con(fecha, horario) is True

    def test_no_se_solapa_con_fecha_distinta(self):
        """Verifica que no hay solapamiento si la fecha es distinta."""
        reserva = Reserva.crear(
            recurso_id="mesa-1",
            fecha=_fecha_futura(),
            horario=_horario(),
            cliente_nombre="Ana",
        )
        otra_fecha = FechaReserva(date.today() + timedelta(days=2))

        assert reserva.se_solapa_con(otra_fecha, _horario()) is False
