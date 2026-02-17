"""Integration tests for REST API endpoints."""

import pytest
import json


class TestContactEndpoints:
    """Test suite for contact API endpoints."""

    def test_get_contacts_empty(self, client):
        """Test GET /contacts when database is empty."""
        response = client.get('/contacts')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []

    def test_create_contact_valid(self, client, sample_contact_dict):
        """Test POST /contacts with valid data."""
        response = client.post(
            '/contacts',
            data=json.dumps(sample_contact_dict),
            content_type='application/json'
        )

        assert response.status_code == 201
        data = json.loads(response.data)
        assert 'id' in data
        assert data['nombre'] == 'Juan Pérez'
        assert data['email'] == 'juan.perez@email.com'
        assert data['telefono'] == '555-1234'

    def test_create_contact_invalid_email(self, client):
        """Test POST /contacts with invalid email."""
        invalid_contact = {
            'nombre': 'Test User',
            'email': 'invalid-email',
            'telefono': '555-0000'
        }

        response = client.post(
            '/contacts',
            data=json.dumps(invalid_contact),
            content_type='application/json'
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'email' in data['error'].lower()

    def test_create_contact_missing_fields(self, client):
        """Test POST /contacts with missing required fields."""
        incomplete_contact = {
            'nombre': 'Test User'
            # Missing email and telefono
        }

        response = client.post(
            '/contacts',
            data=json.dumps(incomplete_contact),
            content_type='application/json'
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_get_contacts_after_create(self, client, sample_contact_dict):
        """Test GET /contacts after creating contacts."""
        # Create first contact
        client.post(
            '/contacts',
            data=json.dumps(sample_contact_dict),
            content_type='application/json'
        )

        # Create second contact
        second_contact = {
            'nombre': 'María García',
            'email': 'maria.garcia@email.com',
            'telefono': '555-5678'
        }
        client.post(
            '/contacts',
            data=json.dumps(second_contact),
            content_type='application/json'
        )

        # Get all contacts
        response = client.get('/contacts')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 2
        assert data[0]['nombre'] == 'Juan Pérez'
        assert data[1]['nombre'] == 'María García'

    def test_get_contact_by_id_exists(self, client, sample_contact_dict):
        """Test GET /contacts/<id> when contact exists."""
        # Create contact
        create_response = client.post(
            '/contacts',
            data=json.dumps(sample_contact_dict),
            content_type='application/json'
        )
        created_data = json.loads(create_response.data)
        contact_id = created_data['id']

        # Get contact by ID
        response = client.get(f'/contacts/{contact_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['id'] == contact_id
        assert data['nombre'] == 'Juan Pérez'

    def test_get_contact_by_id_not_exists(self, client):
        """Test GET /contacts/<id> when contact doesn't exist."""
        response = client.get('/contacts/999')

        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data

    def test_update_contact_exists(self, client, sample_contact_dict):
        """Test PUT /contacts/<id> when contact exists."""
        # Create contact
        create_response = client.post(
            '/contacts',
            data=json.dumps(sample_contact_dict),
            content_type='application/json'
        )
        created_data = json.loads(create_response.data)
        contact_id = created_data['id']

        # Update contact
        update_data = {
            'nombre': 'Juan Pérez García',
            'email': 'juan.nuevo@email.com',
            'telefono': '555-9999'
        }
        response = client.put(
            f'/contacts/{contact_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['id'] == contact_id
        assert data['nombre'] == 'Juan Pérez García'
        assert data['email'] == 'juan.nuevo@email.com'
        assert data['telefono'] == '555-9999'

    def test_update_contact_not_exists(self, client):
        """Test PUT /contacts/<id> when contact doesn't exist."""
        update_data = {
            'nombre': 'Fantasma',
            'email': 'fantasma@email.com',
            'telefono': '555-0000'
        }

        response = client.put(
            '/contacts/999',
            data=json.dumps(update_data),
            content_type='application/json'
        )

        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data

    def test_update_contact_partial(self, client, sample_contact_dict):
        """Test PUT /contacts/<id> with partial data (only some fields)."""
        # Create contact
        create_response = client.post(
            '/contacts',
            data=json.dumps(sample_contact_dict),
            content_type='application/json'
        )
        created_data = json.loads(create_response.data)
        contact_id = created_data['id']

        # Partial update (only telefono)
        update_data = {
            'telefono': '555-7777'
        }
        response = client.put(
            f'/contacts/{contact_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['nombre'] == 'Juan Pérez'  # Unchanged
        assert data['email'] == 'juan.perez@email.com'  # Unchanged
        assert data['telefono'] == '555-7777'  # Changed

    def test_delete_contact_exists(self, client, sample_contact_dict):
        """Test DELETE /contacts/<id> when contact exists."""
        # Create contact
        create_response = client.post(
            '/contacts',
            data=json.dumps(sample_contact_dict),
            content_type='application/json'
        )
        created_data = json.loads(create_response.data)
        contact_id = created_data['id']

        # Delete contact
        response = client.delete(f'/contacts/{contact_id}')
        assert response.status_code == 204

        # Verify deletion
        get_response = client.get(f'/contacts/{contact_id}')
        assert get_response.status_code == 404

    def test_delete_contact_not_exists(self, client):
        """Test DELETE /contacts/<id> when contact doesn't exist."""
        response = client.delete('/contacts/999')

        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data

    def test_full_crud_workflow(self, client):
        """Test complete CRUD workflow: Create, Read, Update, Delete."""
        # Create
        create_data = {
            'nombre': 'Ana Martínez',
            'email': 'ana.martinez@email.com',
            'telefono': '555-3456'
        }
        create_response = client.post(
            '/contacts',
            data=json.dumps(create_data),
            content_type='application/json'
        )
        assert create_response.status_code == 201
        contact_id = json.loads(create_response.data)['id']

        # Read (by ID)
        read_response = client.get(f'/contacts/{contact_id}')
        assert read_response.status_code == 200
        assert json.loads(read_response.data)['nombre'] == 'Ana Martínez'

        # Read (all)
        list_response = client.get('/contacts')
        assert list_response.status_code == 200
        assert len(json.loads(list_response.data)) == 1

        # Update
        update_data = {
            'nombre': 'Ana Martínez López',
            'telefono': '555-8888'
        }
        update_response = client.put(
            f'/contacts/{contact_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        assert update_response.status_code == 200
        updated_data = json.loads(update_response.data)
        assert updated_data['nombre'] == 'Ana Martínez López'
        assert updated_data['telefono'] == '555-8888'

        # Delete
        delete_response = client.delete(f'/contacts/{contact_id}')
        assert delete_response.status_code == 204

        # Verify deletion
        verify_response = client.get(f'/contacts/{contact_id}')
        assert verify_response.status_code == 404

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
