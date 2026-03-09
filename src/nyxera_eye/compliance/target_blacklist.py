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
class TargetBlacklist:
    blocked_targets: set[str] = field(default_factory=set)

    def add(self, target: str) -> None:
        self.blocked_targets.add(target.strip().lower())

    def remove(self, target: str) -> None:
        self.blocked_targets.discard(target.strip().lower())

    def is_blocked(self, target: str) -> bool:
        return target.strip().lower() in self.blocked_targets
