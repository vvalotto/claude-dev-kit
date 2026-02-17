"""Unit tests for ContactService."""

import pytest
from app.services.contact_service import ContactService
from app.models.contact import ContactCreate, ContactUpdate, validate_email


class TestContactService:
    """Test suite for ContactService business logic."""

    def test_create_contact_valid_data(self, sample_contact):
        """Test creating a contact with valid data."""
        contact = ContactService.create_contact(sample_contact)

        assert contact.id == 1
        assert contact.nombre == "Juan Pérez"
        assert contact.email == "juan.perez@email.com"
        assert contact.telefono == "555-1234"

    def test_create_contact_invalid_email(self):
        """Test creating a contact with invalid email raises ValueError."""
        with pytest.raises(ValueError, match="Invalid email format"):
            ContactCreate(
                nombre="Test User",
                email="invalid-email",
                telefono="555-0000"
            )

    def test_create_contact_missing_fields(self):
        """Test creating a contact with missing required fields."""
        with pytest.raises(ValueError, match="nombre is required"):
            ContactCreate(
                nombre="",
                email="test@email.com",
                telefono="555-0000"
            )

        with pytest.raises(ValueError, match="email is required"):
            ContactCreate(
                nombre="Test",
                email="",
                telefono="555-0000"
            )

        with pytest.raises(ValueError, match="telefono is required"):
            ContactCreate(
                nombre="Test",
                email="test@email.com",
                telefono=""
            )

    def test_get_all_contacts_empty(self):
        """Test getting all contacts when database is empty."""
        contacts = ContactService.get_all_contacts()
        assert contacts == []

    def test_get_all_contacts_with_data(self, sample_contact):
        """Test getting all contacts after creating some."""
        ContactService.create_contact(sample_contact)
        ContactService.create_contact(ContactCreate(
            nombre="María García",
            email="maria.garcia@email.com",
            telefono="555-5678"
        ))

        contacts = ContactService.get_all_contacts()
        assert len(contacts) == 2
        assert contacts[0].nombre == "Juan Pérez"
        assert contacts[1].nombre == "María García"

    def test_get_contact_by_id_exists(self, sample_contact):
        """Test getting a contact by ID when it exists."""
        created = ContactService.create_contact(sample_contact)
        contact = ContactService.get_contact_by_id(created.id)

        assert contact is not None
        assert contact.id == created.id
        assert contact.nombre == "Juan Pérez"

    def test_get_contact_by_id_not_exists(self):
        """Test getting a contact by ID when it doesn't exist."""
        contact = ContactService.get_contact_by_id(999)
        assert contact is None

    def test_update_contact_exists(self, sample_contact):
        """Test updating an existing contact."""
        created = ContactService.create_contact(sample_contact)
        update_data = ContactUpdate(
            nombre="Juan Pérez García",
            email="juan.nuevo@email.com"
        )

        updated = ContactService.update_contact(created.id, update_data)

        assert updated is not None
        assert updated.id == created.id
        assert updated.nombre == "Juan Pérez García"
        assert updated.email == "juan.nuevo@email.com"
        assert updated.telefono == "555-1234"  # Unchanged

    def test_update_contact_partial(self, sample_contact):
        """Test partial update (only some fields)."""
        created = ContactService.create_contact(sample_contact)
        update_data = ContactUpdate(telefono="555-9999")

        updated = ContactService.update_contact(created.id, update_data)

        assert updated is not None
        assert updated.nombre == "Juan Pérez"  # Unchanged
        assert updated.email == "juan.perez@email.com"  # Unchanged
        assert updated.telefono == "555-9999"  # Changed

    def test_update_contact_not_exists(self):
        """Test updating a contact that doesn't exist."""
        update_data = ContactUpdate(nombre="Fantasma")
        updated = ContactService.update_contact(999, update_data)
        assert updated is None

    def test_delete_contact_exists(self, sample_contact):
        """Test deleting an existing contact."""
        created = ContactService.create_contact(sample_contact)
        deleted = ContactService.delete_contact(created.id)

        assert deleted is True
        assert ContactService.get_contact_by_id(created.id) is None

    def test_delete_contact_not_exists(self):
        """Test deleting a contact that doesn't exist."""
        deleted = ContactService.delete_contact(999)
        assert deleted is False

    def test_email_validation(self):
        """Test email validation function."""
        # Valid emails
        assert validate_email("test@example.com") is True
        assert validate_email("user.name@domain.co.uk") is True
        assert validate_email("test+tag@example.com") is True

        # Invalid emails
        assert validate_email("invalid-email") is False
        assert validate_email("@example.com") is False
        assert validate_email("test@") is False
        assert validate_email("") is False
        assert validate_email("test@domain") is False

    def test_multiple_contacts_unique_ids(self):
        """Test that multiple contacts get unique sequential IDs."""
        contact1 = ContactService.create_contact(ContactCreate(
            nombre="Contact 1",
            email="contact1@email.com",
            telefono="555-0001"
        ))
        contact2 = ContactService.create_contact(ContactCreate(
            nombre="Contact 2",
            email="contact2@email.com",
            telefono="555-0002"
        ))
        contact3 = ContactService.create_contact(ContactCreate(
            nombre="Contact 3",
            email="contact3@email.com",
            telefono="555-0003"
        ))

        assert contact1.id == 1
        assert contact2.id == 2
        assert contact3.id == 3
