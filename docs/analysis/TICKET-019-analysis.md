# TICKET-019: Análisis del Skill implement-us Actual

**Fecha:** 2026-02-09
**Objetivo:** Identificar todas las referencias específicas de framework y documentar puntos de generalización
**Estado:** ✅ Completado

---

## 1. Resumen Ejecutivo

El skill `implement-us.md` actual está fuertemente acoplado a:
- **Stack tecnológico:** PyQt6
- **Patrón arquitectónico:** MVC + Factory/Coordinator
- **Proyecto específico:** ISSE_Simuladores
- **Framework de testing:** pytest-qt

**Líneas de código analizadas:** 707 líneas
**Referencias específicas identificadas:** 47 puntos

---

## 2. Referencias Específicas Identificadas

### 2.1 Referencias al Stack Tecnológico (PyQt)

| Línea | Contexto | Referencia Específica |
|-------|----------|-----------------------|
| 5 | Descripción | "arquitectura MVC + Factory/Coordinator" |
| 11 | Propósito | "proyecto ISSE_Simuladores" |
| 13 | Propósito | "arquitectura de referencia (ADR-003)" |
| 14 | Propósito | "Implementación MVC completa" |
| 50 | Fase 0 | "Verificar patrones: MVC, Factory, Coordinator" |
| 118 | Fase 2 | "Si es panel UI → Modelo + Vista + Controlador" |
| 131 | Ejemplo | "Panel Display (MVC)" |
| 132-134 | Ejemplo | Rutas específicas: `app/presentacion/paneles/display/` |
| 224 | Ejemplo | "Patrón: Modelo MVC (dataclass inmutable)" |
| 226 | Ejemplo | "Referencia: Revisar PanelEstadoModelo en simulador_bateria" |
| 310 | Fase 5 | "Usar mocks de PyQt (pytest-qt)" |

### 2.2 Referencias al Patrón Arquitectónico (MVC)

| Componente | Referencias |
|------------|-------------|
| **Modelo** | Lines 132, 224, 258, 267-283 |
| **Vista** | Lines 133, 259, 332 |
| **Controlador** | Lines 134, 260, 308, 322 |
| **Factory** | Lines 50, 122, 525 |
| **Coordinator** | Lines 50, 122, 526 |

### 2.3 Referencias a Componentes Específicos

**Componentes hardcodeados encontrados:**
- `DisplayModelo` (múltiples referencias)
- `DisplayVista` (múltiples referencias)
- `DisplayControlador` (múltiples referencias)
- `ServidorEstado` (lines 138, 305, 319)
- `EstadoTermostato` (line 306)
- `PanelEstadoModelo` (line 226)

### 2.4 Referencias a Rutas de Proyecto

**Rutas hardcodeadas:**
```
app/presentacion/paneles/display/modelo.py
app/presentacion/paneles/display/vista.py
app/presentacion/paneles/display/controlador.py
tests/test_display_modelo.py
tests/features/US-XXX-*.feature
docs/plans/US-XXX-plan.md
quality/reports/US-XXX-quality.json
```

### 2.5 Referencias a Framework de Testing

| Línea | Referencia |
|-------|------------|
| 310 | "pytest-qt" |
| 315 | "def test_display_actualiza_desde_servidor(qapp, qtbot):" |
| 576-580 | Dependencias: pytest-qt |

### 2.6 Referencias al Dominio del Problema

**Dominio específico: Termostato/HVAC**
- "temperatura" (múltiples referencias)
- "termostato está encendido"
- "Raspberry Pi"
- "climatizador"

---

## 3. Análisis por Fase del Skill

### Fase 0: Validación de Contexto
**Estado:** ⚠️ Parcialmente genérico

**Específico:**
- Line 45: `{producto}/docs/HISTORIAS-USUARIO-*.md` (estructura de docs específica)
- Line 49: "ADR-003" (documento específico del proyecto)
- Line 50: "Verificar patrones: MVC, Factory, Coordinator"

