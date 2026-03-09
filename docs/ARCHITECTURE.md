# Nyxera Eye — Master Architecture Blueprint

## Core Platform Goals

Nyxera Eye is designed as a **continuous network asset intelligence platform**.

The system must support:

* continuous device discovery
* asset intelligence enrichment
* distributed scanning
* vulnerability intelligence
* attack surface visualization

---

# High Level Architecture

```
              +---------------------+
              |     Web UI          |
              +----------+----------+
                         |
                         v
              +---------------------+
              |      API Layer      |
              +----------+----------+
                         |
         +---------------+---------------+
         |                               |
         v                               v
+--------------------+       +---------------------+
| Intelligence Layer |       |   Scanner Engine    |
+---------+----------+       +----------+----------+
          |                             |
          v                             v
+--------------------+       +---------------------+
| Vulnerability DB   |       | Distributed Nodes   |
+--------------------+       +---------------------+

                |
                v

        +-------------------+
        |   Asset Database  |
        +-------------------+
```

---

# Core System Components

## 1. Scanner Engine

Responsible for:

* discovering assets
* probing services
* collecting banners
* sending results to database

Modules:

```
scanner
 ├── discovery
 ├── portscan
 ├── probes
 ├── worker_pool
 ├── rate_limiter
 └── scheduler
```

---

## 2. Intelligence Layer

Responsible for **turning scan data into insights**.

Modules:

```
intel
 ├── fingerprint
 ├── vendor_detection
 ├── firmware_detection
 ├── asset_classification
 ├── vulnerability_mapping
 ├── risk_scoring
 └── relationship_mapper
```

---

## 3. API Layer

Responsible for exposing asset intelligence.

Modules:

```
api
 ├── assets
 ├── services
 ├── vulnerabilities
 ├── telemetry
 └── graph
```

Endpoints example:

```
GET /assets
GET /assets/{ip}
GET /assets/{ip}/services
GET /assets/high-risk
GET /graph/assets
```

---

# Recommended Repository Structure

```
nyxera-eye
│
├── cmd
│   ├── scanner
│   ├── api
│   └── worker
│
├── internal
│
│   ├── scanner
│   │   ├── discovery
│   │   ├── probes
│   │   ├── scheduler
│   │   ├── workers
│   │   └── queue
│   │
│   ├── intel
│   │   ├── fingerprint
│   │   ├── vendor
│   │   ├── firmware
│   │   ├── classification
│   │   └── vulnerabilities
│   │
│   ├── database
│   │   ├── models
│   │   ├── migrations
│   │   └── repository
│   │
│   ├── api
│   │   ├── handlers
│   │   ├── middleware
│   │   └── router
│   │
│   └── telemetry
│
├── web
│   ├── dashboard
│   ├── assets
│   ├── investigation
│   └── graph
│
├── configs
│
├── scripts
│
├── deployments
│
├── .github
│   └── workflows
│
└── docs
```

---

# Scanner Pipeline

The scanning system follows a **multi-stage pipeline**.

```
target_generator
       |
       v
scan_scheduler
       |
       v
task_queue
       |
       v
worker_pool
       |
       v
port_scan
       |
       v
service_probe
       |
       v
fingerprint_engine
       |
       v
database_update
```

---

# Distributed Scanning Model

Scanner nodes connect to a **central coordinator**.

```
scanner-node-1
scanner-node-2
scanner-node-3
       |
       v
   coordinator
       |
       v
  asset database
```

Each node:

* pulls tasks
* runs probes
* submits results

---

# Asset Intelligence Pipeline

Once data is collected it enters the **intelligence pipeline**.

```
scan_result
     |
     v
service_detection
     |
     v
device_fingerprint
     |
     v
vendor_detection
     |
     v
firmware_detection
     |
     v
vulnerability_lookup
     |
     v
risk_scoring
     |
     v
asset_update
```

---

# Database Schema Blueprint

## Assets Table

```
assets
------
id
ip
vendor
device_type
firmware_hint
risk_score
first_seen
last_seen
scan_count
```

---

## Services Table

```
services
--------
id
asset_id
port
protocol
service
banner
version
```

---

## Vulnerabilities Table

```
vulnerabilities
---------------
id
service
version
cve_id
severity
description
```

---

## Scan Nodes Table

```
scan_nodes
----------
id
node_id
status
last_heartbeat
scan_rate
```

---

# Intelligence Graph Model

Asset relationships stored as:

```
asset_relationships
-------------------
source_asset
target_asset
relationship_type
confidence
```

Example relationships:

* shared service
* same infrastructure
* similar fingerprint

---

# UI Architecture

Frontend sections:

```
dashboard
asset_table
asset_detail
scan_status
vulnerability_view
graph_view
```

---

# UI Component Structure

```
web
 ├── components
 │   ├── asset_table
 │   ├── risk_badge
 │   ├── service_list
 │   ├── scan_status
 │   └── graph_visualizer
 │
 ├── pages
 │   ├── dashboard
 │   ├── assets
 │   └── investigation
```

---

# Data Flow

```
scanner
   |
   v
database
   |
   v
intelligence engine
   |
   v
api
   |
   v
web ui
```

---

# CI/CD Architecture

GitHub workflows:

```
.github/workflows

ci.yml
license-check.yml
test.yml
release.yml
```

CI pipeline:

```
push
 |
 v
lint
 |
 v
license check
 |
 v
tests
 |
 v
build
 |
 v
release tag
```

---

# GitFlow Model

Branches:

```
main
qa
dev
feat/sprint-X
```

Workflow:

```
feat/sprint-22
      |
      v
     dev
      |
      v
      qa
      |
      v
     main
```

---

# Development Rules for LLMs

LLMs must follow strict architecture rules.

Never:

* move modules
* change database schema without migration
* introduce new frameworks
* bypass scanner pipeline

Always:

* follow roadmap sprint tasks
* add license headers
* respect folder structure
* produce one commit per task

---

# System Capabilities After Full Roadmap

Nyxera Eye becomes capable of:

### Discovery

* continuous scanning
* distributed scan nodes
* large-scale coverage

### Intelligence

* vendor detection
* firmware hints
* device classification
* vulnerability mapping

### Security Analysis

* risk scoring
* configuration risk detection
* attack surface mapping

### Visualization

* asset dashboards
* investigation tools
* infrastructure graphs

---
