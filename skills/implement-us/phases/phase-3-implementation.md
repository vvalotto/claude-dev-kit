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
