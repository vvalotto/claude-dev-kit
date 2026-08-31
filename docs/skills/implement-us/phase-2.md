# Fase 2: Plan de Implementación

Traduce la historia de usuario en un plan de implementación estructurado: un checklist de archivos a crear, organizados por capa arquitectónica según el perfil activo. Es la hoja de ruta que la Fase 3 ejecutará tarea a tarea.

**Aprobación requerida:** Sí — el usuario debe aprobar el plan explícitamente antes de que comience la implementación.

---

## Para el usuario

### Qué hace esta fase

1. Lee el patrón arquitectónico del perfil activo desde `config.json`
2. Identifica los componentes necesarios según el patrón (MVC, Layered, BFF, Generic)
3. Mapea cada criterio de aceptación a los componentes que lo implementan
4. Genera `docs/plans/{US_ID}-plan.md` con el checklist de tareas
5. Presenta el plan para tu revisión — podés solicitar ajustes antes de aprobar

### Qué esperar

El plan es el punto de control más importante del skill. Una vez aprobado, la Fase 3 ejecuta exactamente lo que dice el plan, tarea por tarea. Si el plan está incorrecto, la implementación también lo estará.

El skill no avanza a Fase 3 hasta que:
1. `docs/plans/{US_ID}-plan.md` existe en disco
2. Aprobaste el plan explícitamente

Podés pedir ajustes antes de aprobar: el skill incorpora tus cambios y vuelve a presentar el plan.

### Artefacto que produce

`docs/plans/{US_ID}-plan.md` — checklist de componentes a crear/modificar por capa, con las rutas exactas de los archivos. La Fase 3 lo lee para guiar la implementación y marca cada checkbox al completar cada tarea.

### Estructura del plan

```markdown
# Plan de Implementación: {US_ID} - {US_TITLE}

**Patrón:** {ARCHITECTURE_PATTERN}
**Producto:** {PRODUCT}

## Componentes a Implementar

### 1. {COMPONENT_NAME} ({ARCHITECTURE_PATTERN})
- [ ] {COMPONENT_PATH}/file1.py
- [ ] {COMPONENT_PATH}/file2.py

### 2. Integración
- [ ] Descripción de conexión con componentes existentes

**Estado:** 0/N tareas completadas
```

> **Nota:** El plan no incluye tests ni quality gates — esos son responsabilidad de las Fases 4, 5, 6 y 7.

### Componentes según patrón

| Patrón | Componentes típicos |
|---|---|
| MVC (PyQt) | Modelo (dataclass inmutable), Vista (QWidget), Controlador (mediador) |
| Layered FastAPI | Schema (Pydantic), Service, Repository, Router |
| Layered Flask REST | Blueprint + endpoints, Domain (dataclass), Repository (ABC + implementación) |
| BFF Flask Webapp | Routes + API Client, Templates (Jinja2), JavaScript, CSS |
| Generic Python | Module, Class, Utils según necesidad |

---

## Referencia técnica

### Entradas

| Entrada | Tipo | Requerida | Fuente |
|---|---|---|---|
| `docs/plans/{US_ID}-context.md` | Artefacto | ✅ Sí | Fase 0 |
| Patrón arquitectónico | `config.json` → `variables.architecture_pattern` | ✅ Sí | Perfil activo |
| Criterios de aceptación | Leídos de la fuente HU | ✅ Sí | Registrado en Fase 0 |
| Estructura de componentes del perfil | `customizations/{perfil}.json` → `component_structure` | ✅ Sí | Perfil activo |

### Salidas

| Salida | Tipo | Descripción |
|---|---|---|
| `docs/plans/{US_ID}-plan.md` | Artefacto físico | Checklist de componentes a implementar por capa |
| Aprobación del usuario | En conversación | El usuario puede solicitar ajustes antes de aprobar |

### Templates

| Template | Ruta en `config.json` | Uso |
|---|---|---|
| Plan de implementación | `templates/planning/implementation-plan.md` | Referencia estructural externa |

> Si existe `templates/planning/implementation-plan.md`, se usa como base estructural. Si no, se usa el template embebido en el archivo de fase.

### Artefactos

| Artefacto | Operación | Ruta |
|---|---|---|
| `{US_ID}-plan.md` | **Genera** | `docs/plans/{US_ID}-plan.md` |
| `{US_ID}-context.md` | **Lee** | `docs/plans/{US_ID}-context.md` |
| `customizations/{perfil}.json` | **Lee** (patrón arquitectónico) | `.claude/skills/implement-us/customizations/{PROFILE}.json` |

### Convenciones

- El plan se genera en `docs/plans/{US_ID}-plan.md` — ruta verificada en disco antes de presentar al usuario.
- El plan **no incluye** secciones de tests, validación ni quality gates (responsabilidad de Fases 4-7).
- Las tareas siguen orden bottom-up: capas inferiores primero (modelo/schema antes que controlador/router).
- El checkpoint de aprobación es imperativo: no se avanza a Fase 3 sin aprobación explícita del usuario.

### Dependencias

| Dirección | Fase | Qué provee |
|---|---|---|
| ← anterior | Fase 0 | `context.md` con patrón y umbrales |
| ← anterior | Fase 1 | (ninguna: el plan es independiente de los escenarios BDD) |
| → siguiente | Fase 3 | Plan de tareas a ejecutar |
| → siguiente | Fase 9 | Lista de tareas completadas para el reporte |

### Checklist de salida

- [ ] `docs/plans/{US_ID}-plan.md` existe en disco
- [ ] El plan fue presentado al usuario
- [ ] El usuario aprobó el plan explícitamente
- [ ] Tracking de Fase 2 cerrado

### Estado en v1.3

| ID | Descripción | Resolución |
|---|---|---|
| D2-2 | El template de output no especificaba la ruta del archivo a guardar | Se especificó `docs/plans/{US_ID}-plan.md` como ruta canónica en el Paso 6 (verificación imperativa) |
| D2-3 | Ambigüedad entre template externo (`templates/planning/`) y template embebido | Se estableció prioridad: si existe el template externo, usarlo; si no, usar el embebido |
| D2-1 | Ejemplos de integración con referencias específicas de PyQt (Factory/Coordinator) en contexto genérico | Reemplazado por referencia genérica al mecanismo de composición del perfil activo |

---

**Fase anterior:** [Fase 1: Generación de Escenarios BDD](phase-1.md)
**Siguiente fase:** [Fase 3: Implementación](phase-3.md)
