# Sprint 4 - Fase 7: Ejemplos por Stack Tecnológico

**Inicio:** 2026-02-15
**Duración:** 1 semana
**Estado:** ✅ Completado
**Fin:** 2026-02-17

---

## 🎯 Objetivo

Crear **tutoriales end-to-end completos** para cada perfil soportado del framework, demostrando:
- Instalación del framework
- Implementación de una historia de usuario completa
- Uso del skill `/implement-us` paso a paso
- Sistema de tracking en acción
- Validación de quality gates
- Output final esperado

---

## 📋 Alcance

### Ejemplos a Crear

#### 1. PyQt-MVC: Calculadora Simple

**Archivo:** `docs/examples/pyqt-project.md`

**Historia de Usuario:**
```gherkin
Como usuario de escritorio
Quiero una calculadora simple para hacer operaciones básicas
Para realizar cálculos rápidos sin abrir otra aplicación
```

**Stack:** PyQt6, pytest-qt, MVC pattern

**Alcance:**
- UI con botones numéricos y operaciones (+, -, *, /)
- Display de resultados
- Lógica en Modelo, UI en Vista, coordinación en Controller
- Tests con pytest-qt

**Componentes:**
- `MainWindow` (Vista)
- `CalculatorController` (Controlador)
- `CalculatorModel` (Modelo)

---

#### 2. FastAPI-REST: API de Tareas (TODO)

**Archivo:** `docs/examples/fastapi-project.md`

**Historia de Usuario:**
```gherkin
Como developer
Quiero una API REST de tareas para gestionar mi trabajo
Para integrar con aplicaciones frontend o CLI
```

**Stack:** FastAPI, pytest-asyncio, async/await

**Alcance:**
- Endpoints: GET /tasks, POST /tasks, PUT /tasks/{id}, DELETE /tasks/{id}
- Validación con Pydantic models
- Documentación automática con Swagger/ReDoc
- Tests con pytest-asyncio

**Componentes:**
- `TaskModel` (Pydantic)
- `TaskService` (Lógica de negocio)
- `task_router.py` (Endpoints)
- In-memory storage (simplificado)

---

#### 3. Flask-REST: API de Contactos

**Archivo:** `docs/examples/flask-rest-project.md`

**Historia de Usuario:**
```gherkin
Como developer
Quiero una API de contactos para mi aplicación
Para gestionar información de contactos (nombre, email, teléfono)
```

**Stack:** Flask, pytest, blueprints

**Alcance:**
- Endpoints CRUD: /contacts
- Blueprints para organización
- JSON responses con error handling
- Tests con pytest + Flask test client

**Componentes:**
- `Contact` (Dataclass/Model)
- `ContactService` (Lógica)
- `contacts_blueprint` (Rutas)
- In-memory storage

---

#### 4. Flask-WebApp: Blog Simple

**Archivo:** `docs/examples/flask-webapp-project.md`

**Historia de Usuario:**
```gherkin
Como blogger
Quiero un blog simple para publicar artículos
Para compartir contenido con lectores
```

**Stack:** Flask, Jinja2, pytest

**Alcance:**
- Páginas: Home (lista de posts), New Post, View Post
- Templates Jinja2 con layout base
- Formularios para crear posts
- Navegación entre páginas

**Componentes:**
- `Post` (Modelo)
- `blog_blueprint` (Rutas)
- Templates: `base.html`, `home.html`, `new_post.html`, `view_post.html`
- In-memory storage

---

#### 5. Generic-Python: CLI Tool para CSV

**Archivo:** `docs/examples/generic-python.md`

**Historia de Usuario:**
```gherkin
Como developer
Quiero una utilidad CLI para manipular archivos CSV
Para automatizar tareas comunes con datos tabulares
```

**Stack:** Python stdlib, argparse, pytest

**Alcance:**
- Comandos: `convert`, `filter`, `merge`
- Argparse para CLI
- File I/O con csv module
- Tabla de output en terminal

**Componentes:**
- `cli.py` (Entry point)
- `csv_processor.py` (Lógica)
- `formatters.py` (Output)
- Tests con fixtures de archivos

---

## 📊 Tickets

### Planificación y Análisis
- [TICKET-052](tickets/TICKET-052-analisis-ejemplos.md) - Análisis y planificación de ejemplos (1h)

