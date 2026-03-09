# Full User Guide

## 1. Overview

Nyxera Eye is an IoT/ICS attack surface intelligence platform for authorized security research and defensive operations.

Main capabilities:
- OSINT ingestion from Shodan/Censys/ZoomEye
- Device normalization and enrichment
- Fingerprinting (favicon/JA3/JARM)
- Vulnerability intelligence and risk scoring
- Operator interfaces (TUI + web/API)
- Media and vision tagging
- Change detection
- Security hardening controls
- Observability telemetry

## 2. Safety Model

Nyxera Eye supports:
- Passive mode (default): non-intrusive intelligence only
- Authorized scope mode: constrained operations on approved scope

Read and follow:
- [Compliance Policy](../../COMPLIANCE.md)
- [Ethics Policy](../../ETHICS.md)
- [Security Disclosure](../../SECURITY_DISCLOSURE.md)

## 3. System Workflow

1. Collect OSINT data
2. Push work to queue
3. Process banners/services/risk profile
4. Normalize records into canonical schema
5. Enrich with fingerprints and vuln intel
6. Expose data for operator investigation (TUI/API)
7. Monitor changes and telemetry

## 4. Installation and Startup

Use:
- [Installation Guide](../guides/INSTALLATION.md)
- [Getting Started](../guides/GETTING_STARTED.md)

## 5. Core Operations

### 5.1 Run deterministic full E2E validation

```bash
PYTHONPATH=src python scripts/e2e_full_validation.py
```

### 5.2 Run test suite

```bash
poetry run pytest -q
```

### 5.3 Validate infrastructure compose

```bash
docker compose config -q
```

## 6. API Usage

Protected endpoints require `X-API-Token`.

Examples:

```bash
curl -s http://127.0.0.1:8000/health
curl -s -H "X-API-Token: <TOKEN>" "http://127.0.0.1:8000/search/opensearch?q=camera"
curl -s -H "X-API-Token: <TOKEN>" "http://127.0.0.1:8000/observability/prometheus"
```

For details, see [API Manual](API_MANUAL.md).

## 7. Operator Usage

TUI shortcut views:
- `S` scan
- `P` pivot
- `V` vulnerabilities
- `M` map

For full workflows, see [Operator Manual](OPERATOR_MANUAL.md).

## 8. QA and Release Validation

Use:
- [E2E Validation Guide](../guides/E2E_VALIDATION.md)
- [QA Runbook](../../RUNBOOK.md)
- [E2E Audit Report](../../E2E_AUDIT.md)

## 9. Security and Compliance Operations

See [Security and Compliance Manual](SECURITY_COMPLIANCE_MANUAL.md).

## 10. Troubleshooting

See [Troubleshooting Manual](TROUBLESHOOTING.md).
