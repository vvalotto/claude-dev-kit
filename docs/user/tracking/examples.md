# Ejemplos de Uso del Sistema de Tracking

## Ejemplo 1: Implementación Simple (Sin Pausas)

```bash
# Usuario inicia implementación
$ /implement-us US-001

# Claude ejecuta automáticamente:
# - Fase 0: Validación de Contexto → tracking iniciado
# - Fase 1: Generación de Escenarios BDD
# - Fase 2-8: Implementación, tests, quality gates
# - Fase 9: Reporte final → tracking finalizado

# Ver reporte al finalizar
$ /track-report US-001
```

**Resultado:** Reporte completo con tiempo por fase, métricas de varianza.

## Ejemplo 2: Implementación con Pausas

```bash
# Iniciar implementación
$ /implement-us US-002

# ... Claude trabaja en Fases 0-2 ...

# Interrumpido por reunión (durante Fase 3)
$ /track-pause "Daily standup"

# ... 15 minutos de reunión ...

# Continuar trabajo
$ /track-resume

# ... Claude continúa Fases 3-9 ...

# Ver estado durante implementación
$ /track-status

# Al finalizar
$ /track-report US-002
```

**Resultado:**
- Reporte muestra pausa de 15m
- Tiempo efectivo excluye la pausa
- Métricas correctas de varianza

## Ejemplo 3: Análisis Retrospectivo

```bash
# Ver historial completo
$ /track-history

# Identificar US con mayor varianza
# Ejemplo: US-005 tiene +45% de varianza

# Revisar reporte detallado
$ /track-report US-005

# Analizar por fase:
# Fase 3 (Implementación): +30m sobre estimado
# Fase 4 (Tests Unitarios): +15m sobre estimado

# Conclusión: Ajustar estimaciones de implementación y testing
# para futuras USs similares
```

## Ejemplo 4: Comparación de Múltiples USs

```bash
# Ver últimas 10 USs
$ /track-history --last 10

# Observar patrones:
# - USs de 3 puntos: 60-75m/punto promedio
# - USs de 5 puntos: 50-60m/punto promedio
# - USs de 8 puntos: 45-55m/punto promedio

# Insight: USs más grandes son más eficientes
# (economías de escala)
```

## Ejemplo 5: Tracking con Múltiples Pausas

```bash
$ /implement-us US-003

# Primera pausa
$ /track-pause "Code review"
# ... 20 minutos ...
$ /track-resume

# Segunda pausa
$ /track-pause "Consulta técnica"
# ... 10 minutos ...
$ /track-resume

# Tercera pausa
$ /track-pause "Break"
# ... 5 minutos ...
$ /track-resume

# Al finalizar, ver reporte
$ /track-report US-003
```

**Resultado:**
- Reporte muestra 3 pausas con razones
- Total pausado: 35 minutos
- Tiempo efectivo correcto

## Ejemplo 6: Monitoreo en Tiempo Real

```bash
$ /implement-us US-004

# Durante la implementación, en otra terminal:
$ /track-status

# Output:
# - Fase actual: Fase 3 - Implementación
# - Tiempo efectivo: 1h 30m
# - Tareas completadas: 8/15
# - Sin pausa activa

# Verificar progreso periódicamente
$ /track-status
```

## Ejemplo 7: Análisis de Fases Críticas

Después de varias USs, identificar fases problemáticas:

```bash
# Revisar 5 USs recientes
$ /track-history --last 5

# Generar reportes individuales
$ /track-report US-010
$ /track-report US-011
$ /track-report US-012

# Observar patrón:
# - Fase 3 (Implementación): Siempre +20-30% sobre estimado
# - Fase 4 (Tests): Generalmente dentro del estimado
# - Fase 7 (Quality Gates): Siempre bajo el estimado

# Acción: Aumentar estimaciones de Fase 3 en un 25%
```

## Formato de Reportes

### Track Status
```
📊 Estado del Tracking - US-001
Estado: ▶️ En progreso
Fase actual: Fase 3 - Implementación
Tiempo efectivo: 1h 45m
Tareas completadas: 10/15 (67%)
```

### Track Report
```
📈 Reporte de Tracking - US-001
Estado: ✅ Completado
Tiempo total: 3h 45m
Tiempo efectivo: 3h 15m
Varianza: +15m (+8.3%)

Fases ejecutadas: 10 fases
Pausas: 1 pausa (30m)
Insights: Implementación más lenta de lo esperado
```

### Track History
```
📚 Historial de Tracking
Total USs: 15
Puntos totales: 65
Tiempo total: 48h 30m
Promedio por punto: 44.8m/punto
```
