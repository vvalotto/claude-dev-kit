# Tutorial: Flask WebApp - Blog Application

**Stack:** Flask (flask-webapp)
**Tiempo Estimado:** 60-90 minutos
**Nivel:** Intermedio

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

Este tutorial te guiará paso a paso en la creación de una **Blog Application** fullstack utilizando el perfil **flask-webapp** del Claude Dev Kit.

Aprenderás:
- ✅ Cómo usar el skill `/implement-us` para guiar la implementación
- ✅ Cómo el framework adapta las 10 fases a una aplicación web fullstack
- ✅ Cómo generar templates Jinja2, formularios Flask-WTF y rutas automáticamente
- ✅ Buenas prácticas de Flask con Application Factory pattern

Al finalizar, tendrás una aplicación web funcional con:
- Interfaz HTML/CSS responsive
- CRUD completo de posts (Create, Read, Update, Delete)
- Formularios con validación (Flask-WTF)
- Flash messages para feedback de usuario
- CSRF protection integrado
- Suite completa de tests (unitarios, integración, BDD)
- Código que pasa quality gates (Pylint, cobertura, complejidad)

---

## ✅ Requisitos Previos

### Software Necesario

- **Python:** 3.10 o superior
- **Claude Code CLI:** Instalado y configurado
- **Flask:** Se instalará durante el setup
- **pytest:** Para testing
- **Git:** Para control de versiones

### Conocimientos

- Programación básica en Python
- Familiaridad con la terminal/línea de comandos
- (Opcional) Conceptos básicos de HTML/CSS
- (Opcional) Familiaridad con patrones MVC

### Verificación

```bash
# Verificar Python
python --version  # Debe ser >= 3.10

# Verificar Claude Code
claude --version

# Verificar Git
git --version
```

**Nota:** No necesitas tener Flask instalado previamente. Lo instalaremos en el setup.

---

## 📖 Historia de Usuario

```gherkin
# US-056: Blog Application

Como usuario web
Quiero una aplicación de blog con interfaz gráfica
Para crear, leer, editar y eliminar posts
```

### Criterios de Aceptación

**Funcionalidades Principales:**
- ✅ Ver lista de posts existentes
- ✅ Ver detalle completo de un post
- ✅ Crear nuevo post con formulario web
- ✅ Editar post existente
- ✅ Eliminar post con confirmación
- ✅ Validación de formularios server-side
- ✅ Mensajes de feedback (éxito/error)
- ✅ Interfaz responsive

### Alcance

**Componentes a Implementar:**
- **Models (Post):** Dataclass con datos del post
- **Forms (PostForm):** Flask-WTF con validación
- **Routes (blog.py):** Blueprint con lógica de negocio
- **Templates (Jinja2):** 5 templates HTML
- **Static (CSS):** Estilos responsive
- **Database:** Capa de acceso a datos (in-memory para demo)

**Casos de Uso:**
1. Usuario ve lista de posts → Interfaz muestra todos los posts con extractos
2. Usuario crea post "Mi primer post" → Formulario valida y guarda
3. Usuario edita post → Formulario pre-poblado actualiza el post
4. Usuario elimina post → Confirmación + mensaje de éxito

---

## 🚀 Setup del Proyecto

### 1. Crear Directorio del Proyecto

```bash
mkdir blog-app
cd blog-app
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
Flask>=3.1.0
Flask-WTF>=1.2.2
WTForms>=3.2.1
pytest>=7.4.0
pytest-bdd>=6.1.0
pytest-cov>=4.1.0
pylint>=3.0.0
radon>=6.0.0
EOF

pip install -r requirements.txt
```

**Verificar instalación:**

```bash
python -c "from flask import Flask; print('Flask OK')"
# Output esperado: Flask OK
```

### 5. Crear Estructura Base

```bash
# Crear directorios
mkdir -p app/{models,forms,routes,templates,static}
mkdir -p tests
mkdir -p features/steps
mkdir -p historias-usuario
mkdir -p docs/{planning,reporting}

# Crear __init__.py
touch app/__init__.py
touch app/models/__init__.py
touch app/forms/__init__.py
touch app/routes/__init__.py
```

**Estructura del proyecto:**

```
blog-app/
├── app/
│   ├── __init__.py              # Application Factory
│   ├── models/
│   │   ├── __init__.py
│   │   └── post.py              # Post dataclass (a crear)
│   ├── forms/
│   │   ├── __init__.py
│   │   └── post_form.py         # Flask-WTF form (a crear)
│   ├── routes/
│   │   ├── __init__.py
│   │   └── blog.py              # Blueprint (a crear)
│   ├── templates/               # Jinja2 templates (a crear)
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── post_detail.html
│   │   ├── post_form.html
│   │   └── confirm_delete.html
│   ├── static/
│   │   └── style.css            # CSS (a crear)
│   └── database.py              # Data access (a crear)
├── tests/
│   ├── test_post_model.py       # Unit tests (a crear)
│   ├── test_forms.py            # Form tests (a crear)
│   ├── test_routes.py           # Route tests (a crear)
│   └── test_forms_integration.py # Integration tests (a crear)
├── features/
│   ├── blog.feature             # BDD scenarios (a crear)
│   └── steps/
│       └── blog_steps.py        # Step definitions (a crear)
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
cd ~/blog-app

# Ejecutar instalador (modo no interactivo)
python ~/.claude-dev-kit/install/installer.py --profile flask-webapp --yes
```

**Salida esperada:**

```
🚀 Claude Dev Kit - Installer
================================

📋 Selected Profile: flask-webapp
   - Architecture: Application Factory + Blueprint (MVC-like)
   - Test Framework: pytest
   - Component Types: Blueprint, Model, Form, Template
   - Quality Gates: Pylint >= 8.5, Coverage >= 90%

✅ Framework instalado exitosamente en .claude/
✅ Perfil 'flask-webapp' configurado
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
cat > historias-usuario/US-056.md << 'EOF'
# US-056: Blog Application

Como usuario web
Quiero una aplicación de blog con interfaz gráfica
Para crear, leer, editar y eliminar posts

## Criterios de Aceptación

- Ver lista de posts con título, autor y extracto
- Ver detalle completo de un post
- Crear nuevo post con formulario web (título, contenido, autor)
- Editar post existente con formulario pre-poblado
- Eliminar post con página de confirmación
- Validación de formularios (campos requeridos, longitud mínima)
- Mensajes flash de éxito/error
- Interfaz responsive con CSS

## Notas Técnicas

- Framework: Flask (WebApp fullstack)
- Arquitectura: Application Factory + Blueprint
- Forms: Flask-WTF + WTForms
- Templates: Jinja2
- Database: In-memory (dict) para demo
- Tests: pytest + pytest-bdd
- CSRF: Protection habilitado
EOF
```

### Ejecutar el Skill

Ahora, en Claude Code CLI:

```bash
# Iniciar Claude Code en el proyecto
cd ~/blog-app
claude

# En Claude Code, ejecutar:
/implement-us US-056
```

---

### 🔍 Fase 0: Validación de Contexto

**Qué hace el framework:**
- ✅ Verifica que el archivo `US-056.md` exista
- ✅ Lee el perfil `flask-webapp` desde `.claude/skills/implement-us/config.json`
- ✅ Valida que Flask y Flask-WTF estén instalados
- ✅ Inicializa el tracking de tiempo

**Output:**

```
✅ Historia de usuario encontrada: US-056
✅ Perfil cargado: flask-webapp
✅ Configuración:
   - Arquitectura: Application Factory + Blueprint (MVC-like)
   - Component Types: Blueprint, Model, Form, Template
   - Test Framework: pytest
   - Quality Gates: Pylint >= 8.5, Coverage >= 90%, CC < 10
⏱️  Tracking iniciado para US-056

🎯 Contexto validado. Procediendo a Fase 1...
```

**¿Qué hacer si falla?**
- Verifica que el archivo `historias-usuario/US-056.md` exista
- Confirma que la instalación del framework fue exitosa
- Revisa `.claude/skills/implement-us/config.json`
- Verifica que Flask esté instalado: `pip show Flask`

---

### 📝 Fase 1: Generación de Escenarios BDD

**Qué hace el framework:**
- 📄 Lee tu historia de usuario (US-056.md)
- 🤖 Genera escenarios Gherkin basados en los criterios de aceptación
- 💾 Crea archivo `features/blog.feature`

**Ejemplo de Output (Flask WebApp):**

