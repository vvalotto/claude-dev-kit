# Guía de Usuario - Sistema de Tracking

## Introducción

El sistema de tracking de tiempo registra automáticamente el tiempo invertido en implementar Historias de Usuario con el skill `/implement-us`.

## Tracking Automático

El tracking se inicia automáticamente al ejecutar:

```bash
/implement-us US-001
```

**No requiere acción manual del usuario.**

El sistema trackea automáticamente:
- Tiempo de inicio y fin de cada fase (0-9)
- Duración total de la implementación
- Pausas manuales (cuando las hagas)
- Métricas de varianza (estimado vs. real)

## Comandos de Control Manual

### Pausar Tracking

Cuando necesites interrumpir el trabajo:

```bash
/track-pause "Reunión del equipo"
```

**Casos de uso:**
- Reuniones
- Breaks
- Code reviews
- Atender otras prioridades
- Interrupciones inesperadas

El tiempo durante la pausa NO se contabiliza en las métricas.

### Reanudar Tracking

Para continuar el trabajo:

```bash
/track-resume
```

El sistema calcula automáticamente la duración de la pausa.

### Ver Estado Actual

Para ver el progreso y tiempo transcurrido:

```bash
/track-status
```

**Muestra:**
- Fase y tarea actual
- Tiempo transcurrido y efectivo
- Progreso de tareas
- Pausa activa (si existe)

## Reportes

### Reporte de una US

Ver reporte detallado de implementación:

```bash
# Tracking actual
/track-report

# US específica
/track-report US-001
```

**Incluye:**
- Resumen de tiempo (total, efectivo, pausado)
- Fases ejecutadas con duraciones
- Pausas registradas con razones
- Métricas finales con varianza
- Insights automáticos

### Historial de Tracking

Ver todas las USs trackeadas:

```bash
# Todo el historial
/track-history

# Últimas 10 USs
/track-history --last 10
```

**Muestra:**
- Tabla con últimas USs completadas
- Estadísticas agregadas (total puntos, tiempo)
- Promedio de tiempo por punto

## Persistencia

Los datos se guardan en:
```
.claude/tracking/{us_id}-tracking.json
```

**Formato:** JSON estructurado con toda la información del tracking.

**Ejemplo:**
```
.claude/tracking/US-001-tracking.json
.claude/tracking/US-002-tracking.json
.claude/tracking/US-003-tracking.json
```

## FAQ

### ¿El tracking funciona si cierro Claude Code?

Sí, los datos se guardan automáticamente después de cada operación. Al reabrir y continuar con `/implement-us`, el tracking se reanuda desde donde quedó.

### ¿Puedo editar manualmente los archivos JSON?

Sí, pero no se recomienda. Los archivos siguen un esquema específico y una edición incorrecta puede romper el tracking.

### ¿Qué pasa si olvido hacer /track-resume?

El tiempo pausado se sigue contabilizando. Puedes editar el JSON manualmente si fue un error, o simplemente hacer `/track-resume` cuando te acuerdes. El tiempo pausado no afecta las métricas de tiempo efectivo.

### ¿Cómo se calcula la varianza?

```
Varianza = Tiempo Real - Tiempo Estimado
Varianza % = (Varianza / Tiempo Estimado) * 100
```

Por ejemplo:
- Estimado: 120 minutos
- Real: 135 minutos
- Varianza: +15 minutos (+12.5%)

### ¿Puedo desactivar el tracking?

Actualmente no. El tracking es parte integral del skill `/implement-us`. Los datos son útiles para mejorar estimaciones futuras y entender dónde se invierte el tiempo.

### ¿El tracking consume muchos recursos?

No. El sistema es ligero:
- Solo guarda JSON en disco
- No usa base de datos
- No requiere servicios adicionales
- Impacto mínimo en rendimiento

## Ejemplo de Flujo Completo

```bash
# 1. Iniciar implementación
$ /implement-us US-001

# ... Claude implementa Fases 0-2 ...

# 2. Durante Fase 3, tienes una reunión
$ /track-pause "Daily standup"

# ... 15 minutos de reunión ...

# 3. Continuar trabajo
$ /track-resume

# ... Claude continúa con Fases 3-9 ...

# 4. Ver estado mientras trabaja
$ /track-status

# 5. Al finalizar, ver reporte
$ /track-report US-001

# 6. Ver historial de todas las USs
$ /track-history
```

## Interpretación de Métricas

### Tiempo Total
Duración desde el inicio hasta el fin de la implementación, incluyendo pausas.

### Tiempo Efectivo
Tiempo realmente trabajando, sin pausas.

### Tiempo Pausado
Suma de todas las pausas manuales.

### Varianza Positiva (+)
La implementación tomó más tiempo del estimado. Común en:
- Bugs inesperados
- Cambios de scope
- Complejidad subestimada

### Varianza Negativa (-)
La implementación fue más rápida del estimado. Indica:
- Estimación conservadora
- Alta eficiencia
- Menos complejidad de la esperada

## Mejora Continua

Usa los reportes para:
1. **Identificar cuellos de botella** - ¿Qué fases toman más tiempo?
2. **Mejorar estimaciones** - Ajustar puntos basado en varianza histórica
3. **Optimizar procesos** - Reducir tiempo en fases específicas
4. **Planificar sprints** - Usar promedio por punto para capacidad del equipo

## Soporte

Para problemas o preguntas:
- Ver documentación técnica: `docs/developer/architecture/tracking.md`
- Ver ejemplos: `docs/user/tracking/examples.md`
- Reportar issues en el repositorio del proyecto
