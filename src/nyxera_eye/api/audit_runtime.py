from __future__ import annotations

from datetime import UTC, datetime
import json
import os
from pathlib import Path
from threading import Lock
from uuid import uuid4


def _iso_now() -> str:
    return datetime.now(UTC).isoformat()


class AuditRuntimeStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self._events: list[dict] = []
        self._max_events = int(os.getenv("NYXERA_AUDIT_MAX_EVENTS", "5000"))
        self._log_path = Path(os.getenv("NYXERA_AUDIT_LOG_PATH", ".run/audit-events.jsonl"))
        self._log_path.parent.mkdir(parents=True, exist_ok=True)

    def append(
        self,
        *,
        actor: str,
        action: str,
        status: str,
        method: str,
        path: str,
        ip: str,
        details: dict | None = None,
    ) -> dict:
        event = {
            "id": str(uuid4()),
            "timestamp": _iso_now(),
            "actor": actor,
            "action": action,
            "status": status,
            "method": method,
            "path": path,
            "ip": ip,
            "details": details or {},
        }
        serialized = json.dumps(event, separators=(",", ":"), sort_keys=True)

        with self._lock:
            self._events.append(event)
            self._events = self._events[-self._max_events :]
            with self._log_path.open("a", encoding="utf-8") as fh:
                fh.write(serialized + "\n")
        return event

    def recent(self, limit: int = 200) -> list[dict]:
        with self._lock:
            bounded = max(1, min(limit, 2000))
            return list(reversed(self._events[-bounded:]))


audit_runtime_store = AuditRuntimeStore()
