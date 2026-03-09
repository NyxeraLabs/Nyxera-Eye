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


def calculate_asset_risk_score(cvss: float, vulnerability_count: int, exposure_level: float = 1.0) -> float:
    return round(cvss + vulnerability_count * 0.75 + exposure_level, 2)
