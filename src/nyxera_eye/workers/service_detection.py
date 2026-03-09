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


class ServiceDetectionWorker:
    _PORT_HINTS: dict[int, str] = {
        21: "ftp",
        22: "ssh",
        23: "telnet",
        80: "http",
        443: "https",
        502: "modbus",
        1883: "mqtt",
    }

    def process(self, parsed: dict[str, str | int | None]) -> dict[str, str | int | None]:
        banner = str(parsed.get("banner") or "").lower()
        port = parsed.get("port")
        service = None

        if isinstance(port, int) and port in self._PORT_HINTS:
            service = self._PORT_HINTS[port]

        if "http" in banner:
            service = "http"
        elif "ssh" in banner:
            service = "ssh"
        elif "modbus" in banner:
            service = "modbus"

        enriched = dict(parsed)
        enriched["service"] = service
        return enriched
