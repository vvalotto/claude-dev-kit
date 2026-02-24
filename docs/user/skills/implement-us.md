# Skill implement-us - Guía Completa

**Última Actualización:** 2026-02-24
**Versión:** v1.1
**Audiencia:** Usuario Final
**Nivel:** Básico - Intermedio

---

## Introducción

El skill `implement-us` es el componente principal de Claude Dev Kit. Automatiza la implementación completa de historias de usuario a través de 10 fases estructuradas.

**Características:**
- ✅ 10 fases guiadas: Desde validación hasta reporte final
- ✅ Tracking automático de tiempo por fase (directivas bash)
- ✅ Generación de BDD, tests y documentación
- ✅ Quality gates automáticos
- ✅ Personalizable por stack tecnológico
- ✅ Gates de entrada por fase (verificación de precondiciones)
- ✅ Checklists de salida verificables antes de avanzar
- ✅ Protocolo de recuperación ante fallas (límite de intentos autónomos)

---

## Uso Básico

```bash
# Implementar historia de usuario
/implement-us US-001

# Con opciones
/implement-us US-001 --skip-bdd --product mi_app
```

---

## Las 10 Fases

### Fase 0: Validación de Contexto

**Propósito:** Verificar prerequisitos y establecer el contexto de ejecución

**Validaciones:**
- ✅ Herramientas requeridas disponibles (pylint, radon, pytest, pytest-bdd) — fail-fast si alguna falta
- ✅ Archivo US-XXX.md existe
- ✅ Proyecto Python válido
- ✅ Git inicializado
- ✅ Configuración y perfil activo válidos

**Clasificación de HU:** El skill analiza el tipo de historia (nueva funcionalidad, refactorización, bug fix, etc.) y decide automáticamente si aplica BDD. Informa la decisión al usuario con justificación y permite override antes de continuar.

**Output:** `docs/plans/{US_ID}-context.md` — decisiones de ejecución, fases a ejecutar, rutas de artefactos y umbrales de calidad del perfil activo

---

### Fase 1: Generación de Escenarios BDD

**Propósito:** Crear escenarios Gherkin ejecutables

**Output:** `tests/features/US-001.feature`

**Ejemplo:**
```gherkin
Feature: Calculadora Simple

  Scenario: Sumar dos números positivos
    Given la calculadora está inicializada
    When sumo 5 y 3
    Then el resultado debe ser 8
```

---

### Fase 2: Plan de Implementación

**Propósito:** Desglosar US en tareas estimadas

**Output:** `docs/plans/{US_ID}-plan.md`

**Contenido:**
- Desglose de componentes
- Tareas con estimaciones de complejidad relativa
- Orden de implementación
- Dependencias

**Control de flujo:** Incluye un bloque STOP antes de avanzar a Fase 3 — el plan debe existir en disco y el usuario debe aprobar explícitamente antes de continuar.

---

### Fase 3: Implementación

**Propósito:** Generar código base de la funcionalidad

**Output:** Archivos en `src/`

**Proceso:**
1. Leer `docs/plans/{US_ID}-plan.md` desde disco (gate de entrada)
2. Verificar que cada tarea cubre al menos un criterio de aceptación de la HU
3. Crear estructura de componentes
4. Implementar lógica core
5. Manejar casos edge
6. Marcar checkboxes del plan al completar cada tarea

---

### Fase 4: Tests Unitarios

**Propósito:** Crear tests unitarios por componente

**Output:** `tests/test_*.py`

**Cobertura:**
- Happy path
- Casos edge
- Excepciones

---

### Fase 5: Tests de Integración

**Propósito:** Tests end-to-end del flujo completo

**Output:** `tests/integration/test_*.py`

**Validación:**
- Integración entre componentes
- Flujo completo de US
- Casos reales de uso

---

### Fase 6: Validación BDD

**Propósito:** Ejecutar escenarios Gherkin

**Comando:** `pytest tests/features/`

**Resultado esperado:** ✅ Todos los scenarios pasan

---

### Fase 7: Quality Gates

**Propósito:** Validar calidad del código

**Validaciones:**
- Pylint score ≥ threshold
- Coverage ≥ threshold
- Complexity ≤ max
- Maintainability ≥ min

---

### Fase 8: Documentación

**Propósito:** Agregar docstrings y comentarios

**Output:** Código documentado

**Incluye:**
- Docstrings de funciones/clases
- Comentarios de lógica compleja
- Type hints

---

### Fase 9: Reporte Final

**Propósito:** Generar resumen de implementación

**Output:** `docs/reports/{US_ID}-report.md`

**Contenido:**
- Tiempo total y por fase
- Métricas de calidad (leídas desde `quality/reports/{US_ID}-quality.json`)
- Archivos creados
- Resumen de tests

