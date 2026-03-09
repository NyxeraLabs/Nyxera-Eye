# Security and Compliance Manual

## 1. Security Controls

Implemented controls:
- RBAC authorization
- API token issuance/verification/revocation
- encrypted secret payload support
- request rate limiting
- operator audit logging

## 2. Compliance Controls

Implemented controls:
- passive intelligence mode default
- authorized scope policy by CIDR allowlist
- target blacklist
- asset owner opt-out registry
- legal usage banner

## 3. Operational Policy

Before any action:
1. confirm legal authorization
2. confirm runtime mode
3. confirm target not blacklisted
4. confirm target not opted out
5. ensure logging enabled

## 4. Token and Access Hygiene

- keep bootstrap/admin tokens out of source control
- rotate tokens periodically
- revoke tokens for inactive operators
- use least-privilege role assignment

## 5. Incident Handling

If unauthorized action is suspected:
1. freeze related token(s)
2. preserve audit logs
3. isolate impacted workflows
4. notify security lead
5. initiate disclosure process if required

## 6. Governing Docs

- [Compliance](../../COMPLIANCE.md)
- [Ethics](../../ETHICS.md)
- [Security Disclosure](../../SECURITY_DISCLOSURE.md)
