# Getting Started Guide

## Goal

Run Nyxera Eye locally and execute the full deterministic E2E validation flow.

## Prerequisites

- Python 3.12+
- Docker with Compose plugin
- Git

## Quick Start

```bash
cd /home/xoce/Workspace/Nyxera-Eye
git checkout dev
git pull origin dev
```

Install dependencies (Poetry path):

```bash
poetry install --no-interaction
```

Run core checks:

```bash
python -m compileall -q src tests scripts
docker compose config -q
PYTHONPATH=src python scripts/e2e_full_validation.py
```

Expected final output:

```text
E2E full roadmap validation passed (local deterministic path).
```

## Where to Go Next

- [Full User Guide](../manuals/USER_GUIDE.md)
- [E2E Validation Guide](E2E_VALIDATION.md)
- [QA Runbook](../../RUNBOOK.md)
