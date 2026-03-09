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


class ShodanCollector(BaseOSINTCollector):
    source_name = "shodan"

    @property
    def endpoint(self) -> str:
        return "https://api.shodan.io/shodan/host/search"

    def build_params(self, query: str, page: int = 1) -> dict[str, str | int]:
        return {
            "key": self.api_key,
            "query": query,
            "page": page,
        }

    def normalize_payload(self, payload: dict) -> list[DeviceRecord]:
        records: list[DeviceRecord] = []
        for item in payload.get("matches", []):
            ip = item.get("ip_str")
            port = item.get("port")
            if not ip or not isinstance(port, int):
                continue
            records.append(
                DeviceRecord(
                    source=self.source_name,
                    ip=ip,
                    port=port,
                    protocol=item.get("transport", "tcp"),
                    banner=item.get("data"),
                    organization=item.get("org"),
                    country=item.get("location", {}).get("country_name"),
                    timestamp=item.get("timestamp"),
                )
            )
        return records
