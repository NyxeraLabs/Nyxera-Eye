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

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from internal.database.models.asset import (
    AssetFingerprintRecord,
    AssetRecord,
    AssetScanHistoryRecord,
    AssetServiceRecord,
    AssetVulnerabilityRecord,
)


class AssetRepository:
    def __init__(self, db_path: str = "data/assets.db") -> None:
        self.db_path = db_path

    def initialize(self) -> None:
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS assets (
                    asset_id TEXT PRIMARY KEY,
                    ip TEXT NOT NULL,
                    vendor TEXT,
                    risk_score REAL,
                    scan_count INTEGER NOT NULL DEFAULT 0,
                    first_seen REAL,
                    last_seen REAL,
                    last_updated REAL,
                    configuration_hash TEXT,
                    configuration_changed INTEGER NOT NULL DEFAULT 0,
                    favicon_hash TEXT,
                    http_server TEXT,
                    html_title TEXT,
                    html_metadata TEXT NOT NULL DEFAULT '{}',
                    model_hint TEXT,
                    firmware_hint TEXT,
                    services TEXT NOT NULL DEFAULT '[]',
                    vulnerabilities TEXT NOT NULL DEFAULT '[]'
                )
                """
            )
            columns = {
                row[1]
                for row in conn.execute("PRAGMA table_info(assets)").fetchall()
            }
            if "vendor" not in columns:
                conn.execute("ALTER TABLE assets ADD COLUMN vendor TEXT")
            if "risk_score" not in columns:
                conn.execute("ALTER TABLE assets ADD COLUMN risk_score REAL")
            if "scan_count" not in columns:
                conn.execute("ALTER TABLE assets ADD COLUMN scan_count INTEGER NOT NULL DEFAULT 0")
            if "first_seen" not in columns:
                conn.execute("ALTER TABLE assets ADD COLUMN first_seen REAL")
            if "last_seen" not in columns:
                conn.execute("ALTER TABLE assets ADD COLUMN last_seen REAL")
            if "last_updated" not in columns:
                conn.execute("ALTER TABLE assets ADD COLUMN last_updated REAL")
            if "configuration_hash" not in columns:
                conn.execute("ALTER TABLE assets ADD COLUMN configuration_hash TEXT")
            if "configuration_changed" not in columns:
                conn.execute("ALTER TABLE assets ADD COLUMN configuration_changed INTEGER NOT NULL DEFAULT 0")
            if "services" not in columns:
                conn.execute("ALTER TABLE assets ADD COLUMN services TEXT NOT NULL DEFAULT '[]'")
            if "vulnerabilities" not in columns:
                conn.execute("ALTER TABLE assets ADD COLUMN vulnerabilities TEXT NOT NULL DEFAULT '[]'")
            conn.commit()

    def upsert(self, record: AssetRecord) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO assets (
                    asset_id,
                    ip,
                    vendor,
                    risk_score,
                    scan_count,
                    first_seen,
                    last_seen,
                    last_updated,
                    configuration_hash,
                    configuration_changed,
                    favicon_hash,
                    http_server,
                    html_title,
                    html_metadata,
                    model_hint,
                    firmware_hint,
                    services,
                    vulnerabilities
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(asset_id) DO UPDATE SET
                    ip=excluded.ip,
                    vendor=excluded.vendor,
                    risk_score=excluded.risk_score,
                    scan_count=excluded.scan_count,
                    first_seen=excluded.first_seen,
                    last_seen=excluded.last_seen,
                    last_updated=excluded.last_updated,
                    configuration_hash=excluded.configuration_hash,
                    configuration_changed=excluded.configuration_changed,
                    favicon_hash=excluded.favicon_hash,
                    http_server=excluded.http_server,
                    html_title=excluded.html_title,
                    html_metadata=excluded.html_metadata,
                    model_hint=excluded.model_hint,
                    firmware_hint=excluded.firmware_hint,
                    services=excluded.services,
                    vulnerabilities=excluded.vulnerabilities
                """,
                (
                    record.asset_id,
                    record.ip,
                    record.vendor,
                    record.risk_score,
                    record.scan_count,
                    record.first_seen,
                    record.last_seen,
                    record.last_updated,
                    record.configuration_hash,
                    int(record.configuration_changed),
                    record.fingerprint.favicon_hash,
                    record.fingerprint.http_server,
                    record.fingerprint.html_title,
                    json.dumps(record.fingerprint.html_metadata, sort_keys=True),
                    record.fingerprint.model_hint,
                    record.fingerprint.firmware_hint,
                    json.dumps(
                        [
                            {
                                "port": item.port,
                                "protocol": item.protocol,
                                "service": item.service,
                                "version": item.version,
                                "banner": item.banner,
                            }
                            for item in record.services
                        ],
                        sort_keys=True,
                    ),
                    json.dumps(
                        [
                            {
                                "cve_id": item.cve_id,
                                "service": item.service,
                                "version": item.version,
                                "severity": item.severity,
                                "summary": item.summary,
                                "cvss": item.cvss,
                            }
                            for item in record.vulnerabilities
                        ],
                        sort_keys=True,
                    ),
                ),
            )
            conn.commit()

    def get(self, asset_id: str) -> AssetRecord | None:
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                """
                SELECT asset_id, ip, vendor, risk_score, scan_count, first_seen, last_seen, last_updated, configuration_hash, configuration_changed, favicon_hash, http_server, html_title, html_metadata, model_hint, firmware_hint, services, vulnerabilities
                FROM assets
                WHERE asset_id = ?
                """,
                (asset_id,),
            ).fetchone()

        if row is None:
            return None

        return AssetRecord(
            asset_id=row[0],
            ip=row[1],
            vendor=row[2],
            risk_score=float(row[3]) if row[3] is not None else None,
            scan_count=int(row[4] or 0),
            first_seen=float(row[5]) if row[5] is not None else None,
            last_seen=float(row[6]) if row[6] is not None else None,
            last_updated=float(row[7]) if row[7] is not None else None,
            configuration_hash=row[8],
            configuration_changed=bool(row[9]),
            fingerprint=AssetFingerprintRecord(
                favicon_hash=row[10],
                http_server=row[11],
                html_title=row[12],
                html_metadata=json.loads(row[13]) if row[13] else {},
                model_hint=row[14],
                firmware_hint=row[15],
            ),
            services=[
                AssetServiceRecord(
                    port=int(item["port"]),
                    protocol=item["protocol"],
                    service=item["service"],
                    version=item["version"],
                    banner=item.get("banner"),
                )
                for item in json.loads(row[16] or "[]")
            ],
            vulnerabilities=[
                AssetVulnerabilityRecord(
                    cve_id=item["cve_id"],
                    service=item["service"],
                    version=item["version"],
                    severity=item["severity"],
                    summary=item["summary"],
                    cvss=float(item["cvss"]),
                )
                for item in json.loads(row[17] or "[]")
            ],
            scan_history=[],
        )

    def get_by_ip(self, ip: str) -> AssetRecord | None:
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT asset_id FROM assets WHERE ip = ?",
                (ip,),
            ).fetchone()
        if row is None:
            return None
        return self.get(str(row[0]))
