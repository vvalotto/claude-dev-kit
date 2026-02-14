# Análisis de Impacto: Nuevos Perfiles Flask en el Sistema

**Fecha:** 2026-02-13
**Perfiles Analizados:** flask-rest.json (TICKET-028), flask-webapp.json (TICKET-029)
**Alcance:** Impacto en agentes (phases) del skill implement-us

---

## Resumen Ejecutivo

Los nuevos perfiles Flask **SÍ impactan** en **7 de las 10 phases** del sistema implement-us. Estas phases contienen ejemplos específicos por stack que necesitarán ser actualizados para incluir los casos de uso Flask.

**Impacto:** Media-Alta complejidad
**Estimación de actualización:** 3-4 horas adicionales
**Archivos afectados:** 7 phases + README.md

---

## Arquitectura del Sistema

### Esquema Completo de Agentes (Phases)

```
skill.md (orquestador)
    ├── Phase 0: Validación de Contexto         ✅ USA variables
    ├── Phase 1: Generación BDD                 ⚠️ No usa variables (genérico)
    ├── Phase 2: Plan de Implementación         ✅ USA variables + EJEMPLOS
    ├── Phase 3: Implementación                 ✅ USA variables + EJEMPLOS
    ├── Phase 4: Tests Unitarios                ✅ USA variables + EJEMPLOS
    ├── Phase 5: Tests de Integración           ⚠️ No usa variables (genérico)
    ├── Phase 6: Validación BDD                 ⚠️ No usa variables (genérico)
    ├── Phase 7: Quality Gates                  ✅ USA variables + EJEMPLOS
    ├── Phase 8: Documentación                  ✅ USA variables
    └── Phase 9: Reporte Final                  ✅ USA variables
```

**Leyenda:**
- ✅ **USA variables**: Lee variables del perfil para adaptar comportamiento
- ⚠️ **No usa variables**: Funciona de forma genérica sin depender del stack

---

## Análisis por Phase

### ✅ Phase 0: Validación de Contexto

**Archivo:** `skills/implement-us/phases/phase-0-validation.md`

**Uso de variables:**
- Lee `{ARCHITECTURE_PATTERN}` para validar arquitectura del proyecto
- Lee `{PROJECT_ROOT}` para validar estructura de directorios

**Impacto Flask:**
- ❌ **NO requiere cambios**
- Validación es genérica, funciona con cualquier perfil

**Razón:** La validación solo verifica que exista config.json y que tenga las variables definidas.

---

### ⚠️ Phase 1: Generación BDD

**Archivo:** `skills/implement-us/phases/phase-1-bdd.md`

**Uso de variables:**
- Ninguno (BDD es agnóstico del stack)

**Impacto Flask:**
- ❌ **NO requiere cambios**
- Los escenarios Gherkin son independientes de la arquitectura

**Razón:** BDD describe comportamiento, no implementación.

---

### ✅ Phase 2: Plan de Implementación

**Archivo:** `skills/implement-us/phases/phase-2-planning.md`

**Uso de variables:**
- `{ARCHITECTURE_PATTERN}` para determinar estructura de componentes
- `{COMPONENT_TYPE}` para nombrar tareas
- `{COMPONENT_PATH}` para rutas de archivos

**Ejemplos actuales:**
1. **Ejemplo 1:** PyQt/MVC - Panel UI (líneas 90-134)
2. **Ejemplo 2:** FastAPI - Endpoint REST (líneas 137-176)
3. **Ejemplo 3:** Django - Vista y Modelo (líneas 178-218)
4. **Ejemplo 4:** Generic Python - Módulo (líneas 220-249)

**Impacto Flask:**
- ✅ **REQUIERE CAMBIOS**
- Necesita agregar **Ejemplo 5: Flask REST API** (basado en TICKET-028)
- Necesita agregar **Ejemplo 6: Flask Webapp** (basado en TICKET-029)

**Cambios necesarios:**

