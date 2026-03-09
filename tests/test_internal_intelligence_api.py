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

from internal.api.handlers import (
    build_asset_by_ip_response,
    build_asset_services_response,
    build_assets_listing_response,
    build_high_risk_assets_response,
)
from internal.database.models import AssetRecord, AssetServiceRecord
from internal.database.repository import AssetRepository


def _seed_repository(tmp_path: Path) -> AssetRepository:
    repository = AssetRepository(str(tmp_path / "assets.db"))
    repository.initialize()
    repository.upsert(
        AssetRecord(
            asset_id="asset-1",
            ip="203.0.113.10",
            vendor="Axis Communications",
            risk_score=9.1,
            services=[AssetServiceRecord(port=443, protocol="tcp", service="https", version="1.0.4", banner="nginx")],
        )
    )
    repository.upsert(
        AssetRecord(
            asset_id="asset-2",
            ip="203.0.113.20",
            vendor="Ubiquiti Inc",
            risk_score=4.2,
            services=[AssetServiceRecord(port=22, protocol="tcp", service="ssh", version="9.0", banner="OpenSSH")],
        )
    )
    return repository


def test_build_assets_listing_response_supports_pagination() -> None:
    records = [
        AssetRecord(asset_id="asset-1", ip="203.0.113.10"),
        AssetRecord(asset_id="asset-2", ip="203.0.113.20"),
    ]

    response = build_assets_listing_response(records, page=2, page_size=1)

    assert response["page"] == 2
    assert response["page_size"] == 1
    assert response["total"] == 2
    assert response["items"][0]["asset_id"] == "asset-2"


def test_repository_list_assets_supports_filtering_and_ordering(tmp_path: Path) -> None:
    repository = _seed_repository(tmp_path)

    filtered = repository.list_assets(vendor="Axis Communications", min_risk_score=7.0)

    assert len(filtered) == 1
    assert filtered[0].asset_id == "asset-1"


def test_build_asset_by_ip_response_and_services_response(tmp_path: Path) -> None:
    repository = _seed_repository(tmp_path)
    record = repository.get_by_ip("203.0.113.10")

    detail = build_asset_by_ip_response(record)
    services = build_asset_services_response(record)

    assert detail is not None
    assert detail["asset_id"] == "asset-1"
    assert services is not None
    assert services["services"][0]["service"] == "https"


def test_build_high_risk_assets_response_filters_by_threshold() -> None:
    response = build_high_risk_assets_response(
        [
            AssetRecord(asset_id="asset-1", ip="203.0.113.10", risk_score=9.1),
            AssetRecord(asset_id="asset-2", ip="203.0.113.20", risk_score=4.2),
        ],
        threshold=7.0,
    )

    assert response["threshold"] == 7.0
    assert len(response["items"]) == 1
    assert response["items"][0]["asset_id"] == "asset-1"
