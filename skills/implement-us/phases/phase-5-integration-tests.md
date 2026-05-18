# Fase 5: Tests de Integración

**Objetivo:** Validar que múltiples componentes funcionan correctamente juntos, probando flujos end-to-end del sistema.


---

## 🔴 Acción Requerida — Verificar precondiciones

Antes de comenzar esta fase, confirmá que los tests unitarios de Fase 4 pasan:

```bash
pytest tests/unit/ -v --tb=short
```

> La precondición es que **los tests pasan**, no solo que el directorio existe.
> Si `tests/unit/` no tiene tests aún, significa que Fase 4 no se completó — completala primero.
> Si algún test falla, resolvé los fallos en Fase 4 antes de continuar.

Si algún test falla, **no avances** — completá Fase 4 primero.

---

## 🔴 Acción Requerida — Iniciar tracking de fase

Ejecutá como primera acción, antes de cualquier otra:

```bash
python .claude/tracking/tracker_cli.py start-phase 5 "Tests de Integración"
```

---

## Acción

Crear tests que validen la integración entre componentes implementados, simulando flujos reales de uso del sistema.

**Diferencia con Tests Unitarios:**
- **Unitarios:** Prueban componentes aislados con mocks
- **Integración:** Prueban componentes trabajando juntos con dependencias reales o parcialmente mockeadas

---

## Estrategias de Integración por Stack

### PyQt/MVC

**Flujos típicos a testear:**
- Señal desde modelo → actualización de vista
- Acción del usuario en vista → actualización de modelo vía controlador
- Comunicación entre múltiples paneles/componentes
- Integración con servicios externos (servidor, DB, APIs)

**Herramientas:**
- `pytest-qt` para simular interacción de usuario (qtbot.mouseClick, qtbot.keyClicks)
- `qtbot.waitSignal()` para esperar señales
- Mocks de servicios externos (servidores, APIs)

---

### FastAPI/Layered

**Flujos típicos a testear:**
- Endpoint → Service → Repository → Database
- Middleware → Endpoint → Response
- Autenticación/autorización en endpoints
- Manejo de excepciones end-to-end
- Validación de datos a través de capas

**Herramientas:**
- `TestClient` de FastAPI para requests HTTP
- Base de datos de prueba (SQLite, TestContainers)
- Mocks de servicios externos (APIs terceros)

---

### Generic Python

**Flujos típicos a testear:**
- Múltiples clases/módulos trabajando juntos
- Pipelines de procesamiento de datos
- Integración con sistemas de archivos
- Integración con APIs/servicios externos

**Herramientas:**
- `unittest.mock` para mocks complejos
- `tmp_path` para filesystem testing
- Fixtures que crean entornos de prueba completos

---

## Pasos de Implementación

### 1. Identificar flujos de integración críticos

Basarse en los escenarios BDD de la Fase 1 para identificar flujos end-to-end que deben testearse.

**Preguntas a responder:**
- ¿Qué flujo completo ejecuta el usuario?
- ¿Qué componentes están involucrados?
- ¿Cuáles son los puntos de integración críticos?
- ¿Qué puede fallar en la comunicación entre componentes?

---

### 2. Crear archivo de tests de integración

Convención: `tests/integration/test_{feature}_integration.py`

**Estructura recomendada:**
```python
"""Tests de integración para {FEATURE_NAME}."""
import pytest
# Imports específicos según stack

class TestIntegration{Feature}:
    """Tests de integración del flujo completo."""

    def test_flujo_exitoso_completo(self, fixtures):
        """Test del happy path end-to-end."""
        # Arrange: Setup del sistema completo
        # Act: Ejecutar acción que atraviesa múltiples componentes
        # Assert: Validar resultado final y estados intermedios
        pass

    def test_flujo_con_error_en_componente_intermedio(self, fixtures):
        """Test de manejo de errores entre componentes."""
        pass

    def test_flujo_con_datos_edge_case(self, fixtures):
        """Test con datos límite que atraviesan el sistema."""
        pass
```

---

### 3. Implementar tests con dependencias reales o mockeadas

#### Ejemplos por Stack

