"""Tests unitarios para FechaReserva."""

from datetime import date, timedelta

import pytest

from reservas.domain.value_objects.fecha_reserva import FechaReserva


class TestCreacion:
    """Tests de creación e inicialización."""

    def test_crear_con_fecha_futura(self):
        """Verifica que se crea correctamente con una fecha futura."""
        manana = date.today() + timedelta(days=1)
        fecha = FechaReserva(manana)

        assert fecha.valor == manana

    def test_crear_con_hoy(self):
        """Verifica que acepta la fecha de hoy."""
        fecha = FechaReserva(date.today())

        assert fecha.es_hoy() is True


class TestValidacion:
    """Tests de validación de datos y errores."""

    def test_rechaza_fecha_pasada(self):
        """Verifica que una fecha pasada es rechazada."""
        ayer = date.today() - timedelta(days=1)

        with pytest.raises(ValueError):
            FechaReserva(ayer)


class TestIgualdad:
    """Tests de igualdad por valor."""

    def test_dos_fechas_iguales_son_iguales(self):
        """Verifica igualdad por valor, no por identidad."""
        manana = date.today() + timedelta(days=1)

        assert FechaReserva(manana) == FechaReserva(manana)

    def test_str_representa_iso(self):
        """Verifica que __str__ devuelve formato ISO."""
        manana = date.today() + timedelta(days=1)

        assert str(FechaReserva(manana)) == manana.isoformat()
