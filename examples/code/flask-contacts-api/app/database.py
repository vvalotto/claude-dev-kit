"""In-memory database for contacts."""

from typing import Dict
from app.models.contact import Contact


# Global in-memory database
_contacts_db: Dict[int, Contact] = {}
_next_id: int = 1


def get_db() -> Dict[int, Contact]:
    """
    Get the contacts database.

    Returns:
        Dictionary mapping contact IDs to Contact objects
    """
    return _contacts_db


def get_next_id() -> int:
    """
    Get the next available contact ID.

    Returns:
        Next available ID (auto-incremented)
    """
    global _next_id
    current_id = _next_id
    _next_id += 1
    return current_id


def reset_db() -> None:
    """
    Reset the database to empty state.

    This is primarily used for testing purposes.
    """
    global _contacts_db, _next_id
    _contacts_db = {}
    _next_id = 1
