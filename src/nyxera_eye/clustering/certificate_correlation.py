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

from collections import defaultdict


def correlate_by_certificate_serial(records: list[dict[str, str]]) -> dict[str, list[str]]:
    """Group observed IPs by TLS certificate serial to track moving infrastructure."""
    clusters: dict[str, list[str]] = defaultdict(list)

    for record in records:
        serial = record.get("certificate_serial", "").strip()
        ip = record.get("ip", "").strip()
        if not serial or not ip:
            continue
        if ip not in clusters[serial]:
            clusters[serial].append(ip)

    return dict(clusters)
