"""Contact routes - REST API endpoints."""

from flask import Blueprint, request, jsonify
from app.models.contact import ContactCreate, ContactUpdate
from app.services.contact_service import ContactService


contacts_bp = Blueprint('contacts', __name__)


@contacts_bp.route('/contacts', methods=['GET'])
def get_contacts():
    """
    Get all contacts.

    Returns:
        JSON: List of all contacts
        Status: 200 OK
    """
    contacts = ContactService.get_all_contacts()
    return jsonify([contact.to_dict() for contact in contacts]), 200


@contacts_bp.route('/contacts/<int:contact_id>', methods=['GET'])
def get_contact(contact_id: int):
    """
    Get a contact by ID.

    Args:
        contact_id: ID of the contact to retrieve

    Returns:
        JSON: Contact data if found
        Status: 200 OK if found, 404 Not Found otherwise
    """
    contact = ContactService.get_contact_by_id(contact_id)
    if contact is None:
        return jsonify({'error': 'Contact not found'}), 404
    return jsonify(contact.to_dict()), 200


@contacts_bp.route('/contacts', methods=['POST'])
def create_contact():
    """
    Create a new contact.

    Request Body (JSON):
        - nombre (str): Contact name
        - email (str): Contact email (must be valid format)
        - telefono (str): Contact phone number

    Returns:
        JSON: Created contact with assigned ID
        Status: 201 Created if successful, 400 Bad Request if validation fails
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        contact_data = ContactCreate(
            nombre=data.get('nombre', ''),
            email=data.get('email', ''),
            telefono=data.get('telefono', '')
        )

        contact = ContactService.create_contact(contact_data)
        return jsonify(contact.to_dict()), 201

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Internal error: {str(e)}'}), 500


@contacts_bp.route('/contacts/<int:contact_id>', methods=['PUT'])
def update_contact(contact_id: int):
    """
    Update an existing contact.

    Args:
        contact_id: ID of the contact to update

    Request Body (JSON):
        - nombre (str, optional): New contact name
        - email (str, optional): New contact email
        - telefono (str, optional): New contact phone number

    Returns:
        JSON: Updated contact
        Status: 200 OK if successful, 404 Not Found if contact doesn't exist,
                400 Bad Request if validation fails
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        contact_data = ContactUpdate(
            nombre=data.get('nombre'),
            email=data.get('email'),
            telefono=data.get('telefono')
        )

        contact = ContactService.update_contact(contact_id, contact_data)
        if contact is None:
            return jsonify({'error': 'Contact not found'}), 404

        return jsonify(contact.to_dict()), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Internal error: {str(e)}'}), 500


@contacts_bp.route('/contacts/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id: int):
    """
    Delete a contact.

    Args:
        contact_id: ID of the contact to delete

    Returns:
        Status: 204 No Content if successful, 404 Not Found if contact doesn't exist
    """
    deleted = ContactService.delete_contact(contact_id)
    if not deleted:
        return jsonify({'error': 'Contact not found'}), 404
    return '', 204
