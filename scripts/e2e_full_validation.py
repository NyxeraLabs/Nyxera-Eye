#!/usr/bin/env python3
"""Comprehensive local E2E validation across implemented roadmap phases."""

from __future__ import annotations

import asyncio
from pathlib import Path
from tempfile import TemporaryDirectory
from time import sleep

from nyxera_eye.adversary import detect_deception, map_protocols_to_attack_techniques
from nyxera_eye.api.command_center import (
    build_global_exposure_map_points,
    build_mining_telemetry,
    build_vulnerability_distribution,
)
from nyxera_eye.api.models import SearchFilters
from nyxera_eye.api.opensearch import OpenSearchQueryService
from nyxera_eye.api.target_cards import build_target_card
from nyxera_eye.audit.logger import AuditLogger
from nyxera_eye.change_detection import DiffEngine
from nyxera_eye.clustering import correlate_by_certificate_serial
from nyxera_eye.collectors import CensysCollector, ShodanCollector, ZoomEyeCollector
from nyxera_eye.collectors.dork_manager import DorkManager
from nyxera_eye.compliance import OptOutRegistry, RuntimeMode, RuntimePolicy, ScopePolicy, TargetBlacklist
from nyxera_eye.enrichment import geolocate_with_fallback
from nyxera_eye.fingerprinting import build_ja3_string, jarm_fingerprint, ja3_hash, murmurhash3_x86_32
from nyxera_eye.media import MinIOThumbnailStore, SnapshotCapture
from nyxera_eye.observability import PlatformMetrics, export_prometheus, start_span
from nyxera_eye.protocols import ONVIFDiscovery, RTSPMetadataProbe, SNMPMetadataExtractor
import nyxera_eye.queue.redis_queue as redis_queue_module
from nyxera_eye.queue.redis_queue import RedisTaskQueue
from nyxera_eye.schema import DeviceSchema, migrate_legacy_record_to_v1, validate_device_schema
from nyxera_eye.schema.models import ServiceRecord, VulnerabilityRecord
from nyxera_eye.security import APITokenStore, RateLimiter, decrypt_secret, encrypt_secret, role_allows
from nyxera_eye.tui import NyxeraSpeedTUI
from nyxera_eye.vision import VisionPipeline, validate_dataset_size
from nyxera_eye.vulnintel import CVEMirrorDB, CVERecord, FirmwareMapper, calculate_risk_score, has_known_exploit
from nyxera_eye.workers.pipeline import ProcessingPipeline
SHODAN_PAYLOAD = {
    "matches": [
        {
            "ip_str": "198.51.100.10",
            "port": 80,
            "transport": "tcp",
            "data": "HTTP/1.1 200 OK",
            "org": "Example ISP",
            "location": {"country_name": "Argentina"},
            "timestamp": "2026-03-01T10:00:00Z",
        }
    ]
}

CENSYS_PAYLOAD = {
    "result": {
        "hits": [
            {
                "ip": "203.0.113.44",
                "services": [
                    {
                        "port": 443,
                        "transport_protocol": "tcp",
                        "banner": "TLS service",
                    }
                ],
                "autonomous_system": {"description": "AS64500"},
                "location": {"country": "US"},
                "last_updated_at": "2026-03-01T10:05:00Z",
            }
        ]
    }
}

ZOOMEYE_PAYLOAD = {
    "matches": [
        {
            "ip": "192.0.2.77",
            "portinfo": {
                "port": 502,
                "transport": "tcp",
                "banner": "Modbus",
            },
            "geoinfo": {
                "organization": "Factory Net",
                "country": {"names": {"en": "Germany"}},
            },
            "timestamp": "2026-03-01T10:10:00Z",
        }
    ]
}


def _phase0_compliance_and_audit(tmp_dir: Path) -> None:
    scope = ScopePolicy()
    scope.add_cidr("198.51.100.0/24")
    policy = RuntimePolicy(mode=RuntimeMode.AUTHORIZED_SCOPE, scope_policy=scope)
    assert policy.can_perform_intrusive_action("198.51.100.10") is True
    assert RuntimePolicy().can_perform_intrusive_action("198.51.100.10") is False

    blacklist = TargetBlacklist()
    blacklist.add("198.51.100.66")
    assert blacklist.is_blocked("198.51.100.66") is True

    opt_out = OptOutRegistry()
    opt_out.register("example.com")
    assert opt_out.is_opted_out("example.com") is True

    audit_file = tmp_dir / "audit.log"
    logger = AuditLogger(log_path=str(audit_file))
    logger.log(actor="operator", action="probe", target="198.51.100.10", mode="authorized_scope")
    assert "operator" in audit_file.read_text(encoding="utf-8")


