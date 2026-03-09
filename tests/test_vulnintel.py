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

from pathlib import Path

from nyxera_eye.vulnintel.cve_mirror import CVEMirrorDB, CVERecord
from nyxera_eye.vulnintel.exploit_detection import has_known_exploit
from nyxera_eye.vulnintel.firmware_mapping import FirmwareMapper
from nyxera_eye.vulnintel.risk_score import calculate_risk_score


def test_cve_mirror_insert_and_get(tmp_path: Path) -> None:
    db_path = tmp_path / "cve.db"
    mirror = CVEMirrorDB(str(db_path))
    mirror.initialize()

    mirror.upsert(
        CVERecord(
            cve_id="CVE-2026-1000",
            summary="Test vulnerability",
            cvss=8.1,
            published_at="2026-03-01",
        )
    )

    fetched = mirror.get("CVE-2026-1000")
    assert fetched is not None
    assert fetched.cvss == 8.1


def test_firmware_mapper_lookup() -> None:
    mapper = FirmwareMapper()
    mapper.add_mapping("Acme", "Cam-7", "1.0.4", ["CVE-2026-1111", "CVE-2026-2222"])

    cves = mapper.find_cves("acme", "cam-7", "1.0.4")
    assert cves == ["CVE-2026-1111", "CVE-2026-2222"]


def test_exploit_detection_from_sources() -> None:
    assert has_known_exploit(
        cve_id="CVE-2026-3000",
        cisa_kev={"CVE-2026-3000"},
        exploitdb_links={},
        epss_scores={},
    ) is True

    assert has_known_exploit(
        cve_id="CVE-2026-3001",
        cisa_kev=set(),
        exploitdb_links={"CVE-2026-3001": "https://www.exploit-db.com/exploits/1"},
        epss_scores={},
    ) is True


def test_risk_score_formula() -> None:
    score = calculate_risk_score(cvss=7.5, epss_probability=0.7, exploit_available=True, exposure_level=2.0)
    assert score == 18.0
