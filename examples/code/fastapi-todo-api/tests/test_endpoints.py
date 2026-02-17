"""Integration tests for API endpoints."""

import pytest
from fastapi import status


class TestRootEndpoint:
    """Tests for root endpoint."""

    def test_root(self, client):
        """Test root endpoint returns welcome message."""
        response = client.get("/")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "message" in data
        assert "docs" in data


class TestGetTasks:
    """Tests for GET /tasks endpoints."""

    def test_get_tasks_empty(self, client):
        """Test getting tasks when database is empty."""
        response = client.get("/tasks/")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_get_tasks_with_data(self, client, sample_task_data):
        """Test getting tasks when database has data."""
        # Create tasks
        client.post("/tasks/", json=sample_task_data)
        client.post("/tasks/", json={"title": "Task 2"})

        response = client.get("/tasks/")

        assert response.status_code == status.HTTP_200_OK
        tasks = response.json()
        assert len(tasks) == 2
        assert tasks[0]["title"] == sample_task_data["title"]

    def test_get_task_by_id(self, client, sample_task_data):
        """Test getting specific task by ID."""
        # Create task
        create_response = client.post("/tasks/", json=sample_task_data)
        task_id = create_response.json()["id"]

        response = client.get(f"/tasks/{task_id}")

        assert response.status_code == status.HTTP_200_OK
        task = response.json()
        assert task["id"] == task_id
        assert task["title"] == sample_task_data["title"]

    def test_get_task_not_found(self, client):
        """Test getting non-existent task returns 404."""
        response = client.get("/tasks/999")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"].lower()


class TestCreateTask:
    """Tests for POST /tasks endpoint."""

    def test_create_task(self, client, sample_task_data):
        """Test creating a task."""
        response = client.post("/tasks/", json=sample_task_data)

        assert response.status_code == status.HTTP_201_CREATED
        task = response.json()
        assert task["id"] == 1
        assert task["title"] == sample_task_data["title"]
        assert task["description"] == sample_task_data["description"]
        assert task["completed"] is False

    def test_create_task_without_description(self, client):
        """Test creating task without optional description."""
        response = client.post("/tasks/", json={"title": "Simple Task"})

        assert response.status_code == status.HTTP_201_CREATED
        task = response.json()
        assert task["title"] == "Simple Task"
        assert task["description"] is None

    def test_create_task_validation_error(self, client):
        """Test creating task with invalid data fails validation."""
        response = client.post("/tasks/", json={})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestUpdateTask:
    """Tests for PUT /tasks/{id} endpoint."""

    def test_update_task(self, client, sample_task_data):
        """Test updating a task."""
        # Create task
        create_response = client.post("/tasks/", json=sample_task_data)
        task_id = create_response.json()["id"]

        # Update task
        update_data = {
            "title": "Updated Title",
            "completed": True
        }
        response = client.put(f"/tasks/{task_id}", json=update_data)

        assert response.status_code == status.HTTP_200_OK
        task = response.json()
        assert task["title"] == "Updated Title"
        assert task["completed"] is True

    def test_update_task_partial(self, client, sample_task_data):
        """Test partial update of task."""
        # Create task
        create_response = client.post("/tasks/", json=sample_task_data)
        task_id = create_response.json()["id"]

        # Update only completed status
        response = client.put(f"/tasks/{task_id}", json={"completed": True})

        assert response.status_code == status.HTTP_200_OK
        task = response.json()
        assert task["title"] == sample_task_data["title"]  # Unchanged
        assert task["completed"] is True  # Changed

    def test_update_task_not_found(self, client):
        """Test updating non-existent task returns 404."""
        response = client.put("/tasks/999", json={"title": "Updated"})

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestDeleteTask:
    """Tests for DELETE /tasks/{id} endpoint."""

    def test_delete_task(self, client, sample_task_data):
        """Test deleting a task."""
        # Create task
        create_response = client.post("/tasks/", json=sample_task_data)
        task_id = create_response.json()["id"]

        # Delete task
        response = client.delete(f"/tasks/{task_id}")

        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify task is deleted
        get_response = client.get(f"/tasks/{task_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_task_not_found(self, client):
        """Test deleting non-existent task returns 404."""
        response = client.delete("/tasks/999")

        assert response.status_code == status.HTTP_404_NOT_FOUND