**PyQt/MVC - Test de integración Modelo-Vista-Controlador:**
```python
# tests/integration/test_user_profile_integration.py
import pytest
from PyQt6.QtCore import Qt
from app.presentacion.paneles.user_profile.modelo import UserProfileModelo
from app.presentacion.paneles.user_profile.vista import UserProfileVista
from app.presentacion.paneles.user_profile.controlador import UserProfileControlador

class TestUserProfileIntegration:
    """Tests de integración del panel User Profile."""

    @pytest.fixture
    def user_profile_system(self, qtbot):
        """Sistema completo: modelo + vista + controlador."""
        modelo = UserProfileModelo(nombre="", edad=0)
        vista = UserProfileVista()
        controlador = UserProfileControlador(modelo, vista)

        qtbot.addWidget(vista)
        return controlador, vista, modelo

    def test_actualizar_nombre_actualiza_vista(self, qtbot, user_profile_system):
        """Usuario actualiza nombre → vista se actualiza."""
        controlador, vista, _ = user_profile_system

        # Simular que usuario escribe en el campo de nombre
        qtbot.keyClicks(vista.input_nombre, "Juan Pérez")
        qtbot.mouseClick(vista.btn_guardar, Qt.MouseButton.LeftButton)

        # Esperar señal de actualización
        with qtbot.waitSignal(controlador.modelo_actualizado, timeout=1000):
            pass

        # Validar que modelo se actualizó
        assert controlador.modelo.nombre == "Juan Pérez"

        # Validar que vista muestra el nombre
        assert vista.label_nombre.text() == "Juan Pérez"

    def test_integracion_con_servicio_externo(self, qtbot, user_profile_system, mocker):
        """Flujo completo: UI → Controlador → Servicio → Backend."""
        controlador, vista, _ = user_profile_system

        # Mock del servicio de guardado
        mock_service = mocker.patch('app.services.user_service.save_user')
        mock_service.return_value = True

        # Usuario guarda perfil
        qtbot.keyClicks(vista.input_nombre, "Juan Pérez")
        qtbot.mouseClick(vista.btn_guardar, Qt.MouseButton.LeftButton)

        # Validar que servicio fue llamado
        mock_service.assert_called_once()
        call_args = mock_service.call_args[0][0]
        assert call_args.nombre == "Juan Pérez"

    def test_comunicacion_entre_paneles(self, qtbot):
        """Test de señales entre múltiples componentes."""
        from app.presentacion.paneles.user_profile.controlador import UserProfileControlador
        from app.presentacion.paneles.dashboard.controlador import DashboardControlador

        profile_ctrl = UserProfileControlador(
            UserProfileModelo(),
            UserProfileVista()
        )
        dashboard_ctrl = DashboardControlador()

        # Conectar señal entre paneles
        profile_ctrl.usuario_actualizado.connect(
            dashboard_ctrl.on_usuario_actualizado
        )

        # Actualizar perfil
        nuevo_modelo = UserProfileModelo(nombre="Juan", edad=30)

        with qtbot.waitSignal(dashboard_ctrl.vista_actualizada, timeout=1000):
            profile_ctrl.actualizar_modelo(nuevo_modelo)

        # Validar que dashboard recibió la actualización
        assert dashboard_ctrl.usuario_actual.nombre == "Juan"
```

---

