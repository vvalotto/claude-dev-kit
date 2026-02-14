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

### Flask/Layered
```bash
# Dependencias necesarias
pytest>=7.0.0
pytest-flask>=1.2.0
pytest-cov>=4.0.0

# Fixtures disponibles
- app: Flask app instance (scope='module')
- client: Flask test client para requests HTTP
- context: Test request context para acceder request/session
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

#### Flask/Layered

**Domain Models (dataclass):**
- Inicialización con valores default/custom
- Método to_dict() para serialización
- Método validar() con reglas de negocio
- Casos edge (valores None, negativos, strings vacíos)

**Repositories (ABC + implementación):**
- CRUD operations (get_all, get_by_id, create, update, delete)
- Comportamiento según storage (memoria, JSON, DB)
- Manejo de items no encontrados (return None)
- Integridad de datos (IDs únicos, etc.)

**API Endpoints (Flask blueprints):**
- Tests de integración con Flask test client
- Request/response correctos (jsonify)
- Status codes apropiados (200, 201, 404, 400)
- Validación de request body
- Error handling (NotFoundError, ValidationError)

**Mappers:**
- Conversión dict → model
- Conversión model → dict
- Validación de datos externos

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

**Flask/Layered - Test de Domain Model (dataclass):**
```python
# tests/unit/test_product_model.py
import pytest
from app.general.products.product import Product

class TestProductCreation:
    """Tests de creación del modelo de dominio."""

    def test_crear_con_valores_default(self):
        """Producto se crea con valores por defecto."""
        product = Product(id=1, nombre="Test Product")
        assert product.id == 1
        assert product.nombre == "Test Product"
        assert product.precio is None  # Optional field

    def test_crear_con_todos_los_campos(self):
        """Producto se crea con todos los campos."""
        product = Product(
            id=1,
            nombre="Laptop",
            precio=1500.50,
            stock=10
        )
        assert product.id == 1
        assert product.nombre == "Laptop"
        assert product.precio == 1500.50
        assert product.stock == 10

class TestProductSerialization:
    """Tests de serialización del modelo."""

    def test_to_dict(self):
        """to_dict() retorna dict con todos los campos."""
        product = Product(id=1, nombre="Mouse", precio=25.99, stock=50)
        data = product.to_dict()

        assert data == {
            'id': 1,
            'nombre': 'Mouse',
            'precio': 25.99,
            'stock': 50
        }

    def test_to_dict_con_valores_none(self):
        """to_dict() maneja correctamente valores None."""
        product = Product(id=1, nombre="Test")
        data = product.to_dict()

        assert data['id'] == 1
        assert data['nombre'] == 'Test'
        assert data['precio'] is None

class TestProductValidation:
    """Tests de validación del modelo."""

    def test_validar_nombre_vacio_falla(self):
        """Validación falla si nombre está vacío."""
        product = Product(id=1, nombre="")

        with pytest.raises(ValueError, match="nombre es requerido"):
            product.validar()

    def test_validar_precio_negativo_falla(self):
        """Validación falla si precio es negativo."""
        product = Product(id=1, nombre="Test", precio=-10.0)

        with pytest.raises(ValueError, match="precio debe ser >= 0"):
            product.validar()

    def test_validar_stock_negativo_falla(self):
        """Validación falla si stock es negativo."""
        product = Product(id=1, nombre="Test", stock=-5)

        with pytest.raises(ValueError, match="stock debe ser >= 0"):
            product.validar()

    def test_validar_producto_valido(self):
        """Validación exitosa retorna True."""
        product = Product(id=1, nombre="Test", precio=100.0, stock=10)
        assert product.validar() is True
```

---

**Flask/Layered - Test de Repository (in-memory):**
```python
# tests/unit/test_product_repository.py
import pytest
from app.datos.products.memoria import ProductRepositoryMemory
from app.general.products.product import Product

@pytest.fixture
def repository():
    """Fixture que retorna repositorio limpio."""
    return ProductRepositoryMemory()

@pytest.fixture
def sample_product():
    """Fixture de producto de ejemplo."""
    return Product(id=0, nombre="Test Product", precio=100.0, stock=10)

class TestRepositoryCreate:
    """Tests de creación en repositorio."""

    def test_create_asigna_id_automaticamente(self, repository, sample_product):
        """create() asigna ID automáticamente."""
        result = repository.create(sample_product)

        assert result.id == 1  # Primer ID asignado
        assert result.nombre == sample_product.nombre

    def test_create_incrementa_id(self, repository):
        """IDs se incrementan automáticamente."""
        product1 = repository.create(Product(id=0, nombre="Product 1"))
        product2 = repository.create(Product(id=0, nombre="Product 2"))

        assert product1.id == 1
        assert product2.id == 2

