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


@dataclass(slots=True)
class ThumbnailObject:
    bucket: str
    object_key: str
    size: int


class MinIOThumbnailStore:
    def __init__(self, bucket: str = "snapshots") -> None:
        self.bucket = bucket

    def object_key(self, device_id: str, timestamp: str) -> str:
        normalized_device = device_id.strip().replace(" ", "-")
        normalized_timestamp = timestamp.replace(":", "-")
        return f"thumbnails/{normalized_device}/{normalized_timestamp}.jpg"

    def prepare_upload(self, device_id: str, timestamp: str, thumbnail_bytes: bytes) -> ThumbnailObject:
        key = self.object_key(device_id=device_id, timestamp=timestamp)
        return ThumbnailObject(bucket=self.bucket, object_key=key, size=len(thumbnail_bytes))