**FastAPI/Layered - Test de integración Endpoint-Service-Repository:**
```python
# tests/integration/test_user_endpoints_integration.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models.user import User

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture
def test_db():
    """Base de datos de prueba con datos iniciales."""
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

    db = TestingSessionLocal()
    yield db

    db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_db):
    """Cliente HTTP de testing."""
    return TestClient(app)

class TestUserEndpointsIntegration:
    """Tests de integración de endpoints de usuario."""

    def test_crear_usuario_flujo_completo(self, client, test_db):
        """POST /users → Service → Repository → DB."""
        # Crear usuario vía API
        response = client.post(
            "/api/v1/users",
            json={"email": "test@example.com", "nombre": "Juan", "edad": 30}
        )

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "test@example.com"
        assert "id" in data

        # Validar que se guardó en DB
        user_in_db = test_db.query(User).filter(User.email == "test@example.com").first()
        assert user_in_db is not None
        assert user_in_db.nombre == "Juan"

    def test_obtener_actualizar_eliminar_flujo(self, client, test_db):
        """Test CRUD completo end-to-end."""
        # 1. Crear usuario
        response = client.post(
            "/api/v1/users",
            json={"email": "test@example.com", "nombre": "Juan", "edad": 30}
        )
        user_id = response.json()["id"]

        # 2. Obtener usuario
        response = client.get(f"/api/v1/users/{user_id}")
        assert response.status_code == 200
        assert response.json()["nombre"] == "Juan"

        # 3. Actualizar usuario
        response = client.put(
            f"/api/v1/users/{user_id}",
            json={"nombre": "Juan Pérez", "edad": 31}
        )
        assert response.status_code == 200
        assert response.json()["nombre"] == "Juan Pérez"

        # 4. Eliminar usuario
        response = client.delete(f"/api/v1/users/{user_id}")
        assert response.status_code == 204

        # 5. Validar que ya no existe
        response = client.get(f"/api/v1/users/{user_id}")
        assert response.status_code == 404

    def test_validacion_propagada_a_traves_de_capas(self, client):
        """Validación de Pydantic → 422 en endpoint."""
        # Email inválido debe ser rechazado
        response = client.post(
            "/api/v1/users",
            json={"email": "not-an-email", "nombre": "Juan", "edad": 30}
        )

        assert response.status_code == 422
        assert "email" in response.json()["detail"][0]["loc"]

    def test_autenticacion_end_to_end(self, client, test_db):
        """Login → Token → Endpoint protegido."""
        # 1. Crear usuario con password
        client.post(
            "/api/v1/auth/register",
            json={"email": "user@example.com", "password": "secret123"}
        )

        # 2. Login para obtener token
        response = client.post(
            "/api/v1/auth/login",
            data={"username": "user@example.com", "password": "secret123"}
        )
        token = response.json()["access_token"]

        # 3. Acceder a endpoint protegido
        response = client.get(
            "/api/v1/users/me",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        assert response.json()["email"] == "user@example.com"
```

---

**Generic Python - Test de integración de pipeline:**
```python
# tests/integration/test_data_pipeline_integration.py
import pytest
from pathlib import Path
from app.pipeline.extractor import DataExtractor
from app.pipeline.transformer import DataTransformer
from app.pipeline.loader import DataLoader

class TestDataPipelineIntegration:
    """Tests de integración del pipeline de datos."""

    @pytest.fixture
    def sample_data_file(self, tmp_path):
        """Archivo de datos de prueba."""
        data_file = tmp_path / "data.csv"
        data_file.write_text("id,name,value\n1,item1,100\n2,item2,200\n")
        return data_file

    @pytest.fixture
    def output_dir(self, tmp_path):
        """Directorio de salida."""
        output = tmp_path / "output"
        output.mkdir()
        return output

    def test_pipeline_completo_end_to_end(self, sample_data_file, output_dir):
        """Test del flujo completo: Extract → Transform → Load."""
        # 1. Extract
        extractor = DataExtractor()
        raw_data = extractor.extract(sample_data_file)

        assert len(raw_data) == 2
        assert raw_data[0]['name'] == 'item1'

        # 2. Transform
        transformer = DataTransformer()
        transformed_data = transformer.transform(raw_data)

        assert len(transformed_data) == 2
        assert transformed_data[0]['value_doubled'] == 200

        # 3. Load
        loader = DataLoader()
        output_file = output_dir / "output.json"
        loader.load(transformed_data, output_file)

        # 4. Validar resultado final
        assert output_file.exists()
        import json
        with open(output_file) as f:
            loaded_data = json.load(f)

        assert len(loaded_data) == 2
        assert loaded_data[0]['value_doubled'] == 200

    def test_pipeline_con_error_en_transform(self, sample_data_file, output_dir):
        """Test de manejo de errores en pipeline."""
        # Datos inválidos
        bad_file = sample_data_file.parent / "bad.csv"
        bad_file.write_text("id,name,value\n1,item1,invalid\n")

        extractor = DataExtractor()
        transformer = DataTransformer()

        raw_data = extractor.extract(bad_file)

        # Transform debe manejar error
        with pytest.raises(ValueError, match="Invalid value"):
            transformer.transform(raw_data)

    def test_pipeline_con_multiples_archivos(self, tmp_path, output_dir):
        """Test de procesamiento batch."""
        # Crear múltiples archivos
        files = []
        for i in range(3):
            f = tmp_path / f"data{i}.csv"
            f.write_text(f"id,name,value\n{i},item{i},{i*100}\n")
            files.append(f)

        # Procesar todos
        extractor = DataExtractor()
        transformer = DataTransformer()
        loader = DataLoader()

        all_data = []
        for file in files:
            raw = extractor.extract(file)
            transformed = transformer.transform(raw)
            all_data.extend(transformed)

        output_file = output_dir / "combined.json"
        loader.load(all_data, output_file)

        # Validar
        import json
        with open(output_file) as f:
            loaded = json.load(f)

        assert len(loaded) == 3
```

