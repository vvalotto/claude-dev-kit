"""Tests de integración para ReservaRepositoryMemoria + Reserva real."""

from datetime import date, time, timedelta

import pytest

from reservas.domain.aggregates.reserva import Reserva
from reservas.domain.value_objects.fecha_reserva import FechaReserva
from reservas.domain.value_objects.rango_horario import RangoHorario
from reservas.infrastructure.repositories.reserva_repository_memoria import (
    ReservaRepositoryMemoria,
)


@pytest.fixture
def repository():
    """Repositorio en memoria limpio."""
    return ReservaRepositoryMemoria()


def _fecha_futura() -> FechaReserva:
    return FechaReserva(date.today() + timedelta(days=1))


class TestFlujoGuardarYRecuperar:
    """Verifica que el repositorio persiste y devuelve aggregates reales."""

    def test_guardar_y_obtener_por_id(self, repository):
        """Verifica que una reserva guardada se recupera intacta por su id."""
        reserva = Reserva.crear(
            recurso_id="mesa-1",
            fecha=_fecha_futura(),
            horario=RangoHorario(time(10, 0), time(11, 0)),
            cliente_nombre="Ana",
        )

        repository.guardar(reserva)
        recuperada = repository.obtener_por_id(reserva.id)

        assert recuperada is not None
        assert recuperada.cliente_nombre == "Ana"
        assert recuperada.recurso_id == "mesa-1"

    def test_existe_solapamiento_detecta_conflicto_real(self, repository):
        """Verifica la detección de solapamiento contra datos ya persistidos."""
        reserva = Reserva.crear(
            recurso_id="mesa-1",
            fecha=_fecha_futura(),
            horario=RangoHorario(time(10, 0), time(11, 0)),
            cliente_nombre="Ana",
        )
        repository.guardar(reserva)

        hay_solapamiento = repository.existe_solapamiento(
            "mesa-1", _fecha_futura(), RangoHorario(time(10, 30), time(11, 30))
        )

        assert hay_solapamiento is True

    def test_existe_solapamiento_ignora_reservas_canceladas(self, repository):
        """Una reserva cancelada no debe bloquear el mismo horario."""
        reserva = Reserva.crear(
            recurso_id="mesa-1",
            fecha=_fecha_futura(),
            horario=RangoHorario(time(10, 0), time(11, 0)),
            cliente_nombre="Ana",
        )
        reserva.cancelar()
        repository.guardar(reserva)

        hay_solapamiento = repository.existe_solapamiento(
            "mesa-1", _fecha_futura(), RangoHorario(time(10, 0), time(11, 0))
        )

        assert hay_solapamiento is False
