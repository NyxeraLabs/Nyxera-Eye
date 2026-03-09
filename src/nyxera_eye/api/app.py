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

import os

try:
    from fastapi import Depends, FastAPI, Header, HTTPException
    from fastapi.responses import PlainTextResponse
except ImportError:  # pragma: no cover
    FastAPI = None

from nyxera_eye.api.models import SearchFilters
from nyxera_eye.api.opensearch import OpenSearchQueryService
from nyxera_eye.api.ops_runtime import ops_runtime_store
from nyxera_eye.api.target_cards import build_target_card
from nyxera_eye.api.command_center import (
    build_global_exposure_map_points,
    build_mining_telemetry,
    build_vulnerability_distribution,
)
from nyxera_eye.observability import PlatformMetrics, export_prometheus
from nyxera_eye.security import APITokenStore, RateLimiter, TokenRecord, role_allows

query_service = OpenSearchQueryService()
token_store = APITokenStore()
rate_limiter = RateLimiter(
    max_requests=int(os.getenv("NYXERA_API_RATE_LIMIT_REQUESTS", "120")),
    window_seconds=int(os.getenv("NYXERA_API_RATE_LIMIT_WINDOW_SECONDS", "60")),
)

bootstrap_token = os.getenv("NYXERA_API_BOOTSTRAP_TOKEN")
if bootstrap_token:
    token_store.add_token(
        token=bootstrap_token,
        subject="bootstrap",
        role=os.getenv("NYXERA_API_BOOTSTRAP_ROLE", "admin"),
    )


def _authorize(token: str | None, required_role: str) -> TokenRecord:
    if token is None or not token.strip():
        raise HTTPException(status_code=401, detail="missing API token")
    record = token_store.verify(token)
    if record is None:
        raise HTTPException(status_code=401, detail="invalid API token")
    if not role_allows(record.role, required_role):
        raise HTTPException(status_code=403, detail=f"requires role '{required_role}' or above")
    if not rate_limiter.allow(record.subject):
        raise HTTPException(status_code=429, detail="rate limit exceeded")
    return record

if FastAPI is not None:
    app = FastAPI(title="Nyxera Eye API", version="0.1.0")

    async def _require_analyst(x_api_token: str | None = Header(default=None, alias="X-API-Token")) -> TokenRecord:
        return _authorize(x_api_token, required_role="analyst")

    async def _require_operator(x_api_token: str | None = Header(default=None, alias="X-API-Token")) -> TokenRecord:
        return _authorize(x_api_token, required_role="operator")

    async def _require_admin(x_api_token: str | None = Header(default=None, alias="X-API-Token")) -> TokenRecord:
        return _authorize(x_api_token, required_role="admin")

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
        _: TokenRecord = Depends(_require_analyst),
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
    async def target_card(
        document: dict,
        _: TokenRecord = Depends(_require_analyst),
    ) -> dict[str, str | float | int | None]:
        return build_target_card(document)

    @app.post("/command-center/map")
    async def global_exposure_map(
        devices: list[dict],
        _: TokenRecord = Depends(_require_operator),
    ) -> list[dict[str, float | str | None]]:
        return build_global_exposure_map_points(devices)

    @app.post("/command-center/vulnerability-distribution")
    async def vulnerability_distribution(
        devices: list[dict],
        _: TokenRecord = Depends(_require_operator),
    ) -> dict[str, int]:
        return build_vulnerability_distribution(devices)

    @app.get("/command-center/telemetry")
    async def mining_telemetry(
        scan_throughput: float = 0.0,
        probe_latency_ms: float = 0.0,
        active_discoveries: int = 0,
        _: TokenRecord = Depends(_require_admin),
    ) -> dict[str, float | int]:
        return build_mining_telemetry(
            scan_throughput=scan_throughput,
            probe_latency_ms=probe_latency_ms,
            active_discoveries=active_discoveries,
        )

    @app.get("/observability/prometheus", response_class=PlainTextResponse)
    async def prometheus_metrics(
        queue_depth: int = 0,
        mining_throughput: float = 0.0,
        probe_success_rate: float = 0.0,
        gpu_utilization: float = 0.0,
        storage_growth_gb: float = 0.0,
        _: TokenRecord = Depends(_require_admin),
    ) -> str:
        metrics = PlatformMetrics(
            queue_depth=queue_depth,
            mining_throughput=mining_throughput,
            probe_success_rate=probe_success_rate,
            gpu_utilization=gpu_utilization,
            storage_growth_gb=storage_growth_gb,
        )
        return export_prometheus(metrics)

    @app.get("/frontend/ops-feed")
    async def frontend_ops_feed() -> dict:
        return ops_runtime_store.snapshot()

    @app.post("/frontend/scan")
    async def frontend_scan(batch_size: int = 64) -> dict:
        return ops_runtime_store.run_scan(batch_size=batch_size)

    @app.post("/frontend/scan/start")
    async def frontend_scan_start(batch_size: int = 96, interval_seconds: int = 10) -> dict:
        started = ops_runtime_store.start_scan_loop(batch_size=batch_size, interval_seconds=interval_seconds)
        return {"ok": started, "status": ops_runtime_store.scan_loop_status()}

    @app.post("/frontend/scan/stop")
    async def frontend_scan_stop() -> dict:
        stopped = ops_runtime_store.stop_scan_loop()
        return {"ok": stopped, "status": ops_runtime_store.scan_loop_status()}

    @app.get("/frontend/scan/status")
    async def frontend_scan_status() -> dict:
        return {"status": ops_runtime_store.scan_loop_status()}

    @app.post("/frontend/findings/{finding_id}/action")
    async def frontend_finding_action(finding_id: str, action: str) -> dict:
        updated = ops_runtime_store.finding_action(finding_id=finding_id, action=action)
        if updated is None:
            raise HTTPException(status_code=404, detail="finding not found")
        return {"ok": True, "finding": updated}

    @app.get("/frontend/findings/{finding_id}/export")
    async def frontend_finding_export(finding_id: str) -> dict:
        finding = ops_runtime_store.get_finding(finding_id=finding_id)
        if finding is None:
            raise HTTPException(status_code=404, detail="finding not found")
        return {"finding": finding}
