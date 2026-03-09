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
