# Tutorial: FastAPI REST API - TODO API

**Stack:** FastAPI (fastapi-rest)
**Tiempo Estimado:** 45-60 minutos
**Nivel:** Principiante

---

## 📋 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Requisitos Previos](#requisitos-previos)
3. [Historia de Usuario](#historia-de-usuario)
4. [Setup del Proyecto](#setup-del-proyecto)
5. [Instalación del Framework](#instalación-del-framework)
6. [Walkthrough: Las 10 Fases](#walkthrough-las-10-fases)
7. [Validación Final](#validación-final)
8. [Troubleshooting](#troubleshooting)
9. [Próximos Pasos](#próximos-pasos)
10. [Recursos](#recursos)

---

## 🎯 Introducción

Este tutorial te guiará paso a paso en la creación de una **TODO API REST** utilizando el perfil **fastapi-rest** del Claude Dev Kit.

Aprenderás:
- ✅ Cómo usar el skill `/implement-us` para guiar la implementación
- ✅ Cómo el framework adapta las 10 fases a una arquitectura en capas (Router → Service → Database)
- ✅ Cómo generar BDD scenarios, tests y documentación automáticamente
- ✅ Buenas prácticas de FastAPI con arquitectura limpia

Al finalizar, tendrás una API REST funcional con:
- 6 endpoints CRUD (GET, POST, PUT, DELETE)
- Validación automática con Pydantic
- Documentación interactiva con Swagger UI
- Suite completa de tests (unitarios, integración, BDD)
- Código que pasa quality gates (Pylint, cobertura, complejidad)

---

## ✅ Requisitos Previos

### Software Necesario

- **Python:** 3.10 o superior
- **Claude Code CLI:** Instalado y configurado
- **FastAPI:** Se instalará durante el setup
- **pytest:** Para testing
- **Git:** Para control de versiones

### Conocimientos

- Programación básica en Python
- Familiaridad con la terminal/línea de comandos
- (Opcional) Conceptos básicos de APIs REST
- (Opcional) Familiaridad con async/await en Python

### Verificación

```bash
# Verificar Python
python --version  # Debe ser >= 3.10

# Verificar Claude Code
claude --version

# Verificar Git
git --version
```

**Nota:** No necesitas tener FastAPI instalado previamente. Lo instalaremos en el setup.

---

## 📖 Historia de Usuario

```gherkin
# US-002: API de Tareas (TODO)

Como desarrollador frontend
Quiero una API REST para gestionar tareas
Para construir una aplicación TODO completa
```

### Criterios de Aceptación

**Funcionalidades Principales:**
- ✅ GET /tasks - Listar todas las tareas
- ✅ GET /tasks/{id} - Obtener tarea por ID
- ✅ POST /tasks - Crear nueva tarea
- ✅ PUT /tasks/{id} - Actualizar tarea existente
- ✅ DELETE /tasks/{id} - Eliminar tarea
- ✅ Validación automática de requests con Pydantic
- ✅ Documentación interactiva con Swagger UI

### Alcance

**Componentes a Implementar:**
- **Models (Pydantic):** TaskCreate, TaskUpdate, Task
- **Router:** Endpoints REST con validación
- **Service:** Lógica de negocio
- **Database:** Capa de acceso a datos (in-memory para demo)

**Casos de Uso:**
1. Usuario crea tarea "Comprar leche" → API retorna task con ID
2. Usuario lista todas las tareas → API retorna array de tasks
3. Usuario actualiza tarea a completada → API actualiza y retorna task
4. Usuario elimina tarea → API retorna 204 No Content

---

## 🚀 Setup del Proyecto

### 1. Crear Directorio del Proyecto

```bash
mkdir todo-api
cd todo-api
```

### 2. Inicializar Git

```bash
git init
git checkout -b develop
```

### 3. Crear Entorno Virtual

```bash
python -m venv venv

# Activar (Linux/macOS)
source venv/bin/activate

# Activar (Windows)
venv\Scripts\activate
```

### 4. Instalar Dependencias Base

```bash
# Crear requirements.txt
cat > requirements.txt << EOF
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
pydantic>=2.5.0
pytest>=7.4.0
pytest-asyncio>=0.23.0
pytest-cov>=4.1.0
pytest-bdd>=6.1.0
httpx>=0.26.0
pylint>=3.0.0
radon>=6.0.0
EOF

pip install -r requirements.txt
```

**Verificar instalación:**

```bash
python -c "from fastapi import FastAPI; print('FastAPI OK')"
# Output esperado: FastAPI OK
```

### 5. Crear Estructura Base

```bash
# Crear directorios
mkdir -p app/{models,routes,services}
mkdir -p tests
mkdir -p features/steps
mkdir -p historias-usuario
mkdir -p docs/{planning,reporting}

# Crear __init__.py
touch app/__init__.py
touch app/models/__init__.py
touch app/routes/__init__.py
touch app/services/__init__.py
touch features/__init__.py
touch features/steps/__init__.py
```

**Estructura del proyecto:**

```
todo-api/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py              # Pydantic models (a crear)
│   ├── routes/
│   │   ├── __init__.py
│   │   └── tasks.py             # API endpoints (a crear)
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py      # Business logic (a crear)
│   └── database.py              # Data layer (a crear)
├── tests/
│   ├── test_task_service.py     # Unit tests (a crear)
│   └── test_endpoints.py        # Integration tests (a crear)
├── features/
│   ├── tasks.feature            # BDD scenarios (a crear)
│   └── steps/
│       └── task_steps.py        # Step definitions (a crear)
├── historias-usuario/
├── docs/
├── requirements.txt
├── main.py                      # Entry point (a crear)
└── README.md                    # (a crear)
```

---

## 📦 Instalación del Framework

### 1. Clonar Claude Dev Kit

```bash
# Clonar en ubicación global (si no lo tienes)
cd ~
git clone https://github.com/vvalotto/claude-dev-kit.git ~/.claude-dev-kit
```

### 2. Ejecutar Instalador

```bash
# Volver a tu proyecto
cd ~/todo-api

# Ejecutar instalador (modo no interactivo)
python ~/.claude-dev-kit/install/installer.py --profile fastapi-rest --yes
```

**Salida esperada:**

```
🚀 Claude Dev Kit - Installer
================================

📋 Selected Profile: fastapi-rest
   - Architecture: Layered (Router → Service → Database)
   - Test Framework: pytest + httpx
   - Component Types: Router, Service, Repository, Pydantic Models
   - Quality Gates: Pylint >= 8.5, Coverage >= 95%

✅ Framework instalado exitosamente en .claude/
✅ Perfil 'fastapi-rest' configurado
✅ Skills disponibles:
   - /implement-us
   - /track-pause, /track-resume, /track-status, /track-report, /track-history
✅ Templates instalados: bdd, planning, testing, reporting
✅ Tracking system initialized

🎉 Installation complete! Ready to use /implement-us
```

### 3. Verificar Instalación

```bash
# Verificar estructura creada
ls -la .claude/

# Contenido esperado:
# .claude/
# ├── skills/
# │   └── implement-us/
# │       ├── skill.md
# │       ├── config.json
# │       └── phases/
# ├── templates/
# │   ├── bdd/
# │   ├── planning/
# │   ├── testing/
# │   └── reporting/
# ├── tracking/
# └── config.json
```

**Ver configuración del perfil:**

```bash
cat .claude/skills/implement-us/config.json
```

---

## 🎬 Walkthrough: Las 10 Fases

### Preparación: Crear Archivo US

Primero, crea un archivo con la historia de usuario:

```bash
cat > historias-usuario/US-002.md << 'EOF'
# US-002: API de Tareas (TODO)

Como desarrollador frontend
Quiero una API REST para gestionar tareas
Para construir una aplicación TODO completa

## Criterios de Aceptación

- GET /tasks - Listar todas las tareas
- GET /tasks/{id} - Obtener tarea por ID
- POST /tasks - Crear nueva tarea con título y descripción
- PUT /tasks/{id} - Actualizar tarea (título, descripción, completada)
- DELETE /tasks/{id} - Eliminar tarea
- Validación automática de requests
- Documentación Swagger UI
- Manejo de errores (404 si task no existe)

## Notas Técnicas

- Framework: FastAPI
- Arquitectura: Capas (Router → Service → Database)
- Validación: Pydantic models
- Database: In-memory (dict) para demo
- Tests: pytest + httpx
EOF
```

### Ejecutar el Skill

Ahora, en Claude Code CLI:

```bash
# Iniciar Claude Code en el proyecto
cd ~/todo-api
claude

# En Claude Code, ejecutar:
/implement-us US-002
```

---

### 🔍 Fase 0: Validación de Contexto

**Qué hace el framework:**
- ✅ Verifica que el archivo `US-002.md` exista
- ✅ Lee el perfil `fastapi-rest` desde `.claude/skills/implement-us/config.json`
- ✅ Valida que FastAPI y pytest estén instalados
- ✅ Inicializa el tracking de tiempo

**Output:**

```
✅ Historia de usuario encontrada: US-002
✅ Perfil cargado: fastapi-rest
✅ Configuración:
   - Arquitectura: Layered (Router → Service → Database)
   - Component Types: Router, Service, Repository, Pydantic Models
   - Test Framework: pytest + httpx
   - Quality Gates: Pylint >= 8.5, Coverage >= 95%, CC < 10
⏱️  Tracking iniciado para US-002

🎯 Contexto validado. Procediendo a Fase 1...
```

**¿Qué hacer si falla?**
- Verifica que el archivo `historias-usuario/US-002.md` exista
- Confirma que la instalación del framework fue exitosa
- Revisa `.claude/skills/implement-us/config.json`
- Verifica que FastAPI esté instalado: `pip show fastapi`

---

### 📝 Fase 1: Generación de Escenarios BDD

**Qué hace el framework:**
- 📄 Lee tu historia de usuario (US-002.md)
- 🤖 Genera escenarios Gherkin basados en los criterios de aceptación
- 💾 Crea archivo `features/tasks.feature`

**Ejemplo de Output (FastAPI):**

```gherkin
# features/tasks.feature

Feature: Task Management API
  Como desarrollador frontend
  Quiero una API REST para gestionar tareas
  Para construir una aplicación TODO completa

  Background:
    Given the API is running
    And the database is empty

  Scenario: Create a new task
    When I create a task with title "Comprar leche" and description "Ir al supermercado"
    Then the response status code should be 201
    And the response should contain a task with title "Comprar leche"
    And the task should have an ID
    And the task should not be completed

  Scenario: List all tasks
    Given I have created a task with title "Tarea 1"
    And I have created a task with title "Tarea 2"
    When I request all tasks
    Then the response status code should be 200
    And the response should contain 2 tasks

  Scenario: Get a specific task
    Given I have created a task with title "Mi tarea"
    When I request the task by ID
    Then the response status code should be 200
    And the response should contain a task with title "Mi tarea"

  Scenario: Update a task
    Given I have created a task with title "Tarea pendiente"
    When I update the task to mark it as completed
    Then the response status code should be 200
    And the task should be completed

  Scenario: Delete a task
    Given I have created a task with title "Tarea a eliminar"
    When I delete the task by ID
    Then the response status code should be 204
    When I request the deleted task by ID
    Then the response status code should be 404

  Scenario: Error when getting non-existent task
    When I request a task with ID 999
    Then the response status code should be 404
```

**Archivo creado:**
```
features/tasks.feature (75 líneas, 6 escenarios)
```

**Interacción:**
Claude te mostrará los escenarios generados y preguntará:

```
📝 Escenarios BDD generados (6 escenarios, 75 líneas)

¿Aprobar estos escenarios? (Sí/No/Ajustar)
```

**Responde:** "Sí" (o ajusta si necesitas cambios específicos)

---

### 📋 Fase 2: Generación de Plan de Implementación

**Qué hace el framework:**
- 🏗️ Analiza los escenarios BDD
- 📊 Crea un plan de tareas desglosadas
- ⏱️ Estima tiempo por componente
- 🎯 Adapta la estructura a arquitectura en capas

**Ejemplo de Output (FastAPI):**

```markdown
# Plan de Implementación - US-002: API de Tareas (TODO)

## 📊 Resumen Ejecutivo

**Arquitectura:** Layered (Router → Service → Database)
**Estimación Total:** 2.5 horas
**Componentes:** 4 (Models, Router, Service, Database)
**Tests:** 23 (10 unitarios, 13 integración)

## 🏗️ Arquitectura

### Arquitectura en Capas

**Layer 1: Router (app/routes/tasks.py):**
- Responsabilidad: Endpoints HTTP, validación de requests
- Dependencias: FastAPI, Pydantic models, Service
- Métodos: GET /tasks, POST /tasks, PUT /tasks/{id}, DELETE /tasks/{id}

**Layer 2: Service (app/services/task_service.py):**
- Responsabilidad: Lógica de negocio
- Dependencias: Database, Pydantic models
- Métodos: create_task(), get_task(), get_all_tasks(), update_task(), delete_task()

**Layer 3: Database (app/database.py):**
- Responsabilidad: Acceso a datos
- Implementación: In-memory dict (demo)
- Métodos: save(), find_by_id(), find_all(), update(), delete()

**Models (app/models/task.py):**
- TaskCreate: Schema para crear tarea (title, description)
- TaskUpdate: Schema para actualizar tarea (partial)
- Task: Schema de respuesta completo (id, title, description, completed)

## 📝 Tareas

### 1. Pydantic Models - 20 min

**Archivo:** `app/models/task.py`

- [ ] TaskCreate (BaseModel)
  - title: str (min_length=1, max_length=200)
  - description: Optional[str] = None
- [ ] TaskUpdate (BaseModel)
  - title: Optional[str] = None
  - description: Optional[str] = None
  - completed: Optional[bool] = None
- [ ] Task (BaseModel)
  - id: int
  - title: str
  - description: Optional[str]
  - completed: bool = False
- [ ] Docstrings y ejemplos

**Complejidad:** Baja
**Dependencias:** Ninguna

### 2. Database Layer - 30 min

**Archivo:** `app/database.py`

- [ ] Clase TaskDatabase con dict interno
- [ ] Método save(task: Task) → Task
- [ ] Método find_by_id(task_id: int) → Optional[Task]
- [ ] Método find_all() → List[Task]
- [ ] Método update(task_id: int, updates: dict) → Optional[Task]
- [ ] Método delete(task_id: int) → bool
- [ ] Auto-incremento de IDs
- [ ] Thread-safety considerations (opcional)

**Complejidad:** Media
**Dependencias:** Task model

### 3. Service Layer - 40 min

**Archivo:** `app/services/task_service.py`

- [ ] Clase TaskService con dependency injection de database
- [ ] Método create_task(data: TaskCreate) → Task
- [ ] Método get_task(task_id: int) → Task (raise 404 si no existe)
- [ ] Método get_all_tasks() → List[Task]
- [ ] Método update_task(task_id: int, data: TaskUpdate) → Task
- [ ] Método delete_task(task_id: int) → None
- [ ] Validación de lógica de negocio
- [ ] Manejo de errores

**Complejidad:** Media
**Dependencias:** TaskDatabase, Pydantic models

### 4. Router Layer - 50 min

**Archivo:** `app/routes/tasks.py`

- [ ] APIRouter con prefix="/tasks"
- [ ] GET / - Listar todas las tareas
  - Response: List[Task]
  - Status: 200
- [ ] GET /{task_id} - Obtener tarea por ID
  - Response: Task
  - Status: 200 (success) | 404 (not found)
- [ ] POST / - Crear nueva tarea
  - Request: TaskCreate
  - Response: Task
  - Status: 201
- [ ] PUT /{task_id} - Actualizar tarea
  - Request: TaskUpdate
  - Response: Task
  - Status: 200 | 404
- [ ] DELETE /{task_id} - Eliminar tarea
  - Status: 204 | 404
- [ ] Dependency injection de TaskService
- [ ] Exception handlers

**Complejidad:** Media
**Dependencias:** TaskService, Pydantic models

### 5. Entry Point (main.py) - 15 min

**Archivo:** `main.py`

- [ ] Imports necesarios
- [ ] Crear FastAPI app
- [ ] Incluir router de tasks
- [ ] Configurar CORS (opcional)
- [ ] Configurar metadata (title, description, version)
- [ ] Run con uvicorn

**Complejidad:** Baja
**Dependencias:** Todos los componentes

## 🧪 Plan de Testing

### Tests Unitarios (10 tests)

**test_task_service.py:**
- test_create_task()
- test_get_task()
- test_get_task_not_found()
- test_get_all_tasks()
- test_update_task()
- test_update_task_partial()
- test_update_task_not_found()
- test_delete_task()
- test_delete_task_not_found()
- test_service_creation()

### Tests de Integración (13 tests)

**test_endpoints.py:**
- test_root()
- test_get_tasks_empty()
- test_create_task()
- test_create_task_validation_error()
- test_get_task_by_id()
- test_get_task_not_found()
- test_update_task()
- test_update_task_partial()
- test_update_task_not_found()
- test_delete_task()
- test_delete_task_not_found()
- test_get_tasks_with_data()
- test_create_task_without_description()

### BDD Step Definitions

**features/steps/task_steps.py:**
- Given steps: API running, database state
- When steps: HTTP requests (GET, POST, PUT, DELETE)
- Then steps: verificar responses, status codes

## 📊 Estimación por Fase

| Fase | Descripción | Estimado |
|------|-------------|----------|
| 3 | Implementación | 2.5h |
| 4 | Tests Unitarios | 45min |
| 5 | Tests Integración | 45min |
| 6 | BDD Validation | 30min |
| 7 | Quality Gates | 15min |
| 8 | Documentación | 20min |

**Total:** ~5 horas

## 🎯 Orden de Implementación

1. **Pydantic Models** (bottom-up, sin dependencias)
2. **Database Layer** (depende de Models)
3. **Service Layer** (depende de Database)
4. **Router Layer** (depende de Service)
5. **main.py** (integra todo)
6. **Tests unitarios** (paralelo a implementación)
7. **Tests integración** (después de integrar componentes)
8. **BDD steps** (al final)

## ⚠️ Riesgos

- **404 handling:** Asegurar respuestas consistentes cuando task no existe
- **Partial updates:** TaskUpdate debe permitir updates parciales (todos los campos opcionales)
- **ID generation:** Auto-incremento thread-safe si se usa concurrencia
- **Dependency injection:** Configurar correctamente get_db() y get_task_service()

## 📋 Checklist Pre-Implementación

- [x] Plan revisado y aprobado
- [x] Arquitectura en capas clara
- [x] Dependencias instaladas
- [x] Estructura de directorios lista
```

**Archivo creado:**
```
docs/planning/US-002-plan.md (180+ líneas)
```

**Interacción:**
Claude te mostrará el plan y preguntará:

```
📋 Plan de implementación generado

¿Proceder con la implementación? (Sí/Revisar/Ajustar)
```

**Responde:** "Sí"

---

### ⚙️ Fase 3: Implementación

**Qué hace el framework:**
- 💻 Guía la creación de cada componente según el plan
- 🔧 Usa snippets específicos del perfil fastapi-rest
- 📁 Crea archivos en la estructura correcta
- ✅ Valida cada paso antes de continuar

#### Componente 1: Pydantic Models

**Archivo:** `app/models/task.py`

Claude genera:

```python
"""
Pydantic models para la API de Tareas.

Define los schemas para validación de requests y responses.
"""

from typing import Optional
from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    """
    Schema para crear una nueva tarea.

    Attributes:
        title: Título de la tarea (requerido, 1-200 caracteres)
        description: Descripción opcional de la tarea
    """
    title: str = Field(..., min_length=1, max_length=200, description="Título de la tarea")
    description: Optional[str] = Field(None, description="Descripción de la tarea")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Comprar leche",
                    "description": "Ir al supermercado y comprar leche desnatada"
                }
            ]
        }
    }


class TaskUpdate(BaseModel):
    """
    Schema para actualizar una tarea existente.

    Permite updates parciales - todos los campos son opcionales.

    Attributes:
        title: Nuevo título (opcional)
        description: Nueva descripción (opcional)
        completed: Nuevo estado de completado (opcional)
    """
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    completed: Optional[bool] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "completed": True
                }
            ]
        }
    }


class Task(BaseModel):
    """
    Schema de respuesta para una tarea.

    Attributes:
        id: ID único de la tarea
        title: Título de la tarea
        description: Descripción de la tarea
        completed: Estado de completado (default: False)
    """
    id: int = Field(..., description="ID único de la tarea")
    title: str = Field(..., description="Título de la tarea")
    description: Optional[str] = Field(None, description="Descripción de la tarea")
    completed: bool = Field(default=False, description="Estado de completado")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "title": "Comprar leche",
                    "description": "Ir al supermercado",
                    "completed": False
                }
            ]
        }
    }
```

**Output:**

```
✅ Pydantic models creados (app/models/task.py)
   - TaskCreate con validación
   - TaskUpdate con partial updates
   - Task como response model
   - Field constraints y ejemplos

⏱️  Tiempo: 15 min (estimado: 20 min)
```

---

#### Componente 2: Database Layer

**Archivo:** `app/database.py`

```python
"""
In-memory database para la API de Tareas.

Proporciona CRUD operations sobre un dict en memoria.
Para producción, reemplazar con SQLAlchemy + PostgreSQL.
"""

from typing import Dict, List, Optional
from app.models.task import Task, TaskCreate, TaskUpdate


class TaskDatabase:
    """
    Base de datos en memoria para tareas.

    Attributes:
        _tasks: Dict que almacena las tareas por ID
        _next_id: Contador para auto-incremento de IDs
    """

    def __init__(self):
        """Inicializa la base de datos vacía."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def save(self, task_create: TaskCreate) -> Task:
        """
        Crea y guarda una nueva tarea.

        Args:
            task_create: Datos para crear la tarea

        Returns:
            La tarea creada con ID asignado
        """
        task = Task(
            id=self._next_id,
            title=task_create.title,
            description=task_create.description,
            completed=False
        )
        self._tasks[task.id] = task
        self._next_id += 1
        return task

    def find_by_id(self, task_id: int) -> Optional[Task]:
        """
        Busca una tarea por ID.

        Args:
            task_id: ID de la tarea a buscar

        Returns:
            La tarea si existe, None si no
        """
        return self._tasks.get(task_id)

    def find_all(self) -> List[Task]:
        """
        Obtiene todas las tareas.

        Returns:
            Lista de todas las tareas
        """
        return list(self._tasks.values())

    def update(self, task_id: int, task_update: TaskUpdate) -> Optional[Task]:
        """
        Actualiza una tarea existente.

        Args:
            task_id: ID de la tarea a actualizar
            task_update: Datos para actualizar (partial)

        Returns:
            La tarea actualizada si existe, None si no
        """
        task = self._tasks.get(task_id)
        if not task:
            return None

        # Crear dict con valores actualizados
        updated_data = task.model_dump()

        # Aplicar solo los campos provistos
        update_dict = task_update.model_dump(exclude_unset=True)
        updated_data.update(update_dict)

        # Crear nueva instancia con datos actualizados
        updated_task = Task(**updated_data)
        self._tasks[task_id] = updated_task

        return updated_task

    def delete(self, task_id: int) -> bool:
        """
        Elimina una tarea.

        Args:
            task_id: ID de la tarea a eliminar

        Returns:
            True si se eliminó, False si no existía
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def clear(self):
        """Limpia todas las tareas (útil para tests)."""
        self._tasks.clear()
        self._next_id = 1


# Instancia singleton para dependency injection
_db_instance: Optional[TaskDatabase] = None


def get_database() -> TaskDatabase:
    """
    Obtiene la instancia singleton de la database.

    Para usar con FastAPI Depends():
        def my_endpoint(db: TaskDatabase = Depends(get_database)):
            ...

    Returns:
        Instancia de TaskDatabase
    """
    global _db_instance
    if _db_instance is None:
        _db_instance = TaskDatabase()
    return _db_instance
```

**Output:**

```
✅ Database layer creado (app/database.py)
   - CRUD completo (Create, Read, Update, Delete)
   - Auto-incremento de IDs
   - Partial updates support
   - Dependency injection con get_database()

⏱️  Tiempo: 28 min (estimado: 30 min)
```

---

#### Componente 3: Service Layer

**Archivo:** `app/services/task_service.py`

```python
"""
Service layer para lógica de negocio de tareas.

Actúa como intermediario entre routers y database.
"""

from typing import List
from fastapi import HTTPException, status
from app.models.task import Task, TaskCreate, TaskUpdate
from app.database import TaskDatabase


class TaskService:
    """
    Service para manejar lógica de negocio de tareas.

    Attributes:
        db: Instancia de TaskDatabase
    """

    def __init__(self, db: TaskDatabase):
        """
        Inicializa el service.

        Args:
            db: Instancia de la database
        """
        self.db = db

    def create_task(self, task_create: TaskCreate) -> Task:
        """
        Crea una nueva tarea.

        Args:
            task_create: Datos para crear la tarea

        Returns:
            La tarea creada
        """
        return self.db.save(task_create)

    def get_task(self, task_id: int) -> Task:
        """
        Obtiene una tarea por ID.

        Args:
            task_id: ID de la tarea

        Returns:
            La tarea encontrada

        Raises:
            HTTPException: 404 si la tarea no existe
        """
        task = self.db.find_by_id(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id {task_id} not found"
            )
        return task

    def get_all_tasks(self) -> List[Task]:
        """
        Obtiene todas las tareas.

        Returns:
            Lista de todas las tareas
        """
        return self.db.find_all()

    def update_task(self, task_id: int, task_update: TaskUpdate) -> Task:
        """
        Actualiza una tarea existente.

        Args:
            task_id: ID de la tarea
            task_update: Datos para actualizar

        Returns:
            La tarea actualizada

        Raises:
            HTTPException: 404 si la tarea no existe
        """
        updated_task = self.db.update(task_id, task_update)
        if not updated_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id {task_id} not found"
            )
        return updated_task

    def delete_task(self, task_id: int) -> None:
        """
        Elimina una tarea.

        Args:
            task_id: ID de la tarea

        Raises:
            HTTPException: 404 si la tarea no existe
        """
        deleted = self.db.delete(task_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id {task_id} not found"
            )


def get_task_service(db: TaskDatabase) -> TaskService:
    """
    Factory function para dependency injection.

    Args:
        db: Instancia de la database

    Returns:
        Instancia de TaskService
    """
    return TaskService(db)
```

**Output:**

```
✅ Service layer creado (app/services/task_service.py)
   - 5 métodos de negocio
   - Manejo de errores con HTTPException
   - Dependency injection preparada
   - Lógica separada de HTTP

⏱️  Tiempo: 35 min (estimado: 40 min)
```

---

#### Componente 4: Router Layer

**Archivo:** `app/routes/tasks.py`

```python
"""
API Router para endpoints de tareas.

Define todos los endpoints REST de la API.
"""

from typing import List
from fastapi import APIRouter, Depends, status
from app.models.task import Task, TaskCreate, TaskUpdate
from app.services.task_service import TaskService, get_task_service
from app.database import get_database, TaskDatabase


# Crear router con prefix
router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)


@router.get("/", response_model=List[Task], status_code=status.HTTP_200_OK)
def get_all_tasks(
    service: TaskService = Depends(lambda db=Depends(get_database): get_task_service(db))
) -> List[Task]:
    """
    Obtener todas las tareas.

    Returns:
        Lista de todas las tareas
    """
    return service.get_all_tasks()


@router.get("/{task_id}", response_model=Task, status_code=status.HTTP_200_OK)
def get_task(
    task_id: int,
    service: TaskService = Depends(lambda db=Depends(get_database): get_task_service(db))
) -> Task:
    """
    Obtener una tarea por ID.

    Args:
        task_id: ID de la tarea

    Returns:
        La tarea encontrada

    Raises:
        HTTPException: 404 si la tarea no existe
    """
    return service.get_task(task_id)


@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(
    task_create: TaskCreate,
    service: TaskService = Depends(lambda db=Depends(get_database): get_task_service(db))
) -> Task:
    """
    Crear una nueva tarea.

    Args:
        task_create: Datos para crear la tarea

    Returns:
        La tarea creada con ID asignado
    """
    return service.create_task(task_create)


@router.put("/{task_id}", response_model=Task, status_code=status.HTTP_200_OK)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    service: TaskService = Depends(lambda db=Depends(get_database): get_task_service(db))
) -> Task:
    """
    Actualizar una tarea existente.

    Soporta partial updates - solo se actualizan los campos provistos.

    Args:
        task_id: ID de la tarea
        task_update: Datos para actualizar

    Returns:
        La tarea actualizada

    Raises:
        HTTPException: 404 si la tarea no existe
    """
    return service.update_task(task_id, task_update)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    service: TaskService = Depends(lambda db=Depends(get_database): get_task_service(db))
) -> None:
    """
    Eliminar una tarea.

    Args:
        task_id: ID de la tarea

    Raises:
        HTTPException: 404 si la tarea no existe
    """
    service.delete_task(task_id)
```

**Output:**

```
✅ Router creado (app/routes/tasks.py)
   - 5 endpoints REST (GET, POST, PUT, DELETE)
   - Response models con Pydantic
   - Status codes correctos
   - Dependency injection completa

⏱️  Tiempo: 45 min (estimado: 50 min)
```

---

#### Componente 5: Entry Point (main.py)

**Archivo:** `main.py`

```python
"""
Entry point de la FastAPI application.
"""

from fastapi import FastAPI
from app.routes import tasks


# Crear app
app = FastAPI(
    title="TODO API",
    description="Simple TODO API built with FastAPI",
    version="1.0.0"
)


# Incluir routers
app.include_router(tasks.router)


# Root endpoint
@app.get("/")
def root():
    """Root endpoint - welcome message."""
    return {"message": "Welcome to TODO API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Ejecutar la aplicación:**

```bash
# Development con auto-reload
uvicorn main:app --reload

# O directamente
python main.py
```

**Acceder a la documentación:**

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

**Output:**

```
✅ main.py creado (entry point)
✅ Aplicación ejecutable
✅ Swagger UI disponible en /docs

🎉 Implementación completa!
   - 4 capas (Models, Database, Service, Router)
   - 5 archivos Python (~540 líneas)
   - Arquitectura limpia y separada

⏱️  Tiempo total Fase 3: 2h 3min (estimado: 2.5h)
```

---

### 🧪 Fase 4: Tests Unitarios

**Qué hace el framework:**
- 🔬 Genera tests unitarios para service layer
- 🎯 Usa pytest con fixtures
- ✅ Cubre lógica de negocio y casos edge
- 📊 Ejecuta tests y reporta cobertura

**Archivo:** `tests/test_task_service.py`

```python
"""
Tests unitarios para TaskService.
"""

import pytest
from fastapi import HTTPException
from app.models.task import TaskCreate, TaskUpdate, Task
from app.services.task_service import TaskService
from app.database import TaskDatabase


@pytest.fixture
def db():
    """Fixture que proporciona una database limpia."""
    database = TaskDatabase()
    yield database
    database.clear()


@pytest.fixture
def service(db):
    """Fixture que proporciona un service con database limpia."""
    return TaskService(db)


class TestTaskService:
    """Suite de tests para TaskService."""

    def test_service_creation(self, db):
        """Test que el service se crea correctamente."""
        service = TaskService(db)
        assert service.db is db

    def test_create_task(self, service):
        """Test de creación de tarea."""
        task_create = TaskCreate(title="Test Task", description="Test Description")
        task = service.create_task(task_create)

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.completed is False

    def test_get_task(self, service):
        """Test de obtener tarea por ID."""
        # Crear tarea primero
        task_create = TaskCreate(title="Test Task")
        created_task = service.create_task(task_create)

        # Obtener por ID
        task = service.get_task(created_task.id)
        assert task.id == created_task.id
        assert task.title == "Test Task"

    def test_get_task_not_found(self, service):
        """Test que get_task lanza 404 si no existe."""
        with pytest.raises(HTTPException) as exc_info:
            service.get_task(999)

        assert exc_info.value.status_code == 404
        assert "not found" in exc_info.value.detail.lower()

    def test_get_all_tasks(self, service):
        """Test de obtener todas las tareas."""
        # Crear varias tareas
        service.create_task(TaskCreate(title="Task 1"))
        service.create_task(TaskCreate(title="Task 2"))
        service.create_task(TaskCreate(title="Task 3"))

        # Obtener todas
        tasks = service.get_all_tasks()
        assert len(tasks) == 3
        assert tasks[0].title == "Task 1"
        assert tasks[1].title == "Task 2"
        assert tasks[2].title == "Task 3"

    def test_update_task(self, service):
        """Test de actualización completa de tarea."""
        # Crear tarea
        task_create = TaskCreate(title="Original Title")
        created_task = service.create_task(task_create)

        # Actualizar
        task_update = TaskUpdate(
            title="Updated Title",
            description="New description",
            completed=True
        )
        updated_task = service.update_task(created_task.id, task_update)

        assert updated_task.title == "Updated Title"
        assert updated_task.description == "New description"
        assert updated_task.completed is True

    def test_update_task_partial(self, service):
        """Test de actualización parcial (solo algunos campos)."""
        # Crear tarea
        task_create = TaskCreate(title="Original", description="Original desc")
        created_task = service.create_task(task_create)

        # Update parcial - solo completed
        task_update = TaskUpdate(completed=True)
        updated_task = service.update_task(created_task.id, task_update)

        # Title y description no cambian
        assert updated_task.title == "Original"
        assert updated_task.description == "Original desc"
        # Solo completed cambió
        assert updated_task.completed is True

    def test_update_task_not_found(self, service):
        """Test que update_task lanza 404 si no existe."""
        task_update = TaskUpdate(title="New Title")

        with pytest.raises(HTTPException) as exc_info:
            service.update_task(999, task_update)

        assert exc_info.value.status_code == 404

    def test_delete_task(self, service):
        """Test de eliminación de tarea."""
        # Crear tarea
        task_create = TaskCreate(title="To Delete")
        created_task = service.create_task(task_create)

        # Eliminar
        service.delete_task(created_task.id)

        # Verificar que no existe
        with pytest.raises(HTTPException):
            service.get_task(created_task.id)

    def test_delete_task_not_found(self, service):
        """Test que delete_task lanza 404 si no existe."""
        with pytest.raises(HTTPException) as exc_info:
            service.delete_task(999)

        assert exc_info.value.status_code == 404
```

**Ejecutar tests unitarios:**

```bash
pytest tests/test_task_service.py -v
```

**Output Esperado:**

```
============================= test session starts ==============================
collected 10 items

tests/test_task_service.py::TestTaskService::test_service_creation PASSED [ 10%]
tests/test_task_service.py::TestTaskService::test_create_task PASSED     [ 20%]
tests/test_task_service.py::TestTaskService::test_get_task PASSED        [ 30%]
tests/test_task_service.py::TestTaskService::test_get_task_not_found PASSED [ 40%]
tests/test_task_service.py::TestTaskService::test_get_all_tasks PASSED   [ 50%]
tests/test_task_service.py::TestTaskService::test_update_task PASSED     [ 60%]
tests/test_task_service.py::TestTaskService::test_update_task_partial PASSED [ 70%]
tests/test_task_service.py::TestTaskService::test_update_task_not_found PASSED [ 80%]
tests/test_task_service.py::TestTaskService::test_delete_task PASSED     [ 90%]
tests/test_task_service.py::TestTaskService::test_delete_task_not_found PASSED [100%]

============================== 10 passed in 0.15s ===============================
```

**Output:**

```
✅ Tests unitarios creados (10 tests)
✅ Todos los tests pasando
✅ Service layer completamente testado

⏱️  Tiempo Fase 4: 40 min (estimado: 45 min)
```

---

### 🔗 Fase 5: Tests de Integración

**Qué hace el framework:**
- 🌐 Genera tests end-to-end de la API
- 🔄 Usa TestClient de FastAPI con httpx
- 🎭 Valida requests y responses HTTP reales

**Archivo:** `tests/conftest.py`

```python
"""
Fixtures compartidos para tests.
"""

import pytest
from fastapi.testclient import TestClient
from main import app
from app.database import TaskDatabase, _db_instance


@pytest.fixture(autouse=True)
def reset_database():
    """
    Resetea la database antes de cada test.

    Esto asegura que cada test comience con database limpia.
    """
    global _db_instance
    if _db_instance:
        _db_instance.clear()
    yield
    if _db_instance:
        _db_instance.clear()


@pytest.fixture
def client():
    """
    Proporciona TestClient para tests de integración.

    Returns:
        TestClient configurado con la app
    """
    return TestClient(app)
```

**Archivo:** `tests/test_endpoints.py`

```python
"""
Tests de integración de endpoints de la API.
"""

import pytest
from fastapi.testclient import TestClient


class TestRootEndpoint:
    """Tests del endpoint raíz."""

    def test_root(self, client: TestClient):
        """Test del endpoint raíz."""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to TODO API"}


class TestGetTasks:
    """Tests de GET /tasks."""

    def test_get_tasks_empty(self, client: TestClient):
        """Test de GET /tasks cuando no hay tareas."""
        response = client.get("/tasks/")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_tasks_with_data(self, client: TestClient):
        """Test de GET /tasks con tareas creadas."""
        # Crear algunas tareas
        client.post("/tasks/", json={"title": "Task 1"})
        client.post("/tasks/", json={"title": "Task 2"})

        # Obtener todas
        response = client.get("/tasks/")
        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) == 2
        assert tasks[0]["title"] == "Task 1"
        assert tasks[1]["title"] == "Task 2"

    def test_get_task_by_id(self, client: TestClient):
        """Test de GET /tasks/{id}."""
        # Crear tarea
        create_response = client.post("/tasks/", json={"title": "My Task"})
        task_id = create_response.json()["id"]

        # Obtener por ID
        response = client.get(f"/tasks/{task_id}")
        assert response.status_code == 200
        task = response.json()
        assert task["id"] == task_id
        assert task["title"] == "My Task"

    def test_get_task_not_found(self, client: TestClient):
        """Test de GET /tasks/{id} cuando no existe."""
        response = client.get("/tasks/999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestCreateTask:
    """Tests de POST /tasks."""

    def test_create_task(self, client: TestClient):
        """Test de creación de tarea."""
        task_data = {
            "title": "Comprar leche",
            "description": "Ir al supermercado"
        }

        response = client.post("/tasks/", json=task_data)
        assert response.status_code == 201

        task = response.json()
        assert task["id"] == 1
        assert task["title"] == "Comprar leche"
        assert task["description"] == "Ir al supermercado"
        assert task["completed"] is False

    def test_create_task_without_description(self, client: TestClient):
        """Test de creación sin description (campo opcional)."""
        task_data = {"title": "Simple Task"}

        response = client.post("/tasks/", json=task_data)
        assert response.status_code == 201

        task = response.json()
        assert task["title"] == "Simple Task"
        assert task["description"] is None

    def test_create_task_validation_error(self, client: TestClient):
        """Test de validación - title requerido."""
        task_data = {"description": "Missing title"}

        response = client.post("/tasks/", json=task_data)
        assert response.status_code == 422  # Validation error


class TestUpdateTask:
    """Tests de PUT /tasks/{id}."""

    def test_update_task(self, client: TestClient):
        """Test de actualización completa."""
        # Crear tarea
        create_response = client.post("/tasks/", json={"title": "Original"})
        task_id = create_response.json()["id"]

        # Actualizar
        update_data = {
            "title": "Updated",
            "description": "New description",
            "completed": True
        }
        response = client.put(f"/tasks/{task_id}", json=update_data)

        assert response.status_code == 200
        task = response.json()
        assert task["title"] == "Updated"
        assert task["description"] == "New description"
        assert task["completed"] is True

    def test_update_task_partial(self, client: TestClient):
        """Test de actualización parcial."""
        # Crear tarea
        create_response = client.post("/tasks/", json={
            "title": "Original",
            "description": "Original desc"
        })
        task_id = create_response.json()["id"]

        # Update parcial - solo completed
        update_data = {"completed": True}
        response = client.put(f"/tasks/{task_id}", json=update_data)

        assert response.status_code == 200
        task = response.json()
        assert task["title"] == "Original"  # No cambió
        assert task["description"] == "Original desc"  # No cambió
        assert task["completed"] is True  # Cambió

    def test_update_task_not_found(self, client: TestClient):
        """Test de update cuando tarea no existe."""
        update_data = {"title": "Updated"}
        response = client.put("/tasks/999", json=update_data)

        assert response.status_code == 404


class TestDeleteTask:
    """Tests de DELETE /tasks/{id}."""

    def test_delete_task(self, client: TestClient):
        """Test de eliminación de tarea."""
        # Crear tarea
        create_response = client.post("/tasks/", json={"title": "To Delete"})
        task_id = create_response.json()["id"]

        # Eliminar
        response = client.delete(f"/tasks/{task_id}")
        assert response.status_code == 204

        # Verificar que no existe
        get_response = client.get(f"/tasks/{task_id}")
        assert get_response.status_code == 404

    def test_delete_task_not_found(self, client: TestClient):
        """Test de delete cuando tarea no existe."""
        response = client.delete("/tasks/999")
        assert response.status_code == 404
```

**Ejecutar tests de integración:**

```bash
pytest tests/test_endpoints.py -v
```

**Output Esperado:**

```
============================= test session starts ==============================
collected 13 items

tests/test_endpoints.py::TestRootEndpoint::test_root PASSED             [  7%]
tests/test_endpoints.py::TestGetTasks::test_get_tasks_empty PASSED      [ 15%]
tests/test_endpoints.py::TestGetTasks::test_get_tasks_with_data PASSED  [ 23%]
tests/test_endpoints.py::TestGetTasks::test_get_task_by_id PASSED       [ 30%]
tests/test_endpoints.py::TestGetTasks::test_get_task_not_found PASSED   [ 38%]
tests/test_endpoints.py::TestCreateTask::test_create_task PASSED        [ 46%]
tests/test_endpoints.py::TestCreateTask::test_create_task_without_description PASSED [ 53%]
tests/test_endpoints.py::TestCreateTask::test_create_task_validation_error PASSED [ 61%]
tests/test_endpoints.py::TestUpdateTask::test_update_task PASSED        [ 69%]
tests/test_endpoints.py::TestUpdateTask::test_update_task_partial PASSED [ 76%]
tests/test_endpoints.py::TestUpdateTask::test_update_task_not_found PASSED [ 84%]
tests/test_endpoints.py::TestDeleteTask::test_delete_task PASSED        [ 92%]
tests/test_endpoints.py::TestDeleteTask::test_delete_task_not_found PASSED [100%]

============================== 13 passed in 0.45s ===============================
```

**Ejecutar todos los tests con cobertura:**

```bash
pytest --cov=app --cov-report=term-missing
```

**Output:**

```
✅ Tests de integración creados (13 tests)
✅ Todos los tests pasando
✅ Cobertura: 98% (objetivo: >= 95%)

⏱️  Tiempo Fase 5: 42 min (estimado: 45 min)
```

---

### ✅ Fase 6: Validación BDD

**Qué hace el framework:**
- 🥒 Genera step definitions para los escenarios Gherkin
- 🔗 Conecta los escenarios con el código real usando pytest-bdd
- ✅ Ejecuta validación completa

**Archivo:** `features/steps/task_steps.py`

```python
"""
Step definitions para scenarios BDD de la API de Tareas.
"""

import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from fastapi.testclient import TestClient
from main import app
from app.database import get_database


# Cargar todos los escenarios del feature file
scenarios('../tasks.feature')


@pytest.fixture
def context():
    """
    Contexto compartido para los steps.

    Proporciona:
    - client: TestClient para hacer requests
    - response: Última respuesta HTTP
    - created_tasks: Lista de tasks creadas durante el test
    """
    client = TestClient(app)

    # Limpiar database antes de cada scenario
    db = get_database()
    db.clear()

    return {
        'client': client,
        'response': None,
        'created_tasks': []
    }


# ============================================================================
# GIVEN steps
# ============================================================================

@given('the API is running')
def api_is_running(context):
    """Verifica que la API esté accesible."""
    response = context['client'].get("/")
    assert response.status_code == 200


@given('the database is empty')
def database_is_empty(context):
    """Verifica que la database esté vacía."""
    response = context['client'].get("/tasks/")
    assert response.json() == []


@given(parsers.parse('I have created a task with title "{title}"'))
def i_have_created_task(context, title):
    """Crea una tarea con el título dado."""
    response = context['client'].post("/tasks/", json={"title": title})
    assert response.status_code == 201
    task = response.json()
    context['created_tasks'].append(task)


# ============================================================================
# WHEN steps
# ============================================================================

@when(parsers.parse('I create a task with title "{title}" and description "{description}"'))
def i_create_task_with_title_and_description(context, title, description):
    """Crea una tarea con título y descripción."""
    task_data = {"title": title, "description": description}
    context['response'] = context['client'].post("/tasks/", json=task_data)


@when('I request all tasks')
def i_request_all_tasks(context):
    """Solicita todas las tareas."""
    context['response'] = context['client'].get("/tasks/")


@when('I request the task by ID')
def i_request_task_by_id(context):
    """Solicita la última tarea creada por ID."""
    task_id = context['created_tasks'][-1]['id']
    context['response'] = context['client'].get(f"/tasks/{task_id}")


@when('I update the task to mark it as completed')
def i_update_task_as_completed(context):
    """Actualiza la última tarea creada a completada."""
    task_id = context['created_tasks'][-1]['id']
    update_data = {"completed": True}
    context['response'] = context['client'].put(f"/tasks/{task_id}", json=update_data)


@when('I delete the task by ID')
def i_delete_task_by_id(context):
    """Elimina la última tarea creada."""
    task_id = context['created_tasks'][-1]['id']
    context['response'] = context['client'].delete(f"/tasks/{task_id}")


@when('I request the deleted task by ID')
def i_request_deleted_task(context):
    """Intenta obtener la tarea eliminada."""
    task_id = context['created_tasks'][-1]['id']
    context['response'] = context['client'].get(f"/tasks/{task_id}")


@when(parsers.parse('I request a task with ID {task_id:d}'))
def i_request_task_with_id(context, task_id):
    """Solicita una tarea por ID específico."""
    context['response'] = context['client'].get(f"/tasks/{task_id}")


# ============================================================================
# THEN steps
# ============================================================================

@then(parsers.parse('the response status code should be {status_code:d}'))
def response_status_code_should_be(context, status_code):
    """Verifica el código de estado HTTP."""
    assert context['response'].status_code == status_code


@then(parsers.parse('the response should contain a task with title "{title}"'))
def response_should_contain_task_with_title(context, title):
    """Verifica que la respuesta contenga una tarea con el título dado."""
    task = context['response'].json()
    assert task['title'] == title


@then('the task should have an ID')
def task_should_have_id(context):
    """Verifica que la tarea tenga un ID."""
    task = context['response'].json()
    assert 'id' in task
    assert isinstance(task['id'], int)


@then('the task should not be completed')
def task_should_not_be_completed(context):
    """Verifica que la tarea no esté completada."""
    task = context['response'].json()
    assert task['completed'] is False


@then(parsers.parse('the response should contain {count:d} tasks'))
def response_should_contain_n_tasks(context, count):
    """Verifica la cantidad de tareas en la respuesta."""
    tasks = context['response'].json()
    assert len(tasks) == count


@then('the task should be completed')
def task_should_be_completed(context):
    """Verifica que la tarea esté completada."""
    task = context['response'].json()
    assert task['completed'] is True
```

**Ejecutar validación BDD:**

```bash
pytest features/steps/ -v
```

**Output Esperado:**

```
============================= test session starts ==============================
collected 6 items

features/steps/task_steps.py::test_create_a_new_task PASSED            [ 16%]
features/steps/task_steps.py::test_list_all_tasks PASSED               [ 33%]
features/steps/task_steps.py::test_get_a_specific_task PASSED          [ 50%]
features/steps/task_steps.py::test_update_a_task PASSED                [ 66%]
features/steps/task_steps.py::test_delete_a_task PASSED                [ 83%]
features/steps/task_steps.py::test_error_when_getting_non_existent_task PASSED [100%]

============================== 6 passed in 0.65s ===============================
```

**Output:**

```
✅ BDD step definitions creadas
✅ 6 escenarios BDD pasando (100%)
✅ Criterios de aceptación validados

⏱️  Tiempo Fase 6: 30 min (estimado: 30 min)
```

---

### 📊 Fase 7: Quality Gates

**Qué hace el framework:**
- 🔍 Ejecuta Pylint con umbrales del perfil fastapi-rest
- 📈 Calcula complejidad ciclomática
- 🎯 Valida índice de mantenibilidad
- 📊 Verifica cobertura de tests

**Umbrales (fastapi-rest):**
- **Pylint:** >= 8.5/10
- **Coverage:** >= 95%
- **Complejidad Ciclomática:** < 10 por función
- **Índice de Mantenibilidad:** >= 25

**Ejecución:**

```bash
# 1. Pylint
pylint app/ --fail-under=8.5

# 2. Complejidad Ciclomática
radon cc app/ -a

# 3. Índice de Mantenibilidad
radon mi app/ -s

# 4. Cobertura
pytest --cov=app --cov-report=term --cov-fail-under=95
```

**Output Esperado:**

```
# Pylint
--------------------------------------------------------------------
Your code has been rated at 9.71/10 (previous run: 9.71/10, +0.00)
✅ PASSED (threshold: 8.5)

# Complejidad Ciclomática
app/database.py
    M 71:4 TaskDatabase.update - A (4)
    C 25:4 TaskDatabase.save - A (1)
    C 41:4 TaskDatabase.find_by_id - A (1)
    C 53:4 TaskDatabase.find_all - A (1)
    C 90:4 TaskDatabase.delete - A (2)

Average complexity: A (1.32)
✅ PASSED (all functions < 10)

# Índice de Mantenibilidad
app/models/task.py - A (55.06)
app/database.py - A (79.50)
app/services/task_service.py - A (81.26)
app/routes/tasks.py - A (84.60)

Average: A (75.11)
✅ PASSED (all modules >= 25)

# Cobertura
---------- coverage: platform darwin, python 3.11.5 -----------
Name                              Stmts   Miss  Cover
-----------------------------------------------------
app/__init__.py                       1      0   100%
app/models/__init__.py                2      0   100%
app/models/task.py                   19      0   100%
app/routes/__init__.py                2      0   100%
app/routes/tasks.py                  30      0   100%
app/services/__init__.py              2      0   100%
app/services/task_service.py         19      1    95%
app/database.py                      35      1    97%
-----------------------------------------------------
TOTAL                               110      2    98%

✅ PASSED (threshold: 95%)
```

**Output:**

```
✅ Quality gates pasados:
   - Pylint: 9.71/10 (objetivo: >= 8.5)
   - Coverage: 98% (objetivo: >= 95%)
   - Complejidad: Promedio 1.32 (objetivo: < 10)
   - Mantenibilidad: Promedio 75.11 (objetivo: >= 25)

⏱️  Tiempo Fase 7: 15 min (estimado: 15 min)
```

---

### 📚 Fase 8: Documentación

**Qué hace el framework:**
- 📖 Genera README.md del proyecto
- 🗂️ Documenta endpoints de la API
- 💡 Incluye ejemplos de uso
- 🏗️ Documenta decisiones arquitectónicas (ADR)

**Archivos creados:**

1. **README.md** (raíz del proyecto) - 219 líneas
2. **docs/architecture/ADR-001-layered-architecture.md**

**README.md incluye:**
- Descripción del proyecto
- Features principales
- Arquitectura (Router → Service → Database)
- Instrucciones de instalación y ejecución
- Documentación de endpoints
- Ejemplos curl
- Cómo ejecutar tests
- Estructura del proyecto

**Output:**

```
✅ Documentación generada:
   - README.md actualizado (219 líneas)
   - ADR-001: Decisión de usar arquitectura en capas
   - Ejemplos de uso con curl
   - Swagger UI disponible en /docs

⏱️  Tiempo Fase 8: 20 min (estimado: 20 min)
```

---

### 📈 Fase 9: Reporte Final

**Qué hace el framework:**
- 📋 Consolida métricas de todas las fases
- ⏱️ Reporta tiempo real vs estimado
- ✅ Lista criterios de aceptación cumplidos
- 📊 Genera reporte completo

**Archivo creado:**

```
docs/reporting/US-002-report.md
```

**Contenido del Reporte:**

```markdown
# Reporte de Implementación: US-002 - API de Tareas (TODO)

## 📊 Resumen Ejecutivo

- **Estado:** ✅ Completado
- **Tiempo Total:** 4h 45min (estimado: 5h)
- **Tests:** 29/29 pasando (100%)
- **Cobertura:** 98%
- **Quality Gates:** ✅ Todos aprobados

## 📝 Componentes Implementados

### 1. Pydantic Models (app/models/task.py)
- **Líneas:** 95
- **Schemas:** 3 (TaskCreate, TaskUpdate, Task)
- **Validación:** Field constraints

### 2. Database Layer (app/database.py)
- **Líneas:** 130
- **Métodos:** 7 CRUD operations
- **Cobertura:** 97%

### 3. Service Layer (app/services/task_service.py)
- **Líneas:** 85
- **Métodos:** 5
- **Cobertura:** 95%

### 4. Router Layer (app/routes/tasks.py)
- **Líneas:** 115
- **Endpoints:** 5 REST endpoints
- **Cobertura:** 100%

### 5. main.py
- **Líneas:** 23
- **Complejidad:** 1.0

**Total:** 448 líneas de código

## 🧪 Testing

### Tests Unitarios
- **Archivos:** 1
- **Tests:** 10
- **Estado:** ✅ 10/10 pasando (100%)
- **Tiempo:** 0.15s

### Tests de Integración
- **Archivos:** 1
- **Tests:** 13
- **Estado:** ✅ 13/13 pasando (100%)
- **Tiempo:** 0.45s

### Escenarios BDD
- **Archivos:** 1 feature + 1 steps
- **Escenarios:** 6
- **Estado:** ✅ 6/6 pasando (100%)
- **Tiempo:** 0.65s

**Total:** 29 tests, 100% pasando, ~1.25s de ejecución

## 📊 Métricas de Calidad

### Pylint
- **Puntuación:** 9.71/10
- **Umbral:** >= 8.5
- **Estado:** ✅ PASSED

### Complejidad Ciclomática
- **Promedio:** 1.32
- **Máxima:** 4 (TaskDatabase.update)
- **Umbral:** < 10
- **Estado:** ✅ PASSED

### Índice de Mantenibilidad
- **Promedio:** 75.11
- **Mínimo:** 55.06 (task.py)
- **Umbral:** >= 25
- **Estado:** ✅ PASSED

### Cobertura de Tests
- **Cobertura:** 98%
- **Umbral:** >= 95%
- **Estado:** ✅ PASSED

## ✅ Criterios de Aceptación

| Criterio | Estado | Validación |
|----------|--------|------------|
| GET /tasks - Listar tareas | ✅ | 2 tests + BDD |
| GET /tasks/{id} - Obtener por ID | ✅ | 2 tests + BDD |
| POST /tasks - Crear tarea | ✅ | 3 tests + BDD |
| PUT /tasks/{id} - Actualizar | ✅ | 3 tests + BDD |
| DELETE /tasks/{id} - Eliminar | ✅ | 2 tests + BDD |
| Validación Pydantic | ✅ | 1 test |
| Documentación Swagger | ✅ | Generada automáticamente |
| Manejo de errores 404 | ✅ | 4 tests + BDD |

**Total:** 8/8 criterios cumplidos (100%)

## ⏱️ Tracking de Tiempo

| Fase | Descripción | Estimado | Real | Varianza |
|------|-------------|----------|------|----------|
| 0 | Validación | - | 2min | - |
| 1 | BDD Generation | - | 5min | - |
| 2 | Planning | - | 10min | - |
| 3 | Implementación | 2.5h | 2h 3min | -19% |
| 4 | Tests Unitarios | 45min | 40min | -11% |
| 5 | Tests Integración | 45min | 42min | -7% |
| 6 | BDD Validation | 30min | 30min | 0% |
| 7 | Quality Gates | 15min | 15min | 0% |
| 8 | Documentación | 20min | 20min | 0% |
| 9 | Reporte | - | 8min | - |

**Total:** 4h 45min (estimado: 5h, -5%)
```

**Output:**

```
✅ Reporte final generado (docs/reporting/US-002-report.md)
✅ Métricas consolidadas
✅ Tracking de tiempo completo

⏱️  Tiempo Fase 9: 8 min

🎉 ¡IMPLEMENTACIÓN COMPLETA!
```

---

## ✅ Validación Final

### Checklist Completo

**Código:**
- [x] Todos los componentes implementados (Models, Database, Service, Router, main)
- [x] Código sigue arquitectura en capas
- [x] Docstrings y type hints presentes
- [x] Código ejecutable sin errores

**Tests:**
- [x] Tests unitarios al 100% passing (10/10)
- [x] Tests de integración al 100% passing (13/13)
- [x] Escenarios BDD validados (6/6)
- [x] Cobertura >= 95% (actual: 98%)

**Calidad:**
- [x] Pylint >= 8.5 (actual: 9.71)
- [x] Complejidad Ciclomática < 10 (actual: máx 4)
- [x] Cobertura >= 95% (actual: 98%)

**Documentación:**
- [x] README actualizado
- [x] Documentación API con Swagger
- [x] ADRs documentados

**Tracking:**
- [x] Reporte de tiempo generado
- [x] Métricas capturadas

### Ejecutar Aplicación

```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar API
python main.py

# O con uvicorn
uvicorn main:app --reload
```

**Verificación Manual:**

1. **Abrir Swagger UI:**
   - URL: http://localhost:8000/docs

2. **Test de Crear Tarea:**
   ```bash
   curl -X POST http://localhost:8000/tasks/ \
     -H "Content-Type: application/json" \
     -d '{"title": "Comprar leche", "description": "Ir al supermercado"}'
   ```
   - Esperado: Status 201, tarea creada con ID ✅

3. **Test de Listar Tareas:**
   ```bash
   curl http://localhost:8000/tasks/
   ```
   - Esperado: Array con la tarea creada ✅

4. **Test de Actualizar:**
   ```bash
   curl -X PUT http://localhost:8000/tasks/1 \
     -H "Content-Type: application/json" \
     -d '{"completed": true}'
   ```
   - Esperado: Tarea actualizada ✅

5. **Test de Eliminar:**
   ```bash
   curl -X DELETE http://localhost:8000/tasks/1
   ```
   - Esperado: Status 204 No Content ✅

---

## 🔧 Troubleshooting

### Problema: Tests fallan con "database not empty"

**Solución:**
El fixture `reset_database` en conftest.py debe ejecutarse antes de cada test. Verificar que `autouse=True` esté configurado.

### Problema: Import errors al ejecutar tests

**Solución:**
```bash
# Asegurar que el módulo esté en PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# O crear pytest.ini
cat > pytest.ini << EOF
[pytest]
pythonpath = .
EOF
```

### Problema: FastAPI no instala correctamente

**Solución:**
```bash
# Reinstalar con todas las dependencias
pip uninstall fastapi uvicorn
pip install "fastapi[all]" "uvicorn[standard]" --no-cache-dir
```

### Problema: Swagger UI muestra "Failed to load API definition"

**Solución:**
- Verificar que la app esté ejecutándose: `curl http://localhost:8000/`
- Revisar logs de uvicorn para errores
- Asegurar que el router esté incluido correctamente en main.py

### Problema: pytest-bdd no encuentra los scenarios

**Solución:**
```python
# En task_steps.py, asegurar que la ruta sea correcta
scenarios('../tasks.feature')  # Relativo al archivo task_steps.py
```

---

## 🚀 Próximos Pasos

### Ampliar la API

1. **Agregar persistencia real:**
   - Reemplazar TaskDatabase con SQLAlchemy + PostgreSQL
   - Agregar migraciones con Alembic

2. **Agregar autenticación:**
   - Implementar JWT authentication
   - Usar fastapi-users o authlib

3. **Agregar paginación:**
   - GET /tasks?skip=0&limit=10
   - Headers con metadata (total, page, etc.)

4. **Agregar filtros:**
   - GET /tasks?completed=true
   - GET /tasks?search=comprar

5. **Agregar background tasks:**
   - Envío de emails
   - Procesamiento asíncrono

### Explorar Otros Perfiles

El Claude Dev Kit soporta múltiples stacks:

- **PyQt-MVC:** Apps de escritorio
- **FastAPI-REST:** APIs async de alto rendimiento (este tutorial)
- **Flask-REST:** APIs REST simples
- **Flask-WebApp:** Aplicaciones web fullstack
- **Generic-Python:** Proyectos Python genéricos

```bash
python ~/.claude-dev-kit/install/installer.py --profile flask-rest --yes
```

### Contribuir al Framework

- Reporta issues en GitHub: https://github.com/vvalotto/claude-dev-kit/issues
- Propón mejoras a los templates
- Comparte tus propios perfiles customizados

---

## 📚 Recursos

### Documentación del Framework

- [Guía de Inicio Rápido](../user/Getting-Started.md)
- [Referencia del Skill implement-us](../user/Implement-US-Skill.md)
- [Sistema de Tracking](../user/Tracking-Guide.md)
- [Personalización de Perfiles](../user/Customization.md)

### Documentación de FastAPI

- **Oficial:** https://fastapi.tiangolo.com/
- **Tutorial:** https://fastapi.tiangolo.com/tutorial/
- **Deployment:** https://fastapi.tiangolo.com/deployment/
- **Advanced User Guide:** https://fastapi.tiangolo.com/advanced/

### Documentación de Pydantic

- **Oficial:** https://docs.pydantic.dev/latest/
- **Models:** https://docs.pydantic.dev/latest/concepts/models/
- **Validation:** https://docs.pydantic.dev/latest/concepts/validators/

### Documentación de pytest

- **Oficial:** https://docs.pytest.org/
- **pytest-bdd:** https://pytest-bdd.readthedocs.io/
- **pytest-cov:** https://pytest-cov.readthedocs.io/

### Comunidad

- **GitHub:** https://github.com/vvalotto/claude-dev-kit
- **Issues:** https://github.com/vvalotto/claude-dev-kit/issues
- **Discussions:** https://github.com/vvalotto/claude-dev-kit/discussions

---

## 📝 Conclusión

¡Felicidades! Has completado tu primer proyecto FastAPI usando el Claude Dev Kit con el perfil **fastapi-rest**.

**Lo que aprendiste:**
- ✅ Instalación y configuración del framework para FastAPI
- ✅ Uso del skill `/implement-us` para guiar implementación
- ✅ Aplicación de arquitectura en capas (Router → Service → Database)
- ✅ Testing completo: unitario, integración y BDD
- ✅ Validación de calidad con quality gates
- ✅ Tracking de tiempo y métricas
- ✅ Generación automática de documentación con Swagger

**Métricas finales del tutorial:**
- **Código:** 448 líneas (Models, Database, Service, Router)
- **Tests:** 29 tests (100% pasando)
- **Cobertura:** 98%
- **Quality:** Pylint 9.71/10
- **Tiempo:** 4h 45min (estimado: 5h)

**Siguiente paso:** Aplica este mismo proceso a tus propios proyectos FastAPI. El framework está diseñado para escalar desde prototipos simples hasta APIs complejas de producción.

¡Ahora eres capaz de construir APIs REST profesionales con arquitectura limpia, tests completos y calidad validada!

---

**Tutorial Creado:** 2026-02-16
**Claude Dev Kit:** v1.0
**Perfil:** fastapi-rest
