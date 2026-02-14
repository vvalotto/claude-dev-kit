# Fase 3: Implementación Guiada por Tareas

**Objetivo:** Implementar cada componente del plan de forma incremental, con revisión y aprobación del usuario en cada paso.

**Duración estimada:** Variable según plan (típicamente 45-90 minutos)

---

## Tracking

**Al inicio de la fase:**
```python
tracker.start_phase(3, "Implementación Guiada por Tareas")
```

---

## Acción

Por cada tarea del plan de implementación, guiar al usuario a través de:
1. Contexto de lo que se va a implementar
2. Código propuesto basado en patrones del proyecto
3. Aprobación antes de escribir
4. Ejecución de tests básicos (si aplica)

---

## Pasos del Flujo de Implementación

### 1. Seleccionar próxima tarea

Identificar la primera tarea no completada del plan generado en Fase 2.

---

### 2. TRACKING: Iniciar tarea

```python
tracker.start_task(
    task_id=f"task_{task_number:03d}",
    task_name="{TASK_NAME}",  # Ej: "Implementar UserModel"
    task_type="{TASK_TYPE}",  # modelo, vista, controlador, servicio, etc.
    estimated_minutes={ESTIMATED_TIME}  # Del plan
)
```

**Tipos de tarea según arquitectura:**

- **MVC (PyQt, Desktop):** `modelo`, `vista`, `controlador`, `factory`, `coordinator`
- **Layered - FastAPI (async):** `model`, `schema`, `service`, `repository`, `endpoint`
- **Layered - Flask (sync):** `api`, `domain`, `repository`, `mapper`, `error_handler`
- **Generic:** `class`, `function`, `module`, `config`

---

### 3. Mostrar contexto de la tarea

Presentar al usuario:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 TAREA {N}/{TOTAL}: {TASK_NAME}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 Ubicación: {COMPONENT_PATH}/{filename}.{ext}

📐 Patrón: {COMPONENT_TYPE} ({ARCHITECTURE_PATTERN})

💡 Referencia: [Ver sección de ejemplos abajo según stack]

✏️  Código propuesto:
───────────────────────────────────────────
[Código generado aquí]
───────────────────────────────────────────

❓ ¿Aprobar e implementar? (yes/no/edit)
```

---

### 4. Generar código base usando patrones del proyecto

Leer la configuración del perfil (`.claude/skills/implement-us/config.json`) para determinar:
- **Base classes** a extender
- **Imports** necesarios según stack
- **Estructura de archivos** esperada
- **Convenciones de naming**

#### Ejemplo: Generar código según stack

**PyQt/MVC - Modelo (dataclass inmutable):**
```python
# {COMPONENT_PATH}/modelo.py
from dataclasses import dataclass, field
from typing import Optional
from {BASE_PATH}.core.modelo_base import ModeloBase

@dataclass(frozen=True)
class {COMPONENT_NAME}Modelo(ModeloBase):
    """Modelo inmutable para {COMPONENT_NAME}.

    Attributes:
        campo1: Descripción del campo
        campo2: Descripción del campo
    """
    campo1: str = ""
    campo2: Optional[int] = None

    def __post_init__(self):
        """Validación de datos."""
        super().__post_init__()
        # Validaciones aquí
```

**FastAPI/Layered - Schema (Pydantic model):**
```python
# {COMPONENT_PATH}/schemas.py
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class {COMPONENT_NAME}Base(BaseModel):
    """Schema base para {COMPONENT_NAME}."""
    campo1: str = Field(..., description="Descripción")
    campo2: Optional[int] = Field(None, ge=0)

class {COMPONENT_NAME}Create({COMPONENT_NAME}Base):
    """Schema para creación."""
    pass

class {COMPONENT_NAME}Response({COMPONENT_NAME}Base):
    """Schema para respuesta."""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
```

**Flask/Layered - API Layer (Blueprint con endpoints):**
```python
# app/servicios/{feature}/api.py
from flask import Blueprint, request, jsonify
from app.general.{feature} import {COMPONENT_NAME}Service
from app.servicios.errors import NotFoundError, ValidationError

