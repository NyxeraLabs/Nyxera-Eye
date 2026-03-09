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


def render_vendor_table(assets: list[dict[str, object]]) -> str:
    rows = "".join(
        "<tr>"
        f"<td>{escape(str(asset.get('asset_id', 'unknown-asset')))}</td>"
        f"<td>{escape(str(asset.get('ip', '0.0.0.0')))}</td>"
        f"<td>{escape(str(asset.get('vendor') or 'unavailable'))}</td>"
        "</tr>"
        for asset in assets
    ) or '<tr><td colspan="3">No assets available</td></tr>'

    return (
        '<table class="vendor-table">'
        "<thead><tr><th>Asset</th><th>IP</th><th>Vendor</th></tr></thead>"
        f"<tbody>{rows}</tbody>"
        "</table>"
    )
