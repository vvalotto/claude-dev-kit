"""BDD step definitions for subscription scenarios."""

import os

import pytest
from pytest_bdd import given, parsers, scenario, then, when

FEATURE_FILE = os.path.join(os.path.dirname(__file__), "..", "suscripciones.feature")


@scenario(FEATURE_FILE, "Create a new subscription")
def test_create_subscription():
    """Test create subscription scenario."""


@scenario(FEATURE_FILE, "Reject a duplicate active subscription")
def test_reject_duplicate_subscription():
    """Test rejecting a duplicate active subscription."""


@scenario(FEATURE_FILE, "Cancel an existing subscription")
def test_cancel_subscription():
    """Test cancel subscription scenario."""


@scenario(FEATURE_FILE, "Reject cancelling a non-existent subscription")
def test_reject_cancel_nonexistent():
    """Test rejecting the cancellation of a non-existent subscription."""


@pytest.fixture
def context():
    """Shared context between steps of a scenario."""
    return {"response": None}


@given("the API is available", target_fixture="context")
def api_available(client, context):
    response = client.get("/")
    assert response.status_code == 200
    return context


@given(parsers.parse('a subscription exists for "{email}" with plan "{plan}"'), target_fixture="context")
def subscription_exists(client, context, email, plan):
    response = client.post("/suscripciones", json={"email": email, "plan": plan})
    assert response.status_code == 201
    context["subscription_id"] = response.json()["id"]
    return context


@when(parsers.parse('a subscription is created for "{email}" with plan "{plan}"'))
def create_subscription(client, context, email, plan):
    context["response"] = client.post("/suscripciones", json={"email": email, "plan": plan})


@when("the subscription is cancelled")
def cancel_subscription(client, context):
    context["response"] = client.post(f"/suscripciones/{context['subscription_id']}/cancelar")


@when(parsers.parse('subscription "{subscription_id}" is cancelled'))
def cancel_subscription_by_id(client, context, subscription_id):
    context["response"] = client.post(f"/suscripciones/{subscription_id}/cancelar")


@then(parsers.parse("the response status code is {status:d}"))
def check_status_code(context, status):
    assert context["response"].status_code == status


@then("the subscription is active")
def check_active(context):
    assert context["response"].json()["activa"] is True


@then("the subscription is not active")
def check_not_active(context):
    assert context["response"].json()["activa"] is False
