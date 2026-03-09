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

from internal.intel.vulnerabilities import CVERecord, VulnerabilityLookupEngine, calculate_asset_risk_score


def test_vulnerability_lookup_engine_matches_service_versions() -> None:
    engine = VulnerabilityLookupEngine()
    engine.upsert(
        CVERecord(
            cve_id="CVE-2026-1000",
            service="http",
            version="1.0.4",
            severity="high",
            summary="Test vulnerability",
            cvss=8.1,
        )
    )

    matches = engine.match("http", "1.0.4")

    assert len(matches) == 1
    assert matches[0].cve_id == "CVE-2026-1000"


def test_calculate_asset_risk_score_is_deterministic() -> None:
    assert calculate_asset_risk_score(cvss=8.1, vulnerability_count=2, exposure_level=1.5) == 11.1