def _phase2_collectors_and_queue() -> list:
    shodan_records = ShodanCollector(api_key="demo").normalize_payload(SHODAN_PAYLOAD)
    censys_records = CensysCollector(api_key="demo").normalize_payload(CENSYS_PAYLOAD)
    zoomeye_records = ZoomEyeCollector(api_key="demo").normalize_payload(ZOOMEYE_PAYLOAD)
    assert len(shodan_records) == len(censys_records) == len(zoomeye_records) == 1

    manager = DorkManager(
        categories={"ics": ["port:502", "port:20000"]},
        rate_limit_seconds={"ics": 2.0},
    )
    assert manager.next_query("ics", now=10.0) == "port:502"
    assert manager.next_query("ics", now=11.0) is None
    assert manager.next_query("ics", now=12.1) == "port:20000"

    queued_payloads: list[dict] = []

    class _FakeRedis:
        async def enqueue_job(self, _job: str, payload: dict) -> None:
            queued_payloads.append(payload)

        async def close(self) -> None:
            return None

    class _FakeRedisSettings:
        def __init__(self, host: str, port: int, database: int) -> None:
            self.host = host
            self.port = port
            self.database = database

    async def _fake_create_pool(_settings: _FakeRedisSettings) -> _FakeRedis:
        return _FakeRedis()

    redis_queue_module.RedisSettings = _FakeRedisSettings
    redis_queue_module.create_pool = _fake_create_pool
    asyncio.run(RedisTaskQueue().enqueue_osint_task(provider="shodan", query="port:80", page=1))
    assert queued_payloads and queued_payloads[0]["provider"] == "shodan"

    return [shodan_records[0], censys_records[0], zoomeye_records[0]]


def _phase3_to_10_core_pipeline(first_record) -> dict:
    normalized = ProcessingPipeline().process_record(first_record)
    assert normalized["normalized"] is True
    assert normalized["service"] in {"http", "https", "modbus", "ssh", "ftp", "mqtt"}

    ja3 = build_ja3_string(
        tls_version=771,
        ciphers=[4865, 4866],
        extensions=[0, 11, 10],
        elliptic_curves=[29, 23],
        ec_point_formats=[0],
    )
    fingerprints = {
        "favicon_hash": str(murmurhash3_x86_32(b"favicon-bytes")),
        "ja3": ja3_hash(ja3),
        "jarm": jarm_fingerprint(["tls1.2:4865", "tls1.3:4866", "ext:sni"]),
    }
    assert len(fingerprints["ja3"]) == 32
    assert len(fingerprints["jarm"]) == 64

    clusters = correlate_by_certificate_serial(
        [
            {"certificate_serial": "SERIAL-1", "ip": "198.51.100.10"},
            {"certificate_serial": "SERIAL-1", "ip": "198.51.100.11"},
        ]
    )
    assert len(clusters["SERIAL-1"]) == 2

    geo = geolocate_with_fallback(
        ip=first_record.ip,
        maxmind_result={"country": "AR", "latitude": -31.4, "longitude": -64.2},
        ipinfo_result={},
    )
    assert geo["country"] == "AR"

    device_doc = {
        "device_id": f"{first_record.ip}:{first_record.port}",
        "ip": first_record.ip,
        "organization": first_record.organization,
        "country": geo["country"],
        "latitude": geo["latitude"],
        "longitude": geo["longitude"],
        "exposure_score": 0.0,
        "services": [{"port": first_record.port}],
        "vulnerabilities": [],
        "iot_metadata": {"vendor": "Acme", "model": "Cam-7", "firmware": "1.0.4"},
        "fingerprints": fingerprints,
        "media": {},
    }

    query = OpenSearchQueryService().build_device_query(
        text="camera",
        filters=SearchFilters(asn="AS64500", vendor="Acme", country="AR", exposure_score_min=5.0),
    )
    assert "must" in query["query"]["bool"]

    target_card = build_target_card(device_doc)
    assert target_card["device_id"] == device_doc["device_id"]
    map_points = build_global_exposure_map_points([device_doc])
    assert map_points[0]["ip"] == device_doc["ip"]
    telemetry = build_mining_telemetry(scan_throughput=200.1, probe_latency_ms=50.2, active_discoveries=1)
    assert telemetry["active_discoveries"] == 1

    return device_doc


