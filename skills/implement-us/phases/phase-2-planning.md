# Fase 2: Generación del Plan de Implementación

**Objetivo:** Crear un plan detallado de implementación basado en la arquitectura configurada del proyecto.

**Duración estimada:** 15-20 minutos

---

## Tracking

**Al inicio de la fase:**
```python
tracker.start_phase(2, "Generación del Plan de Implementación")
```

---

## Acción

Crear plan detallado basado en el patrón arquitectónico configurado (`{ARCHITECTURE_PATTERN}`).

**Template:** `.claude/templates/implementation-plan.md`

---

## Pasos de Generación del Plan

### 1. Identificar componentes a crear según arquitectura

Leer del archivo de configuración `.claude/skills/implement-us/config.json` la estructura de componentes:

```json
{
  "architecture_pattern": "{ARCHITECTURE_PATTERN}",
  "component_structure": {
    "layers": ["layer1", "layer2", "layer3"],
    "base_path": "{COMPONENT_PATH}"
  }
}
```

> **Componentes según patrón:**
>
> **MVC (PyQt, Desktop UI):**
> - Modelo (dataclass inmutable, lógica de negocio)
> - Vista (interfaz gráfica, QWidget)
> - Controlador (mediador entre modelo y vista)
> - Dependencias: Factory, Coordinator (si aplica)
>
> **MVT (Django, Web):**
> - Model (Django ORM, base de datos)
> - View (lógica de negocio, class-based views)
> - Template (HTML con template language)
> - Dependencias: Managers, Forms, Serializers (si aplica)
>
> **Layered (FastAPI, Backend API):**
> - Schema (Pydantic models para validación)
> - Service (lógica de negocio)
> - Repository (acceso a datos)
> - Router (endpoints HTTP)
> - Dependencias: Dependency Injection
>
> **Generic (Python genérico):**
> - Module (módulo principal)
> - Utils (utilidades si son necesarias)
> - Dependencias: Según necesidad del proyecto

### 2. Identificar dependencias y puntos de integración

- Componentes externos que la US necesita consumir
- Servicios o módulos existentes que deben integrarse
- Patrones del proyecto que deben aplicarse

### 3. Generar checklist de tareas

Organizar en secciones:
1. **Componentes principales** (según patrón arquitectónico)
2. **Integración** (conexión con componentes existentes)
3. **Tests** (unitarios, integración, BDD)
4. **Validación** (quality gates)

### 4. Estimar tiempo por tarea

Usar estimaciones estándar según tipo de componente y complejidad de la US.

---

## Ejemplos de Output por Stack

### Ejemplo 1: PyQt/MVC - Panel UI

```markdown
# Plan de Implementación: US-001 - Mostrar información de estado

**Patrón:** MVC
**Producto:** ux_monitor
**Estimación Total:** 2h 15min

## Componentes a Implementar

### 1. Panel Estado (MVC)
- [ ] app/presentacion/paneles/estado/modelo.py (10 min)
  - EstadoModelo: dataclass inmutable con datos del estado
  - Hereda de ModeloBase
- [ ] app/presentacion/paneles/estado/vista.py (20 min)
  - EstadoVista: QWidget con layout y labels
  - Hereda de QWidget
- [ ] app/presentacion/paneles/estado/controlador.py (15 min)
  - EstadoControlador: mediador entre modelo y vista
  - Maneja eventos y actualización de vista

### 2. Integración con Comunicación
- [ ] Conectar ServicioDatos → EstadoControlador (10 min)
  - Suscripción a actualizaciones de datos
  - Callback para actualizar modelo

### 3. Factory y Coordinator
- [ ] Registrar en Factory (5 min)
  - Agregar EstadoControlador a factory_paneles.py
- [ ] Integrar con Coordinator (5 min)
  - Agregar panel a main_coordinator.py

### 4. Tests
- [ ] tests/test_estado_modelo.py (15 min)
- [ ] tests/test_estado_vista.py (20 min)
- [ ] tests/test_estado_controlador.py (20 min)
- [ ] tests/test_estado_integracion.py (15 min)

### 5. Validación
- [ ] Ejecutar escenarios BDD (5 min)
- [ ] Quality gates (Pylint, CC, MI) (5 min)

**Estado:** 0/12 tareas completadas
```

### Ejemplo 2: FastAPI - Endpoint REST

```markdown
# Plan de Implementación: US-002 - Endpoint de consulta de usuarios

**Patrón:** Layered Architecture
**Producto:** api_users
**Estimación Total:** 1h 45min

## Componentes a Implementar

### 1. User Endpoint (Layered)
- [ ] app/domain/schemas/user_schema.py (10 min)
  - UserResponse: Pydantic model para respuesta
  - UserFilter: Pydantic model para filtros
- [ ] app/services/user_service.py (20 min)
  - UserService: lógica de negocio
  - Método get_users(filter: UserFilter)
- [ ] app/repositories/user_repository.py (15 min)
  - UserRepository: acceso a datos
  - Query con filtros dinámicos
- [ ] app/api/v1/routers/users.py (15 min)
  - GET /users endpoint
  - Dependency injection de UserService

### 2. Integración
- [ ] Configurar dependency injection (10 min)
  - Registrar UserService en dependencies.py
  - Configurar repository con session de BD

### 3. Tests
- [ ] tests/unit/test_user_service.py (15 min)
- [ ] tests/integration/test_user_repository.py (15 min)
- [ ] tests/api/test_users_endpoint.py (20 min)

### 4. Validación
- [ ] Ejecutar escenarios BDD (5 min)
- [ ] Quality gates (Pylint, coverage) (5 min)

**Estado:** 0/10 tareas completadas
```

