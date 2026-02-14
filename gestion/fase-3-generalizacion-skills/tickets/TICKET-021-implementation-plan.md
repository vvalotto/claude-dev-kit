# TICKET-021: Plan de Implementación Incremental

**Ticket Principal:** TICKET-021 - Generalizar implement-us.md
**Fecha Plan:** 2026-02-10
**Estrategia:** Implementación incremental por fases
**Estimación Total:** 4 horas

---

## 📊 Dimensión del Problema

- **707 líneas** a generalizar
- **47 referencias específicas** identificadas
- **9 fases** diferentes del skill (Fase 0 a Fase 9)
- **4 dimensiones** de acoplamiento:
  - Stack tecnológico (PyQt6)
  - Patrón arquitectónico (MVC + Factory/Coordinator)
  - Rutas hardcodeadas
  - Framework de testing (pytest-qt)

---

## ⚠️ Riesgos de Implementación Monolítica

1. **Error de concepto:** Si la estrategia de generalización tiene un flaw, afectaría las 707 líneas
2. **Difícil debugging:** Imposible identificar dónde falló
3. **No hay validación intermedia:** Todo o nada
4. **Impacta tickets posteriores:** TICKET-022 a TICKET-027 dependen de esto

---

## 🎯 Estrategia: División en 10 Subtareas Incrementales

Cada subtarea incluye:
- ✅ Objetivo específico
- ⏱️ Estimación de tiempo
- 🎯 Checkpoint de validación
- 💾 Commit incremental

---

## Subtarea 0: Setup y Validación de Concepto

**Estimación:** 30 minutos
**Prioridad:** Crítica (valida el concepto completo)

### Objetivo

Crear estructura base del archivo `skill.md` y validar el concepto de reemplazo de variables.

### Tareas

1. Crear archivo base `skills/implement-us/skill.md`
2. Agregar header del skill
3. Crear sección "Variables Disponibles" con tabla completa:
   - `{ARCHITECTURE_PATTERN}` - Patrón arquitectónico
   - `{COMPONENT_TYPE}` - Tipo de componente
   - `{COMPONENT_PATH}` - Ruta base componentes
   - `{TEST_FRAMEWORK}` - Framework de testing
   - `{BASE_CLASS}` - Clase base
   - `{DOMAIN_CONTEXT}` - Contexto de dominio
   - `{PROJECT_ROOT}` - Raíz del proyecto
   - `{PRODUCT}` - Nombre del producto
4. Validar concepto en 1-2 párrafos de prueba

### Checkpoint

- ¿El concepto de variables es claro?
- ¿La tabla documenta correctamente cada variable?
- ¿El formato es legible?

### Criterios de Aceptación

- [ ] Archivo `skills/implement-us/skill.md` creado
- [ ] Sección de variables completa con 8 variables documentadas
- [ ] Ejemplos de uso incluidos en la tabla
- [ ] Validación de concepto realizada

---

## Subtarea 1: Generalizar Fase 0 - Validación de Contexto

**Estimación:** 20 minutos
**Depende de:** Subtarea 0

### Objetivo

Generalizar la fase de validación de contexto para que sea framework-agnostic.

### Tareas

1. Copiar contenido de Fase 0 del archivo original
2. Reemplazar "MVC, Factory, Coordinator" por `{PATTERNS}`
3. Reemplazar referencia a "ADR-003" por `{ARCHITECTURE_DOC}`
4. Generalizar detección de estructura de proyecto
5. Parametrizar búsqueda de documentación

### Checkpoint

- ¿La validación funciona para cualquier patrón arquitectónico?
- ¿No hay referencias hardcodeadas a rutas específicas?

### Criterios de Aceptación

- [ ] Fase 0 copiada y adaptada en skill.md
- [ ] No hay referencias a MVC/Factory/Coordinator específicas
- [ ] Paths de documentación parametrizados
- [ ] Instrucciones claras para cualquier stack

---

## Subtarea 2: Generalizar Fase 1 - BDD

**Estimación:** 15 minutos
**Depende de:** Subtarea 1

### Objetivo

Generalizar generación de escenarios BDD (ya es mayormente genérico).

### Tareas

1. Copiar contenido de Fase 1
2. Ajustar ejemplos de dominio (quitar referencias a termostato)
3. Usar ejemplos genéricos o múltiples dominios
4. Validar que el proceso es agnóstico

### Checkpoint

- ¿Los ejemplos son genéricos o hay múltiples ejemplos?
- ¿El template BDD es framework-agnostic?

### Criterios de Aceptación

- [ ] Fase 1 copiada en skill.md
- [ ] Ejemplos generalizados (no específicos a termostato)
- [ ] Template BDD sin referencias específicas

---

## Subtarea 3: Generalizar Fase 2 - Plan de Implementación

**Estimación:** 45 minutos
**Prioridad:** CRÍTICA (fase más compleja)
**Depende de:** Subtarea 2

### Objetivo

