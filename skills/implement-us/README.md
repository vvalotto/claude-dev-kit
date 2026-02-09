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
