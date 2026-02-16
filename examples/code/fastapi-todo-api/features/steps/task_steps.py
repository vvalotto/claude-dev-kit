"""BDD step definitions for task scenarios."""

import os
import pytest
from pytest_bdd import scenario, given, when, then, parsers
from fastapi.testclient import TestClient
from main import app
from app.database import get_db, TaskDatabase


# Get absolute path to feature file
FEATURE_FILE = os.path.join(os.path.dirname(__file__), '..', 'tasks.feature')


# Scenario decorators
@scenario(FEATURE_FILE, 'Create a new task')
def test_create_task():
    """Test create task scenario."""
    pass


@scenario(FEATURE_FILE, 'List all tasks')
def test_list_tasks():
    """Test list tasks scenario."""
    pass


@scenario(FEATURE_FILE, 'Get a specific task')
def test_get_task():
    """Test get specific task scenario."""
    pass


@scenario(FEATURE_FILE, 'Update a task')
def test_update_task():
    """Test update task scenario."""
    pass


@scenario(FEATURE_FILE, 'Delete a task')
def test_delete_task():
    """Test delete task scenario."""
    pass


@scenario(FEATURE_FILE, 'Error when getting non-existent task')
def test_get_nonexistent_task():
    """Test error for non-existent task."""
    pass


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
@given("the API is available", target_fixture="api_available")
def api_available(client):
    """Verify API is available."""
    response = client.get("/")
    assert response.status_code == 200
    return True


@given("the database is empty")
def database_empty(context):
    """Ensure database is empty."""
    context['db'].clear()


@given(parsers.re(r'a task exists with:'), target_fixture="existing_task")
@given(parsers.re(r'the following tasks exist:'))
def create_tasks(client, context, datatable):
    """Create tasks from datatable."""
    tasks_created = []

    # Check if this is field/value format or direct columns format
    # field/value format: [[field, value], [title, "Buy milk"], [description, "..."]]
    # direct format: [[title, description], ["Buy milk", "..."]]

    first_row = datatable[0]
    is_field_value_format = first_row[0] == 'field' and len(first_row) >= 2 and first_row[1] == 'value'

    if is_field_value_format:
        # Format: field | value
        # Build a single task from field/value pairs
        task_data = {}
        for row in datatable[1:]:  # Skip header
            if len(row) >= 2:
                field = row[0]
                value = row[1]

                # Convert boolean strings
                if value.lower() == 'true':
                    task_data[field] = True
                elif value.lower() == 'false':
                    task_data[field] = False
                else:
                    task_data[field] = value

        # Create single task
        response = client.post("/tasks/", json=task_data)
        assert response.status_code == 201
        tasks_created.append(response.json())
    else:
        # Format: title | description | ...
        # Multiple tasks with headers
        headers = datatable[0]

        for row in datatable[1:]:  # Skip headers
            task_data = {}
            for i, header in enumerate(headers):
                if i < len(row):
                    value = row[i]

                    # Convert boolean strings
                    if value.lower() == 'true':
                        task_data[header] = True
                    elif value.lower() == 'false':
                        task_data[header] = False
                    else:
                        task_data[header] = value

            # Create task
            response = client.post("/tasks/", json=task_data)
            assert response.status_code == 201
            tasks_created.append(response.json())

    # Store last task_id for single task scenarios
    if len(tasks_created) == 1:
        context['task_id'] = tasks_created[0]['id']

    return tasks_created


# When steps
@when(parsers.re(r'a (?P<method>GET|POST|PUT|DELETE) request is sent to "(?P<endpoint>[^"]+)"'))
def send_request_simple(client, context, method, endpoint):
    """Send HTTP request without body."""
    # Replace {task_id} placeholder
    if '{task_id}' in endpoint:
        endpoint = endpoint.replace('{task_id}', str(context['task_id']))

    if method == "GET":
        context['response'] = client.get(endpoint)
    elif method == "DELETE":
        context['response'] = client.delete(endpoint)


@when(parsers.re(r'a (?P<method>POST|PUT) request is sent to "(?P<endpoint>[^"]+)" with:'))
def send_request_with_body(client, context, method, endpoint, datatable):
    """Send HTTP request with body from datatable."""
    # Replace {task_id} placeholder
    if '{task_id}' in endpoint:
        endpoint = endpoint.replace('{task_id}', str(context['task_id']))

    # Parse table - datatable is a list of lists [[header1, header2], [val1, val2], ...]
    # But we want to build a body from field/value pairs
    body = {}
    for row in datatable:
        # Each row should have a 'field' and 'value'
        # row is like ['title', 'Buy milk'] or ['description', 'Go to supermarket']
        if len(row) >= 2:
            field = row[0]
            value = row[1]

            # Skip header row
            if field == 'field':
                continue

            # Convert types
            if value.lower() == 'true':
                body[field] = True
            elif value.lower() == 'false':
                body[field] = False
            else:
                body[field] = value

    if method == "POST":
        context['response'] = client.post(endpoint, json=body)
    elif method == "PUT":
        context['response'] = client.put(endpoint, json=body)


# Then steps
@then(parsers.parse("the response status code is {status:d}"))
def check_status_code(context, status):
    """Verify response status code."""
    assert context['response'].status_code == status


@then(parsers.re(r'the response JSON contains:'))
def check_response_fields(context, datatable):
    """Verify response contains expected fields."""
    data = context['response'].json()

    # datatable is a list of lists [[header1, header2], [val1, val2], ...]
    headers = datatable[0]  # First row is headers

    for row in datatable[1:]:  # Skip headers
        field = row[0]  # First column is field name
        expected = row[1]  # Second column is expected value

        # Convert types
        if expected.lower() == 'true':
            expected = True
        elif expected.lower() == 'false':
            expected = False

        assert field in data, f"Field {field} not in response"
        assert data[field] == expected, f"Field {field}: expected {expected}, got {data[field]}"


@then(parsers.parse('the field "{field}" is a number greater than {value:d}'))
def check_field_greater_than(context, field, value):
    """Verify field is greater than value."""
    data = context['response'].json()
    assert field in data
    assert isinstance(data[field], int)
    assert data[field] > value


@then(parsers.parse('the response is a list with {count:d} items'))
def check_list_length(context, count):
    """Verify response is a list with expected length."""
    data = context['response'].json()
    assert isinstance(data, list)
    assert len(data) == count


@then(parsers.parse('the response JSON contains the message "{message}"'))
def check_response_message(context, message):
    """Verify response contains message."""
    data = context['response'].json()
    # Check in detail field (FastAPI error format)
    assert 'detail' in data
    assert message.lower() in data['detail'].lower()


@then("the task no longer exists in the database")
def check_task_deleted(client, context):
    """Verify task no longer exists."""
    response = client.get(f"/tasks/{context['task_id']}")
    assert response.status_code == 404
