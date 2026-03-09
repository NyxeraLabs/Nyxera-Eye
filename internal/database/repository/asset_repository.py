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

from internal.database.models.asset import AssetFingerprintRecord, AssetRecord


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
                    favicon_hash TEXT,
                    http_server TEXT,
                    html_title TEXT,
                    html_metadata TEXT NOT NULL DEFAULT '{}',
                    model_hint TEXT,
                    firmware_hint TEXT
                )
                """
            )
            columns = {
                row[1]
                for row in conn.execute("PRAGMA table_info(assets)").fetchall()
            }
            if "vendor" not in columns:
                conn.execute("ALTER TABLE assets ADD COLUMN vendor TEXT")
            conn.commit()

    def upsert(self, record: AssetRecord) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO assets (
                    asset_id,
                    ip,
                    vendor,
                    favicon_hash,
                    http_server,
                    html_title,
                    html_metadata,
                    model_hint,
                    firmware_hint
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(asset_id) DO UPDATE SET
                    ip=excluded.ip,
                    vendor=excluded.vendor,
                    favicon_hash=excluded.favicon_hash,
                    http_server=excluded.http_server,
                    html_title=excluded.html_title,
                    html_metadata=excluded.html_metadata,
                    model_hint=excluded.model_hint,
                    firmware_hint=excluded.firmware_hint
                """,
                (
                    record.asset_id,
                    record.ip,
                    record.vendor,
                    record.fingerprint.favicon_hash,
                    record.fingerprint.http_server,
                    record.fingerprint.html_title,
                    json.dumps(record.fingerprint.html_metadata, sort_keys=True),
                    record.fingerprint.model_hint,
                    record.fingerprint.firmware_hint,
                ),
            )
            conn.commit()

    def get(self, asset_id: str) -> AssetRecord | None:
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                """
                SELECT asset_id, ip, vendor, favicon_hash, http_server, html_title, html_metadata, model_hint, firmware_hint
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
            fingerprint=AssetFingerprintRecord(
                favicon_hash=row[3],
                http_server=row[4],
                html_title=row[5],
                html_metadata=json.loads(row[6]) if row[6] else {},
                model_hint=row[7],
                firmware_hint=row[8],
            ),
        )