bp = Blueprint('{feature}', __name__, url_prefix='/api/{feature}')

@bp.route('/', methods=['GET'])
def get_all():
    """Obtener todos los {COMPONENT_NAME}s.

    Returns:
        JSON list de {COMPONENT_NAME}s
    """
    service = {COMPONENT_NAME}Service()
    items = service.get_all()
    return jsonify([item.to_dict() for item in items]), 200

@bp.route('/<int:item_id>', methods=['GET'])
def get_by_id(item_id):
    """Obtener {COMPONENT_NAME} por ID.

    Args:
        item_id: ID del item

    Returns:
        JSON del {COMPONENT_NAME}

    Raises:
        NotFoundError: Si no se encuentra el item
    """
    service = {COMPONENT_NAME}Service()
    item = service.get_by_id(item_id)
    if not item:
        raise NotFoundError(f"{COMPONENT_NAME} {item_id} not found")
    return jsonify(item.to_dict()), 200

@bp.route('/', methods=['POST'])
def create():
    """Crear nuevo {COMPONENT_NAME}.

    Request Body:
        JSON con datos del {COMPONENT_NAME}

    Returns:
        JSON del {COMPONENT_NAME} creado
    """
    data = request.get_json()
    if not data:
        raise ValidationError("Request body is required")

    service = {COMPONENT_NAME}Service()
    item = service.create(data)
    return jsonify(item.to_dict()), 201
```

**Flask/Layered - Domain Layer (Modelo de negocio):**
```python
# app/general/{feature}/{feature}.py
from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class {COMPONENT_NAME}:
    """Modelo de dominio para {COMPONENT_NAME}.

    Attributes:
        id: Identificador único
        campo1: Descripción del campo
        campo2: Descripción del campo
    """
    id: int
    campo1: str
    campo2: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convertir a diccionario para serialización JSON.

        Returns:
            Dict con datos del modelo
        """
        return {
            'id': self.id,
            'campo1': self.campo1,
            'campo2': self.campo2
        }

    def validar(self) -> bool:
        """Validar reglas de negocio.

        Returns:
            True si es válido

        Raises:
            ValueError: Si hay errores de validación
        """
        if not self.campo1:
            raise ValueError("campo1 es requerido")
        if self.campo2 is not None and self.campo2 < 0:
            raise ValueError("campo2 debe ser >= 0")
        return True
```

**Flask/Layered - Data Layer (Repository ABC + implementación):**
```python
# app/datos/{feature}/repositorio.py
from abc import ABC, abstractmethod
from typing import List, Optional
from app.general.{feature} import {COMPONENT_NAME}

class {COMPONENT_NAME}Repository(ABC):
    """Interface abstracta para repositorio de {COMPONENT_NAME}."""

    @abstractmethod
    def get_all(self) -> List[{COMPONENT_NAME}]:
        """Obtener todos los {COMPONENT_NAME}s."""
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[{COMPONENT_NAME}]:
        """Obtener {COMPONENT_NAME} por ID."""
        pass

    @abstractmethod
    def create(self, item: {COMPONENT_NAME}) -> {COMPONENT_NAME}:
        """Crear nuevo {COMPONENT_NAME}."""
        pass


# app/datos/{feature}/memoria.py
class {COMPONENT_NAME}RepositoryMemory({COMPONENT_NAME}Repository):
    """Implementación in-memory del repositorio."""

    def __init__(self):
        self._items: List[{COMPONENT_NAME}] = []
        self._next_id: int = 1

    def get_all(self) -> List[{COMPONENT_NAME}]:
        """Obtener todos los items."""
        return self._items.copy()

    def get_by_id(self, id: int) -> Optional[{COMPONENT_NAME}]:
        """Obtener item por ID."""
        return next((item for item in self._items if item.id == id), None)

    def create(self, item: {COMPONENT_NAME}) -> {COMPONENT_NAME}:
        """Crear nuevo item."""
        item.id = self._next_id
        self._next_id += 1
        self._items.append(item)
        return item
```

**Flask Webapp - Routes (View Functions + BFF):**
```python
# webapp/routes.py
from flask import Blueprint, render_template, request, redirect, url_for
from webapp.api_client import APIClient
from webapp.forms import {COMPONENT_NAME}Form

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Home page."""
    return render_template('index.html', title='Home')

