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


def render_asset_detail_page(asset: dict[str, object]) -> str:
    services = asset.get("services") if isinstance(asset.get("services"), list) else []
    vulnerabilities = asset.get("vulnerabilities") if isinstance(asset.get("vulnerabilities"), list) else []
    fingerprint = asset.get("fingerprint") if isinstance(asset.get("fingerprint"), dict) else {}

    service_rows = "".join(
        "<tr>"
        f"<td>{escape(str(item.get('service', 'unknown')))}</td>"
        f"<td>{escape(str(item.get('port', '-')))}</td>"
        f"<td>{escape(str(item.get('version', '-')))}</td>"
        "</tr>"
        for item in services
        if isinstance(item, dict)
    ) or '<tr><td colspan="3">No services</td></tr>'

    vulnerability_items = "".join(
        f"<li>{escape(str(item.get('cve_id', 'unknown-cve')))} · {escape(str(item.get('severity', 'unknown')))}</li>"
        for item in vulnerabilities
        if isinstance(item, dict)
    ) or "<li>No known vulnerabilities</li>"

    return (
        '<section class="asset-detail-page">'
        f"<h1>{escape(str(asset.get('asset_id', 'unknown-asset')))}</h1>"
        f"<p>IP: {escape(str(asset.get('ip', '0.0.0.0')))}</p>"
        "<h2>Services</h2>"
        f"<table><thead><tr><th>Service</th><th>Port</th><th>Version</th></tr></thead><tbody>{service_rows}</tbody></table>"
        "<h2>Fingerprint</h2>"
        f"<p>HTTP Server: {escape(str(fingerprint.get('http_server', 'unavailable')))}</p>"
        f"<p>HTML Title: {escape(str(fingerprint.get('html_title', 'unavailable')))}</p>"
        f"<p>Model Hint: {escape(str(fingerprint.get('model_hint', 'unavailable')))}</p>"
        "<h2>Vulnerabilities</h2>"
        f"<ul>{vulnerability_items}</ul>"
        "</section>"
    )
