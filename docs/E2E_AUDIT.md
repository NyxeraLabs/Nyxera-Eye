# E2E Audit Report (Sprint 17)

Date: 2026-03-09
Target: `scripts/e2e_full_validation.py`

## Scope

Audit of the current full-roadmap E2E runner for realism, coverage integrity, and regression risk.

## Findings (Highest Severity First)

1. `HIGH` - Queue integration mutates global module state without restoration
   - Reference: `scripts/e2e_full_validation.py:146-148`
   - Issue: `redis_queue_module.RedisSettings` and `redis_queue_module.create_pool` are monkey-patched globally and never restored.
   - Risk: Subsequent tests/processes in the same Python runtime can run against fake queue behavior unintentionally.
   - Fix: Save originals, patch in `try/finally`, and restore at the end of `_phase2_collectors_and_queue`.

2. `HIGH` - No real API endpoint execution in E2E path
   - Reference: `scripts/e2e_full_validation.py:204-215`, `315-317`
   - Issue: Script validates API builder/helper functions, but does not exercise FastAPI routes, auth dependencies, or HTTP status behaviors.
   - Risk: Route wiring, dependency injection, RBAC enforcement, and rate-limiting regressions can pass unnoticed.
   - Fix: Add HTTP-level E2E segment using `TestClient` (or live app run) and validate `401/403/429/200` paths.

3. `MEDIUM` - External integrations are simulated, not live
   - Reference: `scripts/e2e_full_validation.py:40-90`, `130-149`
   - Issue: OSINT providers and Redis are mocked/deterministic.
   - Risk: Contract drift with provider payloads and queue runtime failures are not detected.
   - Fix: Add optional `--live` mode using environment-gated credentials and real Redis container.

4. `MEDIUM` - Assertions are mostly existence/shape checks, not behavioral invariants
   - Reference: multiple (example `399`, `368`)
   - Issue: Several checks only assert presence or positive values (`> 0`, substring contains).
   - Risk: Logic regressions with still-truthy outputs may pass.
   - Fix: Strengthen assertions to exact expected values for critical paths (risk score, change events, metrics lines).

5. `LOW` - Script duplicates mock payloads already present in tests
   - Reference: `scripts/e2e_full_validation.py:40-90`
   - Issue: Payload duplication increases maintenance burden.
   - Risk: Drift between unit-test fixtures and E2E fixtures.
   - Fix: Centralize fixtures in a shared, importable non-test package.

## Passed Checks

- End-to-end deterministic run passes locally:
  - `PYTHONPATH=src python scripts/e2e_full_validation.py`
- Compose configuration validation passes:
  - `docker compose config -q`

## Audit Verdict

Current E2E provides good cross-module smoke coverage but is not yet a fully realistic production E2E gate.

Status: `CONDITIONAL PASS` for development smoke testing, `NOT SUFFICIENT` as the only release gate.

## Required Hardening Before Release Gate Use

1. Restore monkey-patched queue globals in `try/finally`.
2. Add HTTP-level FastAPI E2E with token/RBAC/rate-limit assertions.
3. Add optional live-integration mode for OSINT + Redis (env-gated).
4. Tighten critical assertions from shape checks to deterministic value checks.
