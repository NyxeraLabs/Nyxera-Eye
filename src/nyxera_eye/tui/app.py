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

try:
    from textual.app import App
except ImportError:  # pragma: no cover
    class App:  # type: ignore[override]
        pass

from nyxera_eye.tui.keymap import NavigationState, handle_shortcut
from nyxera_eye.tui.mongo_query import MongoQueryInterface
from nyxera_eye.tui.search import search_as_you_type


class NyxeraSpeedTUI(App):
    """Textual-oriented TUI shell for keyboard navigation and live filtering."""

    def __init__(self) -> None:
        super().__init__()
        self.nav_state = NavigationState()
        self.mongo = MongoQueryInterface()

    def on_shortcut(self, key: str) -> str:
        self.nav_state = handle_shortcut(self.nav_state, key)
        return self.nav_state.view

    def filter_records(self, query: str, records: list[dict[str, str]]) -> list[dict[str, str]]:
        return search_as_you_type(query, records)

    def query_from_input(self, text: str) -> dict:
        return self.mongo.build_query(text)
