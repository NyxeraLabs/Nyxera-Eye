# Sprint 21 - Security, Identity, and Auditability (2026-03-09)

## Scope Delivered

- Enforced secret hygiene and repository history remediation for leaked TLS key artifacts.
- Dockerized API and frontend runtime so application services run inside Compose stack.
- Added frontend authentication UX (`/login`, `/register`) with token-backed API session flow.
- Added centralized frontend configuration UI (`/settings`) for runtime and scan defaults.
- Implemented end-to-end audit traceability for API operations and user actions.

## Code Paths Updated

- `src/nyxera_eye/api/app.py`
  - Added auth endpoints:
    - `POST /auth/register`
    - `POST /auth/login`
    - `GET /auth/me`
    - `POST /auth/logout`
  - Added settings endpoints:
    - `GET /frontend/settings`
    - `PUT /frontend/settings`
  - Added audit endpoint:
    - `GET /audit/events` (admin only)
  - Added HTTP middleware that records each request with actor, action, status, method, path, and IP.
  - Added OpenAPI URLs:
    - `/api/docs`
    - `/api/redoc`
    - `/api/openapi.json`

- `src/nyxera_eye/api/auth_runtime.py`
  - New runtime auth store with:
    - username registry
    - PBKDF2-HMAC password hashing
    - role assignment
    - authentication checks
  - Default bootstrap admin user support via env vars.

- `src/nyxera_eye/api/audit_runtime.py`
  - New audit ledger store with:
    - in-memory recent event ring
    - JSONL append-only persistence (`.run/audit-events.jsonl`)
    - bounded retrieval for UI/API consumption

- Frontend auth/config/audit UX
  - `frontend/app/components/auth-context.tsx`
  - `frontend/app/login/page.tsx`
  - `frontend/app/register/page.tsx`
  - `frontend/app/settings/page.tsx`
  - `frontend/app/audit/page.tsx`
  - `frontend/app/components/top-nav.tsx` (new links + user session controls)
  - `frontend/app/components/app-shell.tsx` (auth gate for protected routes)
  - `frontend/app/lib/api.ts` (token-aware API client + auth/settings/audit methods)
  - `frontend/app/api/nyxera/[...path]/route.ts` (forwards caller token header)

- Runtime/container operations
  - `Dockerfile.api`
  - `frontend/Dockerfile`
  - `docker-compose.yml` (api + frontend services, proxied via nginx)
  - `config/nginx/nginx.conf` (HTTPS proxy to api/frontend ports)
  - `Makefile` (run-all/docker flow, audit-tail helper, venv-safe run-api)
  - `.gitignore` (key/cert/venv/runtime log artifacts)

## Auditability Design Notes

- Every API request is captured by middleware, including:
  - `actor` (derived from API token subject/role when available)
  - `action` (`http:{METHOD}:{PATH}`)
  - `status` (`ok` or `error`)
  - `timestamp`, `method`, `path`, `ip`
- High-value operational actions are also recorded as domain events:
  - scan single-run
  - scan loop start/stop
  - finding action transitions
- Audit records are persisted as append-only JSON lines to support external SIEM ingestion.

## Security and Compliance Impact

- Added operator identity lifecycle in UI/API.
- Added immutable-style event trail for operator/API actions.
- Improved incident response readiness with retrievable audit ledger endpoint.
- Preserved role-based authorization boundaries for privileged operations.

## Validation Performed

- Local compile path and route wiring reviewed for FastAPI + Next.js integration.
- Compose config verified after service additions.
- Request-token forwarding path validated in Next API proxy route implementation.
