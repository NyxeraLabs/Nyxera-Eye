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

from internal.database.models import CoverageRecord
from internal.database.repository import CoverageRepository


def test_coverage_repository_tracks_last_scan_timestamp() -> None:
    db_path = Path("/tmp/nyxera-coverage-test.db")
    repository = CoverageRepository(str(db_path))
    repository.initialize()
    repository.upsert(CoverageRecord(target_id="target-1", last_scan_at=1700000000.0, priority=4))

    record = repository.get("target-1")

    assert record is not None
    assert record.last_scan_at == 1700000000.0
    assert record.priority == 4
