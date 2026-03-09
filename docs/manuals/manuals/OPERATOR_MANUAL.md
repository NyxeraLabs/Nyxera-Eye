# Operator Manual

## 1. Mission

Use Nyxera Eye to identify exposed infrastructure and prioritize risk for authorized defensive action.

## 2. Operating Modes

- Passive mode: default, non-intrusive intelligence collection.
- Authorized scope mode: constrained by approved CIDR/domain scope.

## 3. Standard Workflow

1. Define mission scope and constraints.
2. Collect and normalize OSINT records.
3. Review service fingerprints and clusters.
4. Correlate vulnerability and exploit status.
5. Visualize map/distribution/telemetry.
6. Generate findings and remediation actions.

## 4. TUI Operations

Core keymap:
- `S` -> scan view
- `P` -> pivot view
- `V` -> vulnerabilities view
- `M` -> map view

Search-as-you-type filters live records by text match.

Mongo query input supports:
- `field:value`
- full text (`$text`)

## 5. Investigation Checklist

- Confirm target is not blacklisted.
- Confirm target has not opted out.
- Confirm runtime mode allows requested action.
- Confirm audit logging is active.
- Record confidence and source for each finding.

## 6. Outputs and Evidence

Required per investigation:
- target identity (`device_id`, IP, country, org)
- service list and exposure profile
- vulnerability evidence (`CVE`, severity, exploit flags)
- time-bounded logs and actions

## 7. Escalation Rules

Escalate to security leadership when:
- exposure includes critical infrastructure indicators
- confirmed exploitable high/critical CVEs
- repeated high-risk reappearance events

## 8. Safety Requirements

Never perform:
- brute force
- exploitation
- intrusive probing outside authorized scope
