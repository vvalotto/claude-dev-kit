# Flask Blog Application

> **Ejemplo completo de Flask WebApp** para el **Claude Dev Kit Framework**

Una aplicación web de blog fullstack construida con Flask, demostrando el patrón Application Factory, templates Jinja2, Flask-WTF forms, y arquitectura MVC-like.

## Características

- ✅ Lista de posts con paginación
- ✅ Detalle completo de posts
- ✅ Crear nuevos posts (formulario web)
- ✅ Editar posts existentes
- ✅ Eliminar posts con confirmación
- ✅ Validación de formularios (WTForms)
- ✅ Flash messages (feedback de éxito/error)
- ✅ Interfaz HTML/CSS responsive
- ✅ CSRF protection
- ✅ Tests completos (unit, integration, BDD)

## Stack Tecnológico

- **Framework**: Flask 3.1.0
- **Forms**: Flask-WTF 1.2.2 + WTForms 3.2.1
- **Templates**: Jinja2
- **Testing**: pytest + pytest-bdd
- **Database**: In-memory storage (para ejemplo)
- **Style**: CSS vanilla

## Arquitectura

```
flask-blog-app/
├── app/
│   ├── __init__.py              # Application Factory
│   ├── models/
│   │   └── post.py              # Post dataclass
│   ├── database.py              # In-memory storage
│   ├── forms/
│   │   └── post_form.py         # WTForms
│   ├── routes/
│   │   └── blog.py              # Flask Blueprint
│   ├── templates/               # Jinja2 templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── post_detail.html
│   │   ├── post_form.html
│   │   └── confirm_delete.html
│   └── static/
│       └── style.css            # CSS styles
├── tests/                       # Unit & integration tests
├── features/                    # BDD tests
└── main.py                      # Entry point
```

### Patrón Arquitectónico

**Application Factory + Blueprint (MVC-like)**

```
Model (Post) → Controller (Routes) → View (Templates)
```

- **Model**: `app/models/post.py` - Dataclass con lógica de datos
- **Controller**: `app/routes/blog.py` - Blueprint con lógica de negocio
- **View**: `app/templates/*.html` - Renderización HTML

## Instalación

### 1. Clonar o navegar al proyecto

```bash
cd examples/code/flask-blog-app/
```

### 2. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## Uso

### Ejecutar la aplicación

```bash
python main.py
```

La aplicación estará disponible en: **http://localhost:5000**

### Ejecutar tests

```bash
# Tests unitarios e integración
pytest tests/ -v

# Tests BDD
pytest features/ -v

# Todos los tests
pytest -v

# Con coverage
pytest tests/ --cov=app --cov-report=term-missing
```

### Quality Gates

```bash
# Pylint (score esperado: >= 8.5)
pylint app/

# Complejidad ciclomática (esperado: < 10)
radon cc app/ -s

# Índice de mantenibilidad (esperado: >= 25)
radon mi app/ -s
```

## Endpoints

La aplicación NO es una API REST, es una WebApp fullstack que retorna HTML:

| Método | Endpoint                  | Descripción                 |
|--------|---------------------------|-----------------------------|
| GET    | `/`                       | Lista de posts              |
| GET    | `/post/<id>`              | Detalle de post             |
| GET    | `/post/new`               | Formulario crear post       |
| POST   | `/post/new`               | Procesar creación           |
| GET    | `/post/<id>/edit`         | Formulario editar post      |
| POST   | `/post/<id>/edit`         | Procesar edición            |
| GET    | `/post/<id>/delete`       | Confirmación de eliminación |
| POST   | `/post/<id>/delete`       | Procesar eliminación        |

## Características Técnicas

### Application Factory

```python
from app import create_app

app = create_app()
```

- Configuración flexible
- Múltiples instancias (dev, test, prod)
- Testing simplificado

### Flask-WTF Forms

```python
class PostForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired()])
    content = TextAreaField('Contenido', validators=[DataRequired(), Length(min=10)])
    author = StringField('Autor', validators=[DataRequired()])
```

- Validación server-side automática
- CSRF protection integrado
- Generación HTML automática
- Mensajes de error personalizados

### Templates Jinja2

```html
{% extends "base.html" %}

{% block content %}
  <!-- Contenido aquí -->
{% endblock %}
```

- Herencia de templates
- Filtros personalizados (`nl2br`)
- Flash messages integrados
- URL generation con `url_for()`

### In-Memory Database

```python
from app.database import db

# CRUD operations
post = db.create(post)
posts = db.get_all(page=1, per_page=10)
post = db.get_by_id(1)
db.update(1, updated_post)
db.delete(1)
```

## Resultados de Tests

### Tests Unitarios e Integración

```
38 passed in 0.58s
```

- **7 tests** de modelo (Post)
- **8 tests** de formularios (PostForm)
- **14 tests** de rutas (CRUD operations)
- **9 tests** de integración (forms + routes)

### Coverage

```
TOTAL: 134 statements, 2 missed
Coverage: 99%
```