@main_bp.route('/{feature}')
def {feature}_list():
    """Lista de {COMPONENT_NAME}s desde API backend (BFF pattern).

    Returns:
        HTML: Template renderizado con lista de items
    """
    api = APIClient()
    try:
        items = api.get_{feature}()  # Call to backend API
        return render_template('{feature}/list.html',
                             items=items,
                             title='{COMPONENT_NAME}s')
    except Exception as e:
        return render_template('errors/500.html', error=str(e)), 500

@main_bp.route('/{feature}/<int:id>')
def {feature}_detail(id):
    """Detalle de {COMPONENT_NAME} por ID.

    Args:
        id: ID del item a mostrar

    Returns:
        HTML: Template renderizado con detalle del item
        404: Si item no existe
    """
    api = APIClient()
    item = api.get_{feature}(id)
    if not item:
        return render_template('errors/404.html'), 404
    return render_template('{feature}/detail.html',
                         item=item,
                         title=f'{COMPONENT_NAME} {id}')

@main_bp.route('/{feature}/new', methods=['GET', 'POST'])
def {feature}_new():
    """Crear nuevo {COMPONENT_NAME} con form.

    GET: Muestra formulario vacío
    POST: Procesa formulario y crea item

    Returns:
        HTML: Form o redirect después de crear
    """
    form = {COMPONENT_NAME}Form()
    if form.validate_on_submit():
        api = APIClient()
        data = {
            'campo1': form.campo1.data,
            'campo2': form.campo2.data
        }
        item = api.create_{feature}(data)
        return redirect(url_for('main.{feature}_detail', id=item['id']))

    return render_template('{feature}/new.html', form=form, title='New {COMPONENT_NAME}')

@main_bp.errorhandler(404)
def not_found(error):
    """Custom 404 error page."""
    return render_template('errors/404.html'), 404

@main_bp.errorhandler(500)
def internal_error(error):
    """Custom 500 error page."""
    return render_template('errors/500.html'), 500
```

**Flask Webapp - Template (Jinja2 SSR):**
```html
<!-- webapp/templates/{feature}/list.html -->
{% extends "base.html" %}

{% block title %}{{ title }}{% endblock %}

{% block content %}
<div class="container">
    <div class="row mb-4">
        <div class="col-md-8">
            <h1>{{ title }}</h1>
        </div>
        <div class="col-md-4 text-end">
            <a href="{{ url_for('main.{feature}_new') }}" class="btn btn-primary">
                New {COMPONENT_NAME}
            </a>
        </div>
    </div>

    {% if items %}
    <div class="row">
        {% for item in items %}
        <div class="col-md-4 mb-3">
            {% include 'components/{feature}_card.html' %}
        </div>
        {% endfor %}
    </div>

    <!-- Paginación (opcional) -->
    {% if pagination %}
    <nav aria-label="Page navigation">
        <ul class="pagination">
            {% if pagination.has_prev %}
            <li class="page-item">
                <a class="page-link" href="{{ url_for('main.{feature}_list', page=pagination.prev_num) }}">
                    Previous
                </a>
            </li>
            {% endif %}
            {% for page_num in pagination.iter_pages() %}
                {% if page_num %}
                <li class="page-item {% if page_num == pagination.page %}active{% endif %}">
                    <a class="page-link" href="{{ url_for('main.{feature}_list', page=page_num) }}">
                        {{ page_num }}
                    </a>
                </li>
                {% endif %}
            {% endfor %}
            {% if pagination.has_next %}
            <li class="page-item">
                <a class="page-link" href="{{ url_for('main.{feature}_list', page=pagination.next_num) }}">
                    Next
                </a>
            </li>
            {% endif %}
        </ul>
    </nav>
    {% endif %}

    {% else %}
    <div class="alert alert-info">
        <p>No {COMPONENT_NAME}s available.</p>
        <a href="{{ url_for('main.{feature}_new') }}" class="btn btn-primary btn-sm">
            Create first {COMPONENT_NAME}
        </a>
    </div>
    {% endif %}
