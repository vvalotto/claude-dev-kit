# Gestión del Proyecto Claude Dev Kit

Este directorio contiene la gestión y seguimiento del proyecto organizado por fases y sprints.

## Estructura

```
gestion/
├── README.md                           # Este archivo
├── fase-1-setup-inicial/              # Fase 1: Setup Inicial
│   ├── sprint-1.md                    # Sprint 1: Setup + Instalación
│   └── tickets/                       # Tickets individuales de la fase
├── fase-2-sistema-instalacion/        # Fase 2: Sistema de Instalación
│   ├── sprint-1.md                    # Sprint 1: Setup + Instalación
│   └── tickets/
├── fase-3-generalizacion-skills/      # Fase 3: Generalización de Skills
│   ├── sprint-2.md                    # Sprint 2: Skills + Templates
│   └── tickets/
├── fase-4-templates/                  # Fase 4: Templates
│   ├── sprint-2.md                    # Sprint 2: Skills + Templates
│   └── tickets/
├── fase-5-sistema-tracking/           # Fase 5: Sistema de Tracking
│   ├── sprint-2.md                    # Sprint 2: Skills + Templates
│   └── tickets/
├── fase-6-documentacion/              # Fase 6: Documentación
│   ├── sprint-3.md                    # Sprint 3: Documentación + Ejemplos
│   └── tickets/
├── fase-7-ejemplos/                   # Fase 7: Ejemplos
│   ├── sprint-3.md                    # Sprint 3: Documentación + Ejemplos
│   └── tickets/
├── fase-8-testing-validacion/         # Fase 8: Testing y Validación
│   ├── sprint-4.md                    # Sprint 4: Testing + Release
│   └── tickets/
└── fase-9-release/                    # Fase 9: Release v1.0
    ├── sprint-4.md                    # Sprint 4: Testing + Release
    └── tickets/
```

## Mapeo Fases → Sprints

| Fase | Nombre | Sprint |
|------|--------|--------|
| 1 | Setup Inicial | Sprint 1 |
| 2 | Sistema de Instalación | Sprint 1 |
| 3 | Generalización de Skills | Sprint 2 |
| 4 | Templates | Sprint 2 |
| 5 | Sistema de Tracking | Sprint 2 |
| 6 | Documentación | Sprint 3 |
| 7 | Ejemplos | Sprint 3 |
| 8 | Testing y Validación | Sprint 4 |
| 9 | Release v1.0 | Sprint 4 |

## Workflow de Gestión

### 1. Documentos de Sprint

Cada `sprint-N.md` contiene:
- Objetivos del sprint
- Fases incluidas
- Lista de tickets
- Métricas y progreso
- Retrospectiva al finalizar

### 2. Tickets

Cada ticket se crea en `fase-X-nombre/tickets/TICKET-NNN.md` con:
- ID único (TICKET-001, TICKET-002, etc.)
- Título descriptivo
- Descripción detallada
- Criterios de aceptación
- Estimación (puntos o tiempo)
- Estado (TODO, IN_PROGRESS, DONE, BLOCKED)
- Asignado a
- Dependencias

### 3. Estados de Tickets

- **TODO**: Pendiente de iniciar
- **IN_PROGRESS**: En desarrollo
- **REVIEW**: En revisión
- **BLOCKED**: Bloqueado por dependencia
- **DONE**: Completado

### 4. Template de Ticket

```markdown
# TICKET-XXX: [Título]

**Fase:** X - Nombre de la Fase
**Sprint:** N
**Estado:** TODO | IN_PROGRESS | REVIEW | BLOCKED | DONE
**Prioridad:** Alta | Media | Baja
**Estimación:** X horas / Y puntos
**Asignado a:** Victor Valotto / Claude Code

## Descripción

[Descripción detallada de la tarea]

## Criterios de Aceptación

- [ ] Criterio 1
- [ ] Criterio 2
- [ ] Criterio 3

## Dependencias

- Depende de: TICKET-XXX
- Bloquea a: TICKET-XXX

## Notas Técnicas

[Notas de implementación, decisiones técnicas, etc.]

## Checklist de Implementación

- [ ] Subtarea 1
- [ ] Subtarea 2
- [ ] Subtarea 3

## Resultado

[Al completar: descripción del resultado, enlaces a commits, archivos creados]
```

## Comandos Útiles

```bash
# Crear nuevo ticket
cat > gestion/fase-X-nombre/tickets/TICKET-XXX.md

# Ver todos los tickets de una fase
ls -la gestion/fase-X-nombre/tickets/

# Buscar tickets por estado
grep -r "Estado: TODO" gestion/*/tickets/

# Listar tickets en progreso
grep -r "Estado: IN_PROGRESS" gestion/*/tickets/
```

## Progreso General

### Sprint 1: Setup + Instalación (Semana 1)
- **Estado:** En Progreso
- **Fases:** 1, 2
- **Tickets:** Ver `fase-1-setup-inicial/sprint-1.md` y `fase-2-sistema-instalacion/sprint-1.md`

### Sprint 2: Skills + Templates (Semana 2)
- **Estado:** Pendiente
- **Fases:** 3, 4, 5

### Sprint 3: Documentación + Ejemplos (Semana 3)
- **Estado:** Pendiente
- **Fases:** 6, 7

### Sprint 4: Testing + Release (Semana 4)
- **Estado:** Pendiente
- **Fases:** 8, 9

---

**Última Actualización:** 2026-02-07
