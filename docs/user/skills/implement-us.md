# Skill implement-us - Guía Completa

**Última Actualización:** 2026-02-15
**Audiencia:** Usuario Final
**Nivel:** Básico - Intermedio

---

## Introducción

El skill `implement-us` es el componente principal de Claude Dev Kit. Automatiza la implementación completa de historias de usuario a través de 10 fases estructuradas.

**Características:**
- ✅ 10 fases guiadas: Desde validación hasta reporte final
- ✅ Tracking automático de tiempo por fase
- ✅ Generación de BDD, tests y documentación
- ✅ Quality gates automáticos
- ✅ Personalizable por stack tecnológico

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

**Propósito:** Verificar prerequisitos antes de comenzar

**Validaciones:**
- ✅ Archivo US-XXX.md existe
- ✅ Proyecto Python válido
- ✅ Git inicializado
- ✅ Configuración válida

**Salida:** Confirmación de que todo está listo

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

**Output:** `docs/planning/US-001-plan.md`

**Contenido:**
- Desglose de componentes
- Tareas con estimaciones
- Orden de implementación
- Dependencias

---

### Fase 3: Implementación

**Propósito:** Generar código base de la funcionalidad

**Output:** Archivos en `src/`

**Proceso:**
1. Crear estructura de componentes
2. Implementar lógica core
3. Manejar casos edge

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

**Output:** `docs/reports/US-001-report.md`

**Contenido:**
- Tiempo total y por fase
- Métricas de calidad
- Archivos creados
- Resumen de tests

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

## Tracking Automático

El skill integra tracking de tiempo automáticamente:

- ⏱️ **Auto-start:** Se inicia al comenzar fase
- ⏸️ **Pausas:** Usa `/track-pause` si necesitas parar
- ▶️ **Resume:** Usa `/track-resume` para continuar
- 📊 **Reportes:** `/track-status` para ver progreso

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

- [Getting Started](../getting-started.md) - Tutorial inicial
- [Personalización](../customization.md) - Modificar comportamiento
- [Tracking](../tracking/user-guide.md) - Sistema de tracking

---

**Anterior:** [Configuración](../configuration.md)
**Siguiente:** [Creando Skills](../../developer/contributing/creating-skills.md)
**Índice:** [Volver al índice](../index.md)
