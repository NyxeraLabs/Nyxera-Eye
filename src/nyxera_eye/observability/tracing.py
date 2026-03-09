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

from contextlib import contextmanager
from dataclasses import dataclass
from time import perf_counter
import secrets
from typing import Iterator


@dataclass(slots=True)
class SpanContext:
    name: str
    trace_id: str
    span_id: str
    duration_ms: float = 0.0


@contextmanager
def start_span(name: str) -> Iterator[SpanContext]:
    context = SpanContext(
        name=name,
        trace_id=secrets.token_hex(16),
        span_id=secrets.token_hex(8),
    )
    start = perf_counter()
    try:
        yield context
    finally:
        context.duration_ms = (perf_counter() - start) * 1000.0
