# Análisis de Integración: CodeGuard ↔ Claude Dev Kit

**Fecha:** 2026-02-18
**Estado:** Propuesta — pendiente de decisión de implementación
**Autor:** Elaborado con Claude Code

---

## 1. Contexto

### Claude Dev Kit

Framework de desarrollo agnóstico de dominio que guía la implementación de historias de usuario con Claude Code. El flujo de trabajo principal es el skill `implement-us`, organizado en 10 fases:

| Fase | Nombre |
|------|--------|
| 0 | Validación de Contexto |
| 1 | Generación de Escenarios BDD |
| 2 | Plan de Implementación |
| 3 | Implementación |
| 4 | Tests Unitarios |
| 5 | Tests de Integración |
| 6 | Validación BDD |
| **7** | **Quality Gates** ← punto de integración principal |
| 8 | Documentación |
| 9 | Reporte Final |

Soporta 5 perfiles de stack: `pyqt-mvc`, `fastapi-rest`, `flask-rest`, `flask-webapp`, `generic-python`.

### CodeGuard (software_limpio v0.1.0)

Agente de calidad de código del proyecto `software_limpio`. Ejecuta análisis estático modular en tres modos:

| Modo | Tiempo | Uso previsto |
|------|--------|--------------|
| `pre-commit` | < 5 s | Análisis rápido durante desarrollo |
| `pr-review` | 2–5 min | Revisión antes de pull request |
| `full` | 10–30 min | Análisis exhaustivo fin de sprint |

Checks disponibles:
- **PEP8Check** — Estilo de código (flake8)
- **PylintCheck** — Score de calidad estática
- **SecurityCheck** — Vulnerabilidades (bandit)
- **ComplexityCheck** — Complejidad ciclomática (radon)
- **TypeCheck** — Anotaciones de tipos (mypy)
- **ImportCheck** — Imports sin usar

Instalable como paquete Python: `pip install quality-agents`
Comando: `codeguard [--analysis-type TYPE] [--format FORMAT] <path>`

---

## 2. Diagnóstico: Estado Actual de la Fase 7

La Fase 7 (Quality Gates) del kit ejecuta actualmente herramientas por separado, definidas en `skills/implement-us/phases/phase-7-quality-gates.md`:

```bash
# Comandos actuales en Phase 7
pylint src/                        # Score mínimo 8.0/10
radon cc src/ -n C                 # Complejidad máxima 10
radon mi src/                      # Índice de mantenibilidad mínimo 20
pytest --cov=src --cov-report=term # Cobertura mínima 95%
```

**Gaps identificados respecto a CodeGuard:**
- No hay análisis de seguridad (bandit)
- No hay verificación de tipos (mypy)
- No hay análisis de imports sin usar
- El output es dispar: cada herramienta con su propio formato
- No hay umbral unificado por perfil de stack

---

## 3. Por Qué la Integración Tiene Sentido

### Complementariedad directa

CodeGuard no es una herramienta más: es un **orquestador de las mismas herramientas** que ya usa el kit (pylint, radon) más otras que le faltan (bandit, mypy). El fit es natural.

### Coherencia de filosofía

Ambos proyectos comparten el mismo principio: **calidad medible con métricas objetivas**. CodeGuard materializa en código lo que el kit prescribe como proceso.

### Mejora de la experiencia del usuario del kit

En lugar de leer output de 4-5 herramientas distintas, el usuario ve un único reporte profesional (Rich) con severidades, colores y sugerencias. Reduce fricción cognitiva.

### Extensión natural de checks

La integración agrega sin costo adicional:
- Análisis de seguridad (crítico para proyectos FastAPI/Flask con APIs públicas)
- Verificación de tipos (relevante para proyectos con type hints como fastapi-rest)
- Detección de imports sin usar (calidad general)

---

## 4. Niveles de Integración Posibles

### Nivel 1 — Sustitución en Phase 7 (mínimo viable)

**Qué cambia:** Solo `phase-7-quality-gates.md`.

