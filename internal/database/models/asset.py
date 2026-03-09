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
class AssetServiceRecord:
    port: int
    protocol: str
    service: str
    version: str
    banner: str | None = None


@dataclass(slots=True)
class AssetScanHistoryRecord:
    scanned_at: float
    configuration_changed: bool
    service_count: int


@dataclass(slots=True)
class AssetRecord:
    asset_id: str
    ip: str
    vendor: str | None = None
    risk_score: float | None = None
    scan_count: int = 0
    first_seen: float | None = None
    last_seen: float | None = None
    last_updated: float | None = None
    configuration_hash: str | None = None
    configuration_changed: bool = False
    fingerprint: AssetFingerprintRecord = field(default_factory=AssetFingerprintRecord)
    services: list[AssetServiceRecord] = field(default_factory=list)
    vulnerabilities: list[AssetVulnerabilityRecord] = field(default_factory=list)
    scan_history: list[AssetScanHistoryRecord] = field(default_factory=list)
