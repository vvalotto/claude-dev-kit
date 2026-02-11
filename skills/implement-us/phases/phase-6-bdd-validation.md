# Fase 6: Validación BDD

**Objetivo:** Ejecutar y validar que todos los escenarios BDD (Gherkin) generados en la Fase 1 pasan correctamente.

**Duración estimada:** 15-20 minutos

---

## Tracking

**Al inicio de la fase:**
```python
tracker.start_phase(6, "Validación BDD")
```

---

## Acción

Ejecutar los escenarios BDD generados en la Fase 1, implementando los steps necesarios y validando que el comportamiento del sistema coincide con las especificaciones.

**Framework:** pytest-bdd (Python) o equivalente según stack

---

## Pasos de Validación

### 1. Configurar pytest-bdd (si no existe)

**Instalar dependencias:**
```bash
pip install pytest-bdd>=6.0.0
```

**Estructura de archivos:**
```
tests/
├── features/                    # Archivos .feature (Gherkin)
│   └── {US_ID}-*.feature       # Escenarios de la US
├── step_defs/                   # Implementación de steps
│   └── test_{feature}_steps.py
└── conftest.py                  # Fixtures compartidos
```

---

### 2. Implementar steps de los escenarios

Los escenarios BDD se componen de tres tipos de steps:

- **Given:** Setup del contexto inicial (precondiciones)
- **When:** Acciones que ejecuta el usuario o sistema
- **Then:** Validaciones del resultado esperado (aserciones)

La implementación de steps varía según el stack tecnológico.

---

#### Ejemplos de Steps por Stack

**PyQt/MVC - Steps con qtbot:**
```python
# tests/step_defs/test_user_profile_steps.py
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from PyQt6.QtCore import Qt
from app.presentacion.paneles.user_profile.vista import UserProfileVista
from app.presentacion.paneles.user_profile.controlador import UserProfileControlador
from app.presentacion.paneles.user_profile.modelo import UserProfileModelo

# Cargar escenarios
scenarios('../features/{US_ID}-user-profile.feature')

@pytest.fixture
def context():
    """Contexto compartido entre steps."""
    return {}

@pytest.fixture
def user_profile_panel(qtbot, context):
    """Panel de perfil de usuario completo."""
    modelo = UserProfileModelo()
    vista = UserProfileVista()
    controlador = UserProfileControlador(modelo, vista)

    qtbot.addWidget(vista)
    vista.show()

    context['controlador'] = controlador
    context['vista'] = vista
    context['modelo'] = modelo

    return controlador

@given("el panel de perfil de usuario está abierto")
def panel_abierto(user_profile_panel):
    """Panel está visible."""
    assert user_profile_panel.vista.isVisible()

@given(parsers.parse('el usuario tiene nombre "{nombre}" y edad {edad:d}'))
def usuario_con_datos(user_profile_panel, nombre, edad):
    """Usuario con datos iniciales."""
    nuevo_modelo = user_profile_panel.modelo.replace(nombre=nombre, edad=edad)
    user_profile_panel.actualizar_modelo(nuevo_modelo)

@when(parsers.parse('el usuario ingresa "{texto}" en el campo nombre'))
def ingresar_nombre(qtbot, context, texto):
    """Usuario escribe en campo nombre."""
    vista = context['vista']
    vista.input_nombre.clear()
    qtbot.keyClicks(vista.input_nombre, texto)

@when("el usuario hace clic en el botón Guardar")
def clic_guardar(qtbot, context):
    """Usuario hace clic en guardar."""
    vista = context['vista']
    qtbot.mouseClick(vista.btn_guardar, Qt.MouseButton.LeftButton)

@then(parsers.parse('el sistema muestra el nombre "{nombre}"'))
def valida_nombre_mostrado(context, nombre):
    """Validar nombre en la vista."""
    vista = context['vista']
    assert vista.label_nombre.text() == nombre

@then(parsers.parse('el modelo tiene edad {edad:d}'))
def valida_edad_modelo(context, edad):
    """Validar edad en el modelo."""
    modelo = context['modelo']
    assert modelo.edad == edad
```

---

