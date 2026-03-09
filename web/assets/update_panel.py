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

from html import escape


def render_asset_update_panel(asset: dict[str, object]) -> str:
    return (
        '<section class="asset-update-panel">'
        f"<h2>{escape(str(asset.get('asset_id', 'unknown-asset')))}</h2>"
        f"<p>Last Updated: {escape(str(asset.get('last_updated', 'unavailable')))}</p>"
        f"<p>First Seen: {escape(str(asset.get('first_seen', 'unavailable')))}</p>"
        f"<p>Last Seen: {escape(str(asset.get('last_seen', 'unavailable')))}</p>"
        f"<p>Scan Count: {escape(str(asset.get('scan_count', 0)))}</p>"
        f"<p>Configuration Changed: {escape(str(asset.get('configuration_changed', False)))}</p>"
        "</section>"
    )
