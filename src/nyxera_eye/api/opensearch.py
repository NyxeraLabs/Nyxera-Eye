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


class OpenSearchQueryService:
    def build_device_query(self, text: str | None, filters: SearchFilters) -> dict:
        must: list[dict] = []
        query_text = (text or "").strip()

        if query_text:
            must.append(
                {
                    "multi_match": {
                        "query": query_text,
                        "fields": [
                            "ip^3",
                            "hostname^2",
                            "organization",
                            "country",
                            "services.banner",
                            "vulnerabilities.cve",
                        ],
                    }
                }
            )

        if filters.asn:
            must.append({"term": {"asn.keyword": filters.asn}})
        if filters.vendor:
            must.append({"term": {"iot_metadata.vendor.keyword": filters.vendor}})
        if filters.vulnerability:
            must.append({"term": {"vulnerabilities.cve.keyword": filters.vulnerability}})
        if filters.country:
            must.append({"term": {"country.keyword": filters.country}})
        if filters.exposure_score_min is not None:
            must.append({"range": {"exposure_score": {"gte": filters.exposure_score_min}}})

        if not must:
            return {"query": {"match_all": {}}, "sort": [{"exposure_score": "desc"}]}

        return {
            "query": {"bool": {"must": must}},
            "sort": [{"exposure_score": "desc"}],
        }
