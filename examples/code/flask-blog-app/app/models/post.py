"""Post model for the blog application."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Post:
    """
    Post model representing a blog post.

    Attributes:
        id: Unique identifier for the post
        title: Post title
        content: Post content/body
        author: Post author name
        created_at: Timestamp when the post was created
    """
    title: str
    content: str
    author: str
    id: Optional[int] = None
    created_at: Optional[datetime] = None

    def __post_init__(self):
        """Initialize created_at if not provided."""
        if self.created_at is None:
            self.created_at = datetime.now()

    def to_dict(self) -> dict:
        """
        Convert post to dictionary.

        Returns:
            Dictionary representation of the post
        """
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'author': self.author,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __str__(self) -> str:
        """String representation of the post."""
        return f"Post(id={self.id}, title='{self.title}', author='{self.author}')"
