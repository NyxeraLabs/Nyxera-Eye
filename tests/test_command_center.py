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

from nyxera_eye.api.command_center import (
    build_global_exposure_map_points,
    build_mining_telemetry,
    build_vulnerability_distribution,
)


def test_global_exposure_map_points() -> None:
    devices = [
        {
            "ip": "203.0.113.10",
            "latitude": -31.4,
            "longitude": -64.2,
            "country": "AR",
            "exposure_score": 8.5,
        }
    ]

    points = build_global_exposure_map_points(devices)
    assert points[0]["ip"] == "203.0.113.10"


def test_vulnerability_distribution() -> None:
    devices = [
        {"vulnerabilities": [{"severity": "high"}, {"severity": "medium"}]},
        {"vulnerabilities": [{"severity": "high"}]},
    ]

    dist = build_vulnerability_distribution(devices)
    assert dist["high"] == 2
    assert dist["medium"] == 1


def test_mining_telemetry_payload() -> None:
    telemetry = build_mining_telemetry(
        scan_throughput=123.456,
        probe_latency_ms=87.654,
        active_discoveries=42,
    )

    assert telemetry["scan_throughput"] == 123.46
    assert telemetry["probe_latency_ms"] == 87.65
    assert telemetry["active_discoveries"] == 42
