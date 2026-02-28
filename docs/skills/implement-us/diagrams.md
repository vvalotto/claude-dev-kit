# Diagramas Visuales — implement-us

**Versión:** 2.1.0 (v1.3.0 del framework)
**Última actualización:** 2026-02-28

Referencia visual del skill `implement-us`. Incluye el flujo de ejecución de las 10 fases y el mapa de artefactos generados.

---

## Flujo de Ejecución

Muestra el pipeline completo: fases en orden estricto, puntos de aprobación (🛑), bifurcación skip-BDD y loop de recuperación en quality gates.

```mermaid
flowchart TD
    START(["/implement-us US-XXX"]) --> P0

    subgraph SETUP ["🔍 Validación"]
        P0["Fase 0 · Validación de Contexto"]
    end

    P0 --> BDD{"¿Aplica BDD?"}
    BDD -- Sí --> P1
    BDD -- "--skip-bdd" --> P2

    subgraph BDD_GEN ["📋 BDD"]
        P1["Fase 1 · Escenarios BDD"]
    end

    P1 --> P2

    subgraph PLAN ["📐 Planning"]
        P2["Fase 2 · Plan de Implementación"]
        STOP1(["🛑 Aprobar plan"])
        P2 --> STOP1
    end

    STOP1 --> P3

    subgraph IMPL ["⚙️ Implementación & Testing"]
        P3["Fase 3 · Implementación"]
        P4["Fase 4 · Tests Unitarios"]
        P5["Fase 5 · Tests de Integración"]
        P6["Fase 6 · Validación BDD"]
        P3 --> P4 --> P5 --> P6
    end

    P6 --> P7

    subgraph QUALITY ["✅ Calidad"]
        P7["Fase 7 · Quality Gates"]
    end

    P7 --> QG{"¿Gates OK?"}
    QG -- No --> P3
    QG -- Sí --> P8

    subgraph DELIVERY ["📦 Entrega"]
        P8["Fase 8 · Documentación"]
        STOP2(["🛑 Reporte en disco"])
        P9["Fase 9 · Reporte Final"]
        P8 --> STOP2 --> P9
    end

    P9 --> END(["✅ US Completada"])

    style STOP1 fill:#e74c3c,color:#fff
    style STOP2 fill:#e74c3c,color:#fff
    style START fill:#27ae60,color:#fff
    style END fill:#27ae60,color:#fff
```

> Los nodos 🛑 son bloques sincrónicos: el agente no avanza hasta que el usuario da aprobación explícita (Fase 2) o hasta que el reporte existe en disco (Fase 9).

---

## Mapa de Artefactos

Muestra el artefacto principal generado por cada fase y su ruta canónica en disco.

```mermaid
flowchart LR
    subgraph PHASES ["Fases"]
        direction TB
        P0["Fase 0"]
        P1["Fase 1"]
        P2["Fase 2"]
        P3["Fase 3"]
        P4["Fase 4"]
        P5["Fase 5"]
        P6["Fase 6"]
        P7["Fase 7"]
        P8["Fase 8"]
        P9["Fase 9"]
    end

    subgraph ARTIFACTS ["Artefactos generados"]
        direction TB
        A0["docs/plans/{US}-context.md"]
        A1["tests/features/{US}-{nombre}.feature"]
        A2["docs/plans/{US}-plan.md"]
        A3["src/*.py"]
        A4["tests/unit/test_*.py"]
        A5["tests/integration/test_*.py"]
        A6["tests/step_defs/test_*_steps.py"]
        A7["quality/reports/{US}-quality.json"]
        A8["Docstrings · CHANGELOG · docs arquitectura"]
        A9["docs/reports/{US}-report.md"]
    end

    P0 --> A0
    P1 --> A1
    P2 --> A2
    P3 --> A3
    P4 --> A4
    P5 --> A5
    P6 --> A6
    P7 --> A7
    P8 --> A8
    P9 --> A9

    style A0 fill:#dfe6e9
    style A1 fill:#dfe6e9
    style A2 fill:#dfe6e9
    style A3 fill:#dfe6e9
    style A4 fill:#dfe6e9
    style A5 fill:#dfe6e9
    style A6 fill:#dfe6e9
    style A7 fill:#dfe6e9
    style A8 fill:#dfe6e9
    style A9 fill:#dfe6e9
```

> La ruta canónica completa de cada artefacto está definida en [`skills/implement-us/artifacts.md`](../../../../skills/implement-us/artifacts.md).

---

## Navegación

[← Índice del skill](index.md) · [Fase 0 →](phase-0.md)