</div>
{% endblock %}

{% block scripts %}
<script src="{{ url_for('static', filename='js/{feature}.js') }}"></script>
{% endblock %}
```

**Flask Webapp - JavaScript Module (Vanilla JS):**
```javascript
// webapp/static/js/{feature}.js
import { fetchJSON, handleError } from './api.js';
import { showToast, confirmDialog } from './ui.js';

/**
 * {COMPONENT_NAME} Manager - Gestiona interacciones del feature
 */
class {COMPONENT_NAME}Manager {
    constructor() {
        this.apiBaseUrl = '/api/{feature}';
        this.init();
    }

    /**
     * Inicializa event listeners
     */
    init() {
        this.setupEventListeners();
    }

    /**
     * Setup event listeners para botones y forms
     */
    setupEventListeners() {
        // Update buttons
        document.querySelectorAll('.btn-update-{feature}').forEach(btn => {
            btn.addEventListener('click', (e) => this.handleUpdate(e));
        });

        // Delete buttons
        document.querySelectorAll('.btn-delete-{feature}').forEach(btn => {
            btn.addEventListener('click', (e) => this.handleDelete(e));
        });

        // Inline edit fields
        document.querySelectorAll('.editable-field').forEach(field => {
            field.addEventListener('blur', (e) => this.handleInlineEdit(e));
        });
    }

    /**
     * Handle update de {COMPONENT_NAME}
     * @param {Event} event - Click event
     */
    async handleUpdate(event) {
        const id = event.target.dataset.itemId;
        const newValue = document.getElementById(`field-input-${id}`).value;

        try {
            const updated = await fetchJSON(`${this.apiBaseUrl}/${id}`, {
                method: 'PUT',
                body: JSON.stringify({ campo1: newValue })
            });

            showToast('Item updated successfully', 'success');
            this.updateUIElement(id, updated);
        } catch (error) {
            handleError(error);
        }
    }

    /**
     * Handle delete de {COMPONENT_NAME}
     * @param {Event} event - Click event
     */
    async handleDelete(event) {
        const id = event.target.dataset.itemId;

        const confirmed = await confirmDialog(
            'Are you sure?',
            'This action cannot be undone.'
        );

        if (!confirmed) return;

        try {
            await fetchJSON(`${this.apiBaseUrl}/${id}`, {
                method: 'DELETE'
            });

            showToast('Item deleted successfully', 'success');
            document.getElementById(`item-${id}`).remove();
        } catch (error) {
            handleError(error);
        }
    }

    /**
     * Handle inline edit de campo
     * @param {Event} event - Blur event
     */
    async handleInlineEdit(event) {
        const field = event.target;
        const id = field.dataset.itemId;
        const fieldName = field.dataset.fieldName;
        const newValue = field.textContent.trim();

        try {
            await fetchJSON(`${this.apiBaseUrl}/${id}`, {
                method: 'PATCH',
                body: JSON.stringify({ [fieldName]: newValue })
            });

            field.classList.add('updated');
            setTimeout(() => field.classList.remove('updated'), 1000);
        } catch (error) {
            handleError(error);
            field.textContent = field.dataset.originalValue; // Restore
        }
    }

    /**
     * Update UI element con datos nuevos
     * @param {number} id - Item ID
     * @param {Object} data - Updated data
     */
    updateUIElement(id, data) {
        const element = document.getElementById(`item-${id}`);
        if (!element) return;

        element.querySelector('.item-campo1').textContent = data.campo1;
        element.querySelector('.item-campo2').textContent = data.campo2;
    }
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    new {COMPONENT_NAME}Manager();
});
```

**Generic Python - Class:**
```python
# {COMPONENT_PATH}/{filename}.py
"""
{COMPONENT_NAME} - Descripción del componente.
"""
from typing import Optional, Dict, Any

