# Template: Test de Integración
# Estructura estándar de tests de integración - framework agnostic
#
# Diferencia con test-unit.py.tpl: valida componentes trabajando juntos,
# con dependencias reales o parcialmente mockeadas (no todo aislado con mocks).

"""
Tests de integración para {FLOW_NAME}.

{TEST_FLOW_DESCRIPTION_COMMENT}
"""

import pytest
{SNIPPET:test_imports}

from {MODULE_PATH} import {CLASS_NAME}


class TestFlujo{FLOW_NAME}:
    """Tests de integración del flujo {FLOW_NAME}."""

    @pytest.fixture
    def contexto_integrado(self):
        """Fixture que arma el conjunto de componentes reales del flujo."""
        # Instanciar componentes reales (no mocks) que colaboran en el flujo
        return {CLASS_NAME}()

    def test_flujo_completo_camino_feliz(self, contexto_integrado):
        """Verifica que el flujo completo produce el resultado esperado."""
        resultado = contexto_integrado.ejecutar_flujo()

        assert resultado == valor_esperado

    def test_flujo_propaga_cambios_entre_componentes(self, contexto_integrado):
        """Verifica que un cambio en un componente se refleja en los demás."""
        contexto_integrado.componente_a.actualizar()

        assert contexto_integrado.componente_b.reaccionó()

    def test_flujo_maneja_dependencia_externa_fallando(self, contexto_integrado):
        """Verifica comportamiento cuando una dependencia externa falla."""
        # Mockear solo el borde externo (DB, API, servidor) — no el flujo interno
        with pytest.raises(Exception):
            contexto_integrado.ejecutar_flujo_con_dependencia_caida()


{SNIPPET:test_integration_fixtures}
