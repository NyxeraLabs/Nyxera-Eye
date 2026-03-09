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

from dataclasses import dataclass

from nyxera_eye.vision.tags import VisionTag
from nyxera_eye.vision.yolo_adapter import YoloAdapter


@dataclass(slots=True)
class VisionMetadata:
    snapshot_id: str
    tags: list[VisionTag]


class VisionWorker:
    def __init__(self, adapter: YoloAdapter | None = None) -> None:
        self.adapter = adapter or YoloAdapter()

    def process(self, snapshot_id: str, model_output: list[dict]) -> VisionMetadata:
        tags = self.adapter.normalize_detections(model_output)
        return VisionMetadata(snapshot_id=snapshot_id, tags=tags)
