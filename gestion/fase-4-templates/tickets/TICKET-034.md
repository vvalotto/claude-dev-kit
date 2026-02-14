# TICKET-034: Generalizar Template implementation-report.md

**Fase:** 4 - Generalización de Templates
**Sprint:** 2
**Estado:** TODO
**Prioridad:** Alta
**Estimación:** 1.5 horas
**Asignado a:** Claude Code

---

## Descripción

Generalizar el template `implementation-report.md` removiendo referencias específicas a Factory/Coordinator/Compositor y secciones muy específicas como "Pruebas con RPi Real".

**Complejidad:** Alta - Template más grande (6,332 bytes) con ~30% de contenido específico.

---

## Criterios de Aceptación

- [ ] Template generalizado en `templates/reporting/implementation-report.md`
- [ ] Secciones específicas (Factory, Coordinator, Compositor, RPi) removidas
- [ ] Variables de integración y deployment implementadas
- [ ] Snippets por perfil creados
- [ ] Template validado con 3 perfiles

---

## Dependencias

**Depende de:**
- ✅ TICKET-030, TICKET-031

**Bloquea a:**
- TICKET-036

---

## Referencias Específicas a Remover

1. **Líneas 122-149:** Integración con Factory/Coordinator/Compositor
2. **Líneas 219-224:** "Pruebas con RPi Real" - demasiado específico

---

## Variables Nuevas

| Variable | Propósito |
|----------|-----------|
| `{INTEGRATION_REPORT}` | Cómo se integró el componente |
| `{DEPLOYMENT_TESTING_REPORT}` | Testing de deployment específico |

---

## Snippets por Perfil

Ver estructura similar a TICKET-033, adaptada para formato de reporte.

---

## Checklist de Implementación

- [ ] Template copiado y generalizado
- [ ] Secciones específicas convertidas a variables/snippets
- [ ] Snippets agregados a 5 perfiles
- [ ] Validación con ejemplos
- [ ] Commit: `feat(templates): generalizar implementation-report.md (TICKET-034)`

---

## Resultado

_A completar al finalizar el ticket._