```markdown
### Ejemplo 5: Flask REST - API Endpoint

# Plan de Implementación: US-005 - Endpoint de termostatos

**Patrón:** Layered (3 capas)
**Producto:** termostatos_api
**Estimación Total:** 1h 45min

## Componentes a Implementar

### 1. Termostato Endpoint (Layered)
- [ ] app/servicios/termostatos/api.py (15 min)
  - Blueprint con rutas HTTP
  - Métodos GET, POST, PUT, DELETE
- [ ] app/general/termostato.py (20 min)
  - Clase Termostato (business logic)
  - Validaciones de dominio
- [ ] app/datos/termostatos/repositorio.py (10 min)
  - Interface abstracta (ABC)
- [ ] app/datos/termostatos/memoria.py (15 min)
  - Implementación in-memory

### 2. Tests
- [ ] tests/test_termostato_api.py (20 min)
- [ ] tests/test_termostato_modelo.py (15 min)
- [ ] tests/test_repositorio.py (10 min)
```

```markdown
### Ejemplo 6: Flask Webapp - Página Web

# Plan de Implementación: US-006 - Página de monitoreo

**Patrón:** BFF + SSR
**Producto:** monitor_webapp
**Estimación Total:** 2h 00min

## Componentes a Implementar

### 1. Monitor Page (BFF + SSR)
- [ ] webapp/routes.py (20 min)
  - Route /monitor
  - View function render_monitor()
- [ ] webapp/templates/monitor/index.html (25 min)
  - Template Jinja2 con layout
  - Bloques de contenido
- [ ] webapp/static/js/monitor.js (20 min)
  - Módulo JavaScript para interactividad
  - Event handlers
- [ ] webapp/api_client.py (15 min)
  - Cliente HTTP para API backend

### 2. Tests
- [ ] tests/test_monitor_routes.py (20 min)
- [ ] tests/test_monitor_template.py (15 min)
- [ ] tests/test_api_client.py (15 min)
```

**Estimación:** 30 minutos para agregar ejemplos

---

### ✅ Phase 3: Implementación

**Archivo:** `skills/implement-us/phases/phase-3-implementation.md`

**Uso de variables:**
- `{COMPONENT_PATH}` para rutas de archivos
- `{COMPONENT_TYPE}` para tipos de componentes
- `{ARCHITECTURE_PATTERN}` para patrones de código
- `{BASE_CLASS}` para herencia

**Ejemplos actuales:**
1. PyQt/MVC - Modelo (líneas 92-113)
2. FastAPI/Layered - Schema (líneas 115-138)
3. Django/MVT - Model (líneas 140-150+)

**Impacto Flask:**
- ✅ **REQUIERE CAMBIOS**
- Necesita agregar ejemplos de código Flask REST
- Necesita agregar ejemplos de código Flask Webapp

**Cambios necesarios:**

```python
# Ejemplo: Flask REST - API Endpoint
# app/servicios/termostatos/api.py
from flask import Blueprint, request, jsonify
from app.general.termostato import Termostato
from app.datos.termostatos.repositorio import get_repositorio

bp = Blueprint('termostatos', __name__, url_prefix='/api/termostatos')

@bp.route('/', methods=['GET'])
def get_termostatos():
    """Obtener todos los termostatos."""
    repo = get_repositorio()
    termostatos = repo.get_all()
    return jsonify([t.to_dict() for t in termostatos]), 200

@bp.route('/<int:id>', methods=['GET'])
def get_termostato(id: int):
    """Obtener termostato por ID."""
    repo = get_repositorio()
    termo = repo.get_by_id(id)
    if not termo:
        return jsonify({"error": "Not found"}), 404
    return jsonify(termo.to_dict()), 200
```

```python
# Ejemplo: Flask Webapp - Route + Template
# webapp/routes.py
from flask import Blueprint, render_template
from webapp.api_client import APIClient

main_bp = Blueprint('main', __name__)

@main_bp.route('/monitor')
def monitor():
    """Página de monitoreo."""
    api = APIClient()
    try:
        termostatos = api.get_termostatos()
        return render_template('monitor/index.html',
                             termostatos=termostatos,
                             title='Monitor')
    except Exception as e:
        return render_template('errors/500.html', error=str(e)), 500
```

**Estimación:** 45 minutos para agregar ejemplos de implementación

---

### ✅ Phase 4: Tests Unitarios

