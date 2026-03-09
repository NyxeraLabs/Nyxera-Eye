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

from internal.scanner.queue import PriorityScanQueue
from internal.scanner.scheduler import ScanCoverageEngine


def test_priority_scan_queue_returns_highest_priority_first() -> None:
    queue = PriorityScanQueue()
    queue.push({"target_id": "low", "priority": 1})
    queue.push({"target_id": "high", "priority": 5})

    assert queue.pop()["target_id"] == "high"
    assert queue.pop()["target_id"] == "low"


def test_scan_coverage_engine_applies_cooldown_and_sampling() -> None:
    engine = ScanCoverageEngine(cooldown_seconds=3600, seed=25)
    targets = [
        {"target_id": "a", "priority": 5},
        {"target_id": "b", "priority": 4},
        {"target_id": "c", "priority": 1},
        {"target_id": "d", "priority": 1},
    ]

    queued, snapshot = engine.schedule(targets, sample_size=3)
    queued_again, snapshot_again = engine.schedule(targets, sample_size=3)

    assert len(queued) == 3
    assert snapshot.coverage_ratio == 0.75
    assert snapshot_again.skipped_due_to_cooldown >= 3
    assert len(queued_again) <= 1
