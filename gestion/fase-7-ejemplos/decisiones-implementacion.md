# Decisiones de Implementación - Fase 7: Ejemplos por Stack

**Fecha:** 2026-02-16
**Ticket:** TICKET-052
**Responsable:** Claude Code

---

## 📋 Resumen Ejecutivo

Este documento registra las decisiones arquitectónicas y de implementación para los tutoriales de ejemplo del Claude Dev Kit.

---

## 1. Estructura de Tutoriales

### Decisión: Template Unificado

**Opción Elegida:** Usar un template base (`docs/examples/TEMPLATE.md`) con placeholders para customización por stack.

**Alternativas Consideradas:**
- ❌ Templates independientes por stack (duplicación excesiva)
- ❌ Template minimalista (falta de guía clara)
- ✅ **Template completo con placeholders** (balance ideal)

**Justificación:**
- Mantiene consistencia entre tutoriales
- Facilita actualizaciones globales
- Los placeholders permiten personalización específica del stack
- Secciones obligatorias aseguran completitud

**Placeholders Definidos:**
```
{STACK_NAME}          # Nombre del stack (PyQt6, FastAPI, etc.)
{PROFILE_ID}          # ID del perfil (pyqt-mvc, fastapi-rest, etc.)
{US_TITLE}            # Título de la historia de usuario
{PROJECT_NAME}        # Nombre del proyecto de ejemplo
{ARCHITECTURE_PATTERN} # MVC, Layered, MVT, etc.
{TEST_FRAMEWORK}      # pytest, pytest-qt, pytest-asyncio, etc.
{MAIN_MODULE}         # Nombre del módulo principal
{COVERAGE_THRESHOLD}  # Umbral de cobertura (85-95%)
{PYLINT_THRESHOLD}    # Umbral de Pylint (8.0-9.0)
```

---

## 2. Código de Ejemplo

### Decisión: Enfoque Híbrido (Inline + Archivos)

**Opción Elegida:** Combinar código inline en tutoriales con archivos ejecutables completos.

**Alternativas Consideradas:**
- ❌ Solo código inline (no ejecutable fácilmente)
- ❌ Solo archivos externos (tutorial menos didáctico)
- ✅ **Híbrido: Inline + Archivos** (mejor experiencia)

**Justificación:**
- **Código Inline:** Muestra fragmentos clave con explicación contextual
- **Archivos Completos:** Permiten copiar/pegar y ejecutar inmediatamente
- Usuarios pueden elegir su método preferido de aprendizaje

**Estructura de Archivos:**

```
examples/
├── code/
│   ├── pyqt-mvc-calculator/
│   │   ├── app/
│   │   ├── tests/
│   │   ├── requirements.txt
│   │   └── README.md
│   ├── fastapi-todo-api/
│   │   ├── app/
│   │   ├── tests/
│   │   ├── requirements.txt
│   │   └── README.md
│   ├── flask-rest-contacts/
│   ├── flask-webapp-blog/
│   └── generic-python-csv-tool/
└── README.md
```

**Ventajas:**
- ✅ Tutorial legible y educativo (inline)
- ✅ Código verificable y ejecutable (archivos)
- ✅ Facilita testing de los tutoriales
- ✅ Usuarios pueden clonar y modificar

---

## 3. Screenshots y Output

### Decisión: Screenshots Selectivos + Output de Terminal

**Opción Elegida:** Screenshots solo para PyQt (GUI), output de terminal para el resto.

**Alternativas Consideradas:**
- ❌ Screenshots para todos (innecesario para APIs/CLI)
- ❌ Sin screenshots (PyQt necesita visualización)
- ✅ **Screenshots selectivos según necesidad**

**Estrategia por Stack:**

| Stack | Screenshots | Output Terminal | Archivos Generados |
|-------|-------------|-----------------|-------------------|
| **PyQt-MVC** | ✅ Sí (UI del calculator) | ✅ Sí (pytest) | ✅ Sí (BDD, plans) |
| **FastAPI-REST** | ❌ No | ✅ Sí (uvicorn, pytest, curl) | ✅ Sí (OpenAPI JSON) |
| **Flask-REST** | ❌ No | ✅ Sí (flask run, pytest, curl) | ✅ Sí (blueprints) |
| **Flask-WebApp** | 🟡 Opcional (home page) | ✅ Sí (flask run, pytest) | ✅ Sí (templates) |
| **Generic-Python** | ❌ No | ✅ Sí (CLI output, pytest) | ✅ Sí (CSV files) |

**Formato de Output de Terminal:**