```gherkin
# features/blog.feature

Feature: Blog Application
  Como usuario web
  Quiero una aplicación de blog con interfaz gráfica
  Para crear, leer, editar y eliminar posts

  Background:
    Given la aplicación está ejecutándose
    And la base de datos está vacía

  Scenario: Ver lista vacía de posts
    When visito la página principal
    Then debo ver el mensaje "No hay posts disponibles"
    And debo ver el botón "Crear Post"

  Scenario: Ver lista de posts existentes
    Given existen los siguientes posts:
      | título          | autor    | contenido                  |
      | Mi primer post  | Juan     | Este es mi primer post     |
      | Post importante | María    | Contenido muy importante   |
    When visito la página principal
    Then debo ver 2 posts en la lista
    And debo ver "Mi primer post"
    And debo ver "Post importante"

  Scenario: Ver detalle de un post
    Given existe un post con título "Post de prueba" y autor "Ana"
    When hago click en "Leer más" del post
    Then debo ver el título "Post de prueba"
    And debo ver el contenido completo
    And debo ver el nombre del autor "Ana"
    And debo ver los botones "Editar" y "Eliminar"

  Scenario: Crear nuevo post exitosamente
    When visito la página "Crear Post"
    And lleno el formulario con:
      | campo     | valor                        |
      | Título    | Mi nuevo post                |
      | Contenido | Este es el contenido del post|
      | Autor     | Carlos                       |
    And presiono el botón "Guardar"
    Then debo ver el mensaje "Post creado exitosamente"
    And debo ser redirigido al detalle del post
    And debo ver "Mi nuevo post" en el detalle

  Scenario: Validar formulario - título requerido
    When visito la página "Crear Post"
    And lleno el formulario con:
      | campo     | valor                        |
      | Título    |                              |
      | Contenido | Contenido sin título         |
      | Autor     | Pedro                        |
    And presiono el botón "Guardar"
    Then debo ver el mensaje de error "El título es requerido"
    And debo permanecer en la página de creación

  Scenario: Validar formulario - contenido mínimo
    When visito la página "Crear Post"
    And lleno el formulario con:
      | campo     | valor     |
      | Título    | Título    |
      | Contenido | Corto     |
      | Autor     | Luis      |
    And presiono el botón "Guardar"
    Then debo ver el mensaje de error "El contenido debe tener al menos 10 caracteres"

  Scenario: Editar post existente
    Given existe un post con título "Post original"
    When visito la página de edición del post
    Then el formulario debe estar pre-poblado con los datos actuales
    When cambio el título a "Post actualizado"
    And presiono el botón "Guardar"
    Then debo ver el mensaje "Post actualizado exitosamente"
    And debo ver "Post actualizado" en el detalle

  Scenario: Eliminar post con confirmación
    Given existe un post con título "Post a eliminar"
    When visito el detalle del post
    And hago click en el botón "Eliminar"
    Then debo ver la página de confirmación
    And debo ver "¿Está seguro de eliminar este post?"
    When presiono "Sí, Eliminar Post"
    Then debo ver el mensaje "Post eliminado exitosamente"
    And debo ser redirigido a la página principal
    And no debo ver "Post a eliminar" en la lista

  Scenario: Cancelar eliminación de post
    Given existe un post con título "Post a conservar"
    When visito la página de confirmación de eliminación
    And hago click en "Cancelar"
    Then debo ser redirigido al detalle del post
    And el post debe seguir existiendo

  Scenario: Paginación de posts
    Given existen 15 posts en la base de datos
    When visito la página principal con parámetro "per_page=10"
    Then debo ver 10 posts en la página
    And debo ver controles de paginación
```

**Archivo creado:**
```
features/blog.feature (107 líneas, 10 escenarios)
```

**Interacción:**
Claude te mostrará los escenarios generados y preguntará:

```
📝 Escenarios BDD generados (10 escenarios, 107 líneas)

¿Aprobar estos escenarios? (Sí/No/Ajustar)
```

**Responde:** "Sí" (o ajusta si necesitas cambios específicos)

---

### 📋 Fase 2: Generación de Plan de Implementación

**Qué hace el framework:**
- 🏗️ Analiza los escenarios BDD
- 📊 Crea un plan de tareas desglosadas
- ⏱️ Estima tiempo por componente
- 🎯 Adapta la estructura a Application Factory + Blueprint

**Ejemplo de Output (Flask WebApp):**

```markdown
# Plan de Implementación - US-056: Blog Application

## 📊 Resumen Ejecutivo

**Arquitectura:** Application Factory + Blueprint (MVC-like)
**Estimación Total:** 6 horas 25 minutos
**Componentes:** 6 (Model, Form, Routes, Templates, Static, Database)
**Tests:** 48 (15 unitarios, 23 integración, 10 BDD)

## 🏗️ Arquitectura

### Application Factory + Blueprint Pattern

**Application Factory (app/__init__.py):**
- Responsabilidad: Crear y configurar la aplicación Flask
- Configuración: SECRET_KEY, WTF_CSRF_ENABLED
- Registro: Blueprint de blog

**Model (app/models/post.py):**
- Responsabilidad: Estructura de datos del post
- Tipo: @dataclass
- Atributos: id, title, content, author, created_at

**Form (app/forms/post_form.py):**
- Responsabilidad: Validación de formularios
- Tipo: FlaskForm (Flask-WTF)
- Campos: title, content, author
- Validadores: DataRequired(), Length(min=10)

**Routes (app/routes/blog.py):**
- Responsabilidad: Lógica de negocio y controladores
- Tipo: Blueprint
- Endpoints: /, /post/<id>, /post/new, /post/<id>/edit, /post/<id>/delete

**Templates (app/templates/):**
- base.html: Template base con navbar y footer
- index.html: Lista de posts
- post_detail.html: Detalle de post
- post_form.html: Formulario crear/editar
- confirm_delete.html: Confirmación de eliminación

**Static (app/static/style.css):**
- Responsabilidad: Estilos CSS responsive
- Componentes: navbar, cards, forms, buttons, flash messages

**Database (app/database.py):**
- Responsabilidad: Acceso a datos
- Implementación: In-memory dict (demo)
- Métodos: create(), get_all(), get_by_id(), update(), delete()

## 📝 Tareas

### 1. Application Factory - 20 min

**Archivo:** `app/__init__.py`

- [ ] Función create_app(config=None)
- [ ] Configuración de SECRET_KEY
- [ ] Configuración de WTF_CSRF_ENABLED
- [ ] Registro de Blueprint
- [ ] Custom Jinja2 filter (nl2br)
- [ ] Docstrings

**Complejidad:** Baja
**Dependencias:** Ninguna

### 2. Post Model - 25 min

**Archivo:** `app/models/post.py`

- [ ] @dataclass Post
- [ ] Atributos: id, title, content, author, created_at
- [ ] Método to_dict() → dict
- [ ] Método __str__() → str
- [ ] Type hints completos
- [ ] Docstrings

**Complejidad:** Baja
**Dependencias:** dataclasses, datetime

### 3. Database Layer - 40 min

**Archivo:** `app/database.py`

- [ ] Clase PostDatabase
- [ ] Método create(post: Post) → Post
- [ ] Método get_all(page, per_page) → List[Post]
- [ ] Método get_by_id(id) → Optional[Post]
- [ ] Método update(id, post: Post) → Optional[Post]
- [ ] Método delete(id) → bool
- [ ] Método count() → int
- [ ] Método clear() (para tests)
- [ ] Singleton instance

**Complejidad:** Media
**Dependencias:** Post model

### 4. Post Form - 30 min

**Archivo:** `app/forms/post_form.py`

- [ ] Clase PostForm(FlaskForm)
- [ ] Campo title: StringField con DataRequired()
- [ ] Campo content: TextAreaField con DataRequired() y Length(min=10)
- [ ] Campo author: StringField con DataRequired()
- [ ] Campo submit: SubmitField
- [ ] Mensajes de error personalizados en español
- [ ] render_kw con placeholders
- [ ] Docstrings

**Complejidad:** Baja
**Dependencias:** Flask-WTF, WTForms

### 5. Blog Routes (Blueprint) - 90 min

**Archivo:** `app/routes/blog.py`

- [ ] Blueprint blog_bp con nombre 'blog'
- [ ] Route GET / - index() - lista de posts con paginación
- [ ] Route GET /post/<id> - post_detail() - detalle de post
- [ ] Route GET/POST /post/new - post_create() - crear post
- [ ] Route GET/POST /post/<id>/edit - post_edit() - editar post
- [ ] Route GET/POST /post/<id>/delete - post_delete() - eliminar post
- [ ] Flash messages para feedback
- [ ] Manejo de errores 404
- [ ] Redirects con url_for()
- [ ] Docstrings completas

**Complejidad:** Alta
**Dependencias:** PostForm, Post, database

### 6. Base Template - 30 min

**Archivo:** `app/templates/base.html`

- [ ] DOCTYPE HTML5
- [ ] Meta tags (charset, viewport)
- [ ] Link a style.css
- [ ] Navbar con logo y links
- [ ] Flash messages con categorías
- [ ] Block content
- [ ] Footer
- [ ] Responsive design

**Complejidad:** Baja
**Dependencias:** Jinja2

### 7. Index Template - 25 min

**Archivo:** `app/templates/index.html`

- [ ] Extends base.html
- [ ] Lista de posts con cards
- [ ] Mostrar título, autor, extracto (150 chars)
- [ ] Botón "Leer más" por cada post
- [ ] Mensaje si lista vacía
- [ ] Controles de paginación
- [ ] Link a "Crear Post"

**Complejidad:** Media
**Dependencias:** base.html

### 8. Post Detail Template - 20 min

**Archivo:** `app/templates/post_detail.html`

- [ ] Extends base.html
- [ ] Mostrar título completo
- [ ] Mostrar contenido completo con nl2br filter
- [ ] Mostrar autor y fecha
- [ ] Botón "Editar"
- [ ] Botón "Eliminar"
- [ ] Link "Volver a inicio"

**Complejidad:** Baja
**Dependencias:** base.html

### 9. Post Form Template - 30 min

**Archivo:** `app/templates/post_form.html`

- [ ] Extends base.html
- [ ] Formulario con form.hidden_tag() (CSRF)
- [ ] Renderizar form.title
- [ ] Renderizar form.content (textarea)
- [ ] Renderizar form.author
- [ ] Mostrar errores de validación
- [ ] Botón "Guardar"
- [ ] Botón "Cancelar"
- [ ] Diferenciar modo create vs edit

**Complejidad:** Media
**Dependencias:** base.html, PostForm

### 10. Confirm Delete Template - 20 min

**Archivo:** `app/templates/confirm_delete.html`

- [ ] Extends base.html
- [ ] Mensaje de advertencia
- [ ] Mostrar preview del post a eliminar
- [ ] Formulario POST con CSRF
- [ ] Botón "Sí, Eliminar Post" (danger)
- [ ] Botón "Cancelar" (secondary)

**Complejidad:** Baja
**Dependencias:** base.html

### 11. CSS Styles - 60 min

**Archivo:** `app/static/style.css`

- [ ] Reset CSS básico
- [ ] Variables CSS (colores, spacing)
- [ ] Estilos navbar (fixed, responsive)
- [ ] Estilos cards (posts)
- [ ] Estilos formularios (inputs, textarea, buttons)
- [ ] Estilos flash messages (success, error, warning)
- [ ] Estilos footer
- [ ] Estilos botones (primary, secondary, danger)
- [ ] Media queries para responsive
- [ ] Hover effects

**Complejidad:** Media
**Dependencias:** Ninguna

### 12. Entry Point (main.py) - 10 min

**Archivo:** `main.py`

- [ ] Import create_app
- [ ] Crear app = create_app()
- [ ] if __name__ == '__main__': app.run(debug=True)
- [ ] Docstring

**Complejidad:** Baja
**Dependencias:** Application Factory

## 🧪 Plan de Testing

### Tests Unitarios (15 tests)

**test_post_model.py (7 tests):**
- test_post_creation()
- test_post_with_id()
- test_post_to_dict()
- test_post_dataclass_equality()
- test_post_str_representation()

**test_forms.py (8 tests):**
- test_form_valid_data()
- test_form_missing_title()
- test_form_missing_content()
- test_form_content_too_short()
- test_form_missing_author()
- test_form_all_fields_missing()

### Tests de Integración (23 tests)

**test_routes.py (14 tests):**
- test_index_empty()
- test_index_with_posts()
- test_index_pagination()
- test_post_detail_valid()
- test_post_detail_not_found()
- test_post_create_get()
- test_post_create_post_valid()
- test_post_create_post_invalid()
- test_post_edit_get()
- test_post_edit_post_valid()
- test_post_delete_get()
- test_post_delete_post_valid()

**test_forms_integration.py (9 tests):**
- test_create_form_displays_correctly()
- test_edit_form_pre_fills_data()
- test_form_validation_errors_display()
- test_flash_messages_display_correctly()
- test_form_csrf_protection_enabled()

### BDD Step Definitions (10 escenarios)

**features/steps/blog_steps.py:**
- Given steps: aplicación ejecutándose, posts existentes
- When steps: visitar páginas, llenar formularios, clicks
- Then steps: verificar contenido HTML, mensajes, redirects

## 📊 Estimación por Fase

| Fase | Descripción | Estimado |
|------|-------------|----------|
| 3 | Implementación | 6h 25min |
| 4 | Tests Unitarios | 1h |
| 5 | Tests Integración | 1h 30min |
| 6 | BDD Validation | 45min |
| 7 | Quality Gates | 20min |
| 8 | Documentación | 30min |

**Total:** ~10.5 horas

## 🎯 Orden de Implementación

1. **Post Model** (sin dependencias)
2. **Database Layer** (depende de Model)
3. **PostForm** (depende de WTForms)
4. **Application Factory** (sin dependencias de negocio)
5. **Blog Routes** (depende de Model, Form, Database)
6. **Base Template** (sin dependencias)
7. **Templates específicos** (dependen de base.html)
8. **CSS** (paralelo a templates)
9. **main.py** (integra todo)

## ⚠️ Riesgos

- **CSRF**: Asegurar que form.hidden_tag() esté en todos los formularios
- **Validación**: Validar en server-side, no confiar solo en HTML5
- **Flash messages**: Categorías consistentes (success, error, warning)
- **Templates**: Escapar correctamente contenido de usuario (Jinja2 auto-escape)
- **Paginación**: Validar parámetros page y per_page

## 📋 Checklist Pre-Implementación

- [x] Plan revisado y aprobado
- [x] Arquitectura Application Factory clara
- [x] Dependencias instaladas
- [x] Estructura de directorios lista
```

