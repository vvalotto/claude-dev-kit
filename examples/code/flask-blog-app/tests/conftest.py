"""Pytest configuration and fixtures for tests."""
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


@pytest.fixture
def sample_post():
    """
    Create a sample post in the database.

    Returns:
        Post: Sample post instance
    """
    from app.models import Post
    post = Post(
        title="Sample Post",
        content="This is sample content for testing purposes.",
        author="Test Author"
    )
    return db.create(post)


@pytest.fixture
def multiple_posts():
    """
    Create multiple posts in the database.

    Returns:
        List[Post]: List of created posts
    """
    from app.models import Post
    posts = []

    for i in range(15):
        post = Post(
            title=f"Post {i+1}",
            content=f"Content for post {i+1}. This is a test post.",
            author=f"Author {i+1}"
        )
        posts.append(db.create(post))

    return posts