```bash
# Comando
$ pytest tests/ -v

# Output esperado (bloques de código)
============================= test session starts ==============================
collected 15 items

tests/test_calculator.py::test_add PASSED                                [ 6%]
tests/test_calculator.py::test_subtract PASSED                           [13%]
...
============================== 15 passed in 0.45s ==============================
```

**Ventajas:**
- Muestra exactamente qué esperar
- Facilita troubleshooting (comparar output)
- No requiere herramientas de captura de pantalla para la mayoría

---

## 4. Historias de Usuario

### Decisión: Historias Realistas y Acotadas

**Criterios de Selección:**
- ✅ Completables en < 60 minutos
- ✅ Representativas del stack
- ✅ Casos de uso comunes
- ✅ Alcance limitado pero funcional

**Historias Definidas:**

#### PyQt-MVC: Calculadora Simple

```gherkin
Como usuario de escritorio
Quiero una calculadora simple para hacer operaciones básicas
Para realizar cálculos rápidos sin abrir otra aplicación
```

**Alcance:**
- UI con botones numéricos y operaciones (+, -, *, /)
- Display de resultados
- Lógica en Modelo, UI en Vista, coordinación en Controller
- Tests con pytest-qt

**Componentes:**
- `MainWindow` (Vista)
- `CalculatorController` (Controlador)
- `CalculatorModel` (Modelo)

---

#### FastAPI-REST: API de Tareas (TODO)

```gherkin
Como developer
Quiero una API REST de tareas para gestionar mi trabajo
Para integrar con aplicaciones frontend o CLI
```

**Alcance:**
- Endpoints: GET /tasks, POST /tasks, PUT /tasks/{id}, DELETE /tasks/{id}
- Validación con Pydantic models
- Documentación automática con Swagger/ReDoc
- Tests con pytest-asyncio

**Componentes:**
- `TaskModel` (Pydantic)
- `TaskService` (Lógica de negocio)
- `task_router.py` (Endpoints)
- In-memory storage (simplificado)

---

#### Flask-REST: API de Contactos

```gherkin
Como developer
Quiero una API de contactos para mi aplicación
Para gestionar información de contactos (nombre, email, teléfono)
```

**Alcance:**
- Endpoints CRUD: /contacts
- Blueprints para organización
- JSON responses con error handling
- Tests con pytest + Flask test client

**Componentes:**
- `Contact` (Dataclass/Model)
- `ContactService` (Lógica)
- `contacts_blueprint` (Rutas)
- In-memory storage

---

#### Flask-WebApp: Blog Simple

```gherkin
Como blogger
Quiero un blog simple para publicar artículos
Para compartir contenido con lectores
```

**Alcance:**
- Páginas: Home (lista de posts), New Post, View Post
- Templates Jinja2 con layout base
- Formularios para crear posts
- Navegación entre páginas

**Componentes:**
- `Post` (Modelo)
- `blog_blueprint` (Rutas)
- Templates: `base.html`, `home.html`, `new_post.html`, `view_post.html`
- In-memory storage

---

#### Generic-Python: CLI Tool para CSV

```gherkin
Como developer
Quiero una utilidad CLI para manipular archivos CSV
Para automatizar tareas comunes con datos tabulares
```

**Alcance:**
- Comandos: `convert`, `filter`, `merge`
- Argparse para CLI
- File I/O con csv module
- Tabla de output en terminal

**Componentes:**
- `cli.py` (Entry point)
- `csv_processor.py` (Lógica)
- `formatters.py` (Output)
- Tests con fixtures de archivos

---

## 5. Checklist de Validación

### Decisión: Checklist Estandarizado para Todos los Tutoriales

**Checklist Obligatorio por Tutorial:**

#### ✅ Contenido del Tutorial

- [ ] **Introducción clara:** Explica qué se va a construir
- [ ] **Requisitos previos:** Software, conocimientos, verificación
- [ ] **Historia de usuario:** Formato Gherkin con alcance
- [ ] **Setup del proyecto:** Comandos paso a paso
- [ ] **Instalación framework:** Instrucciones del instalador
- [ ] **10 fases documentadas:** Todas las fases con ejemplos
- [ ] **Validación final:** Checklist completo
- [ ] **Troubleshooting:** Problemas comunes + soluciones
- [ ] **Próximos pasos:** Guía para ampliar
- [ ] **Recursos:** Links a docs relevantes

#### ✅ Código Ejecutable

- [ ] **Estructura de proyecto:** Archivos en `examples/code/{stack}/`
- [ ] **Requirements.txt:** Dependencias especificadas
- [ ] **README.md:** Instrucciones de ejecución
- [ ] **Tests incluidos:** Unitarios, integración, BDD
- [ ] **Código ejecuta sin errores:** Validado localmente
- [ ] **Tests pasan al 100%:** pytest verde

#### ✅ Calidad

