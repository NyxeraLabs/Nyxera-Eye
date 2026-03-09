<!--
Copyright (c) 2026 NyxeraLabs
Author: José María Micoli
Licensed under BSL 1.1
Change Date: 2033-02-17 → Apache-2.0
-->

# Architecture Migration Map

`docs/ARCHITECTURE.md` is the authoritative target structure for all roadmap work starting from Sprint 22.

This document defines the transition mapping from the current repository layout to the architecture-compliant layout.

## Legacy to Target Mapping

### Application Code

| Legacy Path | Target Path | Scope |
| --- | --- | --- |
| `src/nyxera_eye/collectors` | `internal/scanner/discovery` | target generation and collection logic |
| `src/nyxera_eye/protocols` | `internal/scanner/probes` | service and protocol probe implementations |
| `src/nyxera_eye/queue` | `internal/scanner/queue` | scan task queue integration |
| `src/nyxera_eye/workers` | `internal/scanner/workers` | scanner worker pipeline |
| `src/nyxera_eye/fingerprinting` | `internal/intel/fingerprint` | device and web fingerprint logic |
| `src/nyxera_eye/vulnintel` | `internal/intel/vulnerabilities` | vulnerability intelligence and scoring |
| `src/nyxera_eye/change_detection` | `internal/intel/classification` | state-delta and relationship analysis until split further |
| `src/nyxera_eye/enrichment` | `internal/intel/vendor` and `internal/intel/firmware` | enrichment logic moved by concern |
| `src/nyxera_eye/schema` | `internal/database/models` and `internal/database/migrations` | schema and migration logic |
| `src/nyxera_eye/api` | `internal/api/handlers`, `internal/api/router`, `internal/api/middleware` | HTTP handlers and middleware |
| `src/nyxera_eye/observability` | `internal/telemetry` | metrics and tracing |

### Entry Points

| Legacy Path | Target Path | Scope |
| --- | --- | --- |
| `scripts/` runtime entry scripts | `cmd/scanner`, `cmd/api`, `cmd/worker` | executable entrypoints |

### UI

| Legacy Path | Target Path | Scope |
| --- | --- | --- |
| `frontend/app/page.tsx` | `web/dashboard` | primary dashboard surface |
| `frontend/app/findings` | `web/assets` | asset and finding inventory |
| `frontend/app/map` | `web/graph` | topology and map visualization |
| `frontend/app/events` | `web/investigation` | investigation workflow |
| `frontend/app/components` | `web/*` | shared UI primitives relocated by surface ownership |
| `frontend/public` | `web/assets` | static web assets |

### Configuration and Deployment

| Legacy Path | Target Path | Scope |
| --- | --- | --- |
| `config` | `configs` | service configuration assets |
| `infra` | `deployments` | observability and deployment manifests |

## Transition Policy

* New Sprint 22+ feature code must target architecture-compliant paths.
* Legacy paths may remain temporarily for compatibility and staged migration.
* Temporary wrappers or forwarding modules are allowed only to preserve behavior during migration.
* Legacy modules must not become the primary destination for new roadmap tasks.

## CI Enforcement Policy

CI rejects Sprint 22+ additions in legacy implementation roots:

* `src/`
* `frontend/`
* `config/`
* `infra/`

Exceptions:

* `docs/`
* `tests/`
* `scripts/`
* existing maintenance or bug-fix work explicitly scoped outside roadmap feature delivery
