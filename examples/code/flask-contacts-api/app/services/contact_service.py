"""Contact service layer - Business logic."""

from typing import List, Optional
from app.models.contact import Contact, ContactCreate, ContactUpdate
from app.database import get_db, get_next_id


class ContactService:
    """
    Service layer for contact management.

    Handles business logic and data access for contacts.
    """

    @staticmethod
    def create_contact(contact_data: ContactCreate) -> Contact:
        """
        Create a new contact.

        Args:
            contact_data: Data for the new contact

        Returns:
            Created contact with assigned ID

        Raises:
            ValueError: If validation fails

        Examples:
            >>> data = ContactCreate("John", "john@example.com", "555-1234")
            >>> contact = ContactService.create_contact(data)
            >>> contact.nombre
            'John'
        """
        db = get_db()
        contact_id = get_next_id()

        contact = Contact(
            id=contact_id,
            nombre=contact_data.nombre,
            email=contact_data.email,
            telefono=contact_data.telefono
        )

        db[contact_id] = contact
        return contact

    @staticmethod
    def get_all_contacts() -> List[Contact]:
        """
        Get all contacts.

        Returns:
            List of all contacts (empty list if no contacts exist)

        Examples:
            >>> contacts = ContactService.get_all_contacts()
            >>> len(contacts)
            0
        """
        db = get_db()
        return list(db.values())

    @staticmethod
    def get_contact_by_id(contact_id: int) -> Optional[Contact]:
        """
        Get a contact by ID.

        Args:
            contact_id: ID of the contact to retrieve

        Returns:
            Contact if found, None otherwise

        Examples:
            >>> contact = ContactService.get_contact_by_id(1)
            >>> contact is None
            True
        """
        db = get_db()
        return db.get(contact_id)

    @staticmethod
    def update_contact(contact_id: int, contact_data: ContactUpdate) -> Optional[Contact]:
        """
        Update an existing contact.

        Only updates fields that are provided (not None).

        Args:
            contact_id: ID of the contact to update
            contact_data: Data to update (partial updates allowed)

        Returns:
            Updated contact if found, None otherwise

        Raises:
            ValueError: If validation fails

        Examples:
            >>> update_data = ContactUpdate(nombre="Jane")
            >>> contact = ContactService.update_contact(1, update_data)
            >>> contact is None
            True
        """
        db = get_db()
        contact = db.get(contact_id)

        if contact is None:
            return None

        # Update only provided fields
        if contact_data.nombre is not None:
            contact.nombre = contact_data.nombre
        if contact_data.email is not None:
            contact.email = contact_data.email
        if contact_data.telefono is not None:
            contact.telefono = contact_data.telefono

        return contact

    @staticmethod
    def delete_contact(contact_id: int) -> bool:
        """
        Delete a contact by ID.

        Args:
            contact_id: ID of the contact to delete

        Returns:
            True if contact was deleted, False if not found

        Examples:
            >>> ContactService.delete_contact(999)
            False
        """
        db = get_db()
        if contact_id in db:
            del db[contact_id]
            return True
        return False