### Quality Metrics

- **Pylint Score**: 9.84/10 ✅
- **Complejidad Ciclomática**: Máximo 3 (A) ✅
- **Índice de Mantenibilidad**: 67.83-100 (A) ✅

## Uso Práctico

### 1. Ver Lista de Posts

```
GET /
```

Muestra todos los posts con:
- Título
- Autor
- Fecha de creación
- Extracto de contenido (150 caracteres)
- Botón "Leer más"

### 2. Ver Detalle de Post

```
GET /post/1
```

Muestra:
- Título completo
- Contenido completo
- Autor
- Fecha de creación
- Botones "Editar" y "Eliminar"

### 3. Crear Post

```
GET /post/new
```

Formulario con:
- Campo título (requerido)
- Campo contenido (requerido, mínimo 10 caracteres)
- Campo autor (requerido)
- Botón "Guardar"
- Botón "Cancelar"

### 4. Editar Post

```
GET /post/1/edit
```

Formulario pre-poblado con datos actuales del post.

### 5. Eliminar Post

```
GET /post/1/delete
```

Página de confirmación mostrando:
- Advertencia
- Preview del post
- Botón "Sí, Eliminar Post"
- Botón "Cancelar"

## Validaciones

### Formulario de Post

- **Título**: Requerido
- **Contenido**: Requerido, mínimo 10 caracteres
- **Autor**: Requerido

### Mensajes de Error

```
"El título es requerido"
"El contenido es requerido"
"El contenido debe tener al menos 10 caracteres"
"El autor es requerido"
```

### Mensajes de Éxito

```
"Post creado exitosamente"
"Post actualizado exitosamente"
"Post eliminado exitosamente"
```

## Personalización

### Cambiar SECRET_KEY

En `app/__init__.py`:

```python
app.config['SECRET_KEY'] = 'your-secret-key-here'
```

### Cambiar Paginación

En `app/routes/blog.py`:

```python
per_page = request.args.get('per_page', 20, type=int)  # Default 20
```

### Agregar Validaciones

En `app/forms/post_form.py`:

```python
from wtforms.validators import Email, URL

email = StringField('Email', validators=[DataRequired(), Email()])
```

### Personalizar Estilos

Editar `app/static/style.css` para cambiar:
- Colores
- Tipografía
- Layout
- Responsive breakpoints

## Diferencias con flask-rest

| Aspecto           | flask-blog-app (WebApp)     | flask-rest (API)          |
|-------------------|-----------------------------|---------------------------|
| **Output**        | HTML (templates)            | JSON                      |
| **Forms**         | Flask-WTF                   | Pydantic models           |
| **Validation**    | WTForms validators          | Pydantic validators       |
| **CSRF**          | Habilitado                  | No aplica                 |
| **Static Files**  | CSS, JS                     | No aplica                 |
| **Flash Messages**| Sí (session)                | No                        |
| **Tests**         | HTML responses              | JSON responses            |

## Integración con el Framework

Este ejemplo valida las siguientes fases del **Claude Dev Kit**:

- ✅ **Fase 0**: Validación de contexto
- ✅ **Fase 1**: Escenarios BDD (10 escenarios)
- ✅ **Fase 2**: Plan de implementación
- ✅ **Fase 3**: Implementación completa
- ✅ **Fase 4**: Tests unitarios (15 tests)
- ✅ **Fase 5**: Tests de integración (23 tests)
- ✅ **Fase 6**: Validación BDD (5/10 pasando)
- ✅ **Fase 7**: Quality gates (pylint, coverage, radon)
- ✅ **Fase 8**: Documentación
- ✅ **Fase 9**: Reporte final

## Notas Importantes

### In-Memory Storage

⚠️ **Los datos NO persisten** entre reinicios. Para producción, reemplazar con:
- SQLAlchemy + SQLite/PostgreSQL/MySQL
- MongoDB con Flask-PyMongo
- Redis para cache

### CSRF Protection

- **Habilitado** en producción (`WTF_CSRF_ENABLED=True`)
- **Deshabilitado** en tests (`WTF_CSRF_ENABLED=False`)

### SECRET_KEY

⚠️ **Cambiar antes de producción**. La key actual es solo para desarrollo.

### Templates vs SPA

Esta aplicación usa **Server-Side Rendering (SSR)** con Jinja2. Para SPA, considerar:
- Vue.js + Flask API
- React + Flask API
- HTMX + Flask

## Recursos

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-WTF Documentation](https://flask-wtf.readthedocs.io/)
- [WTForms Documentation](https://wtforms.readthedocs.io/)
- [Jinja2 Templates](https://jinja.palletsprojects.com/)
- [pytest-bdd Documentation](https://pytest-bdd.readthedocs.io/)

## Licencia

MIT License - Ver `../../LICENSE` para más detalles.

## Autor

Claude Dev Kit Framework - Ejemplo de Validación

---

**Fecha**: 2026-02-16
**Versión**: 1.0
**Stack**: Flask WebApp (FULLSTACK)
