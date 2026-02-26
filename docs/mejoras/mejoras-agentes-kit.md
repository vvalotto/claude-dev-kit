# Mejoras Propuestas para el Agent Kit

Documento acumulativo de observaciones detectadas durante el uso del skill `implement-us` en proyectos reales.

- **US-001** (`webapp_termostato`, 2026-02-24): Observaciones 1–4
- **Revisión documental** (2026-02-26): Observaciones 5–6

---

## Observación 1: La Fase 8 (Documentación) no garantiza actualización de todos los documentos de arquitectura

### Qué ocurrió

Durante la ejecución de Fase 8, se actualizó `CLAUDE.md` y `CHANGELOG.md`, pero no se actualizó `docs/arquitectura.md`, que contiene los diagramas C4 del sistema. El documento quedó desactualizado respecto a la nueva arquitectura por capas implementada en US-001.

### Causa raíz

`phase-8-documentation.md` no hace referencia explícita a documentos de arquitectura en formato de diagramas (Mermaid, C4, UML). Las instrucciones de la fase son genéricas ("actualizar documentación de arquitectura") sin enumerar los archivos concretos a revisar.

### Mejora propuesta

En `phase-8-documentation.md`, agregar un paso de discovery explícito antes de escribir documentación:

1. Buscar archivos de arquitectura en el proyecto: `docs/arquitectura.md`, `docs/architecture.md`, archivos con diagramas Mermaid/C4/UML.
2. Para cada archivo encontrado, evaluar si los diagramas reflejan los cambios implementados en la US.
3. Si hay diagramas (C4, classDiagram, sequenceDiagram), actualizarlos para reflejar los nuevos componentes, capas o relaciones.

---

## Observación 2: La Fase 3 (Implementación) no incluye limpieza de código obsoleto

### Qué ocurrió

Tras la refactorización de US-001, quedaron en el código elementos inservibles:
- `VERSION = '2.0.0'` en `webapp/__init__.py` — constante sin ningún importador ni uso.
- Variables globales de módulo (`bootstrap`, `moment`) que podían ser locales a `create_app()`.
- `TermostatoEstadoDTO` — TypedDict creado como modelo pero nunca importado ni usado en ninguna ruta o servicio.

Estos residuos solo se detectaron en una revisión manual posterior, no como parte del proceso guiado.

### Causa raíz

El flujo de las fases contempla crear y validar código nuevo, pero no incluye un paso de revisión de código preexistente que haya quedado huérfano tras los cambios.

### Mejora propuesta

Agregar un paso al final de `phase-3-implementation.md` (o al inicio de `phase-7-quality-gates.md`):

**"Revisión de código obsoleto":**
1. Identificar elementos del código original que la refactorización desplazó: constantes, variables globales, clases o módulos completos.
2. Para cada elemento, verificar si tiene importadores activos (`grep -r "nombre_elemento" --include="*.py"`).
3. Si no tiene importadores ni uso documentado, eliminarlo y registrar el cambio.

---

## Observación 3: El sistema de tracking de tiempo no es ejecutable desde los agentes

### Qué ocurrió

Las fases del skill (`phase-N-*.md`) muestran llamadas al tracker como bloques de código Python:

```python
tracker.start_phase(2, "Generación del Plan de Implementación")
tracker.end_phase(2, auto_approved=False)
```

Estos bloques son pseudocódigo no ejecutable. No existe una interfaz CLI ni ningún mecanismo para que el agente invoque el tracker sin escribir un script ad-hoc. Como resultado, el tracking de tiempo fue completamente omitido durante toda la implementación de US-001.

### Causa raíz

El módulo `.claude/tracking/time_tracker.py` es una clase Python importable pero no tiene punto de entrada CLI (`__main__` o script wrapper). Los archivos de fase asumen que el agente puede "llamar" al tracker como si fuera una función, lo cual no es posible en el contexto de ejecución de Claude Code.

### Mejora propuesta

Dos cambios complementarios:

**A) Agregar CLI al tracker** (`python -m webapp.tracking` o un script `track.py`):
```bash
python .claude/tracking/track.py start-phase 2 "Generación del Plan"
python .claude/tracking/track.py end-phase 2
python .claude/tracking/track.py status
```

**B) Actualizar todos los archivos `phase-N-*.md`** para reemplazar los bloques Python por comandos bash ejecutables:
```bash
# Al inicio de la fase:
python .claude/tracking/track.py start-phase 2 "Generación del Plan de Implementación"

# Al finalizar la fase:
python .claude/tracking/track.py end-phase 2
```

Con esto, el agente puede ejecutar los comandos directamente con la herramienta Bash sin necesidad de escribir código intermedio.

---

## Observación 4: La Fase 2 (Plan) incluye secciones de Tests y Validación que duplican las Fases 4–7

### Qué ocurrió

El template de `phase-2-planning.md` instruía incluir secciones "Tests" y "Validación" en cada plan generado. Todos los ejemplos del archivo (5 stacks distintos) mostraban estas secciones con tareas concretas y estimaciones de tiempo.

Dado que las Fases 4 (tests unitarios), 5 (tests de integración), 6 (BDD) y 7 (quality gates) gestionan exactamente esas actividades de forma dedicada, el resultado fue que:
- Los archivos de test fueron listados en el plan → creados en Fase 3 → recreados en Fases 4/5.
- Los quality gates fueron listados en el plan → ejecutados en Fase 3 → ejecutados de nuevo en Fase 7.