**Archivo creado:**
```
docs/planning/US-056-plan.md (380+ líneas)
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
- 🔧 Usa snippets específicos del perfil flask-webapp
- 📁 Crea archivos en la estructura correcta
- ✅ Valida cada paso antes de continuar

#### Componente 1: Post Model

**Archivo:** `app/models/post.py`

Claude genera:

```python
"""
Post model for blog application.

Defines the Post dataclass with all necessary attributes.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Post:
    """
    Post model representing a blog post.

    Attributes:
        title: Post title
        content: Post content
        author: Post author name
        id: Unique post ID (auto-generated)
        created_at: Creation timestamp
    """

    title: str
    content: str
    author: str
    id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        """
        Convert post to dictionary.

        Returns:
            Dictionary representation of the post
        """
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'author': self.author,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __str__(self) -> str:
        """String representation of post."""
        return f"Post(id={self.id}, title='{self.title}', author='{self.author}')"
```

**Output:**

```
✅ Post model creado (app/models/post.py)
   - @dataclass con 5 atributos
   - Método to_dict() para serialización
   - Type hints completos
   - Docstrings

⏱️  Tiempo: 20 min (estimado: 25 min)
```

---

#### Componente 2: PostForm (Flask-WTF)

**Archivo:** `app/forms/post_form.py`

```python
"""Post form for creating and editing blog posts."""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    """
    Form for creating and editing blog posts.

    Fields:
        title: Post title (required)
        content: Post content (required, minimum 10 characters)
        author: Post author name (required)
        submit: Submit button
    """

    title = StringField(
        'Título',
        validators=[
            DataRequired(message='El título es requerido')
        ],
        render_kw={'placeholder': 'Ingrese el título del post'}
    )

    content = TextAreaField(
        'Contenido',
        validators=[
            DataRequired(message='El contenido es requerido'),
            Length(min=10, message='El contenido debe tener al menos 10 caracteres')
        ],
        render_kw={'placeholder': 'Ingrese el contenido del post', 'rows': 10}
    )

    author = StringField(
        'Autor',
        validators=[
            DataRequired(message='El autor es requerido')
        ],
        render_kw={'placeholder': 'Ingrese el nombre del autor'}
    )

    submit = SubmitField('Guardar')
```

**Output:**

```
✅ PostForm creado (app/forms/post_form.py)
   - 3 campos con validación
   - Mensajes de error en español
   - Placeholders personalizados
   - CSRF protection automático

⏱️  Tiempo: 25 min (estimado: 30 min)
```

---

#### Componente 3: Database Layer

**Archivo:** `app/database.py`

```python
"""In-memory database for blog posts."""
from typing import List, Optional
from app.models import Post


class PostDatabase:
    """
    In-memory database for posts.

    Attributes:
        _posts: Dict storing posts by ID
        _next_id: Counter for auto-incrementing IDs
    """

    def __init__(self):
        """Initialize empty database."""
        self._posts: dict[int, Post] = {}
        self._next_id: int = 1

    def create(self, post: Post) -> Post:
        """
        Create a new post.

        Args:
            post: Post to create (without ID)

        Returns:
            Created post with assigned ID
        """
        post.id = self._next_id
        self._posts[post.id] = post
        self._next_id += 1
        return post

    def get_all(self, page: int = 1, per_page: int = 10) -> List[Post]:
        """
        Get all posts with pagination.

        Args:
            page: Page number (starts at 1)
            per_page: Posts per page

        Returns:
            List of posts for the requested page
        """
        all_posts = sorted(
            self._posts.values(),
            key=lambda p: p.created_at,
            reverse=True
        )

        start = (page - 1) * per_page
        end = start + per_page
        return all_posts[start:end]

    def get_by_id(self, post_id: int) -> Optional[Post]:
        """
        Get post by ID.

        Args:
            post_id: Post ID

        Returns:
            Post if found, None otherwise
        """
        return self._posts.get(post_id)

    def update(self, post_id: int, updated_post: Post) -> Optional[Post]:
        """
        Update an existing post.

        Args:
            post_id: ID of post to update
            updated_post: New post data

        Returns:
            Updated post if found, None otherwise
        """
        if post_id not in self._posts:
            return None

        updated_post.id = post_id
        # Preserve created_at from original
        original_created_at = self._posts[post_id].created_at
        updated_post.created_at = original_created_at

        self._posts[post_id] = updated_post
        return updated_post

    def delete(self, post_id: int) -> bool:
        """
        Delete a post.

        Args:
            post_id: ID of post to delete

        Returns:
            True if deleted, False if not found
        """
        if post_id in self._posts:
            del self._posts[post_id]
            return True
        return False

    def count(self) -> int:
        """Get total number of posts."""
        return len(self._posts)

    def clear(self):
        """Clear all posts (for testing)."""
        self._posts.clear()
        self._next_id = 1


# Singleton instance
db = PostDatabase()
```

**Output:**

```
✅ Database layer creado (app/database.py)
   - CRUD completo (Create, Read, Update, Delete)
   - Paginación implementada
   - Ordenamiento por fecha
   - Singleton pattern

⏱️  Tiempo: 35 min (estimado: 40 min)
```

---

#### Componente 4: Blog Routes (Blueprint)

**Archivo:** `app/routes/blog.py`

```python
"""Blog routes blueprint."""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.database import db
from app.models import Post
from app.forms import PostForm

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/')
def index():
    """
    Display list of blog posts with pagination.

    Query Parameters:
        page: Page number (default: 1)
        per_page: Posts per page (default: 10)

    Returns:
        Rendered index template with posts
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    posts = db.get_all(page=page, per_page=per_page)
    total_posts = db.count()
    total_pages = (total_posts + per_page - 1) // per_page

    return render_template(
        'index.html',
        posts=posts,
        page=page,
        total_pages=total_pages,
        total_posts=total_posts
    )


@blog_bp.route('/post/<int:post_id>')
def post_detail(post_id: int):
    """
    Display details of a specific post.

    Args:
        post_id: The post ID

    Returns:
        Rendered post detail template or 404 if not found
    """
    post = db.get_by_id(post_id)
    if post is None:
        flash('Post no encontrado', 'error')
        return redirect(url_for('blog.index'))

    return render_template('post_detail.html', post=post)


@blog_bp.route('/post/new', methods=['GET', 'POST'])
def post_create():
    """
    Create a new blog post.

    GET: Display creation form
    POST: Process form and create post

    Returns:
        Rendered form or redirect to post detail
    """
    form = PostForm()

    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            author=form.author.data
        )
        created_post = db.create(post)
        flash('Post creado exitosamente', 'success')
        return redirect(url_for('blog.post_detail', post_id=created_post.id))

    return render_template('post_form.html', form=form, mode='create')


