# Sistema de Memorización de Contexto entre Sesiones

**Versión:** 1.0
**Fecha:** 2026-02-08
**Autor:** Claude Dev Kit Team

---

## 🎯 Objetivo

Mantener contexto entre sesiones de Claude Code:
- **Al salir:** Guardar metadata automáticamente mediante hook `SessionEnd`
- **Al iniciar:** Restaurar contexto con comando `/resume`

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────┐
│  SESIÓN ACTUAL (trabajando con Claude)                  │
│  - Implementas código                                   │
│  - Haces commits                                        │
│  - Tomas decisiones                                     │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼ /exit o Ctrl+D
┌─────────────────────────────────────────────────────────┐
│  HOOK SessionEnd (automático)                           │
│  Script: .claude/hooks/save-session.sh                  │
│  ├─ Guarda metadata (timestamp, git status, etc.)      │
│  ├─ Guarda path del transcript                         │
│  └─ Crea flag "resumen pendiente"                      │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼ Sesión cerrada
┌─────────────────────────────────────────────────────────┐
│  MEMORIA PERSISTENTE                                    │
│  ~/.claude/projects/.../memory/                         │
│  ├─ session-metadata.json     (metadata de última sesión)
│  ├─ session-needs-summary.flag (marcador)              │
│  ├─ session-current.md        (resumen + próximas)     │
│  └─ session-history.md        (historial completo)     │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼ Inicia nueva sesión
┌─────────────────────────────────────────────────────────┐
│  NUEVA SESIÓN                                           │
│  Usuario ejecuta: /resume                              │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼ Skill /resume invocado
┌─────────────────────────────────────────────────────────┐
│  RESTAURACIÓN DE CONTEXTO (Skill resume)              │
│  1. Leo session-metadata.json                           │
│  2. Leo session-current.md                             │
│  3. Leo session-history.md                             │
│  4. Genero resumen inteligente                         │
│  5. Muestro: resumen + próximas actividades            │
│  6. Actualizo archivos de tracking                     │
│  7. Elimino flag (si existe)                           │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 Estructura de Archivos

```
claude-dev-kitc/                              # Proyecto
├── .claude/
│   ├── settings.json                         # Configuración de hooks
│   └── hooks/
│       ├── check-session-start.sh            # Script de inicio (ejecutable)
│       └── save-session.sh                   # Script de exit (ejecutable)
├── docs/
│   └── session-memory-system.md              # Este documento
└── TODO.md                                   # Lista de tareas pendientes

~/.claude/projects/.../memory/                # Memoria persistente (auto-cargada)
├── MEMORY.md                                 # Auto-cargado en system prompt
├── session-metadata.json                     # Metadata de última sesión
├── session-needs-summary.flag                # Marcador (cuando existe)
├── session-current.md                        # Resumen actual + próximas
└── session-history.md                        # Historial de sesiones
```

---

## 🚀 Implementación Paso a Paso

### Paso 1: Crear Estructura de Directorios

```bash
# Desde la raíz de tu proyecto
cd /Users/victor/PycharmProjects/claude-dev-kitc

# Crear directorio de hooks
mkdir -p .claude/hooks

# Crear directorio de memoria (si no existe)
mkdir -p ~/.claude/projects/-Users-victor-PycharmProjects-claude-dev-kitc/memory
```

---

### Paso 2: Crear Script de SessionEnd

**Archivo:** `.claude/hooks/save-session.sh`

```bash
#!/bin/bash

# Directorios
PROJECT_DIR="$CLAUDE_PROJECT_DIR"
MEMORY_DIR="$HOME/.claude/projects/-Users-victor-PycharmProjects-claude-dev-kitc/memory"

# Leer hook input desde stdin
INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // "unknown"')
REASON=$(echo "$INPUT" | jq -r '.reason // "other"')
TRANSCRIPT=$(echo "$INPUT" | jq -r '.transcript_path // ""')
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Guardar metadata de la sesión
jq -n \
  --arg session_id "$SESSION_ID" \
  --arg reason "$REASON" \
  --arg transcript "$TRANSCRIPT" \
  --arg timestamp "$TIMESTAMP" \
  --arg git_status "$(cd "$PROJECT_DIR" 2>/dev/null && git status --short 2>/dev/null || echo 'N/A')" \
  --arg git_branch "$(cd "$PROJECT_DIR" 2>/dev/null && git branch --show-current 2>/dev/null || echo 'N/A')" \
  '{
    session_id: $session_id,
    exit_reason: $reason,
    transcript_path: $transcript,
    timestamp: $timestamp,
    git_status: $git_status,
    git_branch: $git_branch
  }' > "$MEMORY_DIR/session-metadata.json" 2>/dev/null

# Crear flag para indicar que necesitamos generar resumen en próxima sesión
touch "$MEMORY_DIR/session-needs-summary.flag"

echo "✅ Session saved. Summary will be ready on next start." >&2
exit 0
```

