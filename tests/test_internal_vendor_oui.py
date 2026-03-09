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

from internal.intel.vendor import OUIVendorDatabase, detect_vendor_from_http_headers


def test_oui_vendor_database_looks_up_known_vendor() -> None:
    database = OUIVendorDatabase()

    vendor = database.lookup("b8:27:eb:12:34:56")

    assert vendor == "Raspberry Pi Trading Ltd"


def test_oui_vendor_database_supports_custom_entries() -> None:
    database = OUIVendorDatabase({"AA-BB-CC": "Acme Devices"})

    vendor = database.lookup("aa:bb:cc:00:11:22")

    assert vendor == "Acme Devices"


def test_oui_vendor_database_returns_none_for_unknown_vendor() -> None:
    database = OUIVendorDatabase()

    assert database.lookup("00:00:00:00:00:00") is None


def test_detect_vendor_from_http_headers_matches_known_vendor_strings() -> None:
    vendor = detect_vendor_from_http_headers(
        {
            "Server": "Hikvision-Webs/2.0",
            "WWW-Authenticate": 'Basic realm="Hikvision Camera"',
        }
    )

    assert vendor == "Hikvision"


def test_detect_vendor_from_http_headers_returns_none_when_no_match_exists() -> None:
    vendor = detect_vendor_from_http_headers({"Server": "nginx/1.25.3"})

    assert vendor is None