**Generalizable:**
✅ Búsqueda de US en docs
✅ Validación de arquitectura
✅ Verificación de estándares

**Propuesta de generalización:**
- Variable: `{ARCHITECTURE_PATTERN}` → "mvc", "mvt", "layered", etc.
- Variable: `{ARCHITECTURE_DOC}` → "ADR-003", "architecture.md", etc.
- Variable: `{PATTERNS}` → Lista de patrones según perfil

---

### Fase 1: Generación de Escenarios BDD
**Estado:** ✅ Mayormente genérico

**Específico:**
- Line 87-93: Ejemplo usa dominio de termostato

**Generalizable:**
✅ Template BDD genérico
✅ Proceso de generación agnóstico

**Propuesta:**
- Mantener como está
- Ejemplos deben ser genéricos o múltiples por dominio

---

### Fase 2: Plan de Implementación
**Estado:** ❌ Altamente específico

**Específico:**
- Lines 118-123: Estructura de componentes MVC hardcodeada
- Lines 131-148: Ejemplo completo de panel MVC con rutas específicas

**Generalizable:**
❌ Estructura de componentes (depende del patrón)
❌ Rutas de archivos
❌ Estimaciones de tiempo (puede variar por stack)

**Propuesta de generalización:**

**Configuración base:**
```json
{
  "component_structure": {
    "mvc": {
      "layers": ["modelo", "vista", "controlador"],
      "base_path": "app/presentacion/{component_name}/"
    },
    "mvt": {
      "layers": ["model", "view", "template"],
      "base_path": "app/{component_name}/"
    },
    "layered": {
      "layers": ["domain", "service", "controller"],
      "base_path": "src/{layer}/{component_name}/"
    }
  }
}
```

**Template generalizado:**
```markdown
### 1. {COMPONENT_NAME} ({ARCHITECTURE_PATTERN})
{{#each layers}}
- [ ] {COMPONENT_PATH}/{layer}.py ({estimated_time} min)
{{/each}}
```

---

### Fase 3: Implementación Guiada por Tareas
**Estado:** ⚠️ Parcialmente genérico

**Específico:**
- Lines 222-234: Ejemplo de guía usa "DisplayModelo"
- Line 224: "Patrón: Modelo MVC (dataclass inmutable)"
- Line 226: Referencia a componente específico del proyecto

**Generalizable:**
✅ Flujo de trabajo de tareas
✅ Sistema de tracking
✅ Aprobación por tarea
✅ Actualización de plan

**Propuesta:**
- Crear templates de código por patrón
- Variables: `{COMPONENT_NAME}`, `{LAYER_TYPE}`, `{BASE_CLASS}`
- Referencia a ejemplos debe ser dinámica según perfil

---

### Fase 4: Tests Unitarios
**Estado:** ⚠️ Semi-específico

**Específico:**
- Lines 257-260: Tipos de tests específicos a MVC
- Lines 267-283: Ejemplo de test usa DisplayModelo

**Generalizable:**
✅ Proceso de testing
✅ Coverage targets
❌ Qué testear (depende del componente)

**Propuesta:**
- Configuración por patrón de qué testear:
```json
{
  "testing_strategy": {
    "mvc": {
      "modelo": ["validación", "inmutabilidad"],
      "vista": ["renderizado", "actualización"],
      "controlador": ["señales", "lógica"]
    },
    "layered": {
      "domain": ["business_logic", "validation"],
      "service": ["orchestration", "error_handling"],
      "controller": ["input_validation", "response_formatting"]
    }
  }
}
```

---

### Fase 5: Tests de Integración
**Estado:** ❌ Altamente específico

**Específico:**
- Lines 304-332: Test completo usa componentes específicos de PyQt
- Line 310: "pytest-qt"
- Line 315: Fixtures específicos: `qapp, qtbot`
- Lines 319-327: Flujo específico de ServidorEstado → DisplayControlador

**Generalizable:**
❌ Framework de testing (pytest-qt)
❌ Componentes a integrar
❌ Flujo de datos

