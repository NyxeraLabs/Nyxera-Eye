<!--
Copyright (c) 2026 NyxeraLabs
Author: José María Micoli
Licensed under BSL 1.1
Change Date: 2033-02-17 → Apache-2.0

You may:
✔ Study
✔ Modify
✔ Use for internal security testing

You may NOT:
✘ Offer as a commercial service
✘ Sell derived competing products
-->

# Infrastructure Notes

Current local operator runtime uses:

- Python FastAPI backend in `src/nyxera_eye/api`
- Next.js frontend in `frontend/app`

## Runtime Services

Nyxera Eye Sprint 2 depends on the following services declared in `docker-compose.yml`:

- `mongodb`
- `opensearch`
- `redis`
- `minio`
- `prometheus`
- `grafana`

## Queue Layer

- Redis is used as the initial task queue backend.
- Python worker integration uses `arq`.

## Local Bring-up

```bash
docker compose up -d
```

## Validation

```bash
docker compose ps
docker compose config -q
```
