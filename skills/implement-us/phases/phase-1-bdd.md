# Fase 1: Generación de Escenarios BDD

**Objetivo:** Analizar la Historia de Usuario y generar escenarios BDD en formato Gherkin.

> **📌 Instrucción de ejecución:** Seguir este archivo de arriba a abajo, en el orden en que aparecen los pasos. No saltar ni reordenar.

---

## Paso 1 🔴 — Verificar precondiciones

Confirmá que existe el artefacto generado en Fase 0:

```bash
ls docs/plans/{US_ID}-context.md
```

Si no existe, **no avances** — completá Fase 0 primero.

---

## Paso 2 🔴 — Iniciar tracking

Ejecutá antes de cualquier otra acción en esta fase:

```bash
python .claude/tracking/tracker_cli.py start-phase 1 "Generación de Escenarios BDD"
```

---

## Paso 3 — Leer criterios de aceptación

Leé los criterios de aceptación directamente del archivo de la HU. La fuente está en el campo `fuente_hu` de `docs/plans/{US_ID}-context.md`.

> **📖 Template de referencia:** Leé el template específico del perfil activo antes de generar los escenarios:
> - PyQt: `.claude/templates/bdd/pyqt-scenario.feature`
> - FastAPI: `.claude/templates/bdd/api-scenario.feature`
> - Flask REST / Flask Webapp / Generic: `.claude/templates/bdd/scenario.feature`
>
> Usá el template como **referencia estructural** — respetá el formato de cabecera (Feature, tags, idioma), pero completá el contenido con los escenarios específicos de la HU. No copies el template literal; adaptalo.

---

## Paso 4 — Generar escenarios Gherkin

Por cada criterio de aceptación:

1. Generar **1 escenario de flujo exitoso** (obligatorio)
2. Si el criterio menciona condiciones de error o estados alternativos, agregar escenarios adicionales para cada uno

> El usuario valida si el set cubre los comportamientos relevantes en el Paso 6.

**Estructura de cada escenario:**

- **Given** — Estado inicial del sistema (contexto/precondición)
- **When** — Acción del usuario o evento del sistema (trigger)
- **Then** — Resultado observable y verificable

**Buenas prácticas:**

✅ Escenarios independientes — cada uno debe poder ejecutarse solo
✅ Lenguaje del negocio — usar términos del dominio, no detalles técnicos
✅ Un escenario = un comportamiento específico

❌ Evitar detalles de implementación, múltiples comportamientos por escenario, dependencias entre escenarios

---

## Paso 5 — Guardar archivo feature

Guardá los escenarios en la ruta canónica definida en `artifacts.md`:

```
tests/features/{US_ID}-{nombre}.feature
```

> **Convención de `{nombre}`:** slug del título de la HU en minúsculas con guiones y sin caracteres especiales.
> Ejemplo: título "Alta de producto" → `{nombre}` = `alta-de-producto`
> Archivo resultante: `US-001-alta-de-producto.feature`

Verificá que existe:

```bash
ls tests/features/{US_ID}-*.feature
```

---

## Paso 6 🔴 — Obtener aprobación del usuario

Presentá los escenarios generados al usuario y esperá respuesta explícita:

> Los escenarios BDD han sido generados en `tests/features/{US_ID}-{nombre}.feature`.
> Revisalos y respondé:
> - **[aprobado]** para avanzar a Fase 2
> - **[revisar]** para ajustar escenarios
> - **[rechazar]** para reescribir desde cero
>
> Solo **[aprobado]** avanza a la siguiente fase.

---

## 📖 Ejemplos de Output por Stack

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

### Ejemplo 3: Módulo Genérico (Generic Python)

```gherkin
Feature: Procesamiento de datos de entrada (US-004)

  Scenario: Procesador valida y transforma datos correctos
    Given un procesador inicializado
    When se envían datos en formato válido
    Then los datos son validados exitosamente
    And la salida tiene el formato esperado
```

---

## ✅ Checklist de Salida

Antes de avanzar a Fase 2, confirmá que:
- [ ] `tests/features/{US_ID}-*.feature` existe en disco: `ls tests/features/{US_ID}-*.feature`
- [ ] Los escenarios fueron presentados al usuario
- [ ] El usuario respondió **[aprobado]**
- [ ] Tracking de Fase 1 cerrado

---

## Paso 7 🔴 — Cerrar tracking

```bash
python .claude/tracking/tracker_cli.py end-phase 1
```

---

**Fase anterior:** [Fase 0: Validación de Contexto](./phase-0-validation.md)
**Siguiente fase:** [Fase 2: Generación del Plan de Implementación](./phase-2-planning.md)
