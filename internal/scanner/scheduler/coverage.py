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

from __future__ import annotations

from dataclasses import dataclass
from random import Random
from time import time


@dataclass(slots=True)
class CoverageSnapshot:
    queued_targets: int
    eligible_targets: int
    skipped_due_to_cooldown: int
    sampled_targets: int
    coverage_ratio: float


class ScanCoverageEngine:
    def __init__(self, cooldown_seconds: int = 300, seed: int = 25) -> None:
        self.cooldown_seconds = max(1, cooldown_seconds)
        self._random = Random(seed)
        self._last_scan_at: dict[str, float] = {}

    def schedule(self, targets: list[dict[str, object]], sample_size: int | None = None) -> tuple[list[dict[str, object]], CoverageSnapshot]:
        now = time()
        eligible: list[dict[str, object]] = []
        skipped_due_to_cooldown = 0

        for target in targets:
            target_id = str(target.get("target_id") or target.get("ip") or "")
            last_scan_at = self._last_scan_at.get(target_id)
            if last_scan_at is not None and now - last_scan_at < self.cooldown_seconds:
                skipped_due_to_cooldown += 1
                continue
            eligible.append(dict(target))

        ordered = sorted(
            eligible,
            key=lambda item: (-int(item.get("priority", 0)), str(item.get("target_id") or item.get("ip") or "")),
        )

        if sample_size is not None and sample_size < len(ordered):
            head = ordered[: max(1, sample_size // 2)]
            tail = ordered[len(head) :]
            self._random.shuffle(tail)
            queued = head + tail[: max(0, sample_size - len(head))]
        else:
            queued = ordered

        for target in queued:
            target_id = str(target.get("target_id") or target.get("ip") or "")
            self._last_scan_at[target_id] = now

        snapshot = CoverageSnapshot(
            queued_targets=len(queued),
            eligible_targets=len(eligible),
            skipped_due_to_cooldown=skipped_due_to_cooldown,
            sampled_targets=len(queued),
            coverage_ratio=round(len(queued) / max(1, len(targets)), 3),
        )
        return queued, snapshot

    def get_last_scan_timestamp(self, target_id: str) -> float | None:
        return self._last_scan_at.get(target_id)