**Archivo:** `skills/implement-us/phases/phase-4-unit-tests.md`

**Uso de variables:**
- `{TEST_FRAMEWORK}` para fixtures y assertions
- `{COMPONENT_TYPE}` para nombrar tests
- `{BASE_CLASS}` para mocking

**Ejemplos actuales (21 menciones de stacks):**
- PyQt: pytest-qt, fixtures qapp/qtbot
- FastAPI: pytest + httpx, fixtures async_client
- Django: pytest-django, fixtures db/client
- Generic: pytest estándar

**Impacto Flask:**
- ✅ **REQUIERE CAMBIOS**
- Necesita ejemplos con Flask test client
- Necesita fixtures específicas de Flask

**Cambios necesarios:**

```python
# Ejemplo: Flask REST - Test de API
# tests/test_termostatos_api.py
import pytest

@pytest.fixture
def client(app):
    """Flask test client."""
    return app.test_client()

def test_get_termostatos(client):
    """Test GET /api/termostatos."""
    response = client.get('/api/termostatos/')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_get_termostato_not_found(client):
    """Test GET termostato inexistente."""
    response = client.get('/api/termostatos/999')
    assert response.status_code == 404
```

```python
# Ejemplo: Flask Webapp - Test de Template
# tests/test_monitor_routes.py
import pytest
from unittest.mock import patch

def test_monitor_page(client):
    """Test página de monitoreo."""
    with patch('webapp.routes.APIClient') as mock_api:
        mock_api.return_value.get_termostatos.return_value = [
            {'id': 1, 'nombre': 'Termo1'}
        ]
        response = client.get('/monitor')
        assert response.status_code == 200
        assert b'Monitor' in response.data
```

**Estimación:** 40 minutos para agregar ejemplos de tests

---

### ⚠️ Phase 5: Tests de Integración

**Archivo:** `skills/implement-us/phases/phase-5-integration-tests.md`

**Uso de variables:**
- Mínimo (tests de integración son mayormente genéricos)

**Impacto Flask:**
- ⚠️ **CAMBIOS MENORES**
- Puede beneficiarse de ejemplos de fixtures Flask

**Estimación:** 15 minutos (opcional)

---

### ⚠️ Phase 6: Validación BDD

**Archivo:** `skills/implement-us/phases/phase-6-bdd-validation.md`

**Uso de variables:**
- Ninguno (ejecuta pytest-bdd de forma genérica)

**Impacto Flask:**
- ❌ **NO requiere cambios**

---

### ✅ Phase 7: Quality Gates

**Archivo:** `skills/implement-us/phases/phase-7-quality-gates.md`

**Uso de variables:**
- Lee `quality_gates` del perfil
- Usa umbrales específicos por stack

**Ejemplos actuales:**
- PyQt: Coverage ≥90%, CC ≤12
- FastAPI: Coverage ≥95%, Pylint ≥8.5
- Generic: Coverage ≥95%

**Impacto Flask:**
- ✅ **REQUIERE CAMBIOS**
- Agregar umbrales de Flask REST (Coverage ≥95%, Pylint ≥8.0)
- Agregar umbrales de Flask Webapp (Coverage ≥90%, Pylint ≥8.0)

**Cambios necesarios:**

```markdown
### Flask REST API (flask-rest.json)
- **Pylint:** ≥8.0/10
- **Complejidad Ciclomática:** ≤10 por función
- **Índice Mantenibilidad:** ≥20
- **Coverage:** ≥95%

### Flask Webapp (flask-webapp.json)
- **Pylint:** ≥8.0/10
- **Complejidad Ciclomática:** ≤10 por función
- **Índice Mantenibilidad:** ≥20
- **Coverage:** ≥90% (solo backend, JS no incluido)
```

**Estimación:** 20 minutos

---

### ✅ Phase 8: Documentación

**Archivo:** `skills/implement-us/phases/phase-8-documentation.md`

**Uso de variables:**
- `{ARCHITECTURE_PATTERN}` para documentar arquitectura
- `{COMPONENT_TYPE}` para describir componentes

