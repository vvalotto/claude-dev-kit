# Fase 7: Quality Gates

Valida que el código implementado cumple con los estándares de calidad del proyecto usando métricas objetivas: análisis estático (Pylint), complejidad ciclomática, índice de mantenibilidad y cobertura de tests.

**Aprobación requerida:** No (el skill avanza automáticamente cuando todas las métricas pasan).

---

## Para el usuario

### Qué hace esta fase

1. Verifica que las tres suites de tests pasan (unitarios, integración, BDD)
2. Ejecuta Pylint sobre el código de producción
3. Calcula complejidad ciclomática con radon
4. Calcula índice de mantenibilidad con radon
5. Mide cobertura de tests con pytest-cov
6. Lee los umbrales del perfil activo y compara contra los valores obtenidos
7. Genera `quality/reports/{US_ID}-quality.json` con métricas, umbrales y estado final

### Qué esperar

El estado del reporte es `APROBADO` si todas las métricas superan sus umbrales, `RECHAZADO` si alguna falla. Si una métrica no pasa, el skill corrige y re-ejecuta antes de avanzar.

### Las 4 métricas

| Métrica | Herramienta | Criterio |
|---|---|---|
| Pylint | `pylint` | Score ≥ `pylint.min_score` del perfil |
| Complejidad Ciclomática | `radon cc` | Cada función ≤ `cyclomatic_complexity.max_per_function` del perfil |
| Índice de Mantenibilidad | `radon mi` | Promedio > `maintainability_index.min_score` del perfil |
| Cobertura | `pytest-cov` | ≥ `coverage.min_percent` del perfil |

> **Nota:** El criterio de CC es por función individual, no por promedio. Una sola función con CC alta rechaza la fase aunque el promedio sea bajo.

### Umbrales por perfil

| Perfil | Pylint | CC máx | MI mín | Coverage |
|---|---|---|---|---|
| PyQt MVC | 8.0 | 12 | 20 | 90% |
| FastAPI REST | 8.5 | 10 | 25 | 95% |
| Flask REST | 8.0 | 10 | 25 | 95% |
| Flask Webapp | 8.0 | 10 | 20 | 90% |
| Generic Python | 8.0 | 10 | 20 | 95% |

Los umbrales exactos se leen siempre del perfil activo en `config.json`, no se hardcodean.

### Artefacto que produce

`quality/reports/{US_ID}-quality.json` — métricas reales, umbrales del perfil activo y estado final (`APROBADO` / `RECHAZADO`). Este archivo es la fuente de verdad para la Fase 9.

---

## Referencia técnica

### Entradas

| Entrada | Tipo | Requerida | Fuente |
|---|---|---|---|
| Archivos de código de producción | Artefactos | ✅ Sí | Fase 3 |
| `pytest tests/unit/ tests/integration/ tests/step_defs/ -v` pasando | Resultado ejecutable | ✅ Sí | Fases 4-5-6 |
| Umbrales del perfil activo | `config.json` → `quality_gates` | ✅ Sí | Perfil activo |
| `{COMPONENT_PATH}` del perfil | `config.json` → `variables.component_path` | ✅ Sí | Perfil activo |

### Salidas

| Salida | Tipo | Descripción |
|---|---|---|
| `quality/reports/{US_ID}-quality.json` | Artefacto físico | Métricas consolidadas + umbrales + estado `APROBADO`/`RECHAZADO` |
| `quality/reports/{US_ID}-pylint.json` | Artefacto físico | Output de Pylint |
| `quality/reports/{US_ID}-cc.json` | Artefacto físico | CC por función |
| `quality/reports/{US_ID}-mi.json` | Artefacto físico | MI por archivo |
| `quality/reports/{US_ID}-coverage.json` | Artefacto físico | Coverage por módulo |
| `quality/reports/{US_ID}-coverage-html/` | Directorio | Reporte HTML de coverage |

### Templates

Ninguno externo. El formato de `quality.json` está embebido en el archivo de fase:

```json
{
  "us_id": "{US_ID}",
  "fecha": "{FECHA_ISO}",
  "componente": "{COMPONENT_PATH}",
  "metricas": {
    "pylint": 0.0,
    "cc_promedio": 0.0,
    "cc_max_por_funcion": 0,
    "mi_promedio": 0.0,
    "coverage": 0.0
  },
  "umbrales": {
    "pylint_min": 0.0,
    "cc_max": 0,
    "mi_min": 0.0,
    "coverage_min": 0.0
  },
  "estado": "APROBADO",
  "observaciones": []
}
```

