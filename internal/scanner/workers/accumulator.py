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

import hashlib
import json

from internal.database.models import (
    AssetFingerprintRecord,
    AssetRecord,
    AssetScanHistoryRecord,
    AssetServiceRecord,
    AssetVulnerabilityRecord,
)


class AssetAccumulator:
    def accumulate(
        self,
        existing: AssetRecord | None,
        scan_result: dict[str, object],
        scanned_at: float,
    ) -> AssetRecord:
        asset_id = str(scan_result.get("asset_id") or "unknown-asset")
        ip = str(scan_result.get("ip") or "0.0.0.0")
        vendor = scan_result.get("vendor")
        fingerprint_input = scan_result.get("fingerprint") if isinstance(scan_result.get("fingerprint"), dict) else {}
        services_input = scan_result.get("services") if isinstance(scan_result.get("services"), list) else []
        vulnerabilities_input = scan_result.get("vulnerabilities") if isinstance(scan_result.get("vulnerabilities"), list) else []

        fingerprint = AssetFingerprintRecord(
            favicon_hash=_as_optional_string(fingerprint_input, "favicon_hash"),
            http_server=_as_optional_string(fingerprint_input, "http_server"),
            html_title=_as_optional_string(fingerprint_input, "html_title"),
            html_metadata=dict(fingerprint_input.get("html_metadata", {})) if isinstance(fingerprint_input.get("html_metadata"), dict) else {},
            model_hint=_as_optional_string(fingerprint_input, "model_hint"),
            firmware_hint=_as_optional_string(fingerprint_input, "firmware_hint"),
        )
        services = [
            AssetServiceRecord(
                port=int(item.get("port", 0)),
                protocol=str(item.get("protocol", "tcp")),
                service=str(item.get("service", "unknown")),
                version=str(item.get("version", "")),
                banner=item.get("banner") if item.get("banner") is None else str(item.get("banner")),
            )
            for item in services_input
            if isinstance(item, dict)
        ]
        vulnerabilities = [
            AssetVulnerabilityRecord(
                cve_id=str(item.get("cve_id", "unknown")),
                service=str(item.get("service", "unknown")),
                version=str(item.get("version", "")),
                severity=str(item.get("severity", "unknown")),
                summary=str(item.get("summary", "")),
                cvss=float(item.get("cvss", 0.0)),
            )
            for item in vulnerabilities_input
            if isinstance(item, dict)
        ]

        configuration_hash = _configuration_hash(vendor, fingerprint, services, vulnerabilities)
        previous_hash = existing.configuration_hash if existing else None
        configuration_changed = previous_hash is not None and previous_hash != configuration_hash
        history = list(existing.scan_history) if existing else []
        history.append(
            AssetScanHistoryRecord(
                scanned_at=scanned_at,
                configuration_changed=configuration_changed,
                service_count=len(services),
            )
        )

        return AssetRecord(
            asset_id=asset_id,
            ip=ip,
            vendor=str(vendor) if vendor else None,
            risk_score=float(scan_result.get("risk_score")) if scan_result.get("risk_score") is not None else (existing.risk_score if existing else None),
            scan_count=(existing.scan_count if existing else 0) + 1,
            first_seen=existing.first_seen if existing and existing.first_seen is not None else scanned_at,
            last_seen=scanned_at,
            last_updated=scanned_at,
            configuration_hash=configuration_hash,
            configuration_changed=configuration_changed,
            fingerprint=fingerprint,
            services=services,
            vulnerabilities=vulnerabilities,
            scan_history=history[-10:],
        )


def _as_optional_string(payload: dict[str, object], key: str) -> str | None:
    value = payload.get(key)
    if value in (None, ""):
        return None
    return str(value)


def _configuration_hash(
    vendor: object,
    fingerprint: AssetFingerprintRecord,
    services: list[AssetServiceRecord],
    vulnerabilities: list[AssetVulnerabilityRecord],
) -> str:
    payload = {
        "vendor": vendor,
        "fingerprint": {
            "favicon_hash": fingerprint.favicon_hash,
            "http_server": fingerprint.http_server,
            "html_title": fingerprint.html_title,
            "html_metadata": fingerprint.html_metadata,
            "model_hint": fingerprint.model_hint,
            "firmware_hint": fingerprint.firmware_hint,
        },
        "services": [
            {
                "port": item.port,
                "protocol": item.protocol,
                "service": item.service,
                "version": item.version,
                "banner": item.banner,
            }
            for item in services
        ],
        "vulnerabilities": [
            {
                "cve_id": item.cve_id,
                "service": item.service,
                "version": item.version,
                "severity": item.severity,
                "summary": item.summary,
                "cvss": item.cvss,
            }
            for item in vulnerabilities
        ],
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
