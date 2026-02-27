# Skill: implement-us

**Nombre del comando:** `/implement-us`

**Descripción:** Implementador asistido de Historias de Usuario siguiendo el patrón arquitectónico configurado para el proyecto.

**Arquitectura:** Orquestador modular que delega cada fase a un agente especializado.

---

## Variables Disponibles

Este skill utiliza las siguientes variables definidas en `config.json` y personalizables mediante perfiles en `customizations/`:

| Variable | Descripción | Valor Default | Ejemplos por Perfil |
|----------|-------------|---------------|---------------------|
| `{ARCHITECTURE_PATTERN}` | Patrón arquitectónico del proyecto | `generic` | **PyQt:** `mvc`<br>**FastAPI:** `layered`<br>**Generic:** `generic` |
| `{COMPONENT_TYPE}` | Tipo de componente a implementar | `Component` | **PyQt:** `Panel`, `Dialog`<br>**FastAPI:** `Endpoint`, `Service`<br>**Generic:** `Module` |
| `{COMPONENT_PATH}` | Ruta base para componentes | `src/{name}/` | **PyQt:** `app/presentacion/{name}/`<br>**FastAPI:** `app/{layer}/{name}/`<br>**Generic:** `src/{name}/` |
| `{TEST_FRAMEWORK}` | Framework de testing | `pytest` | **PyQt:** `pytest + pytest-qt`<br>**FastAPI:** `pytest + httpx`<br>**Generic:** `pytest` |
| `{BASE_CLASS}` | Clase base para componentes | `object` | **PyQt:** `QWidget`, `ModeloBase`<br>**FastAPI:** `BaseModel`, `BaseService`<br>**Generic:** `object` |
| `{DOMAIN_CONTEXT}` | Contexto de dominio del proyecto | `application` | **PyQt:** `presentacion`, `dominio`<br>**FastAPI:** `api`, `domain`<br>**Generic:** `domain` |
| `{PROJECT_ROOT}` | Raíz del proyecto | `.` | **PyQt:** `app/`<br>**FastAPI:** `src/`<br>**Generic:** `.` |
| `{PRODUCT}` | Nombre del producto/módulo | `main` | Cualquier nombre de producto/módulo |

### Cómo se Resuelven las Variables

Las variables se resuelven en el siguiente orden de prioridad:

1. **Perfil de customización** (`.claude/skills/implement-us/customizations/{perfil}.json`)
2. **Configuración base** (`.claude/skills/implement-us/config.json`)
3. **Valores por defecto** (tabla anterior)

**Ejemplo de configuración:**

```json
{
  "architecture_pattern": "mvc",
  "component_type": "Panel",
  "component_path": "app/presentacion/paneles/{name}/",
  "test_framework": "pytest-qt",
  "base_class": "ModeloBase",
  "domain_context": "presentacion",
  "project_root": "app/"
}
```

---

## Propósito

Este skill guía paso a paso la implementación de una Historia de Usuario (US) en cualquier proyecto Python, asegurando:

- Adherencia a la arquitectura configurada para el proyecto
- Generación de escenarios BDD
- Implementación completa según el patrón arquitectónico
- Tests unitarios y de integración
- Validación de quality gates
- Documentación y reporte final

El skill es **framework-agnostic** y se adapta automáticamente según el perfil instalado:
- **PyQt/MVC:** Implementación de componentes UI con arquitectura MVC
- **FastAPI:** Implementación de endpoints REST con arquitectura en capas
- **Flask REST / Flask Webapp:** Implementación de APIs y webapps con Flask
- **Generic Python:** Implementación de módulos Python genéricos

---

## Uso

```bash
/implement-us US-001
/implement-us US-001 --producto {PRODUCT}
/implement-us US-001 --skip-bdd  # Salta generación BDD
```

**Parámetros:**
- `US-XXX`: Identificador de la Historia de Usuario (requerido)
- `--producto`: Nombre del producto/módulo (opcional, default: valor de `{PRODUCT}`)
- `--skip-bdd`: Saltar generación de escenarios BDD (opcional)

---

## Flujo de Ejecución

Este skill orquesta la implementación de una US a través de **9 fases secuenciales**, cada una delegada a un agente especializado:

### 🔍 Fase 0: Validación de Contexto
**Agente:** [`phases/phase-0-validation.md`](./phases/phase-0-validation.md)

**Objetivo:** Verificar que el proyecto tiene todo lo necesario para implementar la US.

