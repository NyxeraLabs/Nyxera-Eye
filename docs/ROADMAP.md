<!--
Copyright (c) 2026 NyxeraLabs
Author: José María Micoli
Licensed under BSL 1.1
Change Date: 2033-03-09 → Apache-2.0

You may:
✔ Study
✔ Modify
✔ Use for internal security testing

You may NOT:
✘ Offer as a commercial service
✘ Sell derived competing products
-->

# Nyxera Eye

**IoT & ICS Attack Surface Intelligence Platform for Security Research and Authorized Red Team Operations**

License: **Business Source License 1.1 (BSL)**
Lead R&D: **Nyxera Labs**

Mission:

> Discover, fingerprint, and monitor exposed IoT and ICS infrastructure worldwide to help defenders and authorized red teams understand exposure risk.

Primary operating modes:

1. **Passive Intelligence Mode (default)**
2. **Authorized Scope Mode (for approved red-team engagements)**

---

# System Architecture

High-level architecture:

```
External Intelligence Sources
        │
        ▼
Data Collectors
        │
        ▼
Redis Streams / Task Queue
        │
        ▼
Processing Workers
(Fingerprinting, Parsing, Enrichment)
        │
        ▼
Normalized Device Intelligence Schema
        │
        ├──────── MongoDB (Metadata)
        │
        ├──────── OpenSearch (Search/Analytics)
        │
        └──────── MinIO (Snapshots / Binary Assets)
                     │
                     ▼
                FastAPI Backend
                     │
       ┌─────────────┴─────────────┐
       ▼                           ▼
   Operator TUI             Web Command Center
```

Observability stack:

```
Prometheus
Grafana
OpenTelemetry
```

Queue layer:

```
Redis Streams (initial)
Kafka (future scaling)
```

---

# Operating Safety Model

### Passive Intelligence Mode (Default)

Allowed:

* ingest OSINT data (Shodan, Censys, ZoomEye)
* banner parsing
* TLS fingerprinting
* metadata correlation

Not allowed:

* authentication attempts
* brute force
* exploit execution

---

### Authorized Scope Mode

Enabled only when:

* user defines approved target scope
* operator logs are enabled
* written authorization exists

Allows:

* controlled probing
* protocol interrogation
* deeper enumeration

---

# Phase 0 — Legal Compliance & Ethical Framework

Purpose: ensure platform operates within acceptable legal and ethical boundaries.

### Sprint 0: Compliance Layer

Tasks:

```
[x] commit: Create COMPLIANCE.md defining allowed use cases
[x] commit: Create ETHICS.md research ethics policy
[x] commit: Create SECURITY_DISCLOSURE.md for responsible disclosure
[x] commit: Implement Passive Mode (default runtime mode)
[x] commit: Implement Authorized Scope Mode with CIDR allowlist
[x] commit: Implement Target Blacklist system
[x] commit: Implement Opt-Out registry for asset owners
[x] commit: Add audit logging subsystem
[x] commit: Add legal banner to UI
```

Policy requirements:

* no exploitation
* no credential brute forcing
* no intrusive scanning outside authorized scope

---

# Phase 1 — Infrastructure Foundation

### Sprint 1: Core Environment

Tasks:

```
[x] commit: Initialize Git repository
[x] commit: Setup Python 3.12 Poetry environment
[x] commit: Add LICENSE.md (BSL 1.1)
[x] commit: Create ROADMAP.md
```

Infrastructure deployment:

```
[x] commit: docker-compose.yml
        MongoDB
        OpenSearch
        Redis
        MinIO
        Prometheus
        Grafana
```

Storage configuration:

```
[x] commit: Configure MongoDB WiredTiger compression
[x] commit: Configure MinIO bucket structure
```

QA:

```
Verify persistent storage
Verify 20GB minimum disk
```

---

# Phase 2 — Intelligence Collection Layer

### Sprint 2: OSINT Harvester Engine

Data sources:

* Shodan
* Censys
* ZoomEye

Tasks:

```
[x] commit: Async Shodan collector
[x] commit: Async Censys collector
[x] commit: Async ZoomEye collector
```

Queue integration:

```
[x] commit: Redis task queue (Arq)
```

Mining management:

```
[x] commit: Dork Manager
       search categories
       rate limiting
       query rotation
```

Testing:

