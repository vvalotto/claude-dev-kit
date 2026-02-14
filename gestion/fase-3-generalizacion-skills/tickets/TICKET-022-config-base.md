# TICKET-022: Crear config.json Base Genérico

**Estado:** ✅ Completado
**Fecha Inicio:** 2026-02-13
**Fecha Fin:** 2026-02-13
**Estimación:** 1 hora
**Tiempo Real:** ~30 minutos

---

## Objetivo

Crear el archivo `skills/implement-us/config.json` con la configuración base genérica que servirá como foundation para todos los perfiles de customización del skill implement-us.

---

## Contexto

Este archivo es crítico porque:
- Define los valores por defecto genéricos para proyectos Python
- Establece la estructura de configuración que todos los perfiles extenderán
- Documenta las 8 variables parametrizadas del skill
- Define las 9 fases del flujo de implementación
- Configura quality gates y tracking

---

## Implementación

### Archivo Creado

**Ubicación:** `skills/implement-us/config.json`
**Tamaño:** ~250 líneas
**Formato:** JSON con comentarios descriptivos (prefijo `_comment_`)

### Estructura del Archivo

#### 1. Metadata (líneas 3-11)
```json
{
  "metadata": {
    "version": "2.0.0",
    "skill_name": "implement-us",
    "description": "...",
    "author": "Claude Dev Kit",
    "created": "2026-02-13",
    "last_updated": "2026-02-13"
  }
}
```

#### 2. Variables (líneas 15-95)

Definición de las 8 variables parametrizadas:

| Variable | Default | Descripción |
|----------|---------|-------------|
| `architecture_pattern` | `generic` | Patrón arquitectónico (mvc, mvt, layered, clean-architecture, generic) |
| `component_type` | `Component` | Tipo de componente según el stack |
| `component_path` | `src/{name}/` | Ruta base para componentes |
| `test_framework` | `pytest` | Framework de testing |
| `base_class` | `object` | Clase base para componentes |
| `domain_context` | `application` | Contexto de dominio |
| `project_root` | `.` | Raíz del proyecto |
| `product` | `main` | Nombre del producto/módulo |

Cada variable incluye:
- `default`: Valor por defecto genérico
- `description`: Documentación
- `available`: Opciones disponibles (donde aplica)
- `examples`: Ejemplos por stack (PyQt, FastAPI, Django, Generic)

#### 3. Phases (líneas 99-180)

Definición completa de las 9 fases del skill:

```json
"phases": {
  "0": {
    "name": "Validación de Contexto",
    "duration_min": 5,
    "duration_max": 10,
    "approval_required": false,
    "agent_file": "phases/phase-0-validation.md"
  },
  // ... fases 1-9
}
```

Cada fase incluye:
- `name`: Nombre descriptivo
- `description`: Propósito de la fase
- `duration_min/max`: Estimaciones de tiempo en minutos
- `approval_required`: Si requiere aprobación del usuario
- `agent_file`: Archivo del agente especializado
- `output_template`: Template de salida (opcional)

#### 4. Tracking (líneas 184-196)

Configuración del sistema de time tracking:
- `enabled`: true por defecto
- `auto_start`: Inicio automático de tracking
- `auto_pause_on_approval`: Pausa automática en checkpoints
- `storage_path`: Ubicación de datos de tracking
- `variance_threshold_percent`: Umbral de varianza permitido (20%)

#### 5. Quality Gates (líneas 200-234)

Umbrales de calidad para Fase 7:

| Métrica | Herramienta | Umbral |
|---------|-------------|--------|
| Pylint | pylint | ≥ 8.0/10 |
| Complejidad Ciclomática | radon | ≤ 10 por función |
| Índice de Mantenibilidad | radon | ≥ 20 |
| Cobertura de Tests | pytest-cov | ≥ 95% |

Cada quality gate incluye:
- `enabled`: Si está activado
- `min/max`: Umbrales numéricos
- `tool`: Herramienta a utilizar
- `exclude_patterns`: Archivos a excluir de la validación

#### 6. Test Framework Config (líneas 238-257)

Configuración del framework de testing:
- `runner`: pytest por defecto
- `plugins`: Lista de plugins (vacía en base, se llena en perfiles)
- `markers`: Marcadores de pytest (unit, integration, bdd, slow)
- `coverage_config`: Configuración de cobertura

#### 7. Component Structure (líneas 261-268)

Estructura por defecto de componentes (muy genérica):
```json
"default": {
  "files": ["__init__.py", "main.py"],
  "test_files": ["test_{component_name}.py"],
  "base_path": "src/{component_name}/",
  "test_path": "tests/test_{component_name}/"
}
```

Esta estructura se especializa en cada perfil de customización.

#### 8. BDD Config (líneas 272-279)

Configuración de BDD (pytest-bdd):
- `runner`: pytest-bdd
- `feature_template`: Template de archivos .feature
- `steps_template`: Template de steps
- `tag_prefix`: Prefijo de tags (@US-)
- `language`: Idioma de los escenarios (es)

#### 9. Documentation Config (líneas 283-290)

Rutas de documentación generada:
- `plan_path`: Planes de implementación
- `report_path`: Reportes finales
- `adr_path`: Architecture Decision Records

