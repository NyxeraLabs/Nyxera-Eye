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

from internal.intel.vendor import OUIVendorDatabase


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
