# Guía para Crear Skills Personalizados

**Última Actualización:** 2026-02-15
**Audiencia:** Desarrollador / Contributor
**Nivel:** Avanzado

---

## Introducción

Esta guía te enseña a crear skills personalizados para extender la funcionalidad de Claude Dev Kit.

**¿Qué es un skill?**
Un skill es un comando ejecutable (ej: `/mi-skill`) que realiza una tarea específica, puede tener múltiples fases, y se integra con el sistema de tracking.

---

## Anatomía de un Skill

### Estructura de Archivos

```
.claude/skills/mi-skill/
├── skill.md           # Definición principal del skill
├── config.json        # Configuración base
├── phases/            # Fases del skill (opcional)
│   ├── phase-0.md
│   ├── phase-1.md
│   └── phase-2.md
└── customizations/    # Perfiles custom (opcional)
    ├── profile-1.json
    └── profile-2.json
```

---

## Crear Skill Básico

### Paso 1: Crear Directorio

```bash
mkdir -p .claude/skills/mi-skill
cd .claude/skills/mi-skill
```

### Paso 2: Crear skill.md

```markdown
# Skill: mi-skill

**Versión:** 1.0.0
**Autor:** Tu Nombre
**Descripción:** Descripción breve del skill

---

## Uso

\```bash
/mi-skill [opciones]
\```

## Instrucciones

Cuando este skill se ejecute:

1. Realizar acción X
2. Generar output Y
3. Validar Z

## Fases

### Fase 0: Preparación

Preparar contexto necesario...

### Fase 1: Ejecución

Ejecutar tarea principal...

### Fase 2: Finalización

Generar reporte final...
```

### Paso 3: Crear config.json

```json
{
  "name": "mi-skill",
  "version": "1.0.0",
  "description": "Mi skill custom",
  "enabled": true,
  "phases": {
    "total": 3
  },
  "options": {
    "flag1": {
      "type": "boolean",
      "default": true,
      "description": "Opción 1"
    }
  }
}
```

### Paso 4: Registrar Skill

En `.claude/config.json`:

```json
{
  "skills": {
    "implement-us": { ... },
    "mi-skill": {
      "enabled": true,
      "config_path": ".claude/skills/mi-skill/config.json"
    }
  }
}
```

---

## Skill con Múltiples Fases

### Arquitectura Modular

```
mi-skill/
├── skill.md           # Orquestador
└── phases/
    ├── phase-0.md     # Fase independiente
    ├── phase-1.md
    └── phase-2.md
```

### skill.md (Orquestador)

```markdown
# Skill: Deployment Automation

## Fases

Este skill ejecuta 3 fases:

0. **Pre-deployment:** Validación de código
1. **Deploy:** Despliegue a staging
2. **Post-deployment:** Tests de smoke

Ver detalles en `phases/phase-X.md`

## Flujo de Ejecución

1. Claude ejecuta Fase 0
2. Usuario aprueba
3. Claude ejecuta Fase 1
4. Usuario valida en staging
5. Claude ejecuta Fase 2
```

### phases/phase-0.md

```markdown
# Fase 0: Pre-deployment

## Objetivo

Validar que el código está listo para despliegue.

## Instrucciones

1. Ejecutar linter:
   \```bash
   pylint src/
   \```

2. Ejecutar tests:
   \```bash
   pytest tests/
   \```

3. Validar coverage:
   \```bash
   pytest --cov=src tests/
   \```

## Criterios de Éxito

- Pylint score ≥ 8.0
- Todos los tests pasan
- Coverage ≥ 90%
```

---

## Integración con Tracking

### Auto-tracking

En skill.md, especifica tracking:

```markdown
## Tracking

Este skill usa tracking automático:

- Fase 0: Estimado 5 min
- Fase 1: Estimado 10 min
- Fase 2: Estimado 5 min

Total: ~20 minutos
```

Claude Code detectará esto y trackeará automáticamente.

---

## Sistema de Variables

Usa variables en tu skill:

```markdown
## Fase 1: Deploy

Desplegar {PROJECT_NAME} a {ENVIRONMENT}:

\```bash
docker build -t {PROJECT_NAME}:{VERSION} .
docker push {REGISTRY}/{PROJECT_NAME}:{VERSION}
kubectl apply -f k8s/{ENVIRONMENT}/
\```
```

