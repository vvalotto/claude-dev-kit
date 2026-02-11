# TICKET-021: Generalizar implement-us.md (remover referencias MVC/PyQt)

**Fase:** 3 - Generalización de Skills
**Sprint:** 2
**Estado:** EN PROGRESO (60% completado - 6/10 subtareas)
**Plan de Implementación:** Ver [TICKET-021-implementation-plan.md](./TICKET-021-implementation-plan.md)
**Prioridad:** Crítica
**Estimación:** 4 horas
**Asignado a:** Claude Code

## Progreso de Subtareas

- [x] **Subtarea 0:** Estructura base de skill.md con sistema de variables ✅ (commit e9e09c9)
- [x] **Subtarea 1:** Generalizar Fase 0 - Validación de Contexto ✅ (commit 89bdfb7)
- [x] **Subtarea 2:** Reestructurar a arquitectura modular (orquestador + phases/) ✅ (commit efe6bcd)
- [x] **Subtarea 3:** Generalizar Fase 2 - Plan de Implementación ✅ (commit 2389e39)
- [x] **Subtarea 4:** Generalizar Fase 3 - Implementación ✅ (commit 94920b6)
- [x] **Subtarea 5:** Generalizar Fase 4 - Tests Unitarios ✅
- [ ] **Subtarea 6:** Generalizar Fase 5 - Tests de Integración
- [ ] **Subtarea 7:** Generalizar Fases 6-9 (finales)
- [ ] **Subtarea 8:** Sincronizar orquestador (skill.md)
- [ ] **Subtarea 9:** Validación final

## Descripción

Generalizar el archivo `implement-us.md` desde su implementación específica de PyQt/MVC a un skill agnóstico de tecnología mediante el reemplazo de referencias hardcodeadas por variables parametrizables.

Este es el ticket más crítico de la Fase 3, ya que el skill es el componente core del framework.

## Criterios de Aceptación

- [ ] Todas las referencias a "MVC" reemplazadas por `{ARCHITECTURE_PATTERN}`
- [ ] Todas las referencias a "Panel", "Display" reemplazadas por `{COMPONENT_TYPE}`
- [ ] Todas las referencias a paths específicos (`app/presentacion/paneles/`) reemplazadas por `{COMPONENT_PATH}`
- [ ] Referencias a PyQt6 generalizadas o movidas a sección condicional
- [ ] Referencias a Factory/Coordinator/ModeloBase generalizadas
- [ ] Instrucciones que lean configuración desde `config.json`
- [ ] Ejemplos genéricos o múltiples ejemplos por stack
- [ ] Documentación de variables al inicio del skill
- [ ] Testing manual con al menos 2 perfiles diferentes
- [ ] Archivo final: `skills/implement-us/skill.md`

## Dependencias

- **Depende de:** TICKET-019 (análisis), TICKET-020 (estructura directorios)
- **Bloquea a:** TICKET-027 (testing), Fase 4 (templates)

## Notas Técnicas

### Archivo Origen

`_work/from-simapp/skills/implement-us.md` (707 líneas)

### Archivo Destino

`skills/implement-us/skill.md`

### Estrategia de Generalización

**1. Agregar sección de variables al inicio:**

```markdown
# Skill: implement-us

## Variables Disponibles

Este skill utiliza las siguientes variables definidas en `config.json`:

| Variable | Descripción | Valor Default | Ejemplo |
|----------|-------------|---------------|---------|
| {ARCHITECTURE_PATTERN} | Patrón arquitectónico | generic | mvc, mvt, layered |
| {COMPONENT_TYPE} | Tipo de componente | Component | Panel, View, Service |
| {COMPONENT_PATH} | Ruta base componentes | src/{name}/ | app/presentacion/paneles/{name}/ |
| {TEST_FRAMEWORK} | Framework de testing | pytest | pytest, unittest |
| {BASE_CLASS} | Clase base | object | ModeloBase, QWidget |

> Las variables se resuelven según el perfil instalado. Ver `.claude/skills/implement-us/config.json`
```

**2. Reemplazar referencias específicas:**

**Antes:**
```markdown
### Fase 3: Implementación

#### 1. Panel Display (MVC)
- [ ] app/presentacion/paneles/display/modelo.py (10 min)
- [ ] app/presentacion/paneles/display/vista.py (20 min)
- [ ] app/presentacion/paneles/display/controlador.py (15 min)

El modelo debe heredar de `ModeloBase` y usar el patrón Factory para dependencias.
```

