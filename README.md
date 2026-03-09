# Nyxera Eye

**Nyxera Eye** is an **IoT and ICS Attack Surface Intelligence Platform** designed for **security research and authorized red-team operations**.

The platform discovers, fingerprints, and analyzes exposed internet infrastructure to help security teams understand **real-world exposure risks**.

Nyxera Eye integrates global OSINT intelligence, device fingerprinting, vulnerability intelligence, and visualization into a single operational platform.

---

# Core Capabilities

• Global exposure discovery
• IoT and ICS fingerprinting
• Infrastructure clustering and tracking
• Vulnerability intelligence correlation
• Real-time exposure monitoring
• Attack surface visualization
• Threat-informed adversary emulation (authorized mode)

---

# Operating Modes

Nyxera Eye includes two safety modes.

### Passive Intelligence Mode (default)

Only non-intrusive OSINT collection:

* Shodan
* Censys
* ZoomEye
* Public banner data
* TLS fingerprinting
* Metadata correlation

No authentication attempts or exploitation occurs.

### Authorized Scope Mode

Used only during **approved security assessments**.

Allows deeper enumeration inside a **defined CIDR or domain scope**.

All operator activity is logged.

---

# System Architecture

Nyxera Eye uses a distributed architecture designed to scale to millions of assets.

Data pipeline:

Data Sources
→ Collectors
→ Redis Streams
→ Processing Workers
→ Device Intelligence Schema
→ MongoDB + OpenSearch
→ FastAPI API Layer
→ Operator Interfaces (TUI + Web)

Binary assets such as snapshots are stored in **MinIO S3**.

---

# Technology Stack

Backend

Python 3.12
FastAPI
Redis Streams
MongoDB
OpenSearch

Infrastructure

Docker
MinIO S3
Prometheus
Grafana

Interfaces

Textual (Terminal UI)
React (Web Dashboard)

---

# Repository Structure

nyxera-eye/

core/
collectors/
fingerprinting/
probing/
vulnintel/
ai/
api/
tui/
frontend/
automation/
storage/
tests/

docs/
docker/
infra/
config/

---

# Legal and Ethical Use

Nyxera Eye is designed **strictly for security research and authorized security testing**.

Prohibited uses include:

• Unauthorized access
• Privacy violations
• Illegal surveillance
• Exploitation of systems without permission

The platform includes:

• Passive Intelligence Mode
• Authorized Scope Mode
• Audit logging
• Opt-out registry
• Responsible disclosure policy

---

# Responsible Disclosure

If Nyxera Eye identifies exposed infrastructure that may present security risks, findings should be reported responsibly following industry disclosure standards.

---

# License

Business Source License 1.1 (BSL)

Additional Use Grant allows use for:

• security research
• defensive security teams
• authorized red-team engagements

Commercial use restrictions may apply.

---

# Status

Early development (R&D stage).

Nyxera Eye is being built by **Nyxera Labs**.
