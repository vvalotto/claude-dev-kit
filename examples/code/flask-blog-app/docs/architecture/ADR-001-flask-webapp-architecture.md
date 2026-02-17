# ADR-001: Flask WebApp Architecture (Server-Side Rendering)

## Status

**Accepted** - 2026-02-16

## Context

Para el Claude Dev Kit Framework, necesitamos un ejemplo completo de Flask WebApp que demuestre:
- Arquitectura MVC-like con Flask
- Server-Side Rendering con templates Jinja2
- Formularios web con validación
- CRUD completo para una entidad
- Diferenciación clara vs APIs REST

### Requisitos

1. Aplicación web fullstack (no API REST)
2. Interfaz HTML con CSS
3. Formularios web con validación server-side
4. Flash messages para feedback de usuario
5. CSRF protection
6. Paginación
7. Tests completos (unit, integration, BDD)

## Decision

Implementamos una arquitectura **Application Factory + Blueprint** con **Server-Side Rendering**, usando:

### 1. Application Factory Pattern

```python
def create_app(config=None):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-key'
    app.config['WTF_CSRF_ENABLED'] = True

    # Register blueprints
    from app.routes import blog_bp
    app.register_blueprint(blog_bp)

    return app
```

**Ventajas**:
- Múltiples instancias de la app (dev, test, prod)
- Configuración flexible
- Testing simplificado
- Mejor organización del código

### 2. Blueprint Pattern

```python
blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/')
def index():
    return render_template('index.html')
```

**Ventajas**:
- Modularidad
- Escalabilidad (múltiples blueprints)
- Organización de código
- Reutilización

### 3. Server-Side Rendering (Jinja2)

```html
{% extends "base.html" %}

{% block content %}
  <!-- Content here -->
{% endblock %}
```

**Ventajas**:
- SEO-friendly
- Carga inicial rápida
- No requiere JavaScript framework
- Menor complejidad
- Flash messages integrados

**Desventajas**:
- Interactividad limitada
- Recarga de página completa
- No ideal para UX moderna

### 4. Flask-WTF + WTForms

```python
class PostForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired()])
    content = TextAreaField('Contenido', validators=[Length(min=10)])
```

**Ventajas**:
- Validación automática client-side y server-side
- CSRF protection integrado
- Generación HTML automática
- Mensajes de error personalizados
- Patrón estándar en Flask

**Desventajas**:
- Menos flexible que validación manual
- Acoplamiento a Flask

### 5. In-Memory Storage

```python
class Database:
    def __init__(self):
        self._posts: dict[int, Post] = {}
        self._next_id: int = 1
```

**Ventajas** (para ejemplo):
- No requiere configuración
- Fácil de entender
- Rápido de implementar
- Sin dependencias externas

**Desventajas**:
- No persiste datos
- No escalable
- No production-ready

### 6. Arquitectura MVC-like

```
Model (models/post.py)
  ↓
Controller (routes/blog.py)
  ↓
View (templates/*.html)
```

**Componentes**:

- **Model**: Dataclass `Post` con lógica de datos
- **Controller**: Blueprint con rutas y lógica de negocio
- **View**: Templates Jinja2 para presentación

## Consequences

### Positive

1. **Simplicidad**: Arquitectura clara y fácil de entender
2. **Patrón estándar**: Uso de patrones recomendados por Flask
3. **Testing**: Fácil de testear con fixtures pytest
4. **Escalabilidad**: Base sólida para crecer
5. **Documentación**: Ejemplos claros de cada componente
6. **Validación**: WTForms proporciona validación robusta
7. **Seguridad**: CSRF protection out-of-the-box

### Negative

1. **Interactividad limitada**: Sin JavaScript framework
2. **UX moderna**: Recarga de página completa
3. **Persistencia**: In-memory no production-ready
4. **SPA trends**: No sigue tendencias modernas (React, Vue)

### Neutral

1. **Server-Side Rendering**: Trade-off SEO vs UX
2. **Template engine**: Jinja2 es poderoso pero limitado vs JSX
3. **Forms**: WTForms es robusto pero menos flexible que validación manual

## Alternatives Considered

### 1. Flask + SPA (React/Vue)

**Pros**:
- UX moderna
- Sin recarga de página
- Componentes reutilizables
- Ecosistema rico

