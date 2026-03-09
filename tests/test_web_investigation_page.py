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

from web.investigation import render_asset_detail_page


def test_render_asset_detail_page_displays_services_fingerprint_and_vulnerabilities() -> None:
    html = render_asset_detail_page(
        {
            "asset_id": "asset-1",
            "ip": "203.0.113.10",
            "services": [{"service": "https", "port": 443, "version": "1.0.4"}],
            "fingerprint": {"http_server": "nginx/1.25.3", "html_title": "Axis P3225-LV", "model_hint": "Axis P3225-LV"},
            "vulnerabilities": [{"cve_id": "CVE-2026-1000", "severity": "high"}],
        }
    )

    assert "https" in html
    assert "443" in html
    assert "Axis P3225-LV" in html
    assert "CVE-2026-1000" in html
