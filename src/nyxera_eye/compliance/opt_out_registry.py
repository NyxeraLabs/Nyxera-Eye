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


@dataclass(slots=True)
class OptOutRegistry:
    opted_out_assets: set[str] = field(default_factory=set)

    def register(self, asset_identifier: str) -> None:
        self.opted_out_assets.add(asset_identifier.strip().lower())

    def unregister(self, asset_identifier: str) -> None:
        self.opted_out_assets.discard(asset_identifier.strip().lower())

    def is_opted_out(self, asset_identifier: str) -> bool:
        return asset_identifier.strip().lower() in self.opted_out_assets
