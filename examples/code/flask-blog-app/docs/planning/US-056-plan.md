# Plan de Implementación - US-056: Aplicación de Blog con Flask

## 1. Información General

- **Historia de Usuario**: US-056
- **Título**: Aplicación de Blog con Flask
- **Perfil Tecnológico**: flask-webapp (FULLSTACK)
- **Complejidad Estimada**: Media (8 Story Points)
- **Tiempo Estimado**: 4-6 horas

## 2. Arquitectura

### 2.1 Patrón Arquitectónico

**Patrón Principal**: Application Factory + Blueprint (MVC-like)

```
Model (models/post.py)
  ↓
Controller (routes/blog.py)
  ↓
View (templates/*.html)
```

### 2.2 Estructura de Directorios

```
flask-blog-app/
├── app/
│   ├── __init__.py              # Application factory
│   ├── models/
│   │   ├── __init__.py
│   │   └── post.py              # Post dataclass
│   ├── database.py              # In-memory storage
│   ├── forms/
│   │   ├── __init__.py
│   │   └── post_form.py         # WTForms
│   ├── routes/
│   │   ├── __init__.py
│   │   └── blog.py              # Flask Blueprint
│   ├── templates/
│   │   ├── base.html            # Base template
│   │   ├── index.html           # Lista de posts
│   │   ├── post_detail.html     # Detalle de post
│   │   ├── post_form.html       # Formulario crear/editar
│   │   └── confirm_delete.html  # Confirmación eliminar
│   └── static/
│       └── style.css            # Estilos CSS
├── tests/
│   ├── conftest.py
│   ├── test_post_model.py
│   ├── test_forms.py
│   ├── test_routes.py
│   └── test_forms_integration.py
├── features/
│   ├── blog.feature
│   └── steps/
│       └── blog_steps.py
├── docs/
│   ├── planning/
│   ├── architecture/
│   └── reporting/
├── main.py
├── requirements.txt
├── pytest.ini
└── .gitignore
```

### 2.3 Componentes Clave

#### Application Factory (`app/__init__.py`)
- Función `create_app()` para crear instancia de Flask
- Configuración de SECRET_KEY
- Registro de Blueprints
- Configuración de templates y static files

#### Modelo (`app/models/post.py`)
- Dataclass `Post` con campos: id, title, content, author, created_at
- Métodos auxiliares para conversión

#### Almacenamiento (`app/database.py`)
- Clase `Database` con almacenamiento in-memory
- Métodos CRUD: get_all(), get_by_id(), create(), update(), delete()
- Contador de IDs auto-incremental

#### Formularios (`app/forms/post_form.py`)
- Clase `PostForm` heredando de FlaskForm
- Campos: title (StringField), content (TextAreaField), author (StringField)
- Validadores: DataRequired, Length

#### Rutas (`app/routes/blog.py`)
- Blueprint `blog_bp`
- Endpoints:
  - GET `/` - index() - Lista de posts
  - GET `/post/<int:id>` - post_detail() - Detalle
  - GET/POST `/post/new` - post_create() - Crear
  - GET/POST `/post/<int:id>/edit` - post_edit() - Editar
  - GET/POST `/post/<int:id>/delete` - post_delete() - Eliminar

#### Templates (Jinja2)
- `base.html`: Layout base con navbar y flash messages
- `index.html`: Lista de posts con paginación
- `post_detail.html`: Detalle completo del post
- `post_form.html`: Formulario reutilizable (crear/editar)
- `confirm_delete.html`: Confirmación de eliminación

#### Static Files
- `style.css`: Estilos básicos (layout, forms, buttons, messages)

## 3. Desglose de Tareas

### 3.1 Configuración Inicial (30 min)
- [ ] Crear estructura de directorios (5 min)
- [ ] Crear `requirements.txt` (5 min)
- [ ] Crear `pytest.ini` (5 min)
- [ ] Crear `.gitignore` (5 min)
- [ ] Crear `main.py` (10 min)

### 3.2 Capa de Modelo (45 min)
- [ ] Implementar `app/models/post.py` (20 min)
- [ ] Implementar `app/database.py` (25 min)

### 3.3 Capa de Formularios (30 min)
- [ ] Implementar `app/forms/post_form.py` (30 min)

### 3.4 Capa de Rutas/Controladores (60 min)
- [ ] Implementar Application Factory `app/__init__.py` (15 min)
- [ ] Implementar Blueprint `app/routes/blog.py` (45 min)
  - [ ] Endpoint index (10 min)
  - [ ] Endpoint post_detail (5 min)
  - [ ] Endpoint post_create (10 min)
  - [ ] Endpoint post_edit (10 min)
  - [ ] Endpoint post_delete (10 min)

### 3.5 Capa de Vista (Templates) (60 min)
- [ ] Implementar `base.html` (15 min)
- [ ] Implementar `index.html` (15 min)
- [ ] Implementar `post_detail.html` (10 min)
- [ ] Implementar `post_form.html` (10 min)
- [ ] Implementar `confirm_delete.html` (10 min)

### 3.6 Static Files (20 min)
- [ ] Implementar `style.css` (20 min)

### 3.7 Tests Unitarios (45 min)
- [ ] Implementar `conftest.py` (10 min)
- [ ] Implementar `test_post_model.py` (15 min)
- [ ] Implementar `test_forms.py` (20 min)

### 3.8 Tests de Integración (60 min)
- [ ] Implementar `test_routes.py` (40 min)
- [ ] Implementar `test_forms_integration.py` (20 min)

### 3.9 Validación BDD (45 min)
- [ ] Implementar `features/steps/blog_steps.py` (45 min)

