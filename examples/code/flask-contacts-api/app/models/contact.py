"""Contact models and validation."""

from dataclasses import dataclass
from typing import Optional
import re


def validate_email(email: str) -> bool:
    """
    Validate email format.

    Args:
        email: Email address to validate

    Returns:
        True if email is valid, False otherwise

    Examples:
        >>> validate_email("test@example.com")
        True
        >>> validate_email("invalid-email")
        False
    """
    if not email:
        return False
    # Simple email validation: contains @ and has text before and after
    email_pattern = r'^[^@]+@[^@]+\.[^@]+$'
    return bool(re.match(email_pattern, email))


@dataclass
class Contact:
    """
    Contact entity with all fields.

    Attributes:
        id: Unique identifier
        nombre: Contact name
        email: Contact email
        telefono: Contact phone number
    """
    id: int
    nombre: str
    email: str
    telefono: str

    def to_dict(self) -> dict:
        """
        Convert contact to dictionary.

        Returns:
            Dictionary representation of contact
        """
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'telefono': self.telefono
        }


@dataclass
class ContactCreate:
    """
    Data for creating a new contact.

    Attributes:
        nombre: Contact name
        email: Contact email (must be valid format)
        telefono: Contact phone number

    Raises:
        ValueError: If email format is invalid
    """
    nombre: str
    email: str
    telefono: str

    def __post_init__(self):
        """Validate contact data after initialization."""
        if not self.nombre:
            raise ValueError("nombre is required")
        if not self.email:
            raise ValueError("email is required")
        if not self.telefono:
            raise ValueError("telefono is required")
        if not validate_email(self.email):
            raise ValueError(f"Invalid email format: {self.email}")


@dataclass
class ContactUpdate:
    """
    Data for updating an existing contact.

    All fields are optional to allow partial updates.

    Attributes:
        nombre: New contact name (optional)
        email: New contact email (optional, must be valid if provided)
        telefono: New contact phone number (optional)

    Raises:
        ValueError: If email format is invalid when provided
    """
    nombre: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None

    def __post_init__(self):
        """Validate contact data after initialization."""
        if self.email is not None and not validate_email(self.email):
            raise ValueError(f"Invalid email format: {self.email}")