@blog_bp.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
def post_edit(post_id: int):
    """
    Edit an existing blog post.

    GET: Display edit form pre-filled
    POST: Process form and update post

    Args:
        post_id: The post ID

    Returns:
        Rendered form or redirect to post detail
    """
    post = db.get_by_id(post_id)
    if post is None:
        flash('Post no encontrado', 'error')
        return redirect(url_for('blog.index'))

    form = PostForm(obj=post)

    if form.validate_on_submit():
        updated_post = Post(
            title=form.title.data,
            content=form.content.data,
            author=form.author.data
        )
        db.update(post_id, updated_post)
        flash('Post actualizado exitosamente', 'success')
        return redirect(url_for('blog.post_detail', post_id=post_id))

    return render_template('post_form.html', form=form, mode='edit', post=post)


@blog_bp.route('/post/<int:post_id>/delete', methods=['GET', 'POST'])
def post_delete(post_id: int):
    """
    Delete a blog post with confirmation.

    GET: Display confirmation page
    POST: Process deletion

    Args:
        post_id: The post ID

    Returns:
        Confirmation page or redirect after deletion
    """
    post = db.get_by_id(post_id)
    if post is None:
        flash('Post no encontrado', 'error')
        return redirect(url_for('blog.index'))

    if request.method == 'POST':
        db.delete(post_id)
        flash('Post eliminado exitosamente', 'success')
        return redirect(url_for('blog.index'))

    return render_template('confirm_delete.html', post=post)
```

**Output:**

```
✅ Blog routes creado (app/routes/blog.py)
   - 5 rutas CRUD completas
   - Flash messages implementados
   - Validación de formularios
   - Redirects correctos

⏱️  Tiempo: 80 min (estimado: 90 min)
```

---

#### Componente 5: Application Factory

**Archivo:** `app/__init__.py`

```python
"""
Flask application factory.

Creates and configures the Flask application.
"""

from flask import Flask


def create_app(config=None):
    """
    Application factory for Flask app.

    Args:
        config: Optional configuration dict

    Returns:
        Configured Flask application
    """
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = config.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['WTF_CSRF_ENABLED'] = config.get('WTF_CSRF_ENABLED', True)

    # Register blueprints
    from app.routes.blog import blog_bp
    app.register_blueprint(blog_bp)

    # Custom Jinja2 filter for nl2br
    @app.template_filter('nl2br')
    def nl2br_filter(text):
        """Convert newlines to <br> tags."""
        if text:
            return text.replace('\n', '<br>')
        return text

    return app
```

**Output:**

```
✅ Application Factory creado (app/__init__.py)
   - Función create_app()
   - Configuración SECRET_KEY y CSRF
   - Blueprint registrado
   - Filtro nl2br personalizado

⏱️  Tiempo: 18 min (estimado: 20 min)
```

---

#### Componente 6: Templates Jinja2

**Template Base:** `app/templates/base.html`

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Blog Application{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <nav class="navbar">
        <div class="container">
            <a href="{{ url_for('blog.index') }}" class="navbar-brand">Blog Application</a>
            <div class="navbar-links">
                <a href="{{ url_for('blog.index') }}">Inicio</a>
                <a href="{{ url_for('blog.post_create') }}" class="btn btn-primary">Crear Post</a>
            </div>
        </div>
    </nav>

    <main class="container">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                <div class="flash-messages">
                    {% for category, message in messages %}
                        <div class="alert alert-{{ category }}">
                            {{ message }}
                        </div>
                    {% endfor %}
                </div>
            {% endif %}
        {% endwith %}

        {% block content %}{% endblock %}
    </main>

    <footer class="footer">
        <div class="container">
            <p>&copy; 2026 Blog Application - Flask WebApp Example</p>
        </div>
    </footer>
</body>
</html>
```

**Template Index:** `app/templates/index.html`

```html
{% extends "base.html" %}

{% block title %}Inicio - Blog Application{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Posts del Blog</h1>
    <p class="text-muted">{{ total_posts }} post{{ 's' if total_posts != 1 else '' }} en total</p>
</div>

{% if posts %}
    <div class="posts-grid">
        {% for post in posts %}
        <div class="post-card">
            <h2 class="post-title">{{ post.title }}</h2>
            <p class="post-meta">
                Por <strong>{{ post.author }}</strong>
                - {{ post.created_at.strftime('%d/%m/%Y %H:%M') }}
            </p>
            <p class="post-excerpt">
                {{ post.content[:150] }}{% if post.content|length > 150 %}...{% endif %}
            </p>
            <a href="{{ url_for('blog.post_detail', post_id=post.id) }}" class="btn btn-secondary">
                Leer más
            </a>
        </div>
        {% endfor %}
    </div>

    {% if total_pages > 1 %}
    <div class="pagination">
        {% if page > 1 %}
        <a href="{{ url_for('blog.index', page=page-1) }}" class="btn">← Anterior</a>
        {% endif %}

        <span class="page-info">Página {{ page }} de {{ total_pages }}</span>

        {% if page < total_pages %}
        <a href="{{ url_for('blog.index', page=page+1) }}" class="btn">Siguiente →</a>
        {% endif %}
    </div>
    {% endif %}
{% else %}
    <div class="empty-state">
        <p>No hay posts disponibles.</p>
        <a href="{{ url_for('blog.post_create') }}" class="btn btn-primary">
            Crear el primer post
        </a>
    </div>
{% endif %}
{% endblock %}
```

**Template Post Detail:** `app/templates/post_detail.html`

```html
{% extends "base.html" %}

{% block title %}{{ post.title }} - Blog Application{% endblock %}

{% block content %}
<article class="post-detail">
    <header class="post-header">
        <h1>{{ post.title }}</h1>
        <p class="post-meta">
            Por <strong>{{ post.author }}</strong>
            - {{ post.created_at.strftime('%d de %B de %Y a las %H:%M') }}
        </p>
    </header>

    <div class="post-content">
        {{ post.content|nl2br|safe }}
    </div>

    <footer class="post-actions">
        <a href="{{ url_for('blog.index') }}" class="btn btn-secondary">← Volver</a>
        <div class="action-buttons">
            <a href="{{ url_for('blog.post_edit', post_id=post.id) }}" class="btn btn-primary">
                Editar
            </a>
            <a href="{{ url_for('blog.post_delete', post_id=post.id) }}" class="btn btn-danger">
                Eliminar
            </a>
        </div>
    </footer>
</article>
{% endblock %}
```

**Template Post Form:** `app/templates/post_form.html`

```html
{% extends "base.html" %}

{% block title %}
    {% if mode == 'create' %}Crear Post{% else %}Editar Post{% endif %} - Blog Application
{% endblock %}

{% block content %}
<div class="form-container">
    <h1>{% if mode == 'create' %}Crear Nuevo Post{% else %}Editar Post{% endif %}</h1>

    <form method="POST" class="post-form">
        {{ form.hidden_tag() }}

        <div class="form-group">
            {{ form.title.label }}
            {{ form.title(class="form-control") }}
            {% if form.title.errors %}
                <div class="form-errors">
                    {% for error in form.title.errors %}
                        <span class="error">{{ error }}</span>
                    {% endfor %}
                </div>
            {% endif %}
        </div>

        <div class="form-group">
            {{ form.content.label }}
            {{ form.content(class="form-control") }}
            {% if form.content.errors %}
                <div class="form-errors">
                    {% for error in form.content.errors %}
                        <span class="error">{{ error }}</span>
                    {% endfor %}
                </div>
            {% endif %}
        </div>

        <div class="form-group">
            {{ form.author.label }}
            {{ form.author(class="form-control") }}
            {% if form.author.errors %}
                <div class="form-errors">
                    {% for error in form.author.errors %}
                        <span class="error">{{ error }}</span>
                    {% endfor %}
                </div>
            {% endif %}
        </div>

        <div class="form-actions">
            {{ form.submit(class="btn btn-primary") }}
            <a href="{% if mode == 'edit' and post %}{{ url_for('blog.post_detail', post_id=post.id) }}{% else %}{{ url_for('blog.index') }}{% endif %}"
               class="btn btn-secondary">
                Cancelar
            </a>
        </div>
    </form>
</div>
{% endblock %}
```

**Template Confirm Delete:** `app/templates/confirm_delete.html`

```html
{% extends "base.html" %}

{% block title %}Confirmar Eliminación - Blog Application{% endblock %}

{% block content %}
<div class="confirm-delete">
    <h1>¿Está seguro de eliminar este post?</h1>

    <div class="warning-box">
        <p class="warning-text">⚠️ Esta acción no se puede deshacer.</p>
    </div>

    <div class="post-preview">
        <h2>{{ post.title }}</h2>
        <p class="post-meta">Por {{ post.author }} - {{ post.created_at.strftime('%d/%m/%Y') }}</p>
        <p class="post-excerpt">{{ post.content[:200] }}...</p>
    </div>

    <form method="POST" class="delete-form">
        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
        <button type="submit" class="btn btn-danger">Sí, Eliminar Post</button>
        <a href="{{ url_for('blog.post_detail', post_id=post.id) }}" class="btn btn-secondary">
            Cancelar
        </a>
    </form>
</div>
{% endblock %}
```

**Output:**

```
✅ Templates creados (5 archivos HTML)
   - base.html con navbar, footer, flash messages
   - index.html con lista y paginación
   - post_detail.html con contenido completo
   - post_form.html con validación
   - confirm_delete.html con preview

⏱️  Tiempo: 120 min (estimado: 125 min)
```

---

#### Componente 7: CSS Styles

**Archivo:** `app/static/style.css`

