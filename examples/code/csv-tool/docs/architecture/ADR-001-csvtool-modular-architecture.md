# ADR-001: Arquitectura Modular para CSV Tool CLI

**Estado:** Aceptado
**Fecha:** 2026-02-17
**Contexto:** US-057 — CSV Tool CLI Utility

---

## Contexto

Necesitamos implementar una herramienta CLI con 4 comandos (convert, filter, merge, stats).
El perfil seleccionado es `generic-python`, que no impone un framework específico.

La decisión clave es cómo organizar el código para maximizar:
- Testabilidad (cada comando testeable de forma independiente)
- Mantenibilidad (agregar comandos sin tocar código existente)
- Claridad (estructura predecible para nuevos colaboradores)

## Opciones Consideradas

### Opción A: Script monolítico (un archivo)
```python
# csvtool.py
if args.command == 'convert':
    ...
elif args.command == 'filter':
    ...
```
**Pros:** Simplicidad inicial
**Contras:** No testeable por partes, crece descontroladamente, viola SRP

### Opción B: Paquete con un módulo por comando (ELEGIDA)
```
csvtool/
├── cli.py          # Solo parsing + dispatch
├── commands/       # Un módulo por comando
├── models/         # Modelos de datos
└── utils/          # Validaciones compartidas
```
**Pros:** SRP respetado, cada módulo testeable independientemente, extensible
**Contras:** Más archivos (aceptable para CLI de este scope)

### Opción C: Click framework
**Pros:** Más ergonómico para CLI complejas
**Contras:** Dependencia externa, no consistente con "Python stdlib only" del perfil generic-python

## Decisión

**Opción B seleccionada:** Paquete modular con un módulo por comando.

## Consecuencias

### Positivas
- ✅ `cli.py` solo hace parsing y dispatch: sin lógica de negocio
- ✅ Cada comando (`convert.py`, `filter_cmd.py`, etc.) testeable sin levantar el CLI completo
- ✅ `CsvData` como modelo central compartido entre comandos
- ✅ `validators.py` centraliza validaciones reutilizadas en todos los comandos
- ✅ Fácil agregar nuevos comandos: nuevo archivo en `commands/` + entrada en parser

### Negativas
- ⚠️ Más archivos que un script monolítico (aceptable, justificado por testabilidad)

## Flujo de Datos

```
CLI Input (argv)
     │
     ▼
cli.py::create_parser()    ← Argparse solo
     │
     ▼
cli.py::run()              ← Dispatch por subcomando
     │
     ▼
commands/*.py              ← Lógica de negocio
     │
     ▼
utils/validators.py        ← Validaciones (raises excepciones)
     │
     ▼
models/csv_data.py         ← Modelo de datos
     │
     ▼
Output (stdout/file)
```

## Manejo de Errores

Todas las excepciones se propagan hasta `cli.py::run()`, que las captura y:
- Imprime `Error: <message>` en stderr
- Retorna exit code 1

Excepciones custom:
- `FileNotFoundError` → Archivo de entrada no existe
- `ValueError` → Formato incorrecto o columna no encontrada
- `PermissionError` → Sin permisos de escritura

---

**Documento generado:** Fase 2 - /implement-us US-057
