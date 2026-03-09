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

from nyxera_eye.vulnintel.cve_mirror import CVEMirrorDB, CVERecord
from nyxera_eye.vulnintel.exploit_detection import has_known_exploit
from nyxera_eye.vulnintel.firmware_mapping import FirmwareMapper
from nyxera_eye.vulnintel.risk_score import calculate_risk_score

__all__ = [
    "CVEMirrorDB",
    "CVERecord",
    "has_known_exploit",
    "FirmwareMapper",
    "calculate_risk_score",
]