### 3.10 Quality Gates (30 min)
- [ ] Ejecutar pylint (10 min)
- [ ] Ejecutar coverage (10 min)
- [ ] Ejecutar radon (10 min)

### 3.11 Documentación (40 min)
- [ ] Crear `README.md` (20 min)
- [ ] Crear ADR-001 (20 min)

### 3.12 Reporte Final (20 min)
- [ ] Crear `US-056-report.md` (20 min)

**Tiempo Total Estimado**: 6 horas 25 minutos

## 4. Dependencias Técnicas

### 4.1 Dependencias Python
```
Flask==3.1.0
Flask-WTF==1.2.2
WTForms==3.2.1
pytest==8.3.4
pytest-bdd==7.3.0
pytest-cov==6.0.0
pylint==3.3.3
radon==6.0.1
```

### 4.2 Configuración Flask
- `SECRET_KEY`: Necesaria para CSRF protection en Flask-WTF
- `TESTING`: Flag para modo test
- `WTF_CSRF_ENABLED`: Control de CSRF protection

## 5. Puntos de Decisión

### 5.1 Decisión: In-Memory Storage vs SQLAlchemy

**Elegido**: In-Memory Storage

**Razones**:
- Simplifica el ejemplo
- Enfoque en patrones de Flask WebApp
- Fácil de entender y ejecutar
- No requiere configuración de base de datos

### 5.2 Decisión: WTForms vs Validación Manual

**Elegido**: WTForms con Flask-WTF

**Razones**:
- Validación automática client-side y server-side
- CSRF protection integrada
- Generación automática de campos HTML
- Patrón estándar en Flask WebApps

### 5.3 Decisión: Templates Jinja2 vs SPA

**Elegido**: Templates Jinja2 (Server-Side Rendering)

**Razones**:
- Patrón tradicional de Flask WebApp
- Más simple para el ejemplo
- No requiere framework JavaScript
- Mejor SEO

### 5.4 Decisión: Blueprint vs Rutas Directas

**Elegido**: Blueprint

**Razones**:
- Mejor organización del código
- Escalabilidad (múltiples blueprints)
- Patrón recomendado en Flask
- Facilita testing

## 6. Criterios de Aceptación Técnicos

### 6.1 Funcionales
- ✅ Todos los endpoints retornan HTML (status 200)
- ✅ Formularios con validación WTForms
- ✅ Flash messages funcionando
- ✅ CSRF protection habilitada
- ✅ Templates heredan de base.html
- ✅ Static files servidos correctamente

### 6.2 Tests
- ✅ Mínimo 10 tests unitarios (models + forms)
- ✅ Mínimo 12 tests de integración (routes + forms)
- ✅ Todos los escenarios BDD pasan (10 escenarios)
- ✅ Coverage >= 90%

### 6.3 Calidad
- ✅ Pylint score >= 8.5/10
- ✅ Complejidad ciclomática < 10
- ✅ Índice de mantenibilidad >= 25
- ✅ Sin código duplicado

### 6.4 Documentación
- ✅ README con instrucciones claras
- ✅ ADR documentando arquitectura
- ✅ Comentarios en código complejo
- ✅ Docstrings en funciones públicas

## 7. Riesgos y Mitigaciones

### 7.1 Riesgo: CSRF Token en Tests

**Impacto**: Alto
**Probabilidad**: Media

**Mitigación**:
- Deshabilitar CSRF en modo testing
- Configurar `WTF_CSRF_ENABLED = False` en tests

### 7.2 Riesgo: Session en Tests

**Impacto**: Medio
**Probabilidad**: Baja

**Mitigación**:
- Usar `with client.session_transaction()` para acceder a session
- Configurar SECRET_KEY en tests

### 7.3 Riesgo: Paginación Compleja

**Impacto**: Bajo
**Probabilidad**: Media

**Mitigación**:
- Implementar paginación simple con offset/limit
- Usar querystring parameters (?page=N)

## 8. Testing Strategy

### 8.1 Tests Unitarios

**Modelo Post**:
- Creación de instancia
- Conversión to_dict()
- Validación de campos

**Formularios**:
- Validación de campos requeridos
- Validación de longitud mínima
- CSRF token generado

### 8.2 Tests de Integración

**Rutas**:
- GET / retorna HTML con lista
- GET /post/<id> retorna detalle
- POST /post/new crea post
- POST /post/<id>/edit actualiza
- POST /post/<id>/delete elimina
- Validación de forms en POST
- Flash messages en responses

### 8.3 Tests BDD

**Escenarios**:
- Ver lista vacía
- Ver lista con posts
- Ver detalle
- Crear post
- Validar formularios
- Editar post
- Eliminar post
- Paginación

## 9. Entregables

### 9.1 Código
- [ ] Código fuente completo
- [ ] Tests (unitarios, integración, BDD)
- [ ] Configuración (requirements.txt, pytest.ini, .gitignore)

### 9.2 Documentación
- [ ] README.md
- [ ] ADR-001-flask-webapp-architecture.md
- [ ] US-056-report.md

### 9.3 Reportes
- [ ] VALIDATION-REPORT.md
- [ ] EXECUTIVE-SUMMARY.md

## 10. Próximos Pasos

1. Implementar configuración inicial
2. Implementar capa de modelo
3. Implementar capa de formularios
4. Implementar capa de rutas
5. Implementar templates
6. Implementar static files
7. Implementar tests
8. Ejecutar quality gates
9. Generar documentación
10. Generar reportes finales

---

**Fecha de Creación**: 2026-02-16
**Versión**: 1.0
**Estado**: Aprobado
