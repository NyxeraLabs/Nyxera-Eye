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
class DeviceRecord:
    source: str
    ip: str
    port: int
    protocol: str
    banner: str | None = None
    organization: str | None = None
    country: str | None = None
    timestamp: str | None = None
