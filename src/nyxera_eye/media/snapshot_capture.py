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
from datetime import UTC, datetime


@dataclass(slots=True)
class SnapshotRecord:
    device_id: str
    source_url: str
    captured_at: str
    content_type: str
    byte_size: int


class SnapshotCapture:
    def capture_metadata(self, device_id: str, source_url: str, image_bytes: bytes, content_type: str = "image/jpeg") -> SnapshotRecord:
        """Metadata-only capture descriptor. No intrusive probing is performed here."""
        return SnapshotRecord(
            device_id=device_id,
            source_url=source_url,
            captured_at=datetime.now(UTC).isoformat(),
            content_type=content_type,
            byte_size=len(image_bytes),
        )

    def build_thumbnail(self, image_bytes: bytes, max_bytes: int = 32768) -> bytes:
        if max_bytes <= 0:
            raise ValueError("max_bytes must be greater than zero")
        return image_bytes[:max_bytes]
