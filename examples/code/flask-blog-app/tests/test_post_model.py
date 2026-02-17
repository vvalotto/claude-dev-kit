"""Unit tests for Post model."""
import pytest
from datetime import datetime
from app.models import Post


@pytest.mark.unit
class TestPostModel:
    """Test suite for Post model."""

    def test_post_creation(self):
        """Test creating a post instance."""
        post = Post(
            title="Test Post",
            content="Test content",
            author="Test Author"
        )

        assert post.title == "Test Post"
        assert post.content == "Test content"
        assert post.author == "Test Author"
        assert post.id is None
        assert isinstance(post.created_at, datetime)

    def test_post_with_id(self):
        """Test creating a post with explicit ID."""
        post = Post(
            id=1,
            title="Test Post",
            content="Test content",
            author="Test Author"
        )

        assert post.id == 1

    def test_post_with_created_at(self):
        """Test creating a post with explicit created_at timestamp."""
        timestamp = datetime(2026, 1, 1, 12, 0, 0)
        post = Post(
            title="Test Post",
            content="Test content",
            author="Test Author",
            created_at=timestamp
        )

        assert post.created_at == timestamp

    def test_post_to_dict(self):
        """Test converting post to dictionary."""
        post = Post(
            id=1,
            title="Test Post",
            content="Test content",
            author="Test Author"
        )

        post_dict = post.to_dict()

        assert post_dict['id'] == 1
        assert post_dict['title'] == "Test Post"
        assert post_dict['content'] == "Test content"
        assert post_dict['author'] == "Test Author"
        assert 'created_at' in post_dict
        assert isinstance(post_dict['created_at'], str)

    def test_post_to_dict_without_id(self):
        """Test converting post without ID to dictionary."""
        post = Post(
            title="Test Post",
            content="Test content",
            author="Test Author"
        )

        post_dict = post.to_dict()

        assert post_dict['id'] is None

    def test_post_str_representation(self):
        """Test string representation of post."""
        post = Post(
            id=1,
            title="Test Post",
            content="Test content",
            author="Test Author"
        )

        str_repr = str(post)

        assert "Post" in str_repr
        assert "id=1" in str_repr
        assert "Test Post" in str_repr
        assert "Test Author" in str_repr

    def test_post_dataclass_equality(self):
        """Test equality comparison between posts."""
        post1 = Post(
            id=1,
            title="Test Post",
            content="Test content",
            author="Test Author"
        )

        post2 = Post(
            id=1,
            title="Test Post",
            content="Test content",
            author="Test Author"
        )

        # Note: created_at will be different, so posts won't be equal
        # This tests that dataclass equality works as expected
        assert post1 != post2  # Different created_at
