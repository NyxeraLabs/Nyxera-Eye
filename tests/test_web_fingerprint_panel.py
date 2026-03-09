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

from web.assets import render_fingerprint_panel


def test_render_fingerprint_panel_displays_asset_fingerprint_fields() -> None:
    html = render_fingerprint_panel(
        {
            "asset_id": "asset-1",
            "ip": "203.0.113.10",
            "fingerprint": {
                "favicon_hash": "12345",
                "http_server": "nginx/1.25.3",
                "html_title": "Axis P3225-LV",
                "html_metadata": {"generator": "Firmware 10.12.3"},
                "model_hint": "Axis P3225-LV",
                "firmware_hint": "10.12.3",
            },
        }
    )

    assert "asset-1" in html
    assert "203.0.113.10" in html
    assert "nginx/1.25.3" in html
    assert "Axis P3225-LV" in html
    assert "12345" in html
    assert "Firmware 10.12.3" in html
