<!--
Copyright (c) 2026 NyxeraLabs
Author: Jose Maria Micoli
Licensed under BSL 1.1
Change Date: 2033-02-17 -> Apache-2.0
-->

# API Manual

## Authentication

Protected endpoints require:

```text
X-API-Token: <token>
```

Role hierarchy:

- `viewer`
- `analyst`
- `operator`
- `admin`

## Core Runtime Endpoints

### Public

- `GET /health`
- `GET /frontend/ops-feed`
- `POST /frontend/scan`
- `POST /frontend/scan/start`
- `POST /frontend/scan/stop`
- `GET /frontend/scan/status`
- `GET /frontend/devices`
- `GET /frontend/devices/{device_id}`
- `GET /frontend/findings`
- `GET /frontend/findings/{finding_id}`
- `POST /frontend/findings/{finding_id}/action`
- `GET /frontend/findings/{finding_id}/export`

### Analyst+

- `GET /frontend/settings`
- `GET /search/opensearch`
- `POST /ui/target-card`

### Operator+

- `POST /command-center/map`
- `POST /command-center/vulnerability-distribution`

### Admin

- `PUT /frontend/settings`
- `GET /audit/events`
- `GET /command-center/telemetry`
- `GET /observability/prometheus`

## Useful Query Parameters

### Device registry

`GET /frontend/devices`

- `q`
- `severity`
- `country`
- `vendor`
- `limit`
- `offset`

### Findings registry

`GET /frontend/findings`

- `q`
- `severity`
- `status`
- `device_id`
- `limit`
- `offset`

## Behavior Notes

- scan results accumulate into a stable inventory
- findings remain linked to stable device IDs
- finding actions update status and action history
- device detail returns linked finding and recent events

## Error Behavior

- `401` missing or invalid token
- `403` role below endpoint requirement
- `404` unknown device or finding
- `429` rate limit exceeded
