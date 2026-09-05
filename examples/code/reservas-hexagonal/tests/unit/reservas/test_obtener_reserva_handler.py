"""Tests unitarios para ObtenerReservaHandler."""

from datetime import date, time, timedelta

import pytest

from reservas.application.commands.crear_reserva_handler import (
    CrearReservaComando,
    CrearReservaHandler,
)
from reservas.application.queries.obtener_reserva_handler import (
    ObtenerReservaHandler,
    ObtenerReservaQuery,
)
from reservas.infrastructure.repositories.reserva_repository_memoria import (
    ReservaRepositoryMemoria,
)


class TestObtenerReservaHandler:
    """Tests de la query ObtenerReservaHandler."""

    @pytest.fixture
    def repository(self):
        """Repositorio en memoria limpio para cada test."""
        return ReservaRepositoryMemoria()

    def test_devuelve_dto_de_reserva_existente(self, repository):
        """Verifica que devuelve un ReservaDTO con los datos correctos."""
        crear_handler = CrearReservaHandler(repository)
        reserva_id = crear_handler.handle(
            CrearReservaComando(
                recurso_id="mesa-1",
                fecha=date.today() + timedelta(days=1),
                hora_inicio=time(10, 0),
                hora_fin=time(11, 0),
                cliente_nombre="Ana",
            )
        )

        handler = ObtenerReservaHandler(repository)
        dto = handler.handle(ObtenerReservaQuery(reserva_id=reserva_id))

        assert dto is not None
        assert dto.id == reserva_id
        assert dto.recurso_id == "mesa-1"
        assert dto.cliente_nombre == "Ana"

    def test_devuelve_none_si_no_existe(self, repository):
        """Verifica que devuelve None cuando la reserva no existe."""
        handler = ObtenerReservaHandler(repository)

        dto = handler.handle(ObtenerReservaQuery(reserva_id="no-existe"))

        assert dto is None
