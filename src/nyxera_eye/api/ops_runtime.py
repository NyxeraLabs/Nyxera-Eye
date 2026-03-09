# Copyright (c) 2026 NyxeraLabs
# Author: Jose Maria Micoli
# Licensed under BSL 1.1
# Change Date: 2033-02-17 -> Apache-2.0
#
# You may:
# - Study
# - Modify
# - Use for internal security testing
#
# You may NOT:
# - Offer as a commercial service
# - Sell derived competing products

from __future__ import annotations

from copy import deepcopy
from datetime import UTC, datetime
from random import Random
from threading import Event, Lock, Thread
from time import sleep

from nyxera_eye.fingerprinting import build_web_fingerprint


_CITY_PROFILES = [
    {"city": "Buenos Aires", "country": "AR", "latitude": -34.6037, "longitude": -58.3816},
    {"city": "Cordoba", "country": "AR", "latitude": -31.4201, "longitude": -64.1888},
    {"city": "Sao Paulo", "country": "BR", "latitude": -23.5505, "longitude": -46.6333},
    {"city": "Rio de Janeiro", "country": "BR", "latitude": -22.9068, "longitude": -43.1729},
    {"city": "Mexico City", "country": "MX", "latitude": 19.4326, "longitude": -99.1332},
    {"city": "Bogota", "country": "CO", "latitude": 4.711, "longitude": -74.0721},
    {"city": "Lima", "country": "PE", "latitude": -12.0464, "longitude": -77.0428},
    {"city": "New York", "country": "US", "latitude": 40.7128, "longitude": -74.006},
    {"city": "Los Angeles", "country": "US", "latitude": 34.0522, "longitude": -118.2437},
    {"city": "Chicago", "country": "US", "latitude": 41.8781, "longitude": -87.6298},
    {"city": "San Francisco", "country": "US", "latitude": 37.7749, "longitude": -122.4194},
    {"city": "Toronto", "country": "CA", "latitude": 43.6532, "longitude": -79.3832},
    {"city": "London", "country": "GB", "latitude": 51.5072, "longitude": -0.1276},
    {"city": "Paris", "country": "FR", "latitude": 48.8566, "longitude": 2.3522},
    {"city": "Madrid", "country": "ES", "latitude": 40.4168, "longitude": -3.7038},
    {"city": "Berlin", "country": "DE", "latitude": 52.52, "longitude": 13.405},
    {"city": "Amsterdam", "country": "NL", "latitude": 52.3676, "longitude": 4.9041},
    {"city": "Rome", "country": "IT", "latitude": 41.9028, "longitude": 12.4964},
    {"city": "Istanbul", "country": "TR", "latitude": 41.0082, "longitude": 28.9784},
    {"city": "Moscow", "country": "RU", "latitude": 55.7558, "longitude": 37.6173},
    {"city": "Cairo", "country": "EG", "latitude": 30.0444, "longitude": 31.2357},
    {"city": "Lagos", "country": "NG", "latitude": 6.5244, "longitude": 3.3792},
    {"city": "Johannesburg", "country": "ZA", "latitude": -26.2041, "longitude": 28.0473},
    {"city": "Nairobi", "country": "KE", "latitude": -1.2864, "longitude": 36.8172},
    {"city": "Dubai", "country": "AE", "latitude": 25.2048, "longitude": 55.2708},
    {"city": "Riyadh", "country": "SA", "latitude": 24.7136, "longitude": 46.6753},
    {"city": "Mumbai", "country": "IN", "latitude": 19.076, "longitude": 72.8777},
    {"city": "Delhi", "country": "IN", "latitude": 28.6139, "longitude": 77.209},
    {"city": "Bengaluru", "country": "IN", "latitude": 12.9716, "longitude": 77.5946},
    {"city": "Singapore", "country": "SG", "latitude": 1.3521, "longitude": 103.8198},
    {"city": "Bangkok", "country": "TH", "latitude": 13.7563, "longitude": 100.5018},
    {"city": "Jakarta", "country": "ID", "latitude": -6.2088, "longitude": 106.8456},
    {"city": "Hong Kong", "country": "HK", "latitude": 22.3193, "longitude": 114.1694},
    {"city": "Shanghai", "country": "CN", "latitude": 31.2304, "longitude": 121.4737},
    {"city": "Beijing", "country": "CN", "latitude": 39.9042, "longitude": 116.4074},
    {"city": "Seoul", "country": "KR", "latitude": 37.5665, "longitude": 126.978},
    {"city": "Tokyo", "country": "JP", "latitude": 35.6762, "longitude": 139.6503},
    {"city": "Sydney", "country": "AU", "latitude": -33.8688, "longitude": 151.2093},
    {"city": "Melbourne", "country": "AU", "latitude": -37.8136, "longitude": 144.9631},
]

