# Copyright (c) 2026 NyxeraLabs
# Author: Jose Maria Micoli
# Licensed under BSL 1.1
# Change Date: 2033-02-17 -> Apache-2.0
#
# You may:
# - Study
# - Modify
# - Use for internal security testing
#
# You may NOT:
# - Offer as a commercial service
# - Sell derived competing products

import pytest

from nyxera_eye.security import APITokenStore, RateLimiter, decrypt_secret, encrypt_secret, role_allows


def test_rbac_hierarchy() -> None:
    assert role_allows("admin", "operator") is True
    assert role_allows("operator", "analyst") is True
    assert role_allows("viewer", "analyst") is False


def test_api_token_issue_verify_and_revoke() -> None:
    store = APITokenStore()
    token = store.issue_token(subject="alice", role="analyst")

    verified = store.verify(token)
    assert verified is not None
    assert verified.subject == "alice"
    assert verified.role == "analyst"

    assert store.revoke(token) is True
    assert store.verify(token) is None


def test_api_token_store_encrypted_export_and_load() -> None:
    store = APITokenStore()
    token = store.issue_token(subject="bob", role="operator")
    payload = store.export_encrypted(master_key="master-key")

    restored = APITokenStore()
    restored.load_encrypted(payload, master_key="master-key")
    assert restored.verify(token) is not None


def test_encrypted_secrets_detect_tampering() -> None:
    payload = encrypt_secret("secret-value", "key-1")
    assert decrypt_secret(payload, "key-1") == "secret-value"

    tampered = payload.replace("a", "b", 1)
    with pytest.raises(ValueError, match="integrity"):
        decrypt_secret(tampered, "key-1")


def test_rate_limiter_window() -> None:
    limiter = RateLimiter(max_requests=2, window_seconds=10)
    subject = "alice"

    assert limiter.allow(subject, now=100.0) is True
    assert limiter.allow(subject, now=101.0) is True
    assert limiter.allow(subject, now=105.0) is False
    assert limiter.allow(subject, now=111.0) is True
