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

from nyxera_eye.adversary.attack_mapping import map_protocols_to_attack_techniques
from nyxera_eye.adversary.deception_detection import DeceptionSignal, detect_deception

__all__ = [
    "DeceptionSignal",
    "detect_deception",
    "map_protocols_to_attack_techniques",
]
