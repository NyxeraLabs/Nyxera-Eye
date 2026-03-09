# Sprint 04 - Canonical Schema

## Objective
Define canonical device schema and migration path from legacy flat records.

## Source Code
- `src/nyxera_eye/schema/models.py`
- `src/nyxera_eye/schema/validation.py`
- `src/nyxera_eye/schema/migrations.py`

## Data Model
`DeviceSchema` captures:
- identity/network: `device_id`, `ip`, `hostname`, `asn`, `organization`, geo
- service set: list of `ServiceRecord`
- fingerprints: favicon/JA3/JARM
- IoT metadata: vendor/model/firmware
- vulnerability list
- media snapshot reference

## Logic
- Validation checks IP correctness, lat/lon ranges, port range, severity taxonomy.
- Migration maps legacy keys (`org`, flat `port/banner`) into v1 nested structure.

## Architecture Impact
- Schema is independent from transport/storage engines.
- v1 migration utility is deterministic and side-effect free.

## Validation Notes
- `tests/test_schema.py` validates valid/invalid schema paths and migration mapping.

## Risks and Follow-ups
- Versioning strategy beyond v1 exists conceptually but no multi-version migration chain yet.

## Mermaid Diagram

```mermaid
flowchart LR
  A[Inputs] --> B[Core Module Logic]
  B --> C[Normalized Output]
  C --> D[Validation Tests]
```
