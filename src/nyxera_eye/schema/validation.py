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

from ipaddress import ip_address

from nyxera_eye.schema.models import DeviceSchema, ServiceRecord


_ALLOWED_SEVERITIES = {"critical", "high", "medium", "low", "unknown"}


def validate_device_schema(record: DeviceSchema) -> None:
    if not record.device_id.strip():
        raise ValueError("device_id is required")

    try:
        ip_address(record.ip)
    except ValueError as exc:
        raise ValueError("ip must be a valid IPv4/IPv6 address") from exc

    if record.latitude is not None and not (-90.0 <= record.latitude <= 90.0):
        raise ValueError("latitude out of range")

    if record.longitude is not None and not (-180.0 <= record.longitude <= 180.0):
        raise ValueError("longitude out of range")

    for service in record.services:
        _validate_service(service)

    for vuln in record.vulnerabilities:
        if not vuln.cve.startswith("CVE-"):
            raise ValueError("vulnerability cve must use CVE- prefix")
        if vuln.severity.lower() not in _ALLOWED_SEVERITIES:
            raise ValueError("vulnerability severity is invalid")


def _validate_service(service: ServiceRecord) -> None:
    if not (1 <= service.port <= 65535):
        raise ValueError("service port out of range")
    if not service.protocol.strip():
        raise ValueError("service protocol is required")