class TestRepositoryGetAll:
    """Tests de get_all()."""

    def test_get_all_vacio_inicialmente(self, repository):
        """get_all() retorna lista vacía si no hay productos."""
        products = repository.get_all()
        assert products == []

    def test_get_all_retorna_todos_los_productos(self, repository):
        """get_all() retorna todos los productos creados."""
        repository.create(Product(id=0, nombre="Product 1"))
        repository.create(Product(id=0, nombre="Product 2"))

        products = repository.get_all()
        assert len(products) == 2

    def test_get_all_retorna_copia(self, repository):
        """get_all() retorna copia (no referencia directa)."""
        repository.create(Product(id=0, nombre="Product 1"))
        products1 = repository.get_all()
        products2 = repository.get_all()

        assert products1 is not products2  # Diferentes objetos

class TestRepositoryGetById:
    """Tests de get_by_id()."""

    def test_get_by_id_existente(self, repository):
        """get_by_id() retorna producto si existe."""
        created = repository.create(Product(id=0, nombre="Test"))
        found = repository.get_by_id(created.id)

        assert found is not None
        assert found.id == created.id
        assert found.nombre == "Test"

    def test_get_by_id_no_existente(self, repository):
        """get_by_id() retorna None si no existe."""
        found = repository.get_by_id(999)
        assert found is None

class TestRepositoryUpdate:
    """Tests de update()."""

    def test_update_producto_existente(self, repository):
        """update() actualiza producto existente."""
        created = repository.create(Product(id=0, nombre="Original", precio=100.0))
        updated = Product(id=created.id, nombre="Updated", precio=150.0)

        result = repository.update(updated)

        assert result.nombre == "Updated"
        assert result.precio == 150.0

    def test_update_producto_no_existente_retorna_none(self, repository):
        """update() retorna None si producto no existe."""
        product = Product(id=999, nombre="No Exists")
        result = repository.update(product)

        assert result is None

class TestRepositoryDelete:
    """Tests de delete()."""

    def test_delete_producto_existente(self, repository):
        """delete() elimina producto existente."""
        created = repository.create(Product(id=0, nombre="To Delete"))

        deleted = repository.delete(created.id)

        assert deleted is True
        assert repository.get_by_id(created.id) is None

    def test_delete_producto_no_existente(self, repository):
        """delete() retorna False si producto no existe."""
        deleted = repository.delete(999)
        assert deleted is False
```

---

**Flask Webapp - Test de Routes (Template Rendering + Mocking):**
```python
# tests/integration/test_products_routes.py
import pytest
from webapp import create_app
from unittest.mock import MagicMock

@pytest.fixture
def app():
    """Create Flask app for testing."""
    app = create_app('testing')
    return app

@pytest.fixture
def client(app):
    """Create Flask test client."""
    return app.test_client()

class TestProductRoutes:
    """Tests de routes de productos."""

    def test_index_page_renders(self, client):
        """Test home page renders correctamente."""
        response = client.get('/')

        assert response.status_code == 200
        assert b'Home' in response.data
        assert b'<!DOCTYPE html>' in response.data

    @pytest.mark.template
    def test_product_list_renders(self, client, mocker):
        """Test product list page con datos de API."""
        # Mock APIClient.get_products()
        mock_api = mocker.patch('webapp.routes.APIClient')
        mock_api.return_value.get_products.return_value = [
            {'id': 1, 'nombre': 'Product 1', 'precio': 100.0, 'stock': 10},
            {'id': 2, 'nombre': 'Product 2', 'precio': 200.0, 'stock': 5}
        ]

        response = client.get('/products')

        assert response.status_code == 200
        assert b'Products' in response.data
        assert b'Product 1' in response.data
        assert b'Product 2' in response.data

    @pytest.mark.template
    def test_product_list_empty(self, client, mocker):
        """Test product list con lista vacía."""
        mock_api = mocker.patch('webapp.routes.APIClient')
        mock_api.return_value.get_products.return_value = []

        response = client.get('/products')

        assert response.status_code == 200
        assert b'No products available' in response.data or b'no products' in response.data.lower()

    @pytest.mark.integration
    def test_product_detail_found(self, client, mocker):
        """Test product detail con producto existente."""
        mock_api = mocker.patch('webapp.routes.APIClient')
        mock_api.return_value.get_product.return_value = {
            'id': 1,
            'nombre': 'Test Product',
            'precio': 150.0,
            'stock': 20
        }

        response = client.get('/products/1')

        assert response.status_code == 200
        assert b'Test Product' in response.data
        assert b'150' in response.data

    @pytest.mark.integration
    def test_product_detail_not_found(self, client, mocker):
        """Test product detail 404 cuando no existe."""
        mock_api = mocker.patch('webapp.routes.APIClient')
        mock_api.return_value.get_product.return_value = None

        response = client.get('/products/999')

        assert response.status_code == 404
        assert b'404' in response.data or b'Not Found' in response.data

    @pytest.mark.integration
    def test_product_list_api_error(self, client, mocker):
        """Test product list cuando API backend falla."""
        mock_api = mocker.patch('webapp.routes.APIClient')
        mock_api.return_value.get_products.side_effect = Exception("Backend unavailable")

        response = client.get('/products')

        assert response.status_code == 500
        assert b'500' in response.data or b'error' in response.data.lower()

