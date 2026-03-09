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


class MongoQueryInterface:
    def build_query(self, text: str) -> dict:
        text = text.strip()
        if not text:
            return {}

        if ":" in text:
            key, value = text.split(":", 1)
            return {key.strip(): value.strip()}

        return {"$text": {"$search": text}}
