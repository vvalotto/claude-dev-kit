"""Pytest configuration and fixtures for BDD tests."""
import pytest
from app import create_app
from app.database import db


@pytest.fixture
def app():
    """
    Create and configure a test Flask application.

    Yields:
        Flask application instance configured for testing
    """
    test_config = {
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret-key'
    }

    app = create_app(config=test_config)
    yield app


@pytest.fixture
def client(app):
    """
    Create a test client for the Flask application.

    Args:
        app: Flask application fixture

    Yields:
        Flask test client
    """
    return app.test_client()


@pytest.fixture(autouse=True)
def clean_database():
    """
    Automatically clear database before each test.

    This fixture runs before every test to ensure a clean state.
    """
    db.clear()
    yield
    db.clear()
