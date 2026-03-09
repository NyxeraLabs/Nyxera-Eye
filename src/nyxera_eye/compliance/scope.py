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

from dataclasses import dataclass, field
from ipaddress import ip_address, ip_network


@dataclass(slots=True)
class ScopePolicy:
    allowed_cidrs: list[str] = field(default_factory=list)

    def add_cidr(self, cidr: str) -> None:
        ip_network(cidr, strict=False)
        if cidr not in self.allowed_cidrs:
            self.allowed_cidrs.append(cidr)

    def is_allowed(self, target_ip: str) -> bool:
        target = ip_address(target_ip)
        for cidr in self.allowed_cidrs:
            if target in ip_network(cidr, strict=False):
                return True
        return False
