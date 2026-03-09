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

import time


class DorkManager:
    def __init__(
        self,
        categories: dict[str, list[str]],
        rate_limit_seconds: dict[str, float] | None = None,
    ) -> None:
        self.categories = {name: dorks[:] for name, dorks in categories.items()}
        self.rate_limit_seconds = rate_limit_seconds or {}
        self._cursor: dict[str, int] = {name: 0 for name in categories}
        self._last_query_at: dict[str, float] = {name: 0.0 for name in categories}

    def next_query(self, category: str, now: float | None = None) -> str | None:
        if category not in self.categories:
            raise KeyError(f"unknown dork category: {category}")

        dorks = self.categories[category]
        if not dorks:
            return None

        current_time = now if now is not None else time.monotonic()
        min_interval = self.rate_limit_seconds.get(category, 0.0)
        elapsed = current_time - self._last_query_at[category]
        if elapsed < min_interval:
            return None

        idx = self._cursor[category]
        query = dorks[idx]
        self._cursor[category] = (idx + 1) % len(dorks)
        self._last_query_at[category] = current_time
        return query
