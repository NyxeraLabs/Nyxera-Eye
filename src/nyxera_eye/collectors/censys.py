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


class CensysCollector(BaseOSINTCollector):
    source_name = "censys"

    @property
    def endpoint(self) -> str:
        return "https://search.censys.io/api/v2/hosts/search"

    def build_params(self, query: str, page: int = 1) -> dict[str, str | int]:
        return {
            "q": query,
            "per_page": 100,
            "virtual_hosts": "EXCLUDE",
            "cursor": page,
        }

    def normalize_payload(self, payload: dict) -> list[DeviceRecord]:
        result = payload.get("result", {})
        records: list[DeviceRecord] = []

        for item in result.get("hits", []):
            ip = item.get("ip")
            services = item.get("services", [])
            if not ip or not services:
                continue

            for service in services:
                port = service.get("port")
                if not isinstance(port, int):
                    continue
                records.append(
                    DeviceRecord(
                        source=self.source_name,
                        ip=ip,
                        port=port,
                        protocol=service.get("transport_protocol", "tcp"),
                        banner=service.get("banner"),
                        organization=item.get("autonomous_system", {}).get("description"),
                        country=item.get("location", {}).get("country"),
                        timestamp=item.get("last_updated_at"),
                    )
                )

        return records
