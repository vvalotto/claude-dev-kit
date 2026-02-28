# Fase 3: Implementación

Fase de mayor duración del skill. Ejecuta el plan de Fase 2 tarea a tarea, generando el código de producción de cada componente. El usuario aprueba cada archivo antes de que se escriba.

**Aprobación requerida:** Sí — por cada tarea individual (ciclo `sí / no / editar`).

---

## Para el usuario

### Qué hace esta fase

1. Lee el plan completo desde disco para identificar las tareas pendientes
2. Lee el `context.md` para verificar el flag `skip_bdd` y las rutas del perfil activo
3. Lee `component_structure` del perfil activo para usar rutas exactas
4. Por cada tarea del plan, en orden:
   - Presenta el código propuesto con contexto (tarea N/total, ruta del archivo, patrón)
   - Espera tu respuesta: `yes`, `no`, o `edit`
   - Si `yes`: escribe el archivo y verifica sintaxis e imports
   - Si `edit`: incorpora tus cambios y vuelve a presentar para aprobación
   - Si `no`: omite la tarea
   - Actualiza el checkbox en `docs/plans/{US_ID}-plan.md` al completar cada tarea
5. Al terminar todas las tareas, busca código obsoleto y presenta una lista para tu confirmación antes de eliminar

### Qué esperar

El ciclo por tarea luce así:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 TAREA 2/5: Implementar ProductoService
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 Ubicación: app/services/producto_service.py
📐 Patrón: Service (Layered Architecture)

✏️  Código propuesto:
───────────────────────────────────────
[Código generado aquí]
───────────────────────────────────────

❓ ¿Aprobar e implementar? (yes/no/edit)
```

Si respondés `edit`, podés describir cambios verbalmente o pegar el código corregido directamente.

### Artefactos que produce

- Archivos de código de producción en las rutas del perfil activo
- `docs/plans/{US_ID}-plan.md` actualizado con checkboxes marcados ✅

> **Importante:** Cada checkbox se marca inmediatamente al completar la tarea, no al final de la fase. Esto permite retomar el trabajo si la sesión se interrumpe.

---

## Referencia técnica

### Entradas

| Entrada | Tipo | Requerida | Fuente |
|---|---|---|---|
| `docs/plans/{US_ID}-plan.md` | Artefacto | ✅ Sí | Fase 2 |
| `docs/plans/{US_ID}-context.md` | Artefacto | ✅ Sí | Fase 0 |
| Perfil activo (rutas, clases base, patrones) | `config.json` + perfil | ✅ Sí | Instalación |
| `customizations/{perfil}.json` → `component_structure` | Perfil | ✅ Sí | Instalación |

### Salidas

| Salida | Tipo | Descripción |
|---|---|---|
| Archivos de código de producción | Artefactos físicos | Según estructura del perfil activo |
| Plan actualizado con checkboxes | `docs/plans/{US_ID}-plan.md` | Cada tarea marcada ✅ al completarse |
| Revisión de código obsoleto | En conversación | Lista de candidatos a eliminar, confirmación antes de borrar |

### Templates

Ninguno externo. El código se genera según el perfil activo. Los perfiles (`customizations/*.json`) incluyen `code_templates` con ejemplos por stack:
- PyQt: `modelo.py`, `vista.py`, `controlador.py`
- FastAPI: `router.py`, `service.py`, `repository.py`, `schema.py`
- Flask REST: `api.py` (Blueprint), `domain.py` (dataclass), `repository.py` (ABC)
- Flask Webapp: `routes.py`, templates Jinja2, JavaScript modules
- Generic: clases Python con docstrings y type hints

### Artefactos

| Artefacto | Operación | Ruta |
|---|---|---|
| `{US_ID}-plan.md` | **Lee y actualiza** (marca ✅ por tarea) | `docs/plans/{US_ID}-plan.md` |
| Archivos de código | **Genera** (según plan) | `{COMPONENT_PATH}/*` |
| `{US_ID}-context.md` | **Lee** | `docs/plans/{US_ID}-context.md` |

### Convenciones

- Tracking de tarea (`start-task` / `end-task`) por cada ítem del plan.
- El tracking de fase inicia **antes** de leer el plan (no después).
- El ciclo `sí/no/editar` es imperativo — no se escribe ningún archivo sin aprobación.
- El plan se lee siempre desde disco, no desde memoria de la conversación.
- Las rutas de componentes se leen desde `customizations/{perfil}.json → component_structure`, no se infieren.
- Si `skip_bdd: true` en `context.md`, Fase 1 y Fase 6 se marcan como omitidas — se anticipa que no habrá feature file al llegar a Fase 6.
- La revisión de código obsoleto es imperativa al finalizar todas las tareas.

### Protocolo de recuperación

Si un archivo falla (sintaxis, imports rotos):
1. Leer el error completo sin asumir la causa
2. Corregir el código
3. Volver a presentar al usuario para aprobación
4. Re-ejecutar la verificación de sintaxis/imports
5. No avanzar a la siguiente tarea hasta resolver

### Dependencias

| Dirección | Fase | Qué provee |
|---|---|---|
| ← anterior | Fase 2 | Plan de implementación aprobado |
| → siguiente | Fase 4 | Código de producción para tests unitarios |
| → siguiente | Fase 5 | Código para tests de integración |
| → siguiente | Fase 7 | Código a analizar con pylint/radon |

### Checklist de salida

- [ ] Todos los componentes del plan implementados (todos los checkboxes marcados en `docs/plans/{US_ID}-plan.md`)
- [ ] Plan actualizado en disco con estado final
- [ ] Criterios de aceptación de la HU tienen cobertura en el código implementado
- [ ] Revisión de código obsoleto ejecutada
- [ ] Tracking de Fase 3 cerrado

### Estado en v1.3

| ID | Descripción | Resolución |
|---|---|---|
| D3-1 | La fase no verificaba el flag `--skip-bdd` — el agente podía intentar leer un feature file inexistente en Fase 6 | Se agregó instrucción explícita: leer `skip_bdd` de `context.md` y marcar Fase 1 y 6 como omitidas si es `true` |
| D3-2 | La fase no incluía instrucción de leer `component_structure` del perfil activo — el agente podía usar rutas por defecto incorrectas | Se agregó instrucción explícita de leer `customizations/{perfil}.json → component_structure` antes de iniciar el ciclo de tareas |

---

**Fase anterior:** [Fase 2: Plan de Implementación](phase-2.md)
**Siguiente fase:** [Fase 4: Tests Unitarios](phase-4.md)
