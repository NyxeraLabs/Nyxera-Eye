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

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class CVERecord:
    cve_id: str
    service: str
    version: str
    severity: str
    summary: str
    cvss: float


class VulnerabilityLookupEngine:
    def __init__(self) -> None:
        self._records: dict[tuple[str, str], list[CVERecord]] = {}

    def upsert(self, record: CVERecord) -> None:
        key = (record.service.strip().lower(), record.version.strip().lower())
        bucket = self._records.setdefault(key, [])
        for index, existing in enumerate(bucket):
            if existing.cve_id == record.cve_id:
                bucket[index] = record
                break
        else:
            bucket.append(record)

    def match(self, service: str, version: str) -> list[CVERecord]:
        key = (service.strip().lower(), version.strip().lower())
        return list(self._records.get(key, []))
