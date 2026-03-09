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

from dataclasses import dataclass


@dataclass(slots=True)
class SNMPMetadata:
    ip: str
    sys_name: str | None
    sys_descr: str | None
    sys_contact: str | None


class SNMPMetadataExtractor:
    def __init__(self, timeout_seconds: float = 12.0, safe_mode: bool = True) -> None:
        self.timeout_seconds = timeout_seconds
        self.safe_mode = safe_mode

    def extract_from_walk(self, ip: str, mib_values: dict[str, str]) -> SNMPMetadata:
        if not self.safe_mode:
            raise ValueError("unsafe SNMP mode is disabled by policy")

        return SNMPMetadata(
            ip=ip,
            sys_name=mib_values.get("1.3.6.1.2.1.1.5.0"),
            sys_descr=mib_values.get("1.3.6.1.2.1.1.1.0"),
            sys_contact=mib_values.get("1.3.6.1.2.1.1.4.0"),
        )
