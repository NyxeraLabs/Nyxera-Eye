<!--
Copyright (c) 2026 NyxeraLabs
Author: Jose Maria Micoli
Licensed under BSL 1.1
Change Date: 2033-02-17 -> Apache-2.0
-->

# Troubleshooting Manual

## `ModuleNotFoundError: nyxera_eye`

Use:

```bash
PYTHONPATH=src <command>
```

## `poetry` not found

Use the local venv flow instead:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pytest fastapi httpx arq uvicorn
```

## Scan counts reset instead of accumulating

Confirm you are running the updated runtime under `src/nyxera_eye/api/ops_runtime.py`.

Expected behavior now:

- repeated single scans add to the device inventory
- scan loop continues accumulation
- device IDs remain stable

## Duplicate devices appear in the registry

The live runtime deduplicates devices by canonical network identity.

If duplicates remain after updating code, restart the backend process so the in-memory store is rebuilt from the corrected runtime.

## World map shows rural or sparse locations only

The current runtime maps assets to a broad major-city catalog with small urban jitter.

If you still see stale rural markers:

1. restart backend
2. run a fresh scan
3. reload `/map`

## Frontend typecheck fails on `.next/types`

Use the current `frontend/tsconfig.json` that excludes `.next/types/**/*.ts` from standalone `tsc --noEmit`.

## API returns `401`, `403`, or `429`

- `401`: missing or invalid token
- `403`: token role is too low
- `429`: rate limit exceeded

## Audit page returns no rows

`/audit` requires an admin-capable token for the backend `GET /audit/events` route.
