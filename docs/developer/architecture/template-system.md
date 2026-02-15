# Sistema de Templates - Documentación Técnica

**Claude Dev Kit - Fase 4**
**Versión:** 1.0
**Fecha:** 2026-02-14

---

## Índice

- [Arquitectura del Sistema](#arquitectura-del-sistema)
- [Algoritmo de Reemplazo](#algoritmo-de-reemplazo)
- [Sistema de Snippets](#sistema-de-snippets)
- [Extensibilidad](#extensibilidad)
- [Best Practices](#best-practices)

---

## Arquitectura del Sistema

### Componentes Principales

```
templates/                    # Templates base generalizados
├── bdd/scenario.feature      # Escenarios Gherkin
├── planning/implementation-plan.md
├── reporting/implementation-report.md
└── testing/test-unit.py

skills/implement-us/
├── config.json               # Configuración base
└── customizations/           # Perfiles específicos
    ├── pyqt-mvc.json
    ├── fastapi-rest.json
    ├── flask-rest.json
    ├── flask-webapp.json
    └── generic-python.json
```

### Flujo de Generación

```
┌─────────────────┐
│ Historia de     │
│ Usuario (US-001)│
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────────────┐
│ Skill /implement-us                             │
│                                                  │
│ 1. Determina fase (BDD, Planning, etc.)         │
│ 2. Carga template base                          │
│ 3. Carga perfil activo (ej: pyqt-mvc)          │
│ 4. Reemplaza variables {VAR}                    │
│ 5. Inserta snippets {SNIPPET:id}               │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
         ┌──────────────────┐
         │ Archivo Generado │
         │ (feature/md/py)  │
         └──────────────────┘
```

---

## Algoritmo de Reemplazo

### Proceso de Generación

El sistema utiliza un mecanismo simple de reemplazo de strings que opera en dos fases:

#### Fase 1: Carga y Preparación

1. **Cargar template base** desde `templates/{categoria}/{nombre}.ext`
2. **Leer configuración de perfil** desde `skills/implement-us/customizations/{profile}.json`
3. **Fusionar variables** del perfil con datos de la historia de usuario

#### Fase 2: Reemplazo

4. **Reemplazar variables simples** - Busca placeholders `{VARIABLE_NAME}` y los sustituye con valores del perfil
5. **Insertar snippets** - Busca `{SNIPPET:id}` y los reemplaza con contenido específico del stack
6. **Preservar indentación** - Mantiene el formato del contexto donde se insertan snippets

### Características Clave

- **Reemplazo simple:** String replacement directo, sin motor de templates complejo
- **Orden secuencial:** Variables primero, luego snippets
- **Snippets vacíos:** Soportados (string vacío `""` para perfiles donde no aplica)
- **Sin validación automática:** No verifica que todas las variables fueron reemplazadas

> **Nota de implementación:** El algoritmo será implementado en el módulo `skills/implement-us/` cuando se integre con el skill. Por ahora, los templates y perfiles están listos para uso manual.

---

## Sistema de Snippets

### Definición

Los **snippets** son bloques de código/texto que se insertan condicionalmente según el perfil tecnológico.

### Sintaxis en Templates

```markdown
{SNIPPET:snippet_id}
```

### Sintaxis en Perfiles

```json
{
  "snippets": {
    "snippet_id": "contenido del snippet...",
    "architecture_code_blocks": "### Factory\n\n```python\n...\n```"
  }
}
```

### Tipos de Snippets

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| **Texto** | Bloques de markdown | Checklists, descripciones |
| **Código** | Bloques de código Python | Imports, clases, fixtures |
| **Multilinea** | Contenido con `\n` | Listas, código indentado |
| **Vacío** | String vacío `""` | Snippets que no aplican al perfil |

### Ejemplos de Snippets

#### Snippet de Texto (Checklist)

**Perfil:** `pyqt-mvc.json`
```json
{
  "snippets": {
    "integration_checklist": "- [ ] Componente integrado en Factory\n- [ ] Señales conectadas en Coordinator\n- [ ] Panel agregado a Compositor"
  }
}
```

**Template:** `implementation-plan.md`
```markdown
### Implementación
{SNIPPET:integration_checklist}
```

**Output:**
```markdown
### Implementación
- [ ] Componente integrado en Factory
- [ ] Señales conectadas en Coordinator
- [ ] Panel agregado a Compositor
```

#### Snippet de Código (Python)

**Perfil:** `pyqt-mvc.json`
```json
{
  "snippets": {
    "test_imports": "from dataclasses import replace\nfrom PyQt6.QtCore import QTimer\nfrom unittest.mock import Mock, patch"
  }
}
```

**Template:** `test-unit.py`
```python
import pytest
{SNIPPET:test_imports}

from {MODULE_PATH} import {CLASS_NAME}
```

**Output:**
```python
import pytest
from dataclasses import replace
from PyQt6.QtCore import QTimer
from unittest.mock import Mock, patch

from app.presentacion.display import DisplayController
```

#### Snippet Condicional (Solo un perfil)

**Perfil:** `pyqt-mvc.json`
```json
{
  "snippets": {
    "test_signals_class": "class TestSignals:\n    \"\"\"Tests de señales PyQt.\"\"\"\n    ..."
  }
}
```

**Perfil:** `fastapi-rest.json`
```json
{
  "snippets": {
    "test_signals_class": ""
  }
}
```

**Template:** `test-unit.py`
```python
{SNIPPET:test_signals_class}

class TestValidacion:
    """Tests de validación."""
```

**Output (pyqt-mvc):**
```python
class TestSignals:
    """Tests de señales PyQt."""
    ...

class TestValidacion:
    """Tests de validación."""
```

**Output (fastapi-rest):**
```python

class TestValidacion:
    """Tests de validación."""
```

---

## Extensibilidad

### Agregar Nuevo Template

1. **Crear archivo en `templates/{categoria}/{nombre}.{ext}`**
2. **Usar sintaxis:**
   - Variables: `{VARIABLE_NAME}`
   - Snippets: `{SNIPPET:snippet_id}`
3. **Documentar variables usadas** en header del archivo
4. **Agregar snippets necesarios** a todos los perfiles
5. **Crear ejemplo** en `templates/{categoria}/examples/`
6. **Actualizar `templates/README.md`** con descripción del template

### Agregar Nueva Variable

1. **Definir en perfiles:**
   ```json
   {
     "template_variables": {
       "MY_NEW_VARIABLE": "valor para este perfil"
     }
   }
   ```

2. **Usar en template:**
   ```markdown
   {MY_NEW_VARIABLE}
   ```

3. **Documentar en `templates/README.md`:**
   - Agregar a tabla de variables
   - Incluir descripción, tipo, ejemplo
   - Indicar en qué templates se usa

### Agregar Nuevo Snippet

1. **Definir en TODOS los perfiles:**
   ```json
   {
     "snippets": {
       "my_new_snippet": "contenido..."
     }
   }
   ```

2. **Usar en template:**
   ```markdown
   {SNIPPET:my_new_snippet}
   ```

3. **Documentar en `templates/README.md`:**
   - Agregar a tabla de snippets
   - Incluir descripción y ejemplo

### Agregar Nuevo Perfil

1. **Duplicar perfil similar:**
   ```bash
   cp customizations/generic-python.json customizations/django-mvt.json
   ```

2. **Personalizar:**
   - `profile_metadata`: Nombre, descripción
   - `variables`: Valores específicos del stack
   - `template_variables`: Variables de templates
   - `snippets`: Código específico del framework

3. **Validar:**
   - Generar ejemplos con el nuevo perfil
   - Verificar sintaxis de snippets de código
   - Ejecutar tests (si son archivos .py)

4. **Actualizar config base:**
   ```json
   {
     "available_profiles": ["pyqt-mvc", "fastapi-rest", ..., "django-mvt"]
   }
   ```

---

## Best Practices

### Para Templates

1. **Variables en MAYÚSCULAS:** `{US_ID}`, `{COMPONENT_NAME}`
2. **Snippets en minúsculas:** `{SNIPPET:integration_checklist}`
3. **Comentarios al inicio:** Documentar variables disponibles
4. **Sintaxis válida base:** Template debe tener sintaxis válida antes de reemplazo
5. **Ejemplos realistas:** No usar `{VAR}` en ejemplos, usar valores reales
6. **Compatibilidad:** Testear con múltiples perfiles

### Para Variables

1. **Nombres descriptivos:** `ARCHITECTURE_DESCRIPTION` vs `ARCH_DESC`
2. **Evitar ambigüedad:** `TEST_FILE_PATTERN` vs `TEST_FILES`
3. **Multilinea con `\n`:** Usar `\n` explícito en JSON
4. **Valores por defecto:** Proveer en config base para fallback
5. **Documentar tipo:** String, Number, Boolean, Snippet

### Para Snippets

1. **Un propósito claro:** Cada snippet hace una cosa
2. **Nombres consistentes:** `*_checklist`, `*_code_blocks`, `*_class`
3. **Indentación preservada:** Snippets deben mantener indentación
4. **Sintaxis validada:** Código en snippets debe compilar
5. **Vacíos permitidos:** `""` para perfiles donde no aplica
6. **Documentación inline:** Incluir comentarios en código de snippets

### Para Perfiles

1. **Estructura consistente:** Mismo schema para todos los perfiles
2. **Testing exhaustivo:** Generar y ejecutar tests con cada perfil
3. **Comentarios útiles:** Explicar decisiones de diseño
4. **Versionado:** Incluir `version` en metadata
5. **Ejemplos incluidos:** Link a proyecto de ejemplo

### Para Testing

1. **Validación de sintaxis:** Lint/compile todos los outputs
2. **Ejecución real:** Tests .py deben pasar pytest
3. **Contenido coherente:** Verificar lógica del contenido
4. **No variables sin reemplazar:** Detectar `{VAR}` restantes
5. **Casos edge:** Probar snippets vacíos, variables missing

---

## Implementación de Referencia

### Estructura de Perfil

Cada perfil tecnológico se define en un archivo JSON con cuatro secciones principales:

1. **`profile_metadata`** - Nombre, versión, descripción del perfil
2. **`variables`** - Variables de configuración del skill (patrones arquitectónicos, rutas, etc.)
3. **`template_variables`** - Variables específicas para templates (ej: `BACKGROUND_SETUP`, `ARCHITECTURE_DESCRIPTION`)
4. **`snippets`** - Bloques de código/texto condicionales (ej: `test_imports`, `integration_checklist`)

**Ejemplo mínimo:**
```json
{
  "profile_metadata": {
    "name": "mi-stack",
    "version": "1.0.0"
  },
  "template_variables": {
    "BACKGROUND_SETUP": "Given el sistema está listo"
  },
  "snippets": {
    "test_imports": "import pytest"
  }
}
```

**Ver perfiles completos en:**
- `skills/implement-us/customizations/pyqt-mvc.json` (~400 líneas)
- `skills/implement-us/customizations/fastapi-rest.json`
- `skills/implement-us/customizations/flask-rest.json`
- `skills/implement-us/customizations/flask-webapp.json`
- `skills/implement-us/customizations/generic-python.json`

---

## Métricas del Sistema

### Templates

- **Total:** 4 templates
- **Categorías:** BDD (1), Planning (1), Reporting (1), Testing (1)
- **Líneas totales:** ~900 líneas

### Variables

- **Total:** 20-25 variables
- **Simples:** ~15 (strings directos)
- **Snippets:** ~10 (bloques multilinea)

### Snippets

- **Total:** 7 tipos de snippets
- **Definiciones:** 7 × 5 perfiles = 35 snippets
- **Líneas de código:** ~500-800 líneas de snippets

### Perfiles

- **Total:** 5 perfiles
- **Tamaño promedio:** ~1,000 líneas por perfil
- **Cobertura:** 85-95% de proyectos Python

---

## Roadmap Futuro

### Corto Plazo (Sprint 3)
- ✅ Implementar sistema de templates (COMPLETADO)
- ⬜ Integrar con skill /implement-us (modificar skill)
- ⬜ Validar con proyectos reales

### Medio Plazo
- ⬜ Agregar perfil Django MVT
- ⬜ Agregar templates adicionales (ADR, Runbook)
- ⬜ Mecanismo de validación automática
- ⬜ Editor visual de templates (CLI)

### Largo Plazo
- ⬜ Soporte para lenguajes adicionales (TypeScript, Go, Rust)
- ⬜ Templates para frameworks frontend (React, Vue)
- ⬜ Integración con IDEs (VSCode extension)
- ⬜ Marketplace de templates custom

---

**Documento generado por:** Claude Code
**Versión:** 1.0
**Última actualización:** 2026-02-14