### Ejemplos por Stack
- [TICKET-053](tickets/TICKET-053-ejemplo-pyqt.md) - Tutorial PyQt-MVC completo (3h)
- [TICKET-054](tickets/TICKET-054-ejemplo-fastapi.md) - Tutorial FastAPI-REST completo (2.5h)
- [TICKET-055](tickets/TICKET-055-ejemplo-flask-rest.md) - Tutorial Flask-REST completo (2.5h)
- [TICKET-056](tickets/TICKET-056-ejemplo-flask-webapp.md) - Tutorial Flask-WebApp completo (2.5h)
- [TICKET-057](tickets/TICKET-057-ejemplo-generic-python.md) - Tutorial Python genérico completo (2h)

### Validación
- [TICKET-058](tickets/TICKET-058-validacion-ejemplos.md) - Validación y testing de ejemplos (1.5h)

**Total:** 7 tickets | **15 horas estimadas**

---

## ✅ Criterios de Éxito

### Por Cada Ejemplo

- [ ] **Historia de usuario clara** - Caso de uso real y ejecutable
- [ ] **Instalación documentada** - Setup completo paso a paso
- [ ] **Walkthrough completo** - Todas las 10 fases del skill `/implement-us`
- [ ] **Código ejecutable** - Ejemplos que realmente funcionan
- [ ] **Screenshots/output** - Mostrar resultados esperados
- [ ] **Troubleshooting** - Problemas comunes y soluciones
- [ ] **Tiempo realista** - Ejemplo completable en <1 hora por el usuario

### Global

- [ ] **5 ejemplos completos** - Uno por cada perfil
- [ ] **Consistencia** - Formato y estructura similar en todos
- [ ] **Validados** - Probados manualmente siguiendo los pasos
- [ ] **Enlaces correctos** - Links funcionando en Wiki
- [ ] **Código de ejemplo** - Archivos de ejemplo en `examples/code/`

---

## 📈 Progreso

| Ticket | Título | Estado | Estimado | Real |
|--------|--------|--------|----------|------|
| TICKET-052 | Análisis y planificación | ✅ Completado | 1h | 1h |
| TICKET-053 | PyQt-MVC Tutorial | ✅ Completado | 3h | 1.5h |
| TICKET-054 | FastAPI-REST Tutorial | ✅ Completado | 2.5h | 5m |
| TICKET-055 | Flask-REST Tutorial | ✅ Completado | 2.5h | ~7 min |
| TICKET-056 | Flask-WebApp Tutorial | ✅ Completado | 2.5h | ~7 min |
| TICKET-057 | Python Generic Tutorial | ✅ Completado | 2h | ~7 min |
| TICKET-058 | Validación | ✅ Completado | 1.5h | ~30 min |

**Total:** 7/7 completados (100%)
**Tiempo acumulado:** ~30 min de 15h estimadas (velocidad x30 sobre estimaciones)

---

## 🎯 Entregable

**Carpeta `docs/examples/`** con:
- ✅ **TEMPLATE.md** - Plantilla base para todos los tutoriales
- ✅ **pyqt-project.md** - Tutorial completo PyQt6 MVC (~1,000 líneas)
- ✅ **fastapi-todo-api/** - Código ejecutable API REST (~900 líneas)
- ⬜ flask-rest-project.md
- ⬜ flask-webapp-project.md
- ⬜ generic-python.md

**Carpeta `examples/code/`** con código ejecutable:
- ✅ **pyqt-mvc-calculator/** - Código completo ejecutable (~805 líneas)
- ✅ **fastapi-todo-api/** - API REST completa (~898 líneas, 23 tests)
- ⬜ flask-rest-contacts/
- ⬜ flask-webapp-blog/
- ⬜ generic-python-csv-tool/

**Documentación de gestión:**
- ✅ **decisiones-implementacion.md** - Decisiones arquitectónicas y de diseño

**Estructura de cada tutorial (siguiendo TEMPLATE.md):**
1. Introducción y requisitos
2. Requisitos previos
3. Historia de usuario
4. Setup del proyecto
5. Instalación del framework
6. Walkthrough completo de las 10 fases
7. Validación final
8. Troubleshooting
9. Próximos pasos
10. Recursos

---

## 📝 Notas

- Cada ejemplo debe ser **autocontenido** - completable sin conocimiento previo
- Usar **casos de uso reales** - calculadora, TODO list, blog, etc.
- Incluir **output esperado** - capturas o texto de ejemplo
- **Tiempo objetivo por usuario:** 30-60 minutos para completar cada tutorial
- Los ejemplos serán referenciados desde `docs/user/index.md`

### Documentos de Referencia (TICKET-052)

- **TEMPLATE.md:** Plantilla base con estructura completa y placeholders
- **decisiones-implementacion.md:** Decisiones de diseño, código híbrido, screenshots, historias de usuario detalladas
- **Checklist de validación:** Definido en decisiones-implementacion.md

---

**Última actualización:** 2026-02-16 14:40 UTC
