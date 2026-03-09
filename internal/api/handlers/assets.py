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

from internal.database.models import AssetRecord


def build_asset_response(record: AssetRecord) -> dict[str, object]:
    return {
        "asset_id": record.asset_id,
        "ip": record.ip,
        "vendor": record.vendor,
        "risk_score": record.risk_score,
        "scan_count": record.scan_count,
        "first_seen": record.first_seen,
        "last_seen": record.last_seen,
        "last_updated": record.last_updated,
        "configuration_changed": record.configuration_changed,
        "fingerprint": {
            "favicon_hash": record.fingerprint.favicon_hash,
            "http_server": record.fingerprint.http_server,
            "html_title": record.fingerprint.html_title,
            "html_metadata": dict(record.fingerprint.html_metadata),
            "model_hint": record.fingerprint.model_hint,
            "firmware_hint": record.fingerprint.firmware_hint,
        },
        "services": [
            {
                "port": item.port,
                "protocol": item.protocol,
                "service": item.service,
                "version": item.version,
                "banner": item.banner,
            }
            for item in record.services
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
            for item in record.vulnerabilities
        ],
        "scan_history": [
            {
                "scanned_at": item.scanned_at,
                "configuration_changed": item.configuration_changed,
                "service_count": item.service_count,
            }
            for item in record.scan_history
        ],
    }
