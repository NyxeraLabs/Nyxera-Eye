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

from dataclasses import dataclass
import hashlib
import json
import secrets

from nyxera_eye.security.encrypted_secrets import decrypt_secret, encrypt_secret


@dataclass(slots=True)
class TokenRecord:
    subject: str
    role: str
    token_hash: str
    active: bool = True


class APITokenStore:
    def __init__(self) -> None:
        self._records_by_hash: dict[str, TokenRecord] = {}

    def issue_token(self, subject: str, role: str) -> str:
        token = secrets.token_urlsafe(32)
        self.add_token(token=token, subject=subject, role=role)
        return token

    def add_token(self, token: str, subject: str, role: str) -> None:
        token_hash = self._hash_token(token)
        self._records_by_hash[token_hash] = TokenRecord(subject=subject, role=role, token_hash=token_hash)

    def verify(self, token: str) -> TokenRecord | None:
        token_hash = self._hash_token(token)
        record = self._records_by_hash.get(token_hash)
        if record is None or not record.active:
            return None
        return record

    def revoke(self, token: str) -> bool:
        token_hash = self._hash_token(token)
        record = self._records_by_hash.get(token_hash)
        if record is None:
            return False
        record.active = False
        return True

    def export_encrypted(self, master_key: str) -> str:
        data = [
            {
                "subject": record.subject,
                "role": record.role,
                "token_hash": record.token_hash,
                "active": record.active,
            }
            for record in self._records_by_hash.values()
        ]
        serialized = json.dumps(data, separators=(",", ":"), sort_keys=True)
        return encrypt_secret(serialized, master_key)

    def load_encrypted(self, payload: str, master_key: str) -> None:
        serialized = decrypt_secret(payload, master_key)
        data = json.loads(serialized)
        restored: dict[str, TokenRecord] = {}
        for item in data:
            token_hash = str(item["token_hash"])
            restored[token_hash] = TokenRecord(
                subject=str(item["subject"]),
                role=str(item["role"]),
                token_hash=token_hash,
                active=bool(item.get("active", True)),
            )
        self._records_by_hash = restored

    @staticmethod
    def _hash_token(token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()
