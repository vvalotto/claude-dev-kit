"""Task service - Business logic for task operations."""

from typing import Optional
from app.models import Task, TaskCreate, TaskUpdate
from app.database import TaskDatabase


class TaskService:
    """Service for task business logic."""

    def __init__(self, db: TaskDatabase):
        """Initialize service with database.

        Args:
            db: Database instance
        """
        self.db = db

    def create_task(self, task_data: TaskCreate) -> Task:
        """Create a new task.

        Args:
            task_data: Task creation data

        Returns:
            Created task
        """
        return self.db.create(
            title=task_data.title,
            description=task_data.description
        )

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get task by ID.

        Args:
            task_id: Task ID

        Returns:
            Task if found, None otherwise
        """
        return self.db.get(task_id)

    def get_all_tasks(self) -> list[Task]:
        """Get all tasks.

        Returns:
            List of all tasks
        """
        return self.db.get_all()

    def update_task(self, task_id: int, task_data: TaskUpdate) -> Optional[Task]:
        """Update task.

        Args:
            task_id: Task ID
            task_data: Task update data

        Returns:
            Updated task if found, None otherwise
        """
        # Only update fields that are provided
        update_dict = task_data.model_dump(exclude_unset=True)
        if not update_dict:
            return self.db.get(task_id)

        return self.db.update(task_id, **update_dict)

    def delete_task(self, task_id: int) -> bool:
        """Delete task.

        Args:
            task_id: Task ID

        Returns:
            True if deleted, False if not found
        """
        return self.db.delete(task_id)