Generalizar la generación del plan de implementación para soportar múltiples patrones arquitectónicos.

### Tareas

1. Copiar contenido de Fase 2
2. Reemplazar estructura MVC hardcodeada por `{ARCHITECTURE_PATTERN}`
3. Parametrizar rutas con `{COMPONENT_PATH}`
4. Reemplazar componentes específicos (Panel, Display) por `{COMPONENT_TYPE}`
5. Agregar ejemplos condicionales para cada patrón:
   - **MVC:** modelo.py, vista.py, controlador.py
   - **MVT:** model.py, view.py, template.html
   - **Layered:** entity.py, service.py, repository.py
   - **Generic:** implementation.py
6. Crear sección de instrucciones según perfil

### Checkpoint

- ¿El plan se puede generar para MVC, MVT, Layered y Generic?
- ¿Las rutas son completamente parametrizadas?
- ¿Los ejemplos cubren los 4 perfiles?

### Criterios de Aceptación

- [ ] Fase 2 completamente generalizada
- [ ] 4 ejemplos de patrones arquitectónicos incluidos
- [ ] Todas las rutas parametrizadas con `{COMPONENT_PATH}`
- [ ] No hay referencias a Panel/Display específicos
- [ ] Instrucciones condicionales según `{ARCHITECTURE_PATTERN}`

---

## Subtarea 4: Generalizar Fase 3 - Implementación

**Estimación:** 30 minutos
**Depende de:** Subtarea 3

### Objetivo

Generalizar guías de implementación guiada por tareas.

### Tareas

1. Copiar contenido de Fase 3
2. Reemplazar ejemplos de código específicos (DisplayModelo)
3. Usar variables: `{COMPONENT_NAME}`, `{BASE_CLASS}`, `{COMPONENT_TYPE}`
4. Generalizar referencias a componentes del proyecto
5. Crear guías condicionales según patrón

### Checkpoint

- ¿Las guías de implementación son claras para cualquier stack?
- ¿No hay referencias a DisplayModelo u otros componentes específicos?

### Criterios de Aceptación

- [ ] Fase 3 generalizada en skill.md
- [ ] Ejemplos de código parametrizados
- [ ] Variables `{BASE_CLASS}`, `{COMPONENT_TYPE}` usadas
- [ ] Referencias a proyectos específicos eliminadas

---

## Subtarea 5: Generalizar Fase 4 - Tests Unitarios

**Estimación:** 30 minutos
**Depende de:** Subtarea 4

### Objetivo

Generalizar testing unitario para múltiples frameworks.

### Tareas

1. Copiar contenido de Fase 4
2. Reemplazar pytest-qt por `{TEST_FRAMEWORK}`
3. Crear secciones condicionales por perfil:
   - **PyQt/MVC:** pytest + pytest-qt (fixtures: qapp, qtbot)
   - **FastAPI:** pytest + httpx (fixtures: client, test_db)
   - **Django:** pytest-django (fixtures: db, client)
   - **Generic:** pytest estándar
4. Generalizar ejemplos de tests
5. Parametrizar fixtures según perfil

### Checkpoint

- ¿El testing es agnóstico de framework?
- ¿Los ejemplos cubren los 4 perfiles?

### Criterios de Aceptación

- [ ] Fase 4 generalizada
- [ ] Variable `{TEST_FRAMEWORK}` usada
- [ ] 4 perfiles de testing documentados
- [ ] Ejemplos de fixtures condicionales
- [ ] No hay referencias específicas a pytest-qt

---

## Subtarea 6: Generalizar Fase 5 - Tests de Integración

**Estimación:** 20 minutos
**Depende de:** Subtarea 5

### Objetivo

Generalizar tests de integración (similar a Fase 4).

### Tareas

1. Copiar contenido de Fase 5
2. Aplicar mismo patrón que Fase 4
3. Generalizar mocks y fixtures
4. Parametrizar según `{TEST_FRAMEWORK}`

### Checkpoint

- ¿Consistente con Fase 4?
- ¿Tests de integración agnósticos?

### Criterios de Aceptación

- [ ] Fase 5 generalizada
- [ ] Consistente con estrategia de Fase 4
- [ ] Mocks parametrizados según perfil

---

## Subtarea 7: Generalizar Fase 6 - Validación BDD

**Estimación:** 15 minutos
**Depende de:** Subtarea 6

### Objetivo

Generalizar validación BDD (ya mayormente genérico).

### Tareas

1. Copiar contenido de Fase 6
2. Verificar que no hay referencias específicas
3. Ajustar si es necesario

### Checkpoint

- ¿Validación BDD framework-agnostic?

### Criterios de Aceptación

- [ ] Fase 6 copiada y validada
- [ ] Sin referencias específicas

---

## Subtarea 8: Generalizar Fase 7 - Quality Gates

**Estimación:** 10 minutos
**Depende de:** Subtarea 7

### Objetivo

