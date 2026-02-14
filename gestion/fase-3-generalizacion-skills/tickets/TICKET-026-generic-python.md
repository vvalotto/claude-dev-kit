# TICKET-026: Crear Perfil generic-python.json

**Estado:** ✅ Completado
**Fecha Inicio:** 2026-02-13
**Fecha Fin:** 2026-02-13
**Estimación:** 1 hora
**Tiempo Real:** ~25 minutos

---

## Objetivo

Crear el perfil de customización `generic-python.json` para proyectos Python genéricos sin framework específico. Este perfil es **minimalista** y usa la mayoría de los defaults del `config.json` base.

---

## Contexto

Este es el **perfil más simple** de todos, diseñado para:
- Proyectos Python sin framework web/UI específico
- Librerías y paquetes Python
- Scripts y herramientas CLI
- Data science / ML projects
- Automatizaciones y bots
- Cualquier proyecto que no encaje en PyQt/FastAPI/Django

**Filosofía:** Si no sabes qué perfil usar, usa este. Es el "default del default".

---

## Implementación

### Archivo Creado

**Ubicación:** `skills/implement-us/customizations/generic-python.json`
**Tamaño:** ~280 líneas
**Características:** Minimalista, usa mayoría de defaults

### Características Principales

#### 1. Mínimos Overrides

Este perfil **NO override** la mayoría de variables del config base:

| Variable | Valor Base | Valor Generic | Override? |
|----------|------------|---------------|-----------|
| `architecture_pattern` | `generic` | `generic` | ❌ No (usa default) |
| `component_type` | `Component` | `Module` | ✅ Sí (más descriptivo) |
| `component_path` | `src/{name}/` | `src/{name}/` | ❌ No (usa default) |
| `test_framework` | `pytest` | `pytest` | ❌ No (usa default) |
| `base_class` | `object` | `object` | ❌ No (usa default) |
| `domain_context` | `application` | `core` | ✅ Sí (más genérico) |
| `project_root` | `.` | `.` | ❌ No (usa default) |

**Solo 2 variables override:** `component_type` y `domain_context`.

#### 2. Use Cases Documentados

```json
"use_cases": [
  "Proyectos Python sin framework web/UI específico",
  "Librerías y paquetes Python",
  "Scripts y herramientas de línea de comandos",
  "Proyectos de data science / machine learning",
  "Automatizaciones y bots",
  "Microservicios sin FastAPI/Flask",
  "Cualquier proyecto Python que no encaje en PyQt/FastAPI/Django"
]
```

#### 3. Component Structure Simple

**2 estructuras:**

1. **python_module:** Módulo simple
   ```
   src/{module_name}/
   ├── {module_name}.py
   └── __init__.py
   ```

2. **python_package:** Paquete completo
   ```
   src/{package_name}/
   ├── __init__.py
   ├── core.py
   ├── utils.py
   └── exceptions.py
   ```

**Archivos opcionales:**
- `constants.py` (constantes)
- `exceptions.py` (excepciones custom)
- `types.py` (type aliases, protocols)
- `utils.py` (funciones auxiliares)

#### 4. Test Framework Básico

**Solo pytest + pytest-cov:**
```json
"plugins": ["pytest-cov"]
```

**Sin fixtures específicos** (usa defaults de pytest).

**Markers:**
- `unit`, `integration`, `slow`
- `requires_network`, `requires_file`

#### 5. Quality Gates Estándar

**Sin modificaciones** - Usa defaults del config base:
- Pylint ≥8.0
- CC ≤10
- MI ≥20
- Coverage ≥95%

#### 6. Dependencies Mínimas

**Required:**
- pytest ≥7.0.0
- pytest-cov ≥4.0.0

**Development:**
- pylint, radon, black, mypy, isort

**Optional:**
- pytest-bdd (si se usa BDD)
- hypothesis (property-based testing)
- pytest-mock (mocking)
- pytest-timeout (timeouts)

#### 7. Design Patterns

**Patrones recomendados:**

1. **SOLID Principles:** SRP, OCP, LSP, ISP, DIP
2. **Composition over Inheritance:** Preferir composición
3. **Type Hints:** Usar en todo el código
4. **Docstrings:** Google style o NumPy style

#### 8. Best Practices

**Code Style:**
- Formatter: black (PEP 8)
- Import sorting: isort
- Line length: 88
- Quotes: double

**Type Checking:**
- Tool: mypy
- Strictness: `mypy --strict`
- Protocol usage: typing.Protocol

**Testing:**
- Style: AAA pattern (Arrange-Act-Assert)
- Naming: `test_<function>_<scenario>_<expected>`
- Parametrize: `@pytest.mark.parametrize`

**Project Structure:**
- Recommended: src layout (`src/{package}/`)
- Benefits: Evita imports ambiguos

#### 9. Packaging

