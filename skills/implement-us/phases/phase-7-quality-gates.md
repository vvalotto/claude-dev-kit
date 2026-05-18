# Fase 7: Quality Gates

**Objetivo:** Validar que el código implementado cumple con los estándares de calidad definidos mediante métricas objetivas.


---

## 🔴 Acción Requerida — Iniciar tracking de fase

Ejecutá como primera acción, antes de cualquier otra:

```bash
python .claude/tracking/tracker_cli.py start-phase 7 "Quality Gates"
```

---

## 🔴 Acción Requerida — Verificar precondiciones

Confirmá que las tres suites de tests de fases anteriores pasan:

```bash
pytest tests/unit/ tests/integration/ tests/step_defs/ -v --tb=short
```

Si algún test falla, **no avances** — resolvé los fallos en la fase correspondiente primero.

---

## Acción

Ejecutar herramientas de análisis estático y validar que todas las métricas de calidad superan los umbrales mínimos establecidos.

---

## Métricas de Calidad

> **Si el perfil activo es `hexagonal-ddd-bc`:** No usar `radon` directamente.
> Usar `codeguard` que orquesta pylint + radon + designreviewer en una sola pasada.
>
> ```bash
> codeguard src/{bc}/ --format json > quality/reports/codeguard/{US_ID}-codeguard.json
> ```
>
> `designreviewer` se ejecuta **al cierre del Incremento** (no por US), vía pre-push hook
> o manualmente. Si reporta CRITICAL, bloquea el merge.

### 1. Pylint (Análisis Estático)

**Objetivo:** Validar estilo, convenciones y errores potenciales.

**Comando:**
```bash
pylint {COMPONENT_PATH}/ --output-format=json
```

**Target:** ≥ valor de `quality_gates.pylint.min_score` del perfil activo

**Qué valida:**
- Convenciones de naming (PEP 8)
- Imports no utilizados
- Variables no usadas
- Código inalcanzable
- Errores de lógica potenciales
- Documentación faltante

**Ejemplo de output:**
```
************* Module user_profile.modelo
user_profile/modelo.py:1:0: C0114: Missing module docstring (missing-module-docstring)

-----------------------------------
Your code has been rated at 9.2/10
```

**Si no pasa (no alcanza el umbral del perfil activo):**
- Revisar warnings/errors reportados
- Corregir issues identificados
- Re-ejecutar hasta superar umbral

---

### 2. Complejidad Ciclomática (CC)

**Objetivo:** Medir complejidad del código (cantidad de caminos de ejecución).

**Herramientas:**
- `radon` (Python general)
- `mccabe` (incluido con flake8)
- `lizard` (multi-lenguaje)

**Comando con radon:**
```bash
# Ver CC por función individual (criterio de aprobación)
radon cc {COMPONENT_PATH}/ -s

# Ver promedio general (orientativo)
radon cc {COMPONENT_PATH}/ -a -s
```

**Target:** CC de cada función ≤ `max_per_function` del perfil activo

> El criterio de aprobación es el **máximo por función** (`max_per_function` en config.json), no el promedio. El promedio es orientativo. Si alguna función supera el umbral, debe refactorizarse aunque el promedio general sea bajo.

**Interpretación por función:**
- **1-5:** Código simple, fácil de testear
- **6-10:** Moderadamente complejo, aceptable
- **11-20:** Complejo, considerar refactorizar
- **21+:** Muy complejo, refactorizar urgente

**Ejemplo de output:**
```
user_profile/modelo.py
    M 12:0 UserProfileModelo.__post_init__ - A (2)
    M 25:0 UserProfileModelo.validate - A (3)

Average complexity: A (2.5)
```

**Si no pasa (supera el umbral `max_per_function` del perfil activo):**
- Identificar funciones/métodos con CC alta
- Extraer lógica a funciones auxiliares
- Simplificar condicionales anidados
- Aplicar patrones de diseño (Strategy, Command)

---

### 3. Índice de Mantenibilidad (MI)

**Objetivo:** Medir facilidad de mantenimiento del código (0-100).

