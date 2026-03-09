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

from abc import ABC, abstractmethod

import httpx

from nyxera_eye.collectors.models import DeviceRecord


class BaseOSINTCollector(ABC):
    source_name: str

    def __init__(self, api_key: str, timeout_seconds: float = 20.0) -> None:
        self.api_key = api_key
        self.timeout_seconds = timeout_seconds

    @property
    @abstractmethod
    def endpoint(self) -> str:
        pass

    @abstractmethod
    def build_params(self, query: str, page: int = 1) -> dict[str, str | int]:
        pass

    @abstractmethod
    def normalize_payload(self, payload: dict) -> list[DeviceRecord]:
        pass

    async def fetch(
        self,
        query: str,
        page: int = 1,
        client: httpx.AsyncClient | None = None,
    ) -> list[DeviceRecord]:
        params = self.build_params(query=query, page=page)

        if client is not None:
            response = await client.get(self.endpoint, params=params)
            response.raise_for_status()
            return self.normalize_payload(response.json())

        async with httpx.AsyncClient(timeout=self.timeout_seconds) as local_client:
            response = await local_client.get(self.endpoint, params=params)
            response.raise_for_status()
            return self.normalize_payload(response.json())
