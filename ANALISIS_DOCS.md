# Análisis de Documentos en docs/

**Fecha:** 2026-02-15
**Propósito:** Entender qué documento va dónde y por qué

---

## 📋 Análisis Documento por Documento

| Documento | Audiencia Real | Propósito Real | ¿Ubicación Correcta? |
|-----------|----------------|----------------|---------------------|
| **index.md** | Usuario/Todos | Hub de navegación | ✅ SÍ |
| **README.md** | Desarrollador | Guía de navegación de docs/ | ✅ SÍ |
| **TEMPLATE.md** | Desarrollador | Plantilla para crear docs | ✅ SÍ |
| **getting-started.md** | Usuario final | Tutorial de inicio | ✅ SÍ |
| **installation.md** | Usuario final | Cómo instalar | ✅ SÍ |
| **customization.md** | Usuario avanzado | Cómo personalizar | ✅ SÍ |
| **configuration.md** | Usuario avanzado | Referencia de config | ✅ SÍ |
| **skills/implement-us.md** | Usuario final | Cómo USAR el skill | ✅ SÍ |
| **skills/creating-skills.md** | Desarrollador/Contributor | Cómo CREAR skills | ⚠️ DUDOSO |
| **templates/template-system.md** | Desarrollador/Usuario avanzado | Cómo funcionan templates | ⚠️ DUDOSO |
| **tracking/user-guide.md** | Usuario final | Cómo usar tracking | ✅ SÍ |
| **tracking/examples.md** | Usuario final | Ejemplos de tracking | ✅ SÍ |
| **tracking/architecture.md** | Desarrollador | Arquitectura interna | ❌ NO |
| **internal/session-memory.md** | Desarrollador | Sistema interno | ❌ NO |
| **internal/analysis/TICKET-043...** | Mantenedor | Análisis de trabajo | ❌ NO |

---

## 🔍 Problemas Identificados

### Problema 1: Documentación TÉCNICA mezclada con USUARIO

**Archivos técnicos en docs/:**
- `tracking/architecture.md` → Esto es arquitectura INTERNA
- `templates/template-system.md` → Es MUY técnico (variables, snippets, arquitectura)
- `skills/creating-skills.md` → Para desarrolladores del framework

**¿Por qué es un problema?**
- docs/ debería ser SOLO para usuarios del framework
- La documentación técnica debería estar con el código fuente

---

### Problema 2: docs/internal/ no tiene sentido

**¿Por qué?**
- Si es "internal", ¿por qué está en docs/ que es PÚBLICO?
- docs/ se supone que es documentación de usuario
- "internal" debería estar fuera de docs/

**Contenido de internal/:**
- `session-memory.md` → Arquitectura del sistema de sesiones (TÉCNICO)
- `analysis/TICKET-043...` → Análisis de trabajo (GESTIÓN)

---

### Problema 3: Confusión entre "Técnico" y "Avanzado"

**Hay diferencia entre:**

**Usuario Avanzado:**
- Quiere personalizar el framework
- Necesita entender variables, snippets, configuración
- **Ejemplo:** customization.md, configuration.md

**Desarrollador/Contributor:**
- Quiere EXTENDER o MODIFICAR el framework
- Necesita entender arquitectura interna
- **Ejemplo:** creating-skills.md, architecture.md

**¿Dónde va cada uno?**
- Usuario avanzado → ✅ docs/
- Desarrollador → ❌ NO en docs/

---

## 🎯 Propuesta de Reorganización

### Opción A: Separación Estricta (Recomendada)

```
docs/                              # SOLO documentación de USUARIO
├── index.md                       # Hub
├── getting-started.md             # Usuario básico
├── installation.md                # Usuario básico
├── customization.md               # Usuario avanzado
├── configuration.md               # Usuario avanzado
├── skills/
│   └── implement-us.md            # Cómo USAR el skill
├── templates/
│   └── using-templates.md         # Cómo USAR templates (usuario)
├── tracking/
│   ├── user-guide.md              # Cómo usar
│   └── examples.md                # Ejemplos
└── examples/                      # Tutoriales (Fase 7)

technical/                         # Documentación TÉCNICA (nuevo)
├── README.md                      # Guía de contribución
├── architecture/
│   ├── session-memory.md          # Sistema de sesiones
│   ├── tracking-system.md         # Arquitectura tracking
│   └── template-system.md         # Arquitectura templates
├── contributing/
│   ├── creating-skills.md         # Cómo crear skills
│   ├── coding-standards.md        # Estándares
│   └── testing.md                 # Testing del framework
└── analysis/                      # Análisis de tickets
    └── TICKET-043-doc-structure.md
```

