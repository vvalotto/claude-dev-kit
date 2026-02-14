# TICKET-032: Generalizar Template bdd-scenario.feature

**Fase:** 4 - Generalización de Templates
**Sprint:** 2
**Estado:** TODO
**Prioridad:** Media
**Estimación:** 0.5 horas
**Asignado a:** Claude Code

---

## Descripción

Generalizar el template `bdd-scenario.feature` para que sea framework-agnostic. Este template ya está ~90% genérico, solo requiere ajustes menores en la sección `Background` para soportar diferentes tipos de aplicaciones.

---

## Criterios de Aceptación

- [ ] Template copiado de `_work/from-simapp/templates/` a `templates/bdd/scenario.feature`
- [ ] Sección `Background` generalizada (remover "aplicación está iniciada", "configuración está cargada")
- [ ] Variable `{BACKGROUND_SETUP}` implementada
- [ ] Comentarios actualizados para ser framework-agnostic
- [ ] Template validado sintácticamente (Gherkin válido)
- [ ] Documentación actualizada en header del archivo

---

## Dependencias

**Depende de:**
- ✅ TICKET-030: Análisis completado
- ✅ TICKET-031: Estructura creada

**Bloquea a:**
- TICKET-036: Testing y validación

---

## Análisis del Template Actual

**Archivo fuente:** `_work/from-simapp/templates/bdd-scenario.feature` (897 bytes)

**Estado actual:** ~90% genérico

**Variables ya usadas:**
- `{FEATURE_TITLE}`
- `{US_ID}`
- `{USER_ROLE}`
- `{USER_WANT}`
- `{USER_BENEFIT}`
- `{SCENARIO_N_NAME}`
- `{PRECONDITION_N}`
- `{ACTION}`
- `{EXPECTED_RESULT_N}`

**Trabajo requerido:**

### Sección Background (líneas 9-11)

**Actual:**
```gherkin
  Background:
    Given la aplicación está iniciada
    And la configuración está cargada
```

**Generalizado:**
```gherkin
  Background:
{BACKGROUND_SETUP}
```

**Valores por perfil:**

| Perfil | BACKGROUND_SETUP |
|--------|------------------|
| pyqt-mvc | `    Given la aplicación está iniciada\n    And la configuración está cargada` |
| fastapi-rest | `    Given el servidor API está corriendo\n    And la base de datos está migrada` |
| flask-rest | `    Given el servidor Flask está corriendo\n    And la base de datos está inicializada` |
| flask-webapp | `    Given la aplicación web está corriendo\n    And el usuario está en la página principal` |
| generic-python | `    Given el sistema está inicializado\n    And las dependencias están cargadas` |

---

## Implementación

### 1. Copiar y Modificar Template

```bash
# Copiar template
cp _work/from-simapp/templates/bdd-scenario.feature templates/bdd/scenario.feature

# Editar con variables generalizadas
```

### 2. Template Generalizado

```gherkin
# Template: Escenario BDD (Gherkin)
# Este template se usa para generar archivos .feature basados en historias de usuario
#
# Variables disponibles:
# - {FEATURE_TITLE}: Título de la feature
# - {US_ID}: ID de historia de usuario (ej. US-001)
# - {USER_ROLE}: Rol del usuario (ej. "un usuario", "un administrador")
# - {USER_WANT}: Acción que quiere realizar
# - {USER_BENEFIT}: Beneficio esperado
# - {BACKGROUND_SETUP}: Steps de setup inicial (específico del perfil)
# - {SCENARIO_N_NAME}: Nombre del escenario N
# - {PRECONDITION_N}: Precondición N
# - {ACTION}: Acción principal del escenario
# - {EXPECTED_RESULT_N}: Resultado esperado N

Feature: {FEATURE_TITLE} ({US_ID})
  Como {USER_ROLE}
  Quiero {USER_WANT}
  Para {USER_BENEFIT}

  Background:
{BACKGROUND_SETUP}

  Scenario: {SCENARIO_1_NAME}
    Given {PRECONDITION_1}
    And {PRECONDITION_2}
    When {ACTION}
    Then {EXPECTED_RESULT_1}
    And {EXPECTED_RESULT_2}

  Scenario: {SCENARIO_2_NAME}
    Given {PRECONDITION}
    When {ACTION}
    Then {EXPECTED_RESULT}

  # Agregar más escenarios según criterios de aceptación

# Notas de implementación:
# - Un escenario por cada criterio de aceptación principal
# - Given: Estado inicial/precondiciones
# - When: Acción del usuario o evento del sistema
# - Then: Resultado observable esperado
# - And/But: Para múltiples condiciones
```

### 3. Actualizar Perfiles

Agregar `BACKGROUND_SETUP` a cada perfil en `skills/implement-us/customizations/*.json`:

```json
{
  "template_variables": {
    "BACKGROUND_SETUP": "    Given el servidor API está corriendo\n    And la base de datos está migrada"
  }
}
```

---

## Checklist de Implementación

- [ ] Template copiado a `templates/bdd/scenario.feature`
- [ ] Header actualizado con lista de variables
- [ ] Sección `Background` generalizada con `{BACKGROUND_SETUP}`
- [ ] Snippets `BACKGROUND_SETUP` agregados a los 5 perfiles
- [ ] Validación sintáctica Gherkin (puede usar plugin VSCode)
- [ ] Commit con mensaje: `feat(templates): generalizar bdd-scenario.feature (TICKET-032)`

---

## Testing Manual

Generar un ejemplo por perfil para validar:

```bash
# Ejemplo: Sustituir variables para pyqt-mvc
# Resultado esperado: archivo .feature válido y específico de PyQt
```

---

## Resultado

_A completar al finalizar el ticket._

**Archivos creados/modificados:**
- `templates/bdd/scenario.feature`
- `skills/implement-us/customizations/pyqt-mvc.json` (+BACKGROUND_SETUP)
- `skills/implement-us/customizations/fastapi-rest.json` (+BACKGROUND_SETUP)
- `skills/implement-us/customizations/flask-rest.json` (+BACKGROUND_SETUP)
- `skills/implement-us/customizations/flask-webapp.json` (+BACKGROUND_SETUP)
- `skills/implement-us/customizations/generic-python.json` (+BACKGROUND_SETUP)
