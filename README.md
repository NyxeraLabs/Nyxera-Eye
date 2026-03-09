<!--
Copyright (c) 2026 NyxeraLabs
Author: Jose Maria Micoli
Licensed under BSL 1.1
Change Date: 2033-02-17 -> Apache-2.0
-->

# Nyxera Eye

Nyxera Eye is a continuous asset intelligence platform for authorized IoT, ICS, and network exposure analysis.

It combines discovery-style scanning, service metadata, web fingerprinting, vendor and firmware hints, vulnerability context, and operator-facing investigation workflows in one platform.

## Current Platform Capabilities

- Accumulating scan runtime with stable device identity and finding history
- Searchable device registry with severity, country, vendor, and text filters
- Searchable findings registry with severity, status, and device filters
- Device investigation view with services, fingerprint metadata, linked findings, and recent events
- Dashboard charts for findings severity, status, vendor distribution, port distribution, country coverage, and scan growth
- World map visualization for assets and events
- API token auth, RBAC, rate limiting, and audit logging
- Python backend plus Next.js/TypeScript operator UI

## Main UI Surfaces

- `/` dashboard
- `/devices` full device registry
- `/devices/{deviceId}` device investigation
- `/findings` findings registry and action panel
- `/map` world map
- `/events` event stream
- `/settings` runtime settings
- `/audit` audit ledger

## Quick Start

```bash
cd /home/xoce/Workspace/Nyxera-Eye
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install pytest fastapi httpx arq uvicorn
cd frontend && npm ci && cd ..
```

Run the key local validation commands:

```bash
./.venv/bin/python scripts/lint_repo.py
./.venv/bin/pytest tests/test_ops_runtime.py -q
docker compose config -q
cd frontend && npm run typecheck
```

## Active Runtime Endpoints

Core live frontend API routes:

- `GET /frontend/ops-feed`
- `POST /frontend/scan`
- `POST /frontend/scan/start`
- `POST /frontend/scan/stop`
- `GET /frontend/scan/status`
- `GET /frontend/devices`
- `GET /frontend/devices/{device_id}`
- `GET /frontend/findings`
- `GET /frontend/findings/{finding_id}`
- `POST /frontend/findings/{finding_id}/action`
- `GET /frontend/findings/{finding_id}/export`

## Repository Notes

- Active backend runtime currently lives under `src/nyxera_eye/api`.
- Active web runtime currently lives under `frontend/app`.
- Architecture target documentation still exists under `docs/ARCHITECTURE.md` and `docs/ARCHITECTURE_MIGRATION.md`.
- Generated frontend artifacts such as `frontend/.next/` and dependencies in `frontend/node_modules/` are ignored by git.

## Documentation

- [docs/manuals/INDEX.md](docs/manuals/INDEX.md)
- [docs/RUNBOOK.md](docs/RUNBOOK.md)
- [docs/ROADMAP.md](docs/ROADMAP.md)
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- [docs/ARCHITECTURE_MIGRATION.md](docs/ARCHITECTURE_MIGRATION.md)
- [docs/COMPLIANCE.md](docs/COMPLIANCE.md)
- [docs/ETHICS.md](docs/ETHICS.md)
- [docs/INFRA.md](docs/INFRA.md)

## Safety

Nyxera Eye is for authorized security testing and defensive research only.

- No brute force
- No exploitation
- No intrusive scanning outside explicit approved scope

Read:

- [docs/COMPLIANCE.md](docs/COMPLIANCE.md)
- [docs/ETHICS.md](docs/ETHICS.md)
- [docs/SECURITY_DISCLOSURE.md](docs/SECURITY_DISCLOSURE.md)

## License

Business Source License 1.1. See [LICENSE](LICENSE).
