# Tutorial: Clean Architecture BC-First - Suscripciones

**Stack:** FastAPI + Clean Architecture BC-First (clean-architecture-bc)
**Tiempo Estimado:** < 60 minutos
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

Este tutorial te guiará paso a paso en la creación de un **BC de Suscripciones** (alta y baja de una suscripción) utilizando el perfil **clean-architecture-bc** del Claude Dev Kit.

A diferencia de los perfiles "clásicos" (`fastapi-rest`, `flask-rest`, etc.), `clean-architecture-bc` organiza el código por **Bounded Context** (BC) siguiendo las 4 capas de Clean Architecture: `entities → use_cases → interface_adapters → frameworks`, con la **Dependency Rule** como regla no negociable — las dependencias del código fuente solo pueden apuntar hacia adentro.

Aprenderás:
- ✅ Cómo el skill `/implement-us` adapta las 10 fases a un perfil BC-first
- ✅ Cómo se traduce la Dependency Rule en decisiones concretas de imports y carpetas
- ✅ Cómo separar Entities, UseCases, Ports, Gateways, Repositories y Controllers
- ✅ Por qué el scope de quality gates (Pylint, coverage) es distinto al de los perfiles clásicos

Al finalizar, tendrás una API funcional (`examples/code/suscripciones-clean-arch/`) y comprenderás cómo aplicar Clean Architecture BC-first a tus propios Bounded Contexts.

---

## ✅ Requisitos Previos

### Software Necesario

- **Python:** 3.10 o superior
- **Claude Code CLI:** Instalado y configurado
- **FastAPI:** Se instala como dependencia del proyecto
- **Git:** Para control de versiones

### Conocimientos

- Programación orientada a objetos en Python (dataclasses, ABC)
- Conceptos básicos de arquitectura hexagonal / Ports & Adapters
- (Opcional) Haber leído sobre Clean Architecture (Robert C. Martin)

### Verificación

```bash
python --version   # Debe ser >= 3.10
claude --version
git --version
```

---

## 📖 Historia de Usuario

```gherkin
# US-001: Alta y baja de suscripciones

Como administrador del servicio
Quiero dar de alta y de baja suscripciones de usuarios
Para controlar el acceso al servicio según su plan contratado
```

### Alcance

**Funcionalidades Principales:**
- Dar de alta una nueva suscripción (email + plan)
- Dar de baja (cancelar) una suscripción existente
- Impedir altas duplicadas para un email con suscripción activa
- Notificar (a un servicio externo simulado) cada alta y cada baja

**Componentes a Implementar (BC `suscripciones`):**
- Entity `Suscripcion`
- Ports `SuscripcionRepositoryPort` y `NotificacionGatewayPort`
- UseCases `CrearSuscripcionUseCase` y `CancelarSuscripcionUseCase`
- Repository `MemoriaSuscripcionRepository` (implementa el Port de persistencia)
- Gateway `NotificacionGateway` (implementa el Port de notificaciones)
- Controller `SuscripcionController`
- ApiRouter (FastAPI)

**Casos de Uso:**
1. Un administrador da de alta una suscripción con un email y un plan válidos
2. El sistema rechaza un alta si el email ya tiene una suscripción activa
3. Un administrador cancela una suscripción existente
4. El sistema rechaza cancelar una suscripción inexistente o ya cancelada

---

## 🚀 Setup del Proyecto

### 1. Crear Directorio del Proyecto

```bash
mkdir suscripciones-clean-arch
cd suscripciones-clean-arch
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
cat > requirements.txt << EOF
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.4.0
httpx>=0.25.0
pytest>=7.0.0
pytest-cov>=4.1.0
pytest-bdd>=6.0.0
pylint>=2.15.0
EOF

pip install -r requirements.txt
```

### 5. Crear Estructura Base

A diferencia de un proyecto "clásico" con una única carpeta `app/`, un proyecto BC-first organiza el código **por Bounded Context**, y dentro de cada BC, por capa:

```bash
mkdir -p src/suscripciones/entities
mkdir -p src/suscripciones/use_cases/ports
mkdir -p src/suscripciones/interface_adapters/controllers
mkdir -p src/suscripciones/interface_adapters/gateways
mkdir -p src/suscripciones/frameworks/repositories
mkdir -p src/suscripciones/frameworks/api
mkdir -p tests/unit/suscripciones
mkdir -p tests/integration/suscripciones
mkdir -p features/steps
```

