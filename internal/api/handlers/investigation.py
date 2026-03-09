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

from internal.api.handlers.assets import build_asset_response
from internal.database.models import AssetRecord


def build_asset_detail_response(record: AssetRecord) -> dict[str, object]:
    response = build_asset_response(record)
    response["investigation_ready"] = True
    return response


def build_investigate_link(asset_id: str) -> str:
    normalized = asset_id.strip() or "unknown-asset"
    return f"/investigation/{normalized}"
