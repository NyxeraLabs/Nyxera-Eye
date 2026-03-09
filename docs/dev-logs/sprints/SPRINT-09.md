# Sprint 09 - API Search Layer

## Objective
Expose FastAPI endpoints for OpenSearch query generation and target card construction.

## Source Code
- `src/nyxera_eye/api/app.py`
- `src/nyxera_eye/api/opensearch.py`
- `src/nyxera_eye/api/models.py`
- `src/nyxera_eye/api/target_cards.py`

## Logic
- `OpenSearchQueryService.build_device_query()` builds `match_all` or `bool.must` queries with field filters.
- Search filters include ASN, vendor, vulnerability, country, and exposure score minimum.
- Target card builder summarizes service count and top vulnerability for UI consumption.

## Architecture Impact
- API layer remains composition-driven: endpoint code delegates to service functions and serializers.

## Validation Notes
- `tests/test_api.py`

## Mermaid Diagram

```mermaid
flowchart LR
  A[HTTP Request] --> B[FastAPI Endpoint]
  B --> C[SearchFilters Model]
  C --> D[OpenSearch Query Service]
  D --> E[Query Payload]
  B --> F[Target Card Builder]
  F --> G[UI-ready Summary]
```