**pyproject.toml** (PEP 517/518):
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "{package_name}"
version = "0.1.0"
python_requires = ">=3.8"
```

#### 10. CI/CD Suggestions

**GitHub Actions:**
- Run pytest on push/PR
- Linting (pylint, black, mypy)
- Coverage upload (codecov.io)
- Publish to PyPI on release

**Pre-commit hooks:**
- black, isort, pylint, mypy, pytest

---

## Decisiones de Diseño

### 1. Minimalismo Extremo

**Decisión:** Override solo 2 variables, usar mayoría de defaults.

**Justificación:**
- El config base YA está diseñado para Python genérico
- Menos overrides = menos complejidad
- Más fácil de mantener

**Impacto:** Perfil súper simple (~280 líneas vs ~460 de FastAPI).

### 2. Enfoque en Best Practices

**Decisión:** Documentar best practices en lugar de forzar estructura.

**Justificación:**
- Proyectos genéricos son muy variados
- No se puede forzar una estructura específica
- Mejor guiar que imponer

**Impacto:** Perfil más educativo que prescriptivo.

### 3. Dependencies Mínimas

**Decisión:** Solo pytest + pytest-cov como required.

**Justificación:**
- Proyectos genéricos tienen necesidades variadas
- Dejar que el usuario agregue lo que necesite
- Evitar bloat de dependencias

**Impacto:** Instalación más rápida, menos conflictos.

### 4. Sin Framework-Specific Patterns

**Decisión:** No incluir patterns específicos (MVC, Layered, etc.).

**Justificación:**
- Proyectos genéricos usan patterns variados
- SOLID + Composition son universales
- Dejar libertad arquitectónica

**Impacto:** Más flexible, menos opinionado.

---

## Comparación de Perfiles

| Aspecto | PyQt/MVC | FastAPI/Layered | **Generic** |
|---------|----------|-----------------|-------------|
| **Líneas** | ~350 | ~460 | **~280** |
| **Overrides** | 7 variables | 7 variables | **2 variables** |
| **Files per Feature** | 3 | 5 | **1-2** |
| **Test Framework** | pytest-qt | pytest + httpx | **pytest** |
| **Fixtures** | qapp, qtbot | client, async_client, db | **Ninguno** |
| **Patterns** | MVC, Factory, Coordinator | Layered, DI, Repository | **SOLID, Composition** |
| **Quality Gates** | Ajustados (90% cov) | Elevados (95% cov, Pylint 8.5) | **Estándar (95% cov, Pylint 8.0)** |
| **Opinionado** | Alto | Medio | **Bajo** |
| **Complejidad** | Alta | Media | **Baja** |

---

## Cuándo Usar Cada Perfil

**Use `pyqt-mvc.json` si:**
- ✅ Estás construyendo una aplicación desktop con PyQt6
- ✅ Necesitas arquitectura MVC estricta
- ✅ Tienes UI con widgets

**Use `fastapi-rest.json` si:**
- ✅ Estás construyendo una API REST
- ✅ Necesitas async/await
- ✅ Usas FastAPI

**Use `generic-python.json` si:**
- ✅ Tu proyecto NO es PyQt ni FastAPI
- ✅ Quieres máxima flexibilidad
- ✅ Estás construyendo una librería, CLI tool, script, etc.
- ✅ **No sabes qué perfil usar** → Usa este por defecto

---

## Validación

1. **JSON válido:** ✅ `python3 -m json.tool`
2. **Estructura mínima:** ✅ Solo 2 overrides
3. **Best practices documentadas:** ✅ SOLID, type hints, docstrings, testing
4. **Use cases claros:** ✅ 7 casos de uso documentados
5. **CI/CD suggestions:** ✅ GitHub Actions, pre-commit hooks

---

## Próximos Pasos

Con este perfil completado, tenemos **3 perfiles funcionales:**
1. ✅ PyQt/MVC (aplicaciones desktop)
2. ✅ FastAPI/Layered (APIs REST)
3. ✅ Generic Python (todo lo demás)

### Siguiente Ticket: TICKET-027

**Testing y validación de perfiles:**
- Validar que todos los perfiles se cargan correctamente
- Probar fusión de config base + perfil
- Verificar que variables se reemplazan bien
- Testing de integración del skill con cada perfil
- Documentación de casos de uso

---

## Métricas

- **Tiempo estimado:** 1 hora
- **Tiempo real:** ~25 minutos ⚡ (75% más rápido)
- **Líneas de código:** ~280 líneas
- **Overrides:** 2 variables (mínimo)
- **Dependencies:** 2 required (pytest, pytest-cov)
- **Patterns:** 4 (SOLID, Composition, Type Hints, Docstrings)
- **Best practices:** 6 categorías documentadas

---

## Referencias

- **Config Base:** `skills/implement-us/config.json`
- **Perfil PyQt:** `skills/implement-us/customizations/pyqt-mvc.json`
- **Perfil FastAPI:** `skills/implement-us/customizations/fastapi-rest.json`
- **PEP 8:** https://peps.python.org/pep-0008/
- **PEP 517/518:** https://peps.python.org/pep-0517/

---

**Ticket completado exitosamente.** ✅

El perfil `generic-python.json` está listo como fallback universal para cualquier proyecto Python.
