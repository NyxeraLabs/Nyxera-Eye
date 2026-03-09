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

from nyxera_eye.vision.tags import SUPPORTED_TAGS, VisionTag


class YoloAdapter:
    """Adapter for YOLO model outputs into Nyxera normalized tag labels."""

    def normalize_detections(self, detections: list[dict]) -> list[VisionTag]:
        tags: list[VisionTag] = []
        for det in detections:
            label = str(det.get("label", "")).strip().lower()
            confidence = float(det.get("confidence", 0.0))
            if label in SUPPORTED_TAGS and confidence > 0.0:
                tags.append(VisionTag(label=label, confidence=confidence))
        return tags
