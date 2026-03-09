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

import sqlite3
from pathlib import Path

from internal.database.models.coverage import CoverageRecord


class CoverageRepository:
    def __init__(self, db_path: str = "data/coverage.db") -> None:
        self.db_path = db_path

    def initialize(self) -> None:
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS scan_coverage (
                    target_id TEXT PRIMARY KEY,
                    last_scan_at REAL NOT NULL,
                    priority INTEGER NOT NULL
                )
                """
            )
            conn.commit()

    def upsert(self, record: CoverageRecord) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO scan_coverage (target_id, last_scan_at, priority)
                VALUES (?, ?, ?)
                ON CONFLICT(target_id) DO UPDATE SET
                    last_scan_at=excluded.last_scan_at,
                    priority=excluded.priority
                """,
                (record.target_id, record.last_scan_at, record.priority),
            )
            conn.commit()

    def get(self, target_id: str) -> CoverageRecord | None:
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT target_id, last_scan_at, priority FROM scan_coverage WHERE target_id = ?",
                (target_id,),
            ).fetchone()
        if row is None:
            return None
        return CoverageRecord(target_id=row[0], last_scan_at=float(row[1]), priority=int(row[2]))