class {COMPONENT_NAME}:
    """Descripción de la clase.

    Attributes:
        campo1: Descripción
        campo2: Descripción
    """

    def __init__(self, campo1: str, campo2: Optional[int] = None):
        """Inicializar {COMPONENT_NAME}.

        Args:
            campo1: Descripción
            campo2: Descripción
        """
        self.campo1 = campo1
        self.campo2 = campo2

    def metodo_principal(self) -> Dict[str, Any]:
        """Descripción del método principal.

        Returns:
            Dict con resultados
        """
        return {"campo1": self.campo1, "campo2": self.campo2}
```

---

### 5. Presentar código para revisión

Mostrar el código completo generado y esperar respuesta del usuario:
- **yes**: Proceder a escribir el archivo
- **no**: Cancelar y pasar a siguiente tarea
- **edit**: Permitir al usuario modificar el código antes de escribir

---

### 6. Escribir archivo si usuario aprueba

Usar el tool `Write` para crear el archivo en la ubicación especificada.

```python
# Pseudocódigo
if user_approves:
    write_file(path="{COMPONENT_PATH}/{filename}.{ext}", content=generated_code)
    print(f"✅ Archivo creado: {COMPONENT_PATH}/{filename}.{ext}")
```

---

### 7. Ejecutar tests básicos (si aplica)

Después de crear el archivo, ejecutar validaciones rápidas:

**PyQt/MVC:**
```bash
# Verificar imports
python -c "from {COMPONENT_PATH}.modelo import {COMPONENT_NAME}Modelo"

# Ejecutar tests si existen
pytest tests/test_{component}_modelo.py -v --tb=short
```

**FastAPI:**
```bash
# Verificar schemas
python -c "from {COMPONENT_PATH}.schemas import {COMPONENT_NAME}Create"

# Validar con mypy
mypy {COMPONENT_PATH}/schemas.py
```

**Flask:**
```bash
# Verificar imports (API layer)
python -c "from app.servicios.{feature}.api import bp"

# Verificar domain model
python -c "from app.general.{feature} import {COMPONENT_NAME}"

# Verificar repository
python -c "from app.datos.{feature}.repositorio import {COMPONENT_NAME}Repository"

# Ejecutar tests si existen
pytest tests/unit/test_{component}.py -v --tb=short
pytest tests/integration/test_{feature}_api.py -v --tb=short
```

**Generic Python:**
```bash
# Verificar sintaxis
python -m py_compile {COMPONENT_PATH}/{filename}.py

# Ejecutar tests si existen
pytest tests/test_{filename}.py -v --tb=short
```

---

### 8. TRACKING: Finalizar tarea

```python
tracker.end_task(
    task_id=f"task_{task_number:03d}",
    file_created="{COMPONENT_PATH}/{filename}.{ext}"
)
```

---

### 9. Actualizar plan INMEDIATAMENTE

**IMPORTANTE:** Después de completar cada tarea, actualizar el plan de implementación:

1. Marcar checkbox como completado: `- [x] {TASK_NAME}`
2. Actualizar contador: "Tareas completadas: X/Y"
3. Actualizar porcentaje de progreso
4. Agregar nota si hay cambios al plan

**Esto da visibilidad en tiempo real del progreso** y permite retomar fácilmente si la sesión se interrumpe.

Ejemplo de actualización:
```markdown
## Progreso de Implementación

Tareas completadas: 3/12 (25%)