**Herramienta:** `radon`

**Comando:**
```bash
radon mi {COMPONENT_PATH}/ -s
```

**Target:** MI promedio > valor de `quality_gates.maintainability_index.min_score` del perfil activo

**Interpretación:**
- **0-10:** Muy difícil de mantener
- **10-20:** Difícil de mantener
- **20-50:** Moderadamente mantenible ✅
- **50+:** Altamente mantenible ✅

**Factores que afectan MI:**
- Líneas de código por función
- Complejidad ciclomática
- Volumen de Halstead (operadores/operandos)

**Ejemplo de output:**
```
user_profile/modelo.py - A (78.5)
user_profile/vista.py - B (65.2)

Average MI: A (71.85)
```

**Si no pasa (no alcanza el umbral del perfil activo):**
- Reducir tamaño de funciones (max 20-30 líneas)
- Reducir complejidad ciclomática
- Mejorar documentación

---

### 4. Cobertura de Tests (Coverage)

**Objetivo:** Medir porcentaje de código cubierto por tests.

**Herramienta:** `pytest-cov`

**Comando:**
```bash
pytest tests/ --cov={COMPONENT_PATH} --cov-report=term --cov-report=json
```

**Target:** ≥ valor de `quality_gates.coverage.min_percent` del perfil activo

**Ejemplo de output:**
```
---------- coverage: platform darwin, python 3.11.7 -----------
Name                           Stmts   Miss  Cover
--------------------------------------------------
user_profile/modelo.py            25      1    96%
user_profile/vista.py             42      3    93%
user_profile/controlador.py       18      0   100%
--------------------------------------------------
TOTAL                             85      4    95%
```

**Qué cubrir:**
- ✅ Todos los métodos públicos
- ✅ Lógica condicional (branches)
- ✅ Casos de error/excepciones
- ❌ Código boilerplate (imports, constantes)
- ❌ Métodos abstractos no implementados

**Si no pasa (no alcanza el umbral del perfil activo):**
- Revisar líneas no cubiertas en reporte
- Agregar tests para casos faltantes
- Priorizar código crítico de negocio

---

## Pasos de Ejecución

### 1. Ejecutar Pylint

```bash
cd {PROJECT_PATH}
pylint {COMPONENT_PATH}/ --output-format=json > quality/reports/{US_ID}-pylint.json
pylint {COMPONENT_PATH}/ --output-format=text
```

**Validar:** Score ≥ umbral `pylint.min_score` del perfil activo

---

### 2. Calcular Métricas de Complejidad

**Opción A: Usar radon (recomendado para Python)**

```bash
# Complejidad Ciclomática
radon cc {COMPONENT_PATH}/ -a -s -j > quality/reports/{US_ID}-cc.json

# Índice de Mantenibilidad
radon mi {COMPONENT_PATH}/ -s -j > quality/reports/{US_ID}-mi.json
```

**Opción B: Script personalizado**

Si el proyecto tiene un script de métricas:
```bash
python quality/scripts/calculate_metrics.py {COMPONENT_PATH}
```

**Validar:**
- CC máx por función ≤ `max_per_function` del perfil activo
- MI promedio > `min_score` del perfil activo

---

### 3. Validar Coverage

```bash
pytest tests/ \
  --cov={COMPONENT_PATH} \
  --cov-report=term \
  --cov-report=json:quality/reports/{US_ID}-coverage.json \
  --cov-report=html:quality/reports/{US_ID}-coverage-html
```

**Validar:** Coverage ≥ umbral del perfil activo (`quality_gates.coverage.min_percent` en config.json)

**Ver reporte detallado:**
```bash
# Terminal
pytest --cov={COMPONENT_PATH} --cov-report=term-missing

# HTML (navegador)
open quality/reports/{US_ID}-coverage-html/index.html
```

---

### 4. Generar Reporte Consolidado

Crear archivo JSON con todas las métricas:

**Ubicación:** `{PROJECT_PATH}/quality/reports/{US_ID}-quality.json`

**Formato:**

