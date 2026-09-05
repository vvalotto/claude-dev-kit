"""Fakes de los Ports y fixtures compartidas por los tests unitarios de UseCases."""

from typing import Dict, List, Optional

import pytest

from suscripciones.entities.suscripcion import Suscripcion
from suscripciones.use_cases.cancelar_suscripcion_use_case import CancelarSuscripcionUseCase
from suscripciones.use_cases.crear_suscripcion_use_case import CrearSuscripcionUseCase
from suscripciones.use_cases.ports.notificacion_gateway_port import NotificacionGatewayPort
from suscripciones.use_cases.ports.suscripcion_repository_port import SuscripcionRepositoryPort


class FakeRepositorio(SuscripcionRepositoryPort):
    """Fake en memoria del Port de persistencia, para tests unitarios."""

    def __init__(self):
        self._data: Dict[int, Suscripcion] = {}
        self._next_id = 1

    def guardar(self, suscripcion: Suscripcion) -> Suscripcion:
        if suscripcion.id is None:
            suscripcion.id = self._next_id
            self._next_id += 1
        self._data[suscripcion.id] = suscripcion
        return suscripcion

    def obtener_por_id(self, suscripcion_id: int) -> Optional[Suscripcion]:
        return self._data.get(suscripcion_id)

    def obtener_por_email(self, email: str) -> Optional[Suscripcion]:
        for suscripcion in self._data.values():
            if suscripcion.email == email:
                return suscripcion
        return None


class FakeNotificador(NotificacionGatewayPort):
    """Fake del Port de notificaciones — registra las llamadas recibidas."""

    def __init__(self):
        self.altas: List[Suscripcion] = []
        self.bajas: List[Suscripcion] = []

    def notificar_alta(self, suscripcion: Suscripcion) -> None:
        self.altas.append(suscripcion)

    def notificar_baja(self, suscripcion: Suscripcion) -> None:
        self.bajas.append(suscripcion)


@pytest.fixture
def repositorio():
    return FakeRepositorio()


@pytest.fixture
def notificador():
    return FakeNotificador()


@pytest.fixture
def crear_use_case(repositorio, notificador):
    return CrearSuscripcionUseCase(repositorio, notificador)


@pytest.fixture
def cancelar_use_case(repositorio, notificador):
    return CancelarSuscripcionUseCase(repositorio, notificador)
