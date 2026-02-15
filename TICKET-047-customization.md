# TICKET-047: Guía de Personalización

**Sprint:** Sprint 3 - Fase 6: Documentación General
**Estimación:** 1.5h
**Prioridad:** Media
**Estado:** Pendiente
**Asignado:** Claude
**Branch:** feature/framework-documentation
**Dependencias:** TICKET-043

---

## 📋 Descripción

Crear `docs/customization.md` explicando cómo personalizar el framework para diferentes necesidades: modificar perfiles existentes, crear perfiles custom, personalizar templates y ajustar skills.

---

## 🎯 Objetivos

1. Explicar sistema de perfiles
2. Personalización de skills existentes
3. Personalización de templates
4. Sistema de variables y snippets
5. Creación de perfiles custom
6. Mejores prácticas

---

## 📝 Contenido del Archivo

### Secciones Principales

1. **Sistema de Perfiles**
   - Qué es un perfil
   - Perfiles incluidos (5 perfiles)
   - Cuándo usar cada perfil
   - Anatomía de un perfil

2. **Personalizar Skills Existentes**
   - Modificar config.json
   - Ajustar fases del skill
   - Cambiar templates por defecto
   - Override de variables

3. **Personalizar Templates**
   - Sistema de variables
   - Sistema de snippets
   - Crear templates custom
   - Organización de templates

4. **Variables y Snippets**
   - Tabla completa de variables
   - Tabla de snippets por tipo
   - Cómo usar variables
   - Cómo definir snippets custom

5. **Crear Perfil Custom**
   - Paso a paso para nuevo perfil
   - Estructura de archivo JSON
   - Configurar variables específicas
   - Registrar perfil en instalador

6. **Mejores Prácticas**
   - Nombrado de perfiles
   - Organización de configuración
   - Testing de personalizaciones
   - Compartir perfiles

---

## ✅ Subtareas

1. [ ] Sección: Sistema de perfiles (introducción)
2. [ ] Sección: Personalizar skills (config.json, fases, templates)
3. [ ] Sección: Personalizar templates (variables, snippets)
4. [ ] Sección: Tabla completa de variables (20+ variables)
5. [ ] Sección: Tabla de snippets por tipo (35+ snippets)
6. [ ] Sección: Crear perfil custom (tutorial completo)
7. [ ] Sección: Mejores prácticas
8. [ ] Revisión: Validar ejemplos de personalización

---

## 📊 Criterios de Aceptación

- [ ] Guía completa de personalización creada
- [ ] Sistema de perfiles explicado con ejemplos
- [ ] Tabla completa de variables (20+)
- [ ] Tabla completa de snippets (35+)
- [ ] Tutorial para crear perfil custom
- [ ] Ejemplos de personalización para cada sección
- [ ] Mejores prácticas documentadas

---

## 📁 Archivos a Crear

**Crear:**
- docs/customization.md (~500 líneas)

---

## 🔗 Referencias

- **Config base:** skills/implement-us/config.json
- **Perfiles:** skills/implement-us/customizations/*.json
- **Templates:** templates/
- **Variables:** Definidas en cada perfil
- **Snippets:** templates/*/snippets.json

---

## 📝 Notas

- Incluir tabla completa de variables con descripción
- Incluir tabla completa de snippets por tipo
- Ejemplos deben ser ejecutables
- Tutorial de perfil custom debe ser completo

---

**Tiempo Estimado:** 1.5 horas
**Prioridad:** Media
**Dependencias:** TICKET-043

---

**Última Actualización:** 2026-02-15