_SEVERITIES = ["critical", "high", "medium", "low"]
_FINDING_STATUSES = ["open", "in_progress", "acknowledged", "escalated", "closed"]
_EVENT_TYPES = ["state_change", "deception", "vision", "vulnerability"]
_MAX_DEVICE_POOL = 384
_MAX_EVENTS = 512
_MAX_SCAN_HISTORY = 48
_MAX_ACTIONS = 10
_WEB_PROFILES = [
    {
        "server": "nginx/1.25.3",
        "html": """
        <html>
          <head>
            <title>Axis P3225-LV Camera</title>
            <meta name="generator" content="Firmware 10.12.3">
            <meta name="description" content="Axis P3225-LV video stream gateway">
          </head>
        </html>
        """,
        "favicon": b"axis-p3225-lv",
        "service": "https",
        "protocol": "tcp",
        "port": 443,
        "vendor": "Axis",
    },
    {
        "server": "Boa/0.94.14rc21",
        "html": """
        <html>
          <head>
            <title>Moxa NPort 5110A</title>
            <meta name="generator" content="Firmware 3.11">
            <meta name="description" content="Moxa serial device server">
          </head>
        </html>
        """,
        "favicon": b"moxa-nport-5110a",
        "service": "http",
        "protocol": "tcp",
        "port": 80,
        "vendor": "Moxa",
    },
    {
        "server": "lighttpd/1.4.69",
        "html": """
        <html>
          <head>
            <title>Hikvision DS-2CD2143G0-I</title>
            <meta name="generator" content="Firmware v5.7.12">
            <meta property="og:site_name" content="Hikvision Camera">
          </head>
        </html>
        """,
        "favicon": b"hikvision-ds-2cd2143g0-i",
        "service": "https",
        "protocol": "tcp",
        "port": 8443,
        "vendor": "Hikvision",
    },
    {
        "server": "GoAhead-Webs",
        "html": """
        <html>
          <head>
            <title>Siemens S7-1200</title>
            <meta name="description" content="PLC firmware version 4.5.1">
          </head>
        </html>
        """,
        "favicon": b"siemens-s7-1200",
        "service": "http",
        "protocol": "tcp",
        "port": 8080,
        "vendor": "Siemens",
    },
]


def _iso_now() -> str:
    return datetime.now(UTC).isoformat()


def _device_iot_metadata(device: dict) -> dict:
    metadata = device.get("iot_metadata")
    if isinstance(metadata, dict):
        return metadata
    return {}


def _device_network_key(device: dict) -> str:
    return str(device.get("ip") or device.get("device_id") or "")


class OpsRuntimeStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self._generated_at = _iso_now()
        self._devices_by_id: dict[str, dict] = {}
        self._device_order: list[str] = []
        self._findings_by_id: dict[str, dict] = {}
        self._finding_order: list[str] = []
        self._device_finding_map: dict[str, str] = {}
        self._events: list[dict] = []
        self._scan_history: list[dict] = []
        self._scan_runs = 0
        self._cursor = 0
        self._loop_thread: Thread | None = None
        self._loop_stop = Event()
        self._loop_running = False
        self._loop_batch_size = 64
        self._loop_interval_seconds = 10
        self.run_scan(batch_size=64)

    def run_scan(self, batch_size: int = 64) -> dict:
        with self._lock:
            self._scan_runs += 1
            now = _iso_now()
            rnd = Random(self._scan_runs * 7919)

            for offset in range(max(1, batch_size)):
                slot = (self._cursor + offset) % _MAX_DEVICE_POOL
                profile = _WEB_PROFILES[slot % len(_WEB_PROFILES)]
                web_fingerprint = build_web_fingerprint(
                    server_header=str(profile["server"]),
                    html=str(profile["html"]),
                    favicon_bytes=bytes(profile["favicon"]),
                )
                device = self._build_device(slot=slot, rnd=rnd, now=now, profile=profile, web_fingerprint=web_fingerprint)
                self._upsert_device(device)
                self._upsert_finding(device=device, now=now)
                self._maybe_append_event(device=device, rnd=rnd, now=now)

            self._cursor = (self._cursor + max(1, batch_size)) % _MAX_DEVICE_POOL
            self._generated_at = now
            self._scan_history.append(
                {
                    "run": self._scan_runs,
                    "timestamp": self._generated_at,
                    "devices": len(self._devices_by_id),
                    "findings": len(self._findings_by_id),
                    "events": len(self._events),
                }
            )
            self._scan_history = self._scan_history[-_MAX_SCAN_HISTORY:]
            return self._snapshot_unlocked()

    def _build_device(
        self,
        *,
        slot: int,
        rnd: Random,
        now: str,
        profile: dict,
        web_fingerprint: dict,
    ) -> dict:
        city_profile = _CITY_PROFILES[slot % len(_CITY_PROFILES)]
        severity = _SEVERITIES[(slot + self._scan_runs + rnd.randint(0, 3)) % len(_SEVERITIES)]
        lat = round(float(city_profile["latitude"]) + (((slot % 5) - 2) * 0.012) + rnd.uniform(-0.006, 0.006), 4)
        lon = round(float(city_profile["longitude"]) + (((slot % 5) - 2) * 0.012) + rnd.uniform(-0.006, 0.006), 4)
        host_major = 16 + (slot // 200)
        host_minor = (slot % 200) + 10
        ip = f"172.{host_major}.{slot % 250}.{host_minor}"
        device_id = f"dev-{host_major:03d}-{slot % 250:03d}-{host_minor:03d}"
        return {
            "device_id": device_id,
            "name": f"{city_profile['city']} Edge Asset {slot:03d}",
            "ip": ip,
            "country": str(city_profile["country"]),
            "city": str(city_profile["city"]),
            "latitude": lat,
            "longitude": lon,
            "severity": severity,
            "services": [
                {
                    "port": int(profile["port"]),
                    "protocol": str(profile["protocol"]),
                    "service": str(profile["service"]),
                    "banner": str(profile["server"]),
                }
            ],
            "fingerprints": {
                "favicon_hash": web_fingerprint["favicon_hash"],
                "http_server": web_fingerprint["http_server"],
                "html_title": web_fingerprint["html_title"],
                "html_metadata": web_fingerprint["html_metadata"],
            },
            "iot_metadata": {
                "vendor": str(profile.get("vendor", "")),
                "model": web_fingerprint["model_hint"],
                "firmware": web_fingerprint["firmware_hint"],
            },
            "first_seen": now,
            "last_seen": now,
            "last_updated": now,
            "scan_count": 1,
        }

    def _upsert_device(self, device: dict) -> None:
        canonical_id = _device_network_key(device)
        device["device_id"] = canonical_id
        existing = self._devices_by_id.get(canonical_id)
        if existing is None:
            self._devices_by_id[canonical_id] = deepcopy(device)
            if canonical_id not in self._device_order:
                self._device_order.append(canonical_id)
            return

        existing.update(
            {
                "name": device["name"],
                "ip": device["ip"],
                "country": device["country"],
                "city": device["city"],
                "latitude": device["latitude"],
                "longitude": device["longitude"],
                "severity": device["severity"],
                "services": deepcopy(device["services"]),
                "fingerprints": deepcopy(device["fingerprints"]),
                "iot_metadata": deepcopy(device["iot_metadata"]),
                "last_seen": device["last_seen"],
                "last_updated": device["last_updated"],
                "scan_count": int(existing.get("scan_count", 0)) + 1,
            }
        )

    def _upsert_finding(self, *, device: dict, now: str) -> None:
        device_id = _device_network_key(device)
        finding_id = self._device_finding_map.get(device_id, f"f-{device_id}")
        finding = self._findings_by_id.get(finding_id)
        description = f"Accumulated scan activity detected {device['severity']} exposure posture on asset {device_id}."

        if finding is None:
            finding = {
                "id": finding_id,
                "title": f"{str(device['severity']).upper()} exposure signature",
                "description": description,
                "severity": device["severity"],
                "device_id": device_id,
                "status": "open",
                "actions": [],
                "updated_at": now,
            }
            self._findings_by_id[finding_id] = finding
            self._finding_order.append(finding_id)
            self._device_finding_map[device_id] = finding_id
            return

        finding["title"] = f"{str(device['severity']).upper()} exposure signature"
        finding["description"] = description
        finding["severity"] = device["severity"]
        finding["device_id"] = device_id
        finding["updated_at"] = now
        if finding.get("status") == "closed" and str(device["severity"]) in {"critical", "high"}:
            finding["status"] = "open"

    def _maybe_append_event(self, *, device: dict, rnd: Random, now: str) -> None:
        if rnd.random() <= 0.34:
            return
        event_type = _EVENT_TYPES[(len(self._events) + self._scan_runs) % len(_EVENT_TYPES)]
        self._events.append(
            {
                "id": f"evt-{self._scan_runs}-{device['device_id']}",
                "title": f"{event_type.replace('_', ' ').title()} detected",
                "device_id": device["device_id"],
                "lat": device["latitude"],
                "lon": device["longitude"],
                "severity": device["severity"],
                "type": event_type,
                "timestamp": now,
            }
        )
        self._events = self._events[-_MAX_EVENTS:]

    def snapshot(self) -> dict:
        with self._lock:
            return self._snapshot_unlocked()

    def _snapshot_unlocked(self) -> dict:
        devices: list[dict] = []
        seen_network_keys: set[str] = set()
        for device_id in self._device_order:
            device = deepcopy(self._devices_by_id[device_id])
            network_key = _device_network_key(device)
            if network_key in seen_network_keys:
                continue
            seen_network_keys.add(network_key)
            devices.append(device)
        findings = [deepcopy(self._findings_by_id[finding_id]) for finding_id in self._finding_order]
        severity_counts: dict[str, int] = {level: 0 for level in _SEVERITIES}
        status_counts: dict[str, int] = {status: 0 for status in _FINDING_STATUSES}
        country_counts: dict[str, int] = {}
        vendor_counts: dict[str, int] = {}
        port_counts: dict[str, int] = {}

        for finding in findings:
            severity = str(finding.get("severity", "low"))
            status = str(finding.get("status", "open"))
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
            status_counts[status] = status_counts.get(status, 0) + 1

        for device in devices:
            country = str(device.get("country", "N/A"))
            vendor = str(_device_iot_metadata(device).get("vendor", "Unknown") or "Unknown")
            country_counts[country] = country_counts.get(country, 0) + 1
            vendor_counts[vendor] = vendor_counts.get(vendor, 0) + 1
            for service in device.get("services", []):
                port_key = str(service.get("port", "0"))
                port_counts[port_key] = port_counts.get(port_key, 0) + 1

        top_vendors = sorted(vendor_counts.items(), key=lambda item: (-item[1], item[0]))[:6]
        top_ports = sorted(port_counts.items(), key=lambda item: (-item[1], int(item[0])))[:8]

        return {
            "generated_at": self._generated_at,
            "devices": devices,
            "events": deepcopy(self._events),
            "findings": findings,
            "metrics": {
                "queue_depth": max(0, len(devices) // 5),
                "mining_throughput": round(max(1.0, len(devices) * 2.75), 2),
                "probe_success_rate": round(min(99.5, 84.0 + (len(self._events) / max(1, len(devices))) * 11.5), 2),
                "storage_growth_gb": round((len(findings) * 0.028) + (len(self._events) * 0.004), 3),
                "scan_runs": self._scan_runs,
                "findings_by_severity": severity_counts,
                "findings_by_status": status_counts,
                "devices_by_country": country_counts,
                "devices_by_vendor": {vendor: count for vendor, count in top_vendors},
                "services_by_port": {port: count for port, count in top_ports},
                "scan_history": list(self._scan_history),
                "scan_loop_running": self._loop_running,
                "scan_loop_batch_size": self._loop_batch_size,
                "scan_loop_interval_seconds": self._loop_interval_seconds,
            },
            "source": "api-runtime",
        }

    def start_scan_loop(self, batch_size: int = 96, interval_seconds: int = 10) -> bool:
        with self._lock:
            if self._loop_running:
                return False
            self._loop_batch_size = max(1, batch_size)
            self._loop_interval_seconds = max(1, interval_seconds)
            self._loop_stop.clear()
            self._loop_running = True

        def _runner() -> None:
            try:
                while not self._loop_stop.is_set():
                    self.run_scan(batch_size=self._loop_batch_size)
                    for _ in range(self._loop_interval_seconds):
                        if self._loop_stop.is_set():
                            break
                        sleep(1)
            finally:
                with self._lock:
                    self._loop_running = False
                    self._loop_thread = None

        thread = Thread(target=_runner, daemon=True, name="nyxera-scan-loop")
        with self._lock:
            self._loop_thread = thread
        thread.start()
        return True

    def stop_scan_loop(self) -> bool:
        with self._lock:
            if not self._loop_running:
                return False
            self._loop_stop.set()
            thread = self._loop_thread

        if thread is not None:
            thread.join(timeout=2.0)
        with self._lock:
            self._loop_running = False
            self._loop_thread = None
        return True

    def scan_loop_status(self) -> dict:
        with self._lock:
            return {
                "running": self._loop_running,
                "batch_size": self._loop_batch_size,
                "interval_seconds": self._loop_interval_seconds,
            }

    def finding_action(self, finding_id: str, action: str) -> dict | None:
        with self._lock:
            finding = self._findings_by_id.get(finding_id)
            if finding is None:
                return None
            actions = list(finding.get("actions", []))
            actions.append({"action": action, "at": _iso_now()})
            finding["actions"] = actions[-_MAX_ACTIONS:]
            finding["updated_at"] = _iso_now()
            if action == "escalate":
                finding["status"] = "escalated"
            elif action in {"investigate", "open_device"}:
                finding["status"] = "in_progress"
            elif action == "ack":
                finding["status"] = "acknowledged"
            elif action == "close":
                finding["status"] = "closed"
            device = self._devices_by_id.get(str(finding.get("device_id", "")))
            payload = deepcopy(finding)
            if device is not None:
                payload["device"] = deepcopy(device)
            return payload

    def get_finding(self, finding_id: str) -> dict | None:
        with self._lock:
            finding = self._findings_by_id.get(finding_id)
            if finding is None:
                return None
            payload = deepcopy(finding)
            device = self._devices_by_id.get(str(finding.get("device_id", "")))
            if device is not None:
                payload["device"] = deepcopy(device)
            return payload

    def list_findings(
        self,
        *,
        q: str | None = None,
        severity: str | None = None,
        status: str | None = None,
        device_id: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        with self._lock:
            query = (q or "").strip().lower()
            items: list[dict] = []
            for finding_id in self._finding_order:
                finding = self._findings_by_id[finding_id]
                if severity and str(finding.get("severity")) != severity:
                    continue
                if status and str(finding.get("status")) != status:
                    continue
                if device_id and str(finding.get("device_id")) != device_id:
                    continue
                if query:
                    haystack = " ".join(
                        [
                            str(finding.get("id", "")),
                            str(finding.get("title", "")),
                            str(finding.get("description", "")),
                            str(finding.get("device_id", "")),
                        ]
                    ).lower()
                    if query not in haystack:
                        continue
                items.append(deepcopy(finding))

            total = len(items)
            start = max(0, offset)
            end = start + max(1, min(limit, 500))
            return {"items": items[start:end], "total": total, "offset": start, "limit": max(1, min(limit, 500))}

    def get_device(self, device_id: str) -> dict | None:
        with self._lock:
            device = self._devices_by_id.get(device_id)
            if device is None:
                return None
            payload = deepcopy(device)
            finding_id = self._device_finding_map.get(device_id)
            if finding_id and finding_id in self._findings_by_id:
                payload["finding"] = deepcopy(self._findings_by_id[finding_id])
            payload["events"] = [deepcopy(event) for event in self._events if str(event.get("device_id")) == device_id][-20:]
            return payload

    def list_devices(
        self,
        *,
        q: str | None = None,
        severity: str | None = None,
        country: str | None = None,
        vendor: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        with self._lock:
            query = (q or "").strip().lower()
            items: list[dict] = []
            for device_id in self._device_order:
                device = self._devices_by_id[device_id]
                if _device_network_key(device) != device_id:
                    continue
                metadata = _device_iot_metadata(device)
                device_vendor = str(metadata.get("vendor", ""))
                if severity and str(device.get("severity")) != severity:
                    continue
                if country and str(device.get("country")) != country:
                    continue
                if vendor and device_vendor != vendor:
                    continue
                if query:
                    haystack = " ".join(
                        [
                            str(device.get("device_id", "")),
                            str(device.get("name", "")),
                            str(device.get("ip", "")),
                            str(device.get("country", "")),
                            device_vendor,
                            str(metadata.get("model", "")),
                            str(metadata.get("firmware", "")),
                        ]
                    ).lower()
                    if query not in haystack:
                        continue
                items.append(deepcopy(device))

            total = len(items)
            start = max(0, offset)
            end = start + max(1, min(limit, 500))
            return {"items": items[start:end], "total": total, "offset": start, "limit": max(1, min(limit, 500))}


ops_runtime_store = OpsRuntimeStore()
