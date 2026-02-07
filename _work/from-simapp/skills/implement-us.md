# Skill: implement-us

**Nombre del comando:** `/implement-us`

**Descripción:** Implementador asistido de Historias de Usuario siguiendo arquitectura MVC + Factory/Coordinator

---

## Propósito

Este skill guía paso a paso la implementación de una Historia de Usuario (US) del proyecto ISSE_Simuladores, asegurando:
- Adherencia a la arquitectura de referencia (ADR-003)
- Generación de escenarios BDD
- Implementación MVC completa
- Tests unitarios y de integración
- Validación de quality gates

---

## Uso

```bash
/implement-us US-001
/implement-us US-001 --producto ux_termostato
/implement-us US-001 --skip-bdd  # Salta generación BDD
```

---

## Proceso del Skill

### Fase 0: Validación de Contexto

**TRACKING:** Al inicio de la fase:
```python
from .tracking.time_tracker import TimeTracker

# Inicializar tracker
tracker = TimeTracker(us_id, us_title, us_points, producto)
tracker.start_tracking()
tracker.start_phase(0, "Validación de Contexto")
```

1. **Verificar que existe la historia de usuario**
   - Buscar en `{producto}/docs/HISTORIAS-USUARIO-*.md`
   - Extraer: título, criterios de aceptación, puntos, prioridad

2. **Validar arquitectura de referencia**
   - Confirmar que existe ADR-003 o arquitectura.md
   - Verificar patrones: MVC, Factory, Coordinator

3. **Verificar estándares de calidad**
   - Confirmar CLAUDE.md con quality gates
   - Confirmar estructura de tests (conftest.py)

**Output Fase 0:** Resumen de contexto validado

**TRACKING:** Al finalizar la fase:
```python
tracker.end_phase(0, auto_approved=True)
```

---

### Fase 1: Generación de Escenarios BDD

**TRACKING:** Al inicio de la fase:
```python
tracker.start_phase(1, "Generación de Escenarios BDD")
```

**Acción:** Analizar la US y generar escenarios BDD en formato Gherkin

**Template:** `.claude/templates/bdd-scenario.feature`

**Pasos:**
1. Leer criterios de aceptación de la US
2. Por cada criterio, generar un escenario BDD:
   - Given (contexto/precondición)
   - When (acción del usuario)
   - Then (resultado esperado)
3. Generar archivo: `{producto}/tests/features/US-XXX-{nombre}.feature`

**Ejemplo Output:**
```gherkin
Feature: Ver temperatura ambiente actual (US-001)

  Scenario: Display muestra temperatura cuando hay conexión
    Given el termostato está encendido
    And hay conexión con el Raspberry Pi
    When se recibe temperatura de 22.5°C
    Then el display muestra "22.5"
    And el label muestra "Temperatura Ambiente"
```

**Punto de aprobación:** Usuario revisa y aprueba escenarios BDD

**TRACKING:** Al finalizar la fase:
```python
tracker.end_phase(1, auto_approved=False)  # Requiere aprobación del usuario
```

---

### Fase 2: Generación del Plan de Implementación

**TRACKING:** Al inicio de la fase:
```python
tracker.start_phase(2, "Generación del Plan de Implementación")
```

**Acción:** Crear plan detallado basado en arquitectura MVC

**Template:** `.claude/templates/implementation-plan.md`

**Pasos:**
1. Identificar componentes a crear según arquitectura:
   - Si es panel UI → Modelo + Vista + Controlador
   - Si es comunicación → Cliente o Servidor
   - Si es dominio → Dataclass + lógica
2. Identificar dependencias (Factory, Coordinator)
3. Generar checklist de tareas
4. Estimar tiempo por tarea