**Impacto Flask:**
- ⚠️ **CAMBIOS MENORES**
- La documentación es mayormente genérica
- Puede beneficiarse de ejemplos Flask

**Estimación:** 15 minutos (opcional)

---

### ✅ Phase 9: Reporte Final

**Archivo:** `skills/implement-us/phases/phase-9-final-report.md`

**Uso de variables:**
- Todas las variables para generar reporte completo

**Impacto Flask:**
- ❌ **NO requiere cambios**
- El reporte es generado dinámicamente desde variables

---

## Resumen de Cambios Necesarios

### Archivos que REQUIEREN actualización:

| Archivo | Cambios Necesarios | Estimación |
|---------|-------------------|------------|
| **phase-2-planning.md** | Agregar 2 ejemplos (Flask REST + Webapp) | 30 min |
| **phase-3-implementation.md** | Agregar ejemplos de código Flask | 45 min |
| **phase-4-unit-tests.md** | Agregar ejemplos de tests Flask | 40 min |
| **phase-7-quality-gates.md** | Agregar umbrales Flask | 20 min |
| **README.md** | Actualizar tabla de perfiles | 10 min |

**Total:** ~2h 25min

### Archivos OPCIONALES (mejora calidad):

| Archivo | Cambios Necesarios | Estimación |
|---------|-------------------|------------|
| phase-5-integration-tests.md | Ejemplos de fixtures Flask | 15 min |
| phase-8-documentation.md | Ejemplos de docs Flask | 15 min |

**Total opcional:** ~30 min

---

## Priorización de Cambios

### 🔴 Prioridad ALTA (Requerido para funcionar)

1. **phase-2-planning.md** - Sin ejemplos, los usuarios no sabrán qué tareas crear
2. **phase-3-implementation.md** - Sin ejemplos de código, no se puede implementar
3. **phase-4-unit-tests.md** - Sin ejemplos de tests, no se puede testear

### 🟡 Prioridad MEDIA (Mejora experiencia)

4. **phase-7-quality-gates.md** - Umbrales se pueden inferir del config.json, pero mejor explícitos
5. **README.md** - Necesario para documentación

### 🟢 Prioridad BAJA (Mejora calidad)

6. **phase-5-integration-tests.md** - Opcional, se puede inferir de tests unitarios
7. **phase-8-documentation.md** - Opcional, documentación es mayormente genérica

---

## Estrategias de Implementación

### Opción A: Implementación Secuencial (Conservadora)

```
1. Implementar TICKET-028 (flask-rest.json)
2. Actualizar phases con ejemplos Flask REST
3. Testing de TICKET-028 + phases
4. Implementar TICKET-029 (flask-webapp.json)
5. Actualizar phases con ejemplos Flask Webapp
6. Testing de TICKET-029 + phases
```

**Ventajas:**
- ✅ Cambios incrementales, más fácil detectar errores
- ✅ Testing intermedio reduce riesgos

**Desventajas:**
- ❌ Más tiempo total (2 ciclos de actualización)
- ❌ Más commits

**Estimación:** 6-7 horas total

---

### Opción B: Implementación en Batch (Eficiente) ⭐ RECOMENDADA

```
1. Implementar TICKET-028 + TICKET-029 juntos
2. Actualizar todas las phases con ambos ejemplos Flask
3. Testing completo de ambos perfiles + phases
4. Commit único con familia Flask completa
```

**Ventajas:**
- ✅ Más eficiente (solo 1 ciclo de actualización)
- ✅ Commit atómico con familia Flask completa
- ✅ Menos context switching

**Desventajas:**
- ⚠️ Cambios más grandes, necesita testing exhaustivo

**Estimación:** 4.5-5.5 horas total

**Desglose:**
- TICKET-028 implementación: 1h
- TICKET-029 implementación: 1.5h
- Actualización de phases: 2.5h
- Testing: 1h
- Documentación: 0.5h

---

### Opción C: Implementación Lazy (Mínima) ❌ NO RECOMENDADA

```
1. Implementar TICKET-028 + TICKET-029
2. NO actualizar phases
3. Confiar en que Claude Code infiera comportamiento de config.json
```

**Ventajas:**
- ✅ Mínimo esfuerzo inmediato