> Antes de generar el archivo, leé los umbrales del perfil activo:
> `cat .claude/skills/implement-us/config.json | jq '.quality_gates'`
> Reemplazá `{PYLINT_MIN}`, `{CC_MAX}`, `{MI_MIN}`, `{COVERAGE_MIN}` con los valores obtenidos.

```json
{
  "us_id": "{US_ID}",
  "fecha": "{FECHA_ISO}",
  "componente": "{COMPONENT_PATH}",
  "metricas": {
    "pylint": 0.0,
    "cc_promedio": 0.0,
    "mi_promedio": 0.0,
    "coverage": 0.0
  },
  "umbrales": {
    "pylint_min": "{PYLINT_MIN}",
    "cc_max": "{CC_MAX}",
    "mi_min": "{MI_MIN}",
    "coverage_min": "{COVERAGE_MIN}"
  },
  "estado": "APROBADO",
  "observaciones": []
}
```

**Script de generación (opcional):**

> Los umbrales se leen desde el config del perfil activo — no están hardcodeados.

```python
import json
from datetime import datetime
from pathlib import Path

def leer_umbrales_perfil(config_path=".claude/skills/implement-us/config.json"):
    """Leer umbrales de quality gates desde el perfil activo."""
    with open(config_path) as f:
        config = json.load(f)
    qg = config["quality_gates"]
    return {
        "pylint_min": qg["pylint"]["min_score"],
        "cc_max": qg["cyclomatic_complexity"]["max_per_function"],
        "mi_min": qg["maintainability_index"]["min_score"],
        "coverage_min": qg["coverage"]["min_percent"]
    }

def todas_metricas_pasan(metricas, umbrales):
    """Validar que todas las métricas superan los umbrales del perfil activo."""
    return (
        metricas['pylint'] >= umbrales['pylint_min'] and
        metricas['cc_promedio'] <= umbrales['cc_max'] and
        metricas['mi_promedio'] > umbrales['mi_min'] and
        metricas['coverage'] >= umbrales['coverage_min']
    )

def generar_reporte_quality(us_id, component_path, metricas):
    """Generar reporte JSON de quality gates con umbrales del perfil activo."""
    umbrales = leer_umbrales_perfil()
    estado = "APROBADO" if todas_metricas_pasan(metricas, umbrales) else "RECHAZADO"

    reporte = {
        "us_id": us_id,
        "fecha": datetime.now().isoformat(),
        "componente": component_path,
        "metricas": metricas,
        "umbrales": umbrales,
        "estado": estado,
        "observaciones": calcular_observaciones(metricas, umbrales)
    }

    output_path = f"quality/reports/{us_id}-quality.json"
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(reporte, f, indent=2)

    return reporte
```

---

## Criterio de Éxito

**Todas las métricas deben superar los umbrales:**

| Métrica | Umbral | Descripción |
|---------|--------|-------------|
| Pylint | ≥ `pylint.min_score` del perfil activo | Calidad de código y estilo |
| CC máx/función | ≤ `cyclomatic_complexity.max_per_function` del perfil activo | Complejidad por función |
| MI promedio | > `maintainability_index.min_score` del perfil activo | Mantenibilidad |
| Coverage | ≥ `coverage.min_percent` del perfil activo | Cobertura de tests |

**Estado:** `APROBADO` si todas pasan, `RECHAZADO` si alguna falla

---

## Manejo de Métricas que No Pasan

### Si Pylint no alcanza el umbral del perfil activo

1. **Revisar output detallado:**
   ```bash
   pylint {COMPONENT_PATH}/ --reports=y
   ```

2. **Priorizar errores (E) y warnings (W)**
3. **Ignorar convenciones (C) menos críticas si es necesario**
4. **Configurar .pylintrc si hay false positives**

---

### Si CC > 10

1. **Identificar funciones complejas:**
   ```bash
   radon cc {COMPONENT_PATH}/ -s --min C
   ```

2. **Refactorizar:**
   - Extraer métodos auxiliares
   - Simplificar condicionales
   - Usar diccionarios para dispatch (evitar if/elif largo)
   - Aplicar patrones de diseño