### Componentes Core
- [x] Implementar {COMPONENT_NAME}Modelo (10 min) ✅
- [x] Implementar {COMPONENT_NAME}Vista (15 min) ✅
- [x] Implementar {COMPONENT_NAME}Controlador (20 min) ✅
- [ ] Implementar Factory (15 min)
- [ ] Integrar con Coordinator (15 min)
```

---

### 10. Continuar con siguiente tarea

Repetir los pasos 1-9 para la siguiente tarea no completada hasta finalizar todas las tareas del plan.

---

## Punto de Aprobación

**Usuario debe aprobar cada tarea individualmente antes de proceder.**

Esto permite:
- ✅ Revisión del código propuesto
- ✅ Ajustes antes de escribir archivos
- ✅ Control fino sobre lo que se implementa
- ✅ Aprendizaje incremental de los patrones del proyecto

---

## Manejo de Errores

### Si la implementación falla (imports, sintaxis, etc.):

1. **Diagnosticar el error**
   - Leer mensaje de error completo
   - Identificar causa (import faltante, typo, estructura incorrecta)

2. **Corregir**
   - Ajustar el código
   - Re-presentar al usuario para aprobación

3. **Re-ejecutar tests básicos**

4. **NO avanzar** hasta que la tarea esté funcionando

### Si el usuario rechaza una tarea (responde "no"):

1. **Preguntar razón**
2. **Ajustar approach** según feedback
3. **Re-presentar** o **saltar tarea** según instrucciones

---

## Ejemplos de Referencias por Stack

### PyQt/MVC

**Referencia para Modelos:**
> "Revisar otros modelos existentes en `app/presentacion/paneles/*/modelo.py` para mantener consistencia en:
> - Uso de `@dataclass(frozen=True)` para inmutabilidad
> - Herencia de `ModeloBase`
> - Validaciones en `__post_init__`"

**Referencia para Vistas:**
> "Revisar otras vistas en `app/presentacion/paneles/*/vista.py`:
> - Heredar de `QWidget` o `{BASE_CLASS}`
> - Usar layouts para estructura (QVBoxLayout, QHBoxLayout)
> - Separar construcción de UI en métodos privados"

**Referencia para Controladores:**
> "Revisar controladores existentes:
> - Usar `pyqtSignal` para comunicación
> - Patrón mediador entre modelo y vista
> - Métodos públicos para acciones del usuario"

---

### FastAPI/Layered

**Referencia para Schemas:**
> "Revisar schemas en `app/schemas/*.py`:
> - Usar herencia para DRY (Base, Create, Update, Response)
> - Validaciones con `validator` de Pydantic
> - Config `from_attributes = True` para ORMs"

**Referencia para Services:**
> "Revisar servicios en `app/services/*.py`:
> - Lógica de negocio independiente de framework
> - Inyección de dependencias (repositories)
> - Manejo de excepciones de dominio"

**Referencia para Endpoints:**
> "Revisar routers en `app/api/v1/endpoints/*.py`:
> - Usar dependency injection
> - Status codes apropiados (201, 204, 404)
> - Documentación en docstrings para OpenAPI"

---

### Django/MVT

**Referencia para Models:**
> "Revisar modelos en `app/models/*.py`:
> - Usar validators de Django
> - Definir `Meta` con verbose_name y ordering
> - Implementar `__str__` descriptivo"

**Referencia para Views:**
> "Revisar vistas en `app/views/*.py`:
> - Usar Class-Based Views cuando sea apropiado
> - Generic views para CRUD estándar
> - Decoradores para permisos (@login_required)"

**Referencia para Templates:**
> "Revisar templates en `templates/app/*.html`:
> - Extender de `base.html`
> - Usar template tags y filters
> - Estructurar con bloques reutilizables"

---

### Generic Python

**Referencia para Classes:**
> "Revisar clases existentes en el proyecto:
> - Docstrings en formato Google o NumPy
> - Type hints en métodos públicos
> - Separación de responsabilidades (SRP)"

**Referencia para Functions:**
> "Revisar funciones existentes:
> - Funciones puras cuando sea posible
> - Type hints en signature
> - Documentación de excepciones que puede lanzar"

---

## Tracking al Finalizar

```python
tracker.end_phase(3, auto_approved=True)  # Las tareas ya fueron aprobadas individualmente
```

**Nota:** Se usa `auto_approved=True` porque cada tarea ya fue aprobada por el usuario durante la implementación.

---

## Resumen de la Fase

Al finalizar esta fase:

✅ Todos los componentes del plan están implementados
✅ Cada archivo fue revisado y aprobado por el usuario
✅ Tests básicos de imports/sintaxis ejecutados
✅ Plan actualizado con progreso en tiempo real
✅ Tracking de tiempo por tarea registrado

**Próxima fase:** Fase 4 - Tests Unitarios
