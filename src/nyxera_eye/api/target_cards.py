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


def build_target_card(document: dict) -> dict[str, str | float | int | None]:
    services = document.get("services", [])

    return {
        "device_id": document.get("device_id"),
        "ip": document.get("ip"),
        "organization": document.get("organization"),
        "country": document.get("country"),
        "exposure_score": document.get("exposure_score"),
        "service_count": len(services),
        "top_vulnerability": (document.get("vulnerabilities") or [{}])[0].get("cve"),
    }
