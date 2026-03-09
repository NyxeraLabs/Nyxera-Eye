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
class FirmwareVulnerabilityMapping:
    vendor: str
    model: str
    firmware: str
    cve_ids: list[str]


class FirmwareMapper:
    def __init__(self) -> None:
        self._map: dict[tuple[str, str, str], list[str]] = {}

    def add_mapping(self, vendor: str, model: str, firmware: str, cve_ids: list[str]) -> None:
        key = (vendor.strip().lower(), model.strip().lower(), firmware.strip().lower())
        self._map[key] = sorted(set(cve_ids))

    def find_cves(self, vendor: str, model: str, firmware: str) -> list[str]:
        key = (vendor.strip().lower(), model.strip().lower(), firmware.strip().lower())
        return self._map.get(key, [])
