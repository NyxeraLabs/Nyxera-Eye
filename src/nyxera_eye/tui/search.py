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


def search_as_you_type(query: str, records: list[dict[str, str]]) -> list[dict[str, str]]:
    needle = query.strip().lower()
    if not needle:
        return records

    result: list[dict[str, str]] = []
    for record in records:
        haystack = " ".join(str(value).lower() for value in record.values())
        if needle in haystack:
            result.append(record)
    return result
