# Copyright (c) 2026 NyxeraLabs
# Author: José María Micoli
# Licensed under BSL 1.1
# Change Date: 2033-02-17 → Apache-2.0
#
# You may:
# ✔ Study
# ✔ Modify
# ✔ Use for internal security testing
#
# You may NOT:
# ✘ Offer as a commercial service
# ✘ Sell derived competing products

from collections import Counter
from datetime import UTC, datetime


def build_global_exposure_map_points(devices: list[dict]) -> list[dict[str, float | str | None]]:
    points: list[dict[str, float | str | None]] = []
    for device in devices:
        points.append(
            {
                "ip": device.get("ip"),
                "latitude": device.get("latitude"),
                "longitude": device.get("longitude"),
                "country": device.get("country"),
                "exposure_score": device.get("exposure_score"),
            }
        )
    return points


def build_vulnerability_distribution(devices: list[dict]) -> dict[str, int]:
    severity_counter: Counter[str] = Counter()

    for device in devices:
        for vuln in device.get("vulnerabilities", []):
            severity = str(vuln.get("severity", "unknown")).lower()
            severity_counter[severity] += 1

    return dict(sorted(severity_counter.items()))


def build_mining_telemetry(scan_throughput: float, probe_latency_ms: float, active_discoveries: int) -> dict[str, float | int]:
    return {
        "scan_throughput": round(scan_throughput, 2),
        "probe_latency_ms": round(probe_latency_ms, 2),
        "active_discoveries": active_discoveries,
    }


def build_ops_feed() -> dict:
    now = datetime.now(UTC).isoformat()
    devices = [
        {
            "device_id": "dev-1",
            "name": "Acme Cam-7",
            "ip": "198.51.100.10",
            "country": "AR",
            "latitude": -31.4,
            "longitude": -64.2,
            "severity": "high",
        },
        {
            "device_id": "dev-2",
            "name": "Edge RTSP Node",
            "ip": "203.0.113.44",
            "country": "US",
            "latitude": 37.77,
            "longitude": -122.41,
            "severity": "critical",
        },
        {
            "device_id": "dev-3",
            "name": "Factory PLC",
            "ip": "192.0.2.77",
            "country": "DE",
            "latitude": 52.52,
            "longitude": 13.41,
            "severity": "medium",
        },
    ]
    events = [
        {
            "id": "evt-1",
            "title": "Secure -> Vulnerable",
            "device_id": "dev-2",
            "lat": 37.77,
            "lon": -122.41,
            "severity": "critical",
            "type": "state_change",
            "timestamp": now,
        },
        {
            "id": "evt-2",
            "title": "Deception Signal",
            "device_id": "dev-3",
            "lat": 52.52,
            "lon": 13.41,
            "severity": "medium",
            "type": "deception",
            "timestamp": now,
        },
    ]
    findings = [
        {
            "id": "f-1",
            "title": "CVE-2026-1000 exploit exposure",
            "description": "Device exposes vulnerable firmware with known exploit signals.",
            "severity": "critical",
            "device_id": "dev-2",
        },
        {
            "id": "f-2",
            "title": "Unsafe protocol surface",
            "description": "Modbus service reachable with elevated exposure score.",
            "severity": "high",
            "device_id": "dev-3",
        },
    ]
    metrics = {
        "queue_depth": 12,
        "mining_throughput": 245.5,
        "probe_success_rate": 97.2,
        "storage_growth_gb": 1.24,
    }
    return {
        "generated_at": now,
        "devices": devices,
        "events": events,
        "findings": findings,
        "metrics": metrics,
    }
