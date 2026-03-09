# Nyxera Eye QA Manual Runbook

Date: 2026-03-09  
Scope: Manual QA execution for full platform validation (Sprint 17)  
Primary target: `scripts/e2e_full_validation.py`

## 1. Purpose

This runbook defines the manual QA flow to validate Nyxera Eye end-to-end across implemented roadmap phases.

It covers:
- environment setup
- dependency validation
- infrastructure config checks
- full deterministic E2E run
- optional focused/manual checks
- evidence collection and sign-off

## 2. Preconditions

- OS: Linux/macOS with shell access
- Python: 3.12+
- Docker + Docker Compose plugin
- Git
- Access to repo root: `Nyxera-Eye`

## 3. Repository Setup

```bash
cd /home/xoce/Workspace/Nyxera-Eye
git checkout dev
git pull origin dev
```

Confirm expected files exist:

```bash
ls -la scripts/e2e_full_validation.py docs/E2E_AUDIT.md docs/ROADMAP.md
```

## 4. Python Environment Setup

Use one of the two methods below.

### Option A: Poetry (preferred)

```bash
poetry --version
poetry install --no-interaction
```

### Option B: venv + pip

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install pytest fastapi httpx arq
```

## 5. Static/Build Sanity Checks

Run from repo root:

```bash
python -m compileall -q src tests scripts
docker compose config -q
```

Expected result:
- both commands exit with code `0`
- no error output

## 6. Full E2E Validation (Primary Gate)

Run:

```bash
PYTHONPATH=src python scripts/e2e_full_validation.py
```

Expected output:

```text
E2E full roadmap validation passed (local deterministic path).
```

Expected result:
- exit code `0`
- no traceback

## 7. Optional Focused QA Checks

### 7.1 Unit/Integration test sweep

Poetry:

```bash
poetry run pytest -q
```

venv:

```bash
PYTHONPATH=src pytest -q
```

Expected:
- all tests pass

### 7.2 Security-protected API smoke (manual)

Set bootstrap token and run API app:

```bash
export NYXERA_API_BOOTSTRAP_TOKEN=qa-bootstrap-token
export NYXERA_API_BOOTSTRAP_ROLE=admin
```

Minimal endpoint checks (when app is running):

```bash
curl -s http://127.0.0.1:8000/health
curl -i -s http://127.0.0.1:8000/search/opensearch
curl -i -s -H "X-API-Token: qa-bootstrap-token" "http://127.0.0.1:8000/search/opensearch?q=camera"
```

Expected:
- `/health` returns `{"status":"ok"}`
- protected endpoint without token returns `401`
- protected endpoint with token returns `200`

### 7.3 Observability endpoint smoke

```bash
curl -s -H "X-API-Token: qa-bootstrap-token" "http://127.0.0.1:8000/observability/prometheus?queue_depth=5&mining_throughput=100.1&probe_success_rate=98.2&gpu_utilization=55.0&storage_growth_gb=0.25"
```

Expected response contains:
- `nyxera_queue_depth 5`
- `nyxera_mining_throughput 100.10`
- `nyxera_probe_success_rate 98.20`
- `nyxera_gpu_utilization 55.00`
- `nyxera_storage_growth_gb 0.250`

## 8. QA Evidence Checklist

Collect and attach:
- command history used for QA session
- output of:
  - `python -m compileall -q src tests scripts`
  - `docker compose config -q`
  - `PYTHONPATH=src python scripts/e2e_full_validation.py`
  - optional `pytest -q`
- current branch and commit:

```bash
git branch --show-current
git rev-parse --short HEAD
git status --short
```

## 9. Pass/Fail Criteria

PASS when all are true:
- compile check passed
- docker compose config check passed
- full E2E script passed with expected message
- no unexpected modified/untracked files after run (except approved artifacts)

FAIL when any are true:
- traceback or non-zero exit in primary E2E
- infrastructure config invalid
- protected API checks do not enforce auth behavior

## 10. Troubleshooting

### `ModuleNotFoundError: nyxera_eye`

Use:

```bash
PYTHONPATH=src python scripts/e2e_full_validation.py
```

### `pytest: command not found`

Install test dependencies (Poetry or venv method in section 4).

### `docker: command not found` or compose errors

Install/start Docker Desktop or Docker Engine + Compose plugin, then rerun section 5.

### FastAPI checks fail with 401 even with token

Confirm env vars are exported in same shell before app start:
- `NYXERA_API_BOOTSTRAP_TOKEN`
- `NYXERA_API_BOOTSTRAP_ROLE`

## 11. Sign-off Template

```text
QA RUNBOOK EXECUTION REPORT
Date:
Operator:
Branch:
Commit:

Compile check: PASS/FAIL
Compose check: PASS/FAIL
E2E full validation: PASS/FAIL
Optional pytest sweep: PASS/FAIL/NOT RUN
Optional API auth smoke: PASS/FAIL/NOT RUN

Evidence paths:
- 
- 

Notes:

Final decision: PASS/FAIL
```
