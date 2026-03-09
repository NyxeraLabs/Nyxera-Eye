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

import pytest

from nyxera_eye.schema.migrations import migrate_legacy_record_to_v1
from nyxera_eye.schema.models import DeviceSchema, ServiceRecord, VulnerabilityRecord
from nyxera_eye.schema.validation import validate_device_schema


def test_schema_validation_accepts_valid_record() -> None:
    record = DeviceSchema(
        device_id="dev-1",
        ip="203.0.113.10",
        services=[ServiceRecord(port=443, protocol="tcp", banner="TLS")],
        vulnerabilities=[VulnerabilityRecord(cve="CVE-2026-0001", severity="high")],
    )

    validate_device_schema(record)


def test_schema_validation_rejects_invalid_ip() -> None:
    record = DeviceSchema(device_id="dev-2", ip="999.0.0.1")

    with pytest.raises(ValueError, match="valid IPv4/IPv6"):
        validate_device_schema(record)


def test_schema_migration_maps_legacy_fields() -> None:
    legacy = {
        "ip": "198.51.100.10",
        "port": 80,
        "banner": "HTTP/1.1 200 OK",
        "org": "Legacy ISP",
        "snapshot": "s3://bucket/snap.jpg",
    }

    migrated = migrate_legacy_record_to_v1(legacy)

    assert migrated["schema_version"] == 1
    assert migrated["organization"] == "Legacy ISP"
    assert migrated["services"][0]["port"] == 80
    assert migrated["media"]["snapshot"] == "s3://bucket/snap.jpg"
    assert migrated["fingerprints"]["html_metadata"] == {}
