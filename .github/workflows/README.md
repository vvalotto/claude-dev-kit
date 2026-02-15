# GitHub Actions - Claude Dev Kit

Este directorio contiene los workflows de CI/CD del proyecto.

---

## 📋 Workflows Disponibles

### sync-wiki.yml - Sincronización de Documentación a Wiki

**Propósito:** Sincronizar automáticamente la documentación de `docs/` a la GitHub Wiki del proyecto.

**Trigger:**
- ✅ Automático: Push a `main` que modifique archivos en `docs/`
- ✅ Manual: Botón "Run workflow" en GitHub Actions

**¿Qué sincroniza?**

```
docs/user/          → wiki/user/          # Documentación de usuario
docs/developer/     → wiki/developer/     # Documentación técnica
docs/README.md      → wiki/Home.md        # Página principal de la Wiki
docs/user/index.md  → wiki/Documentation-Index.md  # Índice alternativo
```

**Estructura en Wiki:**

```
Wiki/
├── Home.md                          # Página principal (desde docs/README.md)
├── Documentation-Index.md           # Índice de documentación
│
├── user/                            # Documentación de usuario
│   ├── index.md
│   ├── getting-started.md
│   ├── installation.md
│   ├── customization.md
│   ├── configuration.md
│   ├── skills/
│   │   └── implement-us.md
│   └── tracking/
│       ├── user-guide.md
│       └── examples.md
│
└── developer/                       # Documentación técnica
    ├── architecture/
    │   ├── tracking.md
    │   ├── template-system.md
    │   └── session-memory.md
    └── contributing/
        ├── creating-skills.md
        └── template.md
```

---

## 🚀 Uso

### Ejecución Automática

El workflow se ejecuta automáticamente cuando:
1. Haces push a `main`
2. Los cambios incluyen archivos en `docs/`

**Ejemplo:**
```bash
# Hacer cambios en documentación
vim docs/user/getting-started.md

# Commit y push
git add docs/user/getting-started.md
git commit -m "docs: actualizar getting-started"
git push origin main

# ✅ El workflow se ejecuta automáticamente
```

### Ejecución Manual

Si necesitas sincronizar la Wiki manualmente:

1. Ve a: **Actions** → **Sync Documentation to Wiki**
2. Click en **Run workflow**
3. Selecciona branch `main`
4. Click en **Run workflow** (botón verde)

---

## 🔧 Cómo Funciona

### Paso 1: Checkout
Clona el repositorio principal con todo el historial.

### Paso 2: Configuración Git
Configura git con usuario `github-actions[bot]`.

### Paso 3: Clonar Wiki
Clona el repositorio Wiki (`.wiki.git`).

### Paso 4: Sincronizar User Docs
Copia `docs/user/` → `wiki/user/` manteniendo estructura.

### Paso 5: Sincronizar Developer Docs
Copia `docs/developer/` → `wiki/developer/` manteniendo estructura.

### Paso 6: Sincronizar README e Índice
- `docs/README.md` → `wiki/Home.md` (página principal)
- `docs/user/index.md` → `wiki/Documentation-Index.md`

### Paso 7: Commit y Push
Si hay cambios, hace commit y push al Wiki.

---

## 📊 Monitoreo

### Ver Ejecuciones

1. Ve a la pestaña **Actions** en GitHub
2. Selecciona workflow **Sync Documentation to Wiki**
3. Verás lista de todas las ejecuciones

### Verificar Sincronización

Después de una ejecución exitosa:
1. Ve a **Wiki** del proyecto
2. Verifica que los archivos estén actualizados
3. Revisa timestamp del último commit en Wiki

**Wiki URL:** https://github.com/vvalotto/claude-dev-kit/wiki

---

## ⚠️ Troubleshooting

### Error: "No such file or directory"

**Causa:** Archivos esperados no existen en `docs/`

**Solución:**
- Verifica que la estructura de `docs/` sea correcta
- El workflow usa `2>/dev/null || true` para ignorar archivos faltantes

### Error: "Permission denied"

**Causa:** GitHub Actions no tiene permisos para escribir en Wiki

**Solución:**
1. Ve a **Settings** → **Actions** → **General**
2. En **Workflow permissions**, selecciona:
   - ✅ Read and write permissions
3. Guarda cambios

### Error: "Nothing to commit"

**Causa:** No hay cambios en documentación desde última sincronización

**Solución:**
- Esto es normal, el workflow detecta que no hay cambios y sale exitosamente

### Wiki no se actualiza

**Causa:** El workflow se ejecutó pero no hubo cambios

**Solución:**
1. Verifica logs del workflow en Actions
2. Confirma que los archivos cambiaron en `docs/`
3. Verifica que el push a `main` incluyó archivos en `docs/`

---

## 📝 Mantenimiento

### Actualizar el Workflow

Si necesitas modificar la sincronización:

1. Edita `.github/workflows/sync-wiki.yml`
2. Commit y push a `main`
3. El workflow se actualiza automáticamente

### Agregar Nuevos Directorios

Si agregas una nueva carpeta en `docs/`:

```yaml
- name: Sync New Directory
  run: |
    mkdir -p wiki/new-directory
    cp docs/new-directory/*.md wiki/new-directory/ 2>/dev/null || true
```

### Cambiar Triggers

Para ejecutar en otros eventos:

```yaml
on:
  push:
    branches:
      - main
      - develop  # Agregar otra rama
  pull_request:   # Ejecutar en PRs
    paths:
      - 'docs/**'
```

---

## 🔗 Enlaces

- **Wiki del Proyecto:** https://github.com/vvalotto/claude-dev-kit/wiki
- **GitHub Actions Docs:** https://docs.github.com/en/actions
- **Wiki Docs:** https://docs.github.com/en/communities/documenting-your-project-with-wikis

---

**Última Actualización:** 2026-02-15
