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


def render_fingerprint_panel(asset: dict[str, object]) -> str:
    fingerprint = asset.get("fingerprint")
    if not isinstance(fingerprint, dict):
        fingerprint = {}

    html_metadata = fingerprint.get("html_metadata")
    if not isinstance(html_metadata, dict):
        html_metadata = {}

    metadata_items = "".join(
        f"<li><strong>{escape(str(key))}</strong>: {escape(str(value))}</li>"
        for key, value in sorted(html_metadata.items())
    ) or "<li><strong>metadata</strong>: unavailable</li>"

    def _value(name: str) -> str:
        value = fingerprint.get(name)
        if value in (None, ""):
            return "unavailable"
        return escape(str(value))

    return (
        '<section class="fingerprint-panel">'
        f"<header><h2>{escape(str(asset.get('asset_id', 'unknown-asset')))}</h2>"
        f"<p>{escape(str(asset.get('ip', '0.0.0.0')))}</p></header>"
        "<dl>"
        f"<div><dt>HTTP Server</dt><dd>{_value('http_server')}</dd></div>"
        f"<div><dt>HTML Title</dt><dd>{_value('html_title')}</dd></div>"
        f"<div><dt>Favicon Hash</dt><dd>{_value('favicon_hash')}</dd></div>"
        f"<div><dt>Model Hint</dt><dd>{_value('model_hint')}</dd></div>"
        f"<div><dt>Firmware Hint</dt><dd>{_value('firmware_hint')}</dd></div>"
        "</dl>"
        f"<ul>{metadata_items}</ul>"
        "</section>"
    )