**Ejemplo Output:**
```markdown
# Plan de Implementación: US-001 - Ver temperatura ambiente

## Componentes a Implementar

### 1. Panel Display (MVC)
- [ ] app/presentacion/paneles/display/modelo.py (10 min)
- [ ] app/presentacion/paneles/display/vista.py (20 min)
- [ ] app/presentacion/paneles/display/controlador.py (15 min)

### 2. Integración con Comunicación
- [ ] Conectar ServidorEstado → DisplayControlador (10 min)

### 3. Tests
- [ ] tests/test_display_modelo.py (15 min)
- [ ] tests/test_display_vista.py (20 min)
- [ ] tests/test_display_controlador.py (20 min)
- [ ] tests/test_display_integracion.py (15 min)

### 4. Validación
- [ ] Ejecutar escenarios BDD (5 min)
- [ ] Quality gates (Pylint, CC, MI) (5 min)

**Total estimado:** 2h 15min
**Estado:** 0/12 tareas completadas
```

**Archivo generado:** `{producto}/docs/plans/US-XXX-plan.md`

**Punto de aprobación:** Usuario revisa y aprueba el plan

**TRACKING:** Al finalizar la fase:
```python
tracker.end_phase(2, auto_approved=False)  # Requiere aprobación del usuario
```

---

### Fase 3: Implementación Guiada por Tareas

**TRACKING:** Al inicio de la fase:
```python
tracker.start_phase(3, "Implementación Guiada por Tareas")
```

**Acción:** Por cada tarea del plan, guiar la implementación

**Pasos:**
1. **Seleccionar próxima tarea** del plan (primera no completada)

2. **TRACKING: Iniciar tarea**
   ```python
   tracker.start_task(
       task_id=f"task_{task_number:03d}",
       task_name="Implementar DisplayModelo",  # Nombre de la tarea
       task_type="modelo",  # modelo, vista, controlador, test
       estimated_minutes=10.0  # Del plan
   )
   ```

3. **Mostrar contexto:**
   - Qué se va a implementar
   - Patrón arquitectónico a seguir
   - Ejemplo de código similar existente

4. **Generar código base** usando templates

5. **Presentar código** para revisión del usuario

6. **Escribir archivo** si usuario aprueba

7. **Ejecutar tests** de la tarea si corresponde

8. **TRACKING: Finalizar tarea**
   ```python
   tracker.end_task(
       task_id=f"task_{task_number:03d}",
       file_created="app/presentacion/paneles/display/modelo.py"
   )
   ```

9. **Actualizar plan INMEDIATAMENTE** después de completar la tarea:
   - Marcar checkbox `- [x]` de la tarea completada en el plan
   - Actualizar contador "Tareas completadas: X/Y"
   - Actualizar porcentaje de progreso

10. **Continuar** con siguiente tarea

**IMPORTANTE:** El plan debe actualizarse **después de cada tarea completada**, no al final de todas las tareas. Esto da visibilidad en tiempo real del progreso.

**Ejemplo de Guía para Tarea:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 TAREA 1/12: Implementar DisplayModelo
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 Ubicación: app/presentacion/paneles/display/modelo.py

📐 Patrón: Modelo MVC (dataclass inmutable)

💡 Referencia: Revisar PanelEstadoModelo en simulador_bateria

✏️  Código propuesto:
───────────────────────────────────────────
[Código generado aquí]
───────────────────────────────────────────

❓ ¿Aprobar e implementar? (yes/no/edit)
```

**Punto de aprobación:** Usuario aprueba cada tarea antes de continuar

**TRACKING:** Al finalizar la fase:
```python
tracker.end_phase(3, auto_approved=True)  # Las tareas ya fueron aprobadas individualmente
```

---

### Fase 4: Tests Unitarios

**TRACKING:** Al inicio de la fase:
```python
tracker.start_phase(4, "Tests Unitarios")
```

**Acción:** Por cada componente, implementar tests

**Template:** `.claude/templates/test-unit.py`

**Pasos:**
1. Identificar qué testear según tipo de componente:
   - Modelo: validación de datos, inmutabilidad
   - Vista: renderizado, actualización
   - Controlador: señales, lógica de negocio
2. Generar tests usando fixtures de conftest.py
3. Ejecutar tests: `pytest tests/test_XXX.py -v`
4. Validar coverage: `pytest --cov=app/presentacion/paneles/display --cov-report=term`

**Ejemplo Output:**
```python
# tests/test_display_modelo.py
import pytest
from app.presentacion.paneles.display.modelo import DisplayModelo

