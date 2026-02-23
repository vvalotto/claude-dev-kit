# Registro de Proceso: implement-us

---

## 2026-02-22

### Observaciones - Primera ejecución de `/implement-us HU-003`

#### OBS-001: Tracking no se ejecuta

**Problema:** Las instrucciones de tracking en cada `phase-X.md` están escritas como
fragmentos de código Python a modo de ejemplo. El agente las interpreta como documentación
y no las ejecuta.

**Impacto:** No hay registro de tiempo por fase ni por tarea.

**Mejora propuesta:** Reescribir las instrucciones de tracking como directivas imperativas
en lenguaje natural. Ejemplo:
> **ANTES de comenzar cualquier acción de esta fase, ejecutá el tracking:**
> `python .claude/tracking/time_tracker.py start --phase 0 --us HU-003`

Adicionalmente, agregar una sección `## ✅ Checklist de Salida` al final de cada fase
con items que el agente debe confirmar explícitamente antes de avanzar:
- [ ] Output del archivo generado y guardado en la ruta correcta
- [ ] Tracking de fase cerrado
- [ ] Aprobación del usuario obtenida (si `approval_required: true`)

---

#### OBS-002: Output obligatorio de Fase 2 no se genera

**Problema:** La Fase 2 define que debe generarse un archivo `docs/plans/HU-003-plan.md`
y requerir aprobación del usuario antes de implementar. El agente leyó el archivo de fase
pero avanzó sin crear el documento ni solicitar aprobación.

**Impacto:** Se pierde el punto de control más importante del proceso: el usuario no puede
revisar ni ajustar el plan antes de que empiece la implementación.

**Mejora propuesta:** Agregar al final de `phase-2-planning.md` una sección con bloqueo
explícito:
> **🚫 STOP - No avances a Fase 3 hasta que:**
> 1. El archivo `docs/plans/{US_ID}-plan.md` exista en disco
> 2. El usuario haya respondido con aprobación explícita

---

#### OBS-003: Decisión de BDD queda a cargo del usuario

**Problema:** La bandera `--skip-bdd` debe ser indicada manualmente por el usuario.
Si no la especifica, el agente ejecuta Fase 1 (BDD) siempre, incluso cuando no tiene
sentido (refactorizaciones, correcciones de code smells, etc.).

**Impacto:** El usuario debe conocer el flag y recordar usarlo, o perder tiempo en
escenarios BDD irrelevantes.

**Mejora propuesta:** Incorporar en **Fase 0** un criterio de decisión automático:

| Tipo de HU | ¿BDD tiene sentido? |
|------------|---------------------|
| Nueva funcionalidad | ✅ Sí |
| Mejora de comportamiento existente | ✅ Sí |
| Refactorización (sin cambio de comportamiento) | ❌ No |
| Eliminación de code smells | ❌ No |
| Cambio de arquitectura interna | ❌ No |
| Corrección de bug | ⚠️ Depende |

El agente debe analizar la HU en Fase 0, determinar el tipo, y decidir
automáticamente si aplica BDD. Informar al usuario la decisión y su justificación,
permitiendo que la override si lo desea.

---

#### OBS-005: Fase 9 no exige explícitamente generar el archivo de reporte

**Problema:** `phase-9-final-report.md` describe el contenido del reporte y provee
templates, pero no instruye al agente de forma imperativa a crear el archivo
`docs/reports/{US_ID}-report.md` en disco antes de cerrar el tracking.
Es el mismo patrón que OBS-002 y OBS-004 pero aplicado a la fase final.

**Impacto:** El proceso puede cerrarse sin que quede evidencia persistente de la
implementación. El reporte es el artefacto de cierre más importante: consolida
métricas, criterios de aceptación, lecciones aprendidas y el estado final de la HU.

**Mejora propuesta:** Agregar al inicio de `phase-9-final-report.md` una instrucción
imperativa equivalente a la de Fase 2:
> **ANTES de cerrar el tracking, el archivo `docs/reports/{US_ID}-report.md`
> debe existir en disco. Verificá con `ls docs/reports/{US_ID}-report.md`.
> Si no existe, generalo siguiendo el template antes de continuar.**

**Relación:** Aplica el mismo principio de OBS-002 y OBS-004 — los outputs
obligatorios de cada fase deben estar verificados en disco antes de avanzar.

---

#### OBS-004: Comportamiento inconsistente entre ejecuciones

**Problema:** El mismo agente puede seguir el proceso correctamente en una ejecución
y saltear pasos en otra, sin que haya un error explícito que lo detecte. En HU-003,
en el primer intento no se generó el archivo de plan (`docs/plans/HU-003-plan.md`);
en el segundo intento sí. No hubo una decisión consciente diferente — simplemente
la ausencia de instrucciones imperativas permitió ambos comportamientos.

**Impacto:** El proceso no es reproducible ni auditable. Dependiendo de la ejecución,
el usuario puede o no tener un plan para revisar antes de la implementación.

