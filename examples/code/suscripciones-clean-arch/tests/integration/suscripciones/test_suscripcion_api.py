"""Tests de integración: flujo completo HTTP -> Controller -> UseCase -> Repository."""

import main


class TestAltaSuscripcion:

    def test_crear_suscripcion_devuelve_201(self, client):
        response = client.post(
            "/suscripciones", json={"email": "ana@example.com", "plan": "basico"}
        )

        assert response.status_code == 201
        body = response.json()
        assert body["email"] == "ana@example.com"
        assert body["activa"] is True

    def test_crear_suscripcion_duplicada_devuelve_409(self, client):
        client.post("/suscripciones", json={"email": "ana@example.com", "plan": "basico"})

        response = client.post(
            "/suscripciones", json={"email": "ana@example.com", "plan": "premium"}
        )

        assert response.status_code == 409

    def test_crear_suscripcion_plan_invalido_devuelve_422(self, client):
        response = client.post(
            "/suscripciones", json={"email": "ana@example.com", "plan": "oro"}
        )

        assert response.status_code == 422

    def test_crear_suscripcion_notifica_alta(self, client):
        client.post("/suscripciones", json={"email": "ana@example.com", "plan": "basico"})

        assert len(main.notificador.enviadas) == 1
        assert "ALTA" in main.notificador.enviadas[0]


class TestBajaSuscripcion:

    def test_cancelar_suscripcion_devuelve_200(self, client):
        creada = client.post(
            "/suscripciones", json={"email": "ana@example.com", "plan": "basico"}
        ).json()

        response = client.post(f"/suscripciones/{creada['id']}/cancelar")

        assert response.status_code == 200
        assert response.json()["activa"] is False

    def test_cancelar_suscripcion_inexistente_devuelve_404(self, client):
        response = client.post("/suscripciones/999/cancelar")

        assert response.status_code == 404

    def test_cancelar_suscripcion_dos_veces_devuelve_409(self, client):
        creada = client.post(
            "/suscripciones", json={"email": "ana@example.com", "plan": "basico"}
        ).json()
        client.post(f"/suscripciones/{creada['id']}/cancelar")

        response = client.post(f"/suscripciones/{creada['id']}/cancelar")

        assert response.status_code == 409
