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

from __future__ import annotations

from internal.api.handlers.assets import build_asset_response
from internal.database.models import AssetRecord


def build_assets_listing_response(
    records: list[AssetRecord],
    page: int = 1,
    page_size: int = 25,
) -> dict[str, object]:
    total = len(records)
    start = max(0, (page - 1) * page_size)
    end = start + page_size
    items = [build_asset_response(record) for record in records[start:end]]
    return {
        "items": items,
        "page": page,
        "page_size": page_size,
        "total": total,
    }


def build_asset_by_ip_response(record: AssetRecord | None) -> dict[str, object] | None:
    if record is None:
        return None
    return build_asset_response(record)


def build_asset_services_response(record: AssetRecord | None) -> dict[str, object] | None:
    if record is None:
        return None
    return {
        "asset_id": record.asset_id,
        "ip": record.ip,
        "services": [
            {
                "port": item.port,
                "protocol": item.protocol,
                "service": item.service,
                "version": item.version,
                "banner": item.banner,
            }
            for item in record.services
        ],
    }


def build_high_risk_assets_response(records: list[AssetRecord], threshold: float = 7.0) -> dict[str, object]:
    filtered = [record for record in records if (record.risk_score or 0.0) >= threshold]
    return {"items": [build_asset_response(record) for record in filtered], "threshold": threshold}
