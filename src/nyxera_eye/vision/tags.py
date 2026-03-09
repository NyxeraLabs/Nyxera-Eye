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


SUPPORTED_TAGS = {
    "server racks",
    "keypads",
    "industrial panels",
    "faces",
}


@dataclass(slots=True)
class VisionTag:
    label: str
    confidence: float

    def normalized_label(self) -> str:
        return self.label.strip().lower()
