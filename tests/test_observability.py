# Copyright (c) 2026 NyxeraLabs
# Author: Jose Maria Micoli
# Licensed under BSL 1.1
# Change Date: 2033-02-17 -> Apache-2.0
#
# You may:
# - Study
# - Modify
# - Use for internal security testing
#
# You may NOT:
# - Offer as a commercial service
# - Sell derived competing products

import time

import pytest

from nyxera_eye.observability import PlatformMetrics, export_prometheus, start_span


def test_platform_metrics_validation() -> None:
    with pytest.raises(ValueError, match="queue_depth"):
        PlatformMetrics(
            queue_depth=-1,
            mining_throughput=1.0,
            probe_success_rate=90.0,
            gpu_utilization=10.0,
            storage_growth_gb=0.1,
        )


def test_prometheus_export_contains_all_phase16_metrics() -> None:
    metrics = PlatformMetrics(
        queue_depth=12,
        mining_throughput=245.55,
        probe_success_rate=97.2,
        gpu_utilization=63.1,
        storage_growth_gb=1.234,
    )

    text = export_prometheus(metrics)

    assert "nyxera_queue_depth 12" in text
    assert "nyxera_mining_throughput 245.55" in text
    assert "nyxera_probe_success_rate 97.20" in text
    assert "nyxera_gpu_utilization 63.10" in text
    assert "nyxera_storage_growth_gb 1.234" in text


def test_open_telemetry_style_span_context_duration() -> None:
    with start_span("test-span") as span:
        time.sleep(0.002)

    assert span.name == "test-span"
    assert len(span.trace_id) == 32
    assert len(span.span_id) == 16
    assert span.duration_ms > 0.0
