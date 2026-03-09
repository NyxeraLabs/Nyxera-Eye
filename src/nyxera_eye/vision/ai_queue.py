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

from collections import deque
from dataclasses import dataclass


@dataclass(slots=True)
class VisionQueueItem:
    snapshot_id: str
    image_path: str


class VisionQueue:
    def __init__(self) -> None:
        self._queue: deque[VisionQueueItem] = deque()

    def enqueue(self, item: VisionQueueItem) -> None:
        self._queue.append(item)

    def dequeue(self) -> VisionQueueItem | None:
        if not self._queue:
            return None
        return self._queue.popleft()

    def depth(self) -> int:
        return len(self._queue)
