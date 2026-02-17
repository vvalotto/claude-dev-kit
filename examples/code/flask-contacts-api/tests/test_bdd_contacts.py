"""BDD tests for contact scenarios."""

import json
from pathlib import Path
from pytest_bdd import scenarios, given, when, then, parsers
from app import create_app
from app.database import reset_db


# Load all scenarios from contacts.feature
FEATURE_FILE = Path(__file__).parent.parent / 'features' / 'contacts.feature'
scenarios(str(FEATURE_FILE))


# --- GIVEN STEPS ---

@given('que la API está corriendo', target_fixture='api_client')
def api_is_running():
    """Initialize API client."""
    app = create_app()
    app.config['TESTING'] = True
    return app.test_client()


@given('que la base de datos está vacía')
def database_is_empty():
    """Reset database to empty state."""
    reset_db()


@given(parsers.parse('que existe un contacto con nombre "{nombre}" email "{email}" telefono "{telefono}"'),
       target_fixture='created_contact_id')
def create_contact(api_client, nombre, email, telefono):
    """Create a contact."""
    contact = {
        'nombre': nombre,
        'email': email,
        'telefono': telefono
    }

    response = api_client.post(
        '/contacts',
        data=json.dumps(contact),
        content_type='application/json'
    )

    if response.status_code == 201:
        data = json.loads(response.data)
        return data['id']
    return None


@given('que guardo el ID del contacto creado', target_fixture='saved_contact_id')
def save_contact_id(created_contact_id):
    """Save the created contact ID for later use."""
    return created_contact_id


# --- WHEN STEPS ---

@when(parsers.parse('creo un contacto con nombre "{nombre}" email "{email}" telefono "{telefono}"'),
      target_fixture='api_response')
def create_contact_when(api_client, nombre, email, telefono):
    """Send POST request to create contact."""
    contact = {
        'nombre': nombre,
        'email': email,
        'telefono': telefono
    }

    response = api_client.post(
        '/contacts',
        data=json.dumps(contact),
        content_type='application/json'
    )

    return response


@when('obtengo todos los contactos', target_fixture='api_response')
def get_all_contacts(api_client):
    """Send GET request for all contacts."""
    response = api_client.get('/contacts')
    return response


@when('obtengo el contacto por ID guardado', target_fixture='api_response')
def get_contact_by_saved_id(api_client, saved_contact_id):
    """Send GET request for specific contact ID."""
    response = api_client.get(f'/contacts/{saved_contact_id}')
    return response


@when(parsers.parse('obtengo el contacto con ID {contact_id:d}'),
      target_fixture='api_response')
def get_contact_by_id(api_client, contact_id):
    """Send GET request for specific contact ID."""
    response = api_client.get(f'/contacts/{contact_id}')
    return response


@when(parsers.parse('actualizo el contacto guardado con nombre "{nombre}" email "{email}" telefono "{telefono}"'),
      target_fixture='api_response')
def update_saved_contact(api_client, saved_contact_id, nombre, email, telefono):
    """Send PUT request to update saved contact."""
    contact = {
        'nombre': nombre,
        'email': email,
        'telefono': telefono
    }

    response = api_client.put(
        f'/contacts/{saved_contact_id}',
        data=json.dumps(contact),
        content_type='application/json'
    )

    return response


@when(parsers.parse('actualizo el contacto {contact_id:d} con nombre "{nombre}" email "{email}" telefono "{telefono}"'),
      target_fixture='api_response')
def update_contact_by_id(api_client, contact_id, nombre, email, telefono):
    """Send PUT request to update contact."""
    contact = {
        'nombre': nombre,
        'email': email,
        'telefono': telefono
    }

    response = api_client.put(
        f'/contacts/{contact_id}',
        data=json.dumps(contact),
        content_type='application/json'
    )

    return response


@when('elimino el contacto guardado', target_fixture='api_response')
def delete_saved_contact(api_client, saved_contact_id):
    """Send DELETE request for saved contact."""
    response = api_client.delete(f'/contacts/{saved_contact_id}')
    return response


@when(parsers.parse('elimino el contacto con ID {contact_id:d}'),
      target_fixture='api_response')
def delete_contact_by_id(api_client, contact_id):
    """Send DELETE request for specific contact ID."""
    response = api_client.delete(f'/contacts/{contact_id}')
    return response


@when('intento obtener el contacto eliminado',
      target_fixture='api_response')
def try_get_deleted_contact(api_client, saved_contact_id):
    """Try to get a deleted contact."""
    response = api_client.get(f'/contacts/{saved_contact_id}')
    return response


@when('creo un contacto sin email',
      target_fixture='api_response')
def create_contact_without_email(api_client):
    """Send POST request to create contact without email."""
    contact = {
        'nombre': 'Sin Email',
        'telefono': '555-0000'
    }

    response = api_client.post(
        '/contacts',
        data=json.dumps(contact),
        content_type='application/json'
    )

    return response


# --- THEN STEPS ---

@then(parsers.parse('recibo un código de estado {status_code:d}'))
def check_status_code(api_response, status_code):
    """Check response status code."""
    assert api_response.status_code == status_code, \
        f"Expected {status_code}, got {api_response.status_code}"


@then('la respuesta contiene un campo "id"')
def check_has_id_field(api_response):
    """Check response has id field."""
    data = json.loads(api_response.data)
    assert 'id' in data, "Response should contain 'id' field"


@then('la respuesta contiene un campo "error"')
def check_has_error_field(api_response):
    """Check response has error field."""
    # For 204 No Content, there's no body
    if api_response.status_code == 204:
        return
    data = json.loads(api_response.data)
    assert 'error' in data, "Response should contain 'error' field"


@then(parsers.parse('el campo "{field}" es "{value}"'))
def check_field_value(api_response, field, value):
    """Check field has expected value."""
    data = json.loads(api_response.data)
    assert data[field] == value, \
        f"Expected {field}='{value}', got '{data[field]}'"


@then(parsers.parse('la respuesta es una lista con {count:d} contactos'))
def check_list_count(api_response, count):
    """Check response is a list with expected count."""
    data = json.loads(api_response.data)
    assert isinstance(data, list), "Response should be a list"
    assert len(data) == count, \
        f"Expected {count} contacts, got {len(data)}"


@then(parsers.parse('la lista contiene un contacto con nombre "{nombre}"'))
def check_list_contains_name(api_response, nombre):
    """Check list contains contact with specific name."""
    data = json.loads(api_response.data)
    nombres = [contact['nombre'] for contact in data]
    assert nombre in nombres, \
        f"Expected to find '{nombre}' in {nombres}"


@then('el mensaje de error menciona "email"')
def check_error_mentions_email(api_response):
    """Check error message mentions email."""
    data = json.loads(api_response.data)
    error_msg = data.get('error', '').lower()
    assert 'email' in error_msg, \
        f"Error message should mention 'email': {error_msg}"