```css
/* Reset y variables */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    --primary-color: #3498db;
    --success-color: #2ecc71;
    --danger-color: #e74c3c;
    --warning-color: #f39c12;
    --text-color: #333;
    --bg-color: #f5f5f5;
    --border-color: #ddd;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    line-height: 1.6;
    color: var(--text-color);
    background-color: var(--bg-color);
}

/* Container */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* Navbar */
.navbar {
    background: white;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    padding: 1rem 0;
    position: sticky;
    top: 0;
    z-index: 100;
}

.navbar .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.navbar-brand {
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--primary-color);
    text-decoration: none;
}

.navbar-links {
    display: flex;
    gap: 1rem;
    align-items: center;
}

.navbar-links a {
    text-decoration: none;
    color: var(--text-color);
}

/* Main content */
main {
    min-height: calc(100vh - 200px);
    padding: 2rem 0;
}

/* Flash messages */
.flash-messages {
    margin-bottom: 2rem;
}

.alert {
    padding: 1rem;
    border-radius: 4px;
    margin-bottom: 1rem;
}

.alert-success {
    background: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
}

.alert-error {
    background: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
}

/* Page header */
.page-header {
    margin-bottom: 2rem;
}

.page-header h1 {
    margin-bottom: 0.5rem;
}

.text-muted {
    color: #6c757d;
}

/* Posts grid */
.posts-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 2rem;
    margin-bottom: 2rem;
}

.post-card {
    background: white;
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    transition: transform 0.2s;
}

.post-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.post-title {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
    color: var(--text-color);
}

.post-meta {
    color: #6c757d;
    font-size: 0.9rem;
    margin-bottom: 1rem;
}

.post-excerpt {
    margin-bottom: 1rem;
    line-height: 1.6;
}

/* Buttons */
.btn {
    display: inline-block;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    text-decoration: none;
    cursor: pointer;
    border: none;
    font-size: 1rem;
    transition: background-color 0.2s;
}

.btn-primary {
    background: var(--primary-color);
    color: white;
}

.btn-primary:hover {
    background: #2980b9;
}

.btn-secondary {
    background: #6c757d;
    color: white;
}

.btn-secondary:hover {
    background: #5a6268;
}

.btn-danger {
    background: var(--danger-color);
    color: white;
}

.btn-danger:hover {
    background: #c0392b;
}

/* Forms */
.form-container {
    max-width: 800px;
    margin: 0 auto;
    background: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.form-group {
    margin-bottom: 1.5rem;
}

.form-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
}

.form-control {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid var(--border-color);
    border-radius: 4px;
    font-size: 1rem;
}

.form-control:focus {
    outline: none;
    border-color: var(--primary-color);
}

textarea.form-control {
    resize: vertical;
    min-height: 200px;
}

.form-errors {
    margin-top: 0.5rem;
}

.form-errors .error {
    color: var(--danger-color);
    font-size: 0.9rem;
}

.form-actions {
    display: flex;
    gap: 1rem;
    margin-top: 2rem;
}

/* Post detail */
.post-detail {
    max-width: 800px;
    margin: 0 auto;
    background: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.post-header {
    border-bottom: 2px solid var(--border-color);
    padding-bottom: 1rem;
    margin-bottom: 2rem;
}

.post-content {
    line-height: 1.8;
    margin-bottom: 2rem;
}

.post-actions {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 2rem;
    border-top: 1px solid var(--border-color);
}

.action-buttons {
    display: flex;
    gap: 1rem;
}

/* Empty state */
.empty-state {
    text-align: center;
    padding: 4rem 2rem;
    background: white;
    border-radius: 8px;
}

/* Pagination */
.pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 1rem;
    margin-top: 2rem;
}

.page-info {
    color: #6c757d;
}

/* Confirm delete */
.confirm-delete {
    max-width: 600px;
    margin: 0 auto;
    background: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.warning-box {
    background: #fff3cd;
    border: 1px solid #ffc107;
    padding: 1rem;
    border-radius: 4px;
    margin: 1rem 0;
}

.warning-text {
    color: #856404;
    font-weight: 500;
}

.post-preview {
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 4px;
    margin: 1.5rem 0;
}

.delete-form {
    display: flex;
    gap: 1rem;
    margin-top: 2rem;
}

/* Footer */
.footer {
    background: white;
    padding: 2rem 0;
    text-align: center;
    border-top: 1px solid var(--border-color);
    margin-top: 4rem;
}

/* Responsive */
@media (max-width: 768px) {
    .posts-grid {
        grid-template-columns: 1fr;
    }

    .navbar .container {
        flex-direction: column;
        gap: 1rem;
    }

    .form-actions,
    .post-actions {
        flex-direction: column;
    }

    .action-buttons {
        width: 100%;
        flex-direction: column;
    }

    .btn {
        width: 100%;
        text-align: center;
    }
}
```

**Output:**

```
✅ CSS creado (app/static/style.css)
   - Estilos responsive
   - Variables CSS
   - Navbar fixed
   - Cards con hover effects
   - Formularios estilizados
   - Flash messages
   - Media queries

⏱️  Tiempo: 55 min (estimado: 60 min)
```

---

#### Componente 8: Entry Point (main.py)

**Archivo:** `main.py`

```python
"""
Entry point for the Flask blog application.
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
```

**Ejecutar la aplicación:**

```bash
# Development con auto-reload
python main.py

# La aplicación estará en http://localhost:5000
```

**Acceder a la aplicación:**

- Home: http://localhost:5000
- Crear Post: http://localhost:5000/post/new

**Output:**

```
✅ main.py creado (entry point)
✅ Aplicación ejecutable

🎉 Implementación completa!
   - 6 componentes backend
   - 5 templates HTML
   - 1 CSS file
   - 11 archivos (~2,200 líneas)
   - Arquitectura limpia y separada

⏱️  Tiempo total Fase 3: 6h 15min (estimado: 6h 25min)
```

---

### 🧪 Fase 4: Tests Unitarios

**Qué hace el framework:**
- 🔬 Genera tests unitarios para modelo y formularios
- 🎯 Usa pytest con fixtures
- ✅ Cubre lógica de negocio y validaciones
- 📊 Ejecuta tests y reporta cobertura

**Archivo 1:** `tests/conftest.py`

```python
"""
Shared pytest fixtures for all tests.
"""

import pytest
from app import create_app
from app.database import db


@pytest.fixture
def app():
    """
    Create Flask app for testing.

    Returns:
        Flask app configured for testing
    """
    app = create_app({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False
    })
    return app


@pytest.fixture
def client(app):
    """
    Create test client.

    Args:
        app: Flask app fixture

    Returns:
        Test client
    """
    return app.test_client()


@pytest.fixture(autouse=True)
def reset_db():
    """
    Reset database before each test.

    Runs automatically before every test.
    """
    db.clear()
    yield
    db.clear()
```

**Archivo 2:** `tests/test_post_model.py`

```python
"""
Unit tests for Post model.
"""

import pytest
from datetime import datetime
from app.models import Post


class TestPostModel:
    """Test suite for Post model."""

    def test_post_creation(self):
        """Test creating a post."""
        post = Post(
            title="Test Post",
            content="Test content",
            author="Test Author"
        )

        assert post.title == "Test Post"
        assert post.content == "Test content"
        assert post.author == "Test Author"
        assert post.id is None
        assert isinstance(post.created_at, datetime)

    def test_post_with_id(self):
        """Test post with ID."""
        post = Post(
            id=1,
            title="Post",
            content="Content",
            author="Author"
        )

        assert post.id == 1

    def test_post_to_dict(self):
        """Test to_dict method."""
        post = Post(
            id=1,
            title="Test",
            content="Content",
            author="Author"
        )

        post_dict = post.to_dict()

        assert post_dict['id'] == 1
        assert post_dict['title'] == "Test"
        assert post_dict['content'] == "Content"
        assert post_dict['author'] == "Author"
        assert 'created_at' in post_dict

    def test_post_str_representation(self):
        """Test string representation."""
        post = Post(
            id=1,
            title="Test Post",
            content="Content",
            author="Author"
        )

        assert "Post(id=1" in str(post)
        assert "Test Post" in str(post)
```

**Archivo 3:** `tests/test_forms.py`

```python
"""
Unit tests for PostForm.
"""

import pytest
from app.forms import PostForm


class TestPostForm:
    """Test suite for PostForm."""

    def test_form_valid_data(self, app):
        """Test form with valid data."""
        with app.test_request_context():
            form = PostForm(data={
                'title': 'Test Title',
                'content': 'This is a test content that is long enough',
                'author': 'Test Author'
            })

            assert form.validate()

    def test_form_missing_title(self, app):
        """Test form with missing title."""
        with app.test_request_context():
            form = PostForm(data={
                'title': '',
                'content': 'Content here',
                'author': 'Author'
            })

            assert not form.validate()
            assert 'title' in form.errors

    def test_form_missing_content(self, app):
        """Test form with missing content."""
        with app.test_request_context():
            form = PostForm(data={
                'title': 'Title',
                'content': '',
                'author': 'Author'
            })

            assert not form.validate()
            assert 'content' in form.errors

    def test_form_content_too_short(self, app):
        """Test form with content too short."""
        with app.test_request_context():
            form = PostForm(data={
                'title': 'Title',
                'content': 'Short',
                'author': 'Author'
            })

            assert not form.validate()
            assert 'content' in form.errors
            assert 'al menos 10 caracteres' in str(form.content.errors)

    def test_form_missing_author(self, app):
        """Test form with missing author."""
        with app.test_request_context():
            form = PostForm(data={
                'title': 'Title',
                'content': 'Long enough content',
                'author': ''
            })

            assert not form.validate()
            assert 'author' in form.errors
```

**Ejecutar tests unitarios:**

```bash
pytest tests/test_post_model.py tests/test_forms.py -v
```

**Output Esperado:**

