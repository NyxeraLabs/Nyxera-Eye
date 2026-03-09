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

import hashlib


def jarm_fingerprint(probe_results: list[str]) -> str:
    """Build a deterministic infrastructure fingerprint from TLS probe outputs."""
    canonical = "|".join(item.strip() for item in probe_results)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
