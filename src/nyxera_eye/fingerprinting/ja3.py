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


def build_ja3_string(
    tls_version: int,
    ciphers: list[int],
    extensions: list[int],
    elliptic_curves: list[int],
    ec_point_formats: list[int],
) -> str:
    groups = [
        str(tls_version),
        "-".join(str(item) for item in ciphers),
        "-".join(str(item) for item in extensions),
        "-".join(str(item) for item in elliptic_curves),
        "-".join(str(item) for item in ec_point_formats),
    ]
    return ",".join(groups)


def ja3_hash(ja3_string: str) -> str:
    return hashlib.md5(ja3_string.encode("utf-8")).hexdigest()
