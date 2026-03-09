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
class ONVIFDevice:
    ip: str
    xaddr: str
    scopes: list[str]


class ONVIFDiscovery:
    def __init__(self, timeout_seconds: float = 8.0) -> None:
        self.timeout_seconds = timeout_seconds

    def parse_probe_match(self, ip: str, xaddr: str, scopes: list[str]) -> ONVIFDevice:
        # Parsing only; no intrusive actions or authentication attempts.
        return ONVIFDevice(ip=ip, xaddr=xaddr, scopes=scopes)
