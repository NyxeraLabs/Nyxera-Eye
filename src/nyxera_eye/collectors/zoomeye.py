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

from nyxera_eye.collectors.base import BaseOSINTCollector
from nyxera_eye.collectors.models import DeviceRecord


class ZoomEyeCollector(BaseOSINTCollector):
    source_name = "zoomeye"

    @property
    def endpoint(self) -> str:
        return "https://api.zoomeye.hk/host/search"

    def build_params(self, query: str, page: int = 1) -> dict[str, str | int]:
        return {
            "query": query,
            "page": page,
        }

    def normalize_payload(self, payload: dict) -> list[DeviceRecord]:
        records: list[DeviceRecord] = []
        for item in payload.get("matches", []):
            ip = item.get("ip")
            port = item.get("portinfo", {}).get("port")
            if not ip or not isinstance(port, int):
                continue
            records.append(
                DeviceRecord(
                    source=self.source_name,
                    ip=ip,
                    port=port,
                    protocol=item.get("portinfo", {}).get("transport", "tcp"),
                    banner=item.get("portinfo", {}).get("banner"),
                    organization=item.get("geoinfo", {}).get("organization"),
                    country=item.get("geoinfo", {}).get("country", {}).get("names", {}).get("en"),
                    timestamp=item.get("timestamp"),
                )
            )
        return records
