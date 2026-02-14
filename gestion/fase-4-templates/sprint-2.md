# Sprint 2 - Fase 4: Generalización de Templates

**Fecha Inicio:** 2026-02-14
**Fecha Fin Estimada:** 2026-02-15
**Sprint:** 2 (Semana 2)
**Estado:** 📋 Planificado

---

## Objetivos de la Fase

Generalizar los 4 templates existentes (`bdd-scenario.feature`, `implementation-plan.md`, `implementation-report.md`, `test-unit.py`) para que sean framework-agnostic y funcionen con cualquier perfil tecnológico mediante el sistema de variables.

---

## Tareas (Tickets)

### Pendientes 📋

- [ ] **TICKET-030**: Análisis exhaustivo de templates y planificación de generalización
- [ ] **TICKET-031**: Crear estructura de directorios `templates/`
- [ ] **TICKET-032**: Generalizar template `bdd-scenario.feature`
- [ ] **TICKET-033**: Generalizar template `implementation-plan.md`
- [ ] **TICKET-034**: Generalizar template `implementation-report.md`
- [ ] **TICKET-035**: Generalizar template `test-unit.py`
- [ ] **TICKET-036**: Testing y validación de templates generalizados
- [ ] **TICKET-037**: Documentación de templates y sistema de variables

### Completados ✅

Ninguno aún.

### Desestimados ❌

Ninguno.

### En Progreso 🔄

Ninguno.

---

## Métricas

- **Total de Tickets:** 8
- **Completados:** 0 (0%)
- **Desestimados:** 0 (0%)
- **En Progreso:** 0 (0%)
- **Pendientes:** 8 (100%)
- **Bloqueados:** 0

**Estimación Total:** 8 horas
- Análisis y planificación: 1h
- Estructura y setup: 0.5h
- Generalización de templates (4): 4h
- Testing y validación: 1.5h
- Documentación: 1h

**Progreso:** ░░░░░░░░░░░░░░░░ 0% (0/8 tickets)

**Entregables Esperados:**
- 4 templates generalizados y validados
- Sistema de variables documentado
- README completo con ejemplos de uso
- Tests de validación de templates

---

## Dependencias

**Depende de:**
- ✅ Fase 3: Generalización de Skills (completada)
  - Sistema de variables definido
  - 5 perfiles funcionales creados
  - Arquitectura modular establecida

**Bloquea a:**
- Fase 5: Sistema de Tracking
- Fase 6: Documentación (requiere templates finalizados)
- Fase 7: Ejemplos (requiere templates funcionando)

---

## Criterios de Aceptación de la Fase

- [ ] Estructura `templates/` creada con subdirectorios por categoría
- [ ] Los 4 templates generalizados sin referencias específicas:
  - [ ] `bdd-scenario.feature` - Framework agnostic
  - [ ] `implementation-plan.md` - Sin referencias MVC/PyQt/Factory/Coordinator
  - [ ] `implementation-report.md` - Sin referencias específicas
  - [ ] `test-unit.py` - Sin imports hardcodeados de PyQt/pytest-qt
- [ ] Sistema de variables expandido para cubrir necesidades de templates
- [ ] Templates validados con al menos 3 perfiles diferentes (pyqt-mvc, fastapi-rest, flask-rest)
- [ ] Documentación completa de variables disponibles
- [ ] README con ejemplos de uso por perfil
- [ ] Tests automatizados de generación de templates (opcional pero deseable)

---

## Análisis de Templates Existentes

### 1. bdd-scenario.feature (897 bytes)

**Estado actual:** ~90% genérico
**Variables usadas:** `{FEATURE_TITLE}`, `{US_ID}`, `{USER_ROLE}`, `{USER_WANT}`, `{USER_BENEFIT}`
**Trabajo requerido:** Mínimo - solo ajustes en Background (aplicación/configuración son específicos)

### 2. implementation-plan.md (2,902 bytes)

**Estado actual:** ~40% genérico
**Referencias específicas a remover:**
- Factory/Coordinator/Compositor (líneas 98-99, 143-149)
- Señales PyQt específicas
- "panel", "controladores" hardcodeados

**Variables a agregar:**
- `{INTEGRATION_PATTERN}` - Para reemplazar Factory/Coordinator
- `{COMPONENT_INTEGRATION}` - Cómo se integran componentes

### 3. implementation-report.md (6,332 bytes)

**Estado actual:** ~30% genérico
**Referencias específicas a remover:**
- Factory/Coordinator/Compositor (líneas 122-149)
- "Pruebas con RPi Real" (líneas 219-224) - muy específico
- Señales PyQt específicas

**Variables a agregar:**
- Mismas que implementation-plan.md
- `{DEPLOYMENT_TESTING}` - Para reemplazar pruebas con RPi

### 4. test-unit.py (4,492 bytes)

**Estado actual:** ~20% genérico
**Referencias específicas a remover:**
- `from PyQt6.QtCore import QTimer` (línea 16)
- `pytest-qt` fixtures (`qapp`, `qtbot`) (líneas 77-94)
- Clase `TestSignals` completa es PyQt-specific

**Variables a agregar:**
- `{TEST_IMPORTS}` - Imports específicos del framework
- `{TEST_FRAMEWORK_FIXTURES}` - Fixtures específicas
- `{ASYNC_TEST_DECORATOR}` - Para FastAPI/Flask async