class TestProductForms:
    """Tests de forms de productos."""

    def test_product_new_form_renders(self, client):
        """Test form de nuevo producto renderiza (GET)."""
        response = client.get('/products/new')

        assert response.status_code == 200
        assert b'form' in response.data.lower()
        assert b'csrf_token' in response.data.lower()

    @pytest.mark.integration
    def test_product_create_success(self, client, mocker):
        """Test crear producto via form (POST)."""
        mock_api = mocker.patch('webapp.routes.APIClient')
        mock_api.return_value.create_product.return_value = {
            'id': 1,
            'nombre': 'New Product',
            'precio': 99.99
        }

        data = {
            'nombre': 'New Product',
            'precio': 99.99,
            'stock': 10
        }

        response = client.post('/products/new', data=data, follow_redirects=True)

        assert response.status_code == 200
        mock_api.return_value.create_product.assert_called_once()

class TestErrorHandlers:
    """Tests de error handlers."""

    def test_404_custom_page(self, client):
        """Test custom 404 error page."""
        response = client.get('/nonexistent-page')

        assert response.status_code == 404
        assert b'404' in response.data

    def test_500_custom_page(self, client, mocker):
        """Test custom 500 error page."""
        # Forzar error 500 con mock que falla
        mocker.patch('webapp.routes.APIClient', side_effect=Exception("Forced error"))

        response = client.get('/products')

        assert response.status_code == 500
```

**Flask Webapp - Test de API Client (BFF Pattern):**
```python
# tests/unit/test_api_client.py
import pytest
import requests
from webapp.api_client import APIClient

class TestAPIClientProducts:
    """Tests de APIClient métodos de productos."""

    def test_get_products_success(self, requests_mock):
        """Test get_products retorna lista correctamente."""
        api_url = "http://localhost:5050/api/products"
        mock_data = [
            {'id': 1, 'nombre': 'Product 1'},
            {'id': 2, 'nombre': 'Product 2'}
        ]

        requests_mock.get(api_url, json=mock_data)

        client = APIClient()
        products = client.get_products()

        assert len(products) == 2
        assert products[0]['nombre'] == 'Product 1'

    def test_get_product_success(self, requests_mock):
        """Test get_product retorna producto por ID."""
        api_url = "http://localhost:5050/api/products/1"
        mock_data = {'id': 1, 'nombre': 'Test Product', 'precio': 100.0}

        requests_mock.get(api_url, json=mock_data)

        client = APIClient()
        product = client.get_product(1)

        assert product is not None
        assert product['id'] == 1
        assert product['nombre'] == 'Test Product'

    def test_get_product_not_found(self, requests_mock):
        """Test get_product retorna None cuando 404."""
        api_url = "http://localhost:5050/api/products/999"
        requests_mock.get(api_url, status_code=404)

        client = APIClient()
        product = client.get_product(999)

        assert product is None

    def test_get_products_timeout(self, requests_mock):
        """Test get_products maneja timeout correctamente."""
        api_url = "http://localhost:5050/api/products"
        requests_mock.get(api_url, exc=requests.exceptions.Timeout)

        client = APIClient()

        with pytest.raises(requests.exceptions.Timeout):
            client.get_products()

    def test_create_product_success(self, requests_mock):
        """Test create_product crea producto correctamente."""
        api_url = "http://localhost:5050/api/products"
        request_data = {'nombre': 'New Product', 'precio': 50.0}
        response_data = {'id': 1, 'nombre': 'New Product', 'precio': 50.0}

        requests_mock.post(api_url, json=response_data, status_code=201)

        client = APIClient()
        product = client.create_product(request_data)

        assert product['id'] == 1
        assert product['nombre'] == 'New Product'
```

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
