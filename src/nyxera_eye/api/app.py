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
    from fastapi import Depends, FastAPI, Header, HTTPException, Request
    from fastapi.responses import PlainTextResponse
    from pydantic import BaseModel, Field
except ImportError:  # pragma: no cover
    FastAPI = None

from nyxera_eye.api.models import SearchFilters
from nyxera_eye.api.opensearch import OpenSearchQueryService
from nyxera_eye.api.ops_runtime import ops_runtime_store
from nyxera_eye.api.auth_runtime import auth_runtime_store
from nyxera_eye.api.audit_runtime import audit_runtime_store
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

auth_runtime_store.ensure_admin(
    username=os.getenv("NYXERA_AUTH_ADMIN_USER", "admin"),
    password=os.getenv("NYXERA_AUTH_ADMIN_PASSWORD", "admin-change-me"),
)

frontend_settings: dict[str, str | int | bool] = {
    "runtime_mode": os.getenv("NYXERA_RUNTIME_MODE", "passive"),
    "scan_default_batch_size": int(os.getenv("NYXERA_SCAN_DEFAULT_BATCH_SIZE", "96")),
    "scan_default_interval_seconds": int(os.getenv("NYXERA_SCAN_DEFAULT_INTERVAL_SECONDS", "10")),
    "auto_start_scan_loop": os.getenv("NYXERA_SCAN_AUTO_START_LOOP", "false").lower() == "true",
    "authorized_scope_reference": os.getenv("NYXERA_AUTHORIZED_SCOPE_REFERENCE", ""),
}


if FastAPI is not None:
    class RegisterRequest(BaseModel):
        username: str = Field(min_length=3, max_length=64)
        password: str = Field(min_length=10, max_length=256)
        role: str = Field(default="analyst")


    class LoginRequest(BaseModel):
        username: str = Field(min_length=3, max_length=64)
        password: str = Field(min_length=10, max_length=256)


    class FrontendSettingsRequest(BaseModel):
        runtime_mode: str = Field(default="passive")
        scan_default_batch_size: int = Field(default=96, ge=1, le=1024)
        scan_default_interval_seconds: int = Field(default=10, ge=1, le=300)
        auto_start_scan_loop: bool = False
        authorized_scope_reference: str = Field(default="", max_length=256)


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


def _actor_from_token(token: str | None) -> str:
    if token is None or not token.strip():
        return "anonymous"
    record = token_store.verify(token)
    if record is None:
        return "invalid-token"
    return f"{record.subject}:{record.role}"

