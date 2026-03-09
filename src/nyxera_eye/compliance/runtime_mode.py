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
from enum import StrEnum

from nyxera_eye.compliance.scope import ScopePolicy


class RuntimeMode(StrEnum):
    PASSIVE = "passive"
    AUTHORIZED_SCOPE = "authorized_scope"


@dataclass(slots=True)
class RuntimePolicy:
    mode: RuntimeMode = RuntimeMode.PASSIVE
    scope_policy: ScopePolicy = field(default_factory=ScopePolicy)

    def can_perform_intrusive_action(self, target_ip: str) -> bool:
        if self.mode is RuntimeMode.PASSIVE:
            return False
        return self.scope_policy.is_allowed(target_ip)
