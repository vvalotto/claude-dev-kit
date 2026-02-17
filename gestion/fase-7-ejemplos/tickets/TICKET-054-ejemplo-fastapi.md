# TICKET-054: Tutorial FastAPI-REST Completo 🚀

**Fase:** 7 - Ejemplos por Stack
**Sprint:** 4
**Estado:** ✅ Completado
**Prioridad:** Alta
**Estimación:** 2.5 horas
**Asignado a:** Claude Code

## Descripción

Crear tutorial end-to-end completo para el stack **FastAPI-REST**, demostrando el uso del framework Claude Dev Kit para implementar una API REST asíncrona.

**Historia de Usuario:**
```
US-002: API de Tareas (TODO)

Como developer,
Quiero una API REST para gestionar tareas
Para integrar con mi aplicación frontend

Criterios de Aceptación:
- GET /tasks - Listar todas las tareas
- POST /tasks - Crear nueva tarea
- PUT /tasks/{id} - Actualizar tarea existente
- DELETE /tasks/{id} - Eliminar tarea
- Validación con Pydantic
- Documentación auto-generada (Swagger)
- Tests con pytest + httpx
```

## Criterios de Aceptación

### Contenido del Tutorial

- [ ] **Introducción clara** - API REST asíncrona con FastAPI
- [ ] **Requisitos** - Python 3.9+, FastAPI, uvicorn, pytest, httpx
- [ ] **Setup del proyecto** - Estructura de API REST
- [ ] **Instalación del framework** - Comando con perfil fastapi-rest
- [ ] **Historia de usuario completa** - US-002 documentada

### Walkthrough de las 10 Fases

- [ ] **Fase 0: Validación** - Verificar prerequisitos
- [ ] **Fase 1: BDD** - Escenarios Gherkin para endpoints
- [ ] **Fase 2: Planning** - Plan con arquitectura en capas
- [ ] **Fase 3: Implementación** - Código de:
  - Models (Pydantic schemas)
  - Routes (endpoints)
  - Services (lógica de negocio)
  - Database (in-memory o SQLite)
- [ ] **Fase 4: Tests Unitarios** - Tests de services
- [ ] **Fase 5: Tests Integración** - Tests de endpoints con TestClient
- [ ] **Fase 6: Validación BDD** - Ejecutar escenarios
- [ ] **Fase 7: Quality Gates** - Pylint, cobertura, async best practices
- [ ] **Fase 8: Documentación** - Docstrings + Swagger
- [ ] **Fase 9: Reporte** - Métricas y resumen

### Código y Ejemplos

- [ ] **Código ejecutable** - API funcional
- [ ] **Ejemplos de requests** - curl o httpx
- [ ] **Swagger UI** - Screenshot de documentación auto
- [ ] **Response examples** - JSON responses reales

### Calidad

- [ ] **Troubleshooting** - 5+ problemas comunes
- [ ] **Próximos pasos** - Persistencia, autenticación, etc.
- [ ] **Tiempo realista** - Completable en 40-50 minutos
- [ ] **Links funcionando** - Referencias correctas

## Dependencias

- **Depende de:** TICKET-052 (análisis y template)
- **Bloquea a:** TICKET-058 (validación)

## Notas Técnicas

### Estructura del Proyecto

```
todo-api/
├── main.py                    # FastAPI app
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py           # Pydantic models
│   ├── routes/
│   │   ├── __init__.py
│   │   └── tasks.py          # Endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py   # Business logic
│   └── database.py           # In-memory DB
├── tests/
│   ├── test_task_service.py
│   ├── test_endpoints.py
│   └── conftest.py
└── features/
    ├── tasks.feature
    └── steps/
        └── task_steps.py
```

### Endpoints

```python
# GET /tasks
{
  "tasks": [
    {"id": 1, "title": "Comprar leche", "completed": false},
    {"id": 2, "title": "Estudiar FastAPI", "completed": true}
  ]
}

# POST /tasks
Request: {"title": "Nueva tarea"}
Response: {"id": 3, "title": "Nueva tarea", "completed": false}

# PUT /tasks/1
Request: {"title": "Comprar leche y pan", "completed": true}
Response: {"id": 1, "title": "Comprar leche y pan", "completed": true}

# DELETE /tasks/1
Response: {"message": "Task deleted"}
```

### Componentes Clave

**TaskModel (Pydantic):**
```python
from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str

class Task(TaskCreate):
    id: int
    completed: bool = False
```

**TaskService:**
- add_task(title: str) -> Task
- get_tasks() -> List[Task]
- update_task(id: int, ...) -> Task
- delete_task(id: int) -> bool

**Routes:**
- Async endpoints
- Dependency injection
- Error handling (404, 400)

### Screenshots/Output

1. **Swagger UI** - Documentación interactiva
2. **curl request** - Ejemplo de creación de tarea
3. **Response JSON** - Respuesta formateada

## Checklist de Implementación

### Preparación (10 min)
- [ ] Leer template de TICKET-052
- [ ] Definir estructura del tutorial

### Escritura del Tutorial (1.5h)
- [ ] Sección: Introducción y requisitos
- [ ] Sección: Setup del proyecto
- [ ] Sección: Instalación del framework
- [ ] Sección: Historia de usuario US-002
- [ ] Sección: Fases 0-2 (Validación, BDD, Planning)
- [ ] Sección: Fase 3 (Implementación) - modelos, routes, services
- [ ] Sección: Fases 4-5 (Tests unitarios e integración)
- [ ] Sección: Fases 6-7 (BDD, Quality Gates)
- [ ] Sección: Fases 8-9 (Docs, Reporte)
- [ ] Sección: Ejemplos de uso (curl, httpx)
- [ ] Sección: Troubleshooting
- [ ] Sección: Próximos pasos

### Validación (30 min)
- [ ] Crear API demo y probar endpoints
- [ ] Verificar código ejecutable
- [ ] Verificar ejemplos de requests
- [ ] Verificar tiempo <1h

### Finalización (20 min)
- [ ] Agregar navegación
- [ ] Commit del archivo
- [ ] Actualizar sprint-4.md

## Resultado

✅ **COMPLETADO** - 2026-02-16

**Archivos generados:**
- `examples/code/fastapi-todo-api/` - API completa (43 archivos, 898 líneas)
- `VALIDATION-REPORT.md` - Reporte técnico detallado
- `EXECUTIVE-SUMMARY.md` - Resumen ejecutivo con métricas

**Tests:** 23/23 PASSED (98% cobertura)
**Quality Gates:** Pylint 9.71/10, Complejidad A (1.32), Mantenibilidad A
**Conformidad:** 100% con perfil fastapi-rest.json
**Tiempo:** 5 minutos 3 segundos

**Commit:** 1b9e894