**Relación:** Amplía OBS-002. No alcanza con definir el output en el template —
el skill debe instruir explícitamente al agente a verificar que el archivo existe
en disco antes de continuar a la siguiente fase.

**Mejora propuesta:** Agregar al final de cada fase con output obligatorio:
> **VERIFICACIÓN OBLIGATORIA:** Antes de continuar, confirmá que el archivo
> `{ruta_output}` existe ejecutando: `ls {ruta_output}`. Si no existe, generalo
> antes de avanzar.

**Propósito adicional del archivo de plan:** El archivo `docs/plans/{US_ID}-plan.md`
no es solo un artefacto para revisión del usuario — es el **mecanismo de memoria de
la implementación**. Durante la Fase 3, el agente debe leer ese archivo al inicio de
cada tarea para mantener coherencia con lo planificado, registrar el progreso
(marcar checkboxes), y no depender de reconstruir el contexto desde cero en cada
paso. Sin el archivo, el agente trabaja "de memoria" y es propenso a desviarse del
plan original.

Esto implica que la instrucción en `phase-3-implementation.md` debe comenzar con:
> **ANTES de implementar cada tarea, leé `docs/plans/{US_ID}-plan.md` y marcá la
> tarea como en progreso. Al completarla, actualizá el checkbox correspondiente.**

---

#### OBS-006: No existe una definición centralizada de rutas de artefactos

**Problema:** Cada archivo de fase menciona rutas de salida de forma dispersa, incompleta
y no siempre consistente. No existe un lugar único y autoritativo que defina la estructura
de directorios y los nombres de archivo para todos los artefactos generados durante la
ejecución del skill.

Estado actual relevado:
- Fase 1: genera archivos `.feature` — ruta no especificada
- Fase 2: genera plan de implementación — ruta propuesta en OBS-002 pero no definida en el archivo de fase
- Fase 7: menciona `quality/reports/{US_ID}-*.json` — parcialmente definido
- Fase 8: genera documentación — sin ruta definida
- Fase 9: genera reporte final — ruta propuesta en OBS-005 pero no definida en el archivo de fase

**Impacto:**
- El agente inventa o asume rutas en cada ejecución → inconsistencia entre ejecuciones del mismo skill
- Fase N+1 no sabe dónde buscar el output de Fase N → depende del contexto en memoria de la sesión
- Si la sesión se interrumpe, no hay forma de determinar qué artefactos ya existen y en qué estado

**Mejora propuesta:** Definir en un único lugar (candidato: `skill.md` o un archivo
`artifacts.md` dedicado) la estructura completa de directorios y convención de nombres
para todos los artefactos del skill:

```
docs/
  bdd/{US_ID}.feature          # Fase 1 — Escenarios BDD
  plans/{US_ID}-plan.md        # Fase 2 — Plan de implementación
  reports/{US_ID}-report.md    # Fase 9 — Reporte final
quality/
  reports/{US_ID}-pylint.json  # Fase 7 — Análisis estático
  reports/{US_ID}-cc.json      # Fase 7 — Complejidad ciclomática
  reports/{US_ID}-coverage.json# Fase 7 — Cobertura de tests
```

Cada archivo de fase debe referenciar este mapa en lugar de definir sus propias rutas.
Esto también habilita la verificación de precondiciones propuesta en OBS-002 y OBS-005:
el agente sabe exactamente qué archivo buscar antes de avanzar a la siguiente fase.

---

## Principios de Diseño — Nivel Skill

### PRIN-001: Las estimaciones de esfuerzo no aplican a ejecución por agente

**Contexto:** Las estimaciones de tiempo definidas en los archivos de fase (ej. "10 min", "45-90 minutos")
fueron concebidas con base en el esfuerzo humano. Un agente digital opera a una velocidad
cualitativamente diferente, por lo que comparar tiempo real de ejecución contra esas
estimaciones no produce varianza útil — produce ruido.

**Decisión:** No generar estimaciones de esfuerzo durante la ejecución del skill.
El tiempo registrado por el sistema de tracking tiene un propósito distinto:
**acumular datos empíricos de performance del agente** para construir baselines propios
con el tiempo. Con suficientes ejecuciones, estos datos permitirán responder preguntas como:
- ¿Cuánto tarda realmente un agente en completar una HU Flask de complejidad media?
- ¿Qué tipo de tareas generan más ciclos de aprobación-rechazo-ajuste?
- ¿Cuánto tiempo total insume una HU de extremo a extremo (Fase 0 a Fase 9)?

**Impacto en el skill:**
- Los archivos de fase no deben mostrar estimaciones de tiempo al usuario durante la ejecución
- La sección `Duración estimada` de cada fase puede mantenerse como referencia de diseño
  pero no debe presentarse como objetivo a cumplir
- El sistema de tracking debe registrar tiempos reales sin calcular ni reportar varianza
  respecto a estimaciones humanas