**Propuesta:**
- Variable: `{TEST_FRAMEWORK}` → "pytest-qt", "pytest-django", "pytest", etc.
- Variable: `{INTEGRATION_PATTERN}` → Descripción del flujo según arquitectura
- Templates de integración por stack

**Ejemplo de config:**
```json
{
  "integration_testing": {
    "pyqt-mvc": {
      "framework": "pytest-qt",
      "fixtures": ["qapp", "qtbot"],
      "pattern": "signal_slot_connection"
    },
    "fastapi-rest": {
      "framework": "pytest",
      "fixtures": ["client", "db_session"],
      "pattern": "api_endpoint_flow"
    }
  }
}
```

---

### Fase 6: Validación BDD
**Estado:** ✅ Genérico

**Específico:**
Ninguno (excepto nombres de archivos de ejemplo)

**Propuesta:**
Mantener como está.

---

### Fase 7: Quality Gates
**Estado:** ✅ Genérico

**Específico:**
- Line 389: Ruta específica `app/presentacion/paneles/display/`

**Propuesta:**
- Variable: `{COMPONENT_PATH}` en comandos

---

### Fase 8: Actualización de Documentación
**Estado:** ✅ Genérico

Sin cambios necesarios.

---

### Fase 9: Reporte Final
**Estado:** ✅ Mayormente genérico

**Específico:**
- Ejemplos usan componentes MVC específicos

**Propuesta:**
Template debe usar variables para nombres de componentes.

---

## 4. Configuración del Skill (líneas 539-568)

**Estado:** ⚠️ Parcialmente genérico

**Específico:**
- Line 555: `templates_dir`, `plans_dir`, `reports_dir` (rutas hardcodeadas)

**Propuesta:**
- Configuración base con defaults
- Perfiles pueden override estas rutas

---

## 5. Dependencias (líneas 572-581)

**Estado:** ❌ Específico a PyQt

**Dependencias listadas:**
```
- pytest
- pytest-qt      ← Específico PyQt
- pytest-bdd
- pytest-cov
- pylint
- radon
```

**Propuesta:**
- Configuración de dependencias por perfil:
```json
{
  "dependencies": {
    "core": ["pytest", "pytest-cov", "pylint", "radon"],
    "pyqt-mvc": ["pytest-qt"],
    "fastapi-rest": ["httpx", "pytest-asyncio"],
    "django-mvt": ["pytest-django"]
  }
}
```

---

## 6. Matriz de Generalización

### Variables a Introducir

| Variable | Uso | Ejemplos |
|----------|-----|----------|
| `{ARCHITECTURE_PATTERN}` | Identificar patrón | "mvc", "mvt", "layered", "hexagonal" |
| `{COMPONENT_TYPE}` | Tipo de componente | "Panel", "Service", "View", "Controller" |
| `{COMPONENT_NAME}` | Nombre del componente | "Display", "UserProfile", "OrderProcessor" |
| `{COMPONENT_PATH}` | Ruta base del componente | "app/presentacion/paneles/display" |
| `{LAYER_TYPE}` | Capa arquitectónica | "modelo", "vista", "controlador" |
| `{BASE_CLASS}` | Clase base según patrón | "ModeloBase", "BaseService", "APIView" |
| `{TEST_FRAMEWORK}` | Framework de testing | "pytest-qt", "pytest-django", "pytest" |
| `{INTEGRATION_PATTERN}` | Patrón de integración | "signal_slot", "http_request", "event_bus" |

### Secciones que Necesitan Generalización

| Sección | Prioridad | Complejidad | Impacto |
|---------|-----------|-------------|---------|
| Descripción y Propósito | 🔴 Alta | Baja | Alto |
| Fase 0: Validación | 🟡 Media | Media | Medio |
| Fase 2: Plan de Implementación | 🔴 Alta | Alta | Alto |
| Fase 3: Implementación | 🔴 Alta | Alta | Alto |
| Fase 4: Tests Unitarios | 🟡 Media | Media | Medio |
| Fase 5: Tests de Integración | 🔴 Alta | Alta | Alto |
| Configuración | 🟡 Media | Baja | Medio |
| Dependencias | 🟡 Media | Baja | Medio |

