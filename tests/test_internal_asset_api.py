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
from internal.database.models import (
    AssetFingerprintRecord,
    AssetRecord,
    AssetScanHistoryRecord,
    AssetServiceRecord,
    AssetVulnerabilityRecord,
)


def test_build_asset_response_includes_fingerprint_information() -> None:
    response = build_asset_response(
        AssetRecord(
            asset_id="asset-1",
            ip="203.0.113.10",
            vendor="Axis Communications",
            risk_score=9.7,
            scan_count=2,
            first_seen=1700000000.0,
            last_seen=1700001000.0,
            last_updated=1700001000.0,
            configuration_hash="abc123",
            configuration_changed=True,
            fingerprint=AssetFingerprintRecord(
                favicon_hash="12345",
                http_server="nginx/1.25.3",
                html_title="Axis P3225-LV",
                html_metadata={"generator": "Firmware 10.12.3"},
                model_hint="Axis P3225-LV",
                firmware_hint="10.12.3",
            ),
            services=[
                AssetServiceRecord(port=443, protocol="tcp", service="https", version="1.0.4", banner="nginx"),
            ],
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
            scan_history=[
                AssetScanHistoryRecord(scanned_at=1700000000.0, configuration_changed=False, service_count=1),
                AssetScanHistoryRecord(scanned_at=1700001000.0, configuration_changed=True, service_count=1),
            ],
        )
    )

    assert response["asset_id"] == "asset-1"
    assert response["ip"] == "203.0.113.10"
    assert response["vendor"] == "Axis Communications"
    assert response["risk_score"] == 9.7
    assert response["scan_count"] == 2
    assert response["last_updated"] == 1700001000.0
    assert response["configuration_changed"] is True
    fingerprint = response["fingerprint"]
    assert isinstance(fingerprint, dict)
    assert fingerprint["favicon_hash"] == "12345"
    assert fingerprint["http_server"] == "nginx/1.25.3"
    assert fingerprint["html_title"] == "Axis P3225-LV"
    assert fingerprint["html_metadata"] == {"generator": "Firmware 10.12.3"}
    assert fingerprint["model_hint"] == "Axis P3225-LV"
    assert fingerprint["firmware_hint"] == "10.12.3"
    services = response["services"]
    assert isinstance(services, list)
    assert services[0]["version"] == "1.0.4"
    vulnerabilities = response["vulnerabilities"]
    assert isinstance(vulnerabilities, list)
    assert vulnerabilities[0]["cve_id"] == "CVE-2026-1000"
    history = response["scan_history"]
    assert isinstance(history, list)
    assert history[-1]["configuration_changed"] is True