Validar que Quality Gates es genérico (ya debería serlo).

### Tareas

1. Copiar contenido de Fase 7
2. Verificar que pylint, coverage, complejidad son genéricos
3. Confirmar que no hay ajustes necesarios

### Checkpoint

- ¿Quality gates agnósticos de framework?

### Criterios de Aceptación

- [ ] Fase 7 copiada y validada
- [ ] Métricas de calidad genéricas

---

## Subtarea 9: Generalizar Fases 8-9 - Documentación y Reporte

**Estimación:** 20 minutos
**Depende de:** Subtarea 8

### Objetivo

Generalizar documentación y reporte final.

### Tareas

1. Copiar contenido de Fases 8 y 9
2. Generalizar templates de documentación
3. Parametrizar referencias a componentes
4. Asegurar reportes framework-agnostic

### Checkpoint

- ¿Documentación y reportes genéricos?

### Criterios de Aceptación

- [ ] Fases 8 y 9 generalizadas
- [ ] Templates de documentación parametrizados
- [ ] Reportes sin referencias específicas

---

## Subtarea 10: Verificación Final y Testing

**Estimación:** 25 minutos
**Depende de:** Subtarea 9

### Objetivo

Validar que el archivo completo está correctamente generalizado.

### Tareas

1. Ejecutar greps de verificación:
   ```bash
   # No debe encontrar nada:
   grep -i "Panel\|Display\|Climatizador" skills/implement-us/skill.md
   grep "app/presentacion/paneles" skills/implement-us/skill.md
   grep "ModeloBase" skills/implement-us/skill.md
   grep "pytest-qt" skills/implement-us/skill.md

   # Debe encontrar variables:
   grep "{ARCHITECTURE_PATTERN}\|{COMPONENT_TYPE}" skills/implement-us/skill.md
   ```
2. Lectura completa del archivo
3. Validación contra checklist del TICKET-021
4. Actualizar estadísticas en TICKET-021.md
5. Commit final

### Checkpoint

- ¿Todos los greps pasan?
- ¿Lectura completa sin encontrar referencias específicas?
- ¿Checklist del ticket completado?

### Criterios de Aceptación

- [ ] Greps de verificación ejecutados (todos OK)
- [ ] Lectura completa realizada
- [ ] Checklist de TICKET-021 completado
- [ ] Estadísticas actualizadas en TICKET-021.md
- [ ] Commit final creado

---

## 📋 Tracking de Progreso

### Estado Actual

```
Total: 4/10 fases completadas (40%)
Tiempo invertido: 1.58h / 4h estimadas
Arquitectura: ✅ MODULAR (Orquestador + Agentes)
```

### Checklist de Subtareas

- [x] **Subtarea 0:** Setup y concepto (30 min) ✅ Commit: efe6bcd (refactor modular)
- [x] **Subtarea 1:** Fase 0 - Validación (20 min) ✅ Commit: efe6bcd (refactor modular)
- [x] **Subtarea 2:** Fase 1 - BDD (15 min) ✅ Commit: efe6bcd (refactor modular)
- [x] **Subtarea 3:** Fase 2 - Planning (45 min) ✅ Commit: 2389e39 ← **CRÍTICA COMPLETADA**

**NOTA IMPORTANTE:** La arquitectura fue reestructurada a modular (commit efe6bcd).
- skill.md ahora es ORQUESTADOR
- Fases 0-2 creadas en phases/phase-X.md
- Subtareas 4-9 continuarán creando archivos phase-X.md

- [ ] **Subtarea 4:** Fase 3 - Implementación (30 min) ← **SIGUIENTE**
- [ ] **Subtarea 4:** Fase 3 - Implementación (30 min)
- [ ] **Subtarea 5:** Fase 4 - Tests Unit (30 min)
- [ ] **Subtarea 6:** Fase 5 - Tests Integración (20 min)
- [ ] **Subtarea 7:** Fase 6 - BDD Validation (15 min)
- [ ] **Subtarea 8:** Fase 7 - Quality Gates (10 min)
- [ ] **Subtarea 9:** Fases 8-9 - Docs/Reporte (20 min)
- [ ] **Subtarea 10:** Verificación final (25 min)

---

## ✅ Ventajas de Este Enfoque

1. **Commits incrementales:** Un commit por subtarea = trazabilidad perfecta
2. **Validación continua:** Checkpoint después de cada fase
3. **Detección temprana de problemas:** Si algo falla en Fase 2, no afecta Fase 3-9
4. **Flexibilidad:** Posibilidad de pausar/retomar en cualquier punto
5. **Menor carga cognitiva:** Foco en una fase a la vez
6. **Validación de concepto temprana:** Subtarea 0 valida antes de invertir 4 horas

---

## 🎯 Próximo Paso

**Iniciar con Subtarea 0** para validar el concepto de variables antes de tocar las 9 fases del skill.

---

**Documento creado:** 2026-02-10
**Última actualización:** 2026-02-10
