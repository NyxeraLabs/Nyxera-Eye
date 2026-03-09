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

from internal.intel.vulnerabilities.lookup import CVERecord, VulnerabilityLookupEngine
from internal.intel.vulnerabilities.risk import calculate_asset_risk_score

__all__ = ["CVERecord", "VulnerabilityLookupEngine", "calculate_asset_risk_score"]
