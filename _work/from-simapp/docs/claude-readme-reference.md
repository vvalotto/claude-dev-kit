# Claude Code Skills - ISSE_Simuladores

Este directorio contiene skills personalizados de Claude Code para el proyecto ISSE_Simuladores.

## Skills Disponibles

### `/implement-us` - Implementador de Historias de Usuario

Skill que guía paso a paso la implementación de Historias de Usuario siguiendo la arquitectura MVC + Factory/Coordinator del proyecto.

**Documentación completa:** `skills/implement-us.md`

#### Uso Rápido

```bash
# En Claude Code
/implement-us US-001
```

El skill ejecutará estas fases de forma asistida:
1. ✅ Validación de contexto (historia, arquitectura, estándares)
2. 📝 Generación de escenarios BDD
3. 📋 Generación de plan de implementación
4. 💻 Implementación guiada tarea por tarea
5. 🧪 Tests unitarios
6. 🔗 Tests de integración
7. ✔️  Validación BDD
8. 📊 Quality gates (Pylint, CC, MI, Coverage)
9. 📄 Reporte final

---

## Estructura de Archivos

```
.claude/
├── README.md                       # Este archivo
├── skills/
│   ├── implement-us.md             # Definición del skill
│   └── implement-us-config.json    # Configuración
├── templates/
│   ├── bdd-scenario.feature        # Template escenarios BDD
│   ├── implementation-plan.md      # Template plan implementación
│   ├── test-unit.py                # Template tests unitarios
│   └── implementation-report.md    # Template reporte final
└── logs/
    └── implement-us-*.log          # Logs de ejecución
```

---

## Configuración

### Archivo de Configuración

Editar `.claude/skills/implement-us-config.json` para personalizar:

```json
{
  "quality_gates": {
    "pylint_min": 8.0,      // Mínimo score Pylint
    "cc_max": 10,           // Máxima complejidad ciclomática
    "mi_min": 20,           // Mínimo índice mantenibilidad
    "coverage_min": 95.0    // Mínimo coverage
  },
  "workflow": {
    "checkpoint_approval": true,  // Requiere aprobación por fase
    "auto_run_tests": true,       // Ejecuta tests automáticamente
    "generate_bdd": true          // Genera escenarios BDD
  }
}
```

### Variables de Entorno

Crear `.claude/.env` (opcional):

```bash
IMPLEMENTADOR_VERBOSE=true      # Logs detallados
IMPLEMENTADOR_DRY_RUN=false     # Modo simulación
```

---

## Dependencias del Skill

El skill requiere que el proyecto tenga:

### Documentación Base
- ✅ Historias de Usuario en `{producto}/docs/HISTORIAS-USUARIO-*.md`
- ✅ Arquitectura de referencia (ADR-003 o arquitectura.md)
- ✅ Estándares en `CLAUDE.md`

### Herramientas Python
- pytest (tests unitarios)
- pytest-qt (tests de UI PyQt)
- pytest-cov (coverage)
- pytest-bdd (escenarios BDD - opcional)
- pylint (linting)
- radon (métricas CC/MI)

### Estructura de Testing
- `conftest.py` con fixtures reutilizables
- Patrón de tests: `test_{component}_{aspect}.py`

---

## Ejemplos de Uso

### Ejemplo 1: Implementación Básica

```
User: /implement-us US-001

Claude:
🚀 Implementador de Historia de Usuario

📋 Historia: US-001 - Ver temperatura ambiente
⭐ Prioridad: Alta | 🎯 Puntos: 3

━━━ Validación de Contexto ━━━
✅ Historia encontrada
✅ Arquitectura validada
✅ Estándares confirmados

━━━ Generando Escenarios BDD ━━━
[Muestra 3 escenarios]

¿Aprobar? (yes/no)

User: yes

━━━ Generando Plan ━━━
📦 12 tareas identificadas
⏱️  Estimación: 2h 15min

[Muestra plan detallado]

¿Aprobar? (yes/no)

User: yes

━━━ Tarea 1/12: DisplayModelo ━━━
[Muestra código propuesto]

¿Implementar? (yes/no)
```

### Ejemplo 2: Saltar BDD

```
User: /implement-us US-002 --skip-bdd

Claude:
Saltando generación de BDD...
Generando plan directamente...
```

