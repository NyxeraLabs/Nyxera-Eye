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

import sqlite3
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class CVERecord:
    cve_id: str
    summary: str
    cvss: float
    published_at: str


class CVEMirrorDB:
    def __init__(self, db_path: str = "data/cve_mirror.db") -> None:
        self.db_path = db_path

    def initialize(self) -> None:
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS cve_records (
                    cve_id TEXT PRIMARY KEY,
                    summary TEXT NOT NULL,
                    cvss REAL NOT NULL,
                    published_at TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def upsert(self, record: CVERecord) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO cve_records (cve_id, summary, cvss, published_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(cve_id) DO UPDATE SET
                    summary=excluded.summary,
                    cvss=excluded.cvss,
                    published_at=excluded.published_at
                """,
                (record.cve_id, record.summary, record.cvss, record.published_at),
            )
            conn.commit()

    def get(self, cve_id: str) -> CVERecord | None:
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT cve_id, summary, cvss, published_at FROM cve_records WHERE cve_id = ?",
                (cve_id,),
            ).fetchone()

        if row is None:
            return None

        return CVERecord(
            cve_id=row[0],
            summary=row[1],
            cvss=float(row[2]),
            published_at=row[3],
        )
