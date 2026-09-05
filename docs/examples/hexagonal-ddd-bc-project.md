# Tutorial: Hexagonal DDD BC-First — Reservas API

**Stack:** Hexagonal DDD BC-First (`hexagonal-ddd-bc`)
**Tiempo Estimado:** 45-55 minutos
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

Este tutorial te guiará paso a paso en la creación de **Reservas API**, un
Bounded Context (BC) que permite reservar un recurso (ej. una mesa) en una
fecha y horario, utilizando el perfil **hexagonal-ddd-bc** del Claude Dev Kit.

A diferencia de los perfiles "por capas" (MVC, layered), este perfil organiza
el código **por Bounded Context primero, y por capa hexagonal dentro de cada
BC**: `domain → application → infrastructure → api`. Es el perfil a elegir
cuando tu dominio tiene reglas de negocio no triviales que merecen quedar
aisladas de cualquier framework o mecanismo de persistencia.

Aprenderás:
- ✅ Cómo el skill `/implement-us` aplica el orden de implementación
  obligatorio de DDD: ValueObjects → DomainEvents → AggregateRoot → Ports →
  CommandHandlers → QueryHandlers → Repositories → ApiRouter
- ✅ Cómo mantener `domain/` completamente aislado de infraestructura y
  framework HTTP
- ✅ Cómo expresar una invariante de negocio real (no-solapamiento de
  reservas) sin que el dominio conozca la base de datos
- ✅ Cómo estructura sus tests el perfil: unitarios sobre domain/application,
  integración sobre infrastructure/api, BDD sobre el flujo HTTP completo

Al finalizar, tendrás un BC funcional con:
- 1 AggregateRoot, 2 ValueObjects, 1 DomainEvent, 1 Port, 1 CommandHandler,
  1 QueryHandler, 1 Repository y 1 ApiRouter
- Suite completa de tests (39 tests: unitarios, integración, BDD)
- Código que supera los quality gates del perfil (Pylint 9.60/10, Coverage 100%
  en `domain/` + `application/`)

El proyecto de ejemplo completo está en
[`examples/code/reservas-hexagonal/`](../../examples/code/reservas-hexagonal/).

---

## ✅ Requisitos Previos

### Software Necesario

- **Python:** 3.10 o superior
- **Claude Code CLI:** Instalado y configurado
- **FastAPI:** Se instala como dependencia del proyecto (no requiere instalación previa)
- **Git:** Para control de versiones

### Conocimientos

- Programación orientada a objetos en Python
- Conceptos básicos de DDD: Aggregate, Value Object, Domain Event (el
  tutorial los explica a medida que aparecen, no son prerequisito estricto)
- Familiaridad con APIs REST y la terminal

### Verificación

```bash
# Verificar Python
python --version  # Debe ser >= 3.10

# Verificar Claude Code
claude --version

# Verificar Git
git --version
```

---

## 📖 Historia de Usuario

```gherkin
# US-070: Reserva de un Recurso

Como cliente
Quiero reservar un recurso (ej. una mesa) en una fecha y horario determinados
Para asegurarme su disponibilidad sin superponerme con otra reserva
```

### Criterios de Aceptación

- Un cliente puede crear una reserva indicando recurso, fecha, horario y su nombre.
- El sistema rechaza una reserva si el recurso ya tiene otra reserva
  confirmada que se solape en fecha y horario.
- El sistema rechaza una reserva con fecha en el pasado.
- Un cliente puede consultar el estado de una reserva por su id.
- Consultar una reserva inexistente devuelve un error claro (404).

### Alcance

**Funcionalidades Principales:**
- Crear una reserva (`POST /reservas/`)
- Consultar una reserva por id (`GET /reservas/{id}`)
- Rechazar solapamientos del mismo recurso

**Componentes a Implementar (Bounded Context `reservas`):**
- AggregateRoot `Reserva`
- ValueObjects `FechaReserva` y `RangoHorario`
- DomainEvent `ReservaCreada`
- Port `ReservaRepository`
- CommandHandler `CrearReservaHandler`
- QueryHandler `ObtenerReservaHandler`
- Repository `ReservaRepositoryMemoria`
- ApiRouter con los 2 endpoints

**Casos de Uso:**
1. Un cliente reserva una mesa para una fecha y horario libres → se confirma.
2. Un cliente intenta reservar la misma mesa en un horario que se superpone
   con una reserva existente → se rechaza (409).
3. Un cliente consulta una reserva por id → recibe sus datos y estado.