class TestCreacion:
    """Tests de creación del modelo."""

    def test_crear_con_valores_default(self):
        modelo = DisplayModelo()
        assert modelo.temperatura == 0.0
        assert modelo.encendido is True

    def test_es_inmutable(self):
        modelo = DisplayModelo(temperatura=22.5)
        with pytest.raises(AttributeError):
            modelo.temperatura = 23.0
```

**Objetivo:** Coverage > 95% del nuevo código

**TRACKING:** Al finalizar la fase:
```python
tracker.end_phase(4, auto_approved=True)
```

---

### Fase 5: Tests de Integración

**TRACKING:** Al inicio de la fase:
```python
tracker.start_phase(5, "Tests de Integración")
```

**Acción:** Validar que componentes funcionan juntos

**Pasos:**
1. Crear test que simula flujo completo:
   - ServidorEstado recibe JSON
   - JSON se parsea a EstadoTermostato
   - Señal se emite a DisplayControlador
   - DisplayControlador actualiza modelo
   - Vista se renderiza
2. Usar mocks de PyQt (pytest-qt)
3. Ejecutar: `pytest tests/test_display_integracion.py -v`

**Ejemplo Output:**
```python
def test_display_actualiza_desde_servidor(qapp, qtbot):
    """Test end-to-end: servidor → controlador → vista."""
    # Setup
    servidor = ServidorEstado(puerto=14001)
    controlador = crear_display_controlador()

    # Conectar
    servidor.estado_recibido.connect(
        controlador.actualizar_desde_estado
    )

    # Simular recepción de JSON
    json_data = '{"temp_actual": 22.5, ...}'
    servidor._on_data_received(json_data)

    # Validar
    assert controlador.modelo.temperatura == 22.5
    assert "22.5" in controlador.vista.label_temp.text()
```

**TRACKING:** Al finalizar la fase:
```python
tracker.end_phase(5, auto_approved=True)
```

---

### Fase 6: Validación BDD

**TRACKING:** Al inicio de la fase:
```python
tracker.start_phase(6, "Validación BDD")
```

**Acción:** Ejecutar escenarios BDD generados en Fase 1

**Pasos:**
1. Configurar pytest-bdd si no existe
2. Implementar steps de los escenarios:
   - Given steps (setup de contexto)
   - When steps (acciones)
   - Then steps (aserciones)
3. Ejecutar: `pytest tests/features/US-XXX-*.feature -v`
4. Validar que TODOS los escenarios pasan

**Ejemplo Output:**
```
tests/features/US-001-ver-temperatura.feature::Display muestra temperatura PASSED
tests/features/US-001-ver-temperatura.feature::Display sin conexión PASSED
tests/features/US-001-ver-temperatura.feature::Actualización tiempo real PASSED

