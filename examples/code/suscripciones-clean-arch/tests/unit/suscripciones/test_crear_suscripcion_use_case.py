"""Tests unitarios de CrearSuscripcionUseCase.

Usa fakes de los Ports (ver conftest.py), no la implementación real de
frameworks/, para mantener el test unitario aislado de infraestructura.
"""

from datetime import date

import pytest

from suscripciones.use_cases.dtos import CrearSuscripcionInput
from suscripciones.use_cases.excepciones import SuscripcionYaExisteError


class TestCrearSuscripcion:

    def test_crea_suscripcion_nueva(self, crear_use_case, notificador):
        resultado = crear_use_case.ejecutar(
            CrearSuscripcionInput(email="ana@example.com", plan="basico")
        )

        assert resultado.id == 1
        assert resultado.email == "ana@example.com"
        assert resultado.activa is True
        assert resultado.fecha_alta == date.today()
        assert len(notificador.altas) == 1

    def test_rechaza_email_duplicado_activo(self, crear_use_case):
        crear_use_case.ejecutar(CrearSuscripcionInput(email="ana@example.com", plan="basico"))

        with pytest.raises(SuscripcionYaExisteError):
            crear_use_case.ejecutar(CrearSuscripcionInput(email="ana@example.com", plan="premium"))

    def test_permite_reactivar_email_con_suscripcion_cancelada(
        self, crear_use_case, repositorio
    ):
        primera = crear_use_case.ejecutar(
            CrearSuscripcionInput(email="ana@example.com", plan="basico")
        )
        suscripcion = repositorio.obtener_por_id(primera.id)
        suscripcion.cancelar(date.today())
        repositorio.guardar(suscripcion)

        nueva = crear_use_case.ejecutar(
            CrearSuscripcionInput(email="ana@example.com", plan="premium")
        )

        assert nueva.id != primera.id
        assert nueva.activa is True
