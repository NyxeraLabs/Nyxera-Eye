<!--
Copyright (c) 2026 NyxeraLabs
Author: Jose Maria Micoli
Licensed under BSL 1.1
Change Date: 2033-02-17 -> Apache-2.0
-->

# Installation Guide

## Repository

```bash
git clone <your-repo-url> Nyxera-Eye
cd Nyxera-Eye
```

## Python Runtime

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install pytest fastapi httpx arq uvicorn
```

## Frontend Runtime

```bash
cd frontend
npm ci
cd ..
```

## Validation Commands

```bash
./.venv/bin/python scripts/lint_repo.py
./.venv/bin/pytest tests/test_ops_runtime.py -q
docker compose config -q
cd frontend && npm run typecheck
```

## Optional Local API Bootstrap

```bash
export NYXERA_API_BOOTSTRAP_TOKEN=nyxera-dev-token
export NYXERA_API_BOOTSTRAP_ROLE=admin
```

## Start API

```bash
PYTHONPATH=src .venv/bin/uvicorn nyxera_eye.api.app:app --host 127.0.0.1 --port 18080
```

## Start Frontend

```bash
cd frontend
NEXT_PUBLIC_NYXERA_API_BASE=http://127.0.0.1:18080 npm run dev
```