**Hacer ejecutable:**
```bash
chmod +x .claude/hooks/save-session.sh
```

---

### Paso 3: Crear Script de SessionStart

**Archivo:** `.claude/hooks/check-session-start.sh`

```bash
#!/bin/bash

MEMORY_DIR="$HOME/.claude/projects/-Users-victor-PycharmProjects-claude-dev-kitc/memory"
FLAG_FILE="$MEMORY_DIR/session-needs-summary.flag"

if [ -f "$FLAG_FILE" ]; then
  echo "IMPORTANT: Session summary needed. The file session-needs-summary.flag exists."
  echo "You MUST generate a session summary before proceeding with any other task."
  echo ""
  echo "Steps:"
  echo "1. Read session-metadata.json for basic context"
  echo "2. Generate summary of previous session"
  echo "3. Show summary to user"
  echo "4. Ask about next activities"
  echo "5. Remove the flag file"
  exit 0
else
  # No flag, normal session start
  exit 0
fi
```

**Hacer ejecutable:**
```bash
chmod +x .claude/hooks/check-session-start.sh
```

---

### Paso 4: Configurar Hooks en settings.json

**Archivo:** `.claude/settings.json`

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/check-session-start.sh"
          }
        ]
      }
    ],
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/save-session.sh"
          }
        ]
      }
    ]
  }
}
```

**Nota:** No usar comillas escapadas alrededor de `$CLAUDE_PROJECT_DIR` - la variable de entorno debe usarse directamente.

---

### Paso 5: Crear Archivos Base de Memoria

**Archivo:** `~/.claude/projects/-Users-victor-PycharmProjects-claude-dev-kitc/memory/MEMORY.md`

```markdown
# Claude Dev Kit - Auto Memory

Este archivo se carga automáticamente al inicio de cada sesión.

## Sistema de Sesiones

Al inicio de cada sesión:
1. Verifico si existe `session-needs-summary.flag`
2. Si existe, genero resumen de sesión anterior
3. Muestro resumen + próximas actividades
4. Actualizo `session-current.md` y `session-history.md`

## Instrucciones

- Al detectar el flag, SIEMPRE generar resumen antes de cualquier otra acción
- Leer `session-metadata.json` para contexto básico
- Leer últimas líneas del transcript si es necesario
- Preguntar al usuario sobre próximas actividades si no están claras
```

**Archivo:** `~/.claude/projects/-Users-victor-PycharmProjects-claude-dev-kitc/memory/session-current.md`

```markdown
# Sesión Actual - Claude Dev Kit

_Este archivo se actualiza automáticamente al inicio de cada sesión._

---

## 📝 Última Sesión

**Pendiente:** Primera sesión del sistema de memorización.

---

## 🎯 Próxima Sesión - Plan de Trabajo

### Objetivo
Implementar sistema de memorización de contexto entre sesiones.

### Tareas
1. [ ] Implementar hooks SessionEnd
2. [ ] Crear templates de memoria
3. [ ] Probar flujo completo

---

**Última Actualización:** [Pendiente]
```

**Archivo:** `~/.claude/projects/-Users-victor-PycharmProjects-claude-dev-kitc/memory/session-history.md`

```markdown
# Historial de Sesiones - Claude Dev Kit

---

_El historial se comenzará a registrar después de implementar el sistema._
```

---

### Paso 6: Crear TODO.md en Raíz del Proyecto

**Archivo:** `TODO.md` (raíz del proyecto)

```markdown
# TODO - Claude Dev Kit

## 🔥 Ahora (Esta Sesión)
- [ ] Implementar sistema de memorización entre sesiones
  - [ ] Crear hook SessionEnd
  - [ ] Configurar settings.json
  - [ ] Probar flujo completo

## 📋 Siguiente Sesión
- [ ] Iniciar Fase 2: Sistema de Instalación
  - [ ] Migrar tracking desde _work/from-simapp/
  - [ ] Crear installer.py básico
  - [ ] Crear config.yaml con perfiles

## 🎯 Más Adelante (Sprint 2)
- [ ] Generalizar skills implement-us
- [ ] Generalizar templates
- [ ] Crear documentación

