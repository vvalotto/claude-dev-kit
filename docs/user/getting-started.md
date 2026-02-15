# Guía de Inicio Rápido

**Última Actualización:** 2026-02-15
**Audiencia:** Usuario Final
**Nivel:** Básico
**Tiempo estimado:** 15 minutos

---

## Tabla de Contenidos

- [Introducción](#introducción)
- [Prerequisitos](#prerequisitos)
- [Paso 1: Instalación](#paso-1-instalación-5-minutos)
- [Paso 2: Tu Primera Historia de Usuario](#paso-2-tu-primera-historia-de-usuario-5-minutos)
- [Paso 3: Tracking de Tiempo](#paso-3-tracking-de-tiempo-2-minutos)
- [Paso 4: Personalización Básica](#paso-4-personalización-básica-2-minutos)
- [Paso 5: Siguientes Pasos](#paso-5-siguientes-pasos)
- [Troubleshooting](#troubleshooting)
- [Resumen](#resumen)

---

## Introducción

¡Bienvenido a **Claude Dev Kit**! 🎉

Este framework te ayuda a implementar historias de usuario de forma estructurada, automatizada y trazable. En esta guía aprenderás a:

**Lo que harás en 15 minutos:**
1. ✅ Instalar el framework en tu proyecto (5 min)
2. ✅ Configurar tu perfil tecnológico (incluido)
3. ✅ Implementar tu primera historia de usuario (5 min)
4. ✅ Usar el sistema de tracking de tiempo (2 min)
5. ✅ Conocer opciones de personalización (2 min)

Al finalizar, tendrás el framework instalado y una historia de usuario completamente implementada con tests, documentación y métricas de calidad.

---

## Prerequisitos

Antes de comenzar, asegúrate de tener:

- ✅ **Python 3.9 o superior** instalado
  ```bash
  python --version  # Debe mostrar 3.9+
  ```

- ✅ **Git** instalado y configurado
  ```bash
  git --version  # Cualquier versión reciente
  ```

- ✅ **Claude Code CLI** instalado y funcionando
  ```bash
  claude --version  # Verifica que Claude Code esté instalado
  ```

- 🔷 **(Opcional)** Proyecto Python existente
  - Si no tienes uno, puedes crear un proyecto nuevo para probar

> **Nota:** Si no tienes Claude Code, visita [claude.com/code](https://claude.com/code) para instalarlo.

---

## Paso 1: Instalación (5 minutos)

### 1.1. Clonar el Repositorio

Primero, clona el framework en una ubicación global:

```bash
# Clonar en directorio home
git clone https://github.com/vvalotto/claude-dev-kit.git ~/.claude-dev-kit
```

**Salida esperada:**
```
Cloning into '/Users/tu-usuario/.claude-dev-kit'...
remote: Counting objects: 100% ...
Resolving deltas: 100% ...
```

---

### 1.2. Navegar a tu Proyecto

Si tienes un proyecto Python existente:

```bash
cd ~/mi-proyecto-python
```

Si quieres crear un proyecto nuevo para probar:

```bash
# Crear proyecto nuevo
mkdir ~/test-claude-dev-kit
cd ~/test-claude-dev-kit

# Inicializar proyecto Python
git init
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Crear estructura básica
mkdir -p src tests docs
touch src/__init__.py tests/__init__.py
```

---

### 1.3. Ejecutar el Instalador

Ahora instala el framework en tu proyecto:

```bash
# Instalación interactiva (recomendado para principiantes)
python ~/.claude-dev-kit/install/installer.py
```

**El instalador te preguntará:**

```
=== Claude Dev Kit - Instalador Interactivo ===

Selecciona tu stack tecnológico:

1. pyqt-mvc       - Aplicaciones de escritorio con PyQt6 + MVC
2. fastapi-rest   - APIs REST asíncronas con FastAPI
3. flask-rest     - APIs REST con Flask
4. flask-webapp   - Aplicaciones web fullstack con Flask
5. generic-python - Proyectos Python genéricos

Ingresa el número (1-5):
```

**Selecciona tu perfil:**
- `1` → PyQt-MVC: Para aplicaciones de escritorio PyQt6
- `2` → FastAPI-REST: Para APIs REST con FastAPI
- `3` → Flask-REST: Para APIs REST con Flask
- `4` → Flask-WebApp: Para aplicaciones web con Flask
- `5` → Generic-Python: Para proyectos Python sin framework específico

> **Tip:** Si no estás seguro, elige **5 (generic-python)**. Podrás personalizarlo después.

---

### 1.4. Validar Instalación

El instalador debería mostrar:

```
✅ Framework instalado exitosamente
✅ Configuración creada en .claude/
✅ Skills instalados: implement-us, track-pause, track-resume, track-status
✅ Templates instalados: bdd-scenario, implementation-plan, test-unit, implementation-report

Siguiente paso: Ejecuta /implement-us US-001
```

Verifica que los archivos se crearon:

```bash
ls -la .claude/
```

**Deberías ver:**
```
.claude/
├── config.json
├── skills/
│   ├── implement-us/
│   ├── track-pause/
│   ├── track-resume/
│   └── track-status/
├── templates/
│   ├── bdd/
│   └── planning/
└── tracking/
```

---

## Paso 2: Tu Primera Historia de Usuario (5 minutos)

Ahora implementaremos una historia de usuario simple para ver el framework en acción.

### 2.1. Crear Historia de Usuario

Crea un archivo con tu historia de usuario:

```bash
# Crear directorio
mkdir -p docs/user-stories

# Crear archivo US-001.md
cat > docs/user-stories/US-001.md << 'EOF'
# US-001: Calculadora Simple

**Prioridad:** Alta
**Estimación:** 2 horas

## Descripción

Como usuario de la aplicación, quiero una calculadora simple que sume dos números,
para poder realizar operaciones matemáticas básicas de forma rápida y confiable.

## Criterios de Aceptación

- La función acepta dos números (enteros o flotantes) como parámetros
- Retorna la suma correcta de ambos números
- Maneja casos edge:
  - Suma de números negativos
  - Suma con cero
  - Suma de números muy grandes

## Notas Técnicas

- Implementar en módulo `src/calculator.py`
- Tests en `tests/test_calculator.py`
- Usar pytest para testing

EOF
```

---

### 2.2. Ejecutar el Skill implement-us

Ahora ejecuta el skill que automatiza todo el proceso:

```bash
/implement-us US-001
```

**El skill te guiará por 10 fases:**

```
🚀 Iniciando implementación de US-001: Calculadora Simple

Fase 0: ✅ Validación de Contexto
  - Proyecto Python detectado
  - Archivo US-001.md encontrado
  - Prerequisitos verificados

Fase 1: 📝 Generación de Escenarios BDD
  Creando: tests/features/US-001.feature

  Scenario: Sumar dos números positivos
    Given la calculadora está inicializada
    When sumo 5 y 3
    Then el resultado debe ser 8

Fase 2: 📋 Plan de Implementación
  Creando: docs/planning/US-001-plan.md

  Tareas:
  1. Crear módulo calculator.py (15 min)
  2. Implementar función suma (20 min)
  3. Tests unitarios (30 min)
  4. Validación BDD (15 min)

Fase 3: 💻 Implementación
  Creando: src/calculator.py

  def suma(a: float, b: float) -> float:
      """Suma dos números."""
      return a + b

...
```

---

### 2.3. ¿Qué Está Pasando?

El skill **implement-us** automatiza todo el ciclo de desarrollo:

| Fase | Qué Hace | Output |
|------|----------|--------|
| **0. Validación** | Verifica prerequisitos | - |
| **1. BDD** | Genera escenarios Gherkin | `tests/features/US-001.feature` |
| **2. Planning** | Crea plan detallado | `docs/planning/US-001-plan.md` |
| **3. Implementación** | Genera código base | `src/calculator.py` |
| **4. Tests Unitarios** | Crea tests | `tests/test_calculator.py` |
| **5. Tests Integración** | Tests end-to-end | `tests/integration/` |
| **6. Validación BDD** | Ejecuta escenarios | Resultado pytest-bdd |
| **7. Quality Gates** | Pylint, coverage, CC | Métricas de calidad |
| **8. Documentación** | Docstrings y comentarios | Código documentado |
| **9. Reporte Final** | Resumen y métricas | `docs/reports/US-001-report.md` |

> **Importante:** El skill **sugiere código y tests**, pero tú decides si aceptar, modificar o rechazar cada sugerencia.

---

### 2.4. Resultado Esperado

Al completar las 10 fases, tendrás:

```
mi-proyecto/
├── src/
│   └── calculator.py          # ✅ Código implementado
├── tests/
│   ├── features/
│   │   └── US-001.feature     # ✅ Escenarios BDD
│   ├── test_calculator.py     # ✅ Tests unitarios
│   └── integration/           # ✅ Tests de integración
├── docs/
│   ├── planning/
│   │   └── US-001-plan.md     # ✅ Plan de implementación
│   └── reports/
│       └── US-001-report.md   # ✅ Reporte final
└── .claude/
    └── tracking/
        └── US-001.json        # ✅ Tracking de tiempo
```

---

## Paso 3: Tracking de Tiempo (2 minutos)

El sistema de tracking registra automáticamente el tiempo de cada fase. Puedes controlarlo manualmente cuando lo necesites.

### 3.1. Ver Estado Actual

```bash
/track-status
```

**Salida:**
```
⏱️ Estado de Tracking

US Actual: US-001 (Calculadora Simple)
Fase Actual: Fase 3 - Implementación
Estado: En progreso
Tiempo transcurrido: 12 minutos

Desglose por fase:
✅ Fase 0 - Validación: 1 min
✅ Fase 1 - BDD: 3 min
✅ Fase 2 - Planning: 5 min
🔄 Fase 3 - Implementación: 3 min (en curso)
```

---

### 3.2. Pausar Trabajo

Si necesitas tomar un descanso:

```bash
# Pausar con razón
/track-pause "Lunch break"
```

**Salida:**
```
⏸️ Tracking pausado
Razón: Lunch break
Hora: 12:30
```

---

### 3.3. Reanudar Tracking

Cuando vuelvas:

```bash
/track-resume
```

**Salida:**
```
▶️ Tracking reanudado
Tiempo de pausa: 30 minutos
Continuando con: Fase 3 - Implementación
```

---

### 3.4. Ver Reporte Final

Al terminar la US:

```bash
/track-report US-001
```

**Salida:**
```
📊 Reporte de Tiempo - US-001

Tiempo Total: 1h 45min
Tiempo Estimado: 2h
Varianza: -15min (mejor que estimado)

Desglose por Fase:
✅ Fase 0 - Validación: 2min (est: 2min)
✅ Fase 1 - BDD: 5min (est: 5min)
✅ Fase 2 - Planning: 8min (est: 10min)
✅ Fase 3 - Implementación: 25min (est: 30min)
✅ Fase 4 - Tests Unitarios: 20min (est: 25min)
...

Pausas:
⏸️ Lunch break: 30min (12:30 - 13:00)
```

> **Ver más:** [Tracking - Guía de Usuario](./tracking/user-guide.md)

---

## Paso 4: Personalización Básica (2 minutos)

Ahora que has visto cómo funciona, puedes personalizar el framework a tus necesidades.

### 4.1. Archivo de Configuración

Abre el archivo de configuración:

```bash
# Con VS Code
code .claude/skills/implement-us/config.json

# Con cualquier editor
nano .claude/skills/implement-us/config.json
```

**Verás algo como:**
```json
{
  "profile": "generic-python",
  "architecture_pattern": "layered",
  "test_framework": "pytest",
  "quality_gates": {
    "pylint_threshold": 8.0,
    "coverage_threshold": 90,
    "max_complexity": 10
  },
  "phases": {
    "enable_bdd": true,
    "enable_integration_tests": true,
    "enable_quality_gates": true
  }
}
```

---

### 4.2. Cambios Comunes

**Cambiar patrón arquitectónico:**
```json
"architecture_pattern": "mvc"  // o "mvt", "layered", "hexagonal"
```

**Cambiar framework de tests:**
```json
"test_framework": "pytest-qt"  // o "pytest-asyncio", "unittest"
```

**Ajustar quality gates:**
```json
"quality_gates": {
  "pylint_threshold": 9.0,      // Más estricto
  "coverage_threshold": 95,     // Mayor cobertura
  "max_complexity": 8           // Menor complejidad
}
```

**Deshabilitar fases opcionales:**
```json
"phases": {
  "enable_bdd": false,               // Saltar BDD
  "enable_integration_tests": false  // Saltar tests integración
}
```

> **Ver más:** [Guía de Personalización](./customization.md)

---

### 4.3. Cambiar Perfil Completo

Si quieres cambiar de perfil (ej: de generic-python a fastapi-rest):

```bash
# Re-ejecutar instalador
python ~/.claude-dev-kit/install/installer.py --profile fastapi-rest --yes
```

Esto actualizará `.claude/skills/implement-us/config.json` con la configuración del nuevo perfil.

---

## Paso 5: Siguientes Pasos

¡Felicitaciones! Has completado la guía de inicio rápido. 🎉

### Aprende Más Sobre el Framework

Profundiza en cada componente:

1. **[Instalación Detallada](./installation.md)** - Opciones avanzadas, modos de instalación
2. **[Skill implement-us](./skills/implement-us.md)** - Entender las 10 fases en detalle
3. **[Sistema de Tracking](./tracking/user-guide.md)** - Comandos avanzados, reportes históricos
4. **[Personalización Completa](./customization.md)** - Crear perfiles custom, modificar templates
5. **[Referencia de Configuración](./configuration.md)** - Todas las opciones disponibles

---

### Tutoriales por Stack Tecnológico

Aprende con proyectos reales completos:

- **[Proyecto PyQt-MVC](./examples/pyqt-project.md)** - Aplicación de escritorio con interfaz gráfica
- **[Proyecto FastAPI-REST](./examples/fastapi-project.md)** - API REST asíncrona completa
- **[Proyecto Flask-REST](./examples/flask-rest-project.md)** - API REST con Flask
- **[Proyecto Flask-WebApp](./examples/flask-webapp-project.md)** - Aplicación web con templates
- **[Proyecto Python Genérico](./examples/generic-python.md)** - CLI app o librería Python

---

### Únete a la Comunidad

- **📋 GitHub Issues:** [Reportar bugs o sugerir features](https://github.com/vvalotto/claude-dev-kit/issues)
- **🔀 Pull Requests:** [Contribuir al proyecto](https://github.com/vvalotto/claude-dev-kit/pulls)
- **📖 Changelog:** Ver novedades de cada versión (pendiente)
- **🤝 Contributing:** Guía para contribuir (pendiente)

---

## Troubleshooting

### Problema: "Python version not supported"

**Síntoma:**
```
Error: Python 3.9+ required. Found: 3.8.10
```

**Causa:** Versión de Python antigua

**Solución:**
1. Verificar versión actual: `python --version`
2. Actualizar Python a 3.9 o superior
3. En sistemas con múltiples versiones, usar `python3.9` o `python3.11` explícitamente
4. Re-ejecutar instalador

---

### Problema: "Project not found"

**Síntoma:**
```
Error: No Python project found in current directory
```

**Causa:** Ejecutaste el instalador desde directorio incorrecto

**Solución:**
1. Navega a la raíz de tu proyecto Python: `cd ~/mi-proyecto`
2. Verifica que exista `src/` o archivos `.py`
3. Si es proyecto nuevo, crea estructura básica primero
4. Re-ejecutar instalador

---

### Problema: "Skill /implement-us not found"

**Síntoma:**
```
Command not found: /implement-us
```

**Causa:** El skill no se instaló correctamente

**Solución:**
1. Verificar que existe: `ls .claude/skills/implement-us/`
2. Si no existe, re-ejecutar instalador:
   ```bash
   python ~/.claude-dev-kit/install/installer.py
   ```
3. Reiniciar Claude Code
4. Verificar con `/help` que el skill esté listado

---

### Problema: "Tests failing after implementation"

**Síntoma:**
```
FAILED tests/test_calculator.py::test_suma - AssertionError
```

**Causa:** El código sugerido necesita ajustes

**Solución:**
1. Revisar el código generado en `src/`
2. Ajustar según los requisitos específicos
3. Ejecutar tests manualmente: `pytest tests/`
4. El skill sugiere código base, **tú decides los ajustes finales**

> **Importante:** El framework **asiste** pero no reemplaza tu criterio como desarrollador.

---

### Problema: "Quality gates failing"

**Síntoma:**
```
❌ Pylint score: 7.5/10 (threshold: 8.0)
```

**Causa:** Código no cumple con umbrales de calidad

**Solución:**
1. Revisar output de Pylint: `pylint src/`
2. Corregir issues indicados (imports sin usar, nombres, etc.)
3. O ajustar umbral en config si es razonable:
   ```json
   "pylint_threshold": 7.5
   ```
4. Re-ejecutar quality gates

---

## Resumen

¡Has completado la guía de inicio rápido! ✅

**Lo que lograste:**
- ✅ Framework instalado y configurado
- ✅ Primera US implementada (US-001: Calculadora Simple)
- ✅ Sistema de tracking funcionando
- ✅ Configuración básica personalizada
- ✅ Conocimiento de siguientes pasos

**Tiempo total:** ~15 minutos

---

### Checklist de Progreso

- [x] Instalación del framework
- [x] Selección de perfil tecnológico
- [x] Primera historia de usuario
- [x] Comandos básicos de tracking
- [x] Personalización de configuración
- [ ] **Próximo:** [Instalación Detallada](./installation.md)
- [ ] **Próximo:** [Skill implement-us - Guía Completa](./skills/implement-us.md)
- [ ] **Próximo:** [Tutorial de tu stack](./examples/)

---

### ¿Qué Sigue?

Elige tu próximo paso según tu objetivo:

**Si quieres profundizar en el framework:**
→ [Skill implement-us - Documentación Completa](./skills/implement-us.md)

**Si quieres personalizarlo a tu stack:**
→ [Guía de Personalización](./customization.md)

**Si quieres aprender con un proyecto real:**
→ [Tutoriales por Stack](../examples/)

**Si tienes dudas o problemas:**
→ [GitHub Issues](https://github.com/vvalotto/claude-dev-kit/issues)

---

**Anterior:** [Índice](./index.md)
**Siguiente:** [Instalación Detallada](./installation.md)
**Índice:** [Volver al índice](./index.md)
