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

from internal.database.models import AssetRecord


def build_asset_response(record: AssetRecord) -> dict[str, object]:
    return {
        "asset_id": record.asset_id,
        "ip": record.ip,
        "fingerprint": {
            "favicon_hash": record.fingerprint.favicon_hash,
            "http_server": record.fingerprint.http_server,
            "html_title": record.fingerprint.html_title,
            "html_metadata": dict(record.fingerprint.html_metadata),
            "model_hint": record.fingerprint.model_hint,
            "firmware_hint": record.fingerprint.firmware_hint,
        },
    }
