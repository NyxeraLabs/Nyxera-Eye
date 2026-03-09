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

from pathlib import Path

from internal.database.models import AssetFingerprintRecord, AssetRecord
from internal.database.repository import AssetRepository


def test_asset_repository_persists_fingerprint_data(tmp_path: Path) -> None:
    db_path = tmp_path / "assets.db"
    repository = AssetRepository(str(db_path))
    repository.initialize()

    repository.upsert(
        AssetRecord(
            asset_id="asset-1",
            ip="203.0.113.10",
            vendor="Axis Communications",
            fingerprint=AssetFingerprintRecord(
                favicon_hash="12345",
                http_server="nginx/1.25.3",
                html_title="Axis P3225-LV",
                html_metadata={"generator": "Firmware 10.12.3"},
                model_hint="Axis P3225-LV",
                firmware_hint="10.12.3",
            ),
        )
    )

    fetched = repository.get("asset-1")

    assert fetched is not None
    assert fetched.ip == "203.0.113.10"
    assert fetched.vendor == "Axis Communications"
    assert fetched.fingerprint.favicon_hash == "12345"
    assert fetched.fingerprint.http_server == "nginx/1.25.3"
    assert fetched.fingerprint.html_metadata["generator"] == "Firmware 10.12.3"
    assert fetched.fingerprint.model_hint == "Axis P3225-LV"
    assert fetched.fingerprint.firmware_hint == "10.12.3"
