"""In-memory database for the blog application."""
from typing import List, Optional
from app.models import Post


class Database:
    """
    In-memory database for managing blog posts.

    This is a simple in-memory storage implementation for demonstration purposes.
    In production, this would be replaced with a proper database (SQLAlchemy, etc.).
    """

    def __init__(self):
        """Initialize the database with empty storage."""
        self._posts: dict[int, Post] = {}
        self._next_id: int = 1

    def get_all(self, page: int = 1, per_page: int = 10) -> List[Post]:
        """
        Get all posts with pagination support.

        Args:
            page: Page number (1-indexed)
            per_page: Number of posts per page

        Returns:
            List of posts for the requested page
        """
        all_posts = sorted(self._posts.values(), key=lambda p: p.created_at, reverse=True)
        start = (page - 1) * per_page
        end = start + per_page
        return all_posts[start:end]

    def get_by_id(self, post_id: int) -> Optional[Post]:
        """
        Get a post by its ID.

        Args:
            post_id: The post ID

        Returns:
            The post if found, None otherwise
        """
        return self._posts.get(post_id)

    def create(self, post: Post) -> Post:
        """
        Create a new post.

        Args:
            post: The post to create (without ID)

        Returns:
            The created post with assigned ID
        """
        post.id = self._next_id
        self._next_id += 1
        self._posts[post.id] = post
        return post

    def update(self, post_id: int, post: Post) -> Optional[Post]:
        """
        Update an existing post.

        Args:
            post_id: The post ID to update
            post: The updated post data

        Returns:
            The updated post if found, None otherwise
        """
        if post_id not in self._posts:
            return None

        post.id = post_id
        post.created_at = self._posts[post_id].created_at  # Preserve original creation time
        self._posts[post_id] = post
        return post

    def delete(self, post_id: int) -> bool:
        """
        Delete a post by its ID.

        Args:
            post_id: The post ID to delete

        Returns:
            True if deleted, False if not found
        """
        if post_id in self._posts:
            del self._posts[post_id]
            return True
        return False

    def count(self) -> int:
        """
        Get the total count of posts.

        Returns:
            Total number of posts
        """
        return len(self._posts)

    def clear(self):
        """Clear all posts from the database."""
        self._posts.clear()
        self._next_id = 1


# Global database instance
db = Database()
