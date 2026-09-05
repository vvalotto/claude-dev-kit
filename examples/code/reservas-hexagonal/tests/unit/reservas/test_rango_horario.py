"""Tests unitarios para RangoHorario."""

from datetime import time

import pytest

from reservas.domain.value_objects.rango_horario import RangoHorario


class TestCreacion:
    """Tests de creación e inicialización."""

    def test_crear_rango_valido(self):
        """Verifica que se crea con hora_fin posterior a hora_inicio."""
        rango = RangoHorario(time(10, 0), time(11, 0))

        assert rango.hora_inicio == time(10, 0)
        assert rango.hora_fin == time(11, 0)


class TestValidacion:
    """Tests de validación de datos y errores."""

    def test_rechaza_hora_fin_igual_a_inicio(self):
        """Verifica que rechaza un rango de duración cero."""
        with pytest.raises(ValueError):
            RangoHorario(time(10, 0), time(10, 0))

    def test_rechaza_hora_fin_anterior_a_inicio(self):
        """Verifica que rechaza un rango invertido."""
        with pytest.raises(ValueError):
            RangoHorario(time(11, 0), time(10, 0))


class TestSolapamiento:
    """Tests del método se_solapa_con."""

    def test_rangos_identicos_se_solapan(self):
        """Dos rangos idénticos se solapan."""
        rango = RangoHorario(time(10, 0), time(11, 0))

        assert rango.se_solapa_con(RangoHorario(time(10, 0), time(11, 0))) is True

    def test_rangos_parcialmente_superpuestos_se_solapan(self):
        """Rangos que se cruzan parcialmente se solapan."""
        rango = RangoHorario(time(10, 0), time(11, 0))

        assert rango.se_solapa_con(RangoHorario(time(10, 30), time(12, 0))) is True

    def test_rangos_consecutivos_no_se_solapan(self):
        """Un rango que empieza justo cuando termina el otro no se solapa."""
        rango = RangoHorario(time(10, 0), time(11, 0))

        assert rango.se_solapa_con(RangoHorario(time(11, 0), time(12, 0))) is False

    def test_rangos_disjuntos_no_se_solapan(self):
        """Rangos sin ninguna intersección no se solapan."""
        rango = RangoHorario(time(9, 0), time(10, 0))

        assert rango.se_solapa_con(RangoHorario(time(14, 0), time(15, 0))) is False