---

**Última Actualización:** 2026-02-08
```

---

## 🔄 Flujo de Uso Diario

### 1️⃣ **Inicio de Sesión**

```bash
# Inicias Claude Code
cd /Users/victor/PycharmProjects/claude-dev-kitc
claude
```

**Claude automáticamente:**
1. Detecta si existe `session-needs-summary.flag`
2. Si existe → Genera y muestra resumen de sesión anterior
3. Muestra próximas actividades planificadas
4. Pregunta si quieres ajustar el plan

**Usuario:**
- Lee el resumen
- Confirma o ajusta el plan
- Comienza a trabajar

---

### 2️⃣ **Durante la Sesión**

- Trabajo normal con Claude
- Implementación de código
- Commits
- Claude actualiza `TODO.md` según avances

---

### 3️⃣ **Fin de Sesión**

```bash
# Simplemente salir
/exit
# o Ctrl+D
```

**Hook SessionEnd automáticamente:**
1. Ejecuta `.claude/hooks/save-session.sh`
2. Guarda metadata en `session-metadata.json`
3. Crea flag `session-needs-summary.flag`
4. Sale de Claude Code

**No se requiere ninguna acción adicional.**

---

### 4️⃣ **Próxima Sesión**

Al iniciar de nuevo, Claude detecta el flag y repite el ciclo.

---

## ✅ Verificación de Instalación

### Checklist de Verificación

```bash
# 1. Verificar estructura de directorios
ls -la .claude/hooks/check-session-start.sh
ls -la .claude/hooks/save-session.sh
ls -la .claude/settings.json
ls -la ~/.claude/projects/-Users-victor-PycharmProjects-claude-dev-kitc/memory/

# 2. Verificar que los scripts son ejecutables
test -x .claude/hooks/check-session-start.sh && echo "✅ check-session-start.sh ejecutable" || echo "❌ NO ejecutable"
test -x .claude/hooks/save-session.sh && echo "✅ save-session.sh ejecutable" || echo "❌ NO ejecutable"

# 3. Verificar sintaxis JSON del settings.json
jq empty .claude/settings.json && echo "✅ JSON válido" || echo "❌ JSON inválido"

# 4. Verificar que jq está instalado (requerido por el script)
which jq || echo "❌ jq no instalado - ejecutar: brew install jq"

# 5. Probar el script manualmente
echo '{"session_id":"test","reason":"test","transcript_path":""}' | .claude/hooks/save-session.sh

# 6. Verificar que se creó el flag
ls -la ~/.claude/projects/-Users-victor-PycharmProjects-claude-dev-kitc/memory/session-needs-summary.flag
```

---

## 🧪 Prueba del Sistema Completo

### Prueba 1: Simulación de Exit

```bash
# Ejecutar hook manualmente
echo '{"session_id":"test-123","reason":"manual_test","transcript_path":"/tmp/test.jsonl"}' | \
  .claude/hooks/save-session.sh

# Verificar archivos creados
cat ~/.claude/projects/-Users-victor-PycharmProjects-claude-dev-kitc/memory/session-metadata.json
ls ~/.claude/projects/-Users-victor-PycharmProjects-claude-dev-kitc/memory/session-needs-summary.flag
```

**Resultado esperado:**
```json
{
  "session_id": "test-123",
  "exit_reason": "manual_test",
  "transcript_path": "/tmp/test.jsonl",
  "timestamp": "2026-02-08T...",
  "git_status": "...",
  "git_branch": "main"
}
```

### Prueba 2: Ciclo Completo

1. **Inicia Claude Code** → Debe detectar el flag y generar resumen
2. **Trabaja un poco** → Haz algún cambio, lee archivos, etc.
3. **Sale con `/exit`** → Hook debe ejecutarse
4. **Verifica archivos** → Revisa que metadata se guardó
5. **Inicia de nuevo** → Debe mostrar resumen de la sesión anterior

---

## 🔧 Troubleshooting

### Problema 1: Hook no se ejecuta

**Síntomas:** Al salir, no se crea `session-metadata.json`

**Soluciones:**
```bash
# Verificar que el hook está registrado
grep -A 5 "SessionEnd" .claude/settings.json

# Verificar permisos de ejecución
chmod +x .claude/hooks/save-session.sh

# Ver logs de Claude Code (si hay errores de hook)
# Los errores del hook aparecen en stderr al salir
```

### Problema 2: Script falla por jq

**Síntomas:** Error "jq: command not found"

**Solución:**
```bash
# macOS
brew install jq