#### 10. Git Config (líneas 294-300)

Configuración de integración con Git:
- `auto_commit`: false por defecto (no hacer commits automáticos)
- `commit_message_template`: Template de mensajes de commit
- `branch_naming`: Convención de nombres de branches
- `auto_push`: false por defecto

---

## Decisiones de Diseño

### 1. Uso de Comentarios en JSON

Aunque JSON estándar no soporta comentarios, usamos campos `_comment_*` para documentación inline. Esto permite:
- Documentar el propósito de cada sección
- Guiar a futuros desarrolladores
- Mantener la documentación cerca del código

Los parsers JSON ignoran estos campos automáticamente.

### 2. Valores Genéricos por Defecto

Los valores por defecto son **ultra-genéricos** para Python:
- `architecture_pattern: "generic"`
- `component_type: "Component"`
- `test_framework: "pytest"`
- `project_root: "."`

Esto asegura que el skill funcione "out-of-the-box" en cualquier proyecto Python, aunque no esté optimizado para ningún stack específico.

### 3. Estructura de Variables

Cada variable incluye:
- `default`: Valor fallback
- `description`: Para autodocumentación
- `examples`: Por cada stack soportado (PyQt, FastAPI, Django, Generic)

Esto facilita la creación de perfiles de customización.

### 4. Tiempos Estimados por Fase

Las duraciones `duration_min/max` son **estimaciones conservadoras** basadas en:
- Experiencia del proyecto ISSE_Simuladores
- Tiempo promedio de tareas reales
- Buffer para imprevistos

Los perfiles pueden ajustar estos tiempos según el stack.

### 5. Quality Gates Estrictos

Los umbrales de calidad son **altos pero alcanzables**:
- Pylint ≥ 8.0 (en escala de 10)
- CC ≤ 10 por función (recomendación estándar)
- MI ≥ 20 (código mantenible)
- Coverage ≥ 95% (muy alta cobertura)

Esto fuerza buenas prácticas desde el inicio.

---

## Validación

### Tests Realizados

1. **Validación sintáctica JSON:**
   ```bash
   python3 -m json.tool config.json > /dev/null
   # ✅ JSON válido
   ```

2. **Verificación de estructura:**
   - ✅ Todas las secciones presentes
   - ✅ 8 variables definidas
   - ✅ 9 fases configuradas
   - ✅ Quality gates completos

3. **Verificación de valores:**
   - ✅ Valores por defecto genéricos
   - ✅ Ejemplos por stack incluidos
   - ✅ Umbrales de calidad definidos

---

## Próximos Pasos

Este archivo es la **base** para los siguientes tickets:

### TICKET-023: Perfil pyqt-mvc.json
Extender config.json con:
- `architecture_pattern: "mvc"`
- `test_framework: "pytest + pytest-qt"`
- Estructura de componentes MVC
- Fixtures específicos de PyQt

### TICKET-024: Perfil fastapi-rest.json
Extender config.json con:
- `architecture_pattern: "layered"`
- `test_framework: "pytest + httpx"`
- Estructura de capas (router, service, repository)

### TICKET-025: Perfil django-mvt.json
Extender config.json con:
- `architecture_pattern: "mvt"`
- `test_framework: "pytest-django"`
- Estructura MVT estándar de Django

### TICKET-026: Perfil generic-python.json
Perfil minimalista que usa casi todos los defaults de config.json base.

---

## Notas de Implementación

### Convención de Nombres

- **Campos de configuración:** snake_case (JSON estándar Python)
- **Comentarios:** Prefijo `_comment_` + nombre de sección
- **Templates de paths:** Usar `{variable}` para placeholders

### Extensibilidad

Los perfiles de customización pueden:
1. **Override** cualquier campo del config base
2. **Agregar** nuevos campos específicos del stack
3. **Especializar** la sección `component_structure`

Ejemplo de override:
```json
// En pyqt-mvc.json
{
  "variables": {
    "architecture_pattern": {
      "default": "mvc"  // Override del valor "generic"
    }
  }
}
```

### Merge Strategy

El instalador fusionará:
```
config.json (base) + {perfil}.json (customización) = config instalado
```

Estrategia de merge:
- **Deep merge** de objetos anidados
- **Override completo** de valores primitivos
- **Concatenación** de arrays (donde tenga sentido)

---

## Métricas

- **Tiempo estimado:** 1 hora
- **Tiempo real:** ~30 minutos
- **Líneas de código:** 250 líneas
- **Secciones implementadas:** 10
- **Variables definidas:** 8
- **Fases configuradas:** 9
- **Quality gates:** 4

---

## Referencias

- **Sprint 2 Plan:** `gestion/fase-3-generalizacion-skills/sprint-2.md`
- **Análisis TICKET-019:** `docs/analysis/TICKET-019-analysis.md`
- **Skill Generalizado:** `skills/implement-us/skill.md`
- **Perfiles de Ejemplo:** Sprint 2 (líneas 146-178)

---

**Ticket completado exitosamente.** ✅

El archivo `config.json` base está listo para ser extendido por los 4 perfiles de customización en los siguientes tickets.
