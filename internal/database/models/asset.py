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

from dataclasses import dataclass, field


@dataclass(slots=True)
class AssetFingerprintRecord:
    favicon_hash: str | None = None
    http_server: str | None = None
    html_title: str | None = None
    html_metadata: dict[str, str] = field(default_factory=dict)
    model_hint: str | None = None
    firmware_hint: str | None = None


@dataclass(slots=True)
class AssetVulnerabilityRecord:
    cve_id: str
    service: str
    version: str
    severity: str
    summary: str
    cvss: float


@dataclass(slots=True)
class AssetRecord:
    asset_id: str
    ip: str
    vendor: str | None = None
    risk_score: float | None = None
    fingerprint: AssetFingerprintRecord = field(default_factory=AssetFingerprintRecord)
    vulnerabilities: list[AssetVulnerabilityRecord] = field(default_factory=list)