---

### Si MI < 20

1. **Reducir tamaño de funciones** (max 20-30 líneas)
2. **Reducir CC** (ver arriba)
3. **Mejorar documentación** (docstrings claros)
4. **Eliminar código duplicado**

---

### Si Coverage < 95%

1. **Identificar líneas no cubiertas:**
   ```bash
   pytest --cov={COMPONENT_PATH} --cov-report=term-missing
   ```

2. **Agregar tests para:**
   - Branches no cubiertos (if/else)
   - Casos de error/excepciones
   - Edge cases

3. **Re-ejecutar hasta alcanzar target**

---

## Herramientas Python

- **Linting:** pylint, flake8, ruff
- **Métricas de complejidad:** radon, mccabe
- **Coverage:** pytest-cov, coverage.py

---

## Integración con CI/CD

Automatizar quality gates en pipeline:

```yaml
# .github/workflows/quality-gates.yml
name: Quality Gates

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Run Pylint
        run: |
          pylint {COMPONENT_PATH}/ --fail-under=8.0

      - name: Check Coverage
        run: |
          pytest --cov={COMPONENT_PATH} --cov-fail-under=95

      - name: Calculate Complexity
        run: |
          radon cc {COMPONENT_PATH}/ -a --total-average
```

**Beneficio:** Bloquear merge si quality gates no pasan

---

## Excepciones y Flexibilidad

**Cuándo relajar umbrales:**

- ✅ Código legacy en refactorización gradual
- ✅ Scripts one-off o herramientas internas
- ✅ Prototipos o PoCs

**Cómo documentar excepciones:**

Agregar a observaciones del reporte:
```json
{
  "observaciones": [
    "Coverage 92%: Código legacy de migración, refactorizar en próximo sprint",
    "Pylint 7.8: False positives en métodos generados automáticamente"
  ]
}
```

**Importante:** Excepciones deben ser temporales y justificadas

---


---

## 🔴 Acción Requerida — Generar reporte de quality gates

Antes de cerrar el tracking, generá el reporte JSON con los resultados de todas las métricas:

**Ubicación:** `quality/reports/{US_ID}-quality.json`

Creá el archivo con los valores reales obtenidos en los pasos anteriores:

```json
{
  "us_id": "{US_ID}",
  "fecha": "{FECHA_ISO}",
  "componente": "{COMPONENT_PATH}",
  "metricas": {
    "pylint": 0.0,
    "cc_promedio": 0.0,
    "mi_promedio": 0.0,
    "coverage": 0.0
  },
  "umbrales": {
    "pylint_min": 8.0,
    "cc_max": 10,
    "mi_min": 20,
    "coverage_min": 95.0
  },
  "estado": "APROBADO",
  "observaciones": []
}
```

> Reemplazá los valores `0.0` con los resultados reales de pylint, radon y pytest-cov.
> Leé los umbrales correctos del perfil activo con:
> ```bash
> cat .claude/skills/implement-us/config.json | jq '.quality_gates'
> ```
> Cambiá `"estado"` a `"RECHAZADO"` si alguna métrica no alcanza el umbral. Documentá la causa en `"observaciones"`.

Si el directorio no existe, crealo:

```bash
mkdir -p quality/reports
```

---

## ✅ Checklist de Salida

Antes de avanzar a Fase 8, confirmá que:
- [ ] `quality/reports/{US_ID}-quality.json` existe con estado `APROBADO`
- [ ] Pylint ≥ umbral del perfil activo
- [ ] CC ≤ umbral del perfil activo
- [ ] Coverage ≥ umbral del perfil activo
- [ ] Tracking de Fase 7 cerrado

## 🔴 Acción Requerida — Verificar reporte antes de cerrar

Confirmá que el reporte de quality gates existe en disco antes de avanzar a Fase 8:

```bash
ls quality/reports/{US_ID}-quality.json
```

Si no existe, generalo con los valores reales obtenidos en los pasos anteriores (ver sección "Generar Reporte Consolidado").

