# Documentación Técnica - Claude Dev Kit

Este directorio contiene la **documentación técnica de referencia** del framework.

---

## 📐 Propósito

Esta documentación está diseñada para:
- ✅ Entender las decisiones arquitectónicas tomadas
- ✅ Comprender cómo funcionan los componentes internamente
- ✅ Conocer las especificaciones técnicas del sistema
- ✅ Servir como referencia para futuros desarrolladores

**NO es:**
- ❌ Documentación de usuario (cómo usar el framework)
- ❌ Tutoriales o guías de inicio
- ❌ Seguimiento de progreso o tickets

---

## 📂 Estructura

```
docs/
├── README.md                    # Este archivo
│
├── architecture/                # Decisiones arquitectónicas
│   ├── session-memory.md        # Sistema de memorización de sesiones
│   ├── template-system.md       # Sistema de templates y snippets
│   └── tracking-system.md       # Sistema de tracking de tiempo
│
├── specifications/              # Especificaciones técnicas (futuro)
│   └── (se creará en Fase 6)
│
└── decisions/                   # ADRs - Architecture Decision Records (futuro)
    └── (se creará cuando sea necesario)
```

---

## 🎯 Guía de Uso

### ¿Dónde buscar qué?

**Si quieres entender POR QUÉ algo funciona así:**
→ Ver `architecture/`

**Si quieres saber CÓMO usar el framework:**
→ Ver `README.md` principal o docs de usuario (se crearán en Fase 6)

**Si quieres ver el PROGRESO del proyecto:**
→ Ver `gestion/`

---

## 📋 Documentos Disponibles

### Arquitectura

| Documento | Descripción | Estado |
|-----------|-------------|--------|
| **session-memory.md** | Sistema de memorización entre sesiones | ✅ Completo |
| **template-system.md** | Sistema de templates con variables y snippets | ✅ Completo |
| **tracking-system.md** | Sistema de tracking automático de tiempo | ✅ Completo |

### Especificaciones (futuro)

Pendiente de creación en Fase 6 (Documentación):
- Especificación del skill implement-us
- Sistema de perfiles
- Formatos de persistencia

### Decisiones (futuro)

ADRs se crearán cuando sea necesario documentar decisiones arquitectónicas importantes.

---

## 🔄 Evolución de este Directorio

**Fase actual:** Sprint 3 - Fase 6 (Documentación)

**Cambios recientes:**
- 2026-02-15: Reorganización completa
  - Movidos análisis de tickets a `gestion/`
  - Eliminados documentos temporales
  - Creada estructura `architecture/`
  - Archivos de usuario marcados para Fase 6

**Próximos pasos:**
- Fase 6: Crear `specifications/`
- Futuro: Crear `decisions/` según necesidad

---

## 📖 Documentación de Usuario

La documentación de usuario (getting started, installation, user guides) se encuentra en:

- **README.md** principal del proyecto
- **Docs de usuario** (se crearán en Fase 6)

---

**Última Actualización:** 2026-02-15
