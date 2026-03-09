# API Manual

## 1. Authentication

Protected endpoints require header:

```text
X-API-Token: <token>
```

Role hierarchy:
- `viewer`
- `analyst`
- `operator`
- `admin`

## 2. Endpoints

### Public

- `GET /health`
  - response: `{"status":"ok"}`

### Analyst+

- `GET /search/opensearch`
  - query params:
    - `q`
    - `asn`
    - `vendor`
    - `vulnerability`
    - `country`
    - `exposure_score_min`

- `POST /ui/target-card`
  - body: raw device document
  - response: summarized target card

### Operator+

- `POST /command-center/map`
  - body: device list
  - response: map points

- `POST /command-center/vulnerability-distribution`
  - body: device list
  - response: severity distribution

### Admin

- `GET /command-center/telemetry`
  - params:
    - `scan_throughput`
    - `probe_latency_ms`
    - `active_discoveries`

- `GET /observability/prometheus`
  - params:
    - `queue_depth`
    - `mining_throughput`
    - `probe_success_rate`
    - `gpu_utilization`
    - `storage_growth_gb`

## 3. Error Behavior

- `401`: missing or invalid token
- `403`: role does not satisfy endpoint minimum
- `429`: per-subject rate limit exceeded

## 4. Manual API Smoke

```bash
curl -s http://127.0.0.1:8000/health
curl -i -s "http://127.0.0.1:8000/search/opensearch?q=camera"
curl -i -s -H "X-API-Token: <TOKEN>" "http://127.0.0.1:8000/search/opensearch?q=camera"
```
