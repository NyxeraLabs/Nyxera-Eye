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

from nyxera_eye.vision.ai_queue import VisionQueue, VisionQueueItem
from nyxera_eye.vision.worker import VisionMetadata, VisionWorker


class VisionPipeline:
    def __init__(self, worker: VisionWorker | None = None) -> None:
        self.queue = VisionQueue()
        self.worker = worker or VisionWorker()

    def enqueue_snapshot(self, snapshot_id: str, image_path: str) -> None:
        self.queue.enqueue(VisionQueueItem(snapshot_id=snapshot_id, image_path=image_path))

    def process_next(self, model_output: list[dict]) -> VisionMetadata | None:
        item = self.queue.dequeue()
        if item is None:
            return None
        return self.worker.process(snapshot_id=item.snapshot_id, model_output=model_output)
