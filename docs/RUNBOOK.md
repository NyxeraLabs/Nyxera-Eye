<!--
Copyright (c) 2026 NyxeraLabs
Author: Jose Maria Micoli
Licensed under BSL 1.1
Change Date: 2033-02-17 -> Apache-2.0
-->

# Nyxera Eye Runbook

Date: 2026-03-09

## Purpose

This runbook covers the current manual validation path for the live FastAPI and Next.js runtime.

## Preconditions

- Linux or macOS shell access
- Python 3.12+
- Node.js 20+
- Docker with Compose plugin
- Access to `/home/xoce/Workspace/Nyxera-Eye`

## Backend Setup

```bash
cd /home/xoce/Workspace/Nyxera-Eye
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install pytest fastapi httpx arq uvicorn
```

## Frontend Setup

```bash
cd /home/xoce/Workspace/Nyxera-Eye/frontend
npm ci
cd /home/xoce/Workspace/Nyxera-Eye
```

## Static and Runtime Validation

```bash
./.venv/bin/python scripts/lint_repo.py
./.venv/bin/pytest tests/test_ops_runtime.py -q
docker compose config -q
cd frontend && npm run typecheck
```

## Backend Smoke Start

```bash
cd /home/xoce/Workspace/Nyxera-Eye
export NYXERA_API_BOOTSTRAP_TOKEN=nyxera-dev-token
export NYXERA_API_BOOTSTRAP_ROLE=admin
PYTHONPATH=src .venv/bin/uvicorn nyxera_eye.api.app:app --host 127.0.0.1 --port 18080
```

## Frontend Smoke Start

```bash
cd /home/xoce/Workspace/Nyxera-Eye/frontend
NEXT_PUBLIC_NYXERA_API_BASE=http://127.0.0.1:18080 npm run dev
```

## Manual Functional Checks

1. Run a single scan from the dashboard and confirm asset count increases.
2. Start the scan loop and confirm the device inventory continues to accumulate instead of resetting.
3. Open `/devices` and search by IP, vendor, and country.
4. Open `/findings` and filter by severity and status.
5. Open a device investigation page from `/devices/{deviceId}`.
6. Open `/map` and confirm markers are distributed across major world cities rather than only a few rural coordinates.
7. Open `/audit` with an admin token and confirm event rows load.

## Expected Behavior

- repeated scans update a stable device registry
- device IDs remain stable across scan runs
- findings remain attached to their devices
- investigation links open a real detail page
- audit, settings, findings, devices, map, and dashboard surfaces all load from the same live runtime

## Evidence Collection

```bash
git branch --show-current
git rev-parse --short HEAD
git status --short
```

Store:

- lint output
- pytest output
- compose validation output
- screenshots of dashboard, devices, findings, and map
