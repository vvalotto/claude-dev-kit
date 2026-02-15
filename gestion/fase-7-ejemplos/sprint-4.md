# Sprint 4 - Fase 7: Ejemplos por Stack Tecnológico

**Inicio:** 2026-02-15
**Duración:** 1 semana
**Estado:** 🔄 En progreso

---

## 🎯 Objetivo

Crear **tutoriales end-to-end completos** para cada perfil soportado del framework, demostrando:
- Instalación del framework
- Implementación de una historia de usuario completa
- Uso del skill `/implement-us` paso a paso
- Sistema de tracking en acción
- Validación de quality gates
- Output final esperado

---

## 📋 Alcance

### Ejemplos a Crear

1. **pyqt-project.md** - Aplicación Desktop PyQt6 + MVC
   - Historia de usuario: Calculadora básica
   - Stack: PyQt6, pytest-qt, MVC pattern
   - Componentes: Window, Controller, Model

2. **fastapi-project.md** - API REST con FastAPI
   - Historia de usuario: API de tareas (TODO)
   - Stack: FastAPI, pytest, async/await
   - Endpoints: GET, POST, PUT, DELETE

3. **flask-rest-project.md** - API REST con Flask
   - Historia de usuario: API de contactos
   - Stack: Flask, pytest, blueprints
   - Endpoints: CRUD completo

4. **flask-webapp-project.md** - WebApp con Flask
   - Historia de usuario: Blog simple
   - Stack: Flask, Jinja2, pytest
   - Features: Templates, forms, navegación

5. **generic-python.md** - CLI App / Librería
   - Historia de usuario: Utilidad de archivos
   - Stack: Python stdlib, argparse, pytest
   - Features: CLI interface, file operations

---

## 📊 Tickets

### Planificación y Análisis
- [TICKET-052](tickets/TICKET-052-analisis-ejemplos.md) - Análisis y planificación de ejemplos (1h)

### Ejemplos por Stack
- [TICKET-053](tickets/TICKET-053-ejemplo-pyqt.md) - Tutorial PyQt-MVC completo (3h)
- [TICKET-054](tickets/TICKET-054-ejemplo-fastapi.md) - Tutorial FastAPI-REST completo (2.5h)
- [TICKET-055](tickets/TICKET-055-ejemplo-flask-rest.md) - Tutorial Flask-REST completo (2.5h)
- [TICKET-056](tickets/TICKET-056-ejemplo-flask-webapp.md) - Tutorial Flask-WebApp completo (2.5h)
- [TICKET-057](tickets/TICKET-057-ejemplo-generic-python.md) - Tutorial Python genérico completo (2h)

### Validación
- [TICKET-058](tickets/TICKET-058-validacion-ejemplos.md) - Validación y testing de ejemplos (1.5h)

**Total:** 7 tickets | **15 horas estimadas**

---

## ✅ Criterios de Éxito

### Por Cada Ejemplo

- [ ] **Historia de usuario clara** - Caso de uso real y ejecutable
- [ ] **Instalación documentada** - Setup completo paso a paso
- [ ] **Walkthrough completo** - Todas las 10 fases del skill `/implement-us`
- [ ] **Código ejecutable** - Ejemplos que realmente funcionan
- [ ] **Screenshots/output** - Mostrar resultados esperados
- [ ] **Troubleshooting** - Problemas comunes y soluciones
- [ ] **Tiempo realista** - Ejemplo completable en <1 hora por el usuario

### Global

- [ ] **5 ejemplos completos** - Uno por cada perfil
- [ ] **Consistencia** - Formato y estructura similar en todos
- [ ] **Validados** - Probados manualmente siguiendo los pasos
- [ ] **Enlaces correctos** - Links funcionando en Wiki
- [ ] **Código de ejemplo** - Archivos de ejemplo en `examples/code/`

---

## 📈 Progreso

| Ticket | Título | Estado | Estimado | Real |
|--------|--------|--------|----------|------|
| TICKET-052 | Análisis y planificación | ⏳ Pendiente | 1h | - |
| TICKET-053 | PyQt-MVC Tutorial | ⏳ Pendiente | 3h | - |
| TICKET-054 | FastAPI-REST Tutorial | ⏳ Pendiente | 2.5h | - |
| TICKET-055 | Flask-REST Tutorial | ⏳ Pendiente | 2.5h | - |
| TICKET-056 | Flask-WebApp Tutorial | ⏳ Pendiente | 2.5h | - |
| TICKET-057 | Python Generic Tutorial | ⏳ Pendiente | 2h | - |
| TICKET-058 | Validación | ⏳ Pendiente | 1.5h | - |

**Total:** 0/7 completados (0%)

---

## 🎯 Entregable

**Carpeta `docs/examples/`** con 5 tutoriales completos:
- pyqt-project.md
- fastapi-project.md
- flask-rest-project.md
- flask-webapp-project.md
- generic-python.md

**Carpeta `examples/code/`** (opcional) con código de ejemplo ejecutable.

**Estructura de cada tutorial:**
1. Introducción y requisitos
2. Setup del proyecto
3. Instalación del framework
4. Historia de usuario
5. Walkthrough completo de las 10 fases
6. Validación y testing
7. Output final
8. Troubleshooting
9. Próximos pasos

---

## 📝 Notas

- Cada ejemplo debe ser **autocontenido** - completable sin conocimiento previo
- Usar **casos de uso reales** - calculadora, TODO list, blog, etc.
- Incluir **output esperado** - capturas o texto de ejemplo
- **Tiempo objetivo por usuario:** 30-60 minutos para completar cada tutorial
- Los ejemplos serán referenciados desde `docs/user/index.md`

---

**Última actualización:** 2026-02-15
