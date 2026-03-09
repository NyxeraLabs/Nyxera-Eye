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

from internal.api.handlers import build_asset_detail_response, build_investigate_link
from internal.database.models import AssetRecord
from internal.database.repository import AssetRepository


def test_build_investigate_link_points_to_investigation_route() -> None:
    assert build_investigate_link("asset-1") == "/investigation/asset-1"


def test_build_asset_detail_response_marks_asset_as_investigation_ready() -> None:
    response = build_asset_detail_response(AssetRecord(asset_id="asset-1", ip="203.0.113.10"))

    assert response["investigation_ready"] is True


def test_asset_repository_can_fetch_asset_by_ip(tmp_path: Path) -> None:
    repository = AssetRepository(str(tmp_path / "assets.db"))
    repository.initialize()
    repository.upsert(AssetRecord(asset_id="asset-1", ip="203.0.113.10"))

    fetched = repository.get_by_ip("203.0.113.10")

    assert fetched is not None
    assert fetched.asset_id == "asset-1"
