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


def calculate_risk_score(cvss: float, epss_probability: float, exploit_available: bool, exposure_level: float) -> float:
    exploit_bonus = 1.5 if exploit_available else 0.0
    return round(cvss + epss_probability * 10.0 + exploit_bonus + exposure_level, 2)