def _phase4_schema(device_doc: dict) -> None:
    migrated = migrate_legacy_record_to_v1(
        {
            "ip": device_doc["ip"],
            "port": device_doc["services"][0]["port"],
            "banner": "HTTP/1.1 200 OK",
            "organization": device_doc["organization"],
            "country": device_doc["country"],
            "vendor": "Acme",
            "model": "Cam-7",
            "firmware": "1.0.4",
        }
    )
    assert migrated["schema_version"] == 1

    schema = DeviceSchema(
        device_id=device_doc["device_id"],
        ip=device_doc["ip"],
        country=device_doc["country"],
        latitude=float(device_doc["latitude"]),
        longitude=float(device_doc["longitude"]),
        services=[ServiceRecord(port=int(device_doc["services"][0]["port"]), protocol="tcp", banner="HTTP/1.1")],
        vulnerabilities=[VulnerabilityRecord(cve="CVE-2026-1000", severity="high", exploit_available=True)],
    )
    validate_device_schema(schema)


def _phase6_protocols() -> None:
    onvif = ONVIFDiscovery().parse_probe_match(
        ip="203.0.113.50",
        xaddr="http://203.0.113.50/onvif/device_service",
        scopes=["onvif://www.onvif.org/Profile/Streaming"],
    )
    assert "onvif" in onvif.xaddr

    rtsp = RTSPMetadataProbe().parse_options_response(
        ip="203.0.113.50",
        port=554,
        response_headers={"Public": "OPTIONS, DESCRIBE, SETUP", "Server": "RTSPServer/1.0"},
    )
    assert "DESCRIBE" in rtsp.methods

    snmp = SNMPMetadataExtractor(safe_mode=True).extract_from_walk(
        ip="203.0.113.50",
        mib_values={
            "1.3.6.1.2.1.1.5.0": "edge-switch-1",
            "1.3.6.1.2.1.1.1.0": "Switch",
            "1.3.6.1.2.1.1.4.0": "noc@example.com",
        },
    )
    assert snmp.sys_name == "edge-switch-1"


def _phase7_vulnintel(tmp_dir: Path, device_doc: dict) -> dict:
    db_path = tmp_dir / "cve.db"
    mirror = CVEMirrorDB(str(db_path))
    mirror.initialize()
    mirror.upsert(
        CVERecord(
            cve_id="CVE-2026-1000",
            summary="Camera firmware RCE",
            cvss=8.4,
            published_at="2026-03-01",
        )
    )
    cve = mirror.get("CVE-2026-1000")
    assert cve is not None and cve.cvss == 8.4

    mapper = FirmwareMapper()
    mapper.add_mapping("Acme", "Cam-7", "1.0.4", ["CVE-2026-1000"])
    cves = mapper.find_cves("Acme", "Cam-7", "1.0.4")
    assert cves == ["CVE-2026-1000"]

    exploit = has_known_exploit(
        cve_id="CVE-2026-1000",
        cisa_kev={"CVE-2026-1000"},
        exploitdb_links={},
        epss_scores={},
    )
    risk_score = calculate_risk_score(cvss=cve.cvss, epss_probability=0.65, exploit_available=exploit, exposure_level=2.0)
    assert risk_score > 0

    device_doc["vulnerabilities"] = [{"cve": "CVE-2026-1000", "severity": "high", "exploit_available": exploit}]
    device_doc["exposure_score"] = risk_score
    return device_doc


def _phase8_tui(device_doc: dict) -> None:
    tui = NyxeraSpeedTUI()
    assert tui.on_shortcut("v") == "vulnerabilities"
    filtered = tui.filter_records("acme", [device_doc])
    assert len(filtered) == 1
    assert tui.query_from_input("country:AR") == {"country": "AR"}


