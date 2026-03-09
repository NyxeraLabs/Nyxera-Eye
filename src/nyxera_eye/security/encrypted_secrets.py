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

import base64
import binascii
import hashlib
import hmac
import json
import secrets


def encrypt_secret(plaintext: str, key: str) -> str:
    key_bytes = _derive_key(key)
    nonce = secrets.token_bytes(16)
    encrypted = _xor_stream(plaintext.encode("utf-8"), key_bytes, nonce)
    mac = hmac.new(key_bytes, nonce + encrypted, hashlib.sha256).digest()
    payload = {
        "nonce": base64.b64encode(nonce).decode("ascii"),
        "ciphertext": base64.b64encode(encrypted).decode("ascii"),
        "mac": base64.b64encode(mac).decode("ascii"),
    }
    return json.dumps(payload, separators=(",", ":"), sort_keys=True)


def decrypt_secret(payload: str, key: str) -> str:
    key_bytes = _derive_key(key)
    try:
        parsed = json.loads(payload)
        nonce = base64.b64decode(parsed["nonce"])
        ciphertext = base64.b64decode(parsed["ciphertext"])
        provided_mac = base64.b64decode(parsed["mac"])
    except (json.JSONDecodeError, KeyError, TypeError, binascii.Error) as exc:
        raise ValueError("invalid secret payload integrity check") from exc
    expected_mac = hmac.new(key_bytes, nonce + ciphertext, hashlib.sha256).digest()
    if not hmac.compare_digest(provided_mac, expected_mac):
        raise ValueError("invalid secret payload integrity check")
    plaintext = _xor_stream(ciphertext, key_bytes, nonce)
    try:
        return plaintext.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("invalid secret payload integrity check") from exc


def _derive_key(key: str) -> bytes:
    return hashlib.sha256(key.encode("utf-8")).digest()


def _xor_stream(data: bytes, key: bytes, nonce: bytes) -> bytes:
    output = bytearray()
    counter = 0
    offset = 0

    while offset < len(data):
        block = hashlib.sha256(key + nonce + counter.to_bytes(8, "big")).digest()
        counter += 1
        for b in block:
            if offset >= len(data):
                break
            output.append(data[offset] ^ b)
            offset += 1
    return bytes(output)
