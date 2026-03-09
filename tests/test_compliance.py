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

from pathlib import Path

from nyxera_eye.audit.logger import AuditLogger
from nyxera_eye.compliance.opt_out_registry import OptOutRegistry
from nyxera_eye.compliance.runtime_mode import RuntimeMode, RuntimePolicy
from nyxera_eye.compliance.scope import ScopePolicy
from nyxera_eye.compliance.target_blacklist import TargetBlacklist
from nyxera_eye.ui.legal_banner import legal_banner_text


def test_runtime_policy_defaults_to_passive() -> None:
    policy = RuntimePolicy()
    assert policy.mode is RuntimeMode.PASSIVE
    assert policy.can_perform_intrusive_action("203.0.113.10") is False


def test_authorized_scope_allows_target_in_cidr() -> None:
    scope = ScopePolicy(allowed_cidrs=["203.0.113.0/24"])
    policy = RuntimePolicy(mode=RuntimeMode.AUTHORIZED_SCOPE, scope_policy=scope)
    assert policy.can_perform_intrusive_action("203.0.113.10") is True
    assert policy.can_perform_intrusive_action("198.51.100.10") is False


def test_target_blacklist() -> None:
    blacklist = TargetBlacklist()
    blacklist.add("Example.COM")
    assert blacklist.is_blocked("example.com") is True
    blacklist.remove("example.com")
    assert blacklist.is_blocked("example.com") is False


def test_opt_out_registry() -> None:
    registry = OptOutRegistry()
    registry.register("ASSET-001")
    assert registry.is_opted_out("asset-001") is True
    registry.unregister("asset-001")
    assert registry.is_opted_out("asset-001") is False


def test_audit_logger_writes_json_lines(tmp_path: Path) -> None:
    logfile = tmp_path / "audit" / "events.log"
    logger = AuditLogger(log_path=str(logfile))
    logger.log(actor="operator", action="probe", target="203.0.113.10", mode="authorized_scope")

    content = logfile.read_text(encoding="utf-8").strip()
    assert '"actor": "operator"' in content
    assert '"action": "probe"' in content


def test_legal_banner_contains_notice() -> None:
    banner = legal_banner_text()
    assert "Unauthorized access" in banner
    assert "authorized assessments" in banner
