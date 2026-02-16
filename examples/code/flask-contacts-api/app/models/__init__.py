"""Models package for Flask Contacts API."""

from app.models.contact import Contact, ContactCreate, ContactUpdate, validate_email

__all__ = ['Contact', 'ContactCreate', 'ContactUpdate', 'validate_email']