**FastAPI - Steps con TestClient:**
```python
# tests/step_defs/test_user_api_steps.py
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from fastapi.testclient import TestClient
from app.main import app

scenarios('../features/{US_ID}-user-api.feature')

@pytest.fixture
def context():
    """Contexto compartido."""
    return {'response': None, 'user_id': None}

@pytest.fixture
def api_client():
    """Cliente HTTP de testing."""
    return TestClient(app)

@given("el sistema está operativo")
def sistema_operativo(api_client):
    """API responde."""
    response = api_client.get("/health")
    assert response.status_code == 200

@given(parsers.parse('existe un usuario con email "{email}"'))
def usuario_existente(api_client, context, email, test_db):
    """Crear usuario en DB."""
    from app.models.user import User
    user = User(email=email, nombre="Usuario Test", edad=25)
    test_db.add(user)
    test_db.commit()
    context['user_id'] = user.id

@when(parsers.parse('se envía una petición POST a "/users" con email "{email}"'))
def crear_usuario(api_client, context, email):
    """POST para crear usuario."""
    response = api_client.post(
        "/api/v1/users",
        json={"email": email, "nombre": "Nuevo Usuario", "edad": 30}
    )
    context['response'] = response

@when(parsers.parse('se envía una petición GET a "/users/{user_id}"'))
def obtener_usuario(api_client, context):
    """GET para obtener usuario."""
    user_id = context['user_id']
    response = api_client.get(f"/api/v1/users/{user_id}")
    context['response'] = response

@then(parsers.parse("el sistema responde con código {status_code:d}"))
def valida_status_code(context, status_code):
    """Validar código de respuesta."""
    assert context['response'].status_code == status_code

@then(parsers.parse('la respuesta incluye el campo "{campo}"'))
def valida_campo_respuesta(context, campo):
    """Validar que campo existe en respuesta."""
    data = context['response'].json()
    assert campo in data

@then(parsers.parse('el email es "{email}"'))
def valida_email(context, email):
    """Validar email en respuesta."""
    data = context['response'].json()
    assert data['email'] == email
```

---

**Django - Steps con Django Client:**
```python
# tests/step_defs/test_user_views_steps.py
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from django.contrib.auth import get_user_model
from django.urls import reverse
from app.models import UserProfile

User = get_user_model()

scenarios('../features/{US_ID}-user-views.feature')

@pytest.fixture
def context():
    """Contexto compartido."""
    return {'response': None, 'user': None}

@pytest.mark.django_db
@given("el usuario está autenticado")
def usuario_autenticado(client, context):
    """Usuario autenticado."""
    user = User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass123"
    )
    client.force_login(user)
    context['user'] = user

@pytest.mark.django_db
@given(parsers.parse('existe un perfil con nombre "{nombre}"'))
def perfil_existente(context, nombre):
    """Crear perfil en DB."""
    profile = UserProfile.objects.create(
        user=context['user'],
        nombre=nombre,
        edad=25
    )
    context['profile'] = profile

@pytest.mark.django_db
@when(parsers.parse('el usuario accede a la URL "{url_name}"'))
def acceder_url(client, context, url_name):
    """GET a una URL por nombre."""
    url = reverse(url_name)
    response = client.get(url)
    context['response'] = response

@pytest.mark.django_db
@when(parsers.parse('el usuario envía el formulario con nombre "{nombre}"'))
def enviar_formulario(client, context, nombre):
    """POST de formulario."""
    url = reverse('user_profile_create')
    response = client.post(url, {
        'nombre': nombre,
        'edad': 30,
        'biografia': 'Bio de prueba'
    })
    context['response'] = response

@pytest.mark.django_db
@then(parsers.parse("el sistema responde con código {status_code:d}"))
def valida_status_code(context, status_code):
    """Validar código HTTP."""
    assert context['response'].status_code == status_code

@pytest.mark.django_db
@then(parsers.parse('la página muestra el texto "{texto}"'))
def valida_texto_pagina(context, texto):
    """Validar contenido de página."""
    content = context['response'].content.decode('utf-8')
    assert texto in content

@pytest.mark.django_db
@then(parsers.parse('existe un perfil en la base de datos con nombre "{nombre}"'))
def valida_perfil_db(nombre):
    """Validar que perfil existe en DB."""
    assert UserProfile.objects.filter(nombre=nombre).exists()
```

---

**Generic Python - Steps para lógica de negocio:**
```python
# tests/step_defs/test_calculator_steps.py
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from app.calculator import Calculator

scenarios('../features/{US_ID}-calculator.feature')

@pytest.fixture
def context():
    """Contexto compartido."""
    return {'calculator': None, 'result': None, 'error': None}

@given("una calculadora nueva")
def calculadora_nueva(context):
    """Instanciar calculadora."""
    context['calculator'] = Calculator()

@given(parsers.parse('la calculadora tiene el valor {valor:d}'))
def calculadora_con_valor(context, valor):
    """Calculadora con valor inicial."""
    context['calculator'] = Calculator(initial_value=valor)

@when(parsers.parse('se suma {a:d} y {b:d}'))
def sumar(context, a, b):
    """Ejecutar suma."""
    calc = context['calculator']
    context['result'] = calc.add(a, b)

@when(parsers.parse('se divide {a:d} entre {b:d}'))
def dividir(context, a, b):
    """Ejecutar división."""
    calc = context['calculator']
    try:
        context['result'] = calc.divide(a, b)
    except ZeroDivisionError as e:
        context['error'] = str(e)

@then(parsers.parse('el resultado es {esperado:d}'))
def valida_resultado(context, esperado):
    """Validar resultado."""
    assert context['result'] == esperado

@then(parsers.parse('se obtiene un error "{mensaje}"'))
def valida_error(context, mensaje):
    """Validar error."""
    assert context['error'] is not None
    assert mensaje in context['error']
```

