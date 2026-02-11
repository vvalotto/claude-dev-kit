# Fase 4: Tests Unitarios

**Objetivo:** Implementar tests unitarios exhaustivos para cada componente creado, asegurando calidad y cobertura mínima.

**Duración estimada:** 30-45 minutos

---

## Tracking

**Al inicio de la fase:**
```python
tracker.start_phase(4, "Tests Unitarios")
```

---

## Acción

Por cada componente implementado en la Fase 3, crear tests unitarios que validen su comportamiento de forma aislada.

**Template:** `.claude/templates/test-unit.py`

---

## Configuración de Testing por Stack

Antes de escribir tests, verificar la configuración del framework de testing según el perfil:

### PyQt/MVC
```bash
# Dependencias necesarias
pytest>=7.0.0
pytest-qt>=4.2.0
pytest-cov>=4.0.0

# Fixtures disponibles
- qapp: Aplicación Qt (automático con pytest-qt)
- qtbot: Herramientas de testing de Qt (interacción con widgets)
```

### FastAPI/Layered
```bash
# Dependencias necesarias
pytest>=7.0.0
pytest-asyncio>=0.21.0
httpx>=0.24.0
pytest-cov>=4.0.0

# Fixtures disponibles
- client: Cliente HTTP de testing
- test_db: Base de datos de prueba (si usa DB)
- async_client: Cliente asíncrono
```

### Django/MVT
```bash
# Dependencias necesarias
pytest>=7.0.0
pytest-django>=4.5.0
pytest-cov>=4.0.0

# Fixtures disponibles
- db: Acceso a base de datos de prueba
- client: Cliente HTTP de testing
- admin_client: Cliente autenticado como admin
- django_user_model: Modelo de usuario
```

### Generic Python
```bash
# Dependencias necesarias
pytest>=7.0.0
pytest-cov>=4.0.0

# Fixtures disponibles
- tmp_path: Directorio temporal para tests
- monkeypatch: Monkey patching de objetos
- capsys: Captura de stdout/stderr
```

---

## Pasos de Implementación de Tests

### 1. Identificar qué testear según tipo de componente

La estrategia de testing varía según la arquitectura y tipo de componente:

#### PyQt/MVC

**Modelo:**
- Validación de datos y tipos
- Inmutabilidad (frozen dataclass)
- Comportamiento de métodos de negocio
- Casos edge (valores None, strings vacíos, etc.)

**Vista:**
- Construcción correcta de widgets
- Actualización de UI según modelo
- Interacción con señales
- Layout y estructura visual

**Controlador:**
- Emisión de señales
- Lógica de mediación entre modelo y vista
- Manejo de eventos del usuario
- Actualización del modelo

---

#### FastAPI/Layered

**Models/Entities:**
- Validación de campos (Pydantic)
- Serialización/deserialización
- Validadores personalizados
- Casos de error (ValidationError)

**Schemas:**
- Conversión entre tipos (Create, Update, Response)
- Campos opcionales vs requeridos
- Validación de constraints

**Services:**
- Lógica de negocio aislada
- Interacción con repositories (mock)
- Manejo de excepciones de dominio
- Casos edge y validaciones

**Repositories:**
- CRUD operations (con test_db)
- Queries y filtros
- Manejo de constraints de DB

---

#### Django/MVT

**Models:**
- Validación de campos
- Constraints de DB (unique, foreign keys)
- Métodos del modelo (`__str__`, custom methods)
- Signals (si aplica)

**Views:**
- Status codes correctos
- Templates renderizados correctamente
- Context data esperado
- Permisos y autenticación

**Forms:**
- Validación de datos
- Clean methods personalizados
- Casos de error

**Serializers (DRF):**
- Serialización/deserialización
- Validadores personalizados
- Campos nested

---

#### Generic Python

**Classes:**
- Inicialización y atributos
- Métodos públicos y privados
- Comportamiento esperado
- Casos edge y excepciones

**Functions:**
- Input/output esperado
- Casos edge
- Manejo de errores
- Side effects (si aplica)

---

### 2. Generar estructura de tests

