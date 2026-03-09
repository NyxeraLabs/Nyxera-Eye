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

from nyxera_eye.tui.keymap import NavigationState, handle_shortcut
from nyxera_eye.tui.mongo_query import MongoQueryInterface
from nyxera_eye.tui.search import search_as_you_type


def test_keyboard_navigation_shortcuts() -> None:
    state = NavigationState(view="scan")
    state = handle_shortcut(state, "p")
    assert state.view == "pivot"

    state = handle_shortcut(state, "v")
    assert state.view == "vulnerabilities"


def test_search_as_you_type_filters_records() -> None:
    records = [
        {"ip": "203.0.113.10", "service": "http"},
        {"ip": "198.51.100.8", "service": "modbus"},
    ]

    result = search_as_you_type("modb", records)
    assert len(result) == 1
    assert result[0]["ip"] == "198.51.100.8"


def test_mongo_query_interface() -> None:
    mongo = MongoQueryInterface()

    assert mongo.build_query("") == {}
    assert mongo.build_query("ip:203.0.113.10") == {"ip": "203.0.113.10"}
    assert mongo.build_query("camera") == {"$text": {"$search": "camera"}}
