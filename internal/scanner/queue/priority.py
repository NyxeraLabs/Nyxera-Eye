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

from heapq import heappop, heappush


class PriorityScanQueue:
    def __init__(self) -> None:
        self._items: list[tuple[int, str, dict[str, object]]] = []

    def push(self, target: dict[str, object]) -> None:
        priority = int(target.get("priority", 0))
        target_id = str(target.get("target_id") or target.get("ip") or "")
        heappush(self._items, (-priority, target_id, dict(target)))

    def pop(self) -> dict[str, object] | None:
        if not self._items:
            return None
        return heappop(self._items)[2]

    def __len__(self) -> int:
        return len(self._items)
