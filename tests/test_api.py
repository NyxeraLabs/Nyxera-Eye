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

from nyxera_eye.api.models import SearchFilters
from nyxera_eye.api.opensearch import OpenSearchQueryService
from nyxera_eye.api.target_cards import build_target_card


def test_opensearch_query_builder_with_filters() -> None:
    service = OpenSearchQueryService()
    query = service.build_device_query(
        text="camera",
        filters=SearchFilters(
            asn="AS64500",
            vendor="Acme",
            vulnerability="CVE-2026-1000",
            country="AR",
            exposure_score_min=7.5,
        ),
    )

    must = query["query"]["bool"]["must"]
    assert len(must) == 6


def test_opensearch_query_builder_without_filters() -> None:
    service = OpenSearchQueryService()
    query = service.build_device_query(text=None, filters=SearchFilters())
    assert query["query"] == {"match_all": {}}


def test_target_card_builder() -> None:
    card = build_target_card(
        {
            "device_id": "dev-1",
            "ip": "203.0.113.10",
            "organization": "Nyxera Labs",
            "country": "AR",
            "exposure_score": 8.2,
            "services": [{"port": 80}, {"port": 443}],
            "vulnerabilities": [{"cve": "CVE-2026-1000"}],
        }
    )

    assert card["service_count"] == 2
    assert card["top_vulnerability"] == "CVE-2026-1000"
