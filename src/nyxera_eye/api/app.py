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