**Cons**:
- Mayor complejidad
- Requiere JavaScript expertise
- SEO más complejo
- Dos proyectos separados

**Decisión**: No seleccionado - excede scope del ejemplo

### 2. Flask REST API + Templates

**Pros**:
- Separación de concerns
- API reutilizable
- Escalabilidad

**Cons**:
- Mayor complejidad
- Overhead innecesario
- Dos capas de validación

**Decisión**: No seleccionado - arquitectura híbrida compleja

### 3. Django (MVT Pattern)

**Pros**:
- Admin panel out-of-the-box
- ORM integrado
- Batteries included

**Cons**:
- No es Flask
- Mayor curva de aprendizaje
- Más opinionado

**Decisión**: No seleccionado - fuera de scope

### 4. Flask + SQLAlchemy

**Pros**:
- Persistencia real
- Migraciones
- Relaciones complejas

**Cons**:
- Configuración adicional
- Mayor complejidad
- Dependencia externa

**Decisión**: No seleccionado - in-memory suficiente para ejemplo

## Implementation Details

### Estructura de Directorios

```
flask-blog-app/
├── app/
│   ├── __init__.py              # Application Factory
│   ├── models/
│   │   └── post.py              # Model layer
│   ├── database.py              # Data access layer
│   ├── forms/
│   │   └── post_form.py         # Form layer
│   ├── routes/
│   │   └── blog.py              # Controller layer
│   ├── templates/               # View layer
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── post_detail.html
│   │   ├── post_form.html
│   │   └── confirm_delete.html
│   └── static/
│       └── style.css            # Presentation layer
├── tests/                       # Test layer
├── features/                    # BDD layer
└── main.py                      # Entry point
```

### Responsabilidades

**app/__init__.py**:
- Crear instancia de Flask
- Configurar SECRET_KEY
- Registrar blueprints
- Registrar filtros Jinja2

**app/models/post.py**:
- Definir estructura de Post (dataclass)
- Métodos de conversión (to_dict)
- Representación string

**app/database.py**:
- CRUD operations
- Paginación
- Auto-increment IDs
- Gestión de memoria

**app/forms/post_form.py**:
- Definir campos de formulario
- Validadores
- Mensajes de error personalizados

**app/routes/blog.py**:
- Endpoints HTTP
- Lógica de negocio
- Validación de formularios
- Flash messages
- Redirecciones

**app/templates/*.html**:
- Estructura HTML
- Herencia de templates
- Renderización de datos
- Formularios
- Flash messages

**app/static/style.css**:
- Estilos visuales
- Layout
- Responsive design

### Flujo de Datos

```
User Request
  ↓
Flask Route (Controller)
  ↓
Form Validation (if POST)
  ↓
Database Operation (Model)
  ↓
Template Rendering (View)
  ↓
HTML Response
```

### Testing Strategy

**Unit Tests**:
- Models (Post dataclass)
- Forms (WTForms validation)

**Integration Tests**:
- Routes (HTTP endpoints)
- Forms + Routes (end-to-end flows)

**BDD Tests**:
- User scenarios
- Complete workflows

## Notes

### CSRF Protection

- Habilitado en producción (`WTF_CSRF_ENABLED=True`)
- Deshabilitado en tests (`WTF_CSRF_ENABLED=False`)
- Token automático en formularios

### Flash Messages

```python
flash('Post creado exitosamente', 'success')
flash('Error al crear post', 'error')
```

Categorías:
- `success`: Operación exitosa
- `error`: Operación fallida
- `warning`: Advertencia
- `info`: Información

### Paginación

```python
page = request.args.get('page', 1, type=int)
per_page = request.args.get('per_page', 10, type=int)
posts = db.get_all(page=page, per_page=per_page)
```

### URL Generation

```python
url_for('blog.index')
url_for('blog.post_detail', post_id=1)
url_for('blog.post_create')
```

## References

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-WTF Documentation](https://flask-wtf.readthedocs.io/)
- [Application Factory Pattern](https://flask.palletsprojects.com/en/2.3.x/patterns/appfactories/)
- [Blueprints](https://flask.palletsprojects.com/en/2.3.x/blueprints/)
- [Jinja2 Templates](https://jinja.palletsprojects.com/)

---

**Author**: Claude Dev Kit Framework
**Date**: 2026-02-16
**Version**: 1.0