---

### 3. Ejecutar escenarios BDD

**Comandos de ejecución:**

```bash
# Ejecutar todos los escenarios de la US
pytest tests/features/{US_ID}-*.feature -v

# Ejecutar con output detallado
pytest tests/features/{US_ID}-*.feature -v -s

# Ejecutar escenario específico por nombre
pytest tests/features/{US_ID}-*.feature -k "nombre del escenario" -v

# Generar reporte JUnit (para CI/CD)
pytest tests/features/{US_ID}-*.feature -v --junit-xml=reports/bdd-results.xml
```

**Ejemplo de output exitoso:**
```
tests/features/US-042-user-profile.feature::Usuario puede ver su perfil PASSED
tests/features/US-042-user-profile.feature::Usuario puede editar su nombre PASSED
tests/features/US-042-user-profile.feature::Sistema valida edad mínima PASSED

3 scenarios passed, 0 failed, 0 skipped
```

---

### 4. Validar que TODOS los escenarios pasan

**Criterio de éxito:** 100% de escenarios deben pasar.

**Si algún escenario falla:**

1. **Analizar el error:**
   ```
   FAILED tests/features/US-042-user-profile.feature::Usuario puede editar su nombre

   Step failed: When el usuario ingresa "Juan" en el campo nombre
   AssertionError: assert 'campo_nombre' not found
   ```

2. **Diagnosticar:**
   - ¿El step está bien implementado?
   - ¿El componente tiene un bug?
   - ¿El escenario está mal escrito?

3. **Corregir:**
   - Si es bug en componente → volver a Fase 3 (Implementación)
   - Si es step mal implementado → corregir step
   - Si es escenario mal escrito → ajustar .feature

4. **Re-ejecutar hasta que todos pasen**

---

## Tips de Implementación de Steps

### Usar parsers para parametrizar

```python
from pytest_bdd import parsers

# String parameter
@when(parsers.parse('el usuario ingresa "{texto}"'))
def step(texto):
    pass

# Integer parameter
@when(parsers.parse('el usuario tiene {edad:d} años'))
def step(edad):
    pass

# Float parameter
@when(parsers.parse('la temperatura es {temp:f} grados'))
def step(temp):
    pass
```

---

### Reutilizar fixtures entre steps

```python
@pytest.fixture
def context():
    """Contexto mutable compartido entre steps."""
    return {}

@given("contexto inicial")
def setup(context):
    context['dato'] = "valor"

@when("acción")
def action(context):
    # Acceder a dato guardado en given
    assert context['dato'] == "valor"
```

---

### Organizar steps por feature

```
tests/
├── features/
│   ├── US-042-user-profile.feature
│   └── US-043-user-settings.feature
└── step_defs/
    ├── test_user_profile_steps.py  # Steps para US-042
    └── test_user_settings_steps.py # Steps para US-043
```

---

### Steps compartidos (conftest.py)

Para steps que se reutilizan en múltiples features:

```python
# tests/step_defs/conftest.py
from pytest_bdd import given, when, then

@given("el sistema está operativo")
def sistema_operativo():
    """Step compartido."""
    pass

@then("no hay errores")
def sin_errores():
    """Step compartido."""
    pass
```

---

## Integración con CI/CD

Generar reportes para pipeline:

```bash
# JUnit XML (Jenkins, GitLab CI)
pytest tests/features/ --junit-xml=reports/bdd-junit.xml

# HTML report (más legible)
pytest tests/features/ --html=reports/bdd-report.html --self-contained-html

# JSON report (procesamiento automatizado)
pytest tests/features/ --json-report --json-report-file=reports/bdd-report.json
```

---

## Tracking al Finalizar

```python
tracker.end_phase(6, auto_approved=True)
```

---

## Resumen de la Fase

Al finalizar esta fase:

✅ Todos los escenarios BDD de la Fase 1 implementados como tests
✅ Steps correctamente implementados según el stack
✅ 100% de escenarios pasando (verde)
✅ Validación de que el sistema cumple con las especificaciones
✅ Comportamiento esperado documentado y testeado

**Próxima fase:** Fase 7 - Quality Gates