**Acciones:**
- Buscar y extraer datos de la US
- Validar arquitectura de referencia
- Verificar estándares de calidad

**Aprobación:** Automática

---

### 📝 Fase 1: Generación de Escenarios BDD
**Agente:** [`phases/phase-1-bdd.md`](./phases/phase-1-bdd.md)

**Objetivo:** Generar escenarios BDD en formato Gherkin.

**Acciones:**
- Analizar criterios de aceptación
- Generar escenarios Given-When-Then
- Crear archivo `.feature`

**Aprobación:** Requerida (usuario revisa escenarios)

---

### 📋 Fase 2: Generación del Plan de Implementación
**Agente:** [`phases/phase-2-planning.md`](./phases/phase-2-planning.md)

**Objetivo:** Crear plan detallado basado en arquitectura configurada.

**Acciones:**
- Analizar US y arquitectura
- Definir estructura de componentes según `{ARCHITECTURE_PATTERN}`
- Estimar tiempos por tarea
- Generar checklist de implementación

**Aprobación:** Requerida (usuario revisa plan)

---

### 🔨 Fase 3: Implementación Guiada por Tareas
**Agente:** [`phases/phase-3-implementation.md`](./phases/phase-3-implementation.md)

**Objetivo:** Implementar la funcionalidad siguiendo el plan.

**Acciones:**
- Ejecutar tareas del plan secuencialmente
- Tracking de tiempo por tarea
- Checkpoints opcionales de aprobación

**Aprobación:** Por tarea (configurable)

---

### 🧪 Fase 4: Tests Unitarios
**Agente:** [`phases/phase-4-unit-tests.md`](./phases/phase-4-unit-tests.md)

**Objetivo:** Crear tests unitarios para cada componente.

**Acciones:**
- Generar tests según `{TEST_FRAMEWORK}`
- Configurar fixtures y mocks
- Ejecutar tests y validar cobertura

**Aprobación:** Automática (tests deben pasar)

---

### 🔗 Fase 5: Tests de Integración
**Agente:** [`phases/phase-5-integration-tests.md`](./phases/phase-5-integration-tests.md)

**Objetivo:** Crear tests de integración entre componentes.

**Acciones:**
- Generar tests de integración
- Validar interacción entre componentes
- Ejecutar suite completa

**Aprobación:** Automática (tests deben pasar)

---

### ✅ Fase 6: Validación BDD
**Agente:** [`phases/phase-6-bdd-validation.md`](./phases/phase-6-bdd-validation.md)

**Objetivo:** Implementar y ejecutar steps de los escenarios BDD.

**Acciones:**
- Crear step definitions
- Ejecutar escenarios BDD
- Validar que todos los escenarios pasan

**Aprobación:** Automática (escenarios deben pasar)

---

### 📊 Fase 7: Quality Gates
**Agente:** [`phases/phase-7-quality-gates.md`](./phases/phase-7-quality-gates.md)

**Objetivo:** Validar que el código cumple con estándares de calidad.

**Acciones:**
- Ejecutar pylint
- Validar complejidad ciclomática
- Verificar cobertura de tests
- Generar reporte de calidad

**Aprobación:** Automática (gates deben pasar)

---

### 📚 Fase 8: Documentación
**Agente:** [`phases/phase-8-documentation.md`](./phases/phase-8-documentation.md)

**Objetivo:** Generar documentación de la implementación.

**Acciones:**
- Actualizar documentación de arquitectura
- Generar docstrings si faltan
- Actualizar README o docs del proyecto

**Aprobación:** Requerida (usuario revisa docs)

---

### 📄 Fase 9: Reporte Final
**Agente:** [`phases/phase-9-final-report.md`](./phases/phase-9-final-report.md)

**Objetivo:** Generar reporte completo de la implementación.

**Acciones:**
- Consolidar métricas de todas las fases
- Generar reporte de implementación
- Calcular varianza de estimación vs tiempo real
- Exportar métricas para análisis histórico

**Aprobación:** Automática

---

## Control de Flujo

### Puntos de Aprobación

El skill tiene puntos de aprobación en:
- **Fase 1:** Escenarios BDD (usuario debe revisar)
- **Fase 2:** Plan de implementación (usuario debe revisar)
- **Fase 3:** Opcionalmente por tarea (configurable)
- **Fase 8:** Documentación (usuario debe revisar)

### Fases Opcionales

- `--skip-bdd`: Salta Fase 1 y Fase 6 (no recomendado)

### Manejo de Fallas