---

### 4. Ejecutar tests de integración

**Comandos por stack:**

**PyQt/MVC:**
```bash
# Tests de integración específicos
pytest tests/integration/ -v

# Con coverage
pytest tests/integration/ -v --cov=app --cov-report=term

# Solo tests de integración (marcar con @pytest.mark.integration)
pytest -m integration -v
```

**FastAPI:**
```bash
# Tests con base de datos de prueba
pytest tests/integration/ -v

# Con logs de SQL (debug)
pytest tests/integration/ -v --log-cli-level=DEBUG

# Paralelo (cuidado con DB)
pytest tests/integration/ -v -n auto
```

**Generic Python:**
```bash
# Tests de integración
pytest tests/integration/ -v

# Con output detallado
pytest tests/integration/ -v -s

# Con coverage
pytest tests/integration/ -v --cov={MODULE_NAME} --cov-report=html
```

---

### 5. Validar cobertura de flujos críticos

**Checklist de validación:**

- ✅ ¿Todos los flujos end-to-end del usuario están cubiertos?
- ✅ ¿Se prueban casos de error en la integración?
- ✅ ¿Se valida la comunicación entre componentes?
- ✅ ¿Se testean dependencias externas (con mocks o test doubles)?
- ✅ ¿Los tests son determinísticos (no flaky)?
- ✅ ¿Los tests limpian sus recursos (DB, archivos)?

---

## Diferencias con Tests Unitarios

| Aspecto | Tests Unitarios | Tests de Integración |
|---------|----------------|---------------------|
| **Scope** | Un componente aislado | Múltiples componentes |
| **Dependencias** | Totalmente mockeadas | Reales o parcialmente mockeadas |
| **Velocidad** | Rápidos (ms) | Más lentos (segundos) |
| **Objetivo** | Validar lógica interna | Validar interacción |
| **Coverage** | Alto (>95%) | Flujos críticos |

---

## Estrategia de Mocking

### ¿Qué mockear?

**Mockear siempre:**
- ✅ APIs y servicios externos fuera del sistema (servicios de terceros, backends remotos)
- ✅ Operaciones costosas o no determinísticas (envío de emails, tiempo, random)

**Usar real o test double — no mock puro:**
- ⚠️ Base de datos → usar test DB (SQLite en memoria u otra DB de prueba)
- ⚠️ Filesystem → usar `tmp_path` de pytest
- ⚠️ Componentes propios del sistema → integrarlos realmente (ese es el objetivo del test de integración)

**Excepción válida:** se puede mockear un componente interno cuando su implementación aún no existe (Fase 3 incompleta) o cuando integrarlo correspondería a un nivel de test superior (ej. end-to-end). En ese caso, documentar la razón en el test.

---


---

## ✅ Checklist de Salida

Antes de avanzar a Fase 6, confirmá que:
- [ ] Todos los tests de integración pasan: `pytest tests/integration/ -v`
- [ ] Tracking de Fase 5 cerrado

## 🔴 Acción Requerida — Cerrar tracking

```bash
python .claude/tracking/tracker_cli.py end-phase 5
```

---

## 🚫 Si esta fase falla — Protocolo de recuperación

**Síntoma:** Uno o más tests de integración fallan.

**Protocolo:**
1. Leé el output completo del error
2. Identificá el origen del fallo:
   - **Problema de integración entre componentes** → revisá las interfaces y contratos en Fase 3
   - **Componente individual roto** → volvé a Fase 3 a corregir la implementación, luego volvé a Fase 4 y 5
   - **Test mal configurado** (fixture, mock incorrecto) → corregí el test en esta fase
3. Re-ejecutá los tests de integración: `pytest tests/integration/ -v`
4. No avances a Fase 6 hasta que **todos** los tests pasen
5. Si después de 2 ciclos completos (ejecución → detección de no conformidad → corrección) los tests siguen fallando, informá al usuario antes de continuar

---

## Resumen de la Fase

Al finalizar esta fase:

✅ Tests de integración para flujos críticos
✅ Validación de comunicación entre componentes
✅ Tests end-to-end del happy path y casos de error
✅ Mocking apropiado de dependencias externas
✅ Todos los tests de integración pasando
✅ Confianza en que el sistema funciona como un todo

**Próxima fase:** Fase 6 - Validación BDD