```
[x] commit: Mock API responses
```

Documentation:

```
INFRA.md
.env.example
```

---

# Phase 3 — Data Processing Pipeline

### Sprint 3: Worker Framework

Purpose: decouple ingestion from processing.

Workers:

```
[x] commit: Banner parsing worker
[x] commit: Service detection worker
[x] commit: Device enrichment worker
```

Pipeline:

```
Collector
 → Redis queue
 → Processing worker
 → Normalized schema
 → Database
```

---

# Phase 4 — Device Intelligence Schema

### Sprint 4: Canonical Data Model

Example normalized device record:

```
device_id
ip
hostname
asn
organization
country
latitude
longitude

services:
  port
  protocol
  banner

fingerprints:
  favicon_hash
  ja3
  jarm

iot_metadata:
  vendor
  model
  firmware

vulnerabilities:
  cve
  severity
  exploit_available

media:
  snapshot
```

Tasks:

```
[x] commit: Implement schema validation
[x] commit: Implement schema migration utilities
```

---

# Phase 5 — Fingerprinting & Identity Clustering

### Sprint 5

Capabilities:

```
[x] commit: MurmurHash3 favicon fingerprint miner
[x] commit: JA3 TLS fingerprinting
[x] commit: JARM infrastructure fingerprinting
```

Clustering logic:

```
[x] commit: SSL certificate serial correlation
```

Purpose:

Track infrastructure even when **IP addresses change**.

UI feature:

```
Cluster View
```

---

# Phase 6 — IoT Protocol Enrichment

### Sprint 6

Supported protocols:

```
ONVIF discovery
RTSP metadata probe
SNMP enumeration (safe mode only)
```

Tasks:

```
[x] commit: ONVIF discovery module
[x] commit: RTSP metadata probe
[x] commit: SNMP MIB metadata extraction
```

Geolocation enrichment:

```
MaxMind
IPInfo fallback
```

QA:

```
timeout handling for cellular links
```

---

# Phase 7 — Vulnerability Intelligence

### Sprint 7

Data sources:

```
NVD
CISA KEV
ExploitDB
EPSS
```

Tasks:

```
[x] commit: CVE mirror database
[x] commit: vendor firmware mapping
[x] commit: exploit availability detection
```

Risk score:

```
Risk Score =
CVSS
+ EPSS probability
+ exploit availability
+ exposure level
```

---

# Phase 8 — Operator Terminal UI

### Sprint 8: Nyxera-Speed TUI

Framework:

```
Textual
```

Features:

```
[x] commit: keyboard navigation
[x] commit: search-as-you-type
[x] commit: MongoDB query interface
```

Shortcuts:

```
S → scan
P → pivot
V → vulnerabilities
M → map
```

Color coding:

```
Critical
Open
Secure
```

---

# Phase 9 — Web Intelligence Hub

### Sprint 9

Backend:

```
FastAPI
```

Features:

```
[x] commit: OpenSearch query endpoints
[x] commit: advanced filtering
```

Filter parameters:

```
ASN
vendor
vulnerability
country
exposure score
```

UI element:

```
Target Cards
```

---

# Phase 10 — Global Command Center

### Sprint 10

Frontend stack:

```
React
Mapbox / Leaflet
```

Features:

```
[x] commit: global exposure map
[x] commit: vulnerability distribution charts
[x] commit: real-time mining telemetry
```

Telemetry overlays:

```
scan throughput
probe latency
active discoveries
```

---

# Phase 11 — Media Intelligence

### Sprint 11

Focus on **non-intrusive capture**.

Tasks:

```
[x] commit: snapshot capture system
[x] commit: thumbnail storage in MinIO
```

Optional (Authorized Scope Mode only):

```
RTSP proxy gateway
```

---

# Phase 12 — Threat-Informed Adversary Emulation

### Sprint 12

Features:

```
[x] commit: MITRE ATT&CK mapping for IoT/ICS
[x] commit: deception detection engine
```

Detection logic:

```
TCP jitter
banner inconsistencies
timing anomalies
```

Payload tooling (authorized environments only):

```
cross-compiled test payload generator
```

Architectures:

```
MIPS
ARM
x86
```

---

# Phase 13 — Vision Intelligence Workers

### Sprint 13

Pipeline:

```
Snapshot
 → AI queue
 → Vision worker
 → Metadata tags
```

