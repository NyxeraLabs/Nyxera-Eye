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

from datetime import UTC, datetime
from random import Random
from threading import Event, Lock, Thread
from time import sleep

from nyxera_eye.fingerprinting import build_web_fingerprint


_COUNTRIES = [
    ("AR", -31.42, -64.19),
    ("US", 37.77, -122.41),
    ("DE", 52.52, 13.41),
    ("JP", 35.68, 139.69),
    ("GB", 51.50, -0.12),
    ("BR", -23.55, -46.63),
    ("IN", 19.07, 72.87),
    ("ZA", -26.20, 28.04),
]

_SEVERITIES = ["critical", "high", "medium", "low"]
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
    },
]


def _iso_now() -> str:
    return datetime.now(UTC).isoformat()


class OpsRuntimeStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self._generated_at = _iso_now()
        self._devices: list[dict] = []
        self._events: list[dict] = []
        self._findings: list[dict] = []
        self._scan_history: list[dict] = []
        self._scan_runs = 0
        self._loop_thread: Thread | None = None
        self._loop_stop = Event()
        self._loop_running = False
        self._loop_batch_size = 64
        self._loop_interval_seconds = 10
        self.run_scan(batch_size=64)

    def run_scan(self, batch_size: int = 64) -> dict:
        with self._lock:
            self._scan_runs += 1
            seed = int(datetime.now(UTC).timestamp()) + self._scan_runs * 13
            rnd = Random(seed)

            devices: list[dict] = []
            findings: list[dict] = []
            events: list[dict] = []

            for idx in range(max(1, batch_size)):
                country, base_lat, base_lon = _COUNTRIES[idx % len(_COUNTRIES)]
                severity = _SEVERITIES[rnd.randint(0, len(_SEVERITIES) - 1)]
                ip = f"100.{(idx * 7) % 250}.{(idx * 11) % 250}.{(10 + idx) % 250}"
                device_id = f"dev-{self._scan_runs}-{idx}"
                profile = _WEB_PROFILES[idx % len(_WEB_PROFILES)]
                web_fingerprint = build_web_fingerprint(
                    server_header=str(profile["server"]),
                    html=str(profile["html"]),
                    favicon_bytes=bytes(profile["favicon"]),
                )

                lat = round(base_lat + rnd.uniform(-0.9, 0.9), 4)
                lon = round(base_lon + rnd.uniform(-0.9, 0.9), 4)

                devices.append(
                    {
                        "device_id": device_id,
                        "name": f"Edge-Asset-{idx:03d}",
                        "ip": ip,
                        "country": country,
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
                            "vendor": None,
                            "model": web_fingerprint["model_hint"],
                            "firmware": web_fingerprint["firmware_hint"],
                        },
                    }
                )

                findings.append(
                    {
                        "id": f"f-{self._scan_runs}-{idx}",
                        "title": f"{severity.upper()} exposure signature",
                        "description": f"Scan detected {severity} posture on asset {device_id}.",
                        "severity": severity,
                        "device_id": device_id,
                        "status": "open",
                        "actions": [],
                        "updated_at": _iso_now(),
                    }
                )

                if rnd.random() > 0.38:
                    event_type = rnd.choice(["state_change", "deception", "vision", "vulnerability"])
                    events.append(
                        {
                            "id": f"evt-{self._scan_runs}-{idx}",
                            "title": f"{event_type.replace('_', ' ').title()} detected",
                            "device_id": device_id,
                            "lat": lat,
                            "lon": lon,
                            "severity": severity,
                            "type": event_type,
                            "timestamp": _iso_now(),
                        }
                    )

            self._devices = devices
            self._events = events
            self._findings = findings
            self._generated_at = _iso_now()
            self._scan_history.append(
                {
                    "run": self._scan_runs,
                    "timestamp": self._generated_at,
                    "devices": len(self._devices),
                    "findings": len(self._findings),
                    "events": len(self._events),
                }
            )
            self._scan_history = self._scan_history[-24:]
            return self._snapshot_unlocked()

    def snapshot(self) -> dict:
        with self._lock:
            return self._snapshot_unlocked()

    def _snapshot_unlocked(self) -> dict:
        severity_counts: dict[str, int] = {level: 0 for level in _SEVERITIES}
        country_counts: dict[str, int] = {}

        for finding in self._findings:
            severity_counts[str(finding.get("severity", "low"))] = severity_counts.get(
                str(finding.get("severity", "low")), 0
            ) + 1
        for device in self._devices:
            country = str(device.get("country", "N/A"))
            country_counts[country] = country_counts.get(country, 0) + 1

        return {
            "generated_at": self._generated_at,
            "devices": list(self._devices),
            "events": list(self._events),
            "findings": list(self._findings),
            "metrics": {
                "queue_depth": max(0, int(len(self._devices) * 0.22)),
                "mining_throughput": round(max(1.0, len(self._devices) * 3.9), 2),
                "probe_success_rate": round(86.0 + (len(self._events) / max(1, len(self._devices))) * 14.0, 2),
                "storage_growth_gb": round(len(self._findings) * 0.041, 3),
                "scan_runs": self._scan_runs,
                "findings_by_severity": severity_counts,
                "devices_by_country": country_counts,
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
            for finding in self._findings:
                if finding.get("id") != finding_id:
                    continue
                actions = list(finding.get("actions", []))
                actions.append({"action": action, "at": _iso_now()})
                finding["actions"] = actions[-10:]
                finding["updated_at"] = _iso_now()
                if action == "escalate":
                    finding["status"] = "escalated"
                elif action == "investigate":
                    finding["status"] = "in_progress"
                elif action == "ack":
                    finding["status"] = "acknowledged"
                elif action == "close":
                    finding["status"] = "closed"
                return dict(finding)
            return None

    def get_finding(self, finding_id: str) -> dict | None:
        with self._lock:
            for finding in self._findings:
                if finding.get("id") == finding_id:
                    return dict(finding)
            return None


ops_runtime_store = OpsRuntimeStore()