Crear archivo de tests siguiendo convención: `tests/test_{component_name}.py`

**Estructura recomendada:**
```python
"""Tests unitarios para {COMPONENT_NAME}."""
import pytest
# Imports específicos según stack

class Test{Component}Creation:
    """Tests de creación e inicialización."""

    def test_crear_con_valores_default(self):
        """Test de creación con valores por defecto."""
        pass

    def test_crear_con_valores_custom(self):
        """Test de creación con valores personalizados."""
        pass

class Test{Component}Validation:
    """Tests de validación de datos."""

    def test_validacion_campo_requerido(self):
        """Test que campo requerido falla si no se provee."""
        pass

    def test_validacion_tipo_dato(self):
        """Test que tipos de datos se validan correctamente."""
        pass

class Test{Component}Behavior:
    """Tests de comportamiento y métodos."""

    def test_metodo_principal(self):
        """Test del método principal del componente."""
        pass
```

---

### 3. Escribir tests usando fixtures

#### Ejemplos por Stack

**PyQt/MVC - Test de Modelo (Dataclass Inmutable):**
```python
# tests/test_user_profile_modelo.py
import pytest
from app.presentacion.paneles.user_profile.modelo import UserProfileModelo

class TestCreacion:
    """Tests de creación del modelo."""

    def test_crear_con_valores_default(self):
        """Modelo se crea con valores por defecto."""
        modelo = UserProfileModelo()
        assert modelo.nombre == ""
        assert modelo.edad == 0
        assert modelo.activo is True

    def test_crear_con_valores_custom(self):
        """Modelo se crea con valores personalizados."""
        modelo = UserProfileModelo(
            nombre="Juan Pérez",
            edad=30,
            activo=False
        )
        assert modelo.nombre == "Juan Pérez"
        assert modelo.edad == 30
        assert modelo.activo is False

class TestInmutabilidad:
    """Tests de inmutabilidad del modelo."""

    def test_no_se_puede_modificar_atributo(self):
        """Modelo es inmutable (frozen dataclass)."""
        modelo = UserProfileModelo(nombre="Original")
        with pytest.raises(AttributeError):
            modelo.nombre = "Modificado"

    def test_crear_copia_con_cambios(self):
        """Se puede crear copia modificada con replace()."""
        original = UserProfileModelo(nombre="Original", edad=25)
        modificado = original.replace(edad=30)

        assert original.edad == 25  # Original no cambia
        assert modificado.edad == 30
        assert modificado.nombre == "Original"  # Otros campos igual

class TestValidacion:
    """Tests de validación de datos."""

    def test_edad_negativa_falla(self):
        """Edad negativa lanza excepción."""
        with pytest.raises(ValueError, match="Edad debe ser >= 0"):
            UserProfileModelo(edad=-5)

    def test_nombre_vacio_permitido(self):
        """Nombre vacío es válido (valor default)."""
        modelo = UserProfileModelo(nombre="")
        assert modelo.nombre == ""
```

---

**FastAPI/Layered - Test de Schema (Pydantic):**
```python
# tests/test_user_schemas.py
import pytest
from pydantic import ValidationError
from app.schemas.user import UserCreate, UserResponse, UserUpdate

class TestUserCreate:
    """Tests del schema de creación."""

    def test_crear_schema_valido(self):
        """Schema válido se crea correctamente."""
        schema = UserCreate(
            email="user@example.com",
            nombre="Juan Pérez",
            edad=30
        )
        assert schema.email == "user@example.com"
        assert schema.nombre == "Juan Pérez"
        assert schema.edad == 30

    def test_email_invalido_falla(self):
        """Email inválido lanza ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(email="not-an-email", nombre="Juan")

        errors = exc_info.value.errors()
        assert any(e["loc"] == ("email",) for e in errors)

    def test_edad_negativa_falla(self):
        """Edad negativa falla validación."""
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(email="user@example.com", nombre="Juan", edad=-1)

        errors = exc_info.value.errors()
        assert any("edad" in str(e["loc"]) for e in errors)

class TestUserResponse:
    """Tests del schema de respuesta."""

    def test_from_orm(self):
        """Schema se crea desde modelo ORM."""
        # Mock de modelo ORM
        class MockUser:
            id = 1
            email = "user@example.com"
            nombre = "Juan"
            edad = 30
            created_at = "2024-01-01T00:00:00"

        schema = UserResponse.model_validate(MockUser())
        assert schema.id == 1
        assert schema.email == "user@example.com"
```

