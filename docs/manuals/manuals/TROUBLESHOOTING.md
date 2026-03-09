# Troubleshooting Manual

## 1. `ModuleNotFoundError: nyxera_eye`

Run commands with:

```bash
PYTHONPATH=src <command>
```

Example:

```bash
PYTHONPATH=src python scripts/e2e_full_validation.py
```

## 2. `pytest` or `poetry` not found

Install required tooling:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pytest fastapi httpx arq
```

or install Poetry and run `poetry install`.

## 3. Docker Compose validation fails

Check Docker service status and version:

```bash
docker --version
docker compose version
docker compose config -q
```

## 4. API returns `401` on protected endpoints

Confirm token is present:

```text
X-API-Token: <token>
```

If using bootstrap token, ensure env variables were exported before app start.

## 5. API returns `403`

Token role is below endpoint minimum role.  
Use correct role (`analyst`, `operator`, or `admin`) for the endpoint.

## 6. API returns `429`

Rate limiter reached max requests per window.  
Retry after rate-limit window or raise limit for controlled test environments.

## 7. E2E script fails in queue phase

Validate:
- `src/nyxera_eye/queue/redis_queue.py` imports succeed
- no local edits broke fake queue patch behavior

## 8. Unexpected modified files after QA run

Inspect:

```bash
git status --short
```

If artifacts are expected, clean them explicitly before commit.  
Never use destructive git commands unless approved.
