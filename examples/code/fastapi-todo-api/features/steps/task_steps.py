"""BDD step definitions for task scenarios."""

import os
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from fastapi.testclient import TestClient
from main import app
from app.database import get_db, TaskDatabase


# Load scenarios from features directory
feature_path = os.path.join(os.path.dirname(__file__), '..', 'tasks.feature')
scenarios(feature_path)


# Fixtures
@pytest.fixture
def context():
    """Shared context for scenarios."""
    return {
        'response': None,
        'task_id': None,
        'db': TaskDatabase()
    }


@pytest.fixture
def client(context):
    """Test client with test database."""
    app.dependency_overrides[get_db] = lambda: context['db']
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


# Given steps
@given("que la API está disponible", target_fixture="api_available")
def api_available(client):
    """Verify API is available."""
    response = client.get("/")
    assert response.status_code == 200
    return True


@given("la base de datos está vacía")
def database_empty(context):
    """Ensure database is empty."""
    context['db'].clear()


@given(parsers.parse('que existe una tarea con:\n{table}'), target_fixture="existing_task")
@given(parsers.parse('que existen las siguientes tareas:\n{table}'))
def create_tasks(client, context, table):
    """Create tasks from table."""
    # Parse table (simple parsing for demo)
    lines = [line.strip() for line in table.split('\n') if '|' in line]
    headers = [h.strip() for h in lines[0].split('|')[1:-1]]

    tasks_created = []
    for line in lines[1:]:
        values = [v.strip() for v in line.split('|')[1:-1]]
        task_data = dict(zip(headers, values))

        # Convert boolean strings
        if 'completed' in task_data:
            task_data['completed'] = task_data['completed'].lower() == 'true'

        # Create task
        response = client.post("/tasks/", json=task_data)
        assert response.status_code == 201
        tasks_created.append(response.json())

    # Store last task_id for single task scenarios
    if len(tasks_created) == 1:
        context['task_id'] = tasks_created[0]['id']

    return tasks_created


# When steps
@when(parsers.parse('se envía una petición {method} a "{endpoint}"'))
def send_request_simple(client, context, method, endpoint):
    """Send HTTP request without body."""
    # Replace {task_id} placeholder
    if '{task_id}' in endpoint:
        endpoint = endpoint.replace('{task_id}', str(context['task_id']))

    if method == "GET":
        context['response'] = client.get(endpoint)
    elif method == "DELETE":
        context['response'] = client.delete(endpoint)


@when(parsers.parse('se envía una petición {method} a "{endpoint}" con:\n{table}'))
def send_request_with_body(client, context, method, endpoint, table):
    """Send HTTP request with body from table."""
    # Replace {task_id} placeholder
    if '{task_id}' in endpoint:
        endpoint = endpoint.replace('{task_id}', str(context['task_id']))

    # Parse table
    lines = [line.strip() for line in table.split('\n') if '|' in line]
    headers = [h.strip() for h in lines[0].split('|')[1:-1]]

    body = {}
    for line in lines[1:]:
        values = [v.strip() for v in line.split('|')[1:-1]]
        for header, value in zip(headers, values):
            # Convert types
            if value.lower() == 'true':
                body[header] = True
            elif value.lower() == 'false':
                body[header] = False
            else:
                body[header] = value

    if method == "POST":
        context['response'] = client.post(endpoint, json=body)
    elif method == "PUT":
        context['response'] = client.put(endpoint, json=body)


# Then steps
@then(parsers.parse("la respuesta tiene código de estado {status:d}"))
def check_status_code(context, status):
    """Verify response status code."""
    assert context['response'].status_code == status


@then(parsers.parse('el JSON de respuesta contiene:\n{table}'))
def check_response_fields(context, table):
    """Verify response contains expected fields."""
    data = context['response'].json()

    # Parse table
    lines = [line.strip() for line in table.split('\n') if '|' in line]
    for line in lines[1:]:
        parts = [p.strip() for p in line.split('|')[1:-1]]
        field, expected = parts[0], parts[1]

        # Convert types
        if expected.lower() == 'true':
            expected = True
        elif expected.lower() == 'false':
            expected = False

        assert field in data, f"Field {field} not in response"
        assert data[field] == expected, f"Field {field}: expected {expected}, got {data[field]}"


@then(parsers.parse('el campo "{field}" es un número mayor que {value:d}'))
def check_field_greater_than(context, field, value):
    """Verify field is greater than value."""
    data = context['response'].json()
    assert field in data
    assert isinstance(data[field], int)
    assert data[field] > value


@then(parsers.parse('el JSON de respuesta es una lista con {count:d} elementos'))
def check_list_length(context, count):
    """Verify response is a list with expected length."""
    data = context['response'].json()
    assert isinstance(data, list)
    assert len(data) == count


@then(parsers.parse('el JSON de respuesta contiene el mensaje "{message}"'))
def check_response_message(context, message):
    """Verify response contains message."""
    data = context['response'].json()
    # Check in detail field (FastAPI error format)
    assert 'detail' in data
    assert message.lower() in data['detail'].lower()


@then("la tarea ya no existe en la base de datos")
def check_task_deleted(client, context):
    """Verify task no longer exists."""
    response = client.get(f"/tasks/{context['task_id']}")
    assert response.status_code == 404
