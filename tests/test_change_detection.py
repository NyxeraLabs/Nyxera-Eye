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

from nyxera_eye.change_detection import DiffEngine


def test_diff_engine_detects_secure_to_vulnerable() -> None:
    engine = DiffEngine()
    previous = [{"device_id": "dev-1", "vulnerabilities": []}]
    current = [{"device_id": "dev-1", "vulnerabilities": [{"cve": "CVE-2026-1010"}]}]

    events = engine.diff(previous_devices=previous, current_devices=current)

    assert len(events) == 1
    assert events[0].change_type == "secure_to_vulnerable"
    assert events[0].previous == "secure"
    assert events[0].current == "vulnerable"


def test_diff_engine_detects_firmware_change() -> None:
    engine = DiffEngine()
    previous = [{"device_id": "dev-2", "iot_metadata": {"firmware": "1.0.0"}}]
    current = [{"device_id": "dev-2", "iot_metadata": {"firmware": "1.1.0"}}]

    events = engine.diff(previous_devices=previous, current_devices=current)

    assert len(events) == 1
    assert events[0].change_type == "firmware_changed"
    assert events[0].previous == "1.0.0"
    assert events[0].current == "1.1.0"


def test_diff_engine_detects_device_disappears() -> None:
    engine = DiffEngine()
    previous = [{"device_id": "dev-3"}]
    current: list[dict] = []

    events = engine.diff(previous_devices=previous, current_devices=current)

    assert len(events) == 1
    assert events[0].change_type == "device_disappeared"
    assert events[0].device_id == "dev-3"


def test_diff_engine_detects_device_reappears() -> None:
    engine = DiffEngine()
    first_previous = [{"device_id": "dev-4"}]
    first_current: list[dict] = []
    second_previous: list[dict] = []
    second_current = [{"device_id": "dev-4"}]

    engine.diff(previous_devices=first_previous, current_devices=first_current)
    events = engine.diff(previous_devices=second_previous, current_devices=second_current)

    assert len(events) == 1
    assert events[0].change_type == "device_reappeared"
    assert events[0].device_id == "dev-4"
