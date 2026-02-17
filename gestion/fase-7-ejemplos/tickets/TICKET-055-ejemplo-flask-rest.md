# TICKET-055: Tutorial Flask-REST Completo 🌶️

**Fase:** 7 - Ejemplos por Stack
**Sprint:** 4
**Estado:** ⏳ Pendiente
**Prioridad:** Alta
**Estimación:** 2.5 horas
**Asignado a:** Claude Code

## Descripción

Crear tutorial end-to-end completo para el stack **Flask-REST**, demostrando el uso del framework Claude Dev Kit para implementar una API REST con Flask y Blueprints.

**Historia de Usuario:**
```
US-003: API de Contactos

Como developer,
Quiero una API REST para gestionar contactos
Para mi aplicación de directorio

Criterios de Aceptación:
- GET /contacts - Listar todos los contactos
- POST /contacts - Crear nuevo contacto
- GET /contacts/{id} - Obtener contacto por ID
- PUT /contacts/{id} - Actualizar contacto
- DELETE /contacts/{id} - Eliminar contacto
- Campos: nombre, email, teléfono
- Validación de email y teléfono
- Manejo de errores JSON (404, 400)
```

## Criterios de Aceptación

### Contenido del Tutorial

- [ ] **Introducción clara** - API REST con Flask y Blueprints
- [ ] **Requisitos** - Python 3.9+, Flask, pytest, requests
- [ ] **Setup del proyecto** - Estructura con blueprints
- [ ] **Instalación del framework** - Comando con perfil flask-rest
- [ ] **Historia de usuario completa** - US-003 documentada

### Walkthrough de las 10 Fases

- [ ] **Fase 0: Validación** - Verificar prerequisitos
- [ ] **Fase 1: BDD** - Escenarios para CRUD de contactos
- [ ] **Fase 2: Planning** - Plan con arquitectura Flask
- [ ] **Fase 3: Implementación** - Código de:
  - Flask app factory
  - Blueprint de contactos
  - Contact model/schema
  - In-memory storage
  - Error handlers
- [ ] **Fase 4: Tests Unitarios** - Tests de lógica
- [ ] **Fase 5: Tests Integración** - Tests de endpoints con test_client
- [ ] **Fase 6: Validación BDD** - Ejecutar escenarios
- [ ] **Fase 7: Quality Gates** - Pylint, cobertura
- [ ] **Fase 8: Documentación** - Docstrings
- [ ] **Fase 9: Reporte** - Métricas finales

### Código y Ejemplos

- [ ] **Código ejecutable** - API funcional
- [ ] **Ejemplos de requests** - curl o Python requests
- [ ] **Response examples** - JSON responses
- [ ] **Error handling** - Ejemplos de 404, 400

### Calidad

- [ ] **Troubleshooting** - 5+ problemas comunes
- [ ] **Próximos pasos** - SQLAlchemy, autenticación, etc.
- [ ] **Tiempo realista** - Completable en 40-50 minutos
- [ ] **Links funcionando** - Referencias correctas

## Dependencias

- **Depende de:** TICKET-052 (análisis y template)
- **Bloquea a:** TICKET-058 (validación)

## Notas Técnicas

### Estructura del Proyecto

```
contacts-api/
├── app.py                     # Factory pattern
├── app/
│   ├── __init__.py           # create_app()
│   ├── models/
│   │   ├── __init__.py
│   │   └── contact.py        # Contact dataclass
│   ├── blueprints/
│   │   ├── __init__.py
│   │   └── contacts.py       # Routes
│   ├── services/
│   │   ├── __init__.py
│   │   └── contact_service.py
│   ├── validators.py         # Email, phone validation
│   └── errors.py             # Error handlers
├── tests/
│   ├── test_contact_service.py
│   ├── test_endpoints.py
│   └── conftest.py
└── features/
    ├── contacts.feature
    └── steps/
        └── contact_steps.py
```

### Endpoints

```python
# GET /contacts
{"contacts": [
  {"id": 1, "name": "Juan Pérez", "email": "juan@example.com", "phone": "+54123456789"},
  {"id": 2, "name": "María García", "email": "maria@example.com", "phone": "+54987654321"}
]}

# POST /contacts
Request: {"name": "Ana López", "email": "ana@example.com", "phone": "+54111222333"}
Response: {"id": 3, "name": "Ana López", "email": "ana@example.com", "phone": "+54111222333"}

# GET /contacts/1
{"id": 1, "name": "Juan Pérez", "email": "juan@example.com", "phone": "+54123456789"}

# PUT /contacts/1
Request: {"name": "Juan Pérez", "email": "juanp@example.com", "phone": "+54123456789"}
Response: {"id": 1, "name": "Juan Pérez", "email": "juanp@example.com", "phone": "+54123456789"}

# DELETE /contacts/1
Response: {"message": "Contact deleted successfully"}

# Error 404
{"error": "Contact not found", "status": 404}

# Error 400
{"error": "Invalid email format", "status": 400}
```

### Componentes Clave

**Contact Model:**
```python
from dataclasses import dataclass

@dataclass
class Contact:
    id: int
    name: str
    email: str
    phone: str
```

**Blueprint:**
```python
from flask import Blueprint, jsonify, request

contacts_bp = Blueprint('contacts', __name__, url_prefix='/contacts')

@contacts_bp.route('/', methods=['GET'])
def list_contacts():
    ...

@contacts_bp.route('/', methods=['POST'])
def create_contact():
    ...
```

**Validators:**
- validate_email(email: str) -> bool
- validate_phone(phone: str) -> bool

## Checklist de Implementación

### Preparación (10 min)
- [ ] Leer template de TICKET-052
- [ ] Definir estructura del tutorial

### Escritura del Tutorial (1.5h)
- [ ] Sección: Introducción y requisitos
- [ ] Sección: Setup del proyecto
- [ ] Sección: Instalación del framework
- [ ] Sección: Historia de usuario US-003
- [ ] Sección: Fases 0-2
- [ ] Sección: Fase 3 - Implementación con blueprints
- [ ] Sección: Fases 4-5 - Tests
- [ ] Sección: Fases 6-9
- [ ] Sección: Ejemplos de uso
- [ ] Sección: Troubleshooting
- [ ] Sección: Próximos pasos

### Validación (30 min)
- [ ] Crear API demo y probar
- [ ] Verificar código ejecutable
- [ ] Verificar validaciones funcionando
- [ ] Verificar tiempo <1h

### Finalización (20 min)
- [ ] Agregar navegación
- [ ] Commit del archivo
- [ ] Actualizar sprint-4.md

## Resultado

_Se completará cuando el ticket esté DONE_

**Archivo generado:** `docs/examples/flask-rest-project.md`

**Estado:** ⏳ Pendiente
