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
class RTSPMetadata:
    ip: str
    port: int
    server: str | None
    methods: list[str]


class RTSPMetadataProbe:
    def __init__(self, timeout_seconds: float = 10.0) -> None:
        self.timeout_seconds = timeout_seconds

    def parse_options_response(self, ip: str, port: int, response_headers: dict[str, str]) -> RTSPMetadata:
        public = response_headers.get("Public", "")
        methods = [item.strip() for item in public.split(",") if item.strip()]
        return RTSPMetadata(
            ip=ip,
            port=port,
            server=response_headers.get("Server"),
            methods=methods,
        )
