# TICKET-019: Análisis del skill implement-us actual y planificación de generalización

**Fase:** 3 - Generalización de Skills
**Sprint:** 2
**Estado:** ✅ COMPLETADO
**Prioridad:** Crítica
**Estimación:** 1.5 horas
**Asignado a:** Claude Code

## Descripción

Realizar un análisis exhaustivo del skill `implement-us.md` actual ubicado en `_work/from-simapp/skills/` para identificar todas las referencias específicas a PyQt/MVC que deben ser generalizadas. Generar un documento de mapeo de cambios necesarios.

Este análisis es el fundamento para la generalización del skill y debe identificar:
- Referencias hardcodeadas a tecnologías específicas
- Paths específicos del proyecto
- Patrones arquitectónicos específicos
- Nombres de componentes específicos
- Variables que deben ser parametrizadas

## Criterios de Aceptación

- [ ] Archivo `implement-us.md` leído y analizado completamente
- [ ] Lista completa de referencias específicas identificadas (PyQt, MVC, Factory, Coordinator, Panel, Display, etc.)
- [ ] Documento de mapeo creado mostrando:
  - [ ] Qué referencias específicas existen
  - [ ] Qué variables las reemplazarán
  - [ ] Ejemplos de valores para diferentes perfiles
- [ ] Identificación de secciones que necesitan lógica condicional según perfil
- [ ] Estimación de complejidad para cada sección a generalizar
- [ ] Plan de trabajo detallado para la generalización

## Dependencias

- **Depende de:** Fase 2 completada (instalador funcionando)
- **Bloquea a:** TICKET-020 (estructura directorios), TICKET-021 (generalización)

## Notas Técnicas

### Archivos a Analizar

1. `_work/from-simapp/skills/implement-us.md` (707 líneas)
2. `_work/from-simapp/skills/implement-us-config.json` (106 líneas)

### Referencias a Buscar

Usar grep para encontrar:
```bash
grep -n "MVC\|PyQt\|Factory\|Coordinator\|Panel\|Display\|Climatizador" _work/from-simapp/skills/implement-us.md
grep -n "app/presentacion/paneles" _work/from-simapp/skills/implement-us.md
grep -n "ModeloBase\|pytest-qt\|qapp\|qtbot" _work/from-simapp/skills/implement-us.md
```

### Formato del Documento de Mapeo

Crear archivo: `gestion/fase-3-generalizacion-skills/ANALISIS-GENERALIZACION.md`

```markdown
# Análisis de Generalización - implement-us

## Referencias Específicas Encontradas

### 1. Arquitectura (MVC)
- **Líneas:** X, Y, Z
- **Contexto:** "Panel Display (MVC)"
- **Variable:** {ARCHITECTURE_PATTERN}
- **Valores posibles:** mvc, mvt, layered, clean-architecture, generic

### 2. Tipo de Componente
- **Líneas:** A, B, C
- **Contexto:** "Panel", "Display"
- **Variable:** {COMPONENT_TYPE}
- **Valores posibles:** Panel, View, Service, Controller, Component

[... etc ...]

## Secciones que Necesitan Cambios

### Fase 1: Generación BDD
- Línea X: Cambiar "Panel" por {COMPONENT_TYPE}
- Línea Y: Parametrizar path de componentes

[... etc ...]

## Variables a Crear

| Variable | Propósito | Valor Default | Perfiles que Override |
|----------|-----------|---------------|----------------------|
| {ARCHITECTURE_PATTERN} | Patrón arquitectónico | generic | pyqt-mvc, django-mvt |
| {COMPONENT_TYPE} | Tipo de componente | Component | Todos |

## Plan de Trabajo

1. Crear variables en config.json base
2. Generalizar Fase 0-2 (contexto, BDD, plan)
3. Generalizar Fase 3-6 (implementación, tests)
4. Generalizar Fase 7-9 (quality gates, docs, reporte)
5. Validación con perfiles de prueba
```

## Checklist de Implementación

- [x] Leer `_work/from-simapp/skills/implement-us.md` completo
- [x] Leer `_work/from-simapp/skills/implement-us-config.json` completo
- [x] Ejecutar grep para encontrar referencias específicas
- [x] Crear documento `ANALISIS-GENERALIZACION.md`
- [x] Documentar todas las referencias encontradas
- [x] Mapear referencias a variables
- [x] Identificar valores posibles por perfil
- [x] Crear plan de trabajo secuencial
- [x] Revisar con MIGRATION_NOTES.md para completeness
- [x] Estimar complejidad de cada cambio

## Resultado

**Fecha de Completado:** 2026-02-09

### Análisis Generado

**Documento creado:** `docs/analysis/TICKET-019-analysis.md` (630 líneas)

El análisis completo incluye:
- Identificación sistemática de 47 referencias específicas
- Análisis detallado de las 9 fases del skill
- Matriz de generalización con 8 variables propuestas
- Estrategia completa de generalización con ejemplos de configs
- Ejemplos de perfiles para PyQt, FastAPI, Django y Generic
- Plan de trabajo detallado para siguientes tickets

### Estadísticas

- Total de referencias específicas encontradas: **47**
- Variables a crear: **8** principales
- Líneas a modificar: **170 de 707 (24%)**
- Complejidad estimada: **Media-Alta**
- Fases críticas identificadas: Fase 2, 3 y 5

### Commit

```
ba7950e docs(fase-3): completar análisis del skill implement-us (TICKET-019)
```

**Estado:** ✅ COMPLETADO