En lugar de ejecutar las herramientas por separado:

```bash
# Antes (Phase 7 actual)
pylint src/ && radon cc src/ -n C && pytest --cov=src

# Después (con CodeGuard)
codeguard --analysis-type full --format rich .
pytest --cov=src --cov-report=term   # Coverage sigue separado (no está en CodeGuard)
```

**Ventajas:** Cambio mínimo, bajo riesgo, mejora inmediata del output.
**Desventajas:** No aprovecha configuración por perfil, no hay fallback si CodeGuard no está instalado.

---

### Nivel 2 — Integración por fases del workflow (recomendado)

**Qué cambia:** `phase-7-quality-gates.md` + `phase-3-implementation.md` (opcional).

Mapeo natural entre las fases del kit y los modos de análisis de CodeGuard:

| Fase del kit | Momento | Modo CodeGuard | Tiempo |
|---|---|---|---|
| Fase 3 — Implementación | Durante el desarrollo | `pre-commit` | < 5 s |
| Fase 7 — Quality Gates | Al finalizar implementación | `full` | completo |

**Fase 3 (análisis rápido):**
```bash
# Verificación rápida mientras implementás
codeguard --analysis-type pre-commit .
```

**Fase 7 (quality gates completo):**
```bash
# Análisis exhaustivo antes de cerrar la US
codeguard --analysis-type full --format rich .
pytest --cov=src --cov-report=term
```

**Ventajas:** Respeta el diseño original de CodeGuard, agrega valor en dos puntos del flujo.
**Desventajas:** Requiere modificar dos archivos de phases.

---

### Nivel 3 — Integración profunda con perfiles (futuro)

**Qué cambia:** `phase-7-quality-gates.md` + todos los archivos `customizations/*.json` + `install/installer.py` + `install/config.yaml`.

Cada perfil define sus umbrales de calidad propios en CodeGuard:

```json
// customizations/fastapi-rest.json (fragmento)
"codeguard": {
  "min_pylint_score": 9.0,
  "max_cyclomatic_complexity": 8,
  "check_security": true,
  "check_types": true,
  "check_pep8": true
}

// customizations/generic-python.json (fragmento)
"codeguard": {
  "min_pylint_score": 8.0,
  "max_cyclomatic_complexity": 10,
  "check_security": false,
  "check_types": false,
  "check_pep8": true
}
```

El instalador genera automáticamente la sección `[tool.codeguard]` en el `pyproject.toml` del proyecto del usuario al momento de instalar el kit.

**Ventajas:** Experiencia completamente unificada, umbrales coherentes con el stack.
**Desventajas:** Mayor acoplamiento entre proyectos, requiere coordinación en los cambios de CodeGuard.

---

## 5. Decisión Clave: ¿Requerido u Opcional?

### Opción A — CodeGuard como dependencia requerida

El instalador siempre instala `quality-agents` en el proyecto del usuario:

```yaml
# install/config.yaml
dependencies:
  required:
    - quality-agents>=0.1.0
```

**Pro:** Experiencia unificada, Phase 7 es determinista, no hay variación entre instalaciones.
**Con:** El usuario queda acoplado a un paquete externo; si CodeGuard tiene un bug, bloquea el kit.

### Opción B — CodeGuard como integración opcional (recomendada)

Phase 7 detecta si CodeGuard está disponible y adapta su comportamiento:

```bash
# Lógica de Phase 7
if command -v codeguard &> /dev/null; then
    codeguard --analysis-type full .
else
    # Fallback a herramientas individuales
    pylint src/
    radon cc src/ -n C
    radon mi src/
fi
pytest --cov=src --cov-report=term
```

**Pro:** Sin acoplamiento forzado, el kit funciona con o sin CodeGuard, adopción gradual.
**Con:** Dos caminos de ejecución distintos en Phase 7, mayor complejidad de documentación.

**Recomendación:** Opción B. CodeGuard se instala por defecto pero puede omitirse. El kit funciona en ambos casos.

---

## 6. Impacto en Cada Proyecto

