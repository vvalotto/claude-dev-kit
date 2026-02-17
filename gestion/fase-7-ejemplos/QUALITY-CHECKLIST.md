# Checklist de Calidad para Tutoriales de Ejemplos

**Generado por:** TICKET-058 - Validación y Testing de Ejemplos
**Fecha:** 2026-02-17
**Versión:** 1.0

---

## Uso

Este checklist debe completarse al crear un nuevo tutorial de ejemplo para el Claude Dev Kit.
Usarlo antes de hacer commit del tutorial.

---

## ✅ Checklist Completo

### 1. Estructura del Documento

- [ ] **Título** - `# Tutorial: <Stack> - <Proyecto>`
- [ ] **Metadata** - Stack, Tiempo Estimado, Nivel
- [ ] **Tabla de Contenidos** - Con links internos
- [ ] **Introducción** - Qué aprenderás, por qué este stack
- [ ] **Requisitos Previos** - Software, conocimientos, comandos de verificación
- [ ] **Historia de Usuario** - Contexto, criterios de aceptación
- [ ] **Setup del Proyecto** - Directorio, git init, venv, estructura
- [ ] **Instalación del Framework** - Pasos completos
- [ ] **Walkthrough 10 Fases** - Todas las fases 0-9 documentadas
- [ ] **Validación Final** - Checklist de criterios de aceptación
- [ ] **Troubleshooting** - Mínimo 5 problemas comunes
- [ ] **Próximos Pasos** - Cómo extender el proyecto
- [ ] **Recursos** - Links a documentación oficial
- [ ] **Navegación** - Links anterior/siguiente/índice al final

### 2. Código

- [ ] **Sintaxis correcta** - Sin errores de Python
- [ ] **Ejecutable sin modificaciones** - Copy-paste directo funciona
- [ ] **Output mostrado** - Resultado esperado después de cada comando
- [ ] **Imports completos** - Todos los imports necesarios incluidos
- [ ] **Paths correctos** - Rutas relativas coherentes con la estructura
- [ ] **Comandos verificados** - Todos los comandos bash testeados

### 3. Cobertura de las 10 Fases

| Fase | Requerido |
|------|-----------|
| 0 - Validación de Contexto | US + estructura de directorios |
| 1 - Escenarios BDD | Feature file Gherkin (mínimo 5 escenarios) |
| 2 - Plan de Implementación | Plan + ADR |
| 3 - Implementación | Código completo de todos los módulos |
| 4 - Tests Unitarios | Mínimo 10 tests unitarios |
| 5 - Tests de Integración | Mínimo 5 tests de integración |
| 6 - Validación BDD | Mínimo 5 tests BDD pasando |
| 7 - Quality Gates | Pylint score, Coverage %, Complejidad |
| 8 - Documentación | README + docstrings |
| 9 - Reporte Final | Reporte con métricas |

### 4. Quality Gates Documentados

- [ ] **Pylint Score** - Mostrado en reporte (objetivo ≥ 8.0)
- [ ] **Coverage** - Mostrado con `--cov-report=term-missing` (objetivo ≥ 95%)
- [ ] **Complejidad Ciclomática** - Radon cc (objetivo A/B)
- [ ] **Maintainability Index** - Radon mi (objetivo A/B)
- [ ] **Total tests** - N/N pasando

### 5. Troubleshooting

- [ ] **Mínimo 5 problemas** documentados
- [ ] **Específicos del stack** - No genéricos
- [ ] **Con solución paso a paso** - No solo "verificar el error"
- [ ] **Incluye casos BDD** - pytest-bdd suele tener configuración específica
- [ ] **Incluye casos de imports** - ModuleNotFoundError es común

### 6. Navegación e Integración

- [ ] **Links de navegación** - Anterior / Índice / Siguiente al final
- [ ] **Link en docs/user/index.md** - Actualizado con ruta relativa correcta
- [ ] **Link en docs/README.md** - Verificar que está listado
- [ ] **Estado actualizado** - ✅ Completado (no ⏳ Fase 7)
- [ ] **Código ejecutable en examples/code/** - Directorio con código real

### 7. Artefactos Requeridos en examples/code/<proyecto>/

- [ ] **README.md** - Guía de usuario del código
- [ ] **VALIDATION-REPORT.md** - Evidencia técnica con outputs reales
- [ ] **EXECUTIVE-SUMMARY.md** - Resumen ejecutivo con métricas
- [ ] **requirements.txt** - Dependencias del proyecto
- [ ] **pytest.ini** - Configuración de tests
- [ ] **Tests pasando** - Verificado con `pytest tests/ -q`

### 8. Consistencia con Otros Tutoriales

- [ ] **Mismo formato de encabezados** - # ## ### como los demás
- [ ] **Mismas secciones** - Exactamente las mismas secciones
- [ ] **Nivel de detalle similar** - Ni demasiado corto ni demasiado largo
- [ ] **Mismo tono** - Profesional pero accesible
- [ ] **Mismas convenciones de código** - Mismas herramientas (pylint, radon, pytest-bdd)

---

## Resultados de Validación — Fase 7

| Tutorial | Estructura | Código | Tests | Artefactos | Navegación | Estado |
|----------|-----------|--------|-------|-----------|-----------|--------|
| pyqt-project | ✅ | ✅ | 14/14 | ✅ | ✅ | ✅ |
| fastapi-project | ✅ | ✅ | 23/23 | ✅ | ✅ | ✅ |
| flask-rest-api | ✅ | ✅ | 38/38 | ✅ | ✅ | ✅ |
| flask-webapp | ✅ | ✅ | 38/38 | ✅ | ✅ | ✅ |
| generic-python | ✅ | ✅ | 90/90 | ✅ | ✅ | ✅ |

### Issues Encontrados y Corregidos

| Issue | Tipo | Archivo | Corrección |
|-------|------|---------|-----------|
| Links con formato wiki incorrecto | Crítico | docs/user/index.md | Cambiado a rutas relativas |
| Estado "⏳ Fase 7" desactualizado | Menor | docs/user/index.md | Actualizado a "✅ Completado" |
| Falta navegación anterior/siguiente | Crítico | 5 tutoriales | Agregado footer de navegación |
| Link "Tutorial PyQt-MVC" incorrecto | Menor | docs/user/index.md | Corregida ruta relativa |

---

## Lecciones Aprendidas

1. **Rutas relativas desde el inicio** — Los links deben ser `../examples/pyqt-project.md`, no
   formato wiki `examples-Pyqt-Project`. Verificar en el primer commit.

2. **Navegación es obligatoria** — Cada tutorial necesita links anterior/siguiente desde el día 1.
   Los usuarios no vuelven al índice para continuar al siguiente tutorial.

3. **Estado en índice** — Actualizar `docs/user/index.md` al mismo tiempo que se crea el tutorial,
   no después.

4. **VALIDATION-REPORT + EXECUTIVE-SUMMARY son obligatorios** — No commitear el ejemplo sin estos
   dos archivos. Son el diferenciador de calidad del framework.

5. **Venv por ejemplo** — Cada directorio en `examples/code/` necesita su propio venv para
   aislar dependencias.

---

**Claude Dev Kit v1.0** — Checklist de Calidad para Tutoriales
