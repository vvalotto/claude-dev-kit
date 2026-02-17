# TICKET-065: Propuesta y Actualización de Wiki 📚

**Fase:** 9 - Release v1.0
**Sprint:** 6
**Estado:** ⏳ Pendiente
**Prioridad:** Alta
**Estimación:** 2 horas
**Asignado a:** Claude Code

---

## 🎯 Objetivo

Analizar el estado actual del workflow de sincronización de la Wiki, identificar gaps (especialmente `docs/examples/` que actualmente **no se sincroniza**), proponer y aplicar la estructura de navegación definitiva para la GitHub Wiki v1.0.

---

## 📋 Estado Actual del Workflow

El workflow `sync-wiki.yml` sincroniza actualmente:

| Directorio origen | Prefijo en Wiki |
|-------------------|-----------------|
| `docs/README.md` | `Home.md` |
| `docs/user/index.md` | `Documentation-Index.md` |
| `docs/user/*.md` | `user-{PascalCase}.md` |
| `docs/user/skills/*.md` | `user-skills-{PascalCase}.md` |
| `docs/user/tracking/*.md` | `user-tracking-{PascalCase}.md` |
| `docs/developer/architecture/*.md` | `developer-architecture-{PascalCase}.md` |
| `docs/developer/contributing/*.md` | `developer-contributing-{PascalCase}.md` |

**❌ NO sincronizado:** `docs/examples/` — 5 tutoriales completos (PyQt, FastAPI, Flask REST, Flask WebApp, CLI)

---

## 📋 Tareas

### 1. Análisis y Propuesta de Estructura Wiki (45 min)

Decidir qué documentos deben estar en la Wiki y con qué estructura de navegación.

**Pregunta clave:** ¿Los tutoriales de ejemplos deben estar en la Wiki?

**Argumentos a favor:**
- Son el contenido más valioso para nuevos usuarios
- Demuestran el framework en acción con código real
- Permiten que usuarios sin acceso al repo vean tutoriales completos

**Argumentos en contra:**
- Son documentos muy largos (~2,000-3,000 líneas cada uno)
- Pueden quedar desactualizados fácilmente
- La Wiki ya cubre instalación y uso básico

**Decisión recomendada:** Sincronizar `docs/examples/` con prefijo `examples-`. Cada tutorial es un punto de entrada importante para nuevos usuarios.

**Propuesta de estructura completa de la Wiki v1.0:**

```
Wiki GitHub - Claude Dev Kit v1.0
├── Home.md                            ← docs/README.md
├── Documentation-Index.md             ← docs/user/index.md
│
├── [Usuarios]
│   ├── user-GettingStarted.md         ← docs/user/getting-started.md
│   ├── user-Installation.md           ← docs/user/installation.md
│   ├── user-Customization.md          ← docs/user/customization.md
│   ├── user-Configuration.md          ← docs/user/configuration.md
│   ├── user-skills-ImplementUs.md     ← docs/user/skills/implement-us.md
│   ├── user-tracking-UserGuide.md     ← docs/user/tracking/user-guide.md
│   └── user-tracking-Examples.md      ← docs/user/tracking/examples.md
│
├── [Ejemplos] ← NUEVO en v1.0
│   ├── examples-PyqtProject.md        ← docs/examples/pyqt-project.md
│   ├── examples-FastapiProject.md     ← docs/examples/fastapi-project.md
│   ├── examples-FlaskRestApiProject.md ← docs/examples/flask-rest-api-project.md
│   ├── examples-FlaskWebappProject.md ← docs/examples/flask-webapp-project.md
│   └── examples-GenericPython.md      ← docs/examples/generic-python.md
│
└── [Desarrolladores]
    ├── developer-architecture-TemplateSystem.md
    ├── developer-architecture-Tracking.md
    ├── developer-architecture-SessionMemory.md
    ├── developer-contributing-CreatingSkills.md
    └── developer-contributing-Template.md
```

### 2. Auditoría de Links en Documentos de Wiki (30 min)

Los documentos en `docs/` usan links en formato Wiki (sin extensión `.md`). Verificar que todos los links en documentos que se sincronizan a la Wiki usan el formato correcto:

**Formato Wiki correcto:**
```markdown
[Guía de Inicio Rápido](user-Getting-Started)       ← ✅ Sin .md
[Skill implement-us](user-skills-Implement-Us)       ← ✅ PascalCase con prefijo
```

**Formato incorrecto (solo válido en GitHub, no en Wiki):**
```markdown
[Guía de Inicio Rápido](user/getting-started.md)    ← ❌ Con .md y path
[Skill implement-us](skills/implement-us)            ← ❌ Sin prefijo
```

