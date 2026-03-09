# E2E Validation Guide

## Purpose

Validate implemented roadmap capabilities through one deterministic end-to-end flow.

## Primary Command

```bash
cd /home/xoce/Workspace/Nyxera-Eye
PYTHONPATH=src python scripts/e2e_full_validation.py
```

## Expected Output

```text
E2E full roadmap validation passed (local deterministic path).
```

## What It Covers

- Compliance mode checks
- OSINT collector normalization
- Queue enqueue path (mocked adapter)
- Processing pipeline
- Schema migration and validation
- Fingerprinting and clustering
- Protocol enrichment
- Vulnerability intelligence and risk scoring
- TUI functions
- API query/visualization builders
- Media handling
- Adversary mapping and deception checks
- Vision pipeline
- Change detection
- Security controls
- Observability metrics and tracing

## Companion Documents

- [QA Runbook](../../RUNBOOK.md)
- [E2E Audit Report](../../E2E_AUDIT.md)
