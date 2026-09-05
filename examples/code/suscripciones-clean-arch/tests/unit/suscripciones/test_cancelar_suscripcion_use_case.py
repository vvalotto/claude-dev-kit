"""Tests unitarios de CancelarSuscripcionUseCase."""

from datetime import date

import pytest

from suscripciones.entities.excepciones import SuscripcionYaCanceladaError
from suscripciones.use_cases.dtos import CancelarSuscripcionInput, CrearSuscripcionInput
from suscripciones.use_cases.excepciones import SuscripcionNoEncontradaError


class TestCancelarSuscripcion:

    def test_cancela_suscripcion_activa(self, crear_use_case, cancelar_use_case, notificador):
        creada = crear_use_case.ejecutar(
            CrearSuscripcionInput(email="ana@example.com", plan="basico")
        )

        resultado = cancelar_use_case.ejecutar(
            CancelarSuscripcionInput(suscripcion_id=creada.id, fecha_baja=date.today())
        )

        assert resultado.activa is False
        assert resultado.fecha_baja == date.today()
        assert len(notificador.bajas) == 1

    def test_rechaza_id_inexistente(self, cancelar_use_case):
        with pytest.raises(SuscripcionNoEncontradaError):
            cancelar_use_case.ejecutar(
                CancelarSuscripcionInput(suscripcion_id=999, fecha_baja=date.today())
            )

    def test_rechaza_cancelar_dos_veces(self, crear_use_case, cancelar_use_case):
        creada = crear_use_case.ejecutar(
            CrearSuscripcionInput(email="ana@example.com", plan="basico")
        )
        cancelar_use_case.ejecutar(
            CancelarSuscripcionInput(suscripcion_id=creada.id, fecha_baja=date.today())
        )

        with pytest.raises(SuscripcionYaCanceladaError):
            cancelar_use_case.ejecutar(
                CancelarSuscripcionInput(suscripcion_id=creada.id, fecha_baja=date.today())
            )