---

## 🔴 Acción Requerida — Cerrar tracking

```bash
python .claude/tracking/tracker_cli.py end-phase 7
```

---

## Umbrales Ajustados por Perfil

Los umbrales de quality gates pueden ajustarse según el perfil del proyecto, basándose en la naturaleza del código y proyectos reales de referencia.

### Tabla Comparativa de Umbrales

| Métrica | PyQt MVC | FastAPI REST | Flask REST | Flask Webapp | Generic Python |
|---------|----------|--------------|------------|--------------|----------------|
| **Pylint mín** | 8.0 | 8.5 | 8.0 | 8.0 | 8.0 |
| **CC máx** | 12 | 10 | 10 | 10 | 10 |
| **MI mín** | 20 | 25 | 25 | 20 | 20 |
| **Coverage mín** | 90% | 95% | 95% | **90%** | 95% |

### Justificación de Ajustes

#### PyQt MVC (Desktop UI)
```json
{
  "pylint": { "min_score": 8.0 },
  "cc": { "max_per_function": 12 },
  "mi": { "min_score": 20 },
  "coverage": { "min_percent": 90.0 }
}
```

**Justificación:**
- **Coverage 90%**: Código UI es más difícil de testear (requiere mocks complejos de Qt)
- **CC 12**: Controladores pueden tener lógica de coordinación más compleja
- **Pylint 8.0**: Estándar general Python
- **MI 20**: Mínimo para código mantenible

**Proyecto de referencia:** `simapp_termostato` (PyQt6 + MVC)

---

#### FastAPI REST (Async APIs)
```json
{
  "pylint": { "min_score": 8.5 },
  "cc": { "max_per_function": 10 },
  "mi": { "min_score": 25 },
  "coverage": { "min_percent": 95.0 }
}
```

**Justificación:**
- **Pylint 8.5**: Código API debe ser muy limpio (interfaz pública)
- **Coverage 95%**: APIs críticas requieren alta cobertura
- **MI 25**: Código backend debe ser altamente mantenible
- **CC 10**: Endpoints deben ser simples (delegar a services)

**Características:**
- Async/await patterns
- Dependency injection
- Type hints estrictos (Pydantic)

---

#### Flask REST (Sync APIs)
```json
{
  "pylint": { "min_score": 8.0 },
  "cc": { "max_per_function": 10 },
  "mi": { "min_score": 25 },
  "coverage": { "min_percent": 95.0 }
}
```

**Justificación:**
- **Pylint 8.0**: Estándar Python (Flask es más flexible que FastAPI)
- **Coverage 95%**: APIs requieren alta cobertura de tests
- **MI 25**: Backend debe ser mantenible a largo plazo
- **CC 10**: Separación en capas mantiene funciones simples

**Proyecto de referencia:** `app_termostato` (Flask 3.1 + Layered)
- **Métricas reales:**
  - Pylint: 8.41/10 ✅
  - CC promedio: 1.75 ✅
  - MI: 92.21/100 ✅
  - Coverage: 100% ✅

**Características:**
- Sync (no async/await)
- Repository pattern con ABC
- Singleton pattern (Configurador)
- Blueprints pattern

---

#### Flask Webapp (Fullstack Webapps)
```json
{
  "pylint": { "min_score": 8.0 },
  "cc": { "max_per_function": 10 },
  "mi": { "min_score": 20 },
  "coverage": { "min_percent": 90.0 }
}
```

**Justificación:**
- **Coverage 90%**: Solo backend Python (routes, api_client, forms). Frontend JavaScript NO incluido en coverage.
- **Pylint 8.0**: Estándar Python para webapps
- **MI 20**: Mínimo para código mantenible
- **CC 10**: Routes pueden renderizar múltiples templates pero ideal mantener simple

**Proyecto de referencia:** `webapp_termostato` (Flask 3.1 + Jinja2 + Vanilla JS)

**Características:**
- BFF (Backend for Frontend) pattern
- Server-Side Rendering con Jinja2
- Vanilla JavaScript (ES6 modules)
- Flask-WTF forms + Flask-Bootstrap
- Coverage solo de Python (templates y JS no testeados con pytest)

