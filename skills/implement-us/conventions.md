# Convenciones de Escritura — implement-us

Este archivo define la convención estructural que deben seguir **todos los archivos de fase** del skill `/implement-us`.

Su propósito es distinguir con claridad el contenido que el agente **debe ejecutar** del contenido que el agente puede **consultar como referencia**.

---

## El problema que resuelve

Los agentes digitales no distinguen automáticamente entre instrucciones y ejemplos. Un bloque de código Python dentro de un archivo de fase puede ser interpretado como documentación en lugar de una acción a ejecutar.

**Ejemplo del problema:**

```python
# Esto parece documentación — el agente puede ignorarlo
tracker.start_phase(7, "Quality Gates")
```

Este bloque fue diseñado para que el agente lo ejecutara, pero al estar dentro de un bloque de código sin contexto imperativo, el agente lo trata como referencia y no lo ejecuta.

**La convención define cómo evitar esta ambigüedad.**

---

## Tipos de Sección

### 🔴 Sección Imperativa

Marcada con el encabezado: `## 🔴 Acción Requerida — {descripción breve}`

El agente **DEBE** ejecutar el contenido de esta sección antes de avanzar.

**Características:**
- Usa lenguaje en imperativo directo: "Ejecutá", "Verificá", "Generá"
- Especifica el comando o acción concreta a realizar
- Puede incluir bloques de código, pero siempre precedidos de la instrucción en lenguaje natural
- Termina con una condición de salida clara

**Ejemplo correcto:**

> **🔴 Acción Requerida — Iniciar tracking de fase**
>
> Antes de cualquier otra acción en esta fase, ejecutá el siguiente comando:
> ```bash
> python .claude/tracking/track.py start-phase 7 "Quality Gates"
> ```
> No avances al siguiente paso hasta que el comando se haya ejecutado exitosamente.

---

### 📖 Sección de Referencia

Marcada con el encabezado: `## 📖 Referencia — {descripción breve}`

El agente puede consultar su contenido para orientarse, pero **no está obligado a ejecutarlo**.

**Características:**
- Contiene contexto, ejemplos, explicaciones y alternativas
- Puede incluir código de ejemplo, pero como ilustración
- No contiene instrucciones de acción directa

**Ejemplo correcto:**

> **📖 Referencia — Umbrales de calidad por perfil**
>
> Los umbrales varían según el perfil activo del proyecto. Ver tabla a continuación para referencia. Los valores reales a usar se leen del archivo `config.json` del perfil.
>
> | Perfil | Pylint | Coverage |
> |--------|--------|----------|
> | PyQt   | ≥ 8.0  | ≥ 90%    |
> | FastAPI| ≥ 8.5  | ≥ 95%    |

---

### ✅ Checklist de Salida

Marcada con el encabezado: `## ✅ Checklist de Salida`

Aparece **al final de cada fase**. El agente debe confirmar cada ítem antes de avanzar a la siguiente fase.

**Características:**
- Lista de condiciones verificables (no subjetivas)
- Cada ítem especifica cómo verificar la condición (comando `ls`, resultado de test, etc.)
- El agente no puede avanzar si algún ítem no está marcado

**Ejemplo correcto:**

```markdown
## ✅ Checklist de Salida

Antes de avanzar a Fase 3, confirmá que:
- [ ] `docs/plans/{US_ID}-plan.md` existe en disco: `ls docs/plans/{US_ID}-plan.md`
- [ ] El plan fue presentado al usuario
- [ ] El usuario aprobó el plan explícitamente
- [ ] Tracking de Fase 2 cerrado
```

---

### 🚫 Bloqueo Explícito

Marcado con el encabezado: `## 🚫 STOP`

Se usa cuando el agente **no puede avanzar** bajo ninguna circunstancia sin cumplir una condición específica.

**Diferencia con checklist:** el bloqueo es incondicional; el agente debe detenerse y esperar respuesta o resultado.

**Ejemplo correcto:**

> **🚫 STOP — No avances a Fase 3 hasta que:**
> 1. `docs/plans/{US_ID}-plan.md` exista en disco ✅
> 2. El usuario haya respondido explícitamente con aprobación del plan
>
> Presentá el plan al usuario y esperá su respuesta antes de continuar.

---

## Formato de Instrucción Imperativa

Dentro de una sección imperativa, el texto debe:

1. **Usar segunda persona imperativa:** "Ejecutá", "Verificá", "Generá", "Leé"
2. **Ser específico:** indicar el comando exacto, la ruta exacta o la acción concreta
3. **No asumir contexto de la conversación:** el agente puede estar en una sesión diferente a la que generó el plan

### Antes / Después

**❌ Antes (ambiguo):**
```python
tracker.start_phase(7, "Quality Gates")
```

**✅ Después (imperativo):**
> **🔴 Acción Requerida — Iniciar tracking de fase**
> Ejecutá antes de cualquier otra acción:
> `python .claude/tracking/track.py start-phase 7 "Quality Gates"`

---

**❌ Antes (descriptivo sin acción):**
> El plan debe existir antes de implementar.

**✅ Después (verificación explícita):**
> **🔴 Acción Requerida — Verificar existencia del plan**
> Ejecutá: `ls docs/plans/{US_ID}-plan.md`
> Si el archivo no existe, ejecutá Fase 2 antes de continuar.

---

## Aplicación en los Archivos de Fase

Cada archivo de fase debe tener la siguiente estructura mínima:

```markdown
# Fase N: {Nombre}

**Objetivo:** {descripción concisa}

---

## 🔴 Acción Requerida — Verificar precondiciones
{verificación de artefactos de fase anterior}

## 🔴 Acción Requerida — Iniciar tracking
{comando de inicio de tracking}

---

{Contenido de la fase: pasos, secciones imperativas y de referencia}

---

## ✅ Checklist de Salida
{lista de condiciones verificables antes de avanzar}

## 🔴 Acción Requerida — Cerrar tracking
{comando de cierre de tracking}

---

**Siguiente fase:** [Fase N+1]
```

---

**Referenciado por:** `skill.md`, todos los archivos de fase
**Aplicado en:** Tickets TICKET-073 a TICKET-077