### Cambios en claude-dev-kit

| Archivo | Cambio | Nivel |
|---|---|---|
| `skills/implement-us/phases/phase-7-quality-gates.md` | Agregar comandos CodeGuard con fallback | 1, 2, 3 |
| `skills/implement-us/phases/phase-3-implementation.md` | Agregar análisis rápido opcional | 2, 3 |
| `install/config.yaml` | CodeGuard como dependencia opcional | 2, 3 |
| `install/installer.py` | Ofrecer instalación de `quality-agents` | 2, 3 |
| `skills/implement-us/customizations/*.json` (5 archivos) | Agregar sección `codeguard` con umbrales por perfil | 3 |
| `docs/user/getting-started.md` | Mencionar CodeGuard como herramienta recomendada | 2, 3 |

### Cambios en software_limpio

No se requieren cambios en el código de CodeGuard. El output JSON (`--format json`) ya es suficiente para automatización.

Opcionalmente:
- Agregar documentación de integración con claude-dev-kit en `docs/agentes/`
- Documentar el modo de uso en pipelines de CI/CD similares al kit

---

## 7. Umbrales Propuestos por Perfil (Nivel 3)

| Perfil | Pylint mín. | Complejidad máx. | Seguridad | Types | Cobertura mín. |
|---|---|---|---|---|---|
| `pyqt-mvc` | 8.0 | 10 | No | No | 80% |
| `fastapi-rest` | 9.0 | 8 | **Sí** | **Sí** | 95% |
| `flask-rest` | 9.0 | 8 | **Sí** | No | 94% |
| `flask-webapp` | 8.5 | 10 | **Sí** | No | 90% |
| `generic-python` | 8.0 | 10 | No | No | 95% |

**Criterios usados:**
- Seguridad activada en perfiles con APIs expuestas (fastapi, flask)
- Type checking activado en FastAPI (donde mypy es parte del ecosistema estándar)
- Pylint más exigente en APIs (código más crítico en producción)

---

## 8. Roadmap de Implementación Sugerido

### Paso 1 — Proof of concept (Nivel 1)
Actualizar `phase-7-quality-gates.md` con soporte básico de CodeGuard y fallback.
Validar en un ejemplo real del kit.

### Paso 2 — Integración por fases (Nivel 2)
Agregar análisis `pre-commit` opcional en Phase 3.
Actualizar instalador para ofrecer CodeGuard como dependencia opcional.

### Paso 3 — Perfiles y configuración (Nivel 3)
Definir umbrales por perfil en los `customizations/*.json`.
Actualizar el instalador para generar `[tool.codeguard]` en el `pyproject.toml` del usuario.

---

## 9. Riesgos y Mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| CodeGuard cambia su API de CLI | Media | Alto | Versión fijada en config (`>=0.1.0,<1.0`) |
| Tiempo de análisis `full` es largo en proyectos grandes | Media | Medio | Usar `--analysis-type pr-review` en Phase 7 por defecto |
| Usuario no tiene Python 3.11 requerido por CodeGuard | Baja | Alto | Verificar en paso de validación del instalador |
| Conflicto de versiones de dependencias (pylint, flake8) | Baja | Medio | CodeGuard usa dependencias opcionales aisladas |

---

## 10. Conclusión

La integración de CodeGuard en el kit es **natural, valiosa y de bajo riesgo** si se aborda como Nivel 2 con el enfoque opcional. Los beneficios principales:

1. **Menos fricción**: Un comando unifica lo que hoy son 4-5 herramientas separadas en Phase 7
2. **Más checks**: Seguridad y tipos se agregan sin trabajo adicional del usuario
3. **Output profesional**: Rich con colores, tablas y severidades
4. **Coherencia filosófica**: CodeGuard materializa en código los mismos principios de calidad que el kit promueve como proceso

El punto de partida recomendado es el **Nivel 1** (solo Phase 7) para validar la integración con bajo esfuerzo, y evolucionar al Nivel 2 en base a feedback real de uso.
