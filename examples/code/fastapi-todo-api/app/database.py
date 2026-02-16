"""In-memory database for tasks."""

from typing import Dict, Optional
from app.models import Task


class TaskDatabase:
    """Simple in-memory task database."""

    def __init__(self):
        """Initialize empty database."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def create(self, title: str, description: Optional[str] = None) -> Task:
        """Create a new task.

        Args:
            title: Task title
            description: Optional task description

        Returns:
            Created task
        """
        task = Task(
            id=self._next_id,
            title=title,
            description=description,
            completed=False
        )
        self._tasks[self._next_id] = task
        self._next_id += 1
        return task

    def get(self, task_id: int) -> Optional[Task]:
        """Get task by ID.

        Args:
            task_id: Task ID

        Returns:
            Task if found, None otherwise
        """
        return self._tasks.get(task_id)

    def get_all(self) -> list[Task]:
        """Get all tasks.

        Returns:
            List of all tasks
        """
        return list(self._tasks.values())

    def update(self, task_id: int, **kwargs) -> Optional[Task]:
        """Update task fields.

        Args:
            task_id: Task ID
            **kwargs: Fields to update

        Returns:
            Updated task if found, None otherwise
        """
        task = self._tasks.get(task_id)
        if not task:
            return None

        # Update fields
        updated_data = task.model_dump()
        updated_data.update(kwargs)
        updated_task = Task(**updated_data)
        self._tasks[task_id] = updated_task

        return updated_task

    def delete(self, task_id: int) -> bool:
        """Delete task by ID.

        Args:
            task_id: Task ID

        Returns:
            True if deleted, False if not found
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def clear(self):
        """Clear all tasks (for testing)."""
        self._tasks.clear()
        self._next_id = 1


# Global database instance
db = TaskDatabase()


def get_db() -> TaskDatabase:
    """Get database instance (for dependency injection).

    Returns:
        Database instance
    """
    return db