3 scenarios passed, 0 failed
```

**TRACKING:** Al finalizar la fase:
```python
tracker.end_phase(6, auto_approved=True)
```

---

### Fase 7: Quality Gates

**TRACKING:** Al inicio de la fase:
```python
tracker.start_phase(7, "Quality Gates")
```

**Acción:** Validar métricas de calidad del código

**Pasos:**
1. **Ejecutar Pylint:**
   ```bash
   cd {producto}
   pylint app/presentacion/paneles/display/
   ```
   - **Target:** ≥ 8.0

2. **Calcular Métricas:**
   ```bash
   python quality/scripts/calculate_metrics.py app/presentacion/paneles/display
   ```
   - **CC promedio:** ≤ 10
   - **MI promedio:** > 20

3. **Validar Coverage:**
   ```bash
   pytest tests/test_display_* --cov=app/presentacion/paneles/display --cov-report=term --cov-report=json
   ```
   - **Target:** ≥ 95%
   - **Nota:** Se genera reporte en terminal y JSON (no HTML)

4. **Generar Reporte:**
   - Archivo: `{producto}/quality/reports/US-XXX-quality.json`

**Ejemplo Output:**
```json
{
  "us_id": "US-001",
  "fecha": "2026-01-16T15:30:00",
  "metricas": {
    "pylint": 9.2,
    "cc_promedio": 2.1,
    "mi_promedio": 78.5,
    "coverage": 97.3
  },
  "estado": "APROBADO",
  "observaciones": []
}
```

**Criterio de éxito:** Todas las métricas superan los umbrales

**TRACKING:** Al finalizar la fase:
```python
tracker.end_phase(7, auto_approved=True)
```

---

### Fase 8: Actualización de Documentación

**TRACKING:** Al inicio de la fase:
```python
tracker.start_phase(8, "Actualización de Documentación")
```

**Acción:** Actualizar documentos relevantes

**Pasos:**
1. **Actualizar plan de implementación:**
   - Marcar US como "Completada"
   - Agregar tiempo real vs estimado
   - Notas de lecciones aprendidas

2. **Actualizar arquitectura (si aplica):**
   - Si se agregó panel nuevo, documentar en arquitectura.md
   - Actualizar diagramas si corresponde

3. **Actualizar CHANGELOG.md:**
   - Agregar entrada con US implementada
   - Formato: `[US-001] Ver temperatura ambiente - Display LCD implementado`

4. **Actualizar README (si aplica):**
   - Si se agregó funcionalidad visible, actualizar screenshots/descripción

**TRACKING:** Al finalizar la fase:
```python
tracker.end_phase(8, auto_approved=True)
```

---

### Fase 9: Reporte Final

**TRACKING:** Al inicio de la fase:
```python
tracker.start_phase(9, "Reporte Final")
```

**Acción:** Generar reporte de implementación

**Template:** `.claude/templates/implementation-report.md`

**Contenido:**
```markdown
# Reporte de Implementación: US-001

## Resumen
- **Historia:** US-001 - Ver temperatura ambiente
- **Puntos estimados:** 3
- **Tiempo real:** 2h 10min
- **Estado:** ✅ COMPLETADO

## Componentes Implementados
- ✅ DisplayModelo (modelo.py)
- ✅ DisplayVista (vista.py)
- ✅ DisplayControlador (controlador.py)
- ✅ Tests unitarios (12 tests)
- ✅ Tests integración (3 tests)
- ✅ Escenarios BDD (3 escenarios)

## Métricas de Calidad
- Pylint: 9.2/10 ✅
- CC: 2.1 (target ≤10) ✅
- MI: 78.5 (target >20) ✅
- Coverage: 97.3% (target ≥95%) ✅

## Archivos Creados
- app/presentacion/paneles/display/modelo.py
- app/presentacion/paneles/display/vista.py
- app/presentacion/paneles/display/controlador.py
- tests/test_display_modelo.py
- tests/test_display_vista.py
- tests/test_display_controlador.py
- tests/test_display_integracion.py
- tests/features/US-001-ver-temperatura.feature
- docs/plans/US-001-plan.md
- quality/reports/US-001-quality.json

## Criterios de Aceptación
- [x] Display muestra temperatura con formato X.X °C
- [x] Temperatura se actualiza automáticamente
- [x] Fuente grande y clara (48px+)
- [x] Fondo LCD verde oscuro
- [x] Label indica "Temperatura Ambiente"
- [x] Muestra "---" sin conexión

