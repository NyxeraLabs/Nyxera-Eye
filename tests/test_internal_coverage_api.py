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

from internal.api.handlers import build_coverage_response
from internal.scanner.scheduler import CoverageSnapshot


def test_build_coverage_response_exposes_coverage_metrics() -> None:
    response = build_coverage_response(
        CoverageSnapshot(
            queued_targets=4,
            eligible_targets=6,
            skipped_due_to_cooldown=2,
            sampled_targets=4,
            coverage_ratio=0.667,
        )
    )

    assert response["queued_targets"] == 4
    assert response["coverage_ratio"] == 0.667
