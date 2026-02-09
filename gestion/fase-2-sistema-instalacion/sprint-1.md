# Sprint 1 - Fase 2: Sistema de Instalación

**Fecha Inicio:** 2026-02-09
**Fecha Fin Estimada:** 2026-02-10
**Sprint:** 1 (Semana 1)
**Estado:** 🔄 En Progreso

---

## Objetivos de la Fase

Desarrollar el sistema de instalación completo que permita desplegar el Claude Dev Kit en proyectos de usuario, y migrar el sistema de tracking que está listo para usar.

---

## Tareas (Tickets)

### Completados ✅

- [x] **TICKET-011**: Migrar sistema de tracking de `_work/from-simapp/tracking/` a `tracking/`
- [x] **TICKET-012**: Crear `install/config.yaml` con configuración base

### En Progreso 🔄

Ninguno aún.

### Pendientes 📋
- [ ] **TICKET-012**: Crear `install/config.yaml` con configuración base
- [ ] **TICKET-013**: Desarrollar `install/installer.py` (instalador Python multiplataforma)
- [ ] **TICKET-014**: Crear `scripts/validate-setup.py` (validador post-instalación)
- [ ] **TICKET-015**: Crear `install/install.sh` (script para Unix/macOS)
- [ ] **TICKET-016**: Crear `install/install.ps1` (script para Windows PowerShell)
- [ ] **TICKET-017**: Crear `install/README.md` (documentación de instalación)
- [ ] **TICKET-018**: Testing del sistema de instalación

---

## Métricas

- **Total de Tickets:** 8
- **Completados:** 2 (25%)
- **En Progreso:** 0
- **Pendientes:** 6
- **Bloqueados:** 0

**Estimación Total:** 12 horas
**Tiempo Consumido:** 3 horas
**Tiempo Restante:** 9 horas

---

## Dependencias

**Depende de:**
- ✅ Fase 1: Setup Inicial (completada)

**Bloquea a:**
- Fase 3: Generalización de Skills (requiere instalador para testear)
- Fase 4: Templates (requiere instalador)
- Todas las fases posteriores

---

## Criterios de Aceptación de la Fase

- [ ] Sistema de tracking migrado y funcional en `tracking/`
- [ ] `install/config.yaml` creado con todos los perfiles
- [ ] `install/installer.py` completamente funcional
- [ ] `scripts/validate-setup.py` validando correctamente instalaciones
- [ ] Scripts de instalación `.sh` y `.ps1` funcionando
- [ ] `install/README.md` completo y claro
- [ ] Testing completo en al menos un sistema operativo
- [ ] Instalación exitosa genera estructura `.claude/` correcta en proyecto destino

---

## Notas Técnicas

### Estructura de Instalación Target

```
proyecto-usuario/
├── .claude/
│   ├── skills/implement-us/
│   ├── templates/{bdd,planning,testing,reporting}/
│   ├── tracking/
│   └── config.json
└── CLAUDE.md (si no existe)
```

### Perfiles a Soportar

1. **pyqt-mvc**: PyQt6 + MVC + Factory/Coordinator patterns
2. **fastapi-rest**: FastAPI + REST APIs + Layered architecture
3. **django-mvt**: Django + MVT pattern + Django conventions
4. **generic-python**: Generic Python projects (fallback)

---

## Riesgos Identificados

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Installer sobrescribe archivos existentes | Media | Alto | Implementar --force flag y confirmaciones |
| Config.yaml mal estructurado | Media | Alto | Validación con schema YAML |
| Paths diferentes en Windows | Media | Medio | Usar pathlib para cross-platform paths |
| Python no disponible en PATH | Baja | Alto | Scripts .sh/.ps1 verifican Python primero |

---

## Checklist Pre-Commit

Antes de hacer commit de esta fase:
- [ ] Todos los archivos del sistema de instalación creados
- [ ] installer.py testeado manualmente
- [ ] validate-setup.py funciona correctamente
- [ ] README.md de instalación claro y completo
- [ ] Tracking migrado sin errores de import
- [ ] Al menos un test end-to-end exitoso
- [ ] Actualizar CHANGELOG.md
- [ ] Actualizar TODO.md

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

**Fase 3: Generalización de Skills** - Ver `gestion/fase-3-generalizacion-skills/sprint-2.md`

---

**Última Actualización:** 2026-02-09 (TICKET-012 completado - 25% progreso)
