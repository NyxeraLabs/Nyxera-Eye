# Copyright (c) 2026 NyxeraLabs
# Author: Jose Maria Micoli
# Licensed under BSL 1.1
# Change Date: 2033-02-17 -> Apache-2.0
#
# You may:
# - Study
# - Modify
# - Use for internal security testing
#
# You may NOT:
# - Offer as a commercial service
# - Sell derived competing products

ROLE_PRIORITY: dict[str, int] = {
    "viewer": 10,
    "analyst": 20,
    "operator": 30,
    "admin": 40,
}


def role_allows(role: str, required_role: str) -> bool:
    return ROLE_PRIORITY.get(role, -1) >= ROLE_PRIORITY.get(required_role, 10**9)
