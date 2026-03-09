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

from copy import deepcopy


def migrate_legacy_record_to_v1(raw: dict) -> dict:
    """Normalize legacy flat records into canonical v1 layout."""
    src = deepcopy(raw)

    device_id = src.get("device_id") or f"{src.get('ip', 'unknown')}:{src.get('port', '0')}"

    service = {
        "port": int(src.get("port", 0)),
        "protocol": src.get("protocol", "tcp"),
        "banner": src.get("banner"),
    }

    migrated = {
        "schema_version": 1,
        "device_id": device_id,
        "ip": src.get("ip", "0.0.0.0"),
        "hostname": src.get("hostname"),
        "asn": src.get("asn"),
        "organization": src.get("organization") or src.get("org"),
        "country": src.get("country"),
        "latitude": src.get("latitude"),
        "longitude": src.get("longitude"),
        "services": [service] if service["port"] > 0 else [],
        "fingerprints": {
            "favicon_hash": src.get("favicon_hash"),
            "ja3": src.get("ja3"),
            "jarm": src.get("jarm"),
            "http_server": src.get("http_server"),
            "html_title": src.get("html_title"),
            "html_metadata": src.get("html_metadata", {}),
        },
        "iot_metadata": {
            "vendor": src.get("vendor"),
            "model": src.get("model"),
            "firmware": src.get("firmware"),
        },
        "vulnerabilities": src.get("vulnerabilities", []),
        "media": {
            "snapshot": src.get("snapshot"),
        },
    }

    return migrated
