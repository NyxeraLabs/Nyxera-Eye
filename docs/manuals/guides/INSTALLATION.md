# Installation Guide

## 1. Clone and Enter Repository

```bash
git clone <your-repo-url> Nyxera-Eye
cd Nyxera-Eye
```

## 2. Python Environment

### Option A: Poetry

```bash
poetry install --no-interaction
```

### Option B: venv + pip

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install pytest fastapi httpx arq
```

## 3. Infrastructure Validation

```bash
docker compose config -q
```

## 4. Local Validation

```bash
python -m compileall -q src tests scripts
PYTHONPATH=src python scripts/e2e_full_validation.py
```

## 5. Optional API Bootstrap Token

```bash
export NYXERA_API_BOOTSTRAP_TOKEN=nyxera-dev-token
export NYXERA_API_BOOTSTRAP_ROLE=admin
```

Then start API (example):

```bash
PYTHONPATH=src uvicorn nyxera_eye.api.app:app --host 127.0.0.1 --port 8000
```
