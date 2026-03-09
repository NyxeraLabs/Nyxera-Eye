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

import base64


def murmurhash3_x86_32(data: bytes, seed: int = 0) -> int:
    c1 = 0xCC9E2D51
    c2 = 0x1B873593
    r1 = 15
    r2 = 13
    m = 5
    n = 0xE6546B64

    h = seed & 0xFFFFFFFF
    length = len(data)
    rounded_end = length & 0xFFFFFFFC

    for i in range(0, rounded_end, 4):
        k = int.from_bytes(data[i : i + 4], byteorder="little")
        k = (k * c1) & 0xFFFFFFFF
        k = ((k << r1) | (k >> (32 - r1))) & 0xFFFFFFFF
        k = (k * c2) & 0xFFFFFFFF

        h ^= k
        h = ((h << r2) | (h >> (32 - r2))) & 0xFFFFFFFF
        h = (h * m + n) & 0xFFFFFFFF

    k_tail = 0
    val = length & 0x03
    if val == 3:
        k_tail ^= data[rounded_end + 2] << 16
    if val >= 2:
        k_tail ^= data[rounded_end + 1] << 8
    if val >= 1:
        k_tail ^= data[rounded_end]
        k_tail = (k_tail * c1) & 0xFFFFFFFF
        k_tail = ((k_tail << r1) | (k_tail >> (32 - r1))) & 0xFFFFFFFF
        k_tail = (k_tail * c2) & 0xFFFFFFFF
        h ^= k_tail

    h ^= length
    h ^= h >> 16
    h = (h * 0x85EBCA6B) & 0xFFFFFFFF
    h ^= h >> 13
    h = (h * 0xC2B2AE35) & 0xFFFFFFFF
    h ^= h >> 16

    return h


def favicon_mmh3_from_bytes(raw: bytes) -> int:
    return murmurhash3_x86_32(raw)


def favicon_mmh3_from_base64(content_base64: str) -> int:
    raw = base64.b64decode(content_base64)
    return favicon_mmh3_from_bytes(raw)
