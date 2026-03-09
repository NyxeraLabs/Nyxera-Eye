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
    from fastapi import FastAPI
except ImportError:  # pragma: no cover
    FastAPI = None

from nyxera_eye.api.models import SearchFilters
from nyxera_eye.api.opensearch import OpenSearchQueryService
from nyxera_eye.api.target_cards import build_target_card
from nyxera_eye.api.command_center import (
    build_global_exposure_map_points,
    build_mining_telemetry,
    build_vulnerability_distribution,
)

query_service = OpenSearchQueryService()

if FastAPI is not None:
    app = FastAPI(title="Nyxera Eye API", version="0.1.0")

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/search/opensearch")
    async def opensearch_query(
        q: str | None = None,
        asn: str | None = None,
        vendor: str | None = None,
        vulnerability: str | None = None,
        country: str | None = None,
        exposure_score_min: float | None = None,
    ) -> dict:
        filters = SearchFilters(
            asn=asn,
            vendor=vendor,
            vulnerability=vulnerability,
            country=country,
            exposure_score_min=exposure_score_min,
        )
        return query_service.build_device_query(q, filters)

    @app.post("/ui/target-card")
    async def target_card(document: dict) -> dict[str, str | float | int | None]:
        return build_target_card(document)

    @app.post("/command-center/map")
    async def global_exposure_map(devices: list[dict]) -> list[dict[str, float | str | None]]:
        return build_global_exposure_map_points(devices)

    @app.post("/command-center/vulnerability-distribution")
    async def vulnerability_distribution(devices: list[dict]) -> dict[str, int]:
        return build_vulnerability_distribution(devices)

    @app.get("/command-center/telemetry")
    async def mining_telemetry(
        scan_throughput: float = 0.0,
        probe_latency_ms: float = 0.0,
        active_discoveries: int = 0,
    ) -> dict[str, float | int]:
        return build_mining_telemetry(
            scan_throughput=scan_throughput,
            probe_latency_ms=probe_latency_ms,
            active_discoveries=active_discoveries,
        )
