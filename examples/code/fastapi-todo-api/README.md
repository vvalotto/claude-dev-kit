# FastAPI TODO API

Simple TODO API built with FastAPI, demonstrating the Claude Dev Kit framework with the **fastapi-rest** profile.

## Features

- ✅ **CRUD Operations**: Create, Read, Update, Delete tasks
- ✅ **REST Architecture**: Layered architecture (Router → Service → Database)
- ✅ **Pydantic Validation**: Request/response validation with Pydantic models
- ✅ **Automatic Documentation**: Swagger UI and ReDoc
- ✅ **Comprehensive Tests**: Unit tests + integration tests + BDD scenarios
- ✅ **100% Type Hints**: Full type safety with Python type annotations

## Architecture

```
app/
├── models/          # Pydantic schemas (TaskCreate, TaskUpdate, Task)
├── routes/          # API endpoints (FastAPI routers)
├── services/        # Business logic (TaskService)
└── database.py      # In-memory database (TaskDatabase)
```

### Layered Architecture

1. **Router Layer** (`app/routes/tasks.py`): HTTP endpoints, validation, dependency injection
2. **Service Layer** (`app/services/task_service.py`): Business logic, orchestration
3. **Data Layer** (`app/database.py`): Data access (in-memory for demo)

## Prerequisites

- Python 3.10+
- pip or uv

## Installation

```bash
# Clone or navigate to this directory
cd examples/code/fastapi-todo-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running the API

```bash
# Development mode with auto-reload
uvicorn main:app --reload

# Production mode
python main.py
```

The API will be available at:
- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint (welcome message) |
| GET | `/tasks/` | Get all tasks |
| GET | `/tasks/{id}` | Get task by ID |
| POST | `/tasks/` | Create new task |
| PUT | `/tasks/{id}` | Update task |
| DELETE | `/tasks/{id}` | Delete task |

## Example Usage

### Create a Task

```bash
curl -X POST http://localhost:8000/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Comprar leche", "description": "Ir al supermercado"}'
```

Response:
```json
{
  "id": 1,
  "title": "Comprar leche",
  "description": "Ir al supermercado",
  "completed": false
}
```

### Get All Tasks

```bash
curl http://localhost:8000/tasks/
```

### Update Task

```bash
curl -X PUT http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

### Delete Task

```bash
curl -X DELETE http://localhost:8000/tasks/1
```

## Running Tests

```bash
# All tests (unit + integration + BDD)
pytest

# With coverage report
pytest --cov=app --cov-report=term-missing

# Only unit tests
pytest tests/test_task_service.py

# Only integration tests
pytest tests/test_endpoints.py

# Only BDD tests
pytest features/steps/

# Verbose output
pytest -v
```

**Test Results:** 29 tests passing (23 unit/integration + 6 BDD) with 98% coverage in 0.8 seconds.

## Test Coverage

The project includes comprehensive tests:

- ✅ **Unit Tests** (`tests/test_task_service.py`): 10 tests for TaskService logic
- ✅ **Integration Tests** (`tests/test_endpoints.py`): 13 tests for API endpoints
- ✅ **BDD Scenarios** (`features/tasks.feature`): 6 Gherkin scenarios with pytest-bdd

**Actual Coverage:** 98% (29 tests passing)

## Code Quality

```bash
# Run pylint
pylint app/

# Check cyclomatic complexity
radon cc app/ -a

# Check maintainability index
radon mi app/
```

## Project Structure

```
fastapi-todo-api/
├── main.py                    # FastAPI app entry point
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py           # Pydantic models
│   ├── routes/
│   │   ├── __init__.py
│   │   └── tasks.py          # API endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py   # Business logic
│   └── database.py           # In-memory database
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # Test fixtures
│   ├── test_task_service.py  # Unit tests
│   └── test_endpoints.py     # Integration tests
├── features/
│   ├── __init__.py
│   ├── tasks.feature         # BDD scenarios
│   └── steps/
│       ├── __init__.py
│       └── task_steps.py     # Step definitions
├── requirements.txt
├── pytest.ini
└── README.md
```

## Next Steps

To extend this API:

1. **Add Database Persistence**: Replace in-memory database with SQLAlchemy + PostgreSQL
2. **Add Authentication**: Implement JWT authentication with fastapi-users
3. **Add Filtering/Pagination**: Add query parameters for filtering and pagination
4. **Add Validation**: Add more complex business rules
5. **Add Background Tasks**: Use FastAPI BackgroundTasks for async operations
6. **Add Caching**: Implement Redis caching for better performance

## Generated with Claude Dev Kit

This project was generated using the [Claude Dev Kit](https://github.com/vvalotto/claude-dev-kit) framework with the **fastapi-rest** profile.

The framework provides:
- ✅ Architecture templates (layered, clean architecture)
- ✅ Testing patterns (unit, integration, BDD)
- ✅ Quality gates (pylint, coverage, complexity)
- ✅ Best practices for FastAPI development

## License

MIT License