**Variables disponibles:**
- `{PROJECT_NAME}` - Nombre del proyecto
- `{VERSION}` - Versión actual
- `{ENVIRONMENT}` - staging, production
- `{USER}` - Usuario actual

---

## Perfiles de Customización

Crea variantes del skill por contexto:

### customizations/aws.json

```json
{
  "profile_name": "aws-deployment",
  "environment": "aws",
  "commands": {
    "deploy": "aws deploy push ...",
    "validate": "aws cloudformation validate-template ..."
  }
}
```

### customizations/gcp.json

```json
{
  "profile_name": "gcp-deployment",
  "environment": "gcp",
  "commands": {
    "deploy": "gcloud app deploy ...",
    "validate": "gcloud builds submit ..."
  }
}
```

---

## Ejemplos Completos

### Skill: Code Review Automation

```markdown
# Skill: code-review

## Uso
\```bash
/code-review [--pr PR_NUMBER]
\```

## Fases

### Fase 0: Fetch PR
Obtener diff del PR usando gh CLI

### Fase 1: Static Analysis
Ejecutar Pylint, mypy, bandit

### Fase 2: Generate Report
Generar reporte con findings

## Instrucciones

1. Obtener diff:
   \```bash
   gh pr diff {PR_NUMBER}
   \```

2. Ejecutar análisis:
   \```bash
   pylint --output-format=json $(git diff --name-only main)
   \```

3. Generar reporte markdown con findings
```

### Skill: Database Migration

```markdown
# Skill: db-migrate

## Uso
\```bash
/db-migrate --version VERSION [--dry-run]
\```

## Fases

### Fase 0: Backup
Crear backup de BD actual

### Fase 1: Validation
Validar scripts de migración

### Fase 2: Execution
Ejecutar migración

### Fase 3: Verification
Verificar integridad post-migración

## Safety

- Requiere aprobación manual antes de Fase 2
- Dry-run disponible
- Rollback automático si falla
```

---

## Best Practices

### 1. Documentación Clara

```markdown
# Skill: mi-skill

**Qué hace:** Una línea clara
**Cuándo usarlo:** Casos de uso
**Prerequisitos:** Dependencias
```

### 2. Fases Atómicas

Cada fase debe ser:
- Independiente
- Reversible si es posible
- Con criterios de éxito claros

### 3. Manejo de Errores

```markdown
## Si falla la Fase 1

1. Revisar logs en .claude/logs/
2. Validar prerequisitos
3. Re-intentar con --verbose
```

### 4. Testing

Crear tests para tu skill:

```bash
# Dry-run
/mi-skill --dry-run

# Test con datos de prueba
/mi-skill --test-mode
```

---

## Publicar Skill

### 1. Repositorio

```bash
# Crear repo del skill
mkdir claude-skill-mi-skill
cd claude-skill-mi-skill

# Copiar archivos
cp -r .claude/skills/mi-skill/* .

# README
cat > README.md << 'EOF'
# Claude Skill: Mi Skill

Descripción, instalación, uso
EOF

# Publicar
git init
git add .
git commit -m "Initial commit"
git push origin main
```

### 2. Instalación por Usuarios

```bash
# Clonar skill
git clone https://github.com/usuario/claude-skill-mi-skill \
  .claude/skills/mi-skill

# Registrar en config
# Editar .claude/config.json
```

---

## Troubleshooting

### Skill no aparece

**Verificar:**
```bash
# Existe el directorio
ls .claude/skills/mi-skill/

# Registrado en config
cat .claude/config.json | grep mi-skill

# Reiniciar Claude Code
```

### Variables no se reemplazan

**Usar sintaxis correcta:**
```markdown
{VARIABLE}      # ✅ Correcto
{{VARIABLE}}    # ❌ Incorrecto
$VARIABLE       # ❌ Incorrecto
```

---

## Recursos Adicionales

- [Skill implement-us](user/skills/Implement-Us) - Skill de referencia
- [Sistema de Templates](developer/architecture/Template-System) - Variables
- [Tracking](developer/architecture/Tracking) - Integración tracking

---

**Anterior:** [Skill implement-us](user/skills/Implement-Us)
**Siguiente:** [README Principal](../../../README.md)
**Índice:** [Volver al índice](Documentation-Index)