**Fuera de alcance** (para mantener el tutorial en <60 min): cancelación
expuesta por API, persistencia real (SQL), autenticación, Event Sourcing
completo. El aggregate ya soporta `cancelar()`, pero conectarlo a un endpoint
queda como ejercicio en [Próximos Pasos](#próximos-pasos).

---

## 🚀 Setup del Proyecto

### 1. Crear Directorio del Proyecto

```bash
mkdir reservas-hexagonal
cd reservas-hexagonal
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
cat > requirements.txt << 'EOF'
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.4.0
pytest>=7.0.0
pytest-cov>=4.0.0
pytest-bdd>=6.0.0
httpx>=0.24.0
pylint>=2.15.0
radon>=5.1.0
EOF

pip install -r requirements.txt
```

### 5. Crear Estructura Base

El perfil `hexagonal-ddd-bc` organiza el código por Bounded Context. Creamos
de entrada el esqueleto completo del BC `reservas`:

```bash
mkdir -p src/reservas/domain/{aggregates,value_objects,events,ports}
mkdir -p src/reservas/application/{commands,queries}
mkdir -p src/reservas/infrastructure/repositories
mkdir -p src/reservas/api
mkdir -p tests/unit/reservas tests/integration/reservas
mkdir -p features/steps

# __init__.py en cada paquete
find src tests features -type d -exec touch {}/__init__.py \;
```

**Estructura del proyecto:**

```
reservas-hexagonal/
├── src/reservas/
│   ├── domain/                  ← Sin dependencias externas
│   │   ├── aggregates/
│   │   ├── value_objects/
│   │   ├── events/
│   │   └── ports/
│   ├── application/              ← Importa domain/, nunca infrastructure/
│   │   ├── commands/
│   │   └── queries/
│   ├── infrastructure/           ← Implementa los Ports
│   │   └── repositories/
│   └── api/                      ← Importa application/, nunca domain/
├── tests/
│   ├── unit/reservas/
│   └── integration/reservas/
├── features/
│   └── steps/
├── main.py
├── requirements.txt
└── pytest.ini
```

### 6. Crear pytest.ini

```ini
[pytest]
pythonpath = . src

testpaths = tests features/steps

python_files = test_*.py *_steps.py
python_classes = Test*
python_functions = test_*

markers =
    unit: Unit tests (domain/application)
    integration: Integration tests (infrastructure/api)
    bdd: BDD tests (pytest-bdd)
    US-070: BDD tag para la historia de usuario US-070

addopts =
    -v
    --tb=short
    --strict-markers
    --cov=src/reservas
    --cov-report=term-missing

bdd_features_base_dir = features/
```

> **📌 Nota:** `pythonpath = . src` es lo que permite importar `from
> reservas.domain...` en vez de `from src.reservas.domain...` — el código
> vive en `src/` pero se importa como si `src/` fuera la raíz. `pytest` lo
> resuelve solo; para correr `uvicorn` fuera de pytest vas a necesitar
> `PYTHONPATH=src` explícito (ver [Validación Final](#validación-final)).

---

## 📦 Instalación del Framework

### 1. Clonar Claude Dev Kit

```bash
cd ~
git clone https://github.com/vvalotto/claude-dev-kit.git ~/.claude-dev-kit
```

### 2. Ejecutar Instalador

```bash
cd reservas-hexagonal

python ~/.claude-dev-kit/install/installer.py --profile hexagonal-ddd-bc --yes
```

**Salida esperada:**

```
✅ Framework instalado exitosamente en .claude/
✅ Perfil 'hexagonal-ddd-bc' configurado
✅ Skills disponibles:
   - /implement-us
   - /track-pause, /track-resume, /track-status
✅ Templates instalados: bdd, planning, testing, reporting
```

### 3. Verificar Instalación

```bash
ls -la .claude/

# .claude/
# ├── skills/implement-us/
# ├── templates/
# ├── tracking/
# └── config.json
```

El `CLAUDE.md` generado en la raíz del proyecto va a incluir, para este
perfil, una sección **"Capas y Orden de Implementación"** con la tabla de
capas del BC y el orden obligatorio — es lo primero que conviene leer antes
de arrancar Fase 3.

---

## 🎬 Walkthrough: Las 10 Fases

### Preparación: Crear Archivo US

```bash
mkdir -p historias-usuario
cat > historias-usuario/US-070.md << 'EOF'
# US-070: Reserva de un Recurso

Como cliente
Quiero reservar un recurso (ej. una mesa) en una fecha y horario determinados
Para asegurarme su disponibilidad sin superponerme con otra reserva

## Criterios de Aceptación

- Un cliente puede crear una reserva indicando recurso, fecha, horario y su nombre.
- El sistema rechaza una reserva si el recurso ya tiene otra reserva confirmada
  que se solape en fecha y horario.
- El sistema rechaza una reserva con fecha en el pasado.
- Un cliente puede consultar el estado de una reserva por su id.
- Consultar una reserva inexistente devuelve un error claro (404).
EOF
```

### Ejecutar el Skill

```bash
# En Claude Code:
/implement-us US-070
```

---

### 🔍 Fase 0: Validación de Contexto

**Qué hace el framework:**
- ✅ Verifica que `historias-usuario/US-070.md` exista
- ✅ Lee el perfil `hexagonal-ddd-bc` desde `.claude/skills/implement-us/config.json`
- ✅ Genera `docs/plans/US-070-context.md` con las decisiones de ejecución
  (tipo de HU, si aplica BDD, fases a correr, umbrales de calidad)
- ⏱️ Inicializa el tracking de tiempo

**Output:**

```
✅ Historia de usuario encontrada: US-070
✅ Perfil cargado: hexagonal-ddd-bc
✅ Configuración:
   - Arquitectura: hexagonal (domain → application → infrastructure → api)
   - Bounded Context: reservas
   - Test Framework: pytest + httpx
   - Quality Gates: Pylint ≥ 8.0, Coverage ≥ 90% (domain/ + application/)
⏱️  Tracking iniciado para US-070
```

**¿Qué hacer si falla?**
- Verifica que `historias-usuario/US-070.md` exista
- Confirma que la instalación del framework fue exitosa (`ls .claude/`)
- Revisá `.claude/skills/implement-us/customizations/hexagonal-ddd-bc.json`

---

### 📝 Fase 1: Generación de Escenarios BDD

**Qué hace el framework:**
- 📄 Lee los criterios de aceptación de la HU
- 🤖 Genera escenarios Gherkin — para este perfil no hay un template BDD
  específico (`pyqt-mvc` y `fastapi-rest` sí lo tienen), así que usa el
  genérico `templates/bdd/scenario.feature` como referencia estructural
- 💾 Crea `tests/features/US-070-reserva-de-un-recurso.feature`

> **📌 Nota importante:** el `bdd_config` del perfil indica explícitamente
> **no usar `# language: es`** — `pytest-bdd` 8.x requiere keywords en inglés
> (`Given/When/Then/Feature/Scenario`). El *texto* de los escenarios sí puede
> estar en español; solo las palabras clave de Gherkin van en inglés.

**Ejemplo de Output (Reservas):**

```gherkin
@US-070
Feature: Reserva de un recurso (US-070)
  Como cliente
  Quiero reservar un recurso (ej. una mesa) en una fecha y horario
  Para asegurarme su disponibilidad

  Background:
    Given que la API está disponible

  Scenario: Crear una reserva exitosamente
    When se envía una petición POST a "/reservas/" con:
      | campo          | valor       |
      | recurso_id     | mesa-1      |
      | fecha          | manana      |
      | hora_inicio    | 10:00:00    |
      | hora_fin       | 11:00:00    |
      | cliente_nombre | Ana         |
    Then la respuesta tiene código de estado 201
    And la reserva creada puede consultarse y está "CONFIRMADA"

  Scenario: Rechazar una reserva solapada con otra existente
    Given que existe una reserva para "mesa-1" en "manana" de "10:00:00" a "11:00:00"
    When se envía una petición POST a "/reservas/" con:
      | campo          | valor       |
      | recurso_id     | mesa-1      |
      | fecha          | manana      |
      | hora_inicio    | 10:30:00    |
      | hora_fin       | 11:30:00    |
      | cliente_nombre | Bruno       |
    Then la respuesta tiene código de estado 409
```

El feature completo (5 escenarios) está en
[`features/reservas.feature`](../../examples/code/reservas-hexagonal/features/reservas.feature).

**Interacción:**
- Claude te muestra los escenarios generados
- Podés pedir ajustes antes de continuar (ej. agregar un escenario de
  fecha pasada, como en el ejemplo real)
- Checkpoint: `[aprobado]` requerido antes de avanzar a Fase 2

---

### 📐 Fase 2: Plan de Implementación

**Qué hace el framework:**
- 🏗️ Lee `component_structure.bc_feature.implementation_order` del perfil:
  `ValueObjects → DomainEvents → AggregateRoot → Ports → CommandHandlers →
  QueryHandlers → Repositories → ApiRouter`
- 📊 Genera un plan de tareas en ese orden exacto — **no es negociable**: cada
  elemento depende del anterior
- 🎯 Identifica las rutas canónicas de cada componente según
  `component_path.by_component` del perfil

**Decisiones Clave del ejemplo:**
- Orden de implementación: el mismo que dicta el perfil
- Componentes principales: `Reserva` (Aggregate), `FechaReserva` +
  `RangoHorario` (ValueObjects), `ReservaCreada` (DomainEvent),
  `ReservaRepository` (Port), `CrearReservaHandler` (Command),
  `ObtenerReservaHandler` (Query), `ReservaRepositoryMemoria` (Repository)
- Decisión de diseño no trivial: **repositorio en memoria en vez de SQL** —
  mantiene el foco en la arquitectura hexagonal; el `Port` es lo importante,
  no el motor de persistencia (documentado en
  [`docs/reporting/US-070-report.md`](../../examples/code/reservas-hexagonal/docs/reporting/US-070-report.md))

**Archivo creado:**
```
docs/plans/US-070-plan.md
```

Podés ver el plan completo del ejemplo en
[`docs/planning/US-070-plan.md`](../../examples/code/reservas-hexagonal/docs/planning/US-070-plan.md)
(en el proyecto de ejemplo vive en `docs/planning/` en vez de `docs/plans/`
para no pisar el `docs/plans/` real de este repositorio del framework — en tu
propio proyecto, seguí la ruta canónica `docs/plans/{US_ID}-plan.md`).

---

### ⚙️ Fase 3: Implementación

**Qué hace el framework:**
- 💻 Guía la creación de cada componente **en el orden obligatorio**
- 🔧 Valida en cada paso la regla de dependencia: `domain/` no importa nada
  fuera de su propio `domain/`
- 📁 Crea archivos en las rutas de `component_path.by_component`

#### Paso 1-2: ValueObjects

```python
# src/reservas/domain/value_objects/fecha_reserva.py
from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class FechaReserva:
    """Fecha en la que se realiza una reserva.

    Inmutable y con validación propia: no acepta fechas pasadas.
    """

    valor: date

    def __post_init__(self) -> None:
        if self.valor < date.today():
            raise ValueError("La fecha de reserva no puede ser en el pasado")
```

```python
# src/reservas/domain/value_objects/rango_horario.py
@dataclass(frozen=True)
class RangoHorario:
    """Rango horario de una reserva. Valida hora_fin > hora_inicio."""

    hora_inicio: time
    hora_fin: time

    def __post_init__(self) -> None:
        if self.hora_fin <= self.hora_inicio:
            raise ValueError("La hora de fin debe ser posterior a la hora de inicio")

    def se_solapa_con(self, otro: "RangoHorario") -> bool:
        return self.hora_inicio < otro.hora_fin and otro.hora_inicio < self.hora_fin
```

Notá que `se_solapa_con()` vive en el ValueObject: es pura geometría de
intervalos, no conoce nada de reservas ni de persistencia — así se mantiene
100% testeable en aislamiento.

#### Paso 3: DomainEvent

```python
# src/reservas/domain/events/reserva_creada.py
@dataclass(frozen=True)
class ReservaCreada:
    """Describe que una reserva fue creada en el dominio."""

    reserva_id: str
    recurso_id: str
    fecha: date
    hora_inicio: time
    hora_fin: time
    ocurrido_en: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
```

#### Paso 4: AggregateRoot

```python
# src/reservas/domain/aggregates/reserva.py
class Reserva:
    """Aggregate Root: encapsula las invariantes de una reserva."""

    @classmethod
    def crear(cls, recurso_id, fecha, horario, cliente_nombre) -> "Reserva":
        reserva = cls(reserva_id=str(uuid.uuid4()), recurso_id=recurso_id,
                      fecha=fecha, horario=horario, cliente_nombre=cliente_nombre)
        reserva._eventos.append(ReservaCreada(
            reserva_id=reserva.id, recurso_id=recurso_id,
            fecha=fecha.valor, hora_inicio=horario.hora_inicio,
            hora_fin=horario.hora_fin,
        ))
        return reserva

    def se_solapa_con(self, fecha: FechaReserva, horario: RangoHorario) -> bool:
        return self.fecha == fecha and self.horario.se_solapa_con(horario)
```

El aggregate delega la comparación de solapamiento al ValueObject
(`self.horario.se_solapa_con(horario)`) — el aggregate solo decide **cuándo**
aplica esa comparación (misma fecha), no **cómo** se calcula.

#### Paso 5: Port

```python
# src/reservas/domain/ports/reserva_repository.py
class ReservaRepository(ABC):
    """Contrato de persistencia. Solo métodos abstractos."""

    @abstractmethod
    def guardar(self, reserva: Reserva) -> None: ...

    @abstractmethod
    def obtener_por_id(self, reserva_id: str) -> Optional[Reserva]: ...

    @abstractmethod
    def existe_solapamiento(self, recurso_id, fecha, horario) -> bool: ...
```

Este es el límite exacto del hexágono para este BC: todo lo que está antes
(`domain/`) no sabe que existe una base de datos; todo lo que está después
(`infrastructure/`) implementa este contrato sin saber de reglas de negocio.

#### Paso 6: CommandHandler

```python
# src/reservas/application/commands/crear_reserva_handler.py
class CrearReservaHandler:
    """Sin lógica de negocio propia — delega al aggregate."""

    def handle(self, comando: CrearReservaComando) -> str:
        fecha = FechaReserva(comando.fecha)
        horario = RangoHorario(comando.hora_inicio, comando.hora_fin)

        if self._repository.existe_solapamiento(comando.recurso_id, fecha, horario):
            raise ReservaSolapadaError(...)

        reserva = Reserva.crear(recurso_id=comando.recurso_id, fecha=fecha,
                                 horario=horario, cliente_nombre=comando.cliente_nombre)
        self._repository.guardar(reserva)
        return reserva.id
```

#### Paso 7: QueryHandler

```python
# src/reservas/application/queries/obtener_reserva_handler.py
class ObtenerReservaHandler:
    """Lee del repositorio y traduce a DTO. Sin side effects."""

    def handle(self, query: ObtenerReservaQuery) -> Optional[ReservaDTO]:
        reserva = self._repository.obtener_por_id(query.reserva_id)
        if reserva is None:
            return None
        return ReservaDTO(id=reserva.id, recurso_id=reserva.recurso_id, ...)
```

Notá que devuelve un `ReservaDTO`, no el `Reserva` (aggregate) directamente —
`api/` nunca debería recibir un objeto de dominio.

#### Paso 8: Repository (Infrastructure)

```python
# src/reservas/infrastructure/repositories/reserva_repository_memoria.py
class ReservaRepositoryMemoria(ReservaRepository):
    """Implementa el puerto con un diccionario en memoria."""

    def existe_solapamiento(self, recurso_id, fecha, horario) -> bool:
        return any(
            r.recurso_id == recurso_id
            and r.estado == EstadoReserva.CONFIRMADA
            and r.se_solapa_con(fecha, horario)
            for r in self._reservas.values()
        )
```

#### Paso 9: ApiRouter

```python
# src/reservas/api/router.py
@router.post("/", status_code=201)
def crear_reserva(request: CrearReservaRequest, repository: RepositoryDep) -> dict:
    handler = CrearReservaHandler(repository)
    try:
        reserva_id = handler.handle(CrearReservaComando(...))
    except ReservaSolapadaError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    return {"id": reserva_id}
```

El router traduce las excepciones de dominio/aplicación a códigos HTTP
(`ReservaSolapadaError` → 409, `ValueError` de invariante → 422) — es la
única capa que conoce HTTP.

**Archivos creados:**
```
src/reservas/domain/value_objects/fecha_reserva.py
src/reservas/domain/value_objects/rango_horario.py
src/reservas/domain/events/reserva_creada.py
src/reservas/domain/aggregates/reserva.py
src/reservas/domain/ports/reserva_repository.py
src/reservas/domain/errors.py
src/reservas/application/commands/crear_reserva_handler.py
src/reservas/application/queries/obtener_reserva_handler.py
src/reservas/infrastructure/repositories/reserva_repository_memoria.py
src/reservas/api/router.py
main.py
```

**Características del Código:**
- ✅ Sigue estrictamente `domain → application → infrastructure → api`
- ✅ Type hints completos en todas las firmas
- ✅ Cero imports de `infrastructure/` o `api/` dentro de `domain/`
- ✅ Preparado para testing (repositorio inyectado, no global oculto)

---

### 🧪 Fase 4: Tests Unitarios

**Qué hace el framework:**
- 🔬 Genera tests unitarios sobre `domain/` y `application/` (el scope que
  cuenta para el quality gate de coverage de este perfil)
- 🎯 Un test double liviano (`ReservaRepositoryMemoria`) sirve como
  repositorio de test para los Handlers — no hace falta mockear framework

**Ejemplo de Test (ValueObject):**

```python
# tests/unit/reservas/test_rango_horario.py
class TestSolapamiento:
    def test_rangos_parcialmente_superpuestos_se_solapan(self):
        rango = RangoHorario(time(10, 0), time(11, 0))
        assert rango.se_solapa_con(RangoHorario(time(10, 30), time(12, 0))) is True

    def test_rangos_consecutivos_no_se_solapan(self):
        rango = RangoHorario(time(10, 0), time(11, 0))
        assert rango.se_solapa_con(RangoHorario(time(11, 0), time(12, 0))) is False
```

**Ejemplo de Test (CommandHandler con invariante de negocio):**

```python
# tests/unit/reservas/test_crear_reserva_handler.py
def test_rechaza_solapamiento_mismo_recurso_y_horario(self, repository):
    handler = CrearReservaHandler(repository)
    handler.handle(_comando())

    with pytest.raises(ReservaSolapadaError):
        handler.handle(_comando(cliente_nombre="Otro cliente"))
```

**Ejecución:**

```bash
pytest tests/unit/ -v --cov=src/reservas/domain --cov=src/reservas/application --cov-report=term-missing
```

**Output Esperado:**

```
tests/unit/reservas/test_crear_reserva_handler.py ....                 [ ... ]
tests/unit/reservas/test_fecha_reserva.py .....                        [ ... ]
tests/unit/reservas/test_obtener_reserva_handler.py ..                 [ ... ]
tests/unit/reservas/test_rango_horario.py .......                     [ ... ]
tests/unit/reservas/test_reserva.py .........                         [ ... ]

25 passed in 0.XXs

Name                                                            Stmts   Miss  Cover
---------------------------------------------------------------------------------
src/reservas/domain/aggregates/reserva.py                          35      0   100%
src/reservas/domain/value_objects/fecha_reserva.py                 12      0   100%
src/reservas/domain/value_objects/rango_horario.py                 13      0   100%
src/reservas/application/commands/crear_reserva_handler.py         26      0   100%
src/reservas/application/queries/obtener_reserva_handler.py        25      0   100%
---------------------------------------------------------------------------------
TOTAL                                                              100+     0   100%
```

**Archivos creados:**
```
tests/unit/reservas/test_fecha_reserva.py
tests/unit/reservas/test_rango_horario.py
tests/unit/reservas/test_reserva.py
tests/unit/reservas/test_crear_reserva_handler.py
tests/unit/reservas/test_obtener_reserva_handler.py
```

---

### 🔗 Fase 5: Tests de Integración

**Qué hace el framework:**
- 🌐 Genera tests que validan `infrastructure/` (Repository real, no un
  test double) y `api/` end-to-end (request HTTP real vía `TestClient`)
- 🎭 Usa `dependency_overrides` de FastAPI para inyectar un repositorio en
  memoria aislado por test — mismo patrón que usan los ejemplos
  `fastapi-rest` de este repositorio

**Ejemplo de Test (Repository real):**

```python
# tests/integration/reservas/test_reserva_repository_memoria.py
def test_existe_solapamiento_ignora_reservas_canceladas(self, repository):
    """Una reserva cancelada no debe bloquear el mismo horario."""
    reserva = Reserva.crear(recurso_id="mesa-1", fecha=_fecha_futura(),
                             horario=RangoHorario(time(10, 0), time(11, 0)),
                             cliente_nombre="Ana")
    reserva.cancelar()
    repository.guardar(reserva)

    assert repository.existe_solapamiento(
        "mesa-1", _fecha_futura(), RangoHorario(time(10, 0), time(11, 0))
    ) is False
```

**Ejemplo de Test (API end-to-end):**

```python
# tests/integration/reservas/test_api_reservas.py
@pytest.fixture
def client():
    repository = ReservaRepositoryMemoria()
    app.dependency_overrides[get_repository] = lambda: repository
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_crear_reserva_solapada_devuelve_409(self, client):
    client.post("/reservas/", json=_payload())
    respuesta = client.post("/reservas/", json=_payload(cliente_nombre="Otro"))
    assert respuesta.status_code == 409
```

**Ejecución:**

```bash
pytest tests/integration/ -v
```

**Archivos creados:**
```
tests/integration/reservas/test_reserva_repository_memoria.py
tests/integration/reservas/test_api_reservas.py
```

---

### ✅ Fase 6: Validación BDD

**Qué hace el framework:**
- 🥒 Genera step definitions para el `.feature` de Fase 1, con keywords en
  inglés (`given/when/then` de `pytest_bdd`) y texto en español
- 🔗 Reutiliza el mismo patrón de `client` + `dependency_overrides` de Fase 5

**Ejemplo de Step Definitions:**

```python
# features/steps/reserva_steps.py
FEATURE_FILE = os.path.join(os.path.dirname(__file__), "..", "reservas.feature")
scenarios(FEATURE_FILE)

_FECHAS_RELATIVAS = {
    "hoy": lambda: date.today(),
    "manana": lambda: date.today() + timedelta(days=1),
    "ayer": lambda: date.today() - timedelta(days=1),
}


@given(
    parsers.parse(
        'que existe una reserva para "{recurso_id}" en "{fecha}" '
        'de "{hora_inicio}" a "{hora_fin}"'
    )
)
def existe_reserva(client, recurso_id, fecha, hora_inicio, hora_fin):
    respuesta = client.post("/reservas/", json={
        "recurso_id": recurso_id, "fecha": _resolver_fecha(fecha),
        "hora_inicio": hora_inicio, "hora_fin": hora_fin,
        "cliente_nombre": "Cliente Previo",
    })
    assert respuesta.status_code == 201


@then(parsers.parse("la respuesta tiene código de estado {status:d}"))
def verificar_status(context, status):
    assert context["response"].status_code == status
```

> **📌 Nota:** los alias `"manana"`/`"ayer"` en las tablas Gherkin se resuelven
> a fechas ISO concretas en el step — así el `.feature` no queda con fechas
> hardcodeadas que expiran.

**Ejecución:**

```bash
pytest features/steps/ -v
```

**Output Esperado:**

```
features/steps/reserva_steps.py::test_crear_una_reserva_exitosamente PASSED
features/steps/reserva_steps.py::test_rechazar_una_reserva_solapada_con_otra_existente PASSED
features/steps/reserva_steps.py::test_permitir_reservar_el_mismo_recurso_en_un_horario_distinto PASSED
features/steps/reserva_steps.py::test_rechazar_una_reserva_con_fecha_pasada PASSED
features/steps/reserva_steps.py::test_consultar_una_reserva_inexistente PASSED

5 passed
```

**Archivos creados:**
```
features/reservas.feature
features/steps/reserva_steps.py
```

---

### 📊 Fase 7: Quality Gates

**Qué hace el framework:**
- 🔍 Ejecuta Pylint sobre el scope del perfil: `domain/` + `application/`
  (no todo `src/`)
- 📈 Calcula complejidad ciclomática con `radon` (vía CodeGuard)
- 📊 Verifica cobertura ≥ 90% sobre ese mismo scope

**Umbrales (hexagonal-ddd-bc):**

| Métrica | Umbral | Scope |
|---|---|---|
| Pylint | ≥ 8.0 | `domain/` + `application/` |
| Complejidad ciclomática | ≤ 10 por función | Todo el BC |
| Coverage | ≥ 90% | `domain/` + `application/` |

**Ejecución:**

```bash
# Pylint (scope del perfil)
PYTHONPATH=src pylint src/reservas/domain src/reservas/application

# Complejidad
radon cc src/reservas -a

# Cobertura (ya calculada en Fase 4/5, se re-verifica acá contra el umbral)
pytest --cov=src/reservas/domain --cov=src/reservas/application --cov-fail-under=90
```

**Output Esperado:**

```
Your code has been rated at 9.60/10

42 blocks (classes, functions, methods) analyzed.
Average complexity: A (1.62)

TOTAL   100%   Required test coverage of 90% reached.
```

**¿Qué hacer si fallan?**
- Pylint bajo 8.0: revisá `too-many-arguments`/`too-many-branches` — suele
  indicar que una responsabilidad de aplicación se filtró al aggregate
- Coverage bajo 90%: casi siempre falta un test de una rama de validación
  (`__post_init__` de un ValueObject, o un `raise` del handler)
- CC > 10: extraé un método privado del aggregate o handler afectado

En el ejemplo real, el resultado fue **9.60/10** de Pylint y **100%** de
coverage en `domain/` + `application/` — ver el detalle completo en
[`VALIDATION-REPORT.md`](../../examples/code/reservas-hexagonal/VALIDATION-REPORT.md).

---

### 📚 Fase 8: Documentación

**Qué hace el framework:**
- 📖 Actualiza el plan de implementación marcando las tareas completadas
- 🗂️ Registra decisiones de diseño no triviales (ej. por qué repositorio en
  memoria y no SQL)
- 💡 Deja documentado qué queda fuera de alcance para una futura HU

**Archivos actualizados/creados:**

```
docs/plans/US-070-plan.md        (checkboxes marcados)
docs/reports/US-070-report.md    (generado en Fase 9, ver abajo)
```

**Ejemplo de Decisión Documentada:**

> **Invariante de solapamiento resuelta en dos capas**: el ValueObject
> `RangoHorario.se_solapa_con()` resuelve la geometría del solapamiento (sin
> conocer nada de persistencia); el `CommandHandler` orquesta la consulta al
> repositorio y decide si rechazar el comando — así `domain/` no depende de
> infraestructura para su propia lógica de comparación.

---

### 📈 Fase 9: Reporte Final

**Qué hace el framework:**
- 📋 Consolida métricas de todas las fases anteriores
- ⏱️ Reporta tiempo real vs. estimado (vía tracking)
- ✅ Lista los 5 criterios de aceptación y su estado
- 📊 Genera el reporte de cierre de la HU

**Archivo creado:**

```
docs/reports/US-070-report.md
```

**Reporte del ejemplo real** (resumen — ver el completo en
[`docs/reporting/US-070-report.md`](../../examples/code/reservas-hexagonal/docs/reporting/US-070-report.md)):

```markdown
# US-070: Reserva de un Recurso — Reporte Final

## Tests
| Suite | Cantidad | Resultado |
|---|---|---|
| Unitarios | 25 | ✅ Todos pasan |
| Integración | 7 | ✅ Todos pasan |
| BDD | 5 escenarios | ✅ Todos pasan |

## Quality Gates
| Métrica | Umbral | Resultado | Estado |
|---|---|---|---|
| Pylint (domain/+application/) | ≥ 8.0 | 9.60/10 | ✅ APROBADO |
| Coverage (domain/+application/) | ≥ 90% | 100% | ✅ APROBADO |
| CC máx. por función | ≤ 10 | A (máx. 3) | ✅ APROBADO |

**Estado final: APROBADO**
```

**Tracking de Tiempo:**

```bash
/track-report US-070
```

---

## ✅ Validación Final

### Checklist Completo

**Código:**
- [x] 8 componentes del BC implementados en el orden obligatorio
- [x] `domain/` sin ningún import de `infrastructure/` o `api/`
- [x] Type hints y docstrings en todos los componentes

**Tests:**
- [x] 25 tests unitarios — 100% passing
- [x] 7 tests de integración — 100% passing
- [x] 5 escenarios BDD — 100% passing

**Calidad:**
- [x] Pylint 9.60/10 (umbral: 8.0)
- [x] Complejidad Ciclomática: A en todo el BC (umbral: ≤10)
- [x] Coverage 100% en domain/+application/ (umbral: 90%)

**Documentación:**
- [x] Plan de implementación con checklist
- [x] Reporte final con decisiones documentadas
- [x] README con ejemplos de uso vía `curl`

### Ejecutar Aplicación

Cloná o navegá al proyecto de ejemplo completo:

```bash
cd examples/code/reservas-hexagonal
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# PYTHONPATH=src es necesario porque el código vive en src/reservas/
# (pytest lo resuelve solo vía pytest.ini; uvicorn no)
PYTHONPATH=src uvicorn main:app --reload
```

La API queda disponible en `http://localhost:8000` (Swagger UI en `/docs`).

### Verificación Manual

```bash
# Crear una reserva
curl -X POST http://localhost:8000/reservas/ \
  -H "Content-Type: application/json" \
  -d '{
    "recurso_id": "mesa-1",
    "fecha": "2026-12-24",
    "hora_inicio": "20:00:00",
    "hora_fin": "22:00:00",
    "cliente_nombre": "Ana"
  }'
# → 201 {"id": "..."}

# Consultarla
curl http://localhost:8000/reservas/{id}
# → 200 {"id": "...", "recurso_id": "mesa-1", "estado": "CONFIRMADA", ...}

# Intentar una reserva solapada
curl -X POST http://localhost:8000/reservas/ \
  -H "Content-Type: application/json" \
  -d '{
    "recurso_id": "mesa-1",
    "fecha": "2026-12-24",
    "hora_inicio": "20:30:00",
    "hora_fin": "21:30:00",
    "cliente_nombre": "Bruno"
  }'
# → 409 {"detail": "Ya existe una reserva para mesa-1 el 2026-12-24 en el horario 20:00:00-22:00:00"}
```

Corré la suite completa para confirmar los 39 tests en verde:

```bash
pytest
```

---

## 🔧 Troubleshooting

### Problema: El skill /implement-us no se encuentra

**Solución:**
```bash
ls -la .claude/skills/implement-us/
python ~/.claude-dev-kit/install/installer.py --profile hexagonal-ddd-bc --yes
```

### Problema: `ModuleNotFoundError: No module named 'reservas'`

**Causa:** el código vive en `src/reservas/`, pero el comando que ejecutaste
no tiene `src/` en el `PYTHONPATH`. `pytest` lo resuelve solo (vía
`pythonpath = . src` en `pytest.ini`); `uvicorn` no.

**Solución:**
```bash
PYTHONPATH=src uvicorn main:app --reload
```

### Problema: pytest falla con `'US-070' not found in markers configuration option`

**Causa:** `pytest-bdd` convierte los tags de Gherkin (`@US-070`) en markers
de pytest, y `--strict-markers` exige que estén registrados.

**Solución:** agregá el marker a `pytest.ini`:
```ini
markers =
    ...
    US-070: BDD tag para la historia de usuario US-070
```

### Problema: pytest-bdd falla con error de keywords en español

**Causa:** el perfil `hexagonal-ddd-bc` indica explícitamente **no usar**
`# language: es` en los `.feature` — `pytest-bdd` 8.x requiere keywords en
inglés (`Given/When/Then/Feature/Scenario/Background`). Es distinto a los
perfiles `pyqt-mvc`/`fastapi-rest`, que sí soportan `# language: es`.

**Solución:** usá keywords en inglés y texto en el idioma que prefieras:
```gherkin
Feature: Reserva de un recurso (US-070)
  Given que la API está disponible
  When se envía una petición POST a "/reservas/"
  Then la respuesta tiene código de estado 201
```

### Problema: Quality gates fallan (Pylint < 8.0)

**Solución:**
```bash
# Ver issues específicos (solo el scope del perfil)
PYTHONPATH=src pylint src/reservas/domain src/reservas/application --reports=y
```
Los hallazgos más comunes en este perfil son `too-many-arguments` en
aggregates con muchos atributos y `too-few-public-methods` en Handlers — son
esperables en el patrón Command/QueryHandler (que expone un solo método
`handle()`) y no bloquean si el score global sigue ≥8.0.

### Problema: Errores de dependencias

**Solución:**
```bash
pip install --upgrade -r requirements.txt
pip list | grep -E "fastapi|pytest-bdd"
```

---

## 🚀 Próximos Pasos

### Ampliar el Bounded Context

1. **Exponer `cancelar()` vía API:** el aggregate ya soporta cancelación —
   falta un `CancelarReservaHandler` (CommandHandler) y el endpoint
   `DELETE /reservas/{id}` en el router.

2. **Agregar un QueryHandler de listado:** `ListarReservasPorRecursoHandler`,
   siguiendo el mismo patrón de `ObtenerReservaHandler` pero devolviendo una
   lista de DTOs.

3. **Persistencia real:** implementar un segundo adaptador del Port
   `ReservaRepository` (ej. `ReservaRepositorySQLAlchemy`) sin tocar
   `domain/` ni `application/` — es la prueba de que el hexágono está bien
   armado.

### Agregar un Segundo Bounded Context

El perfil está pensado para escalar a múltiples BCs. Si agregás, por
ejemplo, un BC `recursos` (para dar de alta las mesas/salas reservables),
la comunicación entre `reservas` y `recursos` debe pasar **solo por
puertos** (`domain/ports/`) — nunca imports directos entre BCs. El
Anti-Corruption Layer, si hace falta, vive en `infrastructure/` del BC
consumidor.

### Explorar Otros Perfiles del Framework

- **clean-architecture-bc:** misma filosofía BC-first, con capas Clean
  Architecture (`entities → use_cases → interface_adapters → frameworks`) en
  vez de hexagonal — ver el tutorial
  [`clean-architecture-bc-project.md`](clean-architecture-bc-project.md)
- **fastapi-rest:** arquitectura por capas tradicional (no BC-first), para
  APIs sin necesidad de aislar múltiples dominios
- **pyqt-mvc:** aplicaciones de escritorio

```bash
python ~/.claude-dev-kit/install/installer.py --profile clean-architecture-bc --yes
```

---

## 📚 Recursos

### Código Fuente del Ejemplo

- [`examples/code/reservas-hexagonal/`](../../examples/code/reservas-hexagonal/) — proyecto completo
- [Historia de usuario](../../examples/code/reservas-hexagonal/historias-usuario/US-070.md)
- [Plan de implementación](../../examples/code/reservas-hexagonal/docs/planning/US-070-plan.md)
- [Reporte final](../../examples/code/reservas-hexagonal/docs/reporting/US-070-report.md)
- [Reporte de validación](../../examples/code/reservas-hexagonal/VALIDATION-REPORT.md)

### Documentación del Framework

- [Documentación del skill implement-us](../skills/implement-us/index.md)
- [Mapa de artefactos](../../skills/implement-us/artifacts.md)
- [Customization del perfil hexagonal-ddd-bc](../../skills/implement-us/customizations/hexagonal-ddd-bc.json)
- [Guía de instalación](../user/installation.md)

### Documentación de DDD y Arquitectura Hexagonal

- [Ports and Adapters (Alistair Cockburn)](https://alistair.cockburn.us/hexagonal-architecture/)
- [Domain-Driven Design Reference (Eric Evans)](https://www.domainlanguage.com/ddd/reference/)

### Comunidad

- GitHub: https://github.com/vvalotto/claude-dev-kit
- Issues: https://github.com/vvalotto/claude-dev-kit/issues

---

## 📝 Conclusión

¡Felicidades! Completaste tu primer Bounded Context usando el Claude Dev Kit
con el perfil **hexagonal-ddd-bc**.

**Lo que aprendiste:**
- ✅ El orden de implementación obligatorio de DDD y por qué existe (cada
  pieza depende genuinamente de la anterior)
- ✅ Cómo mantener `domain/` libre de dependencias externas mientras
  expresás una invariante de negocio real
- ✅ Cómo estructurar tests por capa: unitarios sobre domain/application,
  integración sobre infrastructure/api, BDD sobre el flujo completo
- ✅ Cómo el `CLAUDE.md` autogenerado documenta capas y orden para vos y para
  Claude Code en sesiones futuras

**Siguiente paso:** aplicá este mismo patrón a tu propio dominio. Si tu
proyecto tiene más de un Bounded Context, este perfil escala naturalmente —
cada BC nuevo repite la misma estructura interna, comunicándose con los
demás solo a través de puertos.

---

**Tutorial Creado:** 2026-09-05
**Claude Dev Kit:** v1.6.0
**Perfil:** hexagonal-ddd-bc
