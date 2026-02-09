# TICKET-019: Análisis del skill implement-us actual y planificación de generalización

**Fase:** 3 - Generalización de Skills
**Sprint:** 2
**Estado:** IN_PROGRESS
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

- [ ] Leer `_work/from-simapp/skills/implement-us.md` completo
- [ ] Leer `_work/from-simapp/skills/implement-us-config.json` completo
- [ ] Ejecutar grep para encontrar referencias específicas
- [ ] Crear documento `ANALISIS-GENERALIZACION.md`
- [ ] Documentar todas las referencias encontradas
- [ ] Mapear referencias a variables
- [ ] Identificar valores posibles por perfil
- [ ] Crear plan de trabajo secuencial
- [ ] Revisar con MIGRATION_NOTES.md para completeness
- [ ] Estimar complejidad de cada cambio

## Resultado

**Fecha de Completado:** _Pendiente_

### Análisis Generado

_A completar al finalizar._

### Estadísticas

- Total de referencias específicas encontradas: _X_
- Variables a crear: _Y_
- Líneas a modificar: _Z_
- Complejidad estimada: Alta/Media/Baja

### Commit

_Pendiente_

**Estado:** 🔄 En Progreso
