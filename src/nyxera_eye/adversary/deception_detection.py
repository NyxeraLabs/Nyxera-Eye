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

from dataclasses import dataclass


@dataclass(slots=True)
class DeceptionSignal:
    tcp_jitter_anomaly: bool
    banner_inconsistency: bool
    timing_anomaly: bool

    @property
    def suspicious(self) -> bool:
        return self.tcp_jitter_anomaly or self.banner_inconsistency or self.timing_anomaly


def detect_deception(
    tcp_jitter_ms_series: list[float],
    observed_banners: list[str],
    response_time_ms_series: list[float],
) -> DeceptionSignal:
    tcp_jitter_anomaly = _has_jitter_anomaly(tcp_jitter_ms_series)
    banner_inconsistency = _has_banner_inconsistency(observed_banners)
    timing_anomaly = _has_timing_anomaly(response_time_ms_series)

    return DeceptionSignal(
        tcp_jitter_anomaly=tcp_jitter_anomaly,
        banner_inconsistency=banner_inconsistency,
        timing_anomaly=timing_anomaly,
    )


def _has_jitter_anomaly(samples: list[float]) -> bool:
    if len(samples) < 3:
        return False
    spread = max(samples) - min(samples)
    return spread > 150.0


def _has_banner_inconsistency(banners: list[str]) -> bool:
    normalized = {banner.strip().lower() for banner in banners if banner.strip()}
    return len(normalized) > 1


def _has_timing_anomaly(samples: list[float]) -> bool:
    if len(samples) < 3:
        return False
    avg = sum(samples) / len(samples)
    if avg == 0:
        return False
    peak = max(samples)
    return peak > avg * 3.0
