<!--
Copyright (c) 2026 NyxeraLabs
Author: José María Micoli
Licensed under BSL 1.1
Change Date: 2033-03-09 → Apache-2.0
-->

# Compliance Policy

Nyxera Eye is designed for lawful security research and authorized defensive operations.

## Allowed Use Cases

- Passive OSINT ingestion from public sources.
- Asset exposure analysis for defensive risk reduction.
- Authorized red team operations with written authorization.
- Internal lab and simulation environments.

## Prohibited Use Cases

- Unauthorized access attempts.
- Credential brute force or password spraying.
- Exploit delivery against non-authorized targets.
- Intrusive scanning outside explicit approved scope.

## Scope Requirements

Authorized Scope Mode requires all of the following:

- Documented customer authorization.
- Explicit CIDR/domain scope definition.
- Audit logs enabled and retained.

## Enforcement Model

- Default runtime is Passive Mode.
- Authorized Scope Mode is opt-in and scope-gated.
- Blacklist and opt-out checks are enforced before active tasks.
