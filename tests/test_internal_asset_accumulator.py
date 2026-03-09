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

from internal.scanner.workers import AssetAccumulator


def test_asset_accumulator_tracks_scan_history_and_configuration_changes() -> None:
    accumulator = AssetAccumulator()

    first = accumulator.accumulate(
        existing=None,
        scan_result={
            "asset_id": "asset-1",
            "ip": "203.0.113.10",
            "vendor": "Axis Communications",
            "fingerprint": {"http_server": "nginx/1.25.3"},
            "services": [{"port": 443, "protocol": "tcp", "service": "https", "version": "1.0"}],
        },
        scanned_at=1700000000.0,
    )
    second = accumulator.accumulate(
        existing=first,
        scan_result={
            "asset_id": "asset-1",
            "ip": "203.0.113.10",
            "vendor": "Axis Communications",
            "fingerprint": {"http_server": "nginx/1.25.4"},
            "services": [{"port": 443, "protocol": "tcp", "service": "https", "version": "1.1"}],
        },
        scanned_at=1700001000.0,
    )

    assert first.scan_count == 1
    assert second.scan_count == 2
    assert second.configuration_changed is True
    assert second.last_updated == 1700001000.0
    assert second.scan_history[-1].configuration_changed is True
