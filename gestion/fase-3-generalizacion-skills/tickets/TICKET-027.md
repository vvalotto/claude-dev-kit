# TICKET-027: Testing de perfiles y validación del skill generalizado

**Fase:** 3 - Generalización de Skills
**Sprint:** 2
**Estado:** TODO
**Prioridad:** Crítica
**Estimación:** 2 horas
**Asignado a:** Claude Code

## Descripción

Realizar testing comprehensivo del skill generalizado y los 4 perfiles de customización para validar que:
1. El skill generalizado no tiene referencias hardcodeadas
2. Todos los perfiles se fusionan correctamente con config.json base
3. Las variables se resuelven apropiadamente
4. No hay conflictos entre perfiles
5. La documentación es clara y completa

Este es el último ticket de la Fase 3 y determina si la generalización fue exitosa.

## Criterios de Aceptación

- [ ] Validación de sintaxis JSON para todos los archivos
- [ ] Verificación de ausencia de referencias hardcodeadas en skill.md
- [ ] Testing de fusión config base + cada perfil
- [ ] Validación de resolución de variables
- [ ] Verificación de compatibilidad con instalador
- [ ] Testing manual de lectura del skill con diferentes perfiles
- [ ] Documento de validación creado con resultados
- [ ] Todos los tests pasando
- [ ] Fase 3 lista para merge a main

## Dependencias

- **Depende de:** TICKET-021, TICKET-022, TICKET-023, TICKET-024, TICKET-025, TICKET-026
- **Bloquea a:** Fase 4 (Templates), Fase 6 (Documentación)

## Notas Técnicas

### Tests a Ejecutar

#### 1. Validación de Sintaxis JSON

```bash
# Validar todos los archivos JSON
python -m json.tool skills/implement-us/config.json
python -m json.tool skills/implement-us/customizations/pyqt-mvc.json
python -m json.tool skills/implement-us/customizations/fastapi-rest.json
python -m json.tool skills/implement-us/customizations/django-mvt.json
python -m json.tool skills/implement-us/customizations/generic-python.json
```

#### 2. Verificación de Referencias Hardcodeadas

```bash
# No debe encontrar nada:
grep -i "Panel\|Display\|Climatizador" skills/implement-us/skill.md
grep "app/presentacion/paneles" skills/implement-us/skill.md
grep "ModeloBase" skills/implement-us/skill.md
grep "pytest-qt\|qapp\|qtbot" skills/implement-us/skill.md
grep "Factory\|Coordinator" skills/implement-us/skill.md

# Debe encontrar variables:
grep "{ARCHITECTURE_PATTERN}" skills/implement-us/skill.md
grep "{COMPONENT_TYPE}" skills/implement-us/skill.md
grep "{COMPONENT_PATH}" skills/implement-us/skill.md
grep "{TEST_FRAMEWORK}" skills/implement-us/skill.md
grep "{BASE_CLASS}" skills/implement-us/skill.md
```

#### 3. Testing de Fusión de Configs

```python
#!/usr/bin/env python3
"""
Test de fusión de configuraciones.
"""
import json
from pathlib import Path

def deep_merge(base: dict, override: dict) -> dict:
    """Fusionar dos diccionarios recursivamente."""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result

def test_profile_merge(profile_name: str):
    """Testear fusión de un perfil específico."""
    base = json.load(open('skills/implement-us/config.json'))
    profile = json.load(open(f'skills/implement-us/customizations/{profile_name}.json'))

    merged = deep_merge(base, profile)

    print(f"\n{'='*60}")
    print(f"Testing: {profile_name}")
    print(f"{'='*60}")

    # Validaciones
    assert 'version' in merged, "Falta 'version'"
    assert 'architecture_patterns' in merged, "Falta 'architecture_patterns'"
    assert 'component_structure' in merged, "Falta 'component_structure'"
    assert 'test_framework' in merged, "Falta 'test_framework'"
    assert 'variables' in merged, "Falta 'variables'"

    print(f"✅ Fusión exitosa")
    print(f"   Architecture: {merged['architecture_patterns']['default']}")
    print(f"   Test Framework: {merged['test_framework']['runner']}")
    print(f"   Variables definidas: {len(merged['variables'])}")

    return merged

# Ejecutar tests
for profile in ['pyqt-mvc', 'fastapi-rest', 'django-mvt', 'generic-python']:
    test_profile_merge(profile)

print(f"\n{'='*60}")
print("✅ TODOS LOS TESTS DE FUSIÓN PASARON")
print(f"{'='*60}")
```

#### 4. Validación de Variables

