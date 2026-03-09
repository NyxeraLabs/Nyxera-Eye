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


_TLS_VENDOR_PATTERNS = {
    "hikvision": "Hikvision",
    "dahua": "Dahua",
    "axis": "Axis Communications",
    "moxa": "Moxa",
    "ubiquiti": "Ubiquiti Inc",
    "cisco": "Cisco Systems",
    "amazon": "Amazon Technologies Inc.",
}


def detect_vendor_from_tls_certificate(subject: str | None, issuer: str | None = None) -> str | None:
    haystacks = [str(subject or "").strip().lower(), str(issuer or "").strip().lower()]
    for haystack in haystacks:
        if not haystack:
            continue
        for needle, vendor in _TLS_VENDOR_PATTERNS.items():
            if needle in haystack:
                return vendor
    return None