# Verificar instalación
jq --version
```

### Problema 3: Flag no se detecta al inicio

**Síntomas:** Claude no genera resumen al iniciar

**Solución:**
- Asegúrate de que `MEMORY.md` existe y tiene las instrucciones
- Mención explícita: "Claude, ¿existe el archivo session-needs-summary.flag?"
- Claude debería detectarlo automáticamente gracias a MEMORY.md

### Problema 4: Path de memoria incorrecto

**Síntomas:** Archivos no se encuentran

**Solución:**
```bash
# Verificar el path correcto de tu proyecto en memoria
ls -la ~/.claude/projects/

# Ajustar path en save-session.sh si es necesario
# La carpeta debería coincidir con la ruta de tu proyecto
```

---

## 📊 Templates de Output

### Template: Inicio de Sesión con Resumen

```
🔄 Detecté una sesión anterior pendiente de resumen...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 RESUMEN DE ÚLTIMA SESIÓN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Fecha:** 2026-02-08 10:30 - 12:45
**Duración:** ~2.5 horas
**Branch:** main

### ✅ Completado
- Implementación del sistema de hooks SessionEnd
- Creación de templates de memoria
- Configuración de settings.json

### 🔍 Decisiones Tomadas
- Usar enfoque híbrido: hook simple + resumen inteligente
- Guardar metadata en JSON para fácil parsing

### 📝 Archivos Modificados
M .claude/settings.json
A .claude/hooks/save-session.sh
M TODO.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 PRÓXIMA SESIÓN - PLAN DE TRABAJO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Objetivo Inmediato
Probar el sistema completo y comenzar Fase 2

### Tareas Prioritarias
1. [ ] Hacer ciclo completo de prueba del sistema de sesiones
2. [ ] Migrar sistema de tracking desde _work/
3. [ ] Comenzar instalador básico

### Archivos a Revisar
- _work/from-simapp/tracking/time_tracker.py
- PROJECT_PLAN_claude-dev-kit.md (Sección 5.2)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

¿Quieres proceder con este plan o ajustarlo?
```

---

## 🎯 Ventajas del Sistema

### Para el Usuario

1. **Continuidad automática** - No necesitas recordar dónde quedaste
2. **Sin fricción** - Exit normal, sin comandos especiales
3. **Contexto inteligente** - Resumen generado por IA, no solo timestamps
4. **Planificación guiada** - Próximas actividades sugeridas al inicio

### Para el Proyecto

1. **Historial de decisiones** - Registro de qué se hizo y por qué
2. **Tracking de progreso** - Fácil ver avance entre sesiones
3. **Documentación automática** - El historial sirve como log del proyecto
4. **Reduced context switching** - Retomar el trabajo es inmediato

---

## 🔮 Mejoras Futuras

### Corto Plazo

- [ ] Agregar estimación de duración de sesión (inicio vs fin)
- [ ] Incluir métricas de commits (cuántos, qué archivos)
- [ ] Mostrar warning si hay cambios sin commitear al salir

### Mediano Plazo

- [ ] Integración con sistema de tracking de tiempo (`/track-*`)
- [ ] Generar reportes semanales automáticos
- [ ] Sugerir próximas tareas basado en patrón de trabajo

### Largo Plazo

- [ ] Machine learning para predecir mejor las próximas actividades
- [ ] Integración con GitHub Issues/Projects
- [ ] Dashboard web de sesiones y progreso

---

## 📚 Referencias

- **Claude Code Hooks Documentation:** Ver agente claude-code-guide
- **Hook Events:** 14 eventos disponibles, SessionEnd y SessionStart clave para este sistema
- **Settings File Locations:** `~/.claude/settings.json` o `.claude/settings.json`
- **Auto Memory:** `~/.claude/projects/<project>/memory/` (auto-cargado)

---

## 📝 Changelog del Sistema

### v1.1 - 2026-02-08 (actualización)

- ✅ Agregado hook SessionStart para detección automática
- ✅ Script check-session-start.sh para notificar a Claude
- ✅ Mejora en flujo automático de inicio de sesión
- ✅ Documentación actualizada con ambos hooks

### v1.0 - 2026-02-08

- ✅ Diseño inicial del sistema
- ✅ Implementación de hook SessionEnd
- ✅ Templates de memoria
- ✅ Documentación completa
- ✅ Guía de troubleshooting

---

**Última Actualización:** 2026-02-08
**Mantenedor:** Victor Valotto / Claude Code
**Licencia:** MIT (parte del proyecto Claude Dev Kit)