**Archivos a auditar:**
- [ ] `docs/user/index.md` — Todos sus links
- [ ] `docs/user/getting-started.md` — Links a otras guías
- [ ] `docs/user/installation.md` — Links a customization
- [ ] `docs/user/skills/implement-us.md` — Links a tracking y examples
- [ ] `docs/README.md` — Links al índice y secciones

**Para los nuevos documentos de ejemplos:**
- [ ] Verificar que los links internos en `docs/examples/*.md` usan formato Wiki

### 3. Actualizar `sync-wiki.yml` (30 min)

Agregar la sincronización de `docs/examples/` al workflow:

```yaml
# Agregar después del bloque de developer/contributing/
# Sincronizar examples/
for file in docs/examples/*.md; do
  [ -f "$file" ] || continue
  [ "$(basename "$file")" = "TEMPLATE.md" ] && continue  # excluir template interno

  filename=$(basename "$file" .md)
  pascal_name=$(to_pascal_case "$filename")
  cp "$file" "wiki/examples-${pascal_name}.md"
done
```

**Ajustes adicionales:**
- [ ] Excluir `docs/examples/TEMPLATE.md` (es para uso interno, no para usuarios)
- [ ] Verificar que `docs/user/index.md` ya referencia los tutoriales de ejemplos

### 4. Actualizar Índice de Documentación (15 min)

`docs/user/index.md` debe incluir una sección de Ejemplos que apunte a los tutoriales con formato Wiki:

```markdown
## 📖 Ejemplos por Stack

Proyectos completos generados con el framework:

- **[PyQt Calculator](examples-PyqtProject)** — Calculadora MVC con PyQt6
- **[FastAPI TODO API](examples-FastapiProject)** — REST API con FastAPI y arquitectura en capas
- **[Flask Contacts API](examples-FlaskRestApiProject)** — API de contactos con Flask
- **[Flask Blog App](examples-FlaskWebappProject)** — Blog fullstack con Jinja2
- **[CSV Tool CLI](examples-GenericPython)** — Herramienta CLI genérica con stdlib
```

---

## 📤 Output

1. **`sync-wiki.yml` actualizado** — Incluye sincronización de `docs/examples/`
2. **`docs/user/index.md` actualizado** — Sección de ejemplos con links correctos
3. **Links corregidos** en documentos que se sincronizan a la Wiki (si se encontraron issues)
4. Notas en `REVIEW-REPORT.md` de TICKET-064 sobre los cambios aplicados

---

## 🎯 Criterios de Aceptación

- [ ] **`docs/examples/` sincronizado a la Wiki** — Workflow actualizado y verificado
- [ ] **`TEMPLATE.md` excluido** — No se sincroniza a la Wiki
- [ ] **`docs/user/index.md` incluye sección Ejemplos** con links correctos en formato Wiki
- [ ] **Todos los links internos en formato Wiki** — Sin `.md`, con prefijos correctos
- [ ] **Workflow sin errores de sintaxis** — `yaml` válido

---

## 🔗 Dependencias

- **Depende de:** TICKET-064 (revisión de docs, puede generar correcciones de links)
- **Bloquea a:** TICKET-068 (el Release debe publicar el workflow ya actualizado)

---

## 📝 Notas Técnicas

### Mapeo de nombres: archivo → Wiki

| Archivo | Prefijo | Resultado en Wiki |
|---------|---------|-------------------|
| `docs/examples/pyqt-project.md` | `examples-` | `examples-PyqtProject.md` |
| `docs/examples/fastapi-project.md` | `examples-` | `examples-FastapiProject.md` |
| `docs/examples/flask-rest-api-project.md` | `examples-` | `examples-FlaskRestApiProject.md` |
| `docs/examples/flask-webapp-project.md` | `examples-` | `examples-FlaskWebappProject.md` |
| `docs/examples/generic-python.md` | `examples-` | `examples-GenericPython.md` |

### Conversión kebab-case → PascalCase de la función `to_pascal_case`

La función en el workflow convierte `flask-rest-api-project` → `FlaskRestApiProject`. Verificar que genera los nombres esperados antes de hacer commit.

### Verificación manual del workflow

Antes del commit, probar localmente la función de conversión:

```bash
to_pascal_case() {
  echo "$1" | sed -E 's/(^|-)([a-z])/\U\2/g'
}
to_pascal_case "flask-rest-api-project"  # → FlaskRestApiProject
to_pascal_case "generic-python"           # → GenericPython
```

---

**Creado:** 2026-02-17
**Depende de:** TICKET-064
**Bloquea a:** TICKET-068
