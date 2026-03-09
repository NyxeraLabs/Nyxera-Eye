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

from internal.scanner.scheduler import CoverageSnapshot


def build_coverage_response(snapshot: CoverageSnapshot) -> dict[str, object]:
    return {
        "queued_targets": snapshot.queued_targets,
        "eligible_targets": snapshot.eligible_targets,
        "skipped_due_to_cooldown": snapshot.skipped_due_to_cooldown,
        "sampled_targets": snapshot.sampled_targets,
        "coverage_ratio": snapshot.coverage_ratio,
    }
