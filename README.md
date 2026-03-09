<!--
Copyright (c) 2026 NyxeraLabs
Author: Jose Maria Micoli
Licensed under BSL 1.1
Change Date: 2033-03-09 -> Apache-2.0
-->

# Nyxera Eye

Nyxera Eye is an IoT and ICS attack surface intelligence platform for authorized security research and defensive operations.

It combines OSINT ingestion, service fingerprinting, vulnerability intelligence, and operator-facing investigation surfaces into one workflow-oriented product.

## Product Highlights

- Multi-source OSINT ingestion (Shodan, Censys, ZoomEye)
- Worker-based processing and canonical schema normalization
- Fingerprinting stack (favicon MMH3, JA3, JARM)
- Vulnerability intelligence (CVE mirror, firmware mapping, exploit detection, risk scoring)
- Operator interfaces (TUI workflows and API command center primitives)
- Media and vision metadata pipeline
- Change detection across infrastructure snapshots
- Security controls (RBAC, API tokens, encrypted secrets, rate limiting)
- Observability metrics and tracing utilities

## Operating Model

Nyxera Eye is built around two safety modes:

- Passive Intelligence Mode (default): non-intrusive intelligence collection only
- Authorized Scope Mode: deeper actions allowed only for explicitly approved scope

Compliance controls include blacklist support, opt-out registry, audit logging, and legal disclosure artifacts.

## Quick Start

```bash
cd /home/xoce/Workspace/Nyxera-Eye
make install
make qa
```

Expected E2E success line:

```text
E2E full roadmap validation passed (local deterministic path).
```

## Makefile Workflow

Core commands:

```bash
make help
make install
make compile
make test
make infra-check
make e2e
make qa
make up
make down
make run-api
```

## Documentation

- Manuals index: [docs/manuals/INDEX.md](docs/manuals/INDEX.md)
- QA runbook: [docs/RUNBOOK.md](docs/RUNBOOK.md)
- E2E audit: [docs/E2E_AUDIT.md](docs/E2E_AUDIT.md)
- Development sprint logs: [docs/dev-logs/INDEX.md](docs/dev-logs/INDEX.md)
- Roadmap: [docs/ROADMAP.md](docs/ROADMAP.md)
- Security policy: [SECURITY.md](SECURITY.md)
- Disclaimer: [DISCLAIMER.md](DISCLAIMER.md)

## Architecture Snapshot

```text
OSINT Sources
-> Collectors
-> Queue
-> Processing Workers
-> Canonical Device Schema
-> Storage (MongoDB/OpenSearch/MinIO)
-> API + TUI/Web Investigation Surfaces
```

## Deployment Notes

Infrastructure configuration is defined in `docker-compose.yml`.

Validate deployment config before startup:

```bash
make infra-check
```

Start local stack:

```bash
make up
```

## Disclaimer

Nyxera Eye is for authorized security testing and defensive research only.

Do not use this project for unauthorized access, disruption, or exploitation. You are responsible for legal compliance in your jurisdiction and target environment.

This software is provided "as is" without warranties; maintainers and contributors are not liable for misuse.

Full text: [DISCLAIMER.md](DISCLAIMER.md)

## License

Business Source License 1.1 (BSL). See [LICENSE](LICENSE).

## Copyright

Copyright (c) 2026 NyxeraLabs. All rights reserved.