## Próximos Pasos
- [ ] Implementar US-002 (Estado climatizador)
- [ ] Integrar DisplayControlador en Factory
- [ ] Conectar en Coordinator con ServidorEstado
```

**Archivo:** `{producto}/docs/reports/US-XXX-report.md`

**TRACKING:** Al finalizar la fase y el tracking completo:
```python
tracker.end_phase(9, auto_approved=True)
tracker.end_tracking()  # Finaliza tracking y genera reportes de tiempo
```

---

## Configuración del Skill

### Variables de Entorno (opcionales)

```bash
# .env o .claude/config
IMPLEMENTADOR_AUTO_COMMIT=false  # Git commit automático por fase
IMPLEMENTADOR_AUTO_TEST=true     # Ejecutar tests automáticamente
IMPLEMENTADOR_VERBOSE=true       # Logs detallados
```

### Archivos de Configuración

**`.claude/skills/implement-us-config.json`**
```json
{
  "templates_dir": ".claude/templates",
  "plans_dir": "docs/plans",
  "reports_dir": "docs/reports",
  "quality_gates": {
    "pylint_min": 8.0,
    "cc_max": 10,
    "mi_min": 20,
    "coverage_min": 95
  },
  "checkpoint_approval": true,
  "auto_run_tests": true,
  "generate_bdd": true
}
```

---

## Dependencias

- Python 3.12+
- pytest
- pytest-qt
- pytest-bdd (opcional, para BDD)
- pytest-cov
- pylint
- radon

---

## Estructura de Archivos Generados

```
{producto}/
├── tests/
│   ├── features/               # Escenarios BDD
│   │   └── US-XXX-*.feature
│   ├── test_XXX_modelo.py      # Tests unitarios
│   ├── test_XXX_vista.py
│   ├── test_XXX_controlador.py
│   └── test_XXX_integracion.py
├── docs/
│   ├── plans/
│   │   └── US-XXX-plan.md      # Plan de implementación
│   └── reports/
│       └── US-XXX-report.md    # Reporte final
└── quality/reports/
    └── US-XXX-quality.json     # Métricas de calidad
```

---

## Ejemplo de Uso Completo

```
User: /implement-us US-001

Claude:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀 Implementador de Historia de Usuario
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Historia: US-001 - Ver temperatura ambiente
📦 Producto: ux_termostato
⭐ Prioridad: Alta
🎯 Puntos: 3

━━━ Fase 0: Validación de Contexto ━━━

✅ Historia encontrada en ux_termostato/docs/historias/catalogo_historias.md
✅ Arquitectura de referencia: ADR-003
✅ Estándares: CLAUDE.md
✅ Tests configurados: conftest.py

━━━ Fase 1: Generación de Escenarios BDD ━━━

Generando escenarios basados en criterios de aceptación...

[Muestra escenarios generados]

¿Aprobar escenarios BDD? (yes/no/edit)

User: yes

Claude:
✅ Escenarios guardados en tests/features/US-001-ver-temperatura.feature

━━━ Fase 2: Plan de Implementación ━━━

[Muestra plan detallado]

¿Aprobar plan? (yes/no/edit)

User: yes

━━━ Fase 3: Implementación Tarea 1/12 ━━━

📋 Implementar DisplayModelo

[Muestra código propuesto]

¿Implementar? (yes/no/edit)

User: yes

✅ Archivo creado: app/presentacion/paneles/display/modelo.py
⏭️  Siguiente tarea: Implementar DisplayVista...
```

---

## Notas de Implementación

### Puntos de Extensión

El skill puede extenderse para:
- Integración con Jira (actualizar estado de US)
- Git automation (crear branch, commits por tarea)
- Notificaciones (Slack, email al completar)
- Dashboard web de progreso
- Análisis de velocity (puntos/día)

### Limitaciones

- No reemplaza revisión de código humana
- Patrones arquitectónicos deben estar bien definidos
- Requiere historias de usuario bien escritas
- Tests BDD requieren pytest-bdd configurado

---

## Mantenimiento

### Actualizar Templates

Los templates están en `.claude/templates/` y pueden editarse:
- `bdd-scenario.feature` - Template de escenarios Gherkin
- `implementation-plan.md` - Template de plan
- `test-unit.py` - Template de test unitario
- `implementation-report.md` - Template de reporte

### Logs

El skill genera logs en `.claude/logs/implement-us-{timestamp}.log`

---

## Versión

**Versión:** 1.0
**Fecha:** 2026-01-16
**Autor:** Victor Valotto
**Proyecto:** ISSE_Simuladores