---

**FastAPI/Layered - Test de Service (Lógica de Negocio):**
```python
# tests/test_user_service.py
import pytest
from unittest.mock import Mock, AsyncMock
from app.services.user_service import UserService
from app.schemas.user import UserCreate

@pytest.fixture
def mock_user_repository():
    """Mock del repositorio de usuarios."""
    repo = Mock()
    repo.create = AsyncMock(return_value={"id": 1, "email": "user@example.com"})
    repo.get_by_email = AsyncMock(return_value=None)
    return repo

@pytest.fixture
def user_service(mock_user_repository):
    """Instancia del servicio con repositorio mockeado."""
    return UserService(repository=mock_user_repository)

class TestCreateUser:
    """Tests de creación de usuario."""

    @pytest.mark.asyncio
    async def test_crear_usuario_exitoso(self, user_service, mock_user_repository):
        """Usuario se crea correctamente."""
        user_data = UserCreate(email="new@example.com", nombre="Juan", edad=30)

        result = await user_service.create_user(user_data)

        assert result["id"] == 1
        mock_user_repository.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_crear_usuario_email_duplicado_falla(self, user_service, mock_user_repository):
        """No se puede crear usuario con email duplicado."""
        # Simular que email ya existe
        mock_user_repository.get_by_email.return_value = {"id": 999, "email": "existing@example.com"}

        user_data = UserCreate(email="existing@example.com", nombre="Juan", edad=30)

        with pytest.raises(ValueError, match="Email ya existe"):
            await user_service.create_user(user_data)
```

---

**Django/MVT - Test de Model:**
```python
# tests/test_user_model.py
import pytest
from django.core.exceptions import ValidationError
from app.models import User

@pytest.mark.django_db
class TestUserModel:
    """Tests del modelo User."""

    def test_crear_usuario(self):
        """Usuario se crea correctamente."""
        user = User.objects.create(
            email="user@example.com",
            nombre="Juan Pérez",
            edad=30
        )
        assert user.id is not None
        assert user.email == "user@example.com"

    def test_str_representation(self):
        """__str__ retorna representación correcta."""
        user = User(email="user@example.com", nombre="Juan Pérez")
        assert str(user) == "Juan Pérez (user@example.com)"

    def test_email_unique_constraint(self):
        """Email debe ser único."""
        User.objects.create(email="user@example.com", nombre="Juan")

        with pytest.raises(Exception):  # IntegrityError
            User.objects.create(email="user@example.com", nombre="Pedro")

    def test_edad_validacion(self):
        """Edad debe ser >= 0."""
        user = User(email="user@example.com", nombre="Juan", edad=-1)

        with pytest.raises(ValidationError):
            user.full_clean()
```

---

**Generic Python - Test de Class:**
```python
# tests/test_calculator.py
import pytest
from app.utils.calculator import Calculator

class TestCalculator:
    """Tests de la clase Calculator."""

    @pytest.fixture
    def calculator(self):
        """Fixture de calculadora."""
        return Calculator()

    def test_suma(self, calculator):
        """Suma funciona correctamente."""
        result = calculator.add(5, 3)
        assert result == 8

    def test_resta(self, calculator):
        """Resta funciona correctamente."""
        result = calculator.subtract(10, 4)
        assert result == 6

    def test_division_por_cero(self, calculator):
        """División por cero lanza excepción."""
        with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
            calculator.divide(10, 0)

    @pytest.mark.parametrize("a,b,expected", [
        (2, 3, 6),
        (0, 5, 0),
        (-2, 3, -6),
        (2, -3, -6),
    ])
    def test_multiplicacion_casos(self, calculator, a, b, expected):
        """Multiplicación con múltiples casos."""
        result = calculator.multiply(a, b)
        assert result == expected
```