**Desventajas:**
- ❌ Experiencia de usuario degradada
- ❌ Claude puede generar código inconsistente
- ❌ Sin ejemplos, usuarios no saben qué esperar
- ❌ Deuda técnica acumulada

**Estimación:** 2.5h (pero genera deuda técnica)

---

## Impacto en Templates

### Templates Actuales

```
templates/
├── bdd/
│   └── scenario.feature           ⚠️ Genérico, no requiere cambios
├── planning/
│   └── implementation-plan.md     ⚠️ Genérico, ejemplos en phase-2
├── testing/
│   ├── test-unit.py              ✅ Requiere ejemplos Flask
│   └── test-integration.py       ⚠️ Mayormente genérico
└── reporting/
    └── implementation-report.md   ⚠️ Generado dinámicamente
```

**Impacto Templates:** BAJO (solo test-unit.py necesita ejemplos Flask opcionales)

---

## Recomendación Final

### Estrategia Recomendada: **Opción B (Batch Implementation)**

**Razones:**
1. ✅ Flask REST y Flask Webapp son muy relacionados (misma familia)
2. ✅ Las phases necesitan ejemplos de AMBOS perfiles
3. ✅ Commit atómico mantiene consistencia
4. ✅ Más eficiente que 2 ciclos separados

**Plan de Acción:**

```
Sprint 2 - Extensión Flask (5.5h estimadas)

PARTE 1: Implementación de Perfiles (2.5h)
├── TICKET-028: Implementar flask-rest.json (1h)
└── TICKET-029: Implementar flask-webapp.json (1.5h)

PARTE 2: Actualización de Phases (2.5h)
├── phase-2-planning.md: Agregar ejemplos Flask (30 min)
├── phase-3-implementation.md: Agregar código Flask (45 min)
├── phase-4-unit-tests.md: Agregar tests Flask (40 min)
├── phase-7-quality-gates.md: Agregar umbrales (20 min)
└── README.md: Actualizar documentación (10 min)

PARTE 3: Testing y Validación (1h)
├── Validar JSONs (5 min)
├── Validar ejemplos en phases (30 min)
└── Testing manual (25 min)

PARTE 4: Documentación (30 min)
├── Actualizar TICKET-028 con estado final
├── Actualizar TICKET-029 con estado final
├── Actualizar session-current.md
└── Commit final
```

---

## Métricas de Impacto

### Archivos Totales Afectados

| Categoría | Cantidad | Archivos |
|-----------|----------|----------|
| **Perfiles JSON** | 2 | flask-rest.json, flask-webapp.json |
| **Phases (Requerido)** | 3 | phase-2, phase-3, phase-4 |
| **Phases (Opcional)** | 2 | phase-5, phase-8 |
| **Quality Gates** | 1 | phase-7 |
| **Documentación** | 1 | README.md |
| **Tickets** | 2 | TICKET-028, TICKET-029 |
| **TOTAL** | **11 archivos** | |

### Líneas de Código Estimadas

| Categoría | Líneas |
|-----------|--------|
| flask-rest.json | ~520 |
| flask-webapp.json | ~590 |
| Ejemplos en phases | ~400-500 |
| Documentación | ~100 |
| **TOTAL** | **~1,610-1,710 líneas** |

---

## Conclusión

**¿Los perfiles Flask impactan en otros agentes?**

**Respuesta: SÍ, impacto MEDIO-ALTO**

- ✅ **7 de 10 phases** usan variables de perfiles
- ✅ **3 phases críticas** requieren ejemplos (planning, implementation, tests)
- ✅ **~2.5h adicionales** para actualizar phases correctamente
- ✅ Implementación en batch (Opción B) es la más eficiente

**Sin actualizar las phases:**
- El sistema funcionará técnicamente (lee variables de config)
- Pero la experiencia de usuario será degradada (sin ejemplos de referencia)
- Claude Code tendrá que inferir patrones Flask sin guía explícita

**Recomendación:** Implementar Opción B (Batch) para mantener consistencia y calidad del framework.

---

**Próxima decisión del usuario:** ¿Proceder con Opción A, B, o C?