def _phase10_visualization(device_doc: dict) -> None:
    distribution = build_vulnerability_distribution([device_doc])
    assert distribution["high"] == 1


def _phase11_media(device_doc: dict) -> None:
    capture = SnapshotCapture()
    image = b"\xff\xd8\xff" + (b"A" * 1000)
    metadata = capture.capture_metadata(
        device_id=str(device_doc["device_id"]),
        source_url="http://example/snap.jpg",
        image_bytes=image,
    )
    thumb = capture.build_thumbnail(image, max_bytes=128)
    upload = MinIOThumbnailStore(bucket="snapshots").prepare_upload(
        device_id=metadata.device_id,
        timestamp=metadata.captured_at,
        thumbnail_bytes=thumb,
    )
    assert upload.bucket == "snapshots"
    assert upload.size == 128


def _phase12_adversary() -> None:
    techniques = map_protocols_to_attack_techniques(["modbus", "mqtt"])
    assert "T0859" in techniques and "T0880" in techniques
    signal = detect_deception(
        tcp_jitter_ms_series=[12.0, 18.0, 220.0],
        observed_banners=["Apache", "nginx"],
        response_time_ms_series=[20.0, 21.0, 110.0],
    )
    assert signal.suspicious is True


def _phase13_vision() -> None:
    pipeline = VisionPipeline()
    pipeline.enqueue_snapshot(snapshot_id="snap-1", image_path="/tmp/snap-1.jpg")
    metadata = pipeline.process_next(
        model_output=[
            {"label": "server racks", "confidence": 0.91},
            {"label": "faces", "confidence": 0.61},
        ]
    )
    assert metadata is not None
    assert len(metadata.tags) == 2
    assert validate_dataset_size(500) is True


def _phase14_change_detection(device_doc: dict) -> None:
    engine = DiffEngine()
    prev = [{**device_doc, "vulnerabilities": []}]
    curr = [{**device_doc, "vulnerabilities": [{"cve": "CVE-2026-1000"}]}]
    events = engine.diff(previous_devices=prev, current_devices=curr)
    assert any(event.change_type == "secure_to_vulnerable" for event in events)


def _phase15_security() -> None:
    assert role_allows("admin", "analyst") is True
    tokens = APITokenStore()
    token = tokens.issue_token(subject="operator-1", role="operator")
    assert tokens.verify(token) is not None
    payload = tokens.export_encrypted(master_key="master")
    restored = APITokenStore()
    restored.load_encrypted(payload, master_key="master")
    assert restored.verify(token) is not None

    encrypted = encrypt_secret("hello", "k")
    assert decrypt_secret(encrypted, "k") == "hello"

    limiter = RateLimiter(max_requests=2, window_seconds=10)
    assert limiter.allow("operator-1", now=0.0) is True
    assert limiter.allow("operator-1", now=1.0) is True
    assert limiter.allow("operator-1", now=2.0) is False


def _phase16_observability() -> None:
    metrics = PlatformMetrics(
        queue_depth=5,
        mining_throughput=150.0,
        probe_success_rate=97.5,
        gpu_utilization=61.0,
        storage_growth_gb=0.25,
    )
    prom = export_prometheus(metrics)
    assert "nyxera_queue_depth 5" in prom
    with start_span("full-validation") as span:
        sleep(0.001)
    assert span.duration_ms > 0.0


def run_full_validation() -> None:
    with TemporaryDirectory(prefix="nyxera-eye-e2e-") as temp_dir:
        tmp_dir = Path(temp_dir)
        _phase0_compliance_and_audit(tmp_dir)
        records = _phase2_collectors_and_queue()
        device_doc = _phase3_to_10_core_pipeline(records[0])
        _phase4_schema(device_doc)
        _phase6_protocols()
        device_doc = _phase7_vulnintel(tmp_dir, device_doc)
        _phase8_tui(device_doc)
        _phase10_visualization(device_doc)
        _phase11_media(device_doc)
        _phase12_adversary()
        _phase13_vision()
        _phase14_change_detection(device_doc)
        _phase15_security()
        _phase16_observability()


if __name__ == "__main__":
    run_full_validation()
    print("E2E full roadmap validation passed (local deterministic path).")