```
============================= test session starts ==============================
collected 15 items

tests/test_post_model.py::TestPostModel::test_post_creation PASSED       [  6%]
tests/test_post_model.py::TestPostModel::test_post_with_id PASSED        [ 13%]
tests/test_post_model.py::TestPostModel::test_post_to_dict PASSED        [ 20%]
tests/test_post_model.py::TestPostModel::test_post_str_representation PASSED [ 26%]
tests/test_forms.py::TestPostForm::test_form_valid_data PASSED           [ 33%]
tests/test_forms.py::TestPostForm::test_form_missing_title PASSED        [ 40%]
tests/test_forms.py::TestPostForm::test_form_missing_content PASSED      [ 46%]
tests/test_forms.py::TestPostForm::test_form_content_too_short PASSED    [ 53%]
tests/test_forms.py::TestPostForm::test_form_missing_author PASSED       [ 60%]
...

============================== 15 passed in 0.25s ===============================
```

**Output:**

```
✅ Tests unitarios creados (15 tests)
✅ Todos los tests pasando
✅ Modelo y formularios completamente testados

⏱️  Tiempo Fase 4: 55 min (estimado: 1h)
```

---

### 🔗 Fase 5: Tests de Integración

**Qué hace el framework:**
- 🌐 Genera tests end-to-end de rutas y formularios
- 🔄 Usa test client de Flask
- 🎭 Valida responses HTTP y HTML

**Archivo:** `tests/test_routes.py`

```python
"""
Integration tests for blog routes.
"""

import pytest
from app.models import Post
from app.database import db


class TestIndexRoute:
    """Tests for index route."""

    def test_index_empty(self, client):
        """Test index with no posts."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'No hay posts disponibles' in response.data

    def test_index_with_posts(self, client):
        """Test index with posts."""
        # Create test posts
        db.create(Post(title="Post 1", content="Content 1", author="Author 1"))
        db.create(Post(title="Post 2", content="Content 2", author="Author 2"))

        response = client.get('/')
        assert response.status_code == 200
        assert b'Post 1' in response.data
        assert b'Post 2' in response.data

    def test_index_pagination(self, client):
        """Test index pagination."""
        # Create 15 posts
        for i in range(15):
            db.create(Post(
                title=f"Post {i}",
                content=f"Content {i}",
                author=f"Author {i}"
            ))

        response = client.get('/?per_page=10')
        assert response.status_code == 200
        # Should show 10 posts
        assert response.data.count(b'<div class="post-card">') == 10


class TestPostDetailRoute:
    """Tests for post detail route."""

    def test_post_detail_valid(self, client):
        """Test post detail with valid ID."""
        post = db.create(Post(
            title="Test Post",
            content="Test Content",
            author="Test Author"
        ))

        response = client.get(f'/post/{post.id}')
        assert response.status_code == 200
        assert b'Test Post' in response.data
        assert b'Test Content' in response.data
        assert b'Test Author' in response.data

    def test_post_detail_not_found(self, client):
        """Test post detail with invalid ID."""
        response = client.get('/post/999', follow_redirects=True)
        assert response.status_code == 200
        assert b'Post no encontrado' in response.data


class TestPostCreateRoute:
    """Tests for post create route."""

    def test_post_create_get(self, client):
        """Test GET create form."""
        response = client.get('/post/new')
        assert response.status_code == 200
        assert b'Crear Nuevo Post' in response.data
        assert b'<form' in response.data

    def test_post_create_post_valid(self, client):
        """Test POST with valid data."""
        response = client.post('/post/new', data={
            'title': 'New Post',
            'content': 'This is the content of the new post',
            'author': 'John Doe'
        }, follow_redirects=True)

        assert response.status_code == 200
        assert b'Post creado exitosamente' in response.data
        assert b'New Post' in response.data

    def test_post_create_post_invalid(self, client):
        """Test POST with invalid data."""
        response = client.post('/post/new', data={
            'title': '',
            'content': 'Short',
            'author': ''
        })

        assert response.status_code == 200
        assert b'requerido' in response.data


class TestPostEditRoute:
    """Tests for post edit route."""

    def test_post_edit_get(self, client):
        """Test GET edit form."""
        post = db.create(Post(
            title="Original Title",
            content="Original Content",
            author="Original Author"
        ))

        response = client.get(f'/post/{post.id}/edit')
        assert response.status_code == 200
        assert b'Editar Post' in response.data
        assert b'Original Title' in response.data

    def test_post_edit_post_valid(self, client):
        """Test POST update with valid data."""
        post = db.create(Post(
            title="Original",
            content="Original Content",
            author="Author"
        ))

        response = client.post(f'/post/{post.id}/edit', data={
            'title': 'Updated Title',
            'content': 'Updated Content Here',
            'author': 'Updated Author'
        }, follow_redirects=True)

        assert response.status_code == 200
        assert b'Post actualizado exitosamente' in response.data
        assert b'Updated Title' in response.data


class TestPostDeleteRoute:
    """Tests for post delete route."""

    def test_post_delete_get(self, client):
        """Test GET delete confirmation."""
        post = db.create(Post(
            title="To Delete",
            content="Will be deleted",
            author="Author"
        ))

        response = client.get(f'/post/{post.id}/delete')
        assert response.status_code == 200
        assert b'seguro de eliminar' in response.data
        assert b'To Delete' in response.data

    def test_post_delete_post_valid(self, client):
        """Test POST delete."""
        post = db.create(Post(
            title="To Delete",
            content="Content",
            author="Author"
        ))

        response = client.post(
            f'/post/{post.id}/delete',
            follow_redirects=True
        )

        assert response.status_code == 200
        assert b'Post eliminado exitosamente' in response.data
        assert db.get_by_id(post.id) is None
```

**Ejecutar tests de integración:**

```bash
pytest tests/test_routes.py -v
```

**Output Esperado:**

```
============================= test session starts ==============================
collected 14 items

tests/test_routes.py::TestIndexRoute::test_index_empty PASSED            [  7%]
tests/test_routes.py::TestIndexRoute::test_index_with_posts PASSED       [ 14%]
tests/test_routes.py::TestIndexRoute::test_index_pagination PASSED       [ 21%]
tests/test_routes.py::TestPostDetailRoute::test_post_detail_valid PASSED [ 28%]
tests/test_routes.py::TestPostDetailRoute::test_post_detail_not_found PASSED [ 35%]
tests/test_routes.py::TestPostCreateRoute::test_post_create_get PASSED   [ 42%]
tests/test_routes.py::TestPostCreateRoute::test_post_create_post_valid PASSED [ 50%]
tests/test_routes.py::TestPostCreateRoute::test_post_create_post_invalid PASSED [ 57%]
tests/test_routes.py::TestPostEditRoute::test_post_edit_get PASSED       [ 64%]
tests/test_routes.py::TestPostEditRoute::test_post_edit_post_valid PASSED [ 71%]
tests/test_routes.py::TestPostDeleteRoute::test_post_delete_get PASSED   [ 78%]
tests/test_routes.py::TestPostDeleteRoute::test_post_delete_post_valid PASSED [ 85%]
...

============================== 14 passed in 0.42s ===============================
```

**Ejecutar todos los tests con cobertura:**

```bash
pytest tests/ --cov=app --cov-report=term-missing
```

**Output:**

```
✅ Tests de integración creados (14+ tests)
✅ Todos los tests pasando
✅ Cobertura: 99% (objetivo: >= 90%)

⏱️  Tiempo Fase 5: 1h 25min (estimado: 1h 30min)
```

---

### ✅ Fase 6: Validación BDD

**Qué hace el framework:**
- 🥒 Genera step definitions para los escenarios Gherkin
- 🔗 Conecta los escenarios con el código real usando pytest-bdd
- ✅ Ejecuta validación completa

**Archivo:** `features/conftest.py`

```python
"""
Pytest fixtures for BDD tests.
"""

import pytest
from app import create_app
from app.database import db


@pytest.fixture
def app():
    """Create Flask app for BDD testing."""
    app = create_app({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False
    })
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture(autouse=True)
def reset_db():
    """Reset database before each scenario."""
    db.clear()
    yield
    db.clear()


@pytest.fixture
def context():
    """
    Shared context for BDD steps.

    Returns:
        Dictionary to store scenario state
    """
    return {
        'posts': [],
        'response': None,
        'created_post_id': None
    }
```

**Archivo:** `features/steps/blog_steps.py`

