from __future__ import annotations

# Copyright (c) 2026 NyxeraLabs
# Author: Jose Maria Micoli
# Licensed under BSL 1.1
# Change Date: 2033-02-17 -> Apache-2.0

from dataclasses import dataclass
import hashlib
import secrets

from nyxera_eye.security.rbac import ROLE_PRIORITY


@dataclass(slots=True)
class UserRecord:
    username: str
    password_salt: str
    password_hash: str
    role: str
    active: bool = True


class AuthRuntimeStore:
    def __init__(self) -> None:
        self._users: dict[str, UserRecord] = {}

    def register(self, username: str, password: str, role: str = "analyst") -> UserRecord:
        normalized = username.strip().lower()
        if not normalized:
            raise ValueError("username is required")
        if normalized in self._users:
            raise ValueError("username already exists")
        if len(password) < 10:
            raise ValueError("password must be at least 10 characters")
        if role not in ROLE_PRIORITY:
            raise ValueError("invalid role")

        salt = secrets.token_hex(16)
        password_hash = self._hash_password(password=password, salt=salt)
        record = UserRecord(username=normalized, password_salt=salt, password_hash=password_hash, role=role)
        self._users[normalized] = record
        return record

    def authenticate(self, username: str, password: str) -> UserRecord | None:
        normalized = username.strip().lower()
        record = self._users.get(normalized)
        if record is None or not record.active:
            return None
        expected = self._hash_password(password=password, salt=record.password_salt)
        if not secrets.compare_digest(expected, record.password_hash):
            return None
        return record

    def get_user(self, username: str) -> UserRecord | None:
        return self._users.get(username.strip().lower())

    def ensure_admin(self, username: str, password: str) -> None:
        normalized = username.strip().lower()
        existing = self._users.get(normalized)
        if existing is not None:
            return
        self.register(username=normalized, password=password, role="admin")

    @staticmethod
    def _hash_password(password: str, salt: str) -> str:
        digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            160_000,
            dklen=32,
        )
        return digest.hex()


auth_runtime_store = AuthRuntimeStore()
