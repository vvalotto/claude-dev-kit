# Fase 8: Documentación

Sincroniza la documentación del proyecto con los cambios realizados durante la implementación. Actualiza el plan con estado y tiempos reales, busca activamente archivos de arquitectura desactualizados, y agrega entrada al CHANGELOG.

**Aprobación requerida:** Sí — el usuario revisa y aprueba la documentación generada antes de avanzar.

---

## Para el usuario

### Qué hace esta fase

1. **Plan de implementación:** Marca la US como `COMPLETADO`, agrega métricas de tiempo real y lecciones aprendidas
2. **Discovery de arquitectura:** Busca activamente archivos con diagramas (Mermaid, PlantUML, C4) para detectar si quedaron desactualizados por los cambios de esta US
3. **CHANGELOG:** Agrega una entrada nueva con los componentes creados, cantidad de tests y cobertura
4. **README:** Actualiza si se agregó funcionalidad visible al usuario o cambiaron dependencias
5. Presenta la documentación actualizada para tu revisión y aprobación

### Qué esperar

El discovery de arquitectura es imperativo: el skill ejecuta `grep` y `find` para buscar archivos de arquitectura aunque no se los indiques. Si detecta archivos desactualizados, los actualiza y te muestra los cambios.

Si el CLI de tracking no está disponible, el skill usa el tiempo observado en la sesión o anota "Tracking no disponible".

### Cuándo se actualiza el README

- Se agregó funcionalidad visible al usuario
- Cambiaron las instrucciones de instalación o configuración
- Se agregaron nuevas dependencias
- Cambió la estructura del proyecto

### Cuándo se actualiza la arquitectura

- Se agregó un componente nuevo significativo
- Se modificó la estructura de módulos
- Se cambió un patrón arquitectónico
- Se agregó una nueva integración externa

---

## Referencia técnica

### Entradas

| Entrada | Tipo | Requerida | Fuente |
|---|---|---|---|
| `quality/reports/{US_ID}-quality.json` | Artefacto | ✅ Sí | Fase 7 |
| `docs/plans/{US_ID}-plan.md` | Artefacto | ✅ Sí | Fase 2 |
| Datos de tracking (tiempo real por fase) | CLI de tracking | ❌ Opcional | Sistema de tracking |
| Archivos de arquitectura del proyecto | Discovery con grep/find | ❌ Opcional | Exploración en Paso 2 |

### Salidas

| Salida | Tipo | Descripción |
|---|---|---|
| `docs/plans/{US_ID}-plan.md` actualizado | Artefacto | Estado COMPLETADO, tiempos reales, lecciones |
| Entrada en `CHANGELOG.md` | Artefacto | Formato Keep a Changelog |
| Archivos de arquitectura actualizados | Varios | Solo si el discovery detectó archivos desactualizados |
| `README.md` actualizado | Artefacto | Solo si aplica (funcionalidad visible o estructura cambiada) |

### Templates

Ninguno externo. Los ejemplos de actualización están embebidos en el archivo de fase.

### Artefactos

| Artefacto | Operación | Ruta |
|---|---|---|
| `{US_ID}-plan.md` | **Actualiza** | `docs/plans/{US_ID}-plan.md` |
| `{US_ID}-quality.json` | **Lee** | `quality/reports/{US_ID}-quality.json` |
| `CHANGELOG.md` | **Actualiza** | raíz del proyecto |
| `docs/architecture*.md` (si existe) | **Actualiza** (si aplica) | Según discovery |
| `README.md` (si aplica) | **Actualiza** | raíz del proyecto |

### Actualización del plan

```markdown
**Estado:** ✅ COMPLETADO
**Fecha completado:** {FECHA}

## Métricas de Tiempo

| Fase | Estimado | Real | Varianza |
|------|----------|------|----------|
| ... | ... | ... | ... |
| **Total** | **Xh** | **Yh** | **±Z** |

## Lecciones Aprendidas

- ✅ {lección positiva}
- ⚠️ {punto de atención}
- 💡 {insight}
```

### Entrada de CHANGELOG (formato Keep a Changelog)

```markdown
## [Unreleased]

### Added
- [{US_ID}] {US_TITLE}
  - Implementado {COMPONENT_TYPE} para {FUNCTIONALITY}
  - {N} tests unitarios y {M} tests de integración
  - Coverage: {COVERAGE}%
```

### Discovery de arquitectura

```bash
# Buscar archivos con diagramas
grep -rl "mermaid\|plantuml\|graph LR\|graph TD\|C4Context" docs/ 2>/dev/null

# Buscar archivos de arquitectura por nombre
find . -iname "ARCHITECTURE*" -o -iname "architecture*" -o -name "*.puml" 2>/dev/null
```

### Convenciones

- El discovery de arquitectura (Paso 2) es **imperativo** (`🔴`) — no se omite aunque el usuario no lo pida.
- Si el CLI de tracking no está disponible, anotar explícitamente: *"Tracking no disponible — tiempos estimados."*
- La aprobación del usuario es requerida antes de avanzar a Fase 9.

### Dependencias

| Dirección | Fase | Qué provee |
|---|---|---|
| ← anterior | Fase 7 | `quality.json` con métricas para documentar |
| → siguiente | Fase 9 | Plan actualizado para incluir en reporte |

### Checklist de salida

- [ ] Plan de implementación actualizado con estado "COMPLETADO" y tiempo real
- [ ] Discovery de arquitectura ejecutado — archivos desactualizados corregidos (o confirmado que no hay)
- [ ] `CHANGELOG.md` tiene entrada nueva para esta US
- [ ] `README.md` actualizado (si aplicó)
- [ ] No hay referencias a código obsoleto en la documentación
- [ ] El usuario revisó y aprobó la documentación generada
- [ ] Tracking de Fase 8 cerrado

### Estado en v1.3

| ID | Descripción | Resolución |
|---|---|---|
| D8-1 | `config.json` → `phases.8.approval_required: false` contradecía `skill.md` que decía "Aprobación: Requerida" | Se corrigió `config.json` a `approval_required: true` para Fase 8, alineado con el comportamiento real del skill |
| D8-2 | Sección "Automatización" mencionaba `python manage.py generate_swagger` (Django, no soportado) | Se eliminó la referencia a Django; la sección ahora menciona FastAPI (OpenAPI automático) y Flask (flask-openapi3 o flasgger si están instalados) |

---

**Fase anterior:** [Fase 7: Quality Gates](phase-7.md)
**Siguiente fase:** [Fase 9: Reporte Final](phase-9.md)
