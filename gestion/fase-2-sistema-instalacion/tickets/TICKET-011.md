# TICKET-011: Migrar sistema de tracking

**Fase:** 2 - Sistema de Instalación
**Sprint:** 1
**Estado:** DONE
**Prioridad:** Alta
**Estimación:** 1 hora
**Asignado a:** Claude Code

## Descripción

Migrar el sistema de tracking completo desde `_work/from-simapp/tracking/` al directorio `tracking/` del proyecto. Este sistema está 100% genérico y no requiere modificaciones, solo copia y verificación de funcionalidad.

El sistema de tracking proporciona funcionalidad de tracking de tiempo automático para fases y tareas, con comandos `/track-*`.

## Criterios de Aceptación

- [ ] Archivo `tracking/time_tracker.py` copiado y funcional
- [ ] Archivo `tracking/commands.py` copiado y funcional
- [ ] Archivo `tracking/__init__.py` copiado y funcional
- [ ] Imports de Python funcionando correctamente
- [ ] No hay errores de sintaxis o dependencias faltantes
- [ ] Archivos tienen la estructura y formato correctos

## Dependencias

- **Depende de:** TICKET-005 (estructura de directorios creada)
- **Bloquea a:** TICKET-013 (instalador necesita tracking para copiar)

## Notas Técnicas

### Archivos a Migrar

```
_work/from-simapp/tracking/
├── time_tracker.py    → tracking/time_tracker.py
├── commands.py        → tracking/commands.py
└── __init__.py        → tracking/__init__.py
```

### Verificación Post-Migración

```python
# Test de imports
python3 -c "from tracking import time_tracker, commands"

# Verificar que no hay errores de sintaxis
python3 -m py_compile tracking/time_tracker.py
python3 -m py_compile tracking/commands.py
python3 -m py_compile tracking/__init__.py
```

### Funcionalidad del Sistema

El sistema tracking proporciona:
- `TimeTracker`: Clase principal para tracking de tiempo
- Modelos: `Task`, `Phase`, `Pause`
- Comandos: `/track-pause`, `/track-resume`, `/track-status`, `/track-report`, `/track-history`
- Persistencia en archivos JSON
- Cálculo de varianza tiempo estimado vs. real

## Checklist de Implementación

- [ ] Copiar `time_tracker.py` a `tracking/`
- [ ] Copiar `commands.py` a `tracking/`
- [ ] Copiar `__init__.py` a `tracking/`
- [ ] Verificar imports funcionan
- [ ] Verificar sintaxis con py_compile
- [ ] Revisar que no hay referencias a rutas específicas de simapp
- [ ] Documentar en commit message

## Resultado

**Fecha de Completado:** 2026-02-09

### Archivos Migrados

```
tracking/
├── __init__.py (1.327 bytes)
├── commands.py (14.381 bytes)
└── time_tracker.py (17.652 bytes)
```

### Verificación

- ✅ Sintaxis Python correcta (py_compile)
- ✅ Imports funcionan correctamente
- ✅ No hay referencias específicas a simapp
- ✅ Commit: b570d68

**Estado:** ✅ Completado
