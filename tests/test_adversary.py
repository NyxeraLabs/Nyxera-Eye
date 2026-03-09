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

from nyxera_eye.adversary.attack_mapping import map_protocols_to_attack_techniques
from nyxera_eye.adversary.deception_detection import detect_deception


def test_attack_mapping_for_ics_protocols() -> None:
    techniques = map_protocols_to_attack_techniques(["modbus", "mqtt"])
    assert "T0859" in techniques
    assert "T0880" in techniques


def test_deception_detection_flags_anomalies() -> None:
    signal = detect_deception(
        tcp_jitter_ms_series=[10.0, 15.0, 220.0],
        observed_banners=["Apache", "nginx"],
        response_time_ms_series=[20.0, 22.0, 110.0],
    )

    assert signal.tcp_jitter_anomaly is True
    assert signal.banner_inconsistency is True
    assert signal.timing_anomaly is True
    assert signal.suspicious is True


def test_deception_detection_normal_traffic() -> None:
    signal = detect_deception(
        tcp_jitter_ms_series=[12.0, 15.0, 14.0],
        observed_banners=["Apache", "Apache"],
        response_time_ms_series=[20.0, 21.0, 19.0],
    )

    assert signal.suspicious is False


def test_deception_detection_flags_moderate_timing_spike() -> None:
    signal = detect_deception(
        tcp_jitter_ms_series=[11.0, 12.0, 10.5],
        observed_banners=["Apache", "Apache"],
        response_time_ms_series=[40.0, 42.0, 170.0],
    )

    assert signal.timing_anomaly is True
    assert signal.suspicious is True
