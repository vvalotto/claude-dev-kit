# Fase 8: Actualización de Documentación

**Objetivo:** Actualizar la documentación del proyecto para reflejar los cambios y componentes implementados.


---

## 🔴 Acción Requerida — Verificar precondiciones

Antes de comenzar esta fase, confirmá que existe el artefacto generado en Fase 7:

```bash
ls quality/reports/{US_ID}-quality.json
```

Si no existe, **no avances** — completá la fase correspondiente primero.

---

## 🔴 Acción Requerida — Iniciar tracking de fase

Ejecutá como primera acción, antes de cualquier otra:

```bash
python .claude/tracking/tracker_cli.py start-phase 8 "Actualización de Documentación"
```

---

## Acción

Actualizar documentos relevantes del proyecto para mantener la documentación sincronizada con el código implementado.

---

## Pasos de Actualización

### 1. Actualizar Plan de Implementación

**Archivo:** `{PROJECT_PATH}/docs/plans/{US_ID}-plan.md` (o ubicación configurada)

**Cambios a realizar:**

1. **Marcar US como completada:**
   ```markdown
   **Estado:** ✅ COMPLETADO
   **Fecha completado:** 2026-02-11
   ```

2. **Agregar tiempo real vs estimado:**
   ```markdown
   ## Métricas de Tiempo

   - **Tiempo estimado:** 3h 00min
   - **Tiempo real:** 2h 45min
   - **Varianza:** -15 min (-8%)
   ```
   > Si el CLI de tracking no está disponible, usá el tiempo real observado en la sesión o dejá la sección con los estimados del plan y una nota: *"Tracking no disponible — tiempos estimados."*

3. **Agregar lecciones aprendidas (opcional pero recomendado):**
   ```markdown
   ## Lecciones Aprendidas

   - ✅ Los tests unitarios detectaron un edge case en validación de datos
   - ⚠️ La integración con {EXTERNAL_SERVICE} tomó más tiempo del esperado
   - 💡 Usar fixtures compartidos redujo duplicación en tests
   ```

**Ejemplo de actualización:**

```markdown
# Plan de Implementación: {US_ID}

**Historia:** {US_TITLE}
**Estimación:** 3 puntos
**Estado:** ✅ COMPLETADO
**Fecha completado:** 2026-02-11

## Métricas de Tiempo

| Fase | Estimado | Real | Varianza |
|------|----------|------|----------|
| BDD Scenarios | 20 min | 15 min | -5 min |
| Plan | 15 min | 20 min | +5 min |
| Implementation | 60 min | 55 min | -5 min |
| Unit Tests | 30 min | 35 min | +5 min |
| Integration Tests | 20 min | 20 min | 0 min |
| BDD Validation | 15 min | 10 min | -5 min |
| Quality Gates | 10 min | 10 min | 0 min |
| Documentation | 10 min | 10 min | 0 min |
| **Total** | **180 min** | **165 min** | **-15 min** |

## Lecciones Aprendidas

- ✅ Arquitectura modular facilitó testing
- 💡 Usar dataclasses inmutables previno bugs de estado compartido
```

---

### 2. 🔴 Acción Requerida — Discovery de documentación de arquitectura

Buscá activamente los archivos de arquitectura del proyecto antes de decidir si actualizar:

```bash
# Buscar archivos con diagramas
grep -rl "mermaid\|plantuml\|graph LR\|graph TD\|C4Context" docs/ 2>/dev/null

# Buscar archivos de arquitectura por nombre
find . -iname "ARCHITECTURE*" -o -iname "architecture*" -o -name "*.puml" 2>/dev/null
```

Leé cada archivo encontrado y evaluá si refleja los cambios realizados en esta US. Si un diagrama o descripción quedó desactualizado, actualizá ese archivo aunque el criterio de abajo no lo indique explícitamente.

---

### 3. Actualizar Arquitectura (si aplica)

**Cuándo actualizar:**
- Se agregó un componente nuevo significativo
- Se modificó la estructura de módulos
- Se cambió un patrón arquitectónico
- Se agregó una nueva integración externa