Model:

```
YOLO
```

Tag categories:

```
server racks
keypads
industrial panels
faces (optional / privacy-aware)
```

Validation:

```
test against 500+ images
```

Tasks:

```
[x] commit: Vision pipeline (Snapshot -> AI queue -> Vision worker -> Metadata tags)
[x] commit: YOLO adapter tag normalization
[x] commit: Vision dataset validation threshold (500+ images)
```

---

# Phase 14 — Change Detection Engine

### Sprint 14

Purpose: detect infrastructure state changes.

Examples:

```
Secure → Vulnerable
Firmware change
Device disappears
Device reappears
```

Tasks:

```
[x] commit: Diff Engine
```

Alerts:

```
Discord
Slack
Webhook
```

Exports:

```
PDF
JSON
CSV
```

---

# Phase 15 — Security Hardening

### Sprint 15

Platform security:

```
[x] commit: RBAC authentication
[x] commit: API token system
[x] commit: encrypted secrets
[x] commit: request rate limiting
```

Audit system:

```
operator action logs
```

---

# Phase 16 — Observability

### Sprint 16

Monitoring stack:

```
Prometheus
Grafana
OpenTelemetry
```

Metrics:

```
queue depth
mining throughput
probe success rate
GPU utilization
storage growth
```

Tasks:

```
[x] commit: Prometheus metrics exporter for core platform KPIs
[x] commit: OpenTelemetry-style span context utility
```

---

# Phase 17 — Final Release

### Sprint 17

Full validation:

```
OSINT query
→ ingestion
→ fingerprinting
→ vulnerability mapping
→ visualization
→ operator investigation
```

Documentation:

```
deployment guide
operator manual
adversary emulation manual
```

Release:

```
Nyxera Eye v1.0
```

---

# Phase 18 — Frontend UX Foundation

### Sprint 18

Frontend stack:

```
Next.js
Tailwind CSS
```

Tasks:

```
[x] commit: Initialize Next.js frontend structure in `frontend/`
[x] commit: Implement shared top navigation across pages
[x] commit: Implement global footer finding action bar
[x] commit: Implement multi-page routes (dashboard, map, events, findings)
```

UX requirements:

```
mobile responsive layout
clear navigation hierarchy
finding context visible at all times
```

---

# Phase 19 — Geospatial Intelligence UX

### Sprint 19

Map requirements:

```
global world map view
device location overlays
event location overlays
```

Tasks:

```
[x] commit: Implement world map component with geolocation plotting
[x] commit: Render device and event markers with legend
[x] commit: Add events page and finding selection integration
[x] commit: Add findings page with footer action workflow
```

---

# Phase 20 — Interactive Map Runtime

### Sprint 20

Map runtime:

```
Leaflet
OpenStreetMap tiles
```

Tasks:

```
[x] commit: Integrate Leaflet + react-leaflet frontend map runtime
[x] commit: Replace static map placeholder with interactive map component
[x] commit: Add map overlay toggles for devices and events
[x] commit: Add popup details for devices/events markers
```

---

# Phase 21 — Infrastructure Security Hardening

### Sprint 21

Ingress and exposure model:

```
Nginx reverse proxy
HTTPS-only web ingress
non-default externally exposed ports
internal-only backend services
```

Tasks:

```
[x] commit: Replace direct service exposure with Nginx TLS ingress layer
[x] commit: Enforce HTTPS-only access to observability/storage/search web surfaces
[x] commit: Move backend datastore services to internal-only docker network
[x] commit: Apply container hardening defaults (no-new-privileges, readonly proxy fs)
```

Security objective:

```
reduce attack surface
minimize direct service exposure
centralize transport security controls
```

---

# Storage Economics

For **100,000 devices**

```
MongoDB metadata: ~200MB
OpenSearch index: ~200MB
Snapshots: ~15GB
AI tagging metadata: ~100MB
```

Total:

```
≈16GB
```

---

# Recommended Repository Structure

```
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
```

---

# Legal Risk Assessment

With the safeguards implemented:

Risk level: **LOW**

Comparable platforms:

* Shodan
* Censys
* GreyNoise

Critical safeguards already included in roadmap:

* passive intelligence mode
* authorized scope mode
* opt-out registry
* responsible disclosure policy
* audit logging
* rate limiting

---
