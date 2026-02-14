# Fase 7: Quality Gates

**Objetivo:** Validar que el código implementado cumple con los estándares de calidad definidos mediante métricas objetivas.

**Duración estimada:** 10-15 minutos

---

## Tracking

**Al inicio de la fase:**
```python
tracker.start_phase(7, "Quality Gates")
```

---

## Acción

Ejecutar herramientas de análisis estático y validar que todas las métricas de calidad superan los umbrales mínimos establecidos.

---

## Métricas de Calidad

### 1. Pylint (Análisis Estático)

**Objetivo:** Validar estilo, convenciones y errores potenciales.

**Comando:**
```bash
pylint {COMPONENT_PATH}/ --output-format=json
```

**Target:** ≥ 8.0/10

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

**Si no pasa (< 8.0):**
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
radon cc {COMPONENT_PATH}/ -a -s
```

**Target:** CC promedio ≤ 10

**Interpretación:**
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

**Si no pasa (> 10):**
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

**Target:** MI promedio > 20

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

**Si no pasa (< 20):**
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

**Target:** ≥ 95%

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

**Si no pasa (< 95%):**
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

**Validar:** Score ≥ 8.0

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
- CC promedio ≤ 10
- MI promedio > 20

---

### 3. Validar Coverage

```bash
pytest tests/ \
  --cov={COMPONENT_PATH} \
  --cov-report=term \
  --cov-report=json:quality/reports/{US_ID}-coverage.json \
  --cov-report=html:quality/reports/{US_ID}-coverage-html
```

**Validar:** Coverage ≥ 95%

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
```json
{
  "us_id": "{US_ID}",
  "fecha": "2026-02-11T15:30:00Z",
  "componente": "{COMPONENT_PATH}",
  "metricas": {
    "pylint": 9.2,
    "cc_promedio": 2.1,
    "mi_promedio": 78.5,
    "coverage": 97.3
  },
  "umbrales": {
    "pylint_min": 8.0,
    "cc_max": 10.0,
    "mi_min": 20.0,
    "coverage_min": 95.0
  },
  "estado": "APROBADO",
  "observaciones": []
}
```

**Script de generación (opcional):**
```python
import json
from datetime import datetime

def generar_reporte_quality(us_id, component_path, metricas):
    """Generar reporte JSON de quality gates."""
    estado = "APROBADO" if todas_metricas_pasan(metricas) else "RECHAZADO"

    reporte = {
        "us_id": us_id,
        "fecha": datetime.now().isoformat(),
        "componente": component_path,
        "metricas": metricas,
        "umbrales": {
            "pylint_min": 8.0,
            "cc_max": 10.0,
            "mi_min": 20.0,
            "coverage_min": 95.0
        },
        "estado": estado,
        "observaciones": calcular_observaciones(metricas)
    }

    output_path = f"quality/reports/{us_id}-quality.json"
    with open(output_path, 'w') as f:
        json.dump(reporte, f, indent=2)

    return reporte

def todas_metricas_pasan(metricas):
    """Validar que todas las métricas superan umbrales."""
    return (
        metricas['pylint'] >= 8.0 and
        metricas['cc_promedio'] <= 10.0 and
        metricas['mi_promedio'] > 20.0 and
        metricas['coverage'] >= 95.0
    )
```

---

## Criterio de Éxito

**Todas las métricas deben superar los umbrales:**

| Métrica | Umbral | Descripción |
|---------|--------|-------------|
| Pylint | ≥ 8.0 | Calidad de código y estilo |
| CC promedio | ≤ 10 | Complejidad por función |
| MI promedio | > 20 | Mantenibilidad |
| Coverage | ≥ 95% | Cobertura de tests |

**Estado:** `APROBADO` si todas pasan, `RECHAZADO` si alguna falla

---

## Manejo de Métricas que No Pasan

### Si Pylint < 8.0

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

## Herramientas Alternativas por Lenguaje

### Python (actual)
- **Linting:** pylint, flake8, ruff
- **Métricas:** radon, mccabe
- **Coverage:** pytest-cov, coverage.py

### TypeScript/JavaScript
- **Linting:** eslint, tslint
- **Métricas:** complexity-report, plato
- **Coverage:** istanbul, nyc, jest --coverage

### Java
- **Linting:** checkstyle, PMD, SpotBugs
- **Métricas:** sonarqube, JaCoCo
- **Coverage:** JaCoCo, Cobertura

### C#/.NET
- **Linting:** StyleCop, FxCop
- **Métricas:** Visual Studio Metrics
- **Coverage:** coverlet, dotnet-coverage

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

## Tracking al Finalizar

```python
tracker.end_phase(7, auto_approved=True)
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

### Comandos de Validación por Perfil

**PyQt MVC:**
```bash
pytest --cov=app/presentacion --cov-fail-under=90
pylint app/presentacion/ --fail-under=8.0
radon cc app/presentacion/ --total-average --min C  # CC ≤ 12
```

**FastAPI REST:**
```bash
pytest --cov=app/api --cov-fail-under=95
pylint app/ --fail-under=8.5
radon cc app/ --total-average  # CC ≤ 10
radon mi app/ --min B  # MI ≥ 25
```

**Flask REST:**
```bash
pytest --cov=app --cov-fail-under=95
pylint app/ --fail-under=8.0
radon cc app/ --total-average  # CC ≤ 10
radon mi app/ --min B  # MI ≥ 25
```

**Generic Python:**
```bash
pytest --cov=src --cov-fail-under=95
pylint src/ --fail-under=8.0
radon cc src/ --total-average  # CC ≤ 10
```

---

## Resumen de la Fase

Al finalizar esta fase:

✅ Todas las métricas de calidad validadas
✅ Pylint ≥ 8.0 (código limpio y bien estructurado)
✅ CC ≤ 10 (código simple y testeable)
✅ MI > 20 (código mantenible)
✅ Coverage ≥ 95% (alta confianza en tests)
✅ Reporte JSON generado con estado APROBADO
✅ Código listo para producción

**Próxima fase:** Fase 8 - Actualización de Documentación