**Estructura del proyecto:**

```
suscripciones-clean-arch/
├── src/suscripciones/
│   ├── entities/
│   ├── use_cases/
│   │   └── ports/
│   ├── interface_adapters/
│   │   ├── controllers/
│   │   └── gateways/
│   └── frameworks/
│       ├── repositories/
│       └── api/
├── tests/
│   ├── unit/suscripciones/
│   └── integration/suscripciones/
├── features/
│   └── steps/
├── main.py
├── requirements.txt
└── README.md
```

---

## 📦 Instalación del Framework

### 1. Clonar Claude Dev Kit

```bash
cd ~
git clone https://github.com/vvalotto/claude-dev-kit.git ~/.claude-dev-kit
```

### 2. Ejecutar Instalador

```bash
cd suscripciones-clean-arch

python ~/.claude-dev-kit/install/installer.py --profile clean-architecture-bc --yes
```

**Salida esperada:**

```
✅ Framework instalado exitosamente en .claude/
✅ Perfil 'clean-architecture-bc' configurado
✅ Skills disponibles:
   - /implement-us
   - /track-pause, /track-resume, /track-status
✅ Templates instalados: bdd, planning, testing, reporting
```

### 3. Verificar Instalación

```bash
ls -la .claude/
cat CLAUDE.md
```

