# Sprint 16 - Observability

## Objective
Expose core platform KPIs in Prometheus format and add span timing utility for tracing.

## Source Code
- `src/nyxera_eye/observability/metrics.py`
- `src/nyxera_eye/observability/tracing.py`
- `src/nyxera_eye/api/app.py` (`/observability/prometheus` endpoint)

## Logic
- `PlatformMetrics` dataclass validates metric domains:
  - queue depth >= 0
  - throughput >= 0
  - probe success rate in `[0,100]`
  - GPU utilization in `[0,100]`
  - storage growth >= 0
- `export_prometheus()` emits HELP/TYPE/metric lines for scraping.
- `start_span()` context manager creates trace/span IDs and computes duration ms on exit.
- API endpoint serves metrics text with admin authorization.

## Architecture Impact
- Observability layer is implementation-agnostic and can feed Prometheus/Grafana without deep coupling.

## Validation Notes
- `tests/test_observability.py`

## Mermaid Diagram

```mermaid
flowchart LR
  A[Runtime Metrics] --> B[PlatformMetrics Validation]
  B --> C[Prometheus Exporter]
  C --> D[/observability/prometheus]
  E[Operation Block] --> F[start_span Context]
  F --> G[Span Duration + IDs]
```
