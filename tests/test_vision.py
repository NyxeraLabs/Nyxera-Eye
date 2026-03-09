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

from nyxera_eye.vision.pipeline import VisionPipeline
from nyxera_eye.vision.validation import validate_dataset_size


def test_vision_pipeline_snapshot_to_metadata_tags() -> None:
    pipeline = VisionPipeline()
    pipeline.enqueue_snapshot(snapshot_id="snap-1", image_path="/tmp/snap-1.jpg")

    metadata = pipeline.process_next(
        model_output=[
            {"label": "server racks", "confidence": 0.93},
            {"label": "industrial panels", "confidence": 0.88},
        ]
    )

    assert metadata is not None
    assert metadata.snapshot_id == "snap-1"
    assert len(metadata.tags) == 2


def test_vision_pipeline_ignores_unknown_tags() -> None:
    pipeline = VisionPipeline()
    pipeline.enqueue_snapshot(snapshot_id="snap-2", image_path="/tmp/snap-2.jpg")

    metadata = pipeline.process_next(
        model_output=[
            {"label": "unknown object", "confidence": 0.99},
            {"label": "faces", "confidence": 0.67},
        ]
    )

    assert metadata is not None
    assert [tag.label for tag in metadata.tags] == ["faces"]


def test_vision_dataset_validation_threshold() -> None:
    assert validate_dataset_size(499) is False
    assert validate_dataset_size(500) is True
