# TICKET-033: Generalizar Template implementation-plan.md

**Fase:** 4 - Generalización de Templates
**Sprint:** 2
**Estado:** TODO
**Prioridad:** Alta
**Estimación:** 1.5 horas
**Asignado a:** Claude Code

---

## Descripción

Generalizar el template `implementation-plan.md` removiendo todas las referencias específicas a MVC/PyQt/Factory/Coordinator y reemplazándolas con variables o snippets por perfil.

**Complejidad:** Alta - Este template tiene ~40% de contenido específico (Factory, Coordinator, Compositor, señales PyQt).

---

## Criterios de Aceptación

- [ ] Template copiado y generalizado en `templates/planning/implementation-plan.md`
- [ ] Referencias a Factory/Coordinator/Compositor removidas
- [ ] Variables de integración implementadas (`{INTEGRATION_PATTERN}`, `{COMPONENT_INTEGRATION}`)
- [ ] Secciones específicas convertidas a snippets
- [ ] Template validado con 3 perfiles diferentes
- [ ] Snippets agregados a perfiles JSON

---

## Dependencias

**Depende de:**
- ✅ TICKET-030: Análisis completado
- ✅ TICKET-031: Estructura creada

**Bloquea a:**
- TICKET-036: Testing y validación

---

## Análisis del Template Actual

**Archivo fuente:** `_work/from-simapp/templates/implementation-plan.md` (2,902 bytes)

**Estado actual:** ~40% genérico

**Referencias específicas a remover:**

1. **Líneas 98-99:** Integración con Factory
2. **Líneas 99:** Integración con Coordinator
3. **Línea 57:** "Conectar señales (si aplica)" - PyQt specific

---

## Variables Nuevas a Implementar

| Variable | Propósito | Ubicación en Template |
|----------|-----------|----------------------|
| `{INTEGRATION_SECTION}` | Sección completa de integración | Reemplaza líneas 98-99 |
| `{COMPONENT_INTEGRATION_TASKS}` | Tareas de integración | Checklist de progreso |

---

## Snippets por Perfil

### pyqt-mvc

```markdown
### Integración
- [ ] Componente integrado en Factory
- [ ] Señales conectadas en Coordinator
```

### fastapi-rest

```markdown
### Integración
- [ ] Router registrado en aplicación principal
- [ ] Dependencias inyectadas
```

### flask-rest

```markdown
### Integración
- [ ] Blueprint registrado en aplicación
- [ ] Rutas configuradas
```

### flask-webapp

```markdown
### Integración
- [ ] Blueprint registrado con templates
- [ ] Rutas y formularios configurados
```

### generic-python

```markdown
### Integración
- [ ] Módulo importado correctamente
- [ ] Dependencias configuradas
```

---

## Implementación

### Template Generalizado (extracto clave)

```markdown
## Checklist de Progreso

### Implementación
- [ ] Componente 1 implementado
- [ ] Componente 2 implementado
{INTEGRATION_SECTION}

### Testing
- [ ] Tests unitarios implementados
...
```

---

## Checklist de Implementación

- [ ] Template copiado a `templates/planning/implementation-plan.md`
- [ ] Referencias específicas removidas
- [ ] Variables `{INTEGRATION_SECTION}` implementadas
- [ ] Snippets agregados a 5 perfiles
- [ ] Header actualizado con lista completa de variables
- [ ] Commit: `feat(templates): generalizar implementation-plan.md (TICKET-033)`

---

## Resultado

_A completar al finalizar el ticket._
