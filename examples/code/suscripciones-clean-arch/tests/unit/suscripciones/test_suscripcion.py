"""Tests unitarios de la entity Suscripcion."""

from datetime import date

import pytest

from suscripciones.entities.excepciones import (
    EmailInvalidoError,
    PlanInvalidoError,
    SuscripcionYaCanceladaError,
)
from suscripciones.entities.suscripcion import Suscripcion


class TestCreacion:
    """Tests de creación e invariantes."""

    def test_crea_suscripcion_valida(self):
        suscripcion = Suscripcion(email="ana@example.com", plan="basico", fecha_alta=date.today())

        assert suscripcion.activa is True
        assert suscripcion.fecha_baja is None

    def test_rechaza_email_sin_arroba(self):
        with pytest.raises(EmailInvalidoError):
            Suscripcion(email="ana-example.com", plan="basico", fecha_alta=date.today())

    def test_rechaza_email_vacio(self):
        with pytest.raises(EmailInvalidoError):
            Suscripcion(email="   ", plan="basico", fecha_alta=date.today())

    def test_rechaza_plan_no_soportado(self):
        with pytest.raises(PlanInvalidoError):
            Suscripcion(email="ana@example.com", plan="oro", fecha_alta=date.today())

    @pytest.mark.parametrize("plan", ["basico", "premium"])
    def test_acepta_planes_validos(self, plan):
        suscripcion = Suscripcion(email="ana@example.com", plan=plan, fecha_alta=date.today())
        assert suscripcion.plan == plan


class TestCancelacion:
    """Tests del método cancelar()."""

    def test_cancela_suscripcion_activa(self):
        suscripcion = Suscripcion(email="ana@example.com", plan="basico", fecha_alta=date.today())
        fecha_baja = date.today()

        suscripcion.cancelar(fecha_baja)

        assert suscripcion.activa is False
        assert suscripcion.fecha_baja == fecha_baja

    def test_rechaza_cancelar_dos_veces(self):
        suscripcion = Suscripcion(email="ana@example.com", plan="basico", fecha_alta=date.today())
        suscripcion.cancelar(date.today())

        with pytest.raises(SuscripcionYaCanceladaError):
            suscripcion.cancelar(date.today())
