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

from internal.intel.vendor.http_headers import detect_vendor_from_http_headers
from internal.intel.vendor.oui import OUIVendorDatabase
from internal.intel.vendor.tls_certificates import detect_vendor_from_tls_certificate


class VendorDetectionEngine:
    def __init__(self, oui_database: OUIVendorDatabase | None = None) -> None:
        self._oui_database = oui_database or OUIVendorDatabase()

    def detect(
        self,
        mac_address: str | None = None,
        http_headers: dict[str, str] | None = None,
        tls_subject: str | None = None,
        tls_issuer: str | None = None,
    ) -> str | None:
        for detector in (
            lambda: detect_vendor_from_http_headers(http_headers),
            lambda: detect_vendor_from_tls_certificate(tls_subject, tls_issuer),
            lambda: self._oui_database.lookup(mac_address or ""),
        ):
            vendor = detector()
            if vendor:
                return vendor
        return None