**Control de flujo:** El tracking no se cierra hasta que el reporte exista en disco. Se verifican los insumos al inicio (plan.md y quality.json).

---

## Opciones del Skill

```bash
# Saltar generación BDD
/implement-us US-001 --skip-bdd

# Especificar producto
/implement-us US-001 --producto mi_app

# Modo dry-run (sin ejecutar)
/implement-us US-001 --dry-run

# Verbose output
/implement-us US-001 --verbose
```

---

## Artefactos del Skill

Cada ejecución genera artefactos en rutas canónicas definidas en `skills/implement-us/artifacts.md`:

| Artefacto | Ruta | Generado en |
|-----------|------|-------------|
| Contexto de ejecución | `docs/plans/{US_ID}-context.md` | Fase 0 |
| Escenarios BDD | `docs/bdd/{US_ID}.feature` | Fase 1 |
| Plan de implementación | `docs/plans/{US_ID}-plan.md` | Fase 2 |
| Reporte de calidad | `quality/reports/{US_ID}-quality.json` | Fase 7 |
| Reporte final | `docs/reports/{US_ID}-report.md` | Fase 9 |

Cada fase verifica que los artefactos de las fases anteriores existen en disco antes de comenzar (gate de entrada).

---

## Protocolo de Recuperación ante Fallas

Si una fase falla, el skill sigue este protocolo:

1. Leer el output completo del error — no asumir la causa
2. Determinar en qué fase está el origen del problema
3. Aplicar la corrección en la fase correspondiente
4. Re-ejecutar la fase completa (no solo el paso que falló)
5. Verificar el checklist de salida antes de avanzar
6. Si después de 2 intentos la fase sigue fallando — informar al usuario

Cada fase de testing (4, 5, 6, 7) incluye un árbol de decisión específico sobre el origen del fallo.

---

## Tracking Automático

El skill integra tracking de tiempo automáticamente mediante comandos bash:

- ⏱️ **Auto-start:** Directiva bash al comenzar cada fase
- ⏸️ **Pausas:** Usa `/track-pause` si necesitas parar
- ▶️ **Resume:** Usa `/track-resume` para continuar
- 📊 **Reportes:** `/track-status` para ver progreso

El tracking acumula datos empíricos de performance del agente. No se compara con estimaciones humanas.

---

## Personalización por Perfil

Cada perfil personaliza el comportamiento:

### PyQt-MVC
- Componentes: Model, View, Controller
- Tests: pytest-qt con QTest
- Arquitectura: MVC con coordinadores

### FastAPI-REST
- Componentes: Router, Service, Repository
- Tests: pytest-asyncio
- Arquitectura: Layered con DI

### Flask
- Componentes: Blueprint, Service, Model
- Tests: pytest-flask
- Arquitectura: Blueprints

---

## Ejemplos Completos

### Ejemplo 1: Feature Simple

```bash
# US-002: Validador de email
/implement-us US-002
```

**Fases ejecutadas:**
1. ✅ Validación OK
2. ✅ BDD: Escenarios de emails válidos/inválidos
3. ✅ Plan: 1 función, 5 tests
4. ✅ Implementación: `src/utils/validators.py`
5. ✅ Tests: 100% coverage
6. ✅ Validación BDD: 5 scenarios ✅
7. ✅ Quality: Pylint 9.2, Coverage 100%
8. ✅ Docs: Docstrings agregados
9. ✅ Reporte: 45 min total

---

### Ejemplo 2: Feature Compleja

```bash
# US-015: Sistema de autenticación JWT
/implement-us US-015 --producto auth_service
```

**Resultado:**
- 8 componentes creados
- 25 tests unitarios
- 5 tests de integración
- Quality gates ✅
- 3.5 horas de implementación

---

## Troubleshooting

### Error: "US file not found"

**Solución:**
```bash
# Verificar que existe docs/user-stories/US-001.md
ls docs/user-stories/US-001.md

# Crear si falta
cat > docs/user-stories/US-001.md << 'EOF'
# US-001: Título
Descripción aquí
EOF
```

---

### Error: "Tests failing"

**Solución:**
1. Revisar código generado
2. Ajustar según requisitos específicos
3. El skill sugiere código base, tú ajustas
4. Re-ejecutar tests: `pytest tests/`

---

### Quality gates failing

**Solución:**
- Revisar output de Pylint
- Corregir issues
- O ajustar thresholds en config

---

## Recursos Adicionales

- [Getting Started](UserGettingStarted) - Tutorial inicial
- [Personalización](UserCustomization) - Modificar comportamiento
- [Tracking](UserTrackingUserGuide) - Sistema de tracking

---

**Anterior:** [Configuración](UserConfiguration)
**Siguiente:** [Creando Skills](DeveloperContributingCreatingSkills)
**Índice:** [Volver al índice](UserIndex)
