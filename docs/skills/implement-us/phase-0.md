# Fase 0: Validación de Contexto

Fase de entrada del skill. Verifica que el entorno del proyecto está listo para ejecutar la implementación, establece las fuentes de información que guiarán todas las fases siguientes, y genera el archivo `context.md` que actúa como fuente de verdad compartida entre fases.

**Aprobación requerida:** No (el skill avanza automáticamente al completarse)

---

## Para el usuario

### Qué hace esta fase

1. Verifica que las herramientas requeridas están instaladas (pylint, radon, pytest, pytest-bdd)
2. Pregunta dónde está la historia de usuario y la documentación de arquitectura
3. Lee y extrae la información de la HU (título, criterios de aceptación, estimación)
4. Lee el perfil de customización activo y sus umbrales de calidad
5. Clasifica el tipo de HU y propone si aplica BDD — espera confirmación del usuario
6. Si faltan `.pylintrc` o `pytest.ini`, los crea automáticamente con los valores del perfil activo
7. Genera `docs/plans/{US_ID}-context.md` con todo el contexto del run

### Qué esperar

El skill te hará dos preguntas antes de avanzar:
- ¿Dónde está la HU? (archivo local, GitHub Issue, Jira ticket, etc.)
- ¿Dónde está la documentación de arquitectura? (o si no existe)

Luego te presentará la clasificación de la HU y la decisión de BDD para que confirmes o ajustes. Respondé:
- `[sí]` para confirmar
- `[no-bdd]` para forzar sin BDD
- `[otro]` para reclasificar

### Artefacto que produce

`docs/plans/{US_ID}-context.md` — contiene: fuentes de HU y arquitectura, datos de la HU, decisión BDD, perfil activo, umbrales de calidad, rutas de todos los artefactos del run.

Este archivo es la única manera confiable de que las fases 1–9 compartan información sin depender de la memoria de la conversación.

---

## Referencia técnica

### Entradas

| Entrada | Tipo | Requerida | Fuente |
|---|---|---|---|
| `{US_ID}` | Parámetro CLI | ✅ Sí | Usuario |
| `--producto {PRODUCT}` | Parámetro CLI | ❌ No | Usuario (default en `config.json`) |
| `--skip-bdd` | Parámetro CLI o `config.json` | ❌ No | Usuario |
| Perfil activo | `config.json` + `customizations/*.json` | ✅ Sí | Instalación del framework |
| Ubicación de la HU | Respuesta del usuario (Paso 3) | ✅ Sí | Usuario en runtime |
| Ubicación de arquitectura | Respuesta del usuario (Paso 3) | ❌ Opcional | Usuario en runtime |

### Salidas

| Salida | Tipo | Descripción |
|---|---|---|
| `docs/plans/{US_ID}-context.md` | Artefacto físico | Fuentes, perfil, umbrales, decisión BDD, rutas de artefactos |
| Confirmación de herramientas | En conversación | Lista de herramientas verificadas |
| Clasificación de HU + decisión BDD | En conversación | Confirmada por el usuario antes de avanzar |

### Templates

Ninguno externo. El template de `context.md` está embebido directamente en el archivo de fase (Paso 8).

### Artefactos

| Artefacto | Operación | Ruta |
|---|---|---|
| `{US_ID}-context.md` | **Genera** | `docs/plans/{US_ID}-context.md` |
| `config.json` | **Lee** | `.claude/skills/implement-us/config.json` |
| `customizations/{perfil}.json` | **Lee** | `.claude/skills/implement-us/customizations/` |
| `.pylintrc` | **Crea si no existe** | raíz del proyecto (con `quality_gates.pylint.min_score` del perfil) |
| `pytest.ini` | **Crea si no existe** | raíz del proyecto (con `test_framework_config.*_path` del perfil) |

### Estructura de `context.md`

```markdown
# Contexto de Ejecución — {US_ID}

## Fuentes
- Fuente HU: {fuente_hu}
- Fuente Arquitectura: {fuente_arquitectura}

## Historia de Usuario
- ID: {US_ID}
- Título: {US_TITLE}
- Tipo: {HU_TYPE}
- Puntos: {US_POINTS}
- Prioridad: {US_PRIORITY}

## Decisiones de Ejecución
- BDD: {Sí / No — justificación}
- skip_bdd: {true / false}
- Fases a ejecutar: 0, [1 si BDD], 2, 3, 4, 5, [6 si BDD], 7, 8, 9

## Perfil Activo
- Perfil: {PROFILE}
- Patrón arquitectónico: {architecture_pattern}
- Umbrales de calidad:
  - pylint ≥ {pylint_min}
  - CC ≤ {cc_max}
  - MI ≥ {mi_min}
  - cobertura ≥ {coverage_min}%

## Rutas de Artefactos
- Contexto: docs/plans/{US_ID}-context.md
- BDD feature: tests/features/{US_ID}-{nombre}.feature
- Plan: docs/plans/{US_ID}-plan.md
- Reporte: docs/reports/{US_ID}-report.md
- Quality report: quality/reports/{US_ID}-quality.json
```

### Convenciones

- El **Paso 1** es imperativo (`🔴`): iniciar tracking antes que cualquier otra acción.
- El orden de los pasos es estricto (de arriba a abajo, sin saltear).
- Si alguna herramienta falta, el skill **detiene** la ejecución con un mensaje claro (fail-fast).
- El archivo `context.md` debe verificarse en disco con `ls` antes de cerrar la fase.
- Los umbrales de calidad provienen siempre del perfil activo — nunca se hardcodean.

### Dependencias

| Dirección | Fase | Qué provee |
|---|---|---|
| → todas (1–9) | Fases siguientes | `context.md` como fuente de verdad compartida |

### Checklist de salida

- [ ] Todas las herramientas requeridas disponibles
- [ ] Fuentes de HU y arquitectura consultadas al usuario
- [ ] HU encontrada y datos extraídos
- [ ] Patrón arquitectónico leído del config y registrado en `context.md`
- [ ] Tipo de HU clasificado y confirmado por el usuario
- [ ] Decisión BDD comunicada y confirmada
- [ ] `docs/plans/{US_ID}-context.md` existe en disco
- [ ] Umbrales de calidad provienen del perfil activo (no hardcodeados)

### Estado en v1.3

Las siguientes discrepancias detectadas en el análisis post v1.2 fueron resueltas en v1.3.0:

| ID | Descripción | Resolución |
|---|---|---|
| D0-2 | Fase 0, Paso 6 no especificaba qué valores escribir en `.pylintrc` y `pytest.ini` | Se explicitó que los valores se leen de `quality_gates.pylint.min_score` y `test_framework_config.*_path` del perfil activo |
| D0-3 | `context.md` no incluía campo `skip_bdd` | Se agregó campo `skip_bdd: {true/false}` en la sección "Decisiones de Ejecución" del template |
| D0-1 | `config.json` incluye clave `"django"` en ejemplos de variables (perfil no soportado) | Baja prioridad — pendiente de limpieza en config.json |

---

**Fase anterior:** —
**Siguiente fase:** [Fase 1: Generación de Escenarios BDD](phase-1.md) (si BDD aplica) / [Fase 2: Plan de Implementación](phase-2.md) (si BDD no aplica)
