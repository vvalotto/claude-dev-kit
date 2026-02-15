# TICKET-049: Documentación del Skill implement-us

**Fase:** 6 - Documentación General
**Sprint:** 3
**Estado:** 📋 Pendiente
**Prioridad:** Alta
**Estimación:** 2 horas
**Asignado a:** Claude Code

---

## Descripción

Crear `docs/skills/implement-us.md` con documentación completa del skill principal del framework. Este skill implementa historias de usuario siguiendo un proceso de 10 fases con tracking automático.

---

## Objetivos

1. Explicar propósito y filosofía del skill
2. Documentar uso básico y opciones
3. Explicar detalladamente las 10 fases
4. Mostrar cómo funciona el tracking automático
5. Personalización por perfil
6. Ejemplos completos por stack
7. Troubleshooting

---

## Contenido del Archivo

### Secciones Principales

1. **Introducción**
   - Qué es el skill implement-us
   - Filosofía: BDD + TDD + Quality Gates
   - Cuándo usarlo
   - Beneficios

2. **Uso Básico**
   - Sintaxis: `/implement-us US-ID [--opciones]`
   - Opciones disponibles
   - Prerequisitos
   - Ejemplo mínimo

3. **Las 10 Fases**
   - **Fase 0:** Validación de Contexto
   - **Fase 1:** Generación de Escenarios BDD
   - **Fase 2:** Plan de Implementación
   - **Fase 3:** Implementación
   - **Fase 4:** Tests Unitarios
   - **Fase 5:** Tests de Integración
   - **Fase 6:** Validación BDD
   - **Fase 7:** Quality Gates
   - **Fase 8:** Documentación
   - **Fase 9:** Reporte Final

   Cada fase con:
   - Propósito
   - Input esperado
   - Output generado
   - Tiempo estimado
   - Checkpoints de aprobación

4. **Tracking Automático**
   - Inicio automático de fase
   - Tareas con estimación
   - Pausas manuales
   - Reportes de varianza

5. **Personalización por Perfil**
   - Cómo cada perfil afecta el skill
   - Variables sustituidas
   - Snippets insertados
   - Ejemplos por stack

6. **Ejemplos Completos**
   - Ejemplo PyQt-MVC
   - Ejemplo FastAPI-REST
   - Ejemplo Flask-REST
   - Ejemplo Generic-Python

7. **Troubleshooting**
   - Errores comunes por fase
   - Debugging
   - Recovery de fases fallidas

---

## Checklist de Implementación

1. [ ] Crear directorio docs/skills/
2. [ ] Sección: Introducción y propósito
3. [ ] Sección: Uso básico (sintaxis, opciones)
4. [ ] Sección: Fase 0 - Validación
5. [ ] Sección: Fase 1 - BDD
6. [ ] Sección: Fase 2 - Planning
7. [ ] Sección: Fase 3 - Implementación
8. [ ] Sección: Fase 4 - Tests Unitarios
9. [ ] Sección: Fase 5 - Tests Integración
10. [ ] Sección: Fase 6 - Validación BDD
11. [ ] Sección: Fase 7 - Quality Gates
12. [ ] Sección: Fase 8 - Documentación
13. [ ] Sección: Fase 9 - Reporte Final
14. [ ] Sección: Tracking automático
15. [ ] Sección: Personalización por perfil
16. [ ] Sección: Ejemplos completos (4 stacks)
17. [ ] Sección: Troubleshooting
18. [ ] Revisión: Validar con skill real

---

## Criterios de Aceptación

- [ ] Documentación completa del skill creada
- [ ] Las 10 fases explicadas en detalle
- [ ] Tabla de opciones del skill
- [ ] Ejemplos de uso básico y avanzado
- [ ] Ejemplos para los 4 stacks principales
- [ ] Tracking automático explicado
- [ ] Troubleshooting con errores comunes por fase
- [ ] Screenshots o ejemplos de output

---

## Archivos

**Crear:**
- docs/skills/ (directorio)
- docs/skills/implement-us.md (~800 líneas)

---

## Notas Técnicas

- **Skill source:** skills/implement-us/skill.md
- **Phases:** skills/implement-us/phases/*.md
- **Config:** skills/implement-us/config.json
- **Perfiles:** skills/implement-us/customizations/*.json

---

## Dependencias

**Depende de:**
- TICKET-043

**Bloquea a:**
- TICKET-051

---

## Notas de Implementación

- Esta es la documentación del skill MÁS IMPORTANTE
- Debe ser exhaustiva pero clara
- Incluir ejemplos visuales de output
- Explicar el flujo completo end-to-end

---

## Resultado

_Se completará al finalizar el ticket con descripción de resultados, commits y archivos creados._