**Ventajas:**
- ✅ Clara separación: Usuario vs Desarrollador
- ✅ docs/ es 100% para usuarios
- ✅ technical/ es para contributors
- ✅ Fácil sincronizar docs/ → Wiki

**Desventajas:**
- ⚠️ Requiere mover varios archivos
- ⚠️ Actualizar muchos enlaces

---

### Opción B: Mantener Todo en docs/ pero CLARAMENTE separado

```
docs/
├── user/                          # Documentación de USUARIO
│   ├── getting-started.md
│   ├── installation.md
│   ├── customization.md
│   └── ...
│
└── developer/                     # Documentación de DESARROLLADOR
    ├── architecture/
    ├── contributing/
    └── ...
```

**Ventajas:**
- ✅ Todo en un lugar
- ✅ Clara separación con subdirectorios

**Desventajas:**
- ❌ Mezcla propósitos diferentes
- ❌ Difícil sincronizar a Wiki (tendría docs técnicos)

---

### Opción C: Híbrida (Pragmática)

```
docs/                              # Documentación de USUARIO
├── [toda la doc de usuario]
├── advanced/                      # Usuario AVANZADO (no técnico)
│   ├── customization.md
│   ├── configuration.md
│   └── templates-usage.md         # Cómo USAR (no arquitectura)
└── contributing/                  # Para CONTRIBUTORS
    └── creating-skills.md         # Link a technical/

technical/                         # Documentación TÉCNICA
├── architecture/
│   ├── session-memory.md
│   ├── tracking-system.md
│   └── template-system.md
└── analysis/
```

**Ventajas:**
- ✅ Balance entre separación y pragmatismo
- ✅ docs/ mayormente para usuarios
- ✅ Fácil sincronizar docs/ → Wiki (excluyendo contributing/)

---

## 🤔 Preguntas para Decidir

### 1. ¿Qué debe ir en docs/?

**A) SOLO usuario final:**
- getting-started, installation, cómo usar skills
- ❌ NO arquitectura interna
- ❌ NO guías de contribución

**B) Usuario + Avanzado:**
- Todo lo anterior
- + customization, configuration (avanzado pero usuario)
- ❌ NO arquitectura interna
- ❌ NO guías de contribución

**C) Usuario + Contributor:**
- Todo lo anterior
- + creating-skills, architecture
- (Mezclado pero todo en un lugar)

### 2. ¿Dónde va la documentación técnica?

**A) Con el código:**
```
skills/implement-us/
├── README.md                 # Arquitectura técnica
└── CONTRIBUTING.md           # Cómo contribuir
```

**B) En directorio technical/:**
```
technical/
├── architecture/
└── contributing/
```

**C) En docs/developer/:**
```
docs/
├── user/
└── developer/
```

### 3. ¿Qué sincronizamos a GitHub Wiki?

**A) Solo docs/ de usuario:**
- getting-started, installation, etc.
- ❌ NO technical/

**B) Todo docs/:**
- Todo lo que esté en docs/
- (Incluyendo técnico si está ahí)

---

## 📌 Mi Recomendación

**Opción A: Separación Estricta**

```
docs/           → Solo usuario (sincronizar a Wiki)
technical/      → Solo desarrollador (no sincronizar)
gestion/        → Solo gestión (no sincronizar)
```

**Razones:**
1. Clara separación de propósitos
2. Fácil sincronización docs/ → Wiki (sin contaminación técnica)
3. Desarrolladores saben dónde buscar (technical/)
4. Usuarios no se confunden con arquitectura interna

**Movimientos necesarios:**
- `docs/tracking/architecture.md` → `technical/architecture/tracking.md`
- `docs/templates/template-system.md` → `technical/architecture/templates.md`
- `docs/skills/creating-skills.md` → `technical/contributing/creating-skills.md`
- `docs/internal/` → `technical/` (eliminar docs/internal/)

---

## ❓ Decisión del Usuario

¿Qué opción prefieres?

**A) Separación Estricta** (docs/ + technical/)
**B) Todo en docs/** (docs/user/ + docs/developer/)
**C) Híbrida** (docs/ + docs/contributing/ + technical/)
**D) Otra** (explícame tu visión)
