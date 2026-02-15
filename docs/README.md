# Documentación - Claude Dev Kit

Este directorio contiene toda la documentación del framework Claude Dev Kit, organizada por tipo de audiencia y propósito.

---

## 📂 Estructura

```
docs/
├── README.md                        # Este archivo
│
├── user/                            # 📘 Documentación de usuario
│   ├── index.md                     # Índice principal (punto de entrada)
│   ├── getting-started.md           # 🚀 Guía de inicio rápido
│   ├── installation.md              # 📦 Instalación detallada
│   ├── customization.md             # 🎨 Personalización del framework
│   ├── configuration.md             # ⚙️ Referencia de configuración
│   │
│   ├── skills/                      # 🛠️ Skills del framework
│   │   └── implement-us.md          # Skill principal para implementar US
│   │
│   └── tracking/                    # ⏱️ Sistema de tracking
│       ├── user-guide.md            # Guía de usuario del tracking
│       └── examples.md              # Ejemplos de uso
│
├── developer/                       # 🏗️ Documentación técnica
│   ├── architecture/                # Arquitectura del sistema
│   │   ├── template-system.md       # Sistema de templates
│   │   ├── tracking.md              # Arquitectura del tracking
│   │   └── session-memory.md        # Sistema de sesiones
│   │
│   └── contributing/                # Guías de contribución
│       ├── creating-skills.md       # Crear skills custom
│       └── template.md              # Plantilla estándar para nuevos documentos
│
└── examples/                        # 📚 Tutoriales por stack
    ├── pyqt-project.md
    ├── fastapi-project.md
    ├── flask-rest-project.md
    ├── flask-webapp-project.md
    └── generic-python.md
```

---

## 🎯 Guía de Uso

### Para Usuarios del Framework

Si eres **nuevo**, comienza aquí:
1. [Índice principal](./user/index.md) - Visión general
2. [Getting Started](./user/getting-started.md) - Primera experiencia en <15 minutos
3. [Instalación](./user/installation.md) - Setup detallado

Si ya tienes el framework instalado:
- [Skill implement-us](./user/skills/implement-us.md) - Implementar historias de usuario
- [Sistema de tracking](./user/tracking/user-guide.md) - Tracking de tiempo automático
- [Personalización](./user/customization.md) - Adaptar a tu stack tecnológico
- [Configuración](./user/configuration.md) - Referencia completa de opciones

### Para Desarrolladores del Framework

Si quieres **contribuir** o **crear skills custom**:
- [Creando Skills](./developer/contributing/creating-skills.md) - Guía completa para crear skills
- [Sistema de Templates](./developer/architecture/template-system.md) - Variables y snippets
- [Tracking - Arquitectura](./developer/architecture/tracking.md) - Diseño del sistema

### Para Mantenedores del Proyecto

Documentación interna y análisis:
- [developer/architecture/](./developer/architecture/) - Documentación técnica del proyecto

---

## 📋 Categorías de Documentación

### 1. Documentación de Usuario 🚀

**Audiencia:** Desarrolladores que usan el framework
**Propósito:** Guías de uso, tutoriales, referencias

**Documentos:**
- [user/index.md](./user/index.md) - Índice principal con navegación
- [user/getting-started.md](./user/getting-started.md) - Guía de inicio rápido (<15 min)
- [user/installation.md](./user/installation.md) - Instalación detallada
- [user/customization.md](./user/customization.md) - Personalización del framework
- [user/configuration.md](./user/configuration.md) - Referencia de configuración
- [user/skills/implement-us.md](./user/skills/implement-us.md) - Uso del skill principal
- [user/tracking/user-guide.md](./user/tracking/user-guide.md) - Guía de tracking de tiempo
- [user/tracking/examples.md](./user/tracking/examples.md) - Ejemplos de tracking

### 2. Documentación Técnica 🛠️

**Audiencia:** Desarrolladores del framework, contributors
**Propósito:** Arquitectura, especificaciones, extensibilidad

**Documentos:**
- [developer/contributing/creating-skills.md](./developer/contributing/creating-skills.md) - Crear skills personalizados
- [developer/architecture/template-system.md](./developer/architecture/template-system.md) - Sistema de templates
- [developer/architecture/tracking.md](./developer/architecture/tracking.md) - Arquitectura del tracking
- [developer/architecture/session-memory.md](./developer/architecture/session-memory.md) - Sistema de sesiones

### 3. Tutoriales por Stack 📚

**Audiencia:** Usuarios aprendiendo con proyectos reales
**Propósito:** Ejemplos completos end-to-end

**Documentos:**
- [examples/pyqt-project.md](./examples/pyqt-project.md) - Proyecto PyQt-MVC completo
- [examples/fastapi-project.md](./examples/fastapi-project.md) - API REST con FastAPI
- [examples/flask-rest-project.md](./examples/flask-rest-project.md) - API REST con Flask
- [examples/flask-webapp-project.md](./examples/flask-webapp-project.md) - WebApp con Flask
- [examples/generic-python.md](./examples/generic-python.md) - Proyecto Python genérico

---

## 📝 Creando Nueva Documentación

Si vas a crear un nuevo documento:

1. **Usa la plantilla estándar:**
   ```bash
   cp docs/developer/contributing/template.md docs/mi-nuevo-doc.md
   ```

2. **Sigue las convenciones:**
   - Ver [template.md](./developer/contributing/template.md) para estructura

3. **Incluye siempre:**
   - Tabla de contenidos
   - Prerequisitos claros
   - Ejemplos ejecutables
   - Sección de troubleshooting
   - Navegación (anterior/siguiente/índice)

4. **Actualiza el índice:**
   - Agregar enlace en [user/index.md](./user/index.md)
   - Agregar entrada en este README

---

## 🔗 Enlaces Rápidos

### Documentos Principales
- [📘 Índice Principal](./user/index.md)
- [🚀 Getting Started](./user/getting-started.md)
- [🛠️ Skill implement-us](./user/skills/implement-us.md)

### Recursos Técnicos
- [📝 Sistema de Templates](./developer/architecture/template-system.md)
- [⏱️ Tracking - Arquitectura](./developer/architecture/tracking.md)

### Proyecto
- [README Principal](../README.md)
- [Plan del Proyecto](../PROJECT_PLAN_claude-dev-kit.md)
- [Gestión de Tareas](../gestion/)
