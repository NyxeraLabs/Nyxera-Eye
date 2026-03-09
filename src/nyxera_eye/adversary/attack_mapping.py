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


_ICS_TECHNIQUES: dict[str, list[str]] = {
    "modbus": ["T0859", "T0885"],
    "dnp3": ["T0802", "T0842"],
    "bacnet": ["T0814"],
    "mqtt": ["T0880"],
    "http": ["T1190"],
}


def map_protocols_to_attack_techniques(protocols: list[str]) -> list[str]:
    techniques: list[str] = []
    for proto in protocols:
        for technique in _ICS_TECHNIQUES.get(proto.lower(), []):
            if technique not in techniques:
                techniques.append(technique)
    return techniques