### Causa raíz

Diseño inicial del template sin considerar que el skill evolucionaría hacia fases dedicadas para testing y calidad. Las secciones de Tests y Validación en el plan tenían sentido en una versión monofásica, pero quedaron como redundancia al agregar las fases especializadas.

### Corrección aplicada

Se actualizó `phase-2-planning.md` para:
1. Eliminar "Tests" y "Validación" de las secciones a generar en el plan.
2. Agregar nota explícita: Tests → Fases 4/5/6; Quality gates → Fase 7.
3. Actualizar los 5 ejemplos eliminando esas secciones.
4. Eliminar las estimaciones de tiempo para tests y validación de "Consideraciones Importantes".

---

## Observación 5: Referencias a Django en archivos del skill pese a ser un perfil no soportado

### Qué ocurrió

El perfil `django` (patrón MVT) aparece documentado en múltiples archivos del skill como si fuera una opción disponible, pero no existe ningún archivo de customización correspondiente. Los perfiles reales son: `pyqt-mvc`, `fastapi-rest`, `flask-rest`, `flask-webapp`, `generic-python`.

### Archivos afectados

| Archivo | Ocurrencias |
|---------|-------------|
| `skills/implement-us/skill.md` | Tabla de variables (líneas 17–23), sección de perfiles (línea 64) |
| `skills/implement-us/config.json` | Entradas `"django"` en 7 claves de configuración |
| `skills/implement-us/customizations/generic-python.json` | Mención en descripción |
| `skills/implement-us/phases/phase-1-bdd.md` | Ruta BDD para Django y Ejemplo 3 completo |
| `skills/implement-us/phases/phase-2-planning.md` | Ruta de plan para Django |
| `skills/implement-us/phases/phase-3-implementation.md` | Sección Django/MVT |
| `skills/implement-us/phases/phase-4-unit-tests.md` | Ejemplos de tests con `pytest-django` |
| `skills/implement-us/phases/phase-5-integration-tests.md` | Sección Django/MVT con ejemplos completos |
| `skills/implement-us/phases/phase-6-bdd-validation.md` | Sección steps con `@pytest.mark.django_db` |
| `skills/implement-us/phases/phase-8-documentation.md` | Sección Django/MVT y API docs |
| `skills/implement-us/phases/phase-9-final-report.md` | Template de reporte Django |

### Causa raíz

Django fue descartado como perfil soportado, pero la documentación y configuración del skill no se actualizó para reflejar ese descarte. El skill quedó con ejemplos y rutas de un perfil inexistente.

### Mejora propuesta

Eliminar todas las referencias a Django de los archivos listados:
1. En `skill.md`: quitar la columna Django de la tabla de variables y la mención en perfiles.
2. En `config.json`: eliminar las entradas `"django"` de todas las claves.
3. En cada `phase-N-*.md`: eliminar las secciones, ejemplos y rutas etiquetados como Django/MVT.
4. En `generic-python.json`: actualizar la descripción para no mencionar Django.

---

## Observación 6: La Fase 0 no consulta la fuente de las HUs ni la ubicación de la arquitectura

### Qué ocurrió

La Fase 0 asume que las historias de usuario están en archivos locales (busca rutas como `docs/HISTORIAS-USUARIO-*.md`, `docs/user-stories/US-*.md`, etc.) y que la documentación de arquitectura está en ubicaciones estándar (`docs/architecture.md`, `ARCHITECTURE.md`, etc.). No pregunta al usuario antes de comenzar.

En proyectos reales, las HUs pueden estar en:
- **Jira** (como issues con número de ticket)
- **GitHub Issues** (referenciadas por número `#N`)
- **Documentos locales** (múltiples formatos y rutas posibles)
- **Notion, Confluence u otros sistemas**

Y la arquitectura puede estar en diagramas externos, wikis, o simplemente no estar documentada.

### Causa raíz

La Fase 0 fue diseñada asumiendo un único modelo de gestión documental (archivos locales en rutas convencionales). No existe un paso de "onboarding de sesión" que establezca el origen de los insumos antes de ir a buscarlos.

### Mejora propuesta

Agregar al inicio de `phase-0-validation.md`, antes de cualquier búsqueda de archivos, un bloque de preguntas obligatorias al usuario:

**"Establecimiento de fuentes":**

> **🔴 Acción Requerida — Consultar fuentes al usuario**
>
> Antes de buscar la HU y la arquitectura, preguntá al usuario:
>
> 1. **Fuente de historias de usuario:** ¿Dónde están las HUs?
>    - a) Documentos locales (indicar ruta o patrón)
>    - b) GitHub Issues (indicar número de issue `#N`)
>    - c) Jira (indicar ticket ID, p.ej. `PROJ-123`)
>    - d) Otro sistema (indicar cómo acceder)
>
> 2. **Fuente de arquitectura:** ¿Dónde está la definición de arquitectura del proyecto?
>    - a) Archivo local (indicar ruta)
>    - b) Wiki / Confluence / Notion (indicar URL o instrucción de acceso)
>    - c) No está documentada (el agente inferirá del código existente)
>
> Registrá las respuestas en el archivo `docs/plans/{US_ID}-context.md` como campos `fuente_hu` y `fuente_arquitectura`.

Esto permite que el skill funcione correctamente independientemente del sistema de gestión que use el proyecto.

---

*Última actualización: 2026-02-26*
