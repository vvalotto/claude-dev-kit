"""Unit tests for TaskService."""

import pytest
from app.services import TaskService
from app.models import TaskCreate, TaskUpdate
from app.database import TaskDatabase


class TestTaskServiceCreation:
    """Tests for TaskService initialization."""

    def test_service_creation(self, test_db):
        """Test service can be created."""
        service = TaskService(test_db)
        assert service is not None
        assert service.db == test_db


class TestTaskServiceMethods:
    """Tests for TaskService business logic."""

    def test_create_task(self, test_db):
        """Test creating a task."""
        service = TaskService(test_db)
        task_data = TaskCreate(title="New Task", description="Test")

        task = service.create_task(task_data)

        assert task.id == 1
        assert task.title == "New Task"
        assert task.description == "Test"
        assert task.completed is False

    def test_get_task(self, test_db):
        """Test getting a task by ID."""
        service = TaskService(test_db)
        created = service.create_task(TaskCreate(title="Test"))

        task = service.get_task(created.id)

        assert task is not None
        assert task.id == created.id
        assert task.title == "Test"

    def test_get_task_not_found(self, test_db):
        """Test getting non-existent task returns None."""
        service = TaskService(test_db)

        task = service.get_task(999)

        assert task is None

    def test_get_all_tasks(self, test_db):
        """Test getting all tasks."""
        service = TaskService(test_db)
        service.create_task(TaskCreate(title="Task 1"))
        service.create_task(TaskCreate(title="Task 2"))

        tasks = service.get_all_tasks()

        assert len(tasks) == 2
        assert tasks[0].title == "Task 1"
        assert tasks[1].title == "Task 2"

    def test_update_task(self, test_db):
        """Test updating a task."""
        service = TaskService(test_db)
        created = service.create_task(TaskCreate(title="Original"))

        updated = service.update_task(
            created.id,
            TaskUpdate(title="Updated", completed=True)
        )

        assert updated is not None
        assert updated.title == "Updated"
        assert updated.completed is True

    def test_update_task_partial(self, test_db):
        """Test partial update (only some fields)."""
        service = TaskService(test_db)
        created = service.create_task(TaskCreate(title="Original", description="Desc"))

        updated = service.update_task(
            created.id,
            TaskUpdate(completed=True)
        )

        assert updated is not None
        assert updated.title == "Original"  # Unchanged
        assert updated.description == "Desc"  # Unchanged
        assert updated.completed is True  # Changed

    def test_update_task_not_found(self, test_db):
        """Test updating non-existent task returns None."""
        service = TaskService(test_db)

        updated = service.update_task(999, TaskUpdate(title="Updated"))

        assert updated is None

    def test_delete_task(self, test_db):
        """Test deleting a task."""
        service = TaskService(test_db)
        created = service.create_task(TaskCreate(title="To Delete"))

        deleted = service.delete_task(created.id)

        assert deleted is True
        assert service.get_task(created.id) is None

    def test_delete_task_not_found(self, test_db):
        """Test deleting non-existent task returns False."""
        service = TaskService(test_db)

        deleted = service.delete_task(999)

        assert deleted is False