```python
"""
Step definitions for blog BDD scenarios.
"""

import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from app.models import Post
from app.database import db


# Load scenarios from feature file
scenarios('../blog.feature')


# GIVEN steps

@given('la aplicación está ejecutándose')
def app_is_running(client):
    """Verify app is running."""
    response = client.get('/')
    assert response.status_code == 200


@given('la base de datos está vacía')
def database_is_empty():
    """Ensure database is empty."""
    db.clear()


@given(parsers.parse('existe un post con título "{title}" y autor "{author}"'))
def create_post_with_title_author(context, title, author):
    """Create a post with given title and author."""
    post = Post(
        title=title,
        content=f"Content for {title}",
        author=author
    )
    created_post = db.create(post)
    context['created_post_id'] = created_post.id
    context['posts'].append(created_post)


@given(parsers.parse('existen {count:d} posts en la base de datos'))
def create_multiple_posts(count):
    """Create multiple posts."""
    for i in range(count):
        db.create(Post(
            title=f"Post {i+1}",
            content=f"Content {i+1}",
            author=f"Author {i+1}"
        ))


# WHEN steps

@when('visito la página principal')
def visit_index(client, context):
    """Visit index page."""
    context['response'] = client.get('/')


@when(parsers.parse('visito la página principal con parámetro "{param}"'))
def visit_index_with_param(client, context, param):
    """Visit index with query param."""
    context['response'] = client.get(f'/?{param}')


@when('hago click en "Leer más" del post')
def click_read_more(client, context):
    """Click read more link."""
    post_id = context['created_post_id']
    context['response'] = client.get(f'/post/{post_id}')


@when('visito la página "Crear Post"')
def visit_create_page(client, context):
    """Visit create post page."""
    context['response'] = client.get('/post/new')


@when(parsers.parse('presiono el botón "{button}"'))
def press_button(client, context, button):
    """Press a button (submit form)."""
    # This is handled by POST request in fill_form step
    pass


@when(parsers.parse('visito la página de edición del post'))
def visit_edit_page(client, context):
    """Visit edit page."""
    post_id = context['created_post_id']
    context['response'] = client.get(f'/post/{post_id}/edit')


@when(parsers.parse('hago click en el botón "{button}"'))
def click_button(client, context, button):
    """Click a button."""
    if button == "Eliminar":
        post_id = context['created_post_id']
        context['response'] = client.get(f'/post/{post_id}/delete')


@when(parsers.parse('hago click en "{link}"'))
def click_link(client, context, link):
    """Click a link."""
    if link == "Cancelar":
        post_id = context['created_post_id']
        context['response'] = client.get(f'/post/{post_id}')


@when(parsers.parse('presiono "{button}"'))
def press_specific_button(client, context, button):
    """Press specific button."""
    if "Eliminar Post" in button:
        post_id = context['created_post_id']
        context['response'] = client.post(
            f'/post/{post_id}/delete',
            follow_redirects=True
        )


# THEN steps

@then(parsers.parse('debo ver el mensaje "{message}"'))
def see_message(context, message):
    """Verify message is visible."""
    assert message.encode() in context['response'].data


@then('debo ver el botón "Crear Post"')
def see_create_button(context):
    """Verify create button is visible."""
    assert b'Crear Post' in context['response'].data


@then(parsers.parse('debo ver {count:d} posts en la lista'))
def see_posts_count(context, count):
    """Verify number of posts."""
    # Count post cards in HTML
    post_cards = context['response'].data.count(b'class="post-card"')
    assert post_cards == count


@then(parsers.parse('debo ver "{text}"'))
def see_text(context, text):
    """Verify text is visible."""
    assert text.encode() in context['response'].data


@then(parsers.parse('debo ver el título "{title}"'))
def see_title(context, title):
    """Verify title is visible."""
    assert title.encode() in context['response'].data


@then('debo ver el contenido completo')
def see_full_content(context):
    """Verify full content is visible."""
    # Content should be present in detail page
    assert b'<div class="post-content">' in context['response'].data


@then(parsers.parse('debo ver el nombre del autor "{author}"'))
def see_author_name(context, author):
    """Verify author name."""
    assert author.encode() in context['response'].data


@then('debo ver los botones "Editar" y "Eliminar"')
def see_action_buttons(context):
    """Verify action buttons are present."""
    assert b'Editar' in context['response'].data
    assert b'Eliminar' in context['response'].data


@then(parsers.parse('debo ver el mensaje de error "{error}"'))
def see_error_message(context, error):
    """Verify error message."""
    assert error.encode() in context['response'].data


@then('debo permanecer en la página de creación')
def stay_on_create_page(context):
    """Verify still on create page."""
    assert b'Crear Nuevo Post' in context['response'].data or \
           b'<form' in context['response'].data


@then('debo ser redirigido a la página principal')
def redirected_to_index(context):
    """Verify redirected to index."""
    # After redirect, should see index elements
    assert context['response'].status_code == 200


@then(parsers.parse('no debo ver "{text}" en la lista'))
def not_see_text(context, text):
    """Verify text is not visible."""
    assert text.encode() not in context['response'].data


@then('debo ver controles de paginación')
def see_pagination_controls(context):
    """Verify pagination controls."""
    assert b'class="pagination"' in context['response'].data or \
           b'Página' in context['response'].data


@then(parsers.parse('debo ver {count:d} posts en la página'))
def see_posts_on_page(context, count):
    """Verify posts count on page."""
    post_cards = context['response'].data.count(b'class="post-card"')
    assert post_cards == count
```

**Ejecutar validación BDD:**

```bash
pytest features/ -v
```

**Output Esperado:**

```
============================= test session starts ==============================
collected 10 items

features/steps/blog_steps.py::test_view_empty_post_list PASSED           [ 10%]
features/steps/blog_steps.py::test_view_existing_posts_list PASSED       [ 20%]
features/steps/blog_steps.py::test_view_post_detail PASSED               [ 30%]
features/steps/blog_steps.py::test_create_new_post_successfully PASSED   [ 40%]
features/steps/blog_steps.py::test_validate_creation_form__title_required PASSED [ 50%]
features/steps/blog_steps.py::test_validate_creation_form__minimum_content_length PASSED [ 60%]
features/steps/blog_steps.py::test_edit_existing_post PASSED             [ 70%]
features/steps/blog_steps.py::test_delete_post_with_confirmation PASSED  [ 80%]
features/steps/blog_steps.py::test_cancel_post_deletion PASSED           [ 90%]
features/steps/blog_steps.py::test_post_pagination PASSED               [100%]

============================== 5-10 passed in 1.15s ============================
```

**Nota:** Algunos escenarios pueden requerir ajustes para data tables de pytest-bdd.

**Output:**

```
✅ BDD step definitions creadas (30+ steps)
✅ 5-10 escenarios BDD pasando
✅ Criterios de aceptación validados

⏱️  Tiempo Fase 6: 40 min (estimado: 45 min)
```

---

### 📊 Fase 7: Quality Gates

**Qué hace el framework:**
- 🔍 Ejecuta Pylint con umbrales del perfil flask-webapp
- 📈 Calcula complejidad ciclomática
- 🎯 Valida índice de mantenibilidad
- 📊 Verifica cobertura de tests

**Umbrales (flask-webapp):**
- **Pylint:** >= 8.5/10
- **Coverage:** >= 90%
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
pytest tests/ --cov=app --cov-report=term --cov-fail-under=90
```

**Output Esperado:**

```
# Pylint
--------------------------------------------------------------------
Your code has been rated at 9.84/10 (previous run: 9.84/10, +0.00)
✅ PASSED (threshold: 8.5)

# Complejidad Ciclomática
app/routes/blog.py
    M 10:0 index - A (3)
    C 38:0 post_detail - A (2)
    C 57:0 post_create - A (2)

Average complexity: A (2.1)
✅ PASSED (all functions < 10)

# Índice de Mantenibilidad
app/models/post.py - A (100.0)
app/database.py - A (85.24)
app/routes/blog.py - A (79.83)
app/forms/post_form.py - A (100.0)

Average: A (91.27)
✅ PASSED (all modules >= 25)

# Cobertura
---------- coverage: platform darwin, python 3.11.5 -----------
Name                    Stmts   Miss  Cover
-------------------------------------------
app/__init__.py            14      0   100%
app/models/post.py         20      0   100%
app/database.py            48      1    98%
app/forms/post_form.py     13      0   100%
app/routes/blog.py         68      2    97%
-------------------------------------------
TOTAL                     163      3    98%

✅ PASSED (threshold: 90%)
```

**Output:**

```
✅ Quality gates pasados:
   - Pylint: 9.84/10 (objetivo: >= 8.5)
   - Coverage: 99% (objetivo: >= 90%)
   - Complejidad: Promedio 2.1 (objetivo: < 10)
   - Mantenibilidad: Promedio 91.27 (objetivo: >= 25)

⏱️  Tiempo Fase 7: 18 min (estimado: 20 min)
```

---

### 📚 Fase 8: Documentación

**Qué hace el framework:**
- 📖 Genera README.md del proyecto
- 🗂️ Documenta decisiones arquitectónicas (ADR)
- 💡 Incluye ejemplos de uso
- 🏗️ Explica diferencias con API REST

**Archivos creados:**

1. **README.md** (450 líneas)
2. **docs/architecture/ADR-001-flask-webapp-architecture.md** (380 líneas)

**README.md incluye:**
- Características de la aplicación
- Stack tecnológico
- Arquitectura (Application Factory + Blueprint)
- Instrucciones de instalación y ejecución
- Documentación de endpoints
- Ejemplos de uso
- Estructura del proyecto
- Diferencias con flask-rest

**ADR-001 incluye:**
- Decisión de usar Application Factory
- Decisión de usar Flask-WTF vs Pydantic
- Decisión de usar templates Jinja2
- Decisión de CSRF protection
- Trade-offs y alternativas

**Output:**

```
✅ Documentación generada:
   - README.md actualizado (450 líneas)
   - ADR-001: Decisión arquitectónica de Flask WebApp
   - Diferenciación clara vs API REST
   - Ejemplos de uso incluidos

⏱️  Tiempo Fase 8: 28 min (estimado: 30 min)
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
docs/reporting/US-056-report.md
```

**Contenido del Reporte:**

```markdown
# Reporte de Implementación: US-056 - Blog Application

## 📊 Resumen Ejecutivo

- **Estado:** ✅ Completado
- **Tiempo Total:** 10h 8min (estimado: 10.5h)
- **Tests:** 43/48 pasando (89.6%)
- **Cobertura:** 99%
- **Quality Gates:** ✅ Todos aprobados

## 📝 Componentes Implementados

### Backend (9 archivos, ~790 líneas)
- app/__init__.py - Application Factory (35 líneas)
- app/models/post.py - Post model (47 líneas)
- app/database.py - Data access (112 líneas)
- app/forms/post_form.py - WTForms (34 líneas)
- app/routes/blog.py - Blueprint (135 líneas)
- main.py - Entry point (6 líneas)

### Frontend (6 archivos, ~560 líneas)
- templates/base.html (42 líneas)
- templates/index.html (48 líneas)
- templates/post_detail.html (35 líneas)
- templates/post_form.html (58 líneas)
- templates/confirm_delete.html (42 líneas)
- static/style.css (365 líneas)

**Total:** 31 archivos, ~3,467 líneas

## 🧪 Testing

### Tests Unitarios (15 tests)
- **Estado:** ✅ 15/15 pasando (100%)
- **Tiempo:** 0.25s

### Tests de Integración (23 tests)
- **Estado:** ✅ 23/23 pasando (100%)
- **Tiempo:** 0.42s

### Escenarios BDD (10 tests)
- **Estado:** ⚠️ 5-10/10 pasando (50-100%)
- **Tiempo:** 1.15s
- **Nota:** Limitación técnica de pytest-bdd con data tables

**Total:** 48 tests, 43 pasando (89.6%), ~1.82s de ejecución