Como el perfil activo es BC-first, el `CLAUDE.md` autogenerado incluye una sección **"Capas y Orden de Implementación"** (ver #57) con la tabla de capas, el orden obligatorio (`Entities → Ports → UseCases → Repositories → Gateways → Controllers`) y la Dependency Rule — no solo la lista plana de tipos de componente que ven los otros perfiles.

---

## 🎬 Walkthrough: Las 10 Fases

### Preparación: Crear Archivo US

```bash
mkdir -p historias-usuario
cat > historias-usuario/US-001.md << 'EOF'
# US-001: Alta y baja de suscripciones

Como administrador del servicio
Quiero dar de alta y de baja suscripciones de usuarios
Para controlar el acceso al servicio según su plan contratado

## Criterios de Aceptación

1. Dado un email y un plan válidos (`basico` o `premium`), al darlos de alta
   se crea una suscripción activa y se notifica el alta.
2. Si el email ya tiene una suscripción activa, el alta se rechaza.
3. Dado el id de una suscripción activa, al cancelarla queda inactiva y se
   notifica la baja.
4. Cancelar una suscripción inexistente o ya cancelada se rechaza.
EOF
```

### Ejecutar el Skill

```bash
# En Claude Code, ejecutar:
/implement-us US-001
```

---

### 🔍 Fase 0: Validación de Contexto

**Qué hace el framework:**
- ✅ Verifica que `historias-usuario/US-001.md` exista
- ✅ Lee el perfil `clean-architecture-bc` desde `.claude/skills/implement-us/config.json`
- ✅ Carga `customizations/clean-architecture-bc.json` — capas, `component_path` por tipo de componente, `implementation_order`
- ✅ Inicializa el tracking de tiempo

**Output:**

```
✅ Historia de usuario encontrada: US-001
✅ Perfil cargado: clean-architecture-bc
✅ Configuración:
   - Arquitectura: clean-architecture (BC-first)
   - Capas: entities → use_cases → interface_adapters → frameworks
   - Test Framework: pytest + httpx
   - Quality Gates: Pylint ≥ 8.0, Coverage ≥ 90% (scope: entities/ + use_cases/)
⏱️  Tracking iniciado para US-001
```

**¿Qué hacer si falla?**
- Verificá que `historias-usuario/US-001.md` exista
- Confirmá que `.claude/skills/implement-us/customizations/clean-architecture-bc.json` existe

---

### 📝 Fase 1: Generación de Escenarios BDD

**Qué hace el framework:**
- 📄 Lee los criterios de aceptación de la HU
- 🤖 Genera escenarios Gherkin — **en inglés** (`Given/When/Then`): `bdd_config.language_note` del perfil indica explícitamente no usar `# language: es`, porque pytest-bdd 8.x requiere keywords en inglés
- 💾 Crea `tests/features/US-001-suscripciones.feature`

**Ejemplo de Output:**

```gherkin
@US-001
Feature: Subscription management
  As a service administrator
  I want to create and cancel subscriptions
  So that users can control their access to the service

  Background:
    Given the API is available

  Scenario: Create a new subscription
    When a subscription is created for "ana@example.com" with plan "basico"
    Then the response status code is 201
    And the subscription is active

  Scenario: Reject a duplicate active subscription
    Given a subscription exists for "ana@example.com" with plan "basico"
    When a subscription is created for "ana@example.com" with plan "premium"
    Then the response status code is 409
```

**Interacción:**
- Claude muestra los escenarios generados
- Podés pedir ajustes antes de continuar
- Checkpoint: ¿Aprobar escenarios? (`[aprobado]`)

---

### 📋 Fase 2: Generación de Plan de Implementación

**Qué hace el framework:**
- 🏗️ Analiza los escenarios BDD
- 📊 Traduce el `implementation_order` del perfil en un plan concreto de tareas
- 🎯 Determina el path exacto de cada componente vía `component_path.by_component`

**Orden obligatorio (Dependency Rule — de adentro hacia afuera):**

```
Entities → Ports → UseCases → Repositories → Gateways → Controllers
```

**Decisiones Clave:**
- BC: `suscripciones`
- Entity: `Suscripcion` (`src/suscripciones/entities/suscripcion.py`)
- Ports: `SuscripcionRepositoryPort`, `NotificacionGatewayPort` (`src/suscripciones/use_cases/ports/`)
- UseCases: `CrearSuscripcionUseCase`, `CancelarSuscripcionUseCase`
- Repository: `MemoriaSuscripcionRepository` (`src/suscripciones/frameworks/repositories/`)
- Gateway: `NotificacionGateway` (`src/suscripciones/interface_adapters/gateways/`)
- Controller: `SuscripcionController` (`src/suscripciones/interface_adapters/controllers/`)

**Archivo creado:** `docs/plans/US-001-plan.md`

---

### ⚙️ Fase 3: Implementación

**Qué hace el framework:**
- 💻 Guía la creación de cada componente **en el orden obligatorio**, nunca salteado
- 🔧 En cada paso, valida el import rule de la capa (`design_patterns.clean_architecture.import_rules` del perfil)
- 📁 Crea archivos en la estructura de `src/suscripciones/`

**1. Entity (capa `entities/`):**

```python
# src/suscripciones/entities/suscripcion.py
@dataclass
class Suscripcion:
    email: str
    plan: str
    fecha_alta: date
    id: Optional[int] = None
    activa: bool = field(default=True)
    fecha_baja: Optional[date] = None

    def __post_init__(self) -> None:
        if "@" not in self.email or not self.email.strip():
            raise EmailInvalidoError(f"Email inválido: '{self.email}'")
        if self.plan not in PLANES_VALIDOS:
            raise PlanInvalidoError(f"Plan '{self.plan}' no soportado")

    def cancelar(self, fecha: date) -> None:
        if not self.activa:
            raise SuscripcionYaCanceladaError(f"La suscripción {self.id} ya estaba cancelada")
        self.activa = False
        self.fecha_baja = fecha
```

Nota la ausencia total de imports de FastAPI, SQLAlchemy o cualquier otra cosa fuera de `entities/` — la regla de oro del perfil: *"`<bc>/entities/ no importa nada fuera de su propio entities/`"*.

**2. Ports (capa `use_cases/ports/`):**

```python
# src/suscripciones/use_cases/ports/suscripcion_repository_port.py
class SuscripcionRepositoryPort(ABC):
    @abstractmethod
    def guardar(self, suscripcion: Suscripcion) -> Suscripcion: ...
    @abstractmethod
    def obtener_por_id(self, suscripcion_id: int) -> Optional[Suscripcion]: ...
    @abstractmethod
    def obtener_por_email(self, email: str) -> Optional[Suscripcion]: ...
```

Los Ports son el único punto de contacto entre `use_cases/` y el mundo exterior — nunca se importa una implementación concreta desde el UseCase, solo el contrato.

**3. UseCases (capa `use_cases/`):**

```python
# src/suscripciones/use_cases/crear_suscripcion_use_case.py
class CrearSuscripcionUseCase:
    def __init__(self, repositorio: SuscripcionRepositoryPort, notificador: NotificacionGatewayPort):
        self._repositorio = repositorio
        self._notificador = notificador

    def ejecutar(self, datos: CrearSuscripcionInput) -> SuscripcionOutput:
        existente = self._repositorio.obtener_por_email(datos.email)
        if existente is not None and existente.activa:
            raise SuscripcionYaExisteError(f"El email '{datos.email}' ya tiene una suscripción activa")

        suscripcion = Suscripcion(email=datos.email, plan=datos.plan, fecha_alta=date.today())
        suscripcion = self._repositorio.guardar(suscripcion)
        self._notificador.notificar_alta(suscripcion)

        return SuscripcionOutput(...)
```

El UseCase recibe sus Ports por constructor (Dependency Injection manual) — nunca instancia una implementación concreta.

**4. Repository, Gateway y Controller (capas externas):**

- `MemoriaSuscripcionRepository` implementa `SuscripcionRepositoryPort` — **simplificación deliberada**: en vez de SQLAlchemy async + PostgreSQL (sugerido por el perfil), usa un diccionario en memoria para que el tutorial corra sin infraestructura externa. La interfaz es idéntica a la que tendría una implementación real.
- `NotificacionGateway` implementa `NotificacionGatewayPort` — simula el envío guardando las notificaciones en una lista.
- `SuscripcionController` traduce `Dict` externos a los DTOs del UseCase, y **solo importa `use_cases/`** — nunca `entities/` ni `frameworks/` directamente.

**5. ApiRouter (capa `frameworks/`, la más externa):**

```python
# src/suscripciones/frameworks/api/router.py
@router.post("", status_code=201)
def crear_suscripcion(body: CrearSuscripcionRequest):
    try:
        return controller.crear(body.model_dump())
    except (EmailInvalidoError, PlanInvalidoError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except SuscripcionYaExisteError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
```

Es la única capa que conoce FastAPI, y la responsable de traducir excepciones de dominio/aplicación a códigos de estado HTTP.

**Composition root (`main.py`):** arma el grafo de dependencias completo — es el único archivo del proyecto que conoce las 4 capas a la vez.

**Archivos creados:**
```
src/suscripciones/entities/suscripcion.py
src/suscripciones/entities/excepciones.py
src/suscripciones/use_cases/ports/suscripcion_repository_port.py
src/suscripciones/use_cases/ports/notificacion_gateway_port.py
src/suscripciones/use_cases/dtos.py
src/suscripciones/use_cases/excepciones.py
src/suscripciones/use_cases/crear_suscripcion_use_case.py
src/suscripciones/use_cases/cancelar_suscripcion_use_case.py
src/suscripciones/interface_adapters/gateways/notificacion_gateway.py
src/suscripciones/interface_adapters/controllers/suscripcion_controller.py
src/suscripciones/frameworks/repositories/memoria_suscripcion_repository.py
src/suscripciones/frameworks/api/router.py
main.py
```

---

### 🧪 Fase 4: Tests Unitarios

**Qué hace el framework:**
- 🔬 Genera tests para `entities/` y `use_cases/` — el scope que cuenta para el quality gate de coverage
- 🎭 Usa **fakes de los Ports**, nunca la implementación real de `frameworks/`, para mantener el test unitario aislado de infraestructura

**Ejemplo — fake del Port de persistencia (`tests/unit/suscripciones/conftest.py`):**

```python
class FakeRepositorio(SuscripcionRepositoryPort):
    def __init__(self):
        self._data: Dict[int, Suscripcion] = {}
        self._next_id = 1

    def guardar(self, suscripcion):
        if suscripcion.id is None:
            suscripcion.id = self._next_id
            self._next_id += 1
        self._data[suscripcion.id] = suscripcion
        return suscripcion
    # ...
```

**Ejemplo de test:**

```python
def test_rechaza_email_duplicado_activo(self, crear_use_case):
    crear_use_case.ejecutar(CrearSuscripcionInput(email="ana@example.com", plan="basico"))

    with pytest.raises(SuscripcionYaExisteError):
        crear_use_case.ejecutar(CrearSuscripcionInput(email="ana@example.com", plan="premium"))
```

**Ejecución:**

```bash
pytest tests/unit/ -v --cov=src/suscripciones/entities --cov=src/suscripciones/use_cases --cov-report=term-missing
```

**Output real obtenido en este ejemplo:**

```
tests/unit/suscripciones/test_suscripcion.py .......                    [ 50%]
tests/unit/suscripciones/test_crear_suscripcion_use_case.py ...         [ 71%]
tests/unit/suscripciones/test_cancelar_suscripcion_use_case.py ...      [100%]

Name                                                          Stmts   Miss  Cover
--------------------------------------------------------------------------------
src/suscripciones/entities/suscripcion.py                        23      0   100%
src/suscripciones/use_cases/crear_suscripcion_use_case.py         18      0   100%
src/suscripciones/use_cases/cancelar_suscripcion_use_case.py      16      0   100%
--------------------------------------------------------------------------------
TOTAL                                                            100      0   100%

14 passed
```

**Archivos creados:**
```
tests/unit/suscripciones/conftest.py
tests/unit/suscripciones/test_suscripcion.py
tests/unit/suscripciones/test_crear_suscripcion_use_case.py
tests/unit/suscripciones/test_cancelar_suscripcion_use_case.py
```

---

### 🔗 Fase 5: Tests de Integración

**Qué hace el framework:**
- 🌐 Genera tests end-to-end usando `TestClient` de FastAPI contra la app real (con `MemoriaSuscripcionRepository`, no un mock)
- 🔄 Valida el flujo completo: HTTP → Controller → UseCase → Repository → respuesta HTTP

**Ejemplo:**

```python
def test_crear_suscripcion_duplicada_devuelve_409(self, client):
    client.post("/suscripciones", json={"email": "ana@example.com", "plan": "basico"})

    response = client.post("/suscripciones", json={"email": "ana@example.com", "plan": "premium"})

    assert response.status_code == 409
```

**Ejecución:**

```bash
pytest tests/integration/ -v
```

**Archivos creados:**
```
tests/conftest.py                                  # fixture `client` compartida
tests/integration/suscripciones/test_suscripcion_api.py
```

---

### ✅ Fase 6: Validación BDD

**Qué hace el framework:**
- 🥒 Genera step definitions para los escenarios Gherkin de Fase 1
- 🔗 Reutiliza la misma fixture `client` de Fase 5 para consistencia
- ⚠️ Respeta `bdd_config.language_note`: keywords en inglés (`@given/@when/@then`), sin `# language: es`

**Ejemplo de Step Definitions:**

```python
@given(parsers.parse('a subscription exists for "{email}" with plan "{plan}"'), target_fixture="context")
def subscription_exists(client, context, email, plan):
    response = client.post("/suscripciones", json={"email": email, "plan": plan})
    assert response.status_code == 201
    context["subscription_id"] = response.json()["id"]
    return context


@then(parsers.parse("the response status code is {status:d}"))
def check_status_code(context, status):
    assert context["response"].status_code == status
```

**Ejecución:**

```bash
pytest features/steps/ -v
```

**Output real obtenido:**

```
features/steps/suscripcion_steps.py::test_create_subscription PASSED
features/steps/suscripcion_steps.py::test_reject_duplicate_subscription PASSED
features/steps/suscripcion_steps.py::test_cancel_subscription PASSED
features/steps/suscripcion_steps.py::test_reject_cancel_nonexistent PASSED

4 passed
```

**Archivos creados:**
```
features/suscripciones.feature
features/steps/suscripcion_steps.py
```

---

### 📊 Fase 7: Quality Gates

**Qué hace el framework:**
- 🔍 Ejecuta CodeGuard (Pylint + radon) — **solo sobre `entities/` + `use_cases/`**
- 📈 Calcula complejidad ciclomática (máx. 10 por función)
- 📊 Verifica cobertura — mismo scope reducido

**Por qué el scope es distinto a los perfiles clásicos:** en `clean-architecture-bc`, `interface_adapters/` y `frameworks/` son capas de "pegamento" (traducción de formatos, configuración de FastAPI) — el perfil considera que la lógica de negocio que realmente necesita cobertura estricta vive en `entities/` y `use_cases/`.

**Umbrales (clean-architecture-bc):**

| Métrica | Umbral | Scope |
|---|---|---|
| Pylint | ≥ 8.0 | `entities/` + `use_cases/` |
| Complejidad Ciclomática | ≤ 10 por función | Todo el BC |
| Coverage | ≥ 90% | `entities/` + `use_cases/` |

**Ejecución:**

```bash
pylint src/suscripciones/entities src/suscripciones/use_cases
pytest --cov=src/suscripciones/entities --cov=src/suscripciones/use_cases --cov-fail-under=90
```

**Output real obtenido en este ejemplo:**

```
Your code has been rated at 9.67/10

TOTAL   100    0   100%
```

Ambos umbrales superados con margen.

**¿Qué hacer si fallan?**
- Pylint bajo: revisar duplicación de código entre UseCases (`R0801`) extrayendo un helper compartido, o funciones con demasiadas responsabilidades
- Coverage bajo: agregar tests de los caminos de excepción (`SuscripcionYaExisteError`, `SuscripcionNoEncontradaError`, `SuscripcionYaCanceladaError`)

---

### 📚 Fase 8: Documentación

**Qué hace el framework:**
- 📖 Actualiza el `docs/plans/US-001-plan.md` con el resultado real
- 🗂️ Documenta las decisiones de diseño no triviales (ej. repositorio en memoria como simplificación)
- 💡 Actualiza el `README.md` del proyecto con endpoints y ejemplos de uso

**Archivos actualizados:**
```
docs/plans/US-001-plan.md
CHANGELOG.md
README.md
```

---

### 📈 Fase 9: Reporte Final

**Ejemplo de Reporte:**

```markdown
# Reporte de Implementación: US-001

## 📊 Resumen Ejecutivo

- **Estado:** ✅ Completado
- **Tests:** 25/25 pasando
- **Cobertura:** 100% (entities/ + use_cases/)
- **Quality Gates:** ✅ Todos aprobados (Pylint 9.67/10)

## 📝 Componentes Implementados

- Entity: Suscripcion
- Ports: SuscripcionRepositoryPort, NotificacionGatewayPort
- UseCases: CrearSuscripcionUseCase, CancelarSuscripcionUseCase
- Repository: MemoriaSuscripcionRepository
- Gateway: NotificacionGateway
- Controller: SuscripcionController
- ApiRouter: FastAPI

## 🧪 Testing

- Tests Unitarios: 14 (100% passing)
- Tests Integración: 7 (100% passing)
- Escenarios BDD: 4 (100% passing)

## 📊 Métricas de Calidad

- Pylint: 9.67/10
- Cobertura: 100% (scope: entities/ + use_cases/)
```

```bash
/track-report US-001
```

---

## ✅ Validación Final

### Checklist Completo

**Código:**
- [x] Las 6 capas del `implementation_order` implementadas en orden
- [x] `entities/` sin imports fuera de sí mismo
- [x] `use_cases/` sin imports de `interface_adapters/` ni `frameworks/`
- [x] `interface_adapters/` sin imports directos de `frameworks/`

**Tests:**
- [x] 14 tests unitarios (entities + use_cases) — 100% passing
- [x] 7 tests de integración — 100% passing
- [x] 4 escenarios BDD — 100% passing

**Calidad:**
- [x] Pylint 9.67/10 (≥ 8.0)
- [x] Complejidad Ciclomática < 10
- [x] Cobertura 100% (≥ 90%), scope entities/ + use_cases/

**Documentación:**
- [x] README del proyecto de ejemplo actualizado
- [x] Este tutorial

### Ejecutar Aplicación

```bash
cd examples/code/suscripciones-clean-arch
source venv/bin/activate
uvicorn main:app --reload
```

### Verificación Manual

```bash
# Alta
curl -X POST http://localhost:8000/suscripciones \
  -H "Content-Type: application/json" \
  -d '{"email": "ana@example.com", "plan": "basico"}'

# Baja (usar el id devuelto arriba)
curl -X POST http://localhost:8000/suscripciones/1/cancelar
```

---

## 🔧 Troubleshooting

### Problema: `ImportError: No module named 'suscripciones'`

**Causa:** el código vive en `src/`, que debe estar en el `PYTHONPATH`.

**Solución:**
```bash
# pytest.ini ya declara pythonpath = . src — si corrés scripts sueltos:
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

### Problema: `'US-001' not found in markers configuration option`

**Causa:** `pytest.ini` tiene `--strict-markers` activo y el tag `@US-001` del `.feature` se registra como marcador de pytest.

**Solución:** agregar el marcador a `pytest.ini`:
```ini
markers =
    US-001: Historia de usuario US-001
```

### Problema: Un test unitario importa `frameworks/` y rompe el aislamiento

**Causa:** se usó `MemoriaSuscripcionRepository` real en vez de un fake del Port en un test de `use_cases/`.

**Solución:** en `tests/unit/`, siempre instanciar un `Fake*` que implemente el Port (`SuscripcionRepositoryPort`, `NotificacionGatewayPort`) — nunca la implementación de `frameworks/` ni `interface_adapters/`.

### Problema: Quality gates fallan con `R0801: Similar lines in 2 files`

**Causa:** los dos UseCases construyen el mismo `SuscripcionOutput` de forma idéntica.

**Solución:** es aceptable si el Pylint global sigue ≥ 8.0 (en este ejemplo: 9.67/10) — si querés eliminarlo, extraé un método `_a_dto(suscripcion)` compartido en un módulo `use_cases/mappers.py`.

---

## 🚀 Próximos Pasos

### Ampliar el BC

1. **`CambiarPlanUseCase`**: nuevo UseCase que reutiliza `SuscripcionRepositoryPort` sin tocar `entities/`
2. **`ListarSuscripcionesUseCase`**: agregar un método `listar()` al Port y su implementación
3. **Persistencia real**: reemplazar `MemoriaSuscripcionRepository` por SQLAlchemy async + PostgreSQL — la interfaz (`SuscripcionRepositoryPort`) no cambia, por lo que ningún UseCase se modifica

### Agregar un segundo BC

En un sistema BC-first real, un segundo Bounded Context (ej. `facturacion`) se comunica con `suscripciones` **solo a través de Ports** — nunca con imports directos entre BCs (`bc_communication` en `design_patterns.clean_architecture` del perfil).

### Explorar Otros Perfiles

- **hexagonal-ddd-bc:** BC-first con DDD táctico completo (Aggregates, DomainEvents) — ver el [tutorial de Reservas](hexagonal-ddd-bc-project.md)
- **fastapi-rest:** API REST en capas, sin organización por BC
- **generic-python:** proyectos Python genéricos

```bash
python ~/.claude-dev-kit/install/installer.py --profile hexagonal-ddd-bc --yes
```

---

## 📚 Recursos

### Documentación del Framework

- [Guía de Inicio Rápido](../user/getting-started.md)
- [Personalización de Perfiles](../user/customization.md)
- [Perfil clean-architecture-bc (customization)](../../skills/implement-us/customizations/clean-architecture-bc.json)

### Clean Architecture

- Robert C. Martin, *Clean Architecture: A Craftsman's Guide to Software Structure and Design*
- [FastAPI — documentación oficial](https://fastapi.tiangolo.com/)

### Comunidad

- GitHub: https://github.com/vvalotto/claude-dev-kit
- Issues: https://github.com/vvalotto/claude-dev-kit/issues

---

## 📝 Conclusión

¡Felicidades! Completaste tu primer BC con Clean Architecture usando el Claude Dev Kit.

**Lo que aprendiste:**
- ✅ Cómo la Dependency Rule se traduce en imports concretos entre carpetas
- ✅ Separar Entities, UseCases, Ports, Gateways, Repositories y Controllers
- ✅ Por qué el quality gate de este perfil solo mide `entities/` + `use_cases/`
- ✅ Cómo simplificar infraestructura (repositorio en memoria) sin romper la arquitectura

**Siguiente paso:** aplicá esta misma estructura a un Bounded Context real de tu dominio.

---

**Tutorial Creado:** 2026-09-05
**Claude Dev Kit:** v1.6.0
**Perfil:** clean-architecture-bc
