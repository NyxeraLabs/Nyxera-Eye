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

from web.dashboard import render_coverage_panel


def test_render_coverage_panel_displays_metrics() -> None:
    html = render_coverage_panel(
        {
            "queued_targets": 4,
            "eligible_targets": 6,
            "skipped_due_to_cooldown": 2,
            "sampled_targets": 4,
            "coverage_ratio": 0.667,
        }
    )

    assert "Scan Coverage" in html
    assert "Queued Targets: 4" in html
    assert "Coverage Ratio: 0.667" in html