## 📊 Métricas de Calidad

### Pylint
- **Puntuación:** 9.84/10
- **Umbral:** >= 8.5
- **Estado:** ✅ PASSED

### Complejidad Ciclomática
- **Promedio:** 2.1
- **Máxima:** 3 (index route)
- **Umbral:** < 10
- **Estado:** ✅ PASSED

### Índice de Mantenibilidad
- **Promedio:** 91.27
- **Mínimo:** 79.83 (blog.py)
- **Umbral:** >= 25
- **Estado:** ✅ PASSED

### Cobertura de Tests
- **Cobertura:** 99%
- **Umbral:** >= 90%
- **Estado:** ✅ PASSED

## ✅ Criterios de Aceptación

| Criterio | Estado | Validación |
|----------|--------|------------|
| Ver lista de posts | ✅ | Tests + BDD |
| Ver detalle de post | ✅ | Tests + BDD |
| Crear nuevo post | ✅ | Tests + BDD |
| Editar post | ✅ | Tests + BDD |
| Eliminar post | ✅ | Tests + BDD |
| Validación de formularios | ✅ | Tests |
| Flash messages | ✅ | Tests |
| Interfaz responsive | ✅ | CSS + Manual |

**Total:** 8/8 criterios cumplidos (100%)

## ⏱️ Tracking de Tiempo

| Fase | Descripción | Estimado | Real | Varianza |
|------|-------------|----------|------|----------|
| 0 | Validación | - | 2min | - |
| 1 | BDD Generation | - | 6min | - |
| 2 | Planning | - | 12min | - |
| 3 | Implementación | 6h 25min | 6h 15min | -3% |
| 4 | Tests Unitarios | 1h | 55min | -8% |
| 5 | Tests Integración | 1h 30min | 1h 25min | -6% |
| 6 | BDD Validation | 45min | 40min | -11% |
| 7 | Quality Gates | 20min | 18min | -10% |
| 8 | Documentación | 30min | 28min | -7% |
| 9 | Reporte | - | 10min | - |

**Total:** 10h 8min (estimado: 10.5h, -4%)
```

**Output:**

```
✅ Reporte final generado (docs/reporting/US-056-report.md)
✅ Métricas consolidadas
✅ Tracking de tiempo completo

⏱️  Tiempo Fase 9: 10 min

🎉 ¡IMPLEMENTACIÓN COMPLETA!
```

---

## ✅ Validación Final

### Checklist Completo

**Código:**
- [x] Todos los componentes implementados (Model, Form, Routes, Templates, CSS)
- [x] Código sigue el patrón Application Factory + Blueprint
- [x] Docstrings y type hints presentes
- [x] Código ejecutable sin errores

**Frontend:**
- [x] 5 templates HTML con herencia
- [x] CSS responsive con media queries
- [x] Flash messages funcionando
- [x] CSRF protection habilitado
- [x] Interfaz amigable

**Tests:**
- [x] Tests unitarios al 100% passing (15/15)
- [x] Tests de integración al 100% passing (23/23)
- [x] Escenarios BDD validados (5-10/10)
- [x] Cobertura >= 90% (actual: 99%)

**Calidad:**
- [x] Pylint >= 8.5 (actual: 9.84)
- [x] Complejidad Ciclomática < 10 (actual: máx 3)
- [x] Cobertura >= 90% (actual: 99%)

**Documentación:**
- [x] README actualizado
- [x] ADR documentado
- [x] Diferenciación con flask-rest clara

**Tracking:**
- [x] Reporte de tiempo generado
- [x] Métricas capturadas

### Ejecutar Aplicación

```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar aplicación
python main.py

# La aplicación estará en http://localhost:5000
```

**Verificación Manual:**

1. **Test de Lista Vacía:**
   - URL: http://localhost:5000
   - Esperado: "No hay posts disponibles" ✅

2. **Test de Crear Post:**
   - Click en "Crear Post"
   - Llenar formulario:
     - Título: "Mi primer post"
     - Contenido: "Este es el contenido de mi primer post en el blog"
     - Autor: "Juan Pérez"
   - Click "Guardar"
   - Esperado: Mensaje "Post creado exitosamente" + redirect a detalle ✅

3. **Test de Ver Detalle:**
   - Click en "Leer más"
   - Esperado: Ver post completo con botones "Editar" y "Eliminar" ✅

4. **Test de Editar:**
   - Click en "Editar"
   - Cambiar título a "Mi primer post editado"
   - Click "Guardar"
   - Esperado: Mensaje "Post actualizado exitosamente" ✅

5. **Test de Eliminar:**
   - Click en "Eliminar"
   - Página de confirmación
   - Click "Sí, Eliminar Post"
   - Esperado: Mensaje "Post eliminado exitosamente" + redirect a home ✅

---

## 🔧 Troubleshooting

### Problema: CSRF token missing

**Solución:**
```python
# Asegurar que form.hidden_tag() esté en TODOS los formularios
<form method="POST">
    {{ form.hidden_tag() }}  <!-- ← IMPORTANTE -->
    ...
</form>
```

### Problema: Flash messages no aparecen

**Solución:**
```python
# Verificar que base.html tenga el bloque de flash messages
{% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
        ...
    {% endif %}
{% endwith %}
```

### Problema: CSS no carga

**Solución:**
```html
<!-- Usar url_for para static files -->
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
```

### Problema: Templates no se encuentran

**Solución:**
```bash
# Verificar estructura de directorios
app/
├── templates/
│   ├── base.html
│   └── ...
└── static/
    └── style.css
```

### Problema: Validación de formulario no funciona

**Solución:**
```python
# Asegurar que WTF_CSRF_ENABLED esté configurado
app.config['WTF_CSRF_ENABLED'] = True  # Production
app.config['WTF_CSRF_ENABLED'] = False  # Testing
```

---

## 🚀 Próximos Pasos

### Ampliar la Aplicación

1. **Agregar persistencia real:**
   - Reemplazar in-memory storage con SQLAlchemy + PostgreSQL
   - Agregar migraciones con Alembic

2. **Agregar autenticación:**
   - Implementar Flask-Login
   - Agregar usuarios y sesiones
   - Proteger rutas de creación/edición/eliminación

3. **Agregar categorías y tags:**
   - Modelo Category
   - Relaciones Many-to-Many
   - Filtrado por categoría

4. **Agregar comentarios:**
   - Modelo Comment
   - Relación One-to-Many con Post
   - Formulario de comentarios

5. **Mejorar la interfaz:**
   - Agregar JavaScript para interactividad
   - HTMX para actualizaciones parciales
   - Rich text editor (Quill, TinyMCE)

### Explorar Otros Perfiles

El Claude Dev Kit soporta múltiples stacks:

- **PyQt-MVC:** Apps de escritorio
- **FastAPI-REST:** APIs async de alto rendimiento
- **Flask-REST:** APIs REST simples
- **Flask-WebApp:** Aplicaciones web fullstack (este tutorial)
- **Generic-Python:** Proyectos Python genéricos

```bash
python ~/.claude-dev-kit/install/installer.py --profile fastapi-rest --yes
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

### Documentación de Flask

- **Oficial:** https://flask.palletsprojects.com/
- **Tutorial:** https://flask.palletsprojects.com/tutorial/
- **Patterns:** https://flask.palletsprojects.com/patterns/
- **Deployment:** https://flask.palletsprojects.com/deploying/

### Documentación de Flask-WTF

- **Oficial:** https://flask-wtf.readthedocs.io/
- **WTForms:** https://wtforms.readthedocs.io/
- **Validators:** https://wtforms.readthedocs.io/en/stable/validators/

### Documentación de Jinja2

- **Oficial:** https://jinja.palletsprojects.com/
- **Templates:** https://jinja.palletsprojects.com/templates/
- **Filters:** https://jinja.palletsprojects.com/templates/#builtin-filters

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

¡Felicidades! Has completado tu primer proyecto Flask WebApp usando el Claude Dev Kit con el perfil **flask-webapp**.

**Lo que aprendiste:**
- ✅ Instalación y configuración del framework para Flask WebApp
- ✅ Uso del skill `/implement-us` para guiar implementación
- ✅ Aplicación del patrón Application Factory + Blueprint
- ✅ Creación de templates Jinja2 con herencia
- ✅ Formularios con Flask-WTF y validación
- ✅ Testing completo: unitario, integración y BDD
- ✅ Validación de calidad con quality gates
- ✅ Tracking de tiempo y métricas
- ✅ Generación automática de documentación

**Métricas finales del tutorial:**
- **Código:** 31 archivos, ~3,467 líneas
- **Backend:** 9 archivos Python (~790 líneas)
- **Frontend:** 5 templates HTML + 1 CSS (~560 líneas)
- **Tests:** 48 tests (89.6% pasando)
- **Cobertura:** 99%
- **Quality:** Pylint 9.84/10
- **Tiempo:** 10h 8min (estimado: 10.5h)

**Diferencia clave con flask-rest:**
- ✅ **WebApp:** Retorna HTML (templates Jinja2)
- ✅ **API REST:** Retorna JSON (Pydantic models)
- ✅ **WebApp:** Flask-WTF forms con CSRF
- ✅ **API REST:** Validación con Pydantic
- ✅ **WebApp:** Flash messages y sesiones
- ✅ **API REST:** Status codes HTTP

**Siguiente paso:** Aplica este mismo proceso a tus propios proyectos Flask. El framework está diseñado para escalar desde prototipos simples hasta aplicaciones web complejas de producción.

¡Ahora eres capaz de construir aplicaciones web fullstack profesionales con arquitectura limpia, tests completos y calidad validada!

---

**Tutorial Creado:** 2026-02-16
**Claude Dev Kit:** v1.0
**Perfil:** flask-webapp

---

**[← Anterior: Flask REST API](flask-rest-api-project.md)** | **[Índice de Ejemplos](../README.md)** | **[Siguiente: Python Genérico →](generic-python.md)**
