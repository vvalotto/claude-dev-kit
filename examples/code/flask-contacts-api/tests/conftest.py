"""Pytest configuration and fixtures."""

import pytest
from app import create_app
from app.database import reset_db
from app.models.contact import ContactCreate


@pytest.fixture
def app():
    """
    Create and configure a Flask app for testing.

    Yields:
        Flask app configured for testing
    """
    app = create_app()
    app.config['TESTING'] = True
    yield app


@pytest.fixture
def client(app):
    """
    Create a test client for the Flask app.

    Args:
        app: Flask app fixture

    Yields:
        Flask test client
    """
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def reset_database():
    """
    Reset the database before each test.

    This fixture runs automatically for every test.
    """
    reset_db()
    yield
    reset_db()


@pytest.fixture
def sample_contact():
    """
    Create sample contact data for testing.

    Returns:
        ContactCreate instance with test data
    """
    return ContactCreate(
        nombre="Juan Pérez",
        email="juan.perez@email.com",
        telefono="555-1234"
    )


@pytest.fixture
def sample_contact_dict():
    """
    Create sample contact data as dictionary.

    Returns:
        Dictionary with contact data
    """
    return {
        'nombre': 'Juan Pérez',
        'email': 'juan.perez@email.com',
        'telefono': '555-1234'
    }
