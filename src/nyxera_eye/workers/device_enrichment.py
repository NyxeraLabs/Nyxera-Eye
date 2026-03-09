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


class DeviceEnrichmentWorker:
    _RISK_BY_SERVICE: dict[str, str] = {
        "telnet": "high",
        "modbus": "high",
        "ftp": "medium",
        "http": "medium",
        "https": "low",
        "ssh": "low",
        "mqtt": "medium",
    }

    def process(self, detected: dict[str, str | int | None]) -> dict[str, str | int | None]:
        service = detected.get("service")
        risk = self._RISK_BY_SERVICE.get(str(service), "unknown")

        result = dict(detected)
        result["risk_profile"] = risk
        result["normalized"] = True
        return result
