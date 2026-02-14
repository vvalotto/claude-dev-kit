# TICKET-030: Análisis Exhaustivo de Templates y Planificación

**Fase:** 4 - Generalización de Templates
**Sprint:** 2
**Estado:** ✅ COMPLETADO
**Prioridad:** Alta
**Estimación:** 1 hora
**Asignado a:** Claude Code

---

## Descripción

Realizar un análisis exhaustivo de los 4 templates existentes en `_work/from-simapp/templates/` para identificar todas las referencias específicas a PyQt/MVC/Coordinator/Factory que necesitan ser generalizadas.

Similar al TICKET-019 (análisis del skill), este ticket debe producir un documento detallado con:
1. Inventario completo de referencias específicas por archivo
2. Propuesta de variables nuevas a agregar al sistema
3. Estrategia de generalización por template
4. Plan de snippets por perfil

---

## Criterios de Aceptación

- [x] Los 4 templates analizados línea por línea
- [ ] Documento de análisis creado en `docs/analysis/TICKET-030-analysis.md`
- [ ] Todas las referencias específicas identificadas con número de línea
- [ ] Variables nuevas propuestas con ejemplos de valores por perfil
- [ ] Estrategia de snippets documentada
- [ ] Matriz de impacto: template x perfil (qué cambios aplican a cada combinación)
- [ ] Estimaciones refinadas por ticket de implementación

---

## Dependencias

**Depende de:**
- ✅ TICKET-027: Testing de perfiles (completado)
- ✅ Fase 3 completada

**Bloquea a:**
- TICKET-031: Crear estructura templates/
- Todos los tickets de implementación (032-037)

---

## Checklist de Análisis

### Inventario de Referencias

- [ ] **bdd-scenario.feature**:
  - [ ] Identificar referencias específicas en Background
  - [ ] Verificar si variables actuales son suficientes
  - [ ] Proponer mejoras

- [ ] **implementation-plan.md**:
  - [ ] Listar todas las menciones a Factory/Coordinator/Compositor
  - [ ] Identificar secciones específicas de PyQt
  - [ ] Mapear variables necesarias

- [ ] **implementation-report.md**:
  - [ ] Listar referencias específicas (Factory, RPi, señales)
  - [ ] Identificar bloques que necesitan ser condicionales
  - [ ] Proponer snippets por perfil

- [ ] **test-unit.py**:
  - [ ] Identificar imports específicos de PyQt
  - [ ] Analizar clases de tests específicas (TestSignals)
  - [ ] Proponer estructura genérica

### Propuesta de Variables

- [ ] Lista completa de variables nuevas con:
  - [ ] Nombre de variable
  - [ ] Propósito/descripción
  - [ ] Valores por perfil (pyqt-mvc, fastapi-rest, flask-rest, flask-webapp, generic-python)
  - [ ] Ejemplo de uso en template

### Estrategia de Snippets

- [ ] Definir qué contenido va en snippets vs variables simples
- [ ] Crear estructura JSON para snippets en perfiles
- [ ] Documentar cómo el skill elige snippets

### Matriz de Impacto

| Template | pyqt-mvc | fastapi-rest | flask-rest | flask-webapp | generic-python |
|----------|----------|--------------|------------|--------------|----------------|
| bdd-scenario.feature | ? | ? | ? | ? | ? |
| implementation-plan.md | ? | ? | ? | ? | ? |
| implementation-report.md | ? | ? | ? | ? | ? |
| test-unit.py | ? | ? | ? | ? | ? |

---

## Entregable

**Documento:** `docs/analysis/TICKET-030-analysis.md`

**Estructura esperada:**
```markdown
# Análisis de Templates para Generalización

## Executive Summary
- Total de referencias específicas encontradas
- Variables nuevas propuestas
- Estrategia de generalización

## 1. Template: bdd-scenario.feature
### Referencias Específicas
### Variables Necesarias
### Estrategia de Generalización

## 2. Template: implementation-plan.md
### Referencias Específicas
### Variables Necesarias
### Snippets Propuestos

## 3. Template: implementation-report.md
### Referencias Específicas
### Variables Necesarias
### Snippets Propuestos

## 4. Template: test-unit.py
### Referencias Específicas
### Variables Necesarias
### Estrategia de Generalización

## Sistema de Variables Expandido
| Variable | Propósito | Valores por Perfil |

## Sistema de Snippets
Estructura JSON y ejemplos

## Matriz de Impacto
Template x Perfil

## Plan de Implementación
Orden recomendado de tickets
```

---

## Notas Técnicas

- Usar `grep` para búsquedas sistemáticas de términos clave: Factory, Coordinator, PyQt, Signal, etc.
- Comparar templates con ejemplos reales de proyectos (app_termostato, webapp_termostato)
- Considerar backwards compatibility si templates ya están en uso

---

## Resultado

✅ **COMPLETADO** - 2026-02-14

### Documento Generado

**Ubicación:** `docs/analysis/TICKET-030-analysis.md`
**Tamaño:** ~1,200 líneas / ~8,500 palabras

### Hallazgos Principales

1. **47 referencias específicas** identificadas en 4 templates
2. **7 variables nuevas** propuestas (total 15 con las existentes)
3. **7 snippets** diseñados × 5 perfiles = 35 definiciones necesarias
4. **Estimación refinada:** 8h → 9.5h (+1.5h por complejidad de snippets)

### Decisiones Clave

- **Orden recomendado:** TICKET-035 (test-unit.py) ANTES de TICKET-034 (report)
- **Mecanismo de snippets:** Sintaxis `{SNIPPET:snippet_id}` en templates
- **Validación crítica:** TICKET-036 debe ejecutar pytest real, no solo validar sintaxis

### Nivel de Complejidad por Template

- ✅ **bdd-scenario.feature:** Baja (2 variables)
- 🟡 **implementation-plan.md:** Media (2 vars + 1 snippet)
- 🔴 **implementation-report.md:** Alta (1 var + 2 snippets grandes)
- 🔴 **test-unit.py:** Alta (2 vars + 4 snippets con código Python)

### Próximo Paso

Iniciar TICKET-031: Crear estructura `templates/` y migrar archivos base.
