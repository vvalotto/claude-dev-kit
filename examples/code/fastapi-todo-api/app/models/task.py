"""Task Pydantic models for request/response validation."""

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    """Schema for creating a new task."""

    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: str | None = Field(None, max_length=1000, description="Task description")

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "title": "Comprar leche",
                "description": "Ir al supermercado y comprar leche"
            }
        }


class TaskUpdate(BaseModel):
    """Schema for updating an existing task."""

    title: str | None = Field(None, min_length=1, max_length=200, description="Task title")
    description: str | None = Field(None, max_length=1000, description="Task description")
    completed: bool | None = Field(None, description="Task completion status")

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "title": "Comprar leche y pan",
                "completed": True
            }
        }


class Task(BaseModel):
    """Schema for task response."""

    id: int = Field(..., description="Task ID")
    title: str = Field(..., description="Task title")
    description: str | None = Field(None, description="Task description")
    completed: bool = Field(False, description="Task completion status")

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Comprar leche",
                "description": "Ir al supermercado y comprar leche",
                "completed": False
            }
        }