**Nota importante sobre coverage:**
- ⚠️ Coverage 90% (no 95%) porque frontend JavaScript no se testea con pytest
- Scope: Solo Python backend (webapp/routes.py, webapp/api_client.py, webapp/forms.py)
- Frontend testing (opcional): Usar Jest/Vitest si hay mucha lógica JS

---

#### Generic Python
```json
{
  "pylint": { "min_score": 8.0 },
  "cc": { "max_per_function": 10 },
  "mi": { "min_score": 20 },
  "coverage": { "min_percent": 95.0 }
}
```

**Justificación:**
- **Defaults estándar Python** para máxima flexibilidad
- Se aplican a librerías, CLI tools, data science, etc.

---

### Cómo Consultar Umbrales del Proyecto

Los umbrales específicos se definen en el archivo de configuración del perfil:

```bash
# Leer umbrales del perfil activo
cat .claude/skills/implement-us/config.json | jq '.quality_gates'
```

**Ejemplo de output (Flask REST):**
```json
{
  "quality_gates": {
    "pylint": {
      "enabled": true,
      "min_score": 8.0
    },
    "cyclomatic_complexity": {
      "enabled": true,
      "max_per_function": 10
    },
    "maintainability_index": {
      "enabled": true,
      "min_score": 25
    },
    "coverage": {
      "enabled": true,
      "min_percent": 95.0
    }
  }
}
```

**Usar estos umbrales en la validación** en lugar de valores hardcodeados.

---

### Comandos de Validación

Leé primero los umbrales y la ruta del componente del perfil activo:

```bash
cat .claude/skills/implement-us/config.json | jq '.quality_gates'
```

Luego ejecutá con los valores obtenidos (reemplazá `{COMPONENT_PATH}`, `{COVERAGE_THRESHOLD}` y `{PYLINT_MIN}` con los valores del perfil):

```bash
# Coverage
pytest --cov={COMPONENT_PATH} --cov-fail-under={COVERAGE_THRESHOLD}

# Pylint
pylint {COMPONENT_PATH}/ --fail-under={PYLINT_MIN}

# CC por función (comparar cada función vs max_per_function del perfil)
radon cc {COMPONENT_PATH}/ -s

# Índice de Mantenibilidad (comparar vs mi_min del perfil)
radon mi {COMPONENT_PATH}/ -s
```

---

## 🚫 Si esta fase falla — Protocolo de recuperación

**Síntoma:** Una o más métricas están por debajo del umbral del perfil activo.

**Protocolo por métrica:**

- **Pylint < umbral** → corregí los issues reportados en el código (Fase 3), re-ejecutá pylint
- **CC > umbral** → identificá las funciones con CC alta, refactorizá en Fase 3, regresá a Fase 7
- **MI < umbral** → reducí tamaño de funciones o CC, corregí en Fase 3
- **Coverage < umbral** → identificá líneas no cubiertas con `pytest --cov-report=term-missing`, agregá tests en Fase 4, regresá a Fase 7

**Si el umbral no se alcanza después de correcciones razonables:**
- No ignorar silenciosamente
- Documentar como excepción justificada en el campo `observaciones` del reporte de calidad
- Informar al usuario antes de continuar

4. Re-ejecutá **todos** los quality gates después de cada corrección
5. No avances a Fase 8 hasta que el reporte tenga estado `APROBADO` o excepción documentada

---

## Resumen de la Fase

Al finalizar esta fase:

✅ Todas las métricas de calidad validadas contra umbrales del perfil activo
✅ Pylint ≥ umbral del perfil (código limpio y bien estructurado)
✅ CC ≤ umbral del perfil (código simple y testeable)
✅ MI > umbral del perfil (código mantenible)
✅ Coverage ≥ umbral del perfil (alta confianza en tests)
✅ Reporte JSON generado con estado APROBADO
✅ Código listo para producción

**Próxima fase:** Fase 8 - Actualización de Documentación