---

## 7. Estrategia de Generalización Recomendada

### Paso 1: Crear Configuración Base
Archivo: `skills/implement-us/config.json`

```json
{
  "skill_version": "2.0-generic",
  "architecture_pattern": "generic",
  "component_structure": {},
  "testing_strategy": {},
  "quality_gates": {
    "pylint_min": 8.0,
    "cc_max": 10,
    "mi_min": 20,
    "coverage_min": 95
  },
  "templates_dir": ".claude/templates",
  "plans_dir": "docs/plans",
  "reports_dir": "docs/reports"
}
```

### Paso 2: Crear Perfiles de Customización

#### skills/implement-us/customizations/pyqt-mvc.json
```json
{
  "extends": "base",
  "architecture_pattern": "mvc",
  "display_name": "PyQt6 MVC + Factory/Coordinator",
  "component_structure": {
    "layers": ["modelo", "vista", "controlador"],
    "base_path": "app/presentacion/{component_type}/{component_name}/",
    "file_pattern": "{layer}.py"
  },
  "base_classes": {
    "modelo": "ModeloBase",
    "vista": "VistaBase",
    "controlador": "ControladorBase"
  },
  "testing": {
    "framework": "pytest-qt",
    "fixtures": ["qapp", "qtbot"],
    "integration_pattern": "signal_slot_connection"
  },
  "dependencies": ["pytest-qt"],
  "patterns": ["Factory", "Coordinator", "Observer"]
}
```

#### skills/implement-us/customizations/fastapi-rest.json
```json
{
  "extends": "base",
  "architecture_pattern": "layered",
  "display_name": "FastAPI REST + Layered Architecture",
  "component_structure": {
    "layers": ["domain", "service", "controller"],
    "base_path": "src/{layer}/{component_name}/",
    "file_pattern": "{component_name}_{layer}.py"
  },
  "base_classes": {
    "domain": "BaseModel",
    "service": "BaseService",
    "controller": "APIRouter"
  },
  "testing": {
    "framework": "pytest",
    "fixtures": ["client", "db_session"],
    "integration_pattern": "http_api_flow"
  },
  "dependencies": ["httpx", "pytest-asyncio"],
  "patterns": ["Dependency Injection", "Repository", "Service Layer"]
}
```

#### skills/implement-us/customizations/django-mvt.json
```json
{
  "extends": "base",
  "architecture_pattern": "mvt",
  "display_name": "Django MVT",
  "component_structure": {
    "layers": ["models", "views", "templates"],
    "base_path": "{app_name}/",
    "file_pattern": "{layer}.py"
  },
  "base_classes": {
    "models": "models.Model",
    "views": "View",
    "templates": null
  },
  "testing": {
    "framework": "pytest-django",
    "fixtures": ["client", "db"],
    "integration_pattern": "request_response"
  },
  "dependencies": ["pytest-django"],
  "patterns": ["ORM", "Class-Based Views", "Template Tags"]
}
```

#### skills/implement-us/customizations/generic-python.json
```json
{
  "extends": "base",
  "architecture_pattern": "generic",
  "display_name": "Generic Python Project",
  "component_structure": {
    "layers": ["implementation"],
    "base_path": "src/{component_name}/",
    "file_pattern": "{component_name}.py"
  },
  "base_classes": {},
  "testing": {
    "framework": "pytest",
    "fixtures": [],
    "integration_pattern": "function_call"
  },
  "dependencies": [],
  "patterns": []
}
```

### Paso 3: Reescribir implement-us.md

**Estructura propuesta:**
```markdown
# Skill: implement-us

**Versión:** 2.0 (Genérico)

## Descripción
Implementador asistido de Historias de Usuario agnóstico de framework.

**Patrones soportados:**
- PyQt6 MVC + Factory/Coordinator
- FastAPI REST + Layered Architecture
- Django MVT
- Generic Python

## Configuración
El skill lee `.claude/skills/implement-us/config.json` para determinar:
- Patrón arquitectónico
- Estructura de componentes
- Framework de testing
- Patrones de diseño

[... resto del documento con variables en lugar de valores hardcodeados ...]
```