---

### 4. Ejecutar tests

Según el stack, ejecutar tests con comandos apropiados:

**PyQt/MVC:**
```bash
# Ejecutar todos los tests
pytest tests/ -v

# Ejecutar tests de un componente específico
pytest tests/test_user_profile_modelo.py -v

# Con coverage
pytest tests/ -v --cov={COMPONENT_PATH} --cov-report=term --cov-report=html

# Solo tests que fallen
pytest tests/ -v --lf
```

**FastAPI:**
```bash
# Ejecutar tests (incluye async)
pytest tests/ -v

# Con coverage
pytest tests/ -v --cov=app --cov-report=term --cov-report=html

# Solo tests async
pytest tests/ -v -k async
```

**Django:**
```bash
# Ejecutar tests
pytest tests/ -v

# Con configuración de DB
pytest tests/ -v --ds=config.settings.test

# Reusar DB para velocidad
pytest tests/ -v --reuse-db

# Coverage
pytest tests/ -v --cov=app --cov-report=term
```

**Generic Python:**
```bash
# Ejecutar tests
pytest tests/ -v

# Con coverage detallado
pytest tests/ -v --cov={MODULE_NAME} --cov-report=term-missing

# Mostrar print statements
pytest tests/ -v -s
```

---

### 5. Validar coverage

**Objetivo mínimo:** Coverage > 95% del código nuevo

```bash
# Generar reporte de coverage
pytest --cov={COMPONENT_PATH} --cov-report=term --cov-report=html

# Ver reporte en terminal
# Debe mostrar líneas cubiertas por tests

# Abrir reporte HTML (más detallado)
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

**Analizar reporte:**
- Líneas no cubiertas (mostradas en rojo en HTML)
- Branches no cubiertos (if/else sin testear ambos casos)
- Funciones sin tests

**Agregar tests para líneas no cubiertas** hasta alcanzar el objetivo.

---

### 6. Fixtures personalizados (conftest.py)

Si hay fixtures reutilizables, crearlos en `tests/conftest.py`:

**PyQt/MVC:**
```python
# tests/conftest.py
import pytest
from PyQt6.QtWidgets import QApplication

@pytest.fixture(scope="session")
def qapp():
    """Aplicación Qt para tests (provisto por pytest-qt)."""
    # pytest-qt lo provee automáticamente
    pass

@pytest.fixture
def sample_modelo():
    """Fixture de modelo de ejemplo."""
    from app.presentacion.paneles.user_profile.modelo import UserProfileModelo
    return UserProfileModelo(nombre="Test User", edad=25)
```

**FastAPI:**
```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture
def test_db():
    """Base de datos de prueba."""
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)

    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestingSessionLocal()

    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_db):
    """Cliente HTTP de testing."""
    return TestClient(app)
```

**Django:**
```python
# tests/conftest.py
import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def test_user(db):
    """Usuario de prueba."""
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass123"
    )

@pytest.fixture
def authenticated_client(client, test_user):
    """Cliente autenticado."""
    client.force_login(test_user)
    return client
```

---

## Objetivo de Coverage

**Target:** > 95% de cobertura del código nuevo

**Qué debe estar cubierto:**
- ✅ Todos los métodos públicos
- ✅ Validaciones y casos edge
- ✅ Paths de error (excepciones)
- ✅ Lógica condicional (if/else)

**Qué puede excluirse:**
- ❌ Métodos abstractos o stubs
- ❌ Código de configuración boilerplate
- ❌ Imports y constantes

---

## Tracking al Finalizar

```python
tracker.end_phase(4, auto_approved=True)
```

---

## Resumen de la Fase

Al finalizar esta fase:

✅ Tests unitarios completos para todos los componentes
✅ Coverage > 95% del código nuevo
✅ Tests ejecutándose correctamente (todos pasan)
✅ Fixtures reutilizables en conftest.py (si aplica)
✅ Validación de comportamiento y casos edge
✅ Tests de regresión para prevenir bugs futuros

**Próxima fase:** Fase 5 - Tests de Integración