- [ ] **Tutorial legible:** Lenguaje claro, bien estructurado
- [ ] **Código de calidad:** Sigue convenciones del stack
- [ ] **Ejemplos realistas:** Casos de uso comunes
- [ ] **Tiempo validado:** Completable en < 60 min
- [ ] **Links funcionando:** Todos los links internos válidos
- [ ] **Formato consistente:** Sigue TEMPLATE.md

#### ✅ Adaptación al Stack

- [ ] **Patrón arquitectónico correcto:** MVC, Layered, etc.
- [ ] **Herramientas del stack:** pytest-qt, uvicorn, etc.
- [ ] **Convenciones respetadas:** Naming, estructura, etc.
- [ ] **Recursos específicos:** Links a docs del stack

---

## 6. Plan de Implementación

### Orden de Ejecución de Tickets

**Secuencia Recomendada:**

1. **TICKET-052:** Análisis y planificación ✅ (Este ticket)
2. **TICKET-053:** PyQt-MVC (más complejo - GUI)
3. **TICKET-054:** FastAPI-REST (APIs modernas)
4. **TICKET-055:** Flask-REST (APIs simples)
5. **TICKET-056:** Flask-WebApp (fullstack)
6. **TICKET-057:** Generic-Python (más simple)
7. **TICKET-058:** Validación de todos los ejemplos

**Justificación del Orden:**
- PyQt primero (más complejo, establece precedente)
- FastAPI antes de Flask (popularidad y complejidad)
- Flask-REST antes de Flask-WebApp (APIs más simples que fullstack)
- Generic último (más simple, valida el framework sin stack específico)

### Tiempo Estimado por Ticket

| Ticket | Tarea | Estimado | Acumulado |
|--------|-------|----------|-----------|
| 052 | Análisis y planificación | 1h | 1h |
| 053 | PyQt-MVC | 3h | 4h |
| 054 | FastAPI-REST | 2.5h | 6.5h |
| 055 | Flask-REST | 2.5h | 9h |
| 056 | Flask-WebApp | 2.5h | 11.5h |
| 057 | Generic-Python | 2h | 13.5h |
| 058 | Validación | 1.5h | 15h |

**Total:** 15 horas (~2 días de trabajo)

---

## 7. Criterios de Aceptación Globales

### Para la Fase 7 Completa

- [ ] **5 tutoriales completos:** Uno por cada perfil
- [ ] **Código ejecutable:** 5 proyectos en `examples/code/`
- [ ] **Documentación clara:** Siguiendo TEMPLATE.md
- [ ] **Validación pasando:** Checklist completo por cada uno
- [ ] **Tiempo validado:** Cada tutorial < 60 min
- [ ] **Links funcionando:** Navegación Wiki correcta
- [ ] **README principal:** `examples/README.md` con índice

---

## 8. Riesgos y Mitigación

### Riesgo 1: Tutoriales Demasiado Largos

**Probabilidad:** Media
**Impacto:** Alto (usuarios no completan)

**Mitigación:**
- Limitar alcance estrictamente
- Timeboxing: validar que cada uno < 60 min
- Usar historias de usuario muy acotadas

### Riesgo 2: Código No Ejecutable

**Probabilidad:** Baja
**Impacto:** Crítico (pérdida de confianza)

**Mitigación:**
- Validar código localmente antes de commit
- Incluir tests automáticos
- CI/CD para validar ejemplos

### Riesgo 3: Inconsistencia Entre Tutoriales

**Probabilidad:** Media
**Impacto:** Medio (confusión)

**Mitigación:**
- Usar TEMPLATE.md obligatoriamente
- Checklist de validación estandarizado
- Revisión cruzada en TICKET-058

---

## 9. Próximos Pasos Inmediatos

1. ✅ **Crear template base** (TEMPLATE.md) - HECHO
2. ✅ **Documentar decisiones** (este archivo) - HECHO
3. ⬜ **Actualizar sprint-4.md** con historias de usuario detalladas
4. ⬜ **Actualizar tickets 053-057** con referencias a TEMPLATE.md
5. ⬜ **Marcar TICKET-052 como completado**
6. ⬜ **Iniciar TICKET-053** (PyQt-MVC)

---

## 10. Referencias

- **TEMPLATE.md:** `docs/examples/TEMPLATE.md`
- **Sprint 4:** `gestion/fase-7-ejemplos/sprint-4.md`
- **Tickets:** `gestion/fase-7-ejemplos/tickets/TICKET-0XX-*.md`
- **Perfiles:** `skills/implement-us/customizations/*.json`

---

**Documento Creado:** 2026-02-16
**Última Actualización:** 2026-02-16
**Estado:** Aprobado para Implementación
