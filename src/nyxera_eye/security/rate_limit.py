# Copyright (c) 2026 NyxeraLabs
# Author: Jose Maria Micoli
# Licensed under BSL 1.1
# Change Date: 2033-02-17 -> Apache-2.0
#
# You may:
# - Study
# - Modify
# - Use for internal security testing
#
# You may NOT:
# - Offer as a commercial service
# - Sell derived competing products

from collections import deque
from time import time


class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int) -> None:
        if max_requests <= 0:
            raise ValueError("max_requests must be greater than zero")
        if window_seconds <= 0:
            raise ValueError("window_seconds must be greater than zero")
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._subjects: dict[str, deque[float]] = {}

    def allow(self, subject: str, now: float | None = None) -> bool:
        current = time() if now is None else now
        history = self._subjects.setdefault(subject, deque())
        cutoff = current - self.window_seconds
        while history and history[0] <= cutoff:
            history.popleft()
        if len(history) >= self.max_requests:
            return False
        history.append(current)
        return True