**Después:**
```markdown
### Fase 3: Implementación

#### 1. {COMPONENT_NAME} ({ARCHITECTURE_PATTERN})
- [ ] {COMPONENT_PATH}/modelo.py (10 min)
- [ ] {COMPONENT_PATH}/vista.py (20 min)
- [ ] {COMPONENT_PATH}/controlador.py (15 min)

> **Nota:** La estructura de archivos depende del patrón arquitectónico configurado.
> - **MVC:** modelo.py, vista.py, controlador.py
> - **MVT:** model.py, view.py, template.html
> - **Layered:** entity.py, service.py, repository.py
> - **Generic:** implementation.py

El modelo/entidad debe heredar de `{BASE_CLASS}` según las convenciones del perfil.
```

**3. Secciones condicionales:**

```markdown
### Fase 4: Tests Unitarios

#### Testing con {TEST_FRAMEWORK}

> **Configuración según perfil:**
> - **PyQt/MVC:** pytest + pytest-qt, fixtures: qapp, qtbot
> - **FastAPI:** pytest + httpx, fixtures: client, test_db
> - **Django:** pytest-django, fixtures: db, client
> - **Generic:** pytest estándar

[Instrucciones generalizadas...]
```

### Cambios Específicos por Sección

**Fase 0: Validación de Contexto**
- Generalizar detección de estructura de proyecto
- No asumir paths específicos

**Fase 1: Generación BDD**
- Ya es mayormente genérico, solo ajustar ejemplos

**Fase 2: Plan de Implementación**
- Reemplazar estructura MVC por {ARCHITECTURE_PATTERN}
- Parametrizar paths y nombres de componentes

**Fases 3-6: Implementación y Tests**
- Reemplazar todos los patrones específicos
- Agregar ejemplos múltiples según perfil

**Fase 7: Quality Gates**
- Mantener genérico (pylint, coverage, etc.)

**Fases 8-9: Documentación y Reporte**
- Generalizar templates de documentación

## Checklist de Implementación

- [ ] Leer ANALISIS-GENERALIZACION.md (resultado TICKET-019)
- [ ] Crear copia de trabajo de implement-us.md
- [ ] Agregar sección de variables al inicio
- [ ] Reemplazar referencias a MVC por {ARCHITECTURE_PATTERN}
- [ ] Reemplazar referencias a Panel/Display por {COMPONENT_TYPE}
- [ ] Reemplazar paths hardcodeados por {COMPONENT_PATH}
- [ ] Reemplazar ModeloBase por {BASE_CLASS}
- [ ] Reemplazar pytest-qt por {TEST_FRAMEWORK}
- [ ] Generalizar Fase 0: Validación
- [ ] Generalizar Fase 1: BDD
- [ ] Generalizar Fase 2: Planning
- [ ] Generalizar Fase 3: Implementación
- [ ] Generalizar Fase 4: Tests Unitarios
- [ ] Generalizar Fase 5: Tests Integración
- [ ] Generalizar Fase 6: Validación BDD
- [ ] Generalizar Fase 7: Quality Gates
- [ ] Generalizar Fase 8: Documentación
- [ ] Generalizar Fase 9: Reporte
- [ ] Agregar ejemplos múltiples según perfil donde sea relevante
- [ ] Verificar con grep que no queden referencias específicas
- [ ] Guardar como skills/implement-us/skill.md
- [ ] Testing manual (lectura completa)

## Resultado

**Fecha de Completado:** _Pendiente_

### Estadísticas

- Líneas originales: 707
- Líneas finales: _X_
- Referencias reemplazadas: _Y_
- Variables creadas: _Z_

### Verificación

```bash
# No debe encontrar nada:
grep -i "Panel\|Display\|Climatizador" skills/implement-us/skill.md
grep "app/presentacion/paneles" skills/implement-us/skill.md
grep "ModeloBase\|pytest-qt" skills/implement-us/skill.md

# Debe encontrar variables:
grep "{ARCHITECTURE_PATTERN}\|{COMPONENT_TYPE}" skills/implement-us/skill.md
```

### Commit

_Pendiente_

**Estado:** 📋 Pendiente