---

## Sistema de Variables a Expandir

Variables actuales (de Fase 3):
- `{ARCHITECTURE_PATTERN}`, `{COMPONENT_TYPE}`, `{COMPONENT_PATH}`
- `{TEST_FRAMEWORK}`, `{BASE_CLASS}`, `{COMPONENT_NAME}`
- `{US_ID}`, `{US_TITLE}`

**Variables nuevas para templates:**

| Variable | Propósito | Ejemplo Valores |
|----------|-----------|-----------------|
| `{INTEGRATION_PATTERN}` | Cómo se integran componentes | Factory/Coordinator, Dependency Injection, Router Registration |
| `{COMPONENT_INTEGRATION}` | Snippet de integración | Factory method, app.include_router(), Blueprint.register() |
| `{TEST_IMPORTS}` | Imports específicos del framework | PyQt6, FastAPI TestClient, Flask test_client |
| `{TEST_FRAMEWORK_FIXTURES}` | Fixtures del framework | qapp/qtbot, async fixtures, flask app |
| `{ASYNC_TEST_DECORATOR}` | Decorador para tests async | @pytest.mark.asyncio, ninguno |
| `{DEPLOYMENT_TESTING}` | Cómo se testea deployment | RPi real, Docker container, Cloud deploy |
| `{BACKGROUND_SETUP}` | Setup del escenario BDD | GUI iniciada, API running, DB migrated |

---

## Estrategia de Generalización

### Enfoque por Niveles

**Nivel 1: Variables Simples**
- Reemplazar hardcoded strings con `{VARIABLE}`
- Ejemplo: "Factory" → `{INTEGRATION_PATTERN}`

**Nivel 2: Bloques Condicionales**
- Usar comentarios para indicar secciones opcionales
- Ejemplo:
  ```markdown
  <!-- PROFILE: pyqt-mvc -->
  ### Factory Integration
  ...
  <!-- /PROFILE -->
  ```

**Nivel 3: Snippets por Perfil**
- Crear snippets específicos por perfil en perfiles JSON
- El skill elige el snippet correcto al generar

### Ejemplo de Snippet en Perfil

```json
{
  "profile_name": "pyqt-mvc",
  "template_snippets": {
    "integration_pattern": "Factory/Coordinator",
    "component_integration": "# Método agregado a ComponenteFactoryUX\ndef _crear_ctrl_{component_name}(self):\n    ...",
    "test_imports": "from PyQt6.QtCore import QTimer\nfrom PyQt6.QtWidgets import QWidget",
    "test_framework_fixtures": "qapp, qtbot",
    "async_test_decorator": "",
    "background_setup": "Given la aplicación está iniciada\nAnd la configuración está cargada"
  }
}
```

---

## Estructura de Directorios Objetivo

```
templates/
├── README.md                    # Documentación de templates
├── bdd/
│   ├── scenario.feature        # Template BDD generalizado
│   └── examples/               # Ejemplos por perfil
│       ├── pyqt-mvc.feature
│       ├── fastapi-rest.feature
│       └── flask-webapp.feature
├── planning/
│   ├── implementation-plan.md  # Template de plan generalizado
│   └── examples/
│       ├── pyqt-mvc.md
│       ├── fastapi-rest.md
│       └── flask-webapp.md
├── testing/
│   ├── test-unit.py           # Template de test generalizado
│   ├── test-integration.py    # (nuevo) Template de test integración
│   └── examples/
│       ├── pyqt-mvc.py
│       ├── fastapi-rest.py
│       └── flask-webapp.py
└── reporting/
    ├── implementation-report.md # Template de reporte generalizado
    └── examples/
        ├── pyqt-mvc.md
        ├── fastapi-rest.md
        └── flask-webapp.md
```

---

## Riesgos Identificados

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Templates demasiado genéricos pierden utilidad | Media | Alto | Mantener snippets específicos por perfil |
| Variables no cubren todos los casos de uso | Alta | Medio | Iteración incremental, agregar variables según necesidad |
| Complejidad de mantenimiento de snippets | Media | Medio | Documentar claramente cada snippet |
| Bloques condicionales difíciles de leer | Baja | Bajo | Usar sintaxis clara con comentarios HTML |

---

## Checklist Pre-Commit

Antes de hacer commit de esta fase:
- [ ] Los 4 templates generalizados sin referencias específicas
- [ ] Templates validados con 3+ perfiles diferentes
- [ ] Sistema de variables documentado en README
- [ ] Ejemplos creados para cada template x perfil
- [ ] Snippets agregados a cada perfil JSON
- [ ] Tests de generación (si aplica)
- [ ] Actualizar CHANGELOG.md
- [ ] Actualizar session-current.md

---

## Retrospectiva (Al finalizar)

### ¿Qué salió bien?

_A completar al finalizar la fase._

### ¿Qué se puede mejorar?

_A completar al finalizar la fase._

### Lecciones Aprendidas

_A completar al finalizar la fase._

---

## Siguiente Fase

**Fase 5: Sistema de Tracking** - Ver `gestion/fase-5-sistema-tracking/sprint-2.md`

---

**Última Actualización:** 2026-02-14 (Planificación inicial creada)
