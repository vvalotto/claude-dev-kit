"""Task endpoints - REST API routes."""

from fastapi import APIRouter, HTTPException, status, Depends
from app.models import Task, TaskCreate, TaskUpdate
from app.services import TaskService
from app.database import get_db, TaskDatabase


router = APIRouter(prefix="/tasks", tags=["tasks"])


def get_task_service(db: TaskDatabase = Depends(get_db)) -> TaskService:
    """Get task service instance (dependency injection).

    Args:
        db: Database instance

    Returns:
        TaskService instance
    """
    return TaskService(db)


@router.get("/", response_model=list[Task], summary="Get all tasks")
def get_tasks(service: TaskService = Depends(get_task_service)):
    """Get all tasks.

    Returns:
        List of all tasks
    """
    return service.get_all_tasks()


@router.get("/{task_id}", response_model=Task, summary="Get task by ID")
def get_task(task_id: int, service: TaskService = Depends(get_task_service)):
    """Get task by ID.

    Args:
        task_id: Task ID

    Returns:
        Task data

    Raises:
        HTTPException: 404 if task not found
    """
    task = service.get_task(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    return task


@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED, summary="Create task")
def create_task(task_data: TaskCreate, service: TaskService = Depends(get_task_service)):
    """Create a new task.

    Args:
        task_data: Task creation data

    Returns:
        Created task
    """
    return service.create_task(task_data)


@router.put("/{task_id}", response_model=Task, summary="Update task")
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    service: TaskService = Depends(get_task_service)
):
    """Update task.

    Args:
        task_id: Task ID
        task_data: Task update data

    Returns:
        Updated task

    Raises:
        HTTPException: 404 if task not found
    """
    task = service.update_task(task_id, task_data)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete task")
def delete_task(task_id: int, service: TaskService = Depends(get_task_service)):
    """Delete task.

    Args:
        task_id: Task ID

    Raises:
        HTTPException: 404 if task not found
    """
    deleted = service.delete_task(task_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
