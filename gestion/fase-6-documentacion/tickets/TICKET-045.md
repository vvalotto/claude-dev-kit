# TICKET-045: Guía de Inicio Rápido

**Fase:** 6 - Documentación General
**Sprint:** 3
**Estado:** 📋 Pendiente
**Prioridad:** Alta
**Estimación:** 1.5 horas
**Asignado a:** Claude Code

---

## Descripción

Crear `docs/getting-started.md` con tutorial paso a paso para nuevos usuarios. Esta guía debe permitir a un usuario completar el setup completo y ejecutar su primera historia de usuario en menos de 15 minutos.

---

## Objetivos

1. Proporcionar instalación rápida (5 minutos)
2. Guiar primera historia de usuario con /implement-us
3. Mostrar comandos básicos de tracking
4. Explicar personalización básica
5. Indicar siguientes pasos y recursos

---

## Contenido del Archivo

### Estructura Propuesta

```markdown
# Guía de Inicio Rápido

## Introducción

Bienvenido a Claude Dev Kit. Esta guía te ayudará a comenzar en menos de 15 minutos.

**Prerequisitos:**
- Python 3.9+
- Git
- Claude Code CLI
- (Opcional) Proyecto Python existente

**Lo que harás:**
1. Instalar el framework (5 min)
2. Configurar tu perfil (2 min)
3. Implementar tu primera historia de usuario (5 min)
4. Usar tracking de tiempo (2 min)
5. Explorar personalización (2 min)

---

## Paso 1: Instalación (5 minutos)

### Clonar el Repositorio

\```bash
git clone https://github.com/vvalotto/claude-dev-kit.git ~/.claude-dev-kit
\```

### Navegar a tu Proyecto

\```bash
cd ~/mi-proyecto-python
\```

### Ejecutar Instalador

\```bash
python ~/.claude-dev-kit/install/installer.py
\```

**Seleccionar perfil:**
- PyQt-MVC: Para aplicaciones de escritorio PyQt6
- FastAPI-REST: Para APIs REST con FastAPI
- Flask-REST: Para APIs REST con Flask
- Flask-WebApp: Para aplicaciones web Flask
- Generic-Python: Para proyectos Python genéricos

> **Tip:** Si no estás seguro, elige "Generic-Python"

---

## Paso 2: Tu Primera Historia de Usuario (5 minutos)

### Crear archivo de historia de usuario

\```bash
# US-001.md
mkdir -p docs/user-stories
cat > docs/user-stories/US-001.md << 'EOF'
# US-001: Calculadora Simple

## Descripción
Como usuario, quiero una calculadora simple que sume dos números,
para poder realizar operaciones matemáticas básicas.

## Criterios de Aceptación
- La función acepta dos números como parámetros
- Retorna la suma correcta
- Maneja casos edge (negativos, ceros)
EOF
\```

### Ejecutar el skill

\```bash
/implement-us US-001
\```

**El skill te guiará por 10 fases:**
0. ✅ Validación de contexto
1. 📝 Generación de escenarios BDD
2. 📋 Plan de implementación
3. 💻 Implementación
4. 🧪 Tests unitarios
5. 🔗 Tests de integración
6. ✅ Validación BDD
7. 📊 Quality Gates
8. 📖 Documentación
9. 📄 Reporte Final

---

## Paso 3: Tracking de Tiempo (2 minutos)

El tracking se inicia automáticamente, pero puedes controlarlo:

### Ver estado actual

\```bash
/track-status
\```

### Pausar trabajo

\```bash
/track-pause "Lunch break"
\```

### Reanudar

\```bash
/track-resume
\```

### Ver reporte

\```bash
/track-report US-001
\```

---

## Paso 4: Personalización Básica (2 minutos)

### Editar configuración

\```bash
# Abrir archivo de configuración
code .claude/skills/implement-us/config.json
\```

**Cambios comunes:**
- architecture_pattern: mvc, mvt, layered
- test_framework: pytest, pytest-qt, pytest-asyncio
- quality_gates: umbrales de pylint, coverage, etc.

> **Ver más:** [Guía de Personalización](./customization.md)

---

## Paso 5: Siguientes Pasos

### Aprende Más

1. **[Guía de Instalación Detallada](./installation.md)** - Opciones avanzadas
2. **[Skill implement-us](./skills/implement-us.md)** - Entender las 10 fases
3. **[Sistema de Tracking](./tracking/user-guide.md)** - Tracking avanzado
4. **[Personalización](./customization.md)** - Crear perfiles custom

### Tutoriales por Stack

- **[PyQt-MVC](./examples/pyqt-project.md)** - Aplicaciones de escritorio
- **[FastAPI-REST](./examples/fastapi-project.md)** - APIs asíncronas
- **[Flask](./examples/flask-rest-project.md)** - APIs y webapps Flask

### Comunidad

- **Issues:** https://github.com/vvalotto/claude-dev-kit/issues
- **Contribuir:** CONTRIBUTING.md
- **Changelog:** CHANGELOG.md

---

## Troubleshooting

### Error: "Python version not supported"
**Solución:** Actualizar a Python 3.9+

### Error: "Project not found"
**Solución:** Ejecutar instalador desde raíz del proyecto Python

### Skill no se encuentra
**Solución:** Verificar que `.claude/skills/implement-us/` existe

---

## Resumen

✅ Framework instalado
✅ Primera US implementada
✅ Tracking funcionando
✅ Configuración básica entendida

**Próximo paso:** [Personalización](./customization.md)

---

**Volver:** [Índice](./index.md)
**Siguiente:** [Instalación Detallada](./installation.md)
```

---

## Checklist de Implementación

1. [ ] Sección: Introducción y prerequisitos
2. [ ] Sección: Instalación en 5 minutos
3. [ ] Sección: Primera historia de usuario (ejemplo completo)
4. [ ] Sección: Comandos de tracking básicos
5. [ ] Sección: Personalización rápida
6. [ ] Sección: Siguientes pasos y recursos
7. [ ] Sección: Troubleshooting común
8. [ ] Revisión: Validar que el tutorial funciona end-to-end

---

## Criterios de Aceptación

- [ ] Guía completa de inicio rápido creada
- [ ] Tutorial permite setup en <15 minutos
- [ ] Incluye ejemplo ejecutable de historia de usuario
- [ ] Comandos básicos de tracking documentados
- [ ] Enlaces a documentación detallada
- [ ] Sección de troubleshooting con problemas comunes
- [ ] Formato markdown limpio y profesional

---

## Archivos

**Crear:**
- docs/getting-started.md (~500 líneas)

---

## Notas Técnicas

- **TICKET-043:** Convenciones de documentación
- **Skill implement-us:** .claude/skills/implement-us/skill.md
- **Sistema de tracking:** docs/tracking/user-guide.md

---

## Dependencias

**Depende de:**
- TICKET-043

**Bloquea a:**
- TICKET-051

---

## Notas de Implementación

- **Crucial:** Esta es la primera experiencia del usuario - debe ser fluida
- Incluir ejemplo completo y ejecutable
- Usar comandos reales que funcionen
- Validar el tutorial ejecutándolo paso a paso
- Mantener tono amigable y motivador

---

## Resultado

_Se completará al finalizar el ticket con descripción de resultados, commits y archivos creados._