```python
#!/usr/bin/env python3
"""
Validar que todas las variables usadas en el skill están definidas en configs.
"""
import re
import json

# Leer skill
with open('skills/implement-us/skill.md') as f:
    skill_content = f.read()

# Extraer variables usadas {VARIABLE_NAME}
variables_used = set(re.findall(r'{(\w+)}', skill_content))

print(f"Variables encontradas en skill.md: {len(variables_used)}")
for var in sorted(variables_used):
    print(f"  - {var}")

# Verificar que estén definidas en config.json
config = json.load(open('skills/implement-us/config.json'))
variables_defined = set(config.get('variables', {}).keys())

print(f"\nVariables definidas en config.json: {len(variables_defined)}")
for var in sorted(variables_defined):
    print(f"  - {var}")

# Verificar inconsistencias
missing = variables_used - variables_defined
if missing:
    print(f"\n❌ VARIABLES USADAS PERO NO DEFINIDAS:")
    for var in missing:
        print(f"  - {var}")
else:
    print(f"\n✅ Todas las variables están definidas")

unused = variables_defined - variables_used
if unused:
    print(f"\n⚠️  VARIABLES DEFINIDAS PERO NO USADAS:")
    for var in unused:
        print(f"  - {var}")
```

#### 5. Validación de Compatibilidad con Instalador

```bash
# Simular instalación (dry-run) con cada perfil
python install/installer.py --profile pyqt-mvc --dry-run
python install/installer.py --profile fastapi-rest --dry-run
python install/installer.py --profile django-mvt --dry-run
python install/installer.py --profile generic-python --dry-run
```

### Documento de Validación

Crear: `gestion/fase-3-generalizacion-skills/TESTING-RESULTS.md`

```markdown
# Resultados de Testing - Fase 3: Generalización de Skills

**Fecha:** YYYY-MM-DD
**Ejecutado por:** Claude Code

## 1. Validación de Sintaxis JSON

- [ ] config.json: ✅ / ❌
- [ ] pyqt-mvc.json: ✅ / ❌
- [ ] fastapi-rest.json: ✅ / ❌
- [ ] django-mvt.json: ✅ / ❌
- [ ] generic-python.json: ✅ / ❌

## 2. Verificación de Referencias Hardcodeadas

- [ ] skill.md libre de referencias a PyQt: ✅ / ❌
- [ ] skill.md libre de referencias a MVC: ✅ / ❌
- [ ] skill.md libre de paths específicos: ✅ / ❌
- [ ] Variables {XXX} presentes: ✅ / ❌

## 3. Testing de Fusión

- [ ] pyqt-mvc: ✅ / ❌
- [ ] fastapi-rest: ✅ / ❌
- [ ] django-mvt: ✅ / ❌
- [ ] generic-python: ✅ / ❌

## 4. Validación de Variables

- Variables usadas: X
- Variables definidas: Y
- Variables faltantes: Z
- Estado: ✅ / ❌

## 5. Compatibilidad con Instalador

- [ ] Instalación pyqt-mvc (dry-run): ✅ / ❌
- [ ] Instalación fastapi-rest (dry-run): ✅ / ❌
- [ ] Instalación django-mvt (dry-run): ✅ / ❌
- [ ] Instalación generic-python (dry-run): ✅ / ❌

## Resumen

- **Total de Tests:** X
- **Pasados:** Y
- **Fallidos:** Z
- **Estado Final:** ✅ APROBADO / ❌ REQUIERE CORRECCIONES

## Problemas Encontrados

[Listar problemas y sus correcciones]

## Conclusión

[Conclusión sobre si la Fase 3 está completa]
```

## Checklist de Implementación

- [ ] Crear scripts de testing (validación JSON, fusión, variables)
- [ ] Ejecutar validación de sintaxis JSON para todos los archivos
- [ ] Ejecutar grep para verificar ausencia de referencias hardcodeadas
- [ ] Ejecutar script de testing de fusión de configs
- [ ] Ejecutar script de validación de variables
- [ ] Ejecutar dry-run del instalador con cada perfil
- [ ] Documentar todos los resultados en TESTING-RESULTS.md
- [ ] Corregir problemas encontrados
- [ ] Re-ejecutar tests después de correcciones
- [ ] Validar que todos los criterios de aceptación se cumplen
- [ ] Actualizar sprint-2.md con resultados finales
- [ ] Preparar para merge a main

## Resultado

**Fecha de Completado:** _Pendiente_

### Estadísticas Finales

- Tests ejecutados: _X_
- Tests pasados: _Y_
- Tests fallidos: _Z_
- Problemas corregidos: _W_

### Commits

_Listar commits de correcciones si fueron necesarios_

### Conclusión

_¿La Fase 3 está completa y lista para merge?_

**Estado:** 📋 Pendiente
