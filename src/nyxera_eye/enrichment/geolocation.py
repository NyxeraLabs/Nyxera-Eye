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


def geolocate_with_fallback(ip: str, maxmind_result: dict | None, ipinfo_result: dict | None) -> dict[str, float | str | None]:
    """Prefer MaxMind data and fallback to IPInfo when fields are missing."""
    maxmind_result = maxmind_result or {}
    ipinfo_result = ipinfo_result or {}

    return {
        "ip": ip,
        "country": maxmind_result.get("country") or ipinfo_result.get("country"),
        "latitude": maxmind_result.get("latitude") or ipinfo_result.get("latitude"),
        "longitude": maxmind_result.get("longitude") or ipinfo_result.get("longitude"),
        "source": "maxmind" if maxmind_result else "ipinfo",
    }