if FastAPI is not None:
    app = FastAPI(
        title="Nyxera Eye API",
        version="0.1.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
    )

    async def _require_analyst(x_api_token: str | None = Header(default=None, alias="X-API-Token")) -> TokenRecord:
        return _authorize(x_api_token, required_role="analyst")

    async def _require_operator(x_api_token: str | None = Header(default=None, alias="X-API-Token")) -> TokenRecord:
        return _authorize(x_api_token, required_role="operator")

    async def _require_admin(x_api_token: str | None = Header(default=None, alias="X-API-Token")) -> TokenRecord:
        return _authorize(x_api_token, required_role="admin")

    @app.middleware("http")
    async def audit_requests(request: Request, call_next):
        token = request.headers.get("X-API-Token")
        actor = _actor_from_token(token)
        method = request.method.upper()
        path = request.url.path
        client_ip = request.client.host if request.client else "unknown"
        try:
            response = await call_next(request)
            status = "ok" if response.status_code < 400 else "error"
            audit_runtime_store.append(
                actor=actor,
                action=f"http:{method}:{path}",
                status=status,
                method=method,
                path=path,
                ip=client_ip,
                details={"status_code": response.status_code},
            )
            return response
        except Exception:
            audit_runtime_store.append(
                actor=actor,
                action=f"http:{method}:{path}",
                status="error",
                method=method,
                path=path,
                ip=client_ip,
                details={"status_code": 500},
            )
            raise

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/auth/register")
    async def auth_register(payload: RegisterRequest) -> dict:
        try:
            user = auth_runtime_store.register(
                username=payload.username,
                password=payload.password,
                role=payload.role,
            )
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

        token = token_store.issue_token(subject=user.username, role=user.role)
        return {"ok": True, "username": user.username, "role": user.role, "token": token}

    @app.post("/auth/login")
    async def auth_login(payload: LoginRequest) -> dict:
        user = auth_runtime_store.authenticate(username=payload.username, password=payload.password)
        if user is None:
            raise HTTPException(status_code=401, detail="invalid credentials")
        token = token_store.issue_token(subject=user.username, role=user.role)
        return {"ok": True, "username": user.username, "role": user.role, "token": token}

    @app.get("/auth/me")
    async def auth_me(record: TokenRecord = Depends(_require_analyst)) -> dict:
        return {"ok": True, "username": record.subject, "role": record.role}

    @app.post("/auth/logout")
    async def auth_logout(x_api_token: str | None = Header(default=None, alias="X-API-Token")) -> dict:
        if x_api_token is None or not x_api_token.strip():
            raise HTTPException(status_code=401, detail="missing API token")
        revoked = token_store.revoke(x_api_token)
        return {"ok": revoked}

    @app.get("/audit/events")
    async def audit_events(limit: int = 200, _: TokenRecord = Depends(_require_admin)) -> dict:
        events = audit_runtime_store.recent(limit=limit)
        return {"ok": True, "events": events}

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

    @app.get("/frontend/devices")
    async def frontend_devices(
        q: str | None = None,
        severity: str | None = None,
        country: str | None = None,
        vendor: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        return ops_runtime_store.list_devices(
            q=q,
            severity=severity,
            country=country,
            vendor=vendor,
            limit=limit,
            offset=offset,
        )

    @app.get("/frontend/devices/{device_id}")
    async def frontend_device_detail(device_id: str) -> dict:
        device = ops_runtime_store.get_device(device_id=device_id)
        if device is None:
            raise HTTPException(status_code=404, detail="device not found")
        return {"device": device}

    @app.get("/frontend/findings")
    async def frontend_findings(
        q: str | None = None,
        severity: str | None = None,
        status: str | None = None,
        device_id: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        return ops_runtime_store.list_findings(
            q=q,
            severity=severity,
            status=status,
            device_id=device_id,
            limit=limit,
            offset=offset,
        )

    @app.get("/frontend/findings/{finding_id}")
    async def frontend_finding_detail(finding_id: str) -> dict:
        finding = ops_runtime_store.get_finding(finding_id=finding_id)
        if finding is None:
            raise HTTPException(status_code=404, detail="finding not found")
        return {"finding": finding}

    @app.get("/frontend/settings")
    async def frontend_get_settings(record: TokenRecord = Depends(_require_analyst)) -> dict:
        return {"ok": True, "settings": frontend_settings, "user_role": record.role}

    @app.put("/frontend/settings")
    async def frontend_put_settings(
        payload: FrontendSettingsRequest,
        _: TokenRecord = Depends(_require_admin),
    ) -> dict:
        if payload.runtime_mode not in {"passive", "authorized_scope"}:
            raise HTTPException(status_code=400, detail="runtime_mode must be passive or authorized_scope")
        frontend_settings.update(
            {
                "runtime_mode": payload.runtime_mode,
                "scan_default_batch_size": payload.scan_default_batch_size,
                "scan_default_interval_seconds": payload.scan_default_interval_seconds,
                "auto_start_scan_loop": payload.auto_start_scan_loop,
                "authorized_scope_reference": payload.authorized_scope_reference,
            }
        )
        return {"ok": True, "settings": frontend_settings}

    @app.post("/frontend/scan")
    async def frontend_scan(batch_size: int = 64) -> dict:
        snapshot = ops_runtime_store.run_scan(batch_size=batch_size)
        audit_runtime_store.append(
            actor="runtime",
            action="scan:single",
            status="ok",
            method="POST",
            path="/frontend/scan",
            ip="local",
            details={"batch_size": batch_size},
        )
        return snapshot

    @app.post("/frontend/scan/start")
    async def frontend_scan_start(batch_size: int = 96, interval_seconds: int = 10) -> dict:
        started = ops_runtime_store.start_scan_loop(batch_size=batch_size, interval_seconds=interval_seconds)
        audit_runtime_store.append(
            actor="runtime",
            action="scan:loop:start",
            status="ok" if started else "error",
            method="POST",
            path="/frontend/scan/start",
            ip="local",
            details={"batch_size": batch_size, "interval_seconds": interval_seconds},
        )
        return {"ok": started, "status": ops_runtime_store.scan_loop_status()}

    @app.post("/frontend/scan/stop")
    async def frontend_scan_stop() -> dict:
        stopped = ops_runtime_store.stop_scan_loop()
        audit_runtime_store.append(
            actor="runtime",
            action="scan:loop:stop",
            status="ok" if stopped else "error",
            method="POST",
            path="/frontend/scan/stop",
            ip="local",
            details={},
        )
        return {"ok": stopped, "status": ops_runtime_store.scan_loop_status()}

    @app.get("/frontend/scan/status")
    async def frontend_scan_status() -> dict:
        return {"status": ops_runtime_store.scan_loop_status()}

    @app.post("/frontend/findings/{finding_id}/action")
    async def frontend_finding_action(finding_id: str, action: str) -> dict:
        updated = ops_runtime_store.finding_action(finding_id=finding_id, action=action)
        if updated is None:
            raise HTTPException(status_code=404, detail="finding not found")
        audit_runtime_store.append(
            actor="runtime",
            action=f"finding:{action}",
            status="ok",
            method="POST",
            path=f"/frontend/findings/{finding_id}/action",
            ip="local",
            details={"finding_id": finding_id},
        )
        return {"ok": True, "finding": updated}

    @app.get("/frontend/findings/{finding_id}/export")
    async def frontend_finding_export(finding_id: str) -> dict:
        finding = ops_runtime_store.get_finding(finding_id=finding_id)
        if finding is None:
            raise HTTPException(status_code=404, detail="finding not found")
        return {"finding": finding}