**Archivos típicos:**
- `docs/architecture.md`
- `docs/ARCHITECTURE.md`
- `README.md` (sección de arquitectura)

**Qué documentar:**

#### PyQt/MVC
```markdown
## Arquitectura - Panel {COMPONENT_NAME}

### Estructura MVC

```
app/presentacion/paneles/{component_name}/
├── modelo.py          # Modelo (dataclass inmutable)
├── vista.py           # Vista (QWidget)
├── controlador.py     # Controlador (mediador)
└── __init__.py        # Factory function
```

### Responsabilidades

- **Modelo:** Estado inmutable, validación de datos
- **Vista:** Interfaz gráfica, layout, widgets
- **Controlador:** Mediación, señales, lógica de presentación

### Integración

- Se conecta con {EXTERNAL_SERVICE} vía {CONNECTION_METHOD}
- Recibe actualizaciones desde {DATA_SOURCE}
```

#### FastAPI/Layered
```markdown
## Arquitectura - {COMPONENT_NAME}

### Estructura en Capas

```
app/
├── api/v1/endpoints/{component}.py  # Endpoints REST
├── services/{component}_service.py  # Lógica de negocio
├── repositories/{component}_repo.py # Acceso a datos
├── models/{component}.py            # Modelos ORM
└── schemas/{component}.py           # Schemas Pydantic
```

### Flujo de Request

```
Cliente → Endpoint → Service → Repository → Database
         ↓          ↓          ↓
       Auth     Business   Data Access
     Validation  Logic
```
```

#### Generic Python
```markdown
## Módulo {COMPONENT_NAME}

### Estructura

```
{module_path}/
├── {component}.py      # Clase principal
├── utils.py           # Utilidades
└── __init__.py        # API pública
```

### API Pública

```python
from {module_path} import {ComponentClass}

# Crear instancia
component = {ComponentClass}(config)

# Método principal
result = component.process(data)
```
```

**Diagramas (si corresponde):**

Actualizar o crear diagramas de:
- Arquitectura de componentes
- Flujo de datos
- Diagrama de clases
- Diagrama de secuencia

**Herramientas:**
- Mermaid (embebido en Markdown)
- PlantUML
- draw.io / Excalidraw

**Ejemplo con Mermaid:**
```markdown
### Diagrama de Componentes

```mermaid
graph LR
    A[Cliente] --> B[{COMPONENT_NAME}Controller]
    B --> C[{COMPONENT_NAME}Service]
    C --> D[Database]
    C --> E[External API]
```
```

---

### 4. Actualizar CHANGELOG.md

**Archivo:** `{PROJECT_PATH}/CHANGELOG.md`

