# Fase 1: Generación de Escenarios BDD

**Objetivo:** Analizar la Historia de Usuario y generar escenarios BDD en formato Gherkin.

**Duración estimada:** 15-20 minutos

---

## Tracking

**Al inicio de la fase:**
```python
tracker.start_phase(1, "Generación de Escenarios BDD")
```

---

## Acción

Analizar la US y generar escenarios BDD en formato Gherkin.

**Template:** `.claude/templates/bdd-scenario.feature`

---

## Pasos de Generación BDD

### 1. Leer criterios de aceptación de la US

- Extraídos en Fase 0
- Cada criterio se convierte en al menos un escenario

### 2. Por cada criterio, generar un escenario BDD:

- **Given** (contexto/precondición) - Estado inicial del sistema
- **When** (acción del usuario/sistema) - Trigger de la funcionalidad
- **Then** (resultado esperado) - Comportamiento observable y verificable

### 3. Generar archivo feature:

> **Ubicación según stack:**
> - **PyQt/MVC:** `{PRODUCT}/tests/features/US-XXX-{nombre}.feature`
> - **FastAPI:** `tests/features/US-XXX-{nombre}.feature`
> - **Django:** `{app}/tests/features/US-XXX-{nombre}.feature`
> - **Generic:** `tests/features/US-XXX-{nombre}.feature`

---

## Ejemplos de Output por Stack

### Ejemplo 1: Aplicación UI (PyQt, Desktop)

```gherkin
Feature: Mostrar información de estado en tiempo real (US-001)

  Scenario: El panel muestra datos cuando hay conexión
    Given la aplicación está iniciada
    And hay conexión con el servicio de datos
    When se recibe información actualizada
    Then el panel muestra los datos recibidos
    And el indicador de estado muestra "Conectado"
```

### Ejemplo 2: API REST (FastAPI, Backend)

```gherkin
Feature: Endpoint de consulta de usuarios (US-002)

  Scenario: GET /users retorna lista de usuarios activos
    Given existen 3 usuarios activos en la base de datos
    And existe 1 usuario inactivo
    When se hace GET a /users?status=active
    Then la respuesta tiene status code 200
    And la respuesta contiene 3 usuarios
    And todos los usuarios tienen status "active"
```

### Ejemplo 3: Aplicación Web (Django, Full Stack)

```gherkin
Feature: Formulario de registro de usuario (US-003)

  Scenario: Usuario se registra con datos válidos
    Given el usuario está en la página de registro
    When ingresa email "user@example.com"
    And ingresa contraseña "SecurePass123"
    And hace clic en "Registrarse"
    Then se muestra mensaje "Registro exitoso"
    And el usuario es redirigido a /dashboard
```

### Ejemplo 4: Módulo Genérico (Generic Python)

```gherkin
Feature: Procesamiento de datos de entrada (US-004)

  Scenario: Procesador valida y transforma datos correctos
    Given un procesador inicializado
    When se envían datos en formato válido
    Then los datos son validados exitosamente
    And la salida tiene el formato esperado
```

---

## Mejores Prácticas BDD

✅ **Escenarios independientes:** Cada escenario debe poder ejecutarse solo
✅ **Lenguaje del negocio:** Usar términos del dominio, no detalles técnicos
✅ **Verificables:** Cada Then debe ser observable y automatizable
✅ **Concisos:** Un escenario = un comportamiento específico

❌ **Evitar:**
- Detalles de implementación en los escenarios
- Múltiples comportamientos en un solo escenario
- Dependencias entre escenarios

---

## Punto de Aprobación

**Usuario revisa y aprueba escenarios BDD**

Este es un punto crítico donde el usuario debe validar que los escenarios:
- Cubren todos los criterios de aceptación
- Están escritos en lenguaje de negocio
- Son verificables y automatizables

---

## Tracking

**Al finalizar la fase:**
```python
tracker.end_phase(1, auto_approved=False)  # Requiere aprobación del usuario
```

---

**Fase anterior:** [Fase 0: Validación de Contexto](./phase-0-validation.md)
**Siguiente fase:** Fase 2: Generación del Plan de Implementación _(pendiente)_
