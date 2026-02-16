# Tutorial: {STACK_NAME} - {US_TITLE}

**Stack:** {STACK_NAME} ({PROFILE_ID})
**Tiempo Estimado:** < 60 minutos
**Nivel:** Principiante

---

## 📋 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Requisitos Previos](#requisitos-previos)
3. [Historia de Usuario](#historia-de-usuario)
4. [Setup del Proyecto](#setup-del-proyecto)
5. [Instalación del Framework](#instalación-del-framework)
6. [Walkthrough: Las 10 Fases](#walkthrough-las-10-fases)
7. [Validación Final](#validación-final)
8. [Troubleshooting](#troubleshooting)
9. [Próximos Pasos](#próximos-pasos)
10. [Recursos](#recursos)

---

## 🎯 Introducción

Este tutorial te guiará paso a paso en la creación de **{PROJECT_NAME}** utilizando el perfil **{PROFILE_ID}** del Claude Dev Kit.

Aprenderás:
- ✅ Cómo usar el skill `/implement-us` para guiar la implementación
- ✅ Cómo el framework adapta las 10 fases a tu stack tecnológico
- ✅ Cómo generar BDD scenarios, tests y documentación automáticamente
- ✅ Buenas prácticas específicas de {STACK_NAME}

Al finalizar, tendrás una aplicación funcional y comprenderás cómo aplicar el framework a tus propios proyectos.

---

## ✅ Requisitos Previos

### Software Necesario

- **Python:** 3.10 o superior
- **Claude Code CLI:** Instalado y configurado
- **{STACK_SPECIFIC_TOOLS}:** (Ejemplo: PyQt6, FastAPI, Flask, etc.)
- **Git:** Para control de versiones

### Conocimientos

- Programación básica en Python
- Familiaridad con la terminal/línea de comandos
- (Opcional) Conceptos básicos de {STACK_NAME}

### Verificación

```bash
# Verificar Python
python --version  # Debe ser >= 3.10

# Verificar Claude Code
claude --version

# Verificar Git
git --version
```

---

## 📖 Historia de Usuario

```gherkin
# US-{US_ID}: {US_TITLE}

Como {USER_ROLE}
Quiero {GOAL}
Para {BUSINESS_VALUE}
```

### Alcance

**Funcionalidades Principales:**
- {FEATURE_1}
- {FEATURE_2}
- {FEATURE_3}

**Componentes a Implementar:**
- {COMPONENT_1}
- {COMPONENT_2}
- {COMPONENT_3}

**Casos de Uso:**
1. {USE_CASE_1}
2. {USE_CASE_2}
3. {USE_CASE_3}

---

## 🚀 Setup del Proyecto

### 1. Crear Directorio del Proyecto

```bash
mkdir {PROJECT_DIR}
cd {PROJECT_DIR}
```

### 2. Inicializar Git

```bash
git init
git checkout -b develop
```

### 3. Crear Entorno Virtual

```bash
python -m venv venv

# Activar (Linux/macOS)
source venv/bin/activate

# Activar (Windows)
venv\Scripts\activate
```

### 4. Instalar Dependencias Base

```bash
# Crear requirements.txt
cat > requirements.txt << EOF
{STACK_DEPENDENCIES}
pytest>=7.0
pytest-bdd>=6.0
pylint>=2.15
EOF

pip install -r requirements.txt
```

### 5. Crear Estructura Base

```bash
{STACK_SPECIFIC_STRUCTURE_COMMANDS}
```

**Estructura del proyecto:**

```
{PROJECT_DIR}/
├── {STACK_STRUCTURE}
├── tests/
├── requirements.txt
└── README.md
```

---

## 📦 Instalación del Framework

### 1. Clonar Claude Dev Kit

```bash
# Clonar en ubicación global (si no lo tienes)
cd ~
git clone https://github.com/vvalotto/claude-dev-kit.git ~/.claude-dev-kit
```

### 2. Ejecutar Instalador

```bash
# Volver a tu proyecto
cd {PROJECT_DIR}

# Ejecutar instalador (modo no interactivo)
python ~/.claude-dev-kit/install/installer.py --profile {PROFILE_ID} --yes
```

**Salida esperada:**

```
✅ Framework instalado exitosamente en .claude/
✅ Perfil '{PROFILE_ID}' configurado
✅ Skills disponibles:
   - /implement-us
   - /track-pause, /track-resume, /track-status
✅ Templates instalados: bdd, planning, testing, reporting
```

### 3. Verificar Instalación

```bash
# Verificar estructura creada
ls -la .claude/

# Contenido esperado:
# .claude/
# ├── skills/
# │   └── implement-us/
# ├── templates/
# ├── tracking/
# └── config.json
```

---

## 🎬 Walkthrough: Las 10 Fases

### Preparación: Crear Archivo US

Primero, crea un archivo con la historia de usuario:

```bash
mkdir -p historias-usuario
cat > historias-usuario/US-{US_ID}.md << 'EOF'
# US-{US_ID}: {US_TITLE}

Como {USER_ROLE}
Quiero {GOAL}
Para {BUSINESS_VALUE}

## Criterios de Aceptación

{ACCEPTANCE_CRITERIA}
EOF
```

### Ejecutar el Skill

```bash
# En Claude Code, ejecutar:
/implement-us US-{US_ID}
```

---

### 🔍 Fase 0: Validación de Contexto

**Qué hace el framework:**
- ✅ Verifica que el archivo US-{US_ID}.md exista
- ✅ Lee el perfil {PROFILE_ID} desde `.claude/skills/implement-us/config.json`
- ✅ Valida que las dependencias estén instaladas
- ✅ Inicializa el tracking de tiempo

**Output:**

```
✅ Historia de usuario encontrada: US-{US_ID}
✅ Perfil cargado: {PROFILE_ID}
✅ Configuración:
   - Arquitectura: {ARCHITECTURE_PATTERN}
   - Test Framework: {TEST_FRAMEWORK}
   - Quality Gates: Activos
⏱️  Tracking iniciado para US-{US_ID}
```

**¿Qué hacer si falla?**
- Verifica que el archivo US-{US_ID}.md exista en `historias-usuario/`
- Confirma que la instalación del framework fue exitosa
- Revisa `.claude/skills/implement-us/config.json`

---

### 📝 Fase 1: Generación de Escenarios BDD

**Qué hace el framework:**
- 📄 Lee tu historia de usuario
- 🤖 Genera escenarios Gherkin basados en los criterios de aceptación
- 💾 Crea archivo `tests/bdd/US-{US_ID}.feature`

**Ejemplo de Output ({STACK_NAME}):**

```gherkin
{BDD_EXAMPLE_SNIPPET}
```

**Archivo creado:**
```
tests/bdd/US-{US_ID}.feature
```

**Interacción:**
- Claude te mostrará los escenarios generados
- Puedes pedir ajustes antes de continuar
- Checkpoint: ¿Aprobar escenarios? (Sí/No)

---

### 📋 Fase 2: Generación de Plan de Implementación

**Qué hace el framework:**
- 🏗️ Analiza los escenarios BDD
- 📊 Crea un plan de tareas desglosadas
- ⏱️ Estima tiempo por componente
- 🎯 Adapta la estructura al patrón {ARCHITECTURE_PATTERN}

**Ejemplo de Output ({STACK_NAME}):**

```markdown
{IMPLEMENTATION_PLAN_SNIPPET}
```

**Archivo creado:**
```
docs/planning/US-{US_ID}-plan.md
```

**Decisiones Clave:**
- Orden de implementación: {IMPLEMENTATION_ORDER}
- Componentes principales: {MAIN_COMPONENTS}
- Dependencias: {DEPENDENCIES}

---

### ⚙️ Fase 3: Implementación

**Qué hace el framework:**
- 💻 Guía la creación de cada componente según el plan
- 🔧 Usa snippets específicos del perfil {PROFILE_ID}
- 📁 Crea archivos en la estructura correcta
- ✅ Valida cada paso antes de continuar

**Componentes Creados ({STACK_NAME}):**

{IMPLEMENTATION_COMPONENTS_LIST}

**Ejemplo de Código Generado:**

{CODE_EXAMPLE_SNIPPET}

**Archivos creados:**
```
{FILES_CREATED_LIST}
```

**Características del Código:**
- ✅ Sigue el patrón {ARCHITECTURE_PATTERN}
- ✅ Usa las convenciones de {STACK_NAME}
- ✅ Incluye docstrings y type hints
- ✅ Preparado para testing

---

### 🧪 Fase 4: Tests Unitarios

**Qué hace el framework:**
- 🔬 Genera tests unitarios para cada componente
- 🎯 Usa {TEST_FRAMEWORK} configurado en el perfil
- ✅ Cubre lógica de negocio y casos edge
- 📊 Ejecuta tests y reporta cobertura

**Ejemplo de Tests ({STACK_NAME}):**

{UNIT_TEST_EXAMPLE}

**Ejecución:**

```bash
pytest tests/unit/ -v --cov={MAIN_MODULE} --cov-report=term-missing
```

**Output Esperado:**

```
{TEST_OUTPUT_EXAMPLE}
```

**Archivos creados:**
```
{UNIT_TEST_FILES}
```

---

### 🔗 Fase 5: Tests de Integración

**Qué hace el framework:**
- 🌐 Genera tests end-to-end
- 🔄 Valida integración entre componentes
- 🎭 Usa fixtures y mocks específicos de {STACK_NAME}

**Ejemplo de Tests ({STACK_NAME}):**

{INTEGRATION_TEST_EXAMPLE}

**Ejecución:**

```bash
pytest tests/integration/ -v
```

**Archivos creados:**
```
{INTEGRATION_TEST_FILES}
```

---

### ✅ Fase 6: Validación BDD

**Qué hace el framework:**
- 🥒 Genera step definitions para los escenarios Gherkin
- 🔗 Conecta los escenarios con el código real
- ✅ Ejecuta validación completa

**Ejemplo de Step Definitions:**

{BDD_STEPS_EXAMPLE}

**Ejecución:**

```bash
pytest tests/bdd/ -v --gherkin-terminal-reporter
```

**Output Esperado:**

```
{BDD_OUTPUT_EXAMPLE}
```

**Archivos creados:**
```
tests/bdd/steps/test_US-{US_ID}_steps.py
```

---

### 📊 Fase 7: Quality Gates

**Qué hace el framework:**
- 🔍 Ejecuta Pylint con umbrales del perfil
- 📈 Calcula complejidad ciclomática
- 🎯 Valida índice de mantenibilidad
- 📊 Verifica cobertura de tests

**Umbrales ({PROFILE_ID}):**

{QUALITY_GATES_THRESHOLDS}

**Ejecución:**

```bash
# Pylint
pylint {MAIN_MODULE}/ --fail-under={PYLINT_THRESHOLD}

# Complejidad
radon cc {MAIN_MODULE}/ -a

# Cobertura
pytest --cov={MAIN_MODULE} --cov-report=term --cov-fail-under={COVERAGE_THRESHOLD}
```

**Output Esperado:**

```
{QUALITY_GATES_OUTPUT}
```

**¿Qué hacer si fallan?**
- Refactoriza funciones complejas (CC > 10)
- Agrega tests para mejorar cobertura
- Corrige issues de Pylint

---

### 📚 Fase 8: Documentación

**Qué hace el framework:**
- 📖 Genera README.md del componente
- 🗂️ Crea documentación técnica
- 💡 Incluye ejemplos de uso
- 🏗️ Documenta decisiones arquitectónicas

**Archivos creados:**

```
docs/components/US-{US_ID}-{COMPONENT_NAME}.md
docs/architecture/ADR-{US_ID}.md
README.md (actualizado)
```

**Ejemplo de Documentación:**

{DOCUMENTATION_EXAMPLE}

---

### 📈 Fase 9: Reporte Final

**Qué hace el framework:**
- 📋 Consolida métricas de todas las fases
- ⏱️ Reporta tiempo real vs estimado
- ✅ Lista criterios de aceptación cumplidos
- 📊 Genera reporte completo

**Archivo creado:**

```
docs/reporting/US-{US_ID}-report.md
```

**Ejemplo de Reporte:**

```markdown
# Reporte de Implementación: US-{US_ID}

## 📊 Resumen Ejecutivo

- **Estado:** ✅ Completado
- **Tiempo Total:** {ACTUAL_TIME} (estimado: {ESTIMATED_TIME})
- **Tests:** {TESTS_PASSED}/{TESTS_TOTAL} pasando
- **Cobertura:** {COVERAGE}%
- **Quality Gates:** ✅ Todos aprobados

## 📝 Componentes Implementados

{COMPONENTS_LIST}

## 🧪 Testing

- Tests Unitarios: {UNIT_TESTS_COUNT} (100% passing)
- Tests Integración: {INTEGRATION_TESTS_COUNT} (100% passing)
- Escenarios BDD: {BDD_SCENARIOS_COUNT} (100% passing)

## 📊 Métricas de Calidad

- Pylint: {PYLINT_SCORE}/10
- Complejidad: {CC_AVG} (promedio)
- Mantenibilidad: {MI_INDEX}
- Cobertura: {COVERAGE}%

## ✅ Criterios de Aceptación

{ACCEPTANCE_CRITERIA_STATUS}
```

**Tracking de Tiempo:**

```bash
# Ver reporte detallado
/track-report US-{US_ID}
```

---

## ✅ Validación Final

### Checklist Completo

Verifica que todos los entregables estén completos:

**Código:**
- [ ] Todos los componentes implementados
- [ ] Código sigue el patrón {ARCHITECTURE_PATTERN}
- [ ] Docstrings y type hints presentes

**Tests:**
- [ ] Tests unitarios al 100% passing
- [ ] Tests de integración al 100% passing
- [ ] Escenarios BDD validados

**Calidad:**
- [ ] Pylint >= {PYLINT_THRESHOLD}
- [ ] Complejidad Ciclomática < 10
- [ ] Cobertura >= {COVERAGE_THRESHOLD}%

**Documentación:**
- [ ] README actualizado
- [ ] Documentación técnica creada
- [ ] ADRs documentados

**Tracking:**
- [ ] Reporte de tiempo generado
- [ ] Métricas capturadas

### Ejecutar Aplicación

{RUN_APPLICATION_COMMANDS}

### Verificación Manual

{MANUAL_VERIFICATION_STEPS}

---

## 🔧 Troubleshooting

### Problema: El skill /implement-us no se encuentra

**Solución:**
```bash
# Verificar instalación
ls -la .claude/skills/implement-us/

# Re-ejecutar instalador si es necesario
python ~/.claude-dev-kit/install/installer.py --profile {PROFILE_ID} --yes
```

### Problema: Tests fallan con imports

**Solución:**
```bash
# Asegurar que el módulo esté en PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# O instalar el paquete en modo desarrollo
pip install -e .
```

### Problema: Quality gates fallan

**Solución:**

```bash
# Ver issues específicos
pylint {MAIN_MODULE}/ --reports=y

# Refactorizar funciones complejas
# Agregar tests para mejorar cobertura
```

### Problema: Claude no genera código esperado

**Solución:**
- Verifica que el perfil {PROFILE_ID} esté configurado correctamente
- Lee `.claude/skills/implement-us/config.json`
- Asegúrate de que la historia de usuario sea clara y específica

### Problema: Errores de dependencias

**Solución:**
```bash
# Reinstalar dependencias
pip install --upgrade -r requirements.txt

# Verificar versiones
pip list | grep {STACK_PACKAGE}
```

---

## 🚀 Próximos Pasos

### Ampliar la Aplicación

Ahora que tienes la base funcionando, puedes:

1. **Agregar más funcionalidades:**
   - Crear nuevas historias de usuario
   - Ejecutar `/implement-us US-XXX` para cada una

2. **Mejorar la arquitectura:**
   - Refactorizar usando patrones avanzados
   - Agregar capas adicionales (caching, logging)

3. **Optimizar testing:**
   - Agregar tests de performance
   - Implementar CI/CD

4. **Deploy:**
   - {STACK_SPECIFIC_DEPLOYMENT_TIPS}

### Explorar Otros Perfiles

El Claude Dev Kit soporta múltiples stacks:

- **PyQt-MVC:** Apps de escritorio
- **FastAPI-REST:** APIs async de alto rendimiento
- **Flask-REST:** APIs REST simples
- **Flask-WebApp:** Aplicaciones web fullstack
- **Generic-Python:** Proyectos Python genéricos

Puedes instalar otro perfil con:

```bash
python ~/.claude-dev-kit/install/installer.py --profile {OTHER_PROFILE} --yes
```

### Contribuir al Framework

Si encuentras formas de mejorar el framework:
- Reporta issues en GitHub
- Propón mejoras a los templates
- Comparte tus propios perfiles customizados

---

## 📚 Recursos

### Documentación del Framework

- [Guía de Inicio Rápido](../../user/Getting-Started.md)
- [Referencia del Skill implement-us](../../user/Implement-US-Skill.md)
- [Sistema de Tracking](../../user/Tracking-Guide.md)
- [Personalización de Perfiles](../../user/Customization.md)

### Documentación de {STACK_NAME}

{STACK_SPECIFIC_RESOURCES}

### Comunidad

- GitHub: https://github.com/vvalotto/claude-dev-kit
- Issues: https://github.com/vvalotto/claude-dev-kit/issues
- Discussions: https://github.com/vvalotto/claude-dev-kit/discussions

---

## 📝 Conclusión

¡Felicidades! Has completado tu primer proyecto usando el Claude Dev Kit con el perfil **{PROFILE_ID}**.

**Lo que aprendiste:**
- ✅ Instalación y configuración del framework
- ✅ Uso del skill `/implement-us` para guiar implementación
- ✅ Cómo el framework adapta las 10 fases a tu stack
- ✅ Generación automática de BDD, tests y documentación
- ✅ Validación de calidad con quality gates
- ✅ Tracking de tiempo y métricas

**Siguiente paso:** Aplica este mismo proceso a tus propios proyectos. El framework está diseñado para escalar desde prototipos hasta aplicaciones de producción.

---

**Tutorial Creado:** {CREATION_DATE}
**Claude Dev Kit:** v1.0
**Perfil:** {PROFILE_ID}
