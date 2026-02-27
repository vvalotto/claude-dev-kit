# Mapa de Artefactos — implement-us

Este archivo es la **fuente de verdad** para todas las rutas y nombres de archivos generados durante la ejecución del skill `/implement-us`.

Cada fase que genera o consume un artefacto debe referenciar este mapa en lugar de definir rutas de forma ad-hoc.

---

## Estructura de Directorios

```
{PROJECT_ROOT}/
├── tests/
│   ├── features/
│   │   └── {US_ID}-{nombre}.feature
│   └── step_defs/
├── docs/
│   ├── plans/
│   │   ├── {US_ID}-context.md
│   │   └── {US_ID}-plan.md
│   └── reports/
│       └── {US_ID}-report.md
└── quality/
    └── reports/
        ├── {US_ID}-pylint.json
        ├── {US_ID}-cc.json
        ├── {US_ID}-mi.json
        ├── {US_ID}-coverage.json
        ├── {US_ID}-coverage-html/
        └── {US_ID}-quality.json
```

---

## Tabla de Artefactos

| Artefacto | Ruta | Generado en | Consumido en |
|-----------|------|-------------|--------------|
| Archivo de contexto | `docs/plans/{US_ID}-context.md` | Fase 0 | Fases 1–9 |
| Feature BDD | `tests/features/{US_ID}-{nombre}.feature` | Fase 1 | Fase 6 |
| Plan de implementación | `docs/plans/{US_ID}-plan.md` | Fase 2 | Fases 3, 9 |
| Reporte Pylint | `quality/reports/{US_ID}-pylint.json` | Fase 7 | Fase 9 |
| Reporte CC | `quality/reports/{US_ID}-cc.json` | Fase 7 | Fase 9 |
| Reporte MI | `quality/reports/{US_ID}-mi.json` | Fase 7 | Fase 9 |
| Reporte Coverage | `quality/reports/{US_ID}-coverage.json` | Fase 7 | Fase 9 |
| Coverage HTML | `quality/reports/{US_ID}-coverage-html/` | Fase 7 | — (revisión manual) |
| Reporte de calidad | `quality/reports/{US_ID}-quality.json` | Fase 7 | Fases 8, 9 |
| Reporte final | `docs/reports/{US_ID}-report.md` | Fase 9 | — (entrega) |

---

## Descripción de Artefactos

### `docs/plans/{US_ID}-context.md`
Generado en Fase 0. Registra las decisiones de ejecución del skill: tipo de HU, si aplica BDD, fases a ejecutar, perfil activo y umbrales de calidad. Todas las fases siguientes deben leerlo al inicio en lugar de asumir el contexto desde la conversación.

### `tests/features/{US_ID}-{nombre}.feature`
Generado en Fase 1. Contiene los escenarios Gherkin (Given-When-Then) aprobados por el usuario. Fase 6 lo utiliza para crear los step definitions en `tests/step_defs/` y validar que todos los escenarios pasan.

### `docs/plans/{US_ID}-plan.md`
Generado en Fase 2. Contiene el plan detallado de implementación con tareas, estimaciones de complejidad relativa y checkboxes de progreso. Fase 3 lo lee al inicio y actualiza los checkboxes después de cada tarea. Fase 9 lo utiliza para listar las tareas completadas en el reporte final.

### `quality/reports/{US_ID}-pylint.json`
Generado en Fase 7. Resultado del análisis de Pylint en formato JSON. Incluye score final y lista de issues detectados.

### `quality/reports/{US_ID}-cc.json`
Generado en Fase 7. Resultado del análisis de complejidad ciclomática con `radon cc`. Incluye CC por función y promedio total.

### `quality/reports/{US_ID}-mi.json`
Generado en Fase 7. Resultado del índice de mantenibilidad con `radon mi`. Incluye MI por archivo y promedio total.

### `quality/reports/{US_ID}-coverage.json`
Generado en Fase 7. Resultado de cobertura de tests en formato JSON (generado por `pytest-cov`). Incluye porcentaje total y detalle por archivo.

### `quality/reports/{US_ID}-quality.json`
Generado en Fase 7. Reporte consolidado con todas las métricas, umbrales del perfil activo y estado final (`APROBADO` / `RECHAZADO`). Fase 9 lo lee para incluir métricas reales en el reporte final.

### `docs/reports/{US_ID}-report.md`
Generado en Fase 9. Reporte completo de la implementación: resumen de la HU, tareas completadas, métricas de calidad reales y decisiones tomadas. Es el artefacto de cierre de la HU.

---

## Comandos de Verificación

Para verificar que un artefacto existe antes de continuar:

```bash
# Archivo de contexto (prerequisito de todas las fases)
ls docs/plans/{US_ID}-context.md

# Feature BDD (prerequisito de Fase 6)
ls tests/features/{US_ID}-*.feature

# Plan (prerequisito de Fase 3)
ls docs/plans/{US_ID}-plan.md

# Reporte de calidad (prerequisito de Fase 9)
ls quality/reports/{US_ID}-quality.json

# Reporte final (prerequisito de cierre)
ls docs/reports/{US_ID}-report.md
```

---

**Referenciado por:** `skill.md`, todos los archivos de fase
**Mantenido por:** Actualizar este archivo cuando se agreguen o modifiquen artefactos del skill
