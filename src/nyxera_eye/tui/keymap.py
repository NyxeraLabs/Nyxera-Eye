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

from dataclasses import dataclass


@dataclass(slots=True)
class NavigationState:
    view: str = "scan"


SHORTCUTS: dict[str, str] = {
    "s": "scan",
    "p": "pivot",
    "v": "vulnerabilities",
    "m": "map",
}


def handle_shortcut(state: NavigationState, key: str) -> NavigationState:
    target = SHORTCUTS.get(key.lower())
    if target is None:
        return state
    return NavigationState(view=target)
