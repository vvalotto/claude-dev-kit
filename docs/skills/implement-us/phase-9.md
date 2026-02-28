# Fase 9: Reporte Final

Genera el reporte completo de la implementación consolidando datos de todas las fases anteriores. Cierra el tracking completo de la US.

**Aprobación requerida:** No (el skill termina automáticamente al generar el reporte).

---

## Para el usuario

### Qué hace esta fase

1. Verifica que existen `docs/plans/{US_ID}-plan.md` y `quality/reports/{US_ID}-quality.json`
2. Lee los umbrales reales desde `quality.json` (no los reconstruye de memoria)
3. Genera `docs/reports/{US_ID}-report.md` con el resumen completo
4. Presenta el reporte completo en la conversación con la ruta del archivo
5. Cierra el tracking completo de la US (`end-phase 9` + `end-tracking`)

### Qué esperar

El reporte consolida todo el trabajo de las fases anteriores en un documento estructurado. Es la evidencia formal de que la historia de usuario fue implementada correctamente.

Las métricas del reporte provienen directamente de `quality/reports/{US_ID}-quality.json` — no se inventan ni se reconstruyen desde memoria.

### Contenido del reporte

```markdown
# Reporte de Implementación: {US_ID}

## Resumen Ejecutivo
- Historia de Usuario: {US_ID} - {US_TITLE}
- Puntos estimados: {STORY_POINTS}
- Tiempo real: {ACTUAL_TIME}
- Estado: ✅ COMPLETADO
- Fecha: {COMPLETION_DATE}

## Componentes Implementados
[Lista con checkmarks y rutas]

## Métricas de Calidad
| Métrica | Valor | Umbral | Estado |
| Pylint  | X.X/10 | ≥ Y | ✅ |
| CC máx/función | N | ≤ M | ✅ |
| MI promedio | XX | > YY | ✅ |
| Coverage | XX% | ≥ YY% | ✅ |

## Tests Implementados
- Unitarios: N tests
- Integración: M tests
- BDD: K escenarios
- Total: N+M+K tests ✅

## Archivos Creados
[Lista completa con líneas de código]

## Criterios de Aceptación
- [x] {criterio 1}
- [x] {criterio 2}

## Próximos Pasos
[Sugerencias para continuación]
```

### Sobre `end-tracking`

`end-tracking` es el cierre del tracking completo de la US. A diferencia de `end-phase N` (que cierra solo la fase actual), calcula el tiempo total acumulado en todas las fases, guarda el histórico en `.claude/tracking/` y genera el reporte de tiempo final. Se ejecuta **después** de `end-phase 9`, nunca en lugar de él.

---

## Referencia técnica

### Entradas

| Entrada | Tipo | Requerida | Fuente |
|---|---|---|---|
| `docs/plans/{US_ID}-plan.md` | Artefacto | ✅ Sí | Fases 2-3-8 |
| `quality/reports/{US_ID}-quality.json` | Artefacto | ✅ Sí | Fase 7 |
| `docs/plans/{US_ID}-context.md` | Artefacto | ❌ Opcional | Fase 0 |
| Templates de reporte por stack | `templates/reporting/` | ❌ Opcional | Framework |

### Salidas

| Salida | Tipo | Descripción |
|---|---|---|
| `docs/reports/{US_ID}-report.md` | Artefacto físico | Reporte completo de implementación |
| Reporte presentado en conversación | En conversación | Contenido completo + ruta del archivo |
| Tracking cerrado | Sistema | `end-phase 9` + `end-tracking` |

### Templates

| Template | Ruta en `config.json` | Uso |
|---|---|---|
| Reporte de implementación | `templates/reporting/implementation-report.md` | Alternativa al template embebido en la fase |

El template por stack (PyQt, FastAPI, Flask REST, Flask Webapp, Generic) está embebido en el archivo de fase. Los templates externos son alternativos.

### Artefactos

| Artefacto | Operación | Ruta |
|---|---|---|
| `{US_ID}-report.md` | **Genera** | `docs/reports/{US_ID}-report.md` |
| `{US_ID}-quality.json` | **Lee** | `quality/reports/{US_ID}-quality.json` |
| `{US_ID}-plan.md` | **Lee** | `docs/plans/{US_ID}-plan.md` |

### Lectura de umbrales desde `quality.json`

Antes de completar el template del reporte, se leen los umbrales reales:

```bash
cat quality/reports/{US_ID}-quality.json | jq '.umbrales'
```

Mapeo de campos:

| Campo en `quality.json → umbrales` | Placeholder en el template |
|---|---|
| `pylint_min` | `{PYLINT_MIN}` |
| `cc_max` | `{CC_MAX}` |
| `mi_min` | `{MI_MIN}` |
| `coverage_min` | `{COVERAGE_MIN}` |

Los valores hardcodeados en el template se reemplazan con los valores reales del `quality.json`.

### Secuencia de cierre de tracking

```bash
# 1. Cerrar la fase 9
python .claude/tracking/track.py end-phase 9

# 2. Cerrar el tracking completo de la US
python .claude/tracking/track.py end-tracking
```

`end-tracking` es el único punto de todo el skill donde se invoca ese subcomando.

### Convenciones

- Las métricas del reporte se leen desde `quality.json`, nunca se reconstruyen desde memoria o desde las herramientas.
- El reporte debe presentarse en la conversación con su contenido completo y la ruta del archivo.
- `end-tracking` se ejecuta **después** de `end-phase 9`.
- El checklist de salida requiere verificar que `docs/reports/{US_ID}-report.md` existe en disco con `ls`.

### Dependencias

| Dirección | Fase | Qué provee |
|---|---|---|
| ← anterior | Fase 7 | `quality.json` con métricas reales |
| ← anterior | Fase 8 | Plan actualizado con tareas completadas |
| → cierre | — | El skill ha completado todas sus fases |

### Checklist de salida

- [ ] `docs/reports/{US_ID}-report.md` existe en disco
- [ ] El reporte incluye métricas reales leídas desde `quality.json` (no reconstruidas)
- [ ] El reporte fue presentado en la conversación con la ruta del archivo
- [ ] `end-phase 9` ejecutado
- [ ] `end-tracking` ejecutado

### Estado en v1.3

| ID | Descripción | Resolución |
|---|---|---|
| D9-1 | El subcomando `end-tracking` no estaba documentado en ningún archivo del skill | Se documentó en `skill.md` y en esta fase: qué hace, cuándo usarlo, y que es el único punto donde aparece |
| D9-2 | Los templates de reporte tenían placeholders `{PYLINT_MIN}` etc. pero no había instrucción de cómo obtener esos valores | Se agregó instrucción explícita: leer `quality.json → umbrales` con `jq` antes de completar el template; tabla de mapeo campo → placeholder incluida |

---

**Fase anterior:** [Fase 8: Documentación](phase-8.md)
**Inicio:** [Volver al índice](index.md)

**El skill implement-us ha completado todas sus fases.** ✅