---

## 8. Puntos Críticos para TICKET-021

Al generalizar `implement-us.md` en TICKET-021, **DEBE**:

1. ✅ Reemplazar TODAS las menciones a MVC con `{ARCHITECTURE_PATTERN}`
2. ✅ Reemplazar TODAS las rutas hardcodeadas con `{COMPONENT_PATH}`
3. ✅ Reemplazar nombres de componentes con `{COMPONENT_NAME}`
4. ✅ Agregar sección de configuración al inicio explicando perfiles
5. ✅ Crear ejemplos múltiples (uno por patrón) en lugar de uno solo
6. ✅ Documentar sistema de variables
7. ✅ Explicar cómo se fusionan config base + perfil

---

## 9. Estimación de Impacto

### Líneas a Modificar
- **Descripción (líneas 1-26):** ~15 líneas
- **Fase 0 (líneas 32-62):** ~10 líneas
- **Fase 2 (líneas 105-161):** ~40 líneas (más crítico)
- **Fase 3 (líneas 164-242):** ~30 líneas
- **Fase 4 (líneas 245-291):** ~20 líneas
- **Fase 5 (líneas 294-338):** ~30 líneas (más crítico)
- **Configuración (líneas 539-568):** ~20 líneas
- **Dependencias (líneas 572-581):** ~5 líneas

**Total de líneas a modificar:** ~170 de 707 (24%)

### Nuevas Secciones a Agregar
1. Sección "Configuración y Perfiles" (~50 líneas)
2. Sección "Sistema de Variables" (~30 líneas)
3. Ejemplos adicionales por patrón (~100 líneas)

**Tamaño estimado del skill generalizado:** ~890 líneas

---

## 10. Conclusiones y Recomendaciones

### ✅ Aspectos Positivos del Skill Actual
- Flujo de trabajo bien definido (9 fases)
- Sistema de tracking de tiempo robusto
- Quality gates claros
- Documentación exhaustiva

### ⚠️ Desafíos de Generalización
- Alta especificidad a PyQt/MVC
- Ejemplos muy acoplados a dominio termostato
- Rutas y nombres hardcodeados en múltiples lugares
- Testing strategy específica a pytest-qt

### 🎯 Recomendaciones

1. **Orden de implementación (TICKETS 020-026):**
   - TICKET-020: Crear estructura de directorios ✅
   - TICKET-022: Crear config.json base primero (antes de generalizar)
   - TICKET-021: Generalizar implement-us.md (con config base lista)
   - TICKET-023-026: Crear perfiles uno por uno

2. **Estrategia de testing:**
   - Validar cada perfil después de crearlo
   - Crear ejemplos de US genéricas para testing
   - Probar generación de código con cada perfil

3. **Documentación:**
   - Crear guía de customización (cómo crear nuevos perfiles)
   - Documentar sistema de variables
   - Ejemplos de uso por cada perfil

4. **Compatibilidad hacia atrás:**
   - El perfil pyqt-mvc debe generar código idéntico al skill actual
   - Esto facilita validación y migración

---

## 11. Próximos Pasos (Siguientes Tickets)

### TICKET-020: Crear Estructura de Directorios ✅
```bash
mkdir -p skills/implement-us/{phases,customizations}
```

### TICKET-021: Generalizar implement-us.md
Usar este análisis como referencia para:
- Identificar cada punto a generalizar
- Aplicar variables sistemáticamente
- Agregar documentación de configuración

### TICKET-022: Crear config.json Base
Implementar configuración base genérica según Sección 7.

### TICKET-023-026: Crear Perfiles
Implementar los 4 perfiles según especificaciones en Sección 7.

---

**Análisis completado:** 2026-02-09
**Tiempo invertido:** ~1.5h
**Próximo ticket:** TICKET-020
