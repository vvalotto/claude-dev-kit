"""Repository: implementa el Port de persistencia en memoria.

Simplificación deliberada para el tutorial (ver README) — en un proyecto
real esta clase usaría SQLAlchemy async contra PostgreSQL, manteniendo
exactamente la misma interfaz (SuscripcionRepositoryPort).
"""

from typing import Dict, Optional

from suscripciones.entities.suscripcion import Suscripcion
from suscripciones.use_cases.ports.suscripcion_repository_port import SuscripcionRepositoryPort


class MemoriaSuscripcionRepository(SuscripcionRepositoryPort):
    """Repositorio en memoria — traduce entities a un dict interno."""

    def __init__(self) -> None:
        self._suscripciones: Dict[int, Suscripcion] = {}
        self._siguiente_id = 1

    def guardar(self, suscripcion: Suscripcion) -> Suscripcion:
        if suscripcion.id is None:
            suscripcion.id = self._siguiente_id
            self._siguiente_id += 1
        self._suscripciones[suscripcion.id] = suscripcion
        return suscripcion

    def obtener_por_id(self, suscripcion_id: int) -> Optional[Suscripcion]:
        return self._suscripciones.get(suscripcion_id)

    def obtener_por_email(self, email: str) -> Optional[Suscripcion]:
        candidatas = [s for s in self._suscripciones.values() if s.email == email]
        if not candidatas:
            return None
        return max(candidatas, key=lambda s: s.id)

    def limpiar(self) -> None:
        """Vacía el repositorio (uso exclusivo de tests)."""
        self._suscripciones.clear()
        self._siguiente_id = 1
