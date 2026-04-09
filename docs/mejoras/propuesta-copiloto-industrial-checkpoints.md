# Propuesta de Solución — Copiloto Industrial con Checkpoints Humanos

Fecha: 2026-03-08
Estado: Propuesta inicial

## 1) Gate de entrada obligatorio

**Debilidad que resuelve:** Automatización iniciada sin condiciones mínimas verificadas.

**Propuesta de solución:**
- Agregar un `preflight gate` antes de Fase 0.
- El flujo `/implement-us` se bloquea si no existe evidencia de:
  - HU validada.
  - BDD aprobado (o excepción explícita justificada).
- Resultado del gate: `PASS` o `BLOCKED`.

**Implementación sugerida:**
- Nuevo comando: `python .claude/tracking/track.py preflight-check {US_ID}`.
- Salida en JSON: `.claude/tracking/{US_ID}-preflight.json`.

**Criterio de aceptación:**
- Si falta evidencia, el skill no arranca y muestra mensaje de bloqueo claro.

---

## 2) Contrato de precondiciones en archivo

**Debilidad que resuelve:** Precondiciones implícitas sin trazabilidad.

**Propuesta de solución:**
- Crear plantilla obligatoria `docs/plans/{US_ID}-precheck.md`.
- Campos mínimos:
  - Fuente HU.
  - Responsable de validación.
  - Fecha de validación.
  - Estado BDD.
  - Riesgos conocidos.

**Implementación sugerida:**
- Nuevo template en `.claude/templates/planning/precheck.md`.
- Fase 0 valida que el archivo exista y tenga secciones completas.

**Criterio de aceptación:**
- No se puede avanzar a Fase 1 sin `precheck.md` completo.

---

## 3) Checkpoints humanos con evidencia mínima

**Debilidad que resuelve:** Aprobaciones superficiales.

**Propuesta de solución:**
- Estandarizar paquete de evidencia por checkpoint.
- Evidencia mínima obligatoria:
  - Resumen del diff.
  - Tests ejecutados y resultado.
  - Cobertura.
  - Impacto arquitectónico.
  - Riesgo y rollback.

**Implementación sugerida:**
- Archivo por checkpoint: `docs/reviews/{US_ID}-phase-{N}.md`.
- Bloquear continuidad si faltan secciones requeridas.

**Criterio de aceptación:**
- Cada STOP tiene evidencia verificable y aprobación explícita.

---

## 4) Matriz de riesgo por tipo de cambio

**Debilidad que resuelve:** Misma autonomía para cambios con riesgo distinto.

**Propuesta de solución:**
- Definir matriz de riesgo:
  - `LOW`: cambios internos sin impacto externo.
  - `MEDIUM`: cambio funcional acotado.
  - `HIGH`: seguridad, datos, contratos públicos, performance crítica.
- Reglas:
  - `LOW`: aprobación estándar.
  - `MEDIUM`: aprobación + evidencia ampliada.
  - `HIGH`: doble aprobación humana.

**Implementación sugerida:**
- Config en `.claude/config.json` con `risk_policy`.
- Clasificación automática inicial + confirmación humana en Fase 0.

**Criterio de aceptación:**
- Todo `HIGH` requiere doble aprobación antes de merge.

---

## 5) Guardrails para acciones peligrosas

**Debilidad que resuelve:** Riesgo operativo en acciones sensibles.

**Propuesta de solución:**
- Lista de acciones bloqueadas por defecto:
  - Migraciones destructivas.
  - Operaciones sobre secretos.
  - Cambios en entorno productivo.
- Solo habilitables con excepción documentada.

**Implementación sugerida:**
- Archivo de política: `.claude/policies/operations-policy.yaml`.
- Hook de validación previo a ejecutar comandos sensibles.

**Criterio de aceptación:**
- Ninguna acción sensible se ejecuta sin aprobación explícita registrada.

---

## 6) Alineación documentación vs ejecución

**Debilidad que resuelve:** Inconsistencias entre lo que se documenta y lo que realmente corre.

**Propuesta de solución:**
- Test automático de consistencia documental.
- Verifica:
  - Comandos referenciados existen.
  - Rutas de artefactos existen o se crean.
  - Nombres de fases y archivos coinciden.

**Implementación sugerida:**
- Nuevo test: `tests/test_docs_consistency.py`.
- Ejecutarlo en CI en cada PR.

**Criterio de aceptación:**
- CI falla si un comando/ruta de docs no es válido.

---

## 7) Validación automática de artefactos críticos

**Debilidad que resuelve:** Avance de fase sin artefactos obligatorios.

**Propuesta de solución:**
- Gate por fase con verificación de artefactos requeridos.
- Ejemplo:
  - Fase 0: `context.md`.
  - Fase 2: `plan.md`.
  - Fase 7: reporte de calidad.
  - Fase 9: reporte final.

**Implementación sugerida:**
- Declarar requisitos en `skills/implement-us/config.json` por fase.
- Función común de validación de artefactos reutilizable.

**Criterio de aceptación:**
- No se avanza si falta un artefacto requerido.

---

## 8) Auditoría completa de decisiones

**Debilidad que resuelve:** Falta de rastro para compliance y postmortem.

**Propuesta de solución:**
- Bitácora estructurada por fase con:
  - Decisión automática propuesta.
  - Evidencia usada.
  - Decisión final humana.
  - Timestamp y responsable.

**Implementación sugerida:**
- Archivo JSONL: `.claude/tracking/{US_ID}-audit.jsonl`.
- Cada evento se agrega en tiempo real.

**Criterio de aceptación:**
- Puede reconstruirse todo el flujo de decisiones de una US.

---

## 9) Quality gates de producto (además de técnicos)

**Debilidad que resuelve:** Calidad técnica sin validar valor de negocio.

**Propuesta de solución:**
- Incluir gates no técnicos:
  - Criterios de negocio cumplidos.
  - UX mínima (si aplica).
  - Seguridad (checklist OWASP básico).
  - Performance (SLO mínimo definido).

**Implementación sugerida:**
- Plantilla `docs/reviews/{US_ID}-product-gates.md`.
- Fase 7 o 8 exige ese documento con estado `PASS/BLOCKED`.

**Criterio de aceptación:**
- No cerrar la US sin aprobación de gates de producto.

---

## 10) Protocolo de recuperación y rollback

**Debilidad que resuelve:** Manejo inconsistente de fallos en ejecución.

**Propuesta de solución:**
- Definir protocolo único ante falla:
  - Identificar causa raíz.
  - Ejecutar rollback según tipo de cambio.
  - Reintentar máximo 2 veces.
  - Escalar a humano si persiste.

**Implementación sugerida:**
- Playbook: `docs/user/recovery-and-rollback.md`.
- Registro obligatorio en auditoría cuando ocurre rollback.

**Criterio de aceptación:**
- Toda falla crítica deja evidencia de recuperación y estado final.

---

## Prioridad de implementación recomendada

1. Gate de entrada + contrato de precondiciones.
2. Checkpoints con evidencia + validación de artefactos.
3. Guardrails + matriz de riesgo.
4. Auditoría completa.
5. Quality gates de producto.
6. Protocolo de rollback.
7. Test de consistencia documentación/ejecución.

## Resultado esperado

Con estas mejoras, el sistema pasa de "automatización guiada" a "copiloto industrial controlado", manteniendo velocidad pero con mayor seguridad, trazabilidad y calidad de decisión.