### Ejemplo 3: Django - Vista y Modelo

```markdown
# Plan de Implementación: US-003 - Formulario de registro

**Patrón:** MVT
**Producto:** web_auth
**Estimación Total:** 2h 00min

## Componentes a Implementar

### 1. User Registration (MVT)
- [ ] users/models.py (15 min)
  - Ampliar modelo User con campos adicionales
  - Agregar custom manager si es necesario
- [ ] users/views.py (20 min)
  - RegistrationView: CreateView para registro
  - Validación de datos
- [ ] users/forms.py (15 min)
  - RegistrationForm: ModelForm con validaciones
- [ ] users/templates/users/register.html (20 min)
  - Template con formulario de registro
  - Manejo de errores y mensajes

### 2. Integración
- [ ] Configurar URLs (5 min)
  - Agregar ruta en users/urls.py
- [ ] Configurar signals (10 min)
  - Signal post-registro para email de bienvenida

### 3. Tests
- [ ] tests/test_user_model.py (10 min)
- [ ] tests/test_registration_form.py (15 min)
- [ ] tests/test_registration_view.py (20 min)

### 4. Validación
- [ ] Ejecutar escenarios BDD (5 min)
- [ ] Quality gates (Pylint, coverage) (5 min)

**Estado:** 0/10 tareas completadas
```

### Ejemplo 4: Generic Python - Módulo de Procesamiento

```markdown
# Plan de Implementación: US-004 - Procesador de datos

**Patrón:** Generic
**Producto:** data_processor
**Estimación Total:** 1h 30min

## Componentes a Implementar

### 1. Data Processor Module
- [ ] src/processor/validator.py (15 min)
  - Clase DataValidator
  - Métodos de validación de datos de entrada
- [ ] src/processor/transformer.py (20 min)
  - Clase DataTransformer
  - Lógica de transformación de datos
- [ ] src/processor/processor.py (15 min)
  - Clase DataProcessor (orquestador)
  - Integra validator y transformer

### 2. Utilidades
- [ ] src/processor/exceptions.py (10 min)
  - Excepciones custom para errores de procesamiento

### 3. Tests
- [ ] tests/test_validator.py (15 min)
- [ ] tests/test_transformer.py (15 min)
- [ ] tests/test_processor.py (20 min)

### 4. Validación
- [ ] Ejecutar escenarios BDD (5 min)
- [ ] Quality gates (Pylint, coverage) (5 min)

**Estado:** 0/8 tareas completadas
```

---

## Template de Output

El plan generado debe seguir esta estructura:

```markdown
# Plan de Implementación: {US_ID} - {US_TITLE}

**Patrón:** {ARCHITECTURE_PATTERN}
**Producto:** {PRODUCT}
**Estimación Total:** Xh XXmin

## Componentes a Implementar

### 1. {COMPONENT_NAME} ({ARCHITECTURE_PATTERN})
- [ ] {COMPONENT_PATH}/file1.py (XX min)
  - Descripción breve del componente
  - Responsabilidades principales
- [ ] {COMPONENT_PATH}/file2.py (XX min)
  ...

### 2. Integración
- [ ] Descripción de integración (XX min)
  - Puntos de conexión con componentes existentes

### 3. Tests
- [ ] tests/test_*.py por cada componente (XX min)

### 4. Validación
- [ ] Ejecutar escenarios BDD (5 min)
- [ ] Quality gates (5 min)

**Estado:** 0/N tareas completadas
```

---

## Ubicación del Archivo Generado

> **Según stack:**
> - **PyQt/MVC:** `{PRODUCT}/docs/plans/US-XXX-plan.md`
> - **FastAPI:** `docs/plans/US-XXX-plan.md`
> - **Django:** `docs/requirements/US-XXX-plan.md`
> - **Generic:** `docs/plans/US-XXX-plan.md`

---

## Consideraciones Importantes

### Estimaciones de Tiempo

**Componentes simples:**
- Modelo/Schema: 10-15 min
- Vista/Template básica: 15-20 min
- Controlador/Service: 15-20 min

**Componentes complejos:**
- Vista interactiva: 25-30 min
- Service con múltiple lógica: 25-35 min
- Repository con queries complejas: 20-30 min

**Tests:**
- Test unitario simple: 10-15 min
- Test con mocks: 15-20 min
- Test de integración: 15-25 min

**Validación:**
- BDD: 5 min
- Quality gates: 5 min

### Organización de Tareas

1. **Secuencia bottom-up:** Empezar por capas inferiores (modelo, schema) hacia superiores (controlador, router)
2. **Dependencias primero:** Componentes sin dependencias antes que los que dependen de otros
3. **Tests después de implementación:** Tests inmediatamente después del componente correspondiente

---

## Punto de Aprobación

**Usuario revisa y aprueba el plan**

Este es un punto crítico donde el usuario debe validar:
- La estructura de componentes es correcta
- Las estimaciones son razonables
- No falta ningún componente o integración importante
- El orden de tareas tiene sentido

**El plan puede ajustarse en esta fase** antes de comenzar la implementación.

---

## Tracking

**Al finalizar la fase:**
```python
tracker.end_phase(2, auto_approved=False)  # Requiere aprobación del usuario
```

---

**Fase anterior:** [Fase 1: Generación de Escenarios BDD](./phase-1-bdd.md)
**Siguiente fase:** Fase 3: Implementación Guiada por Tareas _(pendiente)_
