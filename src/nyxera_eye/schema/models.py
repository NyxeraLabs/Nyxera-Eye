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
class ServiceRecord:
    port: int
    protocol: str
    banner: str | None = None


@dataclass(slots=True)
class Fingerprints:
    favicon_hash: str | None = None
    ja3: str | None = None
    jarm: str | None = None


@dataclass(slots=True)
class IoTMetadata:
    vendor: str | None = None
    model: str | None = None
    firmware: str | None = None


@dataclass(slots=True)
class VulnerabilityRecord:
    cve: str
    severity: str
    exploit_available: bool = False


@dataclass(slots=True)
class MediaRecord:
    snapshot: str | None = None


@dataclass(slots=True)
class DeviceSchema:
    device_id: str
    ip: str
    hostname: str | None = None
    asn: str | None = None
    organization: str | None = None
    country: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    services: list[ServiceRecord] = field(default_factory=list)
    fingerprints: Fingerprints = field(default_factory=Fingerprints)
    iot_metadata: IoTMetadata = field(default_factory=IoTMetadata)
    vulnerabilities: list[VulnerabilityRecord] = field(default_factory=list)
    media: MediaRecord = field(default_factory=MediaRecord)
