# TICKET-063: Validación y Quality Gates ✅

**Fase:** 8 - Testing del Framework
**Sprint:** 5
**Estado:** ⏳ Pendiente
**Prioridad:** Alta
**Estimación:** 1 hora
**Asignado a:** Claude Code

---

## 🎯 Objetivo

Ejecutar la suite completa de tests, verificar cobertura de código, aplicar pylint sobre el código del framework, y documentar los resultados en un informe de validación.

---

## 📋 Tareas

### 1. Ejecutar Suite Completa (10 min)

```bash
# Ejecutar todos los tests
pytest tests/ -v

# Verificar: 0 failures, 0 errors
# Esperado: ~85 tests (23 + 37 + 25)
```

**Criterio:** 100% de tests pasan (0 failures, 0 errors)

### 2. Verificar Cobertura de Código (15 min)

```bash
# Cobertura del instalador
pytest --cov=install --cov-report=term-missing tests/test_installer.py tests/test_config_merge.py

# Cobertura del tracking
pytest --cov=tracking --cov-report=term-missing tests/test_tracking.py

# Reporte HTML completo
pytest --cov=install --cov=tracking --cov-report=html tests/
```

**Criterios:**
- `install/installer.py` → ≥ 90%
- `tracking/time_tracker.py` → ≥ 95%
- Si no se alcanzan: agregar tests faltantes antes de continuar

### 3. Pylint sobre Código del Framework (15 min)

```bash
# Pylint en módulos del framework
pylint install/installer.py tracking/time_tracker.py tracking/reports.py tracking/commands.py

# Pylint en los tests
pylint tests/test_installer.py tests/test_tracking.py tests/test_config_merge.py
```

**Criterio:** Pylint ≥ 8.0/10 en todos los archivos

### 4. Identificar y Corregir Gaps (10 min)

Si algún criterio no se cumple:
- [ ] Cobertura < mínimo → Agregar tests para las líneas no cubiertas
- [ ] Pylint < 8.0 → Corregir issues en código de tests (no en framework)
- [ ] Tests fallando → Investigar y corregir

### 5. Crear VALIDATION-REPORT.md (10 min)

Documentar resultados reales (con outputs copiados directamente de la terminal):

```markdown
# VALIDATION-REPORT.md - Fase 8: Testing del Framework

## Resultados de pytest

\`\`\`
pytest tests/ -v
... (output real)
85 passed in X.XXs
\`\`\`

## Cobertura de Código

| Módulo | Statements | Missing | Coverage |
|--------|-----------|---------|----------|
| install/installer.py | XX | X | XX% |
| tracking/time_tracker.py | XX | X | XX% |

## Pylint

| Archivo | Score |
|---------|-------|
| install/installer.py | X.XX/10 |
| tracking/time_tracker.py | X.XX/10 |
| tests/test_installer.py | X.XX/10 |
| tests/test_tracking.py | X.XX/10 |
| tests/test_config_merge.py | X.XX/10 |
```

### 6. Actualizar Estado en `gestion/` (5 min)

- [ ] `sprint-5.md` — Todos los tickets a ✅ Completado
- [ ] `CLAUDE.md` raíz — Actualizar Fase 8 a ✅ (100%)
- [ ] `session-current.md` — Actualizar próximos pasos

---

## 🎯 Criterios de Aceptación

- [ ] **Suite completa pasa** — `pytest tests/` → X passed, 0 failed, 0 error
- [ ] **Cobertura installer ≥ 90%** — pytest-cov lo confirma
- [ ] **Cobertura tracking ≥ 95%** — pytest-cov lo confirma
- [ ] **Pylint ≥ 8.0** — En código del framework y tests
- [ ] **VALIDATION-REPORT.md creado** — Con outputs reales de las herramientas
- [ ] **sprint-5.md actualizado** — 5/5 tickets completados (100%)

---

## 📤 Output

1. `gestion/fase-8-testing/VALIDATION-REPORT.md` — Resultados reales de validación
2. `sprint-5.md` actualizado — 5/5 tickets (100%)
3. `CLAUDE.md` actualizado — Fase 8 marcada como ✅

---

## 🔗 Dependencias

- **Depende de:** TICKET-060, TICKET-061, TICKET-062
- **Bloquea a:** TICKET-064 (primer ticket de Fase 9, si existe)

---

## 📝 Notas Técnicas

### Comando unificado de cobertura

```bash
# Desde la raíz del proyecto
pytest tests/ \
  --cov=install \
  --cov=tracking \
  --cov-report=term-missing \
  --cov-report=html:htmlcov \
  -v
```

### Interpretación de cobertura

- **Statements** = líneas ejecutables
- **Missing** = líneas no ejecutadas por ningún test
- Si `elapsed_seconds` calculado en bloques `if` no se cubre, agregar test con tiempo simulado

### Umbrales de Pylint por contexto

El código de tests naturalmente tiene menor puntuación que el código de producción porque:
- Muchos `assert` repetitivos
- Nombres de tests largos
- Uso de fixtures como parámetros

Umbral razonable para tests: **≥ 7.5/10**
Umbral para código de framework: **≥ 8.0/10**

---

## ✅ Resultado

_Se completará cuando el ticket esté DONE_

**Estado:** ⏳ Pendiente

---

**Creado:** 2026-02-17
**Depende de:** TICKET-060, TICKET-061, TICKET-062
