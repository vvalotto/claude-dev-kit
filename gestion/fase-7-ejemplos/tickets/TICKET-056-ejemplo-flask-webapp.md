# TICKET-056: Tutorial Flask-WebApp Completo 🌐

**Fase:** 7 - Ejemplos por Stack
**Sprint:** 4
**Estado:** ⏳ Pendiente
**Prioridad:** Alta
**Estimación:** 2.5 horas
**Asignado a:** Claude Code

## Descripción

Crear tutorial end-to-end completo para el stack **Flask-WebApp**, demostrando el uso del framework Claude Dev Kit para implementar una aplicación web fullstack con Flask, Jinja2 y templates.

**Historia de Usuario:**
```
US-004: Blog Simple

Como blogger,
Quiero un blog simple para publicar artículos
Para compartir mis ideas con otros

Criterios de Aceptación:
- Página principal: Lista de posts
- Página de detalle: Ver post completo
- Formulario: Crear nuevo post
- Campos: título, contenido, autor, fecha
- Navegación: Home, New Post
- Templates Jinja2 con herencia
- Estilos básicos CSS
```

## Criterios de Aceptación

### Contenido del Tutorial

- [ ] **Introducción clara** - WebApp con Flask y templates
- [ ] **Requisitos** - Python 3.9+, Flask, pytest, Jinja2
- [ ] **Setup del proyecto** - Estructura MVC con templates
- [ ] **Instalación del framework** - Comando con perfil flask-webapp
- [ ] **Historia de usuario completa** - US-004 documentada

### Walkthrough de las 10 Fases

- [ ] **Fase 0: Validación** - Verificar prerequisitos
- [ ] **Fase 1: BDD** - Escenarios para blog
- [ ] **Fase 2: Planning** - Plan con arquitectura MVT
- [ ] **Fase 3: Implementación** - Código de:
  - Flask app con blueprints
  - Models (Post)
  - Views (routes)
  - Templates (base, index, detail, new)
  - Static CSS
- [ ] **Fase 4: Tests Unitarios** - Tests de lógica
- [ ] **Fase 5: Tests Integración** - Tests de vistas
- [ ] **Fase 6: Validación BDD** - Ejecutar escenarios
- [ ] **Fase 7: Quality Gates** - Pylint, cobertura
- [ ] **Fase 8: Documentación** - Docstrings
- [ ] **Fase 9: Reporte** - Métricas finales

### Código y Ejemplos

- [ ] **Código ejecutable** - WebApp funcional
- [ ] **Screenshots** - 3 pantallas: Home, Detail, New Post
- [ ] **Templates Jinja2** - Ejemplos de herencia
- [ ] **CSS básico** - Estilos simples

### Calidad

- [ ] **Troubleshooting** - 5+ problemas comunes
- [ ] **Próximos pasos** - Autenticación, edición, eliminación
- [ ] **Tiempo realista** - Completable en 45-60 minutos
- [ ] **Links funcionando** - Referencias correctas

## Dependencias

- **Depende de:** TICKET-052 (análisis y template)
- **Bloquea a:** TICKET-058 (validación)

## Notas Técnicas

### Estructura del Proyecto

```
blog-app/
├── app.py                     # Entry point
├── app/
│   ├── __init__.py           # create_app()
│   ├── models/
│   │   ├── __init__.py
│   │   └── post.py           # Post model
│   ├── views/
│   │   ├── __init__.py
│   │   ├── main.py           # Home routes
│   │   └── posts.py          # Post routes
│   ├── services/
│   │   ├── __init__.py
│   │   └── post_service.py
│   ├── forms/
│   │   ├── __init__.py
│   │   └── post_form.py      # WTForms
│   ├── templates/
│   │   ├── base.html         # Base template
│   │   ├── index.html        # Home page
│   │   ├── post_detail.html  # Single post
│   │   └── new_post.html     # Create form
│   └── static/
│       └── style.css         # Styles
├── tests/
│   ├── test_post_service.py
│   ├── test_views.py
│   └── conftest.py
└── features/
    ├── blog.feature
    └── steps/
        └── blog_steps.py
```

### Páginas

**Home (/):**
```html
- Lista de posts
- Título + fecha + autor
- Link "Leer más" → detail
- Link "Nuevo Post" → /posts/new
```

**Detail (/posts/<id>):**
```html
- Título completo
- Contenido completo
- Autor y fecha
- Link "Volver" → /
```

**New Post (/posts/new):**
```html
- Form: título, contenido, autor
- Botón Submit
- Validación de campos
- Redirect a / al crear
```

### Componentes Clave

**Post Model:**
```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Post:
    id: int
    title: str
    content: str
    author: str
    date: datetime
```

**Base Template:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Blog{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <nav>
        <a href="/">Home</a>
        <a href="/posts/new">New Post</a>
    </nav>
    {% block content %}{% endblock %}
</body>
</html>
```

**Views:**
```python
@main_bp.route('/')
def index():
    posts = post_service.get_all()
    return render_template('index.html', posts=posts)

@posts_bp.route('/<int:id>')
def detail(id):
    post = post_service.get_by_id(id)
    return render_template('post_detail.html', post=post)

@posts_bp.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        # Create post
        return redirect('/')
    return render_template('new_post.html')
```

### Screenshots

1. **Home Page** - Lista de posts con navegación
2. **Post Detail** - Vista de post individual
3. **New Post Form** - Formulario de creación

## Checklist de Implementación

### Preparación (10 min)
- [ ] Leer template de TICKET-052
- [ ] Definir estructura del tutorial
- [ ] Crear webapp demo para screenshots

### Escritura del Tutorial (1.5h)
- [ ] Sección: Introducción y requisitos
- [ ] Sección: Setup del proyecto
- [ ] Sección: Instalación del framework
- [ ] Sección: Historia de usuario US-004
- [ ] Sección: Fases 0-2
- [ ] Sección: Fase 3 - Models, Views, Templates
- [ ] Sección: Fases 4-5 - Tests
- [ ] Sección: Fases 6-9
- [ ] Sección: Screenshots y navegación
- [ ] Sección: Troubleshooting
- [ ] Sección: Próximos pasos

### Validación (30 min)
- [ ] Probar webapp completa
- [ ] Verificar templates renderizando
- [ ] Tomar screenshots
- [ ] Verificar tiempo <1h

### Finalización (20 min)
- [ ] Agregar navegación
- [ ] Commit del archivo
- [ ] Actualizar sprint-4.md

## Resultado

_Se completará cuando el ticket esté DONE_

**Archivo generado:** `docs/examples/flask-webapp-project.md`

**Estado:** ⏳ Pendiente