**Formato recomendado:** [Keep a Changelog](https://keepachangelog.com/)

**Agregar entrada:**

```markdown
# Changelog

## [Unreleased]

### Added
- [{US_ID}] {US_TITLE} - {BRIEF_DESCRIPTION}
  - Implemented {COMPONENT_TYPE} for {FUNCTIONALITY}
  - Added {TEST_COUNT} unit tests and {INTEGRATION_TEST_COUNT} integration tests
  - Coverage: {COVERAGE}%

### Changed
- Updated {AFFECTED_MODULE} to support {NEW_FEATURE}

### Fixed
- Fixed {BUG_DESCRIPTION} in {COMPONENT}

---

## [1.2.0] - 2026-02-11

### Added
- [US-042] User profile management - Profile panel implemented
  - Implemented MVC pattern for user profile display and editing
  - Added 15 unit tests and 4 integration tests
  - Coverage: 97%
```

**Categorías estándar:**
- **Added:** Nuevas funcionalidades
- **Changed:** Cambios en funcionalidades existentes
- **Deprecated:** Funcionalidades que serán removidas
- **Removed:** Funcionalidades removidas
- **Fixed:** Correcciones de bugs
- **Security:** Correcciones de seguridad

---

### 5. Actualizar README (si aplica)

**Cuándo actualizar README:**
- ✅ Se agregó funcionalidad visible al usuario
- ✅ Se cambió la forma de instalar/configurar
- ✅ Se agregaron nuevas dependencias
- ✅ Se cambió la estructura del proyecto

**Secciones a actualizar:**

#### Features/Características
```markdown
## Features

- ✅ User authentication and authorization
- ✅ User profile management ← **NUEVO**
- ✅ Dashboard with real-time updates
- ✅ Notifications system
```

#### Screenshots (si aplica)
```markdown
## Screenshots

### User Profile Panel

![User Profile](docs/images/user-profile-screenshot.png)

Features:
- Edit name, email, bio
- Upload profile picture
- Privacy settings
```

#### Installation/Dependencies
```markdown
## Dependencies

- Python 3.12+
- PyQt6 >= 6.6.0
- pytest >= 7.0.0
- pytest-qt >= 4.2.0 ← **NUEVO**
```

#### Usage/Ejemplos
```markdown
## Usage

### Create User Profile

```python
from app.presentacion.paneles.user_profile import crear_user_profile_panel

# Create panel
panel = crear_user_profile_panel(user_id=1)
panel.show()
```
```

---

### 6. Actualizar Documentación Técnica (opcional)

**Para proyectos con documentación extensa:**

#### API Documentation (FastAPI, Flask REST)
```markdown
## API Endpoints - {COMPONENT_NAME}

### List {RESOURCE}

**GET** `/api/v1/{resource}`

**Response:**
```json
{
  "items": [...],
  "total": 42,
  "page": 1
}
```

### Create {RESOURCE}

**POST** `/api/v1/{resource}`

**Request Body:**
```json
{
  "name": "Example",
  "value": 123
}
```
```

#### Developer Guide
```markdown
## Developer Guide - {COMPONENT_NAME}

### Adding a New Field

1. Update model in `models/{component}.py`
2. Create migration: `python manage.py makemigrations`
3. Update serializer in `schemas/{component}.py`
4. Add validation in service
5. Update tests
```

---


---

## Automatización (opcional)

Algunas actualizaciones pueden automatizarse:

### Auto-generar CHANGELOG desde commits
```bash
# Usar conventional-changelog
npx conventional-changelog -p angular -i CHANGELOG.md -s

# O git-chglog
git-chglog -o CHANGELOG.md
```

### Auto-generar documentación de API
```bash
# FastAPI: OpenAPI generado automáticamente
# Accesible en /docs (Swagger UI) y /redoc

# Flask REST: Usar flask-openapi3 o flasgger si están instalados
# Si no hay generación automática, documentar manualmente los endpoints

# Sphinx para código Python (todos los stacks)
sphinx-apidoc -o docs/api/ app/
```

---


---

## ✅ Checklist de Salida

Antes de avanzar a Fase 9, confirmá que:
- [ ] Plan de implementación actualizado con estado "Completado" y tiempo real
- [ ] Discovery de arquitectura ejecutado — archivos desactualizados corregidos
- [ ] CHANGELOG.md tiene entrada nueva para esta US
- [ ] README actualizado (si se agregó funcionalidad visible o cambió estructura)
- [ ] No hay referencias a código obsoleto en la documentación
- [ ] El usuario revisó y aprobó la documentación generada
- [ ] Tracking de Fase 8 cerrado

## 🔴 Acción Requerida — Cerrar tracking

```bash
python .claude/tracking/tracker_cli.py end-phase 8
```

---

## Resumen de la Fase

Al finalizar esta fase:

✅ Plan de implementación actualizado (estado, tiempos, lecciones)
✅ Arquitectura documentada (si hubo cambios)
✅ CHANGELOG.md con entrada de la US
✅ README actualizado con nueva funcionalidad (si aplica)
✅ Documentación técnica sincronizada con código
✅ Screenshots y diagramas actualizados
✅ Proyecto listo para que otros desarrolladores entiendan los cambios

**Próxima fase:** Fase 9 - Reporte Final
