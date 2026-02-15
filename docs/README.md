# Documentación - Claude Dev Kit

Este directorio contiene toda la documentación del framework Claude Dev Kit, organizada por tipo de audiencia y propósito.

---

## 📂 Estructura

```
docs/
├── index.md                    # 📘 Índice principal (punto de entrada)
├── TEMPLATE.md                 # Plantilla estándar para nuevos documentos
│
├── getting-started.md          # 🚀 Guía de inicio rápido
├── installation.md             # 📦 Instalación detallada
├── customization.md            # 🎨 Personalización del framework
├── configuration.md            # ⚙️ Referencia de configuración
│
├── skills/                     # 🛠️ Documentación de skills
│   ├── implement-us.md         # Skill principal para implementar US
│   └── creating-skills.md      # Guía para crear skills custom
│
├── templates/                  # 📝 Sistema de templates
│   └── template-system.md      # Arquitectura y uso de templates
│
├── tracking/                   # ⏱️ Sistema de tracking de tiempo
│   ├── user-guide.md           # Guía de usuario del tracking
│   ├── architecture.md         # Arquitectura técnica del sistema
│   └── examples.md             # Ejemplos de uso
│
├── examples/                   # 📚 Tutoriales por stack (Fase 7)
│   ├── pyqt-project.md
│   ├── fastapi-project.md
│   ├── flask-rest-project.md
│   ├── flask-webapp-project.md
│   └── generic-python.md
│
└── internal/                   # 🔒 Documentación interna
    ├── analysis/               # Análisis de tickets
    │   └── TICKET-043-doc-structure.md
    └── session-memory.md       # Sistema de sesiones (interno)
```

---

## 🎯 Guía de Uso

### Para Usuarios del Framework

Si eres **nuevo**, comienza aquí:
1. [Índice principal](./index.md) - Visión general
2. [Getting Started](./getting-started.md) - Primera experiencia en <15 minutos
3. [Instalación](./installation.md) - Setup detallado

Si ya tienes el framework instalado:
- [Skill implement-us](./skills/implement-us.md) - Implementar historias de usuario
- [Sistema de tracking](./tracking/user-guide.md) - Tracking de tiempo automático
- [Personalización](./customization.md) - Adaptar a tu stack tecnológico
- [Configuración](./configuration.md) - Referencia completa de opciones

### Para Desarrolladores del Framework

Si quieres **contribuir** o **crear skills custom**:
- [Creando Skills](./skills/creating-skills.md) - Guía completa para crear skills
- [Sistema de Templates](./templates/template-system.md) - Variables y snippets
- [Tracking - Arquitectura](./tracking/architecture.md) - Diseño del sistema

### Para Mantenedores del Proyecto

Documentación interna y análisis:
- [internal/](./internal/) - Documentación interna del proyecto
- [internal/analysis/](./internal/analysis/) - Análisis de tickets

---

## 📋 Categorías de Documentación

### 1. Documentación de Usuario 🚀
**Audiencia:** Desarrolladores que usan el framework
**Propósito:** Guías de uso, tutoriales, referencias

| Documento | Descripción | Estado |
|-----------|-------------|--------|
| **index.md** | Índice principal con navegación | 📋 Fase 6 |
| **getting-started.md** | Guía de inicio rápido (<15 min) | 📋 Fase 6 |
| **installation.md** | Instalación detallada | 📋 Fase 6 |
| **customization.md** | Personalización del framework | 📋 Fase 6 |
| **configuration.md** | Referencia de configuración | 📋 Fase 6 |
| **skills/implement-us.md** | Uso del skill principal | 📋 Fase 6 |
| **tracking/user-guide.md** | Guía de tracking de tiempo | ✅ Completo |
| **tracking/examples.md** | Ejemplos de tracking | ✅ Completo |

### 2. Documentación Técnica 🛠️
**Audiencia:** Desarrolladores del framework, contributors
**Propósito:** Arquitectura, especificaciones, extensibilidad

| Documento | Descripción | Estado |
|-----------|-------------|--------|
| **skills/creating-skills.md** | Crear skills personalizados | 📋 Fase 6 |
| **templates/template-system.md** | Sistema de templates | ✅ Completo |
| **tracking/architecture.md** | Arquitectura del tracking | ✅ Completo |

### 3. Tutoriales por Stack 📚
**Audiencia:** Usuarios aprendiendo con proyectos reales
**Propósito:** Ejemplos completos end-to-end

| Documento | Descripción | Estado |
|-----------|-------------|--------|
| **examples/pyqt-project.md** | Proyecto PyQt-MVC completo | ⏳ Fase 7 |
| **examples/fastapi-project.md** | API REST con FastAPI | ⏳ Fase 7 |
| **examples/flask-rest-project.md** | API REST con Flask | ⏳ Fase 7 |
| **examples/flask-webapp-project.md** | WebApp con Flask | ⏳ Fase 7 |
| **examples/generic-python.md** | Proyecto Python genérico | ⏳ Fase 7 |

### 4. Documentación Interna 🔒
**Audiencia:** Mantenedores del proyecto
**Propósito:** Análisis, decisiones de desarrollo

| Documento | Descripción | Estado |
|-----------|-------------|--------|
| **internal/analysis/TICKET-043-doc-structure.md** | Análisis de estructura docs/ | ✅ Completo |
| **internal/session-memory.md** | Sistema de sesiones | ✅ Completo |

---

## 📝 Creando Nueva Documentación

Si vas a crear un nuevo documento de usuario:

1. **Usa la plantilla estándar:**
   ```bash
   cp docs/TEMPLATE.md docs/mi-nuevo-doc.md
   ```

2. **Sigue las convenciones:**
   - Ver [TEMPLATE.md](./TEMPLATE.md) para estructura
   - Ver [internal/analysis/TICKET-043-doc-structure.md](./internal/analysis/TICKET-043-doc-structure.md) para convenciones

3. **Incluye siempre:**
   - Tabla de contenidos
   - Prerequisitos claros
   - Ejemplos ejecutables
   - Sección de troubleshooting
   - Navegación (anterior/siguiente/índice)

4. **Actualiza el índice:**
   - Agregar enlace en [index.md](./index.md)
   - Agregar entrada en este README

---

## 🔗 Enlaces Rápidos

### Documentos Principales
- [📘 Índice Principal](./index.md)
- [🚀 Getting Started](./getting-started.md)
- [🛠️ Skill implement-us](./skills/implement-us.md)

### Recursos Técnicos
- [📝 Sistema de Templates](./templates/template-system.md)
- [⏱️ Tracking - Arquitectura](./tracking/architecture.md)

### Proyecto
- [README Principal](../README.md)
- [Plan del Proyecto](../PROJECT_PLAN_claude-dev-kit.md)
- [Gestión de Tareas](../gestion/)

---

## 🔄 Evolución

**Última Actualización:** 2026-02-15

**Cambios Recientes:**
- **2026-02-15 (TICKET-043):** Reestructuración completa
  - Nueva organización por tipo de audiencia
  - Creados directorios: skills/, examples/, internal/
  - Movida documentación interna a internal/
  - Creada plantilla estándar (TEMPLATE.md)
  - Definidas convenciones de formato

**Próximos Pasos:**
- **Fase 6:** Crear toda la documentación de usuario (TICKET-044 a TICKET-051)
- **Fase 7:** Crear tutoriales por stack en examples/

---

**Estado Actual:** Sprint 3 - Fase 6 (Documentación General)
**Progreso:** 1/9 tickets completados (TICKET-043 ✅)
