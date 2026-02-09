# TICKET-020: Crear estructura de directorios skills/implement-us/

**Fase:** 3 - Generalización de Skills
**Sprint:** 2
**Estado:** TODO
**Prioridad:** Alta
**Estimación:** 0.5 horas
**Asignado a:** Claude Code

## Descripción

Crear la estructura completa de directorios para el skill `implement-us` generalizado siguiendo la arquitectura planificada en PROJECT_PLAN.md.

Esta estructura será la base para organizar el skill generalizado, sus configuraciones, y la documentación de cada fase.

## Criterios de Aceptación

- [ ] Directorio `skills/implement-us/` creado
- [ ] Subdirectorio `skills/implement-us/phases/` creado (para documentación de fases)
- [ ] Subdirectorio `skills/implement-us/customizations/` creado (para perfiles)
- [ ] Archivo `.gitkeep` en directorios vacíos (temporal)
- [ ] Estructura verificada con `tree` o `ls`
- [ ] README.md creado en `skills/implement-us/` explicando la estructura

## Dependencias

- **Depende de:** TICKET-019 (análisis completado)
- **Bloquea a:** TICKET-021, TICKET-022, TICKET-023, TICKET-024, TICKET-025, TICKET-026

## Notas Técnicas

### Estructura a Crear

```
skills/
└── implement-us/
    ├── README.md                    # Documentación del skill
    ├── skill.md                     # Skill generalizado (TICKET-021)
    ├── config.json                  # Config base (TICKET-022)
    ├── phases/                      # Documentación detallada de fases
    │   ├── phase-0-validacion.md
    │   ├── phase-1-bdd.md
    │   ├── phase-2-planning.md
    │   ├── phase-3-implementacion.md
    │   ├── phase-4-tests-unitarios.md
    │   ├── phase-5-tests-integracion.md
    │   ├── phase-6-validacion-bdd.md
    │   ├── phase-7-quality-gates.md
    │   ├── phase-8-documentacion.md
    │   └── phase-9-reporte.md
    └── customizations/              # Perfiles específicos por stack
        ├── pyqt-mvc.json            # TICKET-023
        ├── fastapi-rest.json        # TICKET-024
        ├── django-mvt.json          # TICKET-025
        └── generic-python.json      # TICKET-026
```

### Contenido del README.md

```markdown
# Skill: implement-us

Implementador asistido de Historias de Usuario con soporte para múltiples stacks tecnológicos.

## Archivos

- `skill.md` - Definición completa del skill (leída por Claude Code)
- `config.json` - Configuración base genérica
- `phases/` - Documentación detallada de cada una de las 9 fases
- `customizations/` - Perfiles específicos por stack tecnológico

## Perfiles Disponibles

- **pyqt-mvc**: PyQt6 + arquitectura MVC + Factory/Coordinator
- **fastapi-rest**: FastAPI + APIs REST + arquitectura en capas
- **django-mvt**: Django + patrón MVT + convenciones Django
- **generic-python**: Proyectos Python genéricos

## Uso

El instalador (`install/installer.py`) fusiona `config.json` base con el perfil seleccionado
y despliega el skill en `.claude/skills/implement-us/` del proyecto destino.

## Variables Disponibles

Las siguientes variables están disponibles para personalización en los perfiles:

- `{ARCHITECTURE_PATTERN}` - Patrón arquitectónico (mvc, mvt, layered, etc.)
- `{COMPONENT_TYPE}` - Tipo de componente (Panel, View, Service, etc.)
- `{COMPONENT_PATH}` - Ruta base de componentes
- `{TEST_FRAMEWORK}` - Framework de testing (pytest, unittest, etc.)
- `{BASE_CLASS}` - Clase base de modelos/vistas

Ver `config.json` para lista completa y valores por defecto.
```

### Comandos

```bash
mkdir -p skills/implement-us/{phases,customizations}
touch skills/implement-us/README.md
touch skills/implement-us/phases/.gitkeep
touch skills/implement-us/customizations/.gitkeep
```

## Checklist de Implementación

- [ ] Crear directorio `skills/implement-us/`
- [ ] Crear subdirectorio `phases/`
- [ ] Crear subdirectorio `customizations/`
- [ ] Crear README.md explicativo
- [ ] Agregar .gitkeep temporal en subdirectorios vacíos
- [ ] Verificar estructura con `tree skills/implement-us/`
- [ ] Commit de la estructura

## Resultado

**Fecha de Completado:** _Pendiente_

### Estructura Creada

_A completar al finalizar._

### Commit

_Pendiente_

**Estado:** 📋 Pendiente