Los valores de `umbrales` se leen de `config.json → quality_gates` antes de generar el archivo.

### Artefactos

| Artefacto | Operación | Ruta |
|---|---|---|
| `{US_ID}-quality.json` | **Genera** | `quality/reports/{US_ID}-quality.json` |
| `{US_ID}-pylint.json` | **Genera** | `quality/reports/{US_ID}-pylint.json` |
| `{US_ID}-cc.json` | **Genera** | `quality/reports/{US_ID}-cc.json` |
| `{US_ID}-mi.json` | **Genera** | `quality/reports/{US_ID}-mi.json` |
| `{US_ID}-coverage.json` | **Genera** | `quality/reports/{US_ID}-coverage.json` |

### Comandos de validación

Los valores de `{COMPONENT_PATH}`, `{COVERAGE_THRESHOLD}` y `{PYLINT_MIN}` se leen del perfil activo antes de ejecutar:

```bash
# Leer umbrales del perfil activo
cat .claude/skills/implement-us/config.json | jq '.quality_gates'

# Coverage
pytest tests/ --cov={COMPONENT_PATH} --cov-fail-under={COVERAGE_THRESHOLD} \
  --cov-report=term --cov-report=json:quality/reports/{US_ID}-coverage.json

# Pylint
pylint {COMPONENT_PATH}/ --fail-under={PYLINT_MIN} \
  --output-format=json > quality/reports/{US_ID}-pylint.json

# CC por función (criterio: cada función ≤ max_per_function del perfil)
radon cc {COMPONENT_PATH}/ -s -j > quality/reports/{US_ID}-cc.json

# Índice de Mantenibilidad (criterio: promedio > mi_min del perfil)
radon mi {COMPONENT_PATH}/ -s -j > quality/reports/{US_ID}-mi.json
```

### Convenciones

- El tracking de fase inicia **antes** de la verificación de precondiciones.
- Los umbrales provienen siempre del perfil activo — nunca hardcodeados.
- El criterio de CC es por función individual (`max_per_function`), no por promedio.
- Si una métrica no alcanza el umbral después de correcciones razonables, se documenta como excepción justificada en el campo `observaciones` del `quality.json` y se informa al usuario antes de continuar.

### Protocolo de recuperación por métrica

| Métrica | Acción |
|---|---|
| Pylint < umbral | Corregir issues reportados en código (Fase 3), re-ejecutar pylint |
| CC > umbral | Identificar funciones con CC alta, refactorizar en Fase 3, regresar a Fase 7 |
| MI < umbral | Reducir tamaño de funciones o CC, corregir en Fase 3 |
| Coverage < umbral | Identificar líneas no cubiertas con `--cov-report=term-missing`, agregar tests en Fase 4, regresar a Fase 7 |

### Dependencias

| Dirección | Fase | Qué provee |
|---|---|---|
| ← anterior | Fases 4-5-6 | Tests pasando (precondición ejecutable) |
| → siguiente | Fase 8 | `quality.json` para documentar en plan |
| → siguiente | Fase 9 | `quality.json` para métricas del reporte final |

### Checklist de salida

- [ ] `quality/reports/{US_ID}-quality.json` existe con estado `APROBADO`
- [ ] Pylint ≥ umbral del perfil activo
- [ ] CC máx/función ≤ umbral del perfil activo
- [ ] MI promedio > umbral del perfil activo
- [ ] Coverage ≥ umbral del perfil activo
- [ ] Tracking de Fase 7 cerrado

### Estado en v1.3

| ID | Descripción | Resolución |
|---|---|---|
| D7-1 | El cuerpo de las secciones de métricas hardcodeaba targets (8.0, 95%, etc.) en lugar de leer del perfil | Se reemplazaron todos los valores hardcodeados por referencias a claves del config: `quality_gates.pylint.min_score`, `quality_gates.coverage.min_percent`, etc. |
| D7-2 | El script Python `generar_reporte_quality` hardcodeaba los umbrales (8.0, 10.0, 20.0, 95.0) | Se corrigió el script para leer umbrales con `leer_umbrales_perfil()` desde `config.json` |
| D7-3 | El template de `quality.json` tenía el campo `umbrales` con valores fijos | Se instruyó leer los umbrales del perfil activo con `jq '.quality_gates'` antes de generar el archivo |

---

**Fase anterior:** [Fase 6: Validación BDD](phase-6.md)
**Siguiente fase:** [Fase 8: Documentación](phase-8.md)
