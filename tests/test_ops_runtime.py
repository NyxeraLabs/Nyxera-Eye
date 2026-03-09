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

from threading import Thread

from nyxera_eye.api.ops_runtime import OpsRuntimeStore


def test_ops_runtime_store_initial_scan_completes_without_deadlock() -> None:
    result: dict[str, dict] = {}

    def _build_store() -> None:
        result["snapshot"] = OpsRuntimeStore().snapshot()

    thread = Thread(target=_build_store, daemon=True)
    thread.start()
    thread.join(timeout=2.0)

    assert not thread.is_alive()
    assert result["snapshot"]["metrics"]["scan_runs"] == 1
    assert len(result["snapshot"]["metrics"]["scan_history"]) == 1
    assert len(result["snapshot"]["devices"]) == 64


def test_ops_runtime_run_scan_accumulates_inventory_and_findings() -> None:
    store = OpsRuntimeStore()

    initial = store.snapshot()
    snapshot = store.run_scan(batch_size=128)

    assert snapshot["metrics"]["scan_runs"] == 2
    assert len(snapshot["devices"]) == 192
    assert len(snapshot["findings"]) == 192
    assert len(snapshot["metrics"]["scan_history"]) == 2
    assert snapshot["devices"][0]["fingerprints"]["favicon_hash"] is not None
    assert snapshot["devices"][0]["fingerprints"]["html_title"]
    assert snapshot["devices"][0]["iot_metadata"]["model"]
    assert len(initial["devices"]) < len(snapshot["devices"])
    assert snapshot["metrics"]["devices_by_vendor"]
    assert snapshot["metrics"]["services_by_port"]


def test_ops_runtime_supports_device_and_finding_filters() -> None:
    store = OpsRuntimeStore()

    devices = store.list_devices(q="Axis", vendor="Axis")
    assert devices["total"] > 0
    device_id = devices["items"][0]["device_id"]

    findings = store.list_findings(device_id=device_id, severity=devices["items"][0]["severity"])
    assert findings["total"] > 0

    detail = store.get_device(device_id)
    assert detail is not None
    assert detail["finding"]["device_id"] == device_id
    assert isinstance(detail["events"], list)