Si una fase falla, seguí este protocolo en orden:

1. **Identificar la causa concreta** — leer el output completo del error, no asumir
2. **Determinar en qué fase está el problema** — puede ser la fase actual u otra anterior
3. **Aplicar la corrección en la fase correspondiente** — no parchear síntomas
4. **Re-ejecutar la fase completa** — no solo el paso que falló
5. **Verificar el checklist de salida** antes de avanzar a la siguiente fase
6. **Si después de 2 intentos la fase sigue fallando** — informar al usuario y no continuar de forma autónoma

> Una fase con checklist de salida incompleto **no puede avanzar**. El agente no debe saltear fases ni marcar ítems como completos sin haberlos verificado.

**Protocolos específicos por fase** — ver sección "Si esta fase falla" en cada archivo de fase.

---

## Tracking de Tiempo

El skill usa el sistema de tracking integrado (`.claude/tracking/track.py`) para:
- Registrar tiempo real por fase y por tarea (Fase 3)
- Acumular datos empíricos de performance del agente a lo largo del tiempo
- Generar reportes históricos comparables entre ejecuciones del agente

> **Nota (PRIN-001):** Las estimaciones de duración definidas en los archivos de fase son referencias de complejidad relativa basadas en esfuerzo humano. No representan tiempos esperados de ejecución del agente. El tracking registra tiempos reales sin comparar contra estimaciones humanas.

**Comandos CLI:**

| Comando | Cuándo usarlo |
|---------|--------------|
| `python .claude/tracking/track.py start-phase N "Nombre"` | Al inicio de cada fase (N = 0..9) |
| `python .claude/tracking/track.py end-phase N` | Al cerrar cada fase |
| `python .claude/tracking/track.py start-task "nombre"` | Al iniciar cada tarea dentro de Fase 3 |
| `python .claude/tracking/track.py end-task "nombre"` | Al completar cada tarea dentro de Fase 3 |
| `python .claude/tracking/track.py end-tracking` | **Solo en Fase 9**, al finalizar la US completa |

> **`end-tracking` vs `end-phase`:** `end-phase` cierra únicamente la fase actual. `end-tracking` cierra el tracking completo de la US: calcula el tiempo total real acumulado, guarda el histórico en disco y genera el reporte de tiempo final. Solo debe invocarse una vez, al final de Fase 9, después de `end-phase 9`.

---

## Arquitectura Modular

Este skill sigue una **arquitectura de orquestador + agentes especializados**:

- **skill.md** (este archivo): Orquestador que coordina el flujo
- **phases/*.md**: Agentes especializados, uno por fase
- **customizations/*.json**: Configuraciones específicas por stack
- **config.json**: Configuración base compartida

**Beneficios:**
✅ **Modularidad:** Cada fase es independiente y modificable
✅ **Mantenibilidad:** Cambios en una fase no afectan otras
✅ **Testeable:** Cada fase se puede probar individualmente
✅ **Extensible:** Fácil agregar nuevas fases o modificar existentes

---

## Ejemplo de Validación de Concepto

### ❌ ANTES (Monolítico - PyQt/MVC específico):

```markdown
### Implementación
- app/presentacion/paneles/display/modelo.py
- app/presentacion/paneles/display/vista.py
- El modelo debe heredar de ModeloBase
```

### ✅ DESPUÉS (Modular - Framework Agnostic):

**Orquestador (skill.md):**
```markdown
### Fase 3: Implementación
Ver phases/phase-3-implementation.md para instrucciones detalladas
```

**Agente Especializado (phase-3-implementation.md):**
```markdown
# Estructura según {ARCHITECTURE_PATTERN}:

**MVC:** {COMPONENT_PATH}/modelo.py, vista.py, controlador.py
**Layered:** {COMPONENT_PATH}/schemas.py, service.py, router.py

El componente debe heredar de {BASE_CLASS}
```

---

## Documentos de Referencia del Skill

- **[`artifacts.md`](./artifacts.md):** Mapa centralizado de rutas y artefactos generados por el skill. Fuente de verdad para todas las rutas de archivos.
- **[`conventions.md`](./conventions.md):** Convención estructural de los archivos de fase — distingue secciones imperativas (`🔴 Acción Requerida`) de secciones de referencia (`📖 Referencia`).

---

**Versión:** 2.1.0 (Mejoras v1.1 — artifacts, conventions)
**Última actualización:** 2026-02-24
**Basado en:** `_work/from-simapp/skills/implement-us.md` (versión PyQt/MVC)
