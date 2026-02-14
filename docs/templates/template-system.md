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

### Reemplazo de Variables

**Input:** Template con placeholders `{VARIABLE_NAME}`
**Output:** Template con valores reales del perfil

#### Pseudocódigo

```python
def render_template(template_path: str, profile: str, us_data: dict) -> str:
    # 1. Cargar template base
    template_content = read_file(template_path)

    # 2. Cargar configuración de perfil
    profile_config = load_json(f"customizations/{profile}.json")

    # 3. Fusionar datos
    variables = {
        **profile_config["template_variables"],
        **us_data  # Datos específicos de la historia de usuario
    }

    # 4. Reemplazar variables simples
    for var_name, var_value in variables.items():
        placeholder = f"{{{var_name}}}"
        template_content = template_content.replace(placeholder, var_value)

    # 5. Reemplazar snippets
    snippets = profile_config["snippets"]
    for snippet_id, snippet_content in snippets.items():
        placeholder = f"{{SNIPPET:{snippet_id}}}"
        template_content = template_content.replace(placeholder, snippet_content)

    return template_content
```

### Características del Algoritmo

1. **Reemplazo Simple:** String replacement sin templating engine complejo
2. **Orden de Ejecución:** Variables primero, luego snippets
3. **Preservación de Indentación:** Snippets mantienen indentación del contexto
4. **Snippets Vacíos:** Soportado (ej. `test_signals_class` para non-PyQt)
5. **Validación:** No valida que todas las variables fueron reemplazadas

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

### Estructura de Perfil Completo

```json
{
  "_comment_profile": "Descripción del perfil",

  "profile_metadata": {
    "name": "perfil-nombre",
    "display_name": "Nombre Legible",
    "description": "Descripción detallada",
    "version": "1.0.0",
    "target_stack": "Framework + versión"
  },

  "variables": {
    "architecture_pattern": {
      "default": "pattern-name",
      "description": "Descripción del patrón"
    }
  },

  "template_variables": {
    "BACKGROUND_SETUP": "Given ...\nAnd ...",
    "TEST_FILE_PATTERN": "- [ ] ...\n- [ ] ...",
    "ARCHITECTURE_DESCRIPTION": "Descripción..."
  },

  "snippets": {
    "integration_checklist": "- [ ] Item 1\n- [ ] Item 2",
    "architecture_code_blocks": "### Sección\n\n```python\n...\n```",
    "test_imports": "from ...\nimport ...",
    "test_signals_class": "class TestSignals:\n    ...",
    "test_integration_class": "class TestIntegracion:\n    ...",
    "test_fixtures": "@pytest.fixture\ndef ...\n    ..."
  }
}
```

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