### Ejemplo 3: Solo Generar Plan

```
User: /implement-us US-003 --plan-only

Claude:
Generando solo el plan de implementación...
Plan guardado en: docs/plans/US-003-plan.md
```

---

## Flujo Completo de Trabajo

### 1. Preparación
```bash
# Asegurar que el producto tiene historias de usuario
ls ux_termostato/docs/HISTORIAS-USUARIO-*.md

# Revisar configuración del skill
cat .claude/skills/implement-us-config.json
```

### 2. Invocación
```
En Claude Code: /implement-us US-001
```

### 3. Revisión de Outputs

**Archivos generados:**
```
ux_termostato/
├── tests/features/
│   └── US-001-ver-temperatura.feature    # Escenarios BDD
├── docs/plans/
│   └── US-001-plan.md                    # Plan detallado
├── docs/reports/
│   └── US-001-report.md                  # Reporte final
├── app/presentacion/paneles/display/
│   ├── modelo.py                         # Código implementado
│   ├── vista.py
│   └── controlador.py
├── tests/
│   ├── test_display_modelo.py            # Tests unitarios
│   ├── test_display_vista.py
│   ├── test_display_controlador.py
│   └── test_display_integracion.py
└── quality/reports/
    └── US-001-quality.json               # Métricas
```

### 4. Validación Manual

```bash
# Ejecutar tests
cd ux_termostato
pytest tests/test_display_* -v

# Verificar quality gates
pylint app/presentacion/paneles/display/
pytest --cov=app/presentacion/paneles/display --cov-report=html

# Revisar reporte
cat docs/reports/US-001-report.md
```

### 5. Integración

El skill genera el código pero NO integra automáticamente en Factory/Coordinator.
Debes:

1. Agregar método en Factory:
```python
def _crear_ctrl_display(self):
    # Código generado por el skill
```

2. Llamar en Coordinator:
```python
self._ctrl['display'] = factory._crear_ctrl_display()
```

3. Agregar en Compositor:
```python
layout.addWidget(self._ctrl['display'].vista)
```

---

## Personalización de Templates

### Modificar Template BDD

Editar `.claude/templates/bdd-scenario.feature`:

```gherkin
# Agregar tu estructura preferida
Feature: {FEATURE_TITLE}
  # Tu formato personalizado
```

### Modificar Template de Tests

Editar `.claude/templates/test-unit.py`:

```python
# Agregar fixtures personalizadas
# Cambiar estructura de clases
# Agregar helpers específicos
```

---

## Troubleshooting

### Problema: "Historia no encontrada"

**Solución:** Verificar que existe el archivo de historias:
```bash
ls {producto}/docs/HISTORIAS-USUARIO-*.md
```

### Problema: "Arquitectura no validada"

**Solución:** Confirmar que existe ADR-003 o arquitectura.md en docs/

### Problema: "Tests fallan"

**Solución:**
1. Verificar que pytest está instalado
2. Confirmar que fixtures están en conftest.py
3. Revisar imports de los módulos

### Problema: "Quality gates no pasan"

**Solución:**
1. Ejecutar pylint manualmente para ver errores
2. Ajustar umbrales en config si es necesario
3. Refactorizar código para cumplir estándares

---

## Extensiones Futuras

El skill puede extenderse para:

- [ ] Integración con Jira (actualizar estado automáticamente)
- [ ] Git automation (branches, commits por tarea)
- [ ] Notificaciones (Slack, email)
- [ ] Dashboard web de progreso
- [ ] AI code review automático
- [ ] Análisis de velocity del equipo

---

## Contribuir

Para mejorar el skill:

1. Editar `skills/implement-us.md` (definición)
2. Actualizar `templates/` (templates)
3. Modificar `implement-us-config.json` (configuración)
4. Probar con una historia de usuario real
5. Documentar cambios en este README

---

## Soporte

**Documentación completa:** `.claude/skills/implement-us.md`
**Configuración:** `.claude/skills/implement-us-config.json`
**Templates:** `.claude/templates/`
**Logs:** `.claude/logs/`

---

## Versión

**Versión:** 1.0
**Fecha:** 2026-01-16
**Autor:** Victor Valotto
**Proyecto:** ISSE_Simuladores
