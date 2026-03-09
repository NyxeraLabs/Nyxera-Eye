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

from internal.api.handlers import build_asset_response
from internal.database.models import AssetFingerprintRecord, AssetRecord, AssetVulnerabilityRecord


def test_build_asset_response_includes_fingerprint_information() -> None:
    response = build_asset_response(
        AssetRecord(
            asset_id="asset-1",
            ip="203.0.113.10",
            vendor="Axis Communications",
            risk_score=9.7,
            fingerprint=AssetFingerprintRecord(
                favicon_hash="12345",
                http_server="nginx/1.25.3",
                html_title="Axis P3225-LV",
                html_metadata={"generator": "Firmware 10.12.3"},
                model_hint="Axis P3225-LV",
                firmware_hint="10.12.3",
            ),
            vulnerabilities=[
                AssetVulnerabilityRecord(
                    cve_id="CVE-2026-1000",
                    service="http",
                    version="1.0.4",
                    severity="high",
                    summary="Test vulnerability",
                    cvss=8.1,
                )
            ],
        )
    )

    assert response["asset_id"] == "asset-1"
    assert response["ip"] == "203.0.113.10"
    assert response["vendor"] == "Axis Communications"
    assert response["risk_score"] == 9.7
    fingerprint = response["fingerprint"]
    assert isinstance(fingerprint, dict)
    assert fingerprint["favicon_hash"] == "12345"
    assert fingerprint["http_server"] == "nginx/1.25.3"
    assert fingerprint["html_title"] == "Axis P3225-LV"
    assert fingerprint["html_metadata"] == {"generator": "Firmware 10.12.3"}
    assert fingerprint["model_hint"] == "Axis P3225-LV"
    assert fingerprint["firmware_hint"] == "10.12.3"
    vulnerabilities = response["vulnerabilities"]
    assert isinstance(vulnerabilities, list)
    assert vulnerabilities[0]["cve_id"] == "CVE-2026-1000"
