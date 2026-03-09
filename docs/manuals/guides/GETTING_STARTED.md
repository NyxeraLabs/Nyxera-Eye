<!--
Copyright (c) 2026 NyxeraLabs
Author: Jose Maria Micoli
Licensed under BSL 1.1
Change Date: 2033-02-17 -> Apache-2.0
-->

# Getting Started Guide

## Goal

Bring up the current Nyxera Eye runtime and validate the main operator surfaces.

## Quick Start

```bash
cd /home/xoce/Workspace/Nyxera-Eye
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install pytest fastapi httpx arq uvicorn
cd frontend && npm ci && cd ..
```

Run the baseline checks:

```bash
./.venv/bin/python scripts/lint_repo.py
./.venv/bin/pytest tests/test_ops_runtime.py -q
docker compose config -q
cd frontend && npm run typecheck
```

Then launch the runtime:

```bash
export NYXERA_API_BOOTSTRAP_TOKEN=nyxera-dev-token
export NYXERA_API_BOOTSTRAP_ROLE=admin
PYTHONPATH=src .venv/bin/uvicorn nyxera_eye.api.app:app --host 127.0.0.1 --port 18080
```

In another shell:

```bash
cd /home/xoce/Workspace/Nyxera-Eye/frontend
NEXT_PUBLIC_NYXERA_API_BASE=http://127.0.0.1:18080 npm run dev
```

## First Checks

1. Open the dashboard and run `Single Scan`.
2. Start `Scan Loop` and confirm device counts increase instead of resetting.
3. Open `/devices` and search for a vendor or IP.
4. Open `/findings` and investigate a finding into `/devices/{deviceId}`.
5. Open `/map` and verify distribution across major cities.
