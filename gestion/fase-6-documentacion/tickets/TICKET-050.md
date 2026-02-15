# TICKET-050: Guía de Creación de Skills

**Fase:** 6 - Documentación General
**Sprint:** 3
**Estado:** 📋 Pendiente
**Prioridad:** Baja
**Estimación:** 1 hora
**Asignado a:** Claude Code

---

## Descripción

Crear `docs/skills/creating-skills.md` para desarrolladores que quieran extender el framework creando skills custom. Esta guía debe cubrir desde la anatomía básica hasta integración con tracking.

---

## Objetivos

1. Explicar anatomía de un skill
2. Estructura de archivos requerida
3. Formato skill.md y sintaxis
4. Sistema de fases opcional
5. Integración con tracking
6. Testing de skills
7. Ejemplo completo funcional

---

## Contenido del Archivo

### Secciones Principales

1. **Anatomía de un Skill**
   - Qué es un skill de Claude Code
   - Componentes de un skill
   - Skills simples vs. complejos
   - Cuándo crear un skill

2. **Estructura de Archivos**
   ```
   .claude/skills/mi-skill/
   ├── skill.md           # Definición del skill
   ├── config.json        # Configuración (opcional)
   ├── phases/            # Fases (opcional)
   └── README.md          # Documentación
   ```

3. **Formato skill.md**
   - Front matter (metadata)
   - Secciones del skill
   - Sintaxis de instrucciones
   - Variables y placeholders
   - Ejemplos

4. **Sistema de Fases**
   - Cuándo usar fases
   - Orquestador + agentes
   - Comunicación entre fases
   - Ejemplo de skill con fases

5. **Integración con Tracking**
   - Usar TimeTracker en skills
   - Tracking de fases y tareas
   - Reportes automáticos
   - Ejemplo de código

6. **Testing de Skills**
   - Testing manual
   - Testing automatizado
   - Validación de output
   - Checklist de calidad

7. **Ejemplo Completo**
   - Skill: `/code-review`
   - Análisis de código
   - Reporte de mejoras
   - Integración con tracking

---

## Checklist de Implementación

1. [ ] Sección: Anatomía de un skill
2. [ ] Sección: Estructura de archivos
3. [ ] Sección: Formato skill.md (sintaxis completa)
4. [ ] Sección: Sistema de fases (orquestador)
5. [ ] Sección: Integración con tracking (ejemplos de código)
6. [ ] Sección: Testing de skills (checklist)
7. [ ] Sección: Ejemplo completo (/code-review funcional)
8. [ ] Revisión: Validar que el ejemplo funciona

---

## Criterios de Aceptación

- [ ] Guía completa de creación de skills
- [ ] Anatomía explicada con diagramas
- [ ] Estructura de archivos documentada
- [ ] Formato skill.md con sintaxis completa
- [ ] Sistema de fases explicado
- [ ] Integración con tracking con código de ejemplo
- [ ] Ejemplo completo de skill funcional
- [ ] Checklist de validación

---

## Archivos

**Crear:**
- docs/skills/creating-skills.md (~400 líneas)

---

## Notas Técnicas

- **Skill implement-us:** skills/implement-us/skill.md (ejemplo de referencia)
- **Tracking:** tracking/time_tracker.py
- **Skills existentes:** .claude/skills/

---

## Dependencias

**Depende de:**
- TICKET-043

**Bloquea a:**
- TICKET-051

---

## Notas de Implementación

- Audiencia: Desarrolladores avanzados
- Incluir código Python ejecutable
- Ejemplo debe ser completo y funcional
- Explicar mejores prácticas

---

## Resultado

_Se completará al finalizar el ticket con descripción de resultados, commits y archivos creados._
