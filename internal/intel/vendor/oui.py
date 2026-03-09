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


class OUIVendorDatabase:
    def __init__(self, entries: dict[str, str] | None = None) -> None:
        self._entries = {
            "B8:27:EB": "Raspberry Pi Trading Ltd",
            "44:65:0D": "Amazon Technologies Inc.",
            "00:1B:63": "Cisco Systems",
            "3C:5A:B4": "Google Nest",
            "FC:D7:33": "Ubiquiti Inc",
        }
        if entries:
            for oui, vendor in entries.items():
                self._entries[_normalize_oui(oui)] = vendor.strip()

    def add(self, oui: str, vendor: str) -> None:
        self._entries[_normalize_oui(oui)] = vendor.strip()

    def lookup(self, mac_address: str) -> str | None:
        if not mac_address.strip():
            return None
        return self._entries.get(_extract_oui(mac_address))


def _extract_oui(mac_address: str) -> str:
    normalized = mac_address.strip().replace("-", ":").upper()
    parts = normalized.split(":")
    if len(parts) < 3:
        return normalized
    return ":".join(parts[:3])


def _normalize_oui(oui: str) -> str:
    return _extract_oui(oui)
