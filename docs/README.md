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
1. [Índice principal](Documentation-Index) - Visión general
2. [Getting Started](user-Getting-Started) - Primera experiencia en <15 minutos
3. [Instalación](user-Installation) - Setup detallado

Si ya tienes el framework instalado:
- [Skill implement-us](user-skills-Implement-Us) - Implementar historias de usuario
- [Sistema de tracking](user-tracking-User-Guide) - Tracking de tiempo automático
- [Personalización](user-Customization) - Adaptar a tu stack tecnológico
- [Configuración](user-Configuration) - Referencia completa de opciones

### Para Desarrolladores del Framework

Si quieres **contribuir** o **crear skills custom**:
- [Creando Skills](developer-contributing-Creating-Skills) - Guía completa para crear skills
- [Sistema de Templates](developer-architecture-Template-System) - Variables y snippets
- [Tracking - Arquitectura](developer-architecture-Tracking) - Diseño del sistema

### Para Mantenedores del Proyecto

Documentación interna y análisis:
- [developer/architecture/](developer-architecture) - Documentación técnica del proyecto

---

## 📋 Categorías de Documentación

### 1. Documentación de Usuario 🚀

**Audiencia:** Desarrolladores que usan el framework
**Propósito:** Guías de uso, tutoriales, referencias

**Documentos:**
- [user/index.md](Documentation-Index) - Índice principal con navegación
- [user/getting-started.md](user-Getting-Started) - Guía de inicio rápido (<15 min)
- [user/installation.md](user-Installation) - Instalación detallada
- [user/customization.md](user-Customization) - Personalización del framework
- [user/configuration.md](user-Configuration) - Referencia de configuración
- [user/skills/implement-us.md](user-skills-Implement-Us) - Uso del skill principal
- [user/tracking/user-guide.md](user-tracking-User-Guide) - Guía de tracking de tiempo
- [user/tracking/examples.md](user-tracking-Examples) - Ejemplos de tracking

### 2. Documentación Técnica 🛠️

**Audiencia:** Desarrolladores del framework, contributors
**Propósito:** Arquitectura, especificaciones, extensibilidad

**Documentos:**
- [developer/contributing/creating-skills.md](developer-contributing-Creating-Skills) - Crear skills personalizados
- [developer/architecture/template-system.md](developer-architecture-Template-System) - Sistema de templates
- [developer/architecture/tracking.md](developer-architecture-Tracking) - Arquitectura del tracking
- [developer/architecture/session-memory.md](developer-architecture-Session-Memory) - Sistema de sesiones

### 3. Tutoriales por Stack 📚

**Audiencia:** Usuarios aprendiendo con proyectos reales
**Propósito:** Ejemplos completos end-to-end

**Documentos:**
- [examples/pyqt-project.md](examples-Pyqt-Project) - Proyecto PyQt-MVC completo
- [examples/fastapi-project.md](examples-Fastapi-Project) - API REST con FastAPI
- [examples/flask-rest-project.md](examples-Flask-Rest-Project) - API REST con Flask
- [examples/flask-webapp-project.md](examples-Flask-Webapp-Project) - WebApp con Flask
- [examples/generic-python.md](examples-Generic-Python) - Proyecto Python genérico

---

## 📝 Creando Nueva Documentación

Si vas a crear un nuevo documento:

1. **Usa la plantilla estándar:**
   ```bash
   cp docs/developer/contributing/template.md docs/mi-nuevo-doc.md
   ```

2. **Sigue las convenciones:**
   - Ver [template.md](developer-contributing-Template) para estructura

3. **Incluye siempre:**
   - Tabla de contenidos
   - Prerequisitos claros
   - Ejemplos ejecutables
   - Sección de troubleshooting
   - Navegación (anterior/siguiente/índice)

4. **Actualiza el índice:**
   - Agregar enlace en [user/index.md](Documentation-Index)
   - Agregar entrada en este README

---

## 🔗 Enlaces Rápidos

### Documentos Principales
- [📘 Índice Principal](Documentation-Index)
- [🚀 Getting Started](user-Getting-Started)
- [🛠️ Skill implement-us](user-skills-Implement-Us)

### Recursos Técnicos
- [📝 Sistema de Templates](developer-architecture-Template-System)
- [⏱️ Tracking - Arquitectura](developer-architecture-Tracking)

### Proyecto
- [README Principal](../README.md)
- [Plan del Proyecto](../PROJECT_PLAN_claude-dev-kit.md)
- [Gestión de Tareas](../gestion/)
