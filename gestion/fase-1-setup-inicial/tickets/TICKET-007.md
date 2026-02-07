# TICKET-007: Configurar .gitignore optimizado

**Fase:** 1 - Setup Inicial
**Sprint:** 1
**Estado:** TODO
**Prioridad:** Media
**Estimación:** 15 minutos
**Asignado a:** Claude Code

## Descripción

Revisar y optimizar el archivo .gitignore actual para asegurar que excluye todos los archivos y directorios que no deben estar en control de versiones, especialmente para un proyecto framework Python.

El .gitignore actual es bastante completo (viene del template de Python), pero hay que verificar y posiblemente agregar exclusiones específicas para este proyecto.

## Criterios de Aceptación

- [ ] .gitignore incluye exclusiones estándar de Python (`__pycache__/`, `*.pyc`, etc.)
- [ ] Excluye directorios de entornos virtuales (`.venv/`, `venv/`, `env/`)
- [ ] Excluye archivos de IDEs (`.idea/`, `.vscode/`)
- [ ] Excluye logs (`*.log`, `logs/`)
- [ ] Excluye archivos de testing (`htmlcov/`, `.coverage`, `.pytest_cache/`)
- [ ] Considera excluir `_work/` si es temporal (decisión a tomar)
- [ ] Incluye exclusiones específicas para el framework si necesario
- [ ] No excluye archivos que SÍ deben estar versionados
- [ ] Testeado que no commitea archivos no deseados

## Dependencias

- **Depende de:** TICKET-002 (repositorio clonado)
- **Bloquea a:** TICKET-010 (primer commit)

## Notas Técnicas

### .gitignore Actual

El .gitignore actual ya es bastante completo. Revisar especialmente:

1. **¿Debe incluirse `_work/` en git?**
   - PRO: Es material de referencia útil para el desarrollo
   - CONTRA: Son archivos de trabajo temporal de migración
   - **Decisión recomendada:** INCLUIR en git (es documentación valiosa)

2. **¿Debe incluirse `.idea/` en git?**
   - Actualmente comentado en el .gitignore
   - **Decisión recomendada:** EXCLUIR (es configuración específica del IDE)

3. **Exclusiones adicionales específicas del framework:**
   - `.claude/tracking/*.json` (datos de tracking generados)
   - `.claude/logs/` (logs generados)
   - Estos se aplicarán en proyectos que USEN el kit, no en el kit mismo

### Verificación

Después de modificar .gitignore:
```bash
# Ver qué archivos se trackearían
git status

# Ver qué archivos están siendo ignorados
git status --ignored

# Verificar que no haya archivos sensibles
git ls-files
```

## Checklist de Implementación

- [ ] Leer .gitignore actual completamente
- [ ] Decidir sobre `_work/` (incluir o excluir)
- [ ] Descomentar exclusión de `.idea/` si está comentada
- [ ] Verificar que todas las exclusiones estándar de Python están
- [ ] Agregar exclusiones específicas si necesario
- [ ] Testear con `git status` que no incluye archivos no deseados
- [ ] Documentar decisiones tomadas

## Resultado

_A completar al finalizar._
