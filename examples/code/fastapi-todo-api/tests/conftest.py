"""Test fixtures and configuration."""

import pytest
from fastapi.testclient import TestClient
from main import app
from app.database import get_db, TaskDatabase


@pytest.fixture
def test_db():
    """Create a clean test database."""
    db = TaskDatabase()
    yield db
    db.clear()


@pytest.fixture
def client(test_db):
    """Create test client with test database."""
    # Override dependency
    app.dependency_overrides[get_db] = lambda: test_db

    with TestClient(app) as test_client:
        yield test_client

    # Clean up
    app.dependency_overrides.clear()


@pytest.fixture
def sample_task_data():
    """Sample task data for tests."""
    return {
        "title": "Test Task",
        "description": "Test Description"
    }
