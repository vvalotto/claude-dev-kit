"""Tests unitarios para CrearReservaHandler."""

from datetime import date, time, timedelta

import pytest

from reservas.application.commands.crear_reserva_handler import (
    CrearReservaComando,
    CrearReservaHandler,
)
from reservas.domain.errors import ReservaSolapadaError
from reservas.infrastructure.repositories.reserva_repository_memoria import (
    ReservaRepositoryMemoria,
)


def _comando(**overrides) -> CrearReservaComando:
    defaults = {
        "recurso_id": "mesa-1",
        "fecha": date.today() + timedelta(days=1),
        "hora_inicio": time(10, 0),
        "hora_fin": time(11, 0),
        "cliente_nombre": "Ana",
    }
    defaults.update(overrides)
    return CrearReservaComando(**defaults)


class TestCrearReservaHandler:
    """Tests de creación e inicialización."""

    @pytest.fixture
    def repository(self):
        """Repositorio en memoria limpio para cada test."""
        return ReservaRepositoryMemoria()

    def test_crea_reserva_y_devuelve_id(self, repository):
        """Verifica que handle() persiste la reserva y devuelve su id."""
        handler = CrearReservaHandler(repository)

        reserva_id = handler.handle(_comando())

        assert repository.obtener_por_id(reserva_id) is not None

    def test_rechaza_solapamiento_mismo_recurso_y_horario(self, repository):
        """Verifica que una segunda reserva solapada es rechazada."""
        handler = CrearReservaHandler(repository)
        handler.handle(_comando())

        with pytest.raises(ReservaSolapadaError):
            handler.handle(_comando(cliente_nombre="Otro cliente"))

    def test_permite_mismo_recurso_en_horario_distinto(self, repository):
        """Verifica que el mismo recurso admite reservas sin solapamiento."""
        handler = CrearReservaHandler(repository)
        handler.handle(_comando())

        segundo_id = handler.handle(
            _comando(hora_inicio=time(12, 0), hora_fin=time(13, 0))
        )

        assert repository.obtener_por_id(segundo_id) is not None

    def test_permite_recurso_distinto_mismo_horario(self, repository):
        """Verifica que recursos distintos no compiten por el mismo horario."""
        handler = CrearReservaHandler(repository)
        handler.handle(_comando())

        segundo_id = handler.handle(_comando(recurso_id="mesa-2"))

        assert repository.obtener_por_id(segundo_id) is not None
