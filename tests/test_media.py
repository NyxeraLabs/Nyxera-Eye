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

import pytest

from nyxera_eye.media.minio_thumbnail_store import MinIOThumbnailStore
from nyxera_eye.media.snapshot_capture import SnapshotCapture


def test_snapshot_capture_metadata() -> None:
    capture = SnapshotCapture()
    image = b"\xff\xd8" + b"A" * 100

    record = capture.capture_metadata(
        device_id="dev-1",
        source_url="http://example/snapshot.jpg",
        image_bytes=image,
    )

    assert record.device_id == "dev-1"
    assert record.byte_size == 102


def test_snapshot_thumbnail_build() -> None:
    capture = SnapshotCapture()
    image = b"B" * 200

    thumb = capture.build_thumbnail(image, max_bytes=64)
    assert len(thumb) == 64


def test_snapshot_thumbnail_invalid_max_bytes() -> None:
    capture = SnapshotCapture()
    with pytest.raises(ValueError, match="max_bytes"):
        capture.build_thumbnail(b"abc", max_bytes=0)


def test_minio_thumbnail_prepare_upload() -> None:
    store = MinIOThumbnailStore(bucket="snapshots")
    obj = store.prepare_upload(
        device_id="dev-42",
        timestamp="2026-03-09T12:00:00+00:00",
        thumbnail_bytes=b"thumb-bytes",
    )

    assert obj.bucket == "snapshots"
    assert obj.object_key.startswith("thumbnails/dev-42/")
    assert obj.size == len(b"thumb-bytes")
