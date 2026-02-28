# Fase 1: Generación de Escenarios BDD

Transforma los criterios de aceptación de la HU en escenarios ejecutables en formato Gherkin. Esta fase se **omite** si la HU fue clasificada como no-BDD en Fase 0 o si se activó `--skip-bdd`.

**Aprobación requerida:** Sí — el usuario debe responder `[aprobado]` antes de avanzar a Fase 2.

---

## Para el usuario

### Qué hace esta fase

1. Lee los criterios de aceptación de la HU desde la fuente registrada en `context.md`
2. Consulta el template BDD del perfil activo como referencia estructural
3. Genera escenarios Gherkin en formato Given-When-Then: un escenario de happy path por criterio, más escenarios de error para condiciones alternativas
4. Guarda el archivo `.feature` en `tests/features/{US_ID}-{nombre}.feature`
5. Presenta los escenarios para tu revisión y espera aprobación explícita

### Qué esperar

El skill te presentará los escenarios generados y esperará tu respuesta:
- `[aprobado]` para avanzar a Fase 2
- `[revisar]` para ajustar escenarios
- `[rechazar]` para reescribir desde cero

Solo `[aprobado]` avanza a la siguiente fase.

### Artefacto que produce

`tests/features/{US_ID}-{nombre}.feature` — especificación ejecutable del comportamiento esperado del sistema. Persiste hasta la Fase 6, donde se implementan sus steps y se valida que el sistema cumple con lo especificado.

> **Convención de nombre:** `{nombre}` es el slug del título de la HU en minúsculas con guiones.
> Ejemplo: "Alta de producto" → `US-001-alta-de-producto.feature`

### Buenas prácticas de escenarios BDD

✅ Escenarios independientes — cada uno puede ejecutarse solo
✅ Lenguaje del negocio — términos del dominio, no detalles técnicos
✅ Un escenario = un comportamiento específico

❌ Evitar detalles de implementación en los steps
❌ Evitar dependencias entre escenarios

### Ejemplos de output por stack

**Aplicación UI (PyQt, Desktop):**
```gherkin
Feature: Mostrar información de estado en tiempo real (US-001)

  Scenario: El panel muestra datos cuando hay conexión
    Given la aplicación está iniciada
    And hay conexión con el servicio de datos
    When se recibe información actualizada
    Then el panel muestra los datos recibidos
    And el indicador de estado muestra "Conectado"
```

**API REST (FastAPI, Backend):**
```gherkin
Feature: Endpoint de consulta de usuarios (US-002)

  Scenario: GET /users retorna lista de usuarios activos
    Given existen 3 usuarios activos en la base de datos
    When se hace GET a /users?status=active
    Then la respuesta tiene status code 200
    And la respuesta contiene 3 usuarios
```

**Módulo genérico (Python):**
```gherkin
Feature: Procesamiento de datos de entrada (US-004)

  Scenario: Procesador valida y transforma datos correctos
    Given un procesador inicializado
    When se envían datos en formato válido
    Then los datos son validados exitosamente
    And la salida tiene el formato esperado
```

---

## Referencia técnica

### Entradas

| Entrada | Tipo | Requerida | Fuente |
|---|---|---|---|
| `docs/plans/{US_ID}-context.md` | Artefacto | ✅ Sí | Fase 0 |
| Criterios de aceptación de la HU | Leídos de la fuente HU | ✅ Sí | Registrado en Fase 0 |
| Perfil activo (idioma, tag_prefix) | `config.json` → `bdd_config` | ✅ Sí | Instalación |
| Template BDD del perfil | `templates/bdd/` | ❌ Opcional | Perfil activo |

### Salidas

| Salida | Tipo | Descripción |
|---|---|---|
| `tests/features/{US_ID}-{nombre}.feature` | Artefacto físico | Escenarios Gherkin con tag `@US-{ID}` |
| Aprobación del usuario | En conversación | Respuesta `[aprobado]` requerida antes de avanzar |

### Templates

| Template | Ruta | Uso |
|---|---|---|
| Feature genérico | `templates/bdd/scenario.feature` | Referencia estructural para todos los perfiles |
| Feature PyQt | `templates/bdd/pyqt-scenario.feature` | Referencia para perfil `pyqt-mvc` |
| Feature FastAPI | `templates/bdd/api-scenario.feature` | Referencia para perfil `fastapi-rest` |

El template se usa como **referencia estructural** (formato de cabecera, tags, idioma). El contenido se genera con los escenarios específicos de la HU — no se copia el template literal.

### Artefactos

| Artefacto | Operación | Ruta |
|---|---|---|
| `{US_ID}-{nombre}.feature` | **Genera** | `tests/features/{US_ID}-{nombre}.feature` |
| `{US_ID}-context.md` | **Lee** | `docs/plans/{US_ID}-context.md` |

### Convenciones

- La ruta canónica del feature file es `tests/features/{US_ID}-{nombre}.feature` (definida en `artifacts.md`).
- `{nombre}` es el slug del título de la HU: minúsculas, guiones, sin caracteres especiales.
- El skill verifica que el archivo existe en disco con `ls` antes de presentarlo al usuario.
- El punto de aprobación es imperativo: sin `[aprobado]` no se avanza a Fase 2.
- La fase se omite completamente si `skip_bdd: true` en `context.md`.

### Dependencias

| Dirección | Fase | Qué provee |
|---|---|---|
| ← anterior | Fase 0 | `context.md` con criterios y decisión BDD |
| → siguiente | Fase 2 | (ninguna dependencia directa) |
| → siguiente | Fase 6 | Feature file para implementar steps y validar |

### Checklist de salida

- [ ] `tests/features/{US_ID}-*.feature` existe en disco
- [ ] Escenarios presentados al usuario
- [ ] Usuario respondió `[aprobado]`
- [ ] Tracking de Fase 1 cerrado

### Estado en v1.3

| ID | Descripción | Resolución |
|---|---|---|
| D1-1 | La fase no indicaba cómo usar el template BDD (¿leerlo? ¿copiarlo? ¿completar variables?) | Se especificó: leer el template del perfil activo como referencia estructural; completar con los escenarios específicos de la HU sin copiar el template literal |
| D1-3 | No se especificaba qué nombre de archivo usar para `{nombre}` | Se explicitó: slug del título de la HU en minúsculas con guiones, sin caracteres especiales |
| D1-2 | `bdd_config.language: "es"` redundante entre `config.json` y perfiles | Baja prioridad — anotado como deuda técnica |

---

**Fase anterior:** [Fase 0: Validación de Contexto](phase-0.md)
**Siguiente fase:** [Fase 2: Plan de Implementación](phase-2.md)
