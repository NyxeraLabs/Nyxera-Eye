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

from dataclasses import dataclass


@dataclass(slots=True)
class PlatformMetrics:
    queue_depth: int
    mining_throughput: float
    probe_success_rate: float
    gpu_utilization: float
    storage_growth_gb: float

    def __post_init__(self) -> None:
        if self.queue_depth < 0:
            raise ValueError("queue_depth must be non-negative")
        if self.mining_throughput < 0:
            raise ValueError("mining_throughput must be non-negative")
        if not 0.0 <= self.probe_success_rate <= 100.0:
            raise ValueError("probe_success_rate must be in [0, 100]")
        if not 0.0 <= self.gpu_utilization <= 100.0:
            raise ValueError("gpu_utilization must be in [0, 100]")
        if self.storage_growth_gb < 0:
            raise ValueError("storage_growth_gb must be non-negative")


def export_prometheus(metrics: PlatformMetrics) -> str:
    lines = [
        "# HELP nyxera_queue_depth Current queue depth.",
        "# TYPE nyxera_queue_depth gauge",
        f"nyxera_queue_depth {metrics.queue_depth}",
        "# HELP nyxera_mining_throughput Current mining throughput.",
        "# TYPE nyxera_mining_throughput gauge",
        f"nyxera_mining_throughput {metrics.mining_throughput:.2f}",
        "# HELP nyxera_probe_success_rate Probe success rate percentage.",
        "# TYPE nyxera_probe_success_rate gauge",
        f"nyxera_probe_success_rate {metrics.probe_success_rate:.2f}",
        "# HELP nyxera_gpu_utilization GPU utilization percentage.",
        "# TYPE nyxera_gpu_utilization gauge",
        f"nyxera_gpu_utilization {metrics.gpu_utilization:.2f}",
        "# HELP nyxera_storage_growth_gb Storage growth in GB.",
        "# TYPE nyxera_storage_growth_gb counter",
        f"nyxera_storage_growth_gb {metrics.storage_growth_gb:.3f}",
    ]
    return "\n".join(lines) + "\n"
